from __future__ import annotations

import os
import sys
from datetime import datetime

from PyQt6.QtCore import QThread, QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QFont, QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QApplication, QFileDialog, QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPlainTextEdit, QProgressBar, QPushButton,
    QScrollArea, QSizePolicy, QVBoxLayout, QWidget
)

from ..config import load_settings
from ..core import JarvisCore
from ..llm import LLMError, OllamaProvider
from ..memory import MemoryRepository
from ..tools import default_tools
from ..runtime.state import JarvisState
from .facial_avatar import FacetedAvatar


try:
    import psutil
except ImportError:  # optional UI telemetry
    psutil = None


CYAN = "#00e5e5"
TEXT = "#b9f9f5"
MUTED = "#5c9ca4"
BG = "#020a0d"
PANEL = "#031216"
BORDER = "#07505a"
GREEN = "#00ff88"
RED = "#ff315e"
YELLOW = "#ffd21a"


class ChatWorker(QThread):
    chunk = pyqtSignal(str)
    done = pyqtSignal()
    failed = pyqtSignal(str)

    def __init__(self, core, text):
        super().__init__()
        self.core = core
        self.text = text

    def run(self):
        try:
            for part in self.core.stream_chat(self.text):
                self.chunk.emit(part)
            self.done.emit()
        except Exception as exc:
            self.failed.emit(str(exc))


class TelemetryCard(QFrame):
    def __init__(self, title: str, value: str = "--", suffix: str = ""):
        super().__init__()
        self.setObjectName("telemetryCard")
        box = QVBoxLayout(self)
        box.setContentsMargins(9, 7, 9, 7)
        top = QHBoxLayout()
        self.title = QLabel(title)
        self.value = QLabel(value + suffix)
        top.addWidget(self.title)
        top.addStretch()
        top.addWidget(self.value)
        box.addLayout(top)
        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        self.bar.setValue(0)
        self.bar.setTextVisible(False)
        self.bar.setFixedHeight(5)
        box.addWidget(self.bar)

    def set_value(self, value: float, suffix: str = "%"):
        v = max(0, min(100, int(value)))
        self.value.setText(f"{v}{suffix}")
        self.bar.setValue(v)


class Section(QFrame):
    def __init__(self, title: str):
        super().__init__()
        self.setObjectName("section")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(9, 8, 9, 9)
        self.layout.setSpacing(7)
        head = QLabel("◆  " + title.upper())
        head.setObjectName("sectionTitle")
        self.layout.addWidget(head)


class ControlButton(QPushButton):
    def __init__(self, text: str, callback=None, accent=False):
        super().__init__(text)
        self.setObjectName("controlButtonAccent" if accent else "controlButton")
        self.setMinimumHeight(30)
        if callback:
            self.clicked.connect(callback)


class DesktopJARVIS(QMainWindow):
    """Ambient, panel-driven JARVIS HUD.

    This is an original implementation inspired by the interaction density of
    modern sci-fi assistant dashboards. Business logic remains in the core;
    this class is presentation and user-input orchestration only.
    """

    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        self.provider = OllamaProvider(
            self.settings.ollama_base_url,
            self.settings.ollama_model,
            self.settings.ollama_timeout,
        )
        self.core = JarvisCore(
            self.settings,
            self.provider,
            MemoryRepository(self.settings.db_path),
            default_tools(self.settings.workspace),
        )
        self.worker = None
        self.muted = False
        self.listening = True
        self._fullscreen = False
        self._build_window()
        self._build_ui()
        self._start_timers()
        self._log("SYS", "JARVIS HUD initialized • local-first mode")
        self._log("SYS", f"Ollama: {self.settings.ollama_base_url}")
        self._log("SYS", f"Model: {self.settings.ollama_model}")

    def _build_window(self):
        self.setWindowTitle("JARVIS • Local Ambient Intelligence")
        self.resize(1600, 900)
        self.setMinimumSize(1180, 720)
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background: {BG};
                color: {TEXT};
                font-family: 'Consolas', 'Cascadia Mono', monospace;
                font-size: 11px;
            }}
            QFrame#panel, QFrame#section, QFrame#telemetryCard {{
                background: {PANEL};
                border: 1px solid {BORDER};
            }}
            QFrame#section {{ border-radius: 2px; }}
            QFrame#telemetryCard {{ border-radius: 4px; }}
            QLabel#brand {{
                color: {CYAN};
                font-size: 23px;
                font-weight: 700;
                letter-spacing: 3px;
            }}
            QLabel#subbrand, QLabel#sectionTitle, QLabel#footer {{
                color: {MUTED};
            }}
            QLabel#sectionTitle {{
                color: {CYAN};
                font-size: 10px;
            }}
            QLabel#state {{
                color: #9dfff5;
                font-size: 15px;
                font-weight: 700;
                letter-spacing: 2px;
            }}
            QLabel#telemetryCard QLabel {{
                color: {MUTED};
                font-size: 9px;
            }}
            QProgressBar {{
                background: #02181c;
                border: 0;
                border-radius: 2px;
            }}
            QProgressBar::chunk {{ background: {CYAN}; border-radius: 2px; }}
            QPushButton {{
                color: {TEXT};
                background: #031b21;
                border: 1px solid #0a5961;
                border-radius: 2px;
                padding: 7px 9px;
            }}
            QPushButton:hover {{ background: #06313a; color: white; }}
            QPushButton#controlButtonAccent {{
                color: #06100e;
                background: {GREEN};
                border-color: {GREEN};
                font-weight: 700;
            }}
            QLineEdit, QPlainTextEdit {{
                background: #02080b;
                color: {TEXT};
                border: 1px solid #0a4c54;
                border-radius: 2px;
                selection-background-color: #075c64;
                padding: 7px;
            }}
            QPlainTextEdit#activity {{
                font-size: 10px;
            }}
            QScrollArea {{
                border: 0;
                background: transparent;
            }}
        """)

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(10, 6, 10, 7)
        outer.setSpacing(5)

        # Header
        header = QHBoxLayout()
        mark = QLabel("JARVIS")
        mark.setObjectName("brand")
        header.addWidget(QLabel("JARVIS LOCAL"))
        header.itemAt(0).widget().setStyleSheet(f"color:{MUTED}; font-size:10px;")
        header.addStretch()
        header.addWidget(mark)
        header.addStretch()
        self.clock = QLabel()
        self.clock.setStyleSheet(f"color:{CYAN}; font-size:17px; font-weight:700;")
        header.addWidget(self.clock)
        outer.addLayout(header)

        subtitle = QLabel("JUST A RATHER VERY INTELLIGENT SYSTEM")
        subtitle.setObjectName("subbrand")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(subtitle)

        body = QHBoxLayout()
        body.setSpacing(5)
        outer.addLayout(body, 1)

        # LEFT CONTROL COLUMN
        left = QFrame()
        left.setObjectName("panel")
        left.setFixedWidth(245)
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(9, 8, 9, 8)
        left_layout.setSpacing(6)

        controls = Section("Controls")
        left_layout.addWidget(controls)
        controls.layout.addWidget(ControlButton("◉  REMOTE CONTROL", self._remote_info, True))
        controls.layout.addWidget(ControlButton("◌  FULLSCREEN  [F11]", self.toggle_fullscreen))
        controls.layout.addWidget(ControlButton("▣  FILE / FOLDER", self._choose_file))
        self.autostart_btn = ControlButton("□  AUTO-START: OFF", self._toggle_autostart)
        controls.layout.addWidget(self.autostart_btn)
        controls.layout.addWidget(ControlButton("⚙  CUSTOMIZE ASSISTANT", self._customize))
        self.brief_btn = ControlButton("✦  MORNING BRIEF: ON", self._toggle_brief, True)
        controls.layout.addWidget(self.brief_btn)
        self.wake_btn = ControlButton("◈  WAKE WORD: ON", self._toggle_wake, True)
        controls.layout.addWidget(self.wake_btn)
        controls.layout.addWidget(ControlButton("◉  SLEEP NOW", self.sleep_now))
        self.ptt_btn = ControlButton("▣  PUSH-TO-TALK: OFF", self._toggle_ptt)
        controls.layout.addWidget(self.ptt_btn)
        controls.layout.addWidget(ControlButton("◉  HUD: FACETED FACE", self._avatar_info))
        controls.layout.addWidget(ControlButton("♧  AUDIO DEVICES", self._audio_info))
        controls.layout.addWidget(ControlButton("▣  MEMORY", lambda: self.panel("MEMORY")))
        controls.layout.addWidget(ControlButton("✣  PLUGINS", lambda: self.panel("TOOLS")))
        controls.layout.addWidget(ControlButton("⚙  PLUGIN SETTINGS", lambda: self.panel("SYSTEM")))

        left_layout.addStretch()

        self.ai_core = QLabel("AI CORE\nACTIVE")
        self.ai_core.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ai_core.setStyleSheet(f"color:{GREEN}; border:1px solid #08734e; padding:8px;")
        left_layout.addWidget(self.ai_core)
        self.security = QLabel("SEC\nCLEARED")
        self.security.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.security.setStyleSheet(f"color:{GREEN}; border:1px solid #08734e; padding:8px;")
        left_layout.addWidget(self.security)
        self.protocol = QLabel("PROTOCOL\nLOCAL")
        self.protocol.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.protocol.setStyleSheet(f"color:{CYAN}; border:1px solid {BORDER}; padding:8px;")
        left_layout.addWidget(self.protocol)
        body.addWidget(left)

        # CENTER
        center = QVBoxLayout()
        center.setSpacing(4)
        body.addLayout(center, 1)

        center_top = QHBoxLayout()
        self.center_state = QLabel("●  LISTENING")
        self.center_state.setObjectName("state")
        center_top.addStretch()
        center_top.addWidget(self.center_state)
        center_top.addStretch()
        center.addLayout(center_top)

        self.avatar = FacetedAvatar()
        center.addWidget(self.avatar, 1, Qt.AlignmentFlag.AlignCenter)

        self.wave = QLabel("▁▂▃▂▁▂▅▇▅▂▁▂▃▅▃▂▁▂▅▇▅▂▁")
        self.wave.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.wave.setStyleSheet(f"color:{CYAN}; font-size:13px;")
        center.addWidget(self.wave)

        # NEWS / CONTENT PANEL
        news = Section("News — local information surface")
        self.news = QPlainTextEdit()
        self.news.setReadOnly(True)
        self.news.setMaximumHeight(190)
        self.news.setPlainText(
            "JARVIS CONTENT CHANNEL\n\n"
            "Web/news tools are available through the local tool router.\n"
            "No external service is required for the core assistant.\n\n"
            "Use the command field below to ask JARVIS to search, inspect, "
            "summarize or execute an approved task."
        )
        news.layout.addWidget(self.news)
        center.addWidget(news)

        # RIGHT COLUMN
        right = QFrame()
        right.setObjectName("panel")
        right.setFixedWidth(345)
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(9, 8, 9, 8)
        right_layout.setSpacing(7)

        activity = Section("Activity Log")
        self.activity = QPlainTextEdit()
        self.activity.setObjectName("activity")
        self.activity.setReadOnly(True)
        activity.layout.addWidget(self.activity)
        right_layout.addWidget(activity, 1)

        upload = Section("File Upload")
        upload_label = QLabel("↑\nDrop a file here or click to browse\n\nImages · Video · Audio · PDF · Docs · Code")
        upload_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        upload_label.setStyleSheet(f"color:{CYAN}; border:1px dashed #0b5962; padding:18px;")
        upload_label.mousePressEvent = lambda event: self._choose_file()
        upload.layout.addWidget(upload_label)
        self.file_status = QLabel("No file loaded")
        self.file_status.setStyleSheet(f"color:{MUTED};")
        upload.layout.addWidget(self.file_status)
        right_layout.addWidget(upload)

        command = Section("Command Input")
        row = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Escribe una orden para JARVIS…")
        self.input.returnPressed.connect(self.send)
        row.addWidget(self.input, 1)
        send = QPushButton("▶")
        send.clicked.connect(self.send)
        send.setFixedWidth(42)
        row.addWidget(send)
        command.layout.addLayout(row)

        interrupt = QPushButton("◉  INTERRUPT   [ESC]")
        interrupt.setStyleSheet(f"color:{RED}; border:1px solid {RED};")
        interrupt.clicked.connect(self.interrupt)
        command.layout.addWidget(interrupt)

        self.mic_button = QPushButton("♟  MICROPHONE ACTIVE")
        self.mic_button.setStyleSheet(f"color:{GREEN}; border:1px solid #08734e;")
        self.mic_button.clicked.connect(self._toggle_mic)
        command.layout.addWidget(self.mic_button)
        right_layout.addWidget(command)

        body.addWidget(right)

        footer = QLabel("[F4] Mute     [F11] Fullscreen     •     OLLAMA / LOCAL-FIRST / POLICY-GATED")
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(footer)

        self.esc = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        self.esc.activated.connect(self.interrupt)
        self.f11 = QShortcut(QKeySequence(Qt.Key.Key_F11), self)
        self.f11.activated.connect(self.toggle_fullscreen)

    def _start_timers(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(1000)
        self._tick()

        self.wave_timer = QTimer(self)
        self.wave_timer.timeout.connect(self._animate_wave)
        self.wave_timer.start(140)

    def _tick(self):
        now = datetime.now()
        self.clock.setText(now.strftime("%H:%M:%S"))
        if psutil:
            try:
                cpu = psutil.cpu_percent(interval=None)
                mem = psutil.virtual_memory().percent
                self._set_telemetry_text(cpu, mem)
            except Exception:
                pass

    def _set_telemetry_text(self, cpu, mem):
        # Keep telemetry compact in the activity stream so the HUD remains stable.
        self._last_cpu, self._last_mem = cpu, mem

    def _animate_wave(self):
        if self.worker and self.worker.isRunning():
            self.wave.setText("▁▃▅▇▆▃▅▇▅▃▁▂▆▇▅▂▁▃▆▇▅▂▁")
        elif self.listening:
            self.wave.setText("▁▂▃▂▁▂▅▇▅▂▁▂▃▅▃▂▁▂▅▇▅▂▁")
        else:
            self.wave.setText("▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁")

    def _log(self, source: str, message: str):
        stamp = datetime.now().strftime("%H:%M:%S")
        self.activity.appendPlainText(f"[{stamp}] [{source}] {message}")
        self.activity.ensureCursorVisible()

    def send(self):
        text = self.input.text().strip()
        if not text or (self.worker and self.worker.isRunning()):
            return
        self.input.clear()
        self._log("USER", text)
        self._log("JARVIS", "")
        self.center_state.setText("●  THINKING")
        self.avatar.set_state("THINKING")
        self.ai_core.setText("AI CORE\nTHINKING")
        self.worker = ChatWorker(self.core, text)
        self.worker.chunk.connect(self._chunk)
        self.worker.done.connect(self._done)
        self.worker.failed.connect(self._failed)
        self.worker.start()

    def _chunk(self, chunk: str):
        self.activity.moveCursor(self.activity.textCursor().MoveOperation.End)
        self.activity.insertPlainText(chunk)
        self.activity.ensureCursorVisible()
        self.avatar.set_level(min(1.0, 0.25 + len(chunk) / 300.0))

    def _done(self):
        self.activity.appendPlainText("\n")
        self.center_state.setText("●  LISTENING" if self.listening else "○  SLEEPING")
        self.avatar.set_state("LISTENING" if self.listening else "SLEEPING")
        self.avatar.set_level(0.3)
        self.ai_core.setText("AI CORE\nACTIVE")

    def _failed(self, error: str):
        self._log("ERROR", error)
        self.center_state.setText("●  ERROR")
        self.avatar.set_state("ERROR")
        self.ai_core.setText("AI CORE\nERROR")

    def interrupt(self):
        if self.worker and self.worker.isRunning():
            self._log("SYS", "Interrupt requested.")
            self.worker.requestInterruption()
        self.center_state.setText("●  LISTENING")
        self.avatar.set_state("LISTENING")

    def toggle_fullscreen(self):
        self._fullscreen = not self._fullscreen
        self.showFullScreen() if self._fullscreen else self.showNormal()

    def sleep_now(self):
        self.listening = False
        self.center_state.setText("○  SLEEPING")
        self.avatar.set_state("SLEEPING")
        self.wake_btn.setText("◈  WAKE WORD: OFF")
        self.wake_btn.setObjectName("controlButton")
        self.wake_btn.setStyle(self.wake_btn.style())
        self._log("SYS", "Sleeping — no active speech input.")

    def _toggle_wake(self):
        self.listening = not self.listening
        self.wake_btn.setText(f"◈  WAKE WORD: {'ON' if self.listening else 'OFF'}")
        self.center_state.setText("●  LISTENING" if self.listening else "○  SLEEPING")
        self.avatar.set_state("LISTENING" if self.listening else "SLEEPING")
        self._log("SYS", f"Wake-word UI state: {'ON' if self.listening else 'OFF'}")

    def _toggle_mic(self):
        self.muted = not self.muted
        self.mic_button.setText("♟  MICROPHONE MUTED" if self.muted else "♟  MICROPHONE ACTIVE")
        self.mic_button.setStyleSheet(
            f"color:{RED}; border:1px solid {RED};" if self.muted
            else f"color:{GREEN}; border:1px solid #08734e;"
        )
        self._log("SYS", f"Microphone indicator: {'muted' if self.muted else 'active'}")

    def _toggle_ptt(self):
        text = "ON" if "OFF" in self.ptt_btn.text() else "OFF"
        self.ptt_btn.setText(f"▣  PUSH-TO-TALK: {text}")
        self._log("SYS", f"Push-to-talk UI mode: {text}")

    def _toggle_brief(self):
        enabled = "OFF" in self.brief_btn.text()
        self.brief_btn.setText(f"✦  MORNING BRIEF: {'ON' if enabled else 'OFF'}")
        self._log("SYS", f"Morning briefing: {'enabled' if enabled else 'disabled'}")

    def _toggle_autostart(self):
        enabled = "OFF" in self.autostart_btn.text()
        self.autostart_btn.setText(f"□  AUTO-START: {'ON' if enabled else 'OFF'}")
        self._log("SYS", f"Auto-start UI state: {'enabled' if enabled else 'disabled'}")

    def _choose_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select file for JARVIS")
        if path:
            self.file_status.setText(os.path.basename(path))
            self._log("FILE", f"Selected: {path}")

    def _remote_info(self):
        self._log("REMOTE", "Remote gateway is permission-gated and remains disabled until configured.")

    def _customize(self):
        self._log("UI", "Customization surface selected. Core settings remain centralized in .env/config.")

    def _avatar_info(self):
        self._log("UI", "Original procedural faceted avatar active.")

    def _audio_info(self):
        self._log("AUDIO", "Audio-device abstraction is available; install local voice extras to activate hardware I/O.")

    def panel(self, name: str):
        if name == "MEMORY":
            self._log("MEMORY", "Persistent local memory repository is attached to the core.")
        elif name == "TOOLS":
            try:
                names = [x["name"] for x in self.core.tools.definitions()]
                self._log("TOOLS", "Registered: " + ", ".join(names))
            except Exception as exc:
                self._log("TOOLS", str(exc))
        else:
            self._log("SYSTEM", f"Provider={self.settings.llm_provider} | Ollama={self.settings.ollama_base_url}")

    def closeEvent(self, event):
        if self.worker and self.worker.isRunning():
            self.worker.requestInterruption()
            self.worker.wait(1000)
        event.accept()


def launch_desktop():
    app = QApplication.instance() or QApplication(sys.argv)
    win = DesktopJARVIS()
    win.show()
    return app.exec()
