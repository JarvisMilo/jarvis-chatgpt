from __future__ import annotations
import sys
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QPlainTextEdit, QVBoxLayout, QWidget, QFrame
from ..config import load_settings
from ..core import JarvisCore
from ..llm import OllamaProvider, LLMError
from ..memory import MemoryRepository
from ..tools import default_tools
from .ambient import ReactorWidget

class ChatWorker(QThread):
    chunk=pyqtSignal(str); done=pyqtSignal(); failed=pyqtSignal(str)
    def __init__(self,core,text): super().__init__(); self.core=core; self.text=text
    def run(self):
        try:
            for part in self.core.stream_chat(self.text): self.chunk.emit(part)
            self.done.emit()
        except Exception as exc: self.failed.emit(str(exc))

class DesktopJARVIS(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle("JARVIS • Local Intelligence"); self.resize(1280,820)
        self.setStyleSheet("QMainWindow{background:#05090f;} QWidget{color:#dff7ff;font-family:'Segoe UI';} QFrame{background:#08121b;border:1px solid #17354b;border-radius:14px;} QLineEdit,QPlainTextEdit{background:#050b12;border:1px solid #1b4359;border-radius:10px;color:#e9fbff;padding:10px;} QPushButton{background:#0b2533;border:1px solid #24566d;border-radius:9px;color:#dff7ff;padding:9px 14px;} QPushButton:hover{background:#10384a;}")
        self.settings=load_settings(); provider=OllamaProvider(self.settings.ollama_base_url,self.settings.ollama_model,self.settings.ollama_timeout)
        self.core=JarvisCore(self.settings,provider,MemoryRepository(self.settings.db_path),default_tools(self.settings.workspace)); self.worker=None
        root=QWidget(); self.setCentralWidget(root); main=QHBoxLayout(root); main.setContentsMargins(18,18,18,18)
        left=QFrame(); ll=QVBoxLayout(left); title=QLabel("JARVIS"); title.setFont(QFont("Segoe UI",26,QFont.Weight.Bold)); ll.addWidget(title)
        sub=QLabel("LOCAL INTELLIGENCE • OLLAMA"); sub.setStyleSheet("color:#78b9ce;"); ll.addWidget(sub)
        self.reactor=ReactorWidget(); ll.addWidget(self.reactor,1,Qt.AlignmentFlag.AlignCenter)
        self.status=QLabel("READY / SLEEPING"); self.status.setAlignment(Qt.AlignmentFlag.AlignCenter); ll.addWidget(self.status)
        self.telemetry=QLabel(f"Provider: Ollama\\nModel: {self.settings.ollama_model}\\nWorkspace: {self.settings.workspace}"); self.telemetry.setStyleSheet("color:#80a7b5;"); ll.addWidget(self.telemetry)
        main.addWidget(left,1)
        right=QFrame(); rl=QVBoxLayout(right); rl.addWidget(QLabel("CONVERSATION"))
        self.output=QPlainTextEdit(); self.output.setReadOnly(True); rl.addWidget(self.output,1)
        row=QHBoxLayout(); self.input=QLineEdit(); self.input.setPlaceholderText("Habla con JARVIS…"); self.input.returnPressed.connect(self.send); row.addWidget(self.input,1)
        self.send_button=QPushButton("SEND"); self.send_button.clicked.connect(self.send); row.addWidget(self.send_button); rl.addLayout(row)
        buttons=QHBoxLayout()
        for label in ("MEMORY","TOOLS","SYSTEM","SETTINGS"):
            b=QPushButton(label); b.clicked.connect(lambda checked=False,x=label:self.panel(x)); buttons.addWidget(b)
        rl.addLayout(buttons); main.addWidget(right,2)
    def panel(self,name):
        if name=="MEMORY": self.output.appendPlainText("[MEMORY] Local persistent memory is active.")
        elif name=="TOOLS": self.output.appendPlainText("[TOOLS]\\n"+"\\n".join(x["name"] for x in self.core.tools.definitions()))
        elif name=="SYSTEM": self.output.appendPlainText("[SYSTEM] Provider="+self.settings.llm_provider+" | Ollama="+self.settings.ollama_base_url)
        else: self.output.appendPlainText("[SETTINGS] Configuration is read from .env / central Settings.")
    def send(self):
        text=self.input.text().strip()
        if not text or self.worker and self.worker.isRunning(): return
        self.input.clear(); self.output.appendPlainText("YOU  › "+text); self.output.appendPlainText("JARVIS › "); self.status.setText("THINKING"); self.reactor.set_state(__import__('jarvis.runtime.state',fromlist=['JarvisState']).JarvisState.THINKING)
        self.worker=ChatWorker(self.core,text); self.worker.chunk.connect(self._chunk); self.worker.done.connect(self._done); self.worker.failed.connect(self._failed); self.worker.start()
    def _chunk(self,s): self.output.moveCursor(self.output.textCursor().MoveOperation.End); self.output.insertPlainText(s); self.output.ensureCursorVisible()
    def _done(self): self.output.appendPlainText("\\n"); self.status.setText("READY"); self.reactor.set_state(__import__('jarvis.runtime.state',fromlist=['JarvisState']).JarvisState.SUCCESS)
    def _failed(self,e): self.output.appendPlainText("\\n[ERROR] "+e); self.status.setText("ERROR"); self.reactor.set_state(__import__('jarvis.runtime.state',fromlist=['JarvisState']).JarvisState.ERROR)

def launch_desktop():
    app=QApplication.instance() or QApplication(sys.argv); win=DesktopJARVIS(); win.show(); return app.exec()
