from __future__ import annotations
import math, sys
from datetime import datetime
from PyQt6.QtCore import Qt, QTimer, QRectF
from PyQt6.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from ..runtime.state import JarvisState

class ReactorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent); self.phase=0.0; self.state=JarvisState.SLEEPING; self.level=.25; self.setMinimumSize(360,360)
        timer=QTimer(self); timer.timeout.connect(self._tick); timer.start(33)
    def _tick(self): self.phase += .055; self.update()
    def set_state(self,state): self.state=state; self.update()
    def paintEvent(self,event):
        p=QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing); c=self.rect().center(); base=min(self.width(),self.height())*.38
        color=QColor(90,210,255)
        if self.state in {JarvisState.ERROR,JarvisState.RECOVERING}: color=QColor(255,105,105)
        elif self.state in {JarvisState.EXECUTING,JarvisState.THINKING,JarvisState.PLANNING}: color=QColor(150,235,255)
        for i,scale in enumerate((1,.86,.72)):
            pen=QPen(QColor(color.red(),color.green(),color.blue(),35+i*25),2+i); p.setPen(pen)
            r=base*scale+math.sin(self.phase*2+i)*5; p.drawEllipse(QRectF(c.x()-r,c.y()-r,r*2,r*2))
        core=base*.36+12*self.level; p.setPen(Qt.PenStyle.NoPen); p.setBrush(QBrush(QColor(color.red(),color.green(),color.blue(),170)))
        p.drawEllipse(QRectF(c.x()-core,c.y()-core,core*2,core*2)); p.setBrush(QBrush(QColor(225,250,255,220)))
        p.drawEllipse(QRectF(c.x()-core*.42,c.y()-core*.42,core*.84,core*.84))
        p.setPen(QPen(QColor(190,240,255,150),1))
        for n in range(24):
            a=self.phase+n*math.pi*2/24; rr=base*.96; x=c.x()+math.cos(a)*rr; y=c.y()+math.sin(a)*rr
            p.drawLine(int(x),int(y),int(x-math.cos(a)*8),int(y-math.sin(a)*8))

class AmbientHUD(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle("JARVIS"); self.setMinimumSize(1100,760)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground); self.setWindowFlags(Qt.WindowType.FramelessWindowHint|Qt.WindowType.Window)
        root=QWidget(); root.setObjectName("root"); root.setStyleSheet("#root{background:#05090f;border:1px solid #17354b;border-radius:22px;} QLabel{color:#dff7ff;font-family:'Segoe UI';}")
        self.setCentralWidget(root); layout=QVBoxLayout(root); layout.setContentsMargins(34,24,34,28); layout.setSpacing(10)
        top=QLabel("J A R V I S   •   LOCAL INTELLIGENCE"); top.setFont(QFont("Segoe UI",12,QFont.Weight.DemiBold)); layout.addWidget(top)
        self.reactor=ReactorWidget(); layout.addWidget(self.reactor,1,Qt.AlignmentFlag.AlignCenter)
        self.state=QLabel("SLEEPING"); self.state.setAlignment(Qt.AlignmentFlag.AlignCenter); self.state.setFont(QFont("Segoe UI",20,QFont.Weight.Bold)); layout.addWidget(self.state)
        self.message=QLabel("Awaiting command."); self.message.setAlignment(Qt.AlignmentFlag.AlignCenter); self.message.setWordWrap(True); self.message.setFont(QFont("Segoe UI",13)); layout.addWidget(self.message)
        self.activity=QLabel("SYSTEM  •  OLLAMA  •  LOCAL-FIRST  •  "+datetime.now().strftime("%H:%M")); self.activity.setAlignment(Qt.AlignmentFlag.AlignCenter); self.activity.setStyleSheet("color:#83b7c9;"); layout.addWidget(self.activity)
        self._drag_pos=None
    def set_state(self,state): self.state.setText(state.value); self.reactor.set_state(state)
    def set_message(self,message): self.message.setText(message)
    def mousePressEvent(self,event):
        if event.button()==Qt.MouseButton.LeftButton: self._drag_pos=event.globalPosition().toPoint()-self.frameGeometry().topLeft()
    def mouseMoveEvent(self,event):
        if self._drag_pos is not None and event.buttons()&Qt.MouseButton.LeftButton: self.move(event.globalPosition().toPoint()-self._drag_pos)
    def mouseReleaseEvent(self,event): self._drag_pos=None

def launch_hud():
    app=QApplication.instance() or QApplication(sys.argv); hud=AmbientHUD(); hud.show(); return app.exec()
