from __future__ import annotations
import math
from PyQt6.QtCore import QTimer, QRectF, Qt
from PyQt6.QtGui import QColor, QPainter, QPen, QPolygonF
from PyQt6.QtWidgets import QWidget


class FacetedAvatar(QWidget):
    """Original procedural faceted face used as JARVIS visual status surface."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.phase = 0.0
        self.state = "LISTENING"
        self.level = 0.35
        self.setMinimumSize(420, 430)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        timer = QTimer(self)
        timer.timeout.connect(self._tick)
        timer.start(33)

    def set_state(self, state: str):
        self.state = str(state)
        self.update()

    def set_level(self, level: float):
        self.level = max(0.0, min(1.0, float(level)))
        self.update()

    def _tick(self):
        self.phase += 0.045
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        cx, cy = self.width() * 0.5, self.height() * 0.47
        scale = min(self.width() / 560.0, self.height() / 540.0)
        rx, ry = 160 * scale, 205 * scale

        # Ambient field.
        for r, alpha in ((240, 16), (215, 12), (190, 9)):
            p.setPen(QPen(QColor(0, 220, 225, alpha), 1))
            p.drawEllipse(QRectF(cx-r*scale, cy-r*scale, 2*r*scale, 2*r*scale))

        # Neck and shoulders.
        neck = QPolygonF([
            (cx-rx*.34, cy+ry*.70), (cx-rx*.18, cy+ry*1.02),
            (cx+rx*.18, cy+ry*1.02), (cx+rx*.34, cy+ry*.70)
        ])
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(10, 155, 160, 125))
        p.drawPolygon(neck)

        # Faceted head silhouette.
        outline = [
            (-.98,-.42),(-.88,-.78),(-.52,-1.00),(0,-1.06),(.52,-1.00),(.88,-.78),
            (.98,-.42),(.93,.18),(.76,.63),(.44,.90),(0,1.00),(-.44,.90),
            (-.76,.63),(-.93,.18)
        ]
        pts = [ (cx+x*rx, cy+y*ry) for x,y in outline ]
        p.setBrush(QColor(18, 177, 180, 185))
        p.drawPolygon(QPolygonF([__import__("PyQt6.QtCore", fromlist=["QPointF"]).QPointF(x,y) for x,y in pts]))

        # Internal triangular facets.
        rows = [
            (-.80,-.40,-.48,-.78,0,-.98,.48,-.78,.80,-.40),
            (-.93,.10,-.46,-.18,0,-.34,.46,-.18,.93,.10),
            (-.76,.55,-.34,.34,0,.46,.34,.34,.76,.55),
            (-.42,.83,-.18,.52,0,.62,.18,.52,.42,.83),
        ]
        p.setBrush(Qt.BrushStyle.NoBrush)
        for row in rows:
            pts2 = [__import__("PyQt6.QtCore", fromlist=["QPointF"]).QPointF(cx+x*rx, cy+y*ry) for x,y in zip(row[::2], row[1::2])]
            p.setPen(QPen(QColor(90, 240, 235, 78), max(0.7, scale*1.2)))
            p.drawPolyline(QPolygonF(pts2))

        # Additional diagonal mesh lines.
        p.setPen(QPen(QColor(70, 235, 235, 54), max(0.6, scale)))
        for i in range(-4, 5):
            x = cx + i*rx*.17
            p.drawLine(int(x), int(cy-ry*.86), int(x-i*rx*.03), int(cy+ry*.80))
        for i in range(5):
            y = cy + (-.58+i*.30)*ry
            p.drawArc(QRectF(cx-rx*.82, y-ry*.12, rx*1.64, ry*.24), 0, 180*16)

        # Brows, eyes and luminous pupils.
        blink = 0.05 if math.sin(self.phase*.65) > .985 else 1.0
        for side in (-1, 1):
            ex = cx + side*rx*.38
            ey = cy - ry*.22
            p.setPen(QPen(QColor(120, 255, 248, 190), max(1.2, scale*2.0)))
            p.drawLine(int(ex-side*rx*.13), int(ey-ry*.08), int(ex+side*rx*.12), int(ey-ry*.10))
            p.setBrush(QColor(0, 45, 50, 220))
            p.drawEllipse(QRectF(ex-rx*.12, ey-ry*.045, rx*.24, max(2.0, ry*.09*blink)))
            p.setBrush(QColor(80, 255, 220, 230))
            p.drawEllipse(QRectF(ex-rx*.035, ey-ry*.025, rx*.07, max(2.0, ry*.05*blink)))

        # Nose bridge.
        p.setPen(QPen(QColor(70, 238, 232, 90), max(0.7, scale)))
        p.drawLine(int(cx), int(cy-ry*.12), int(cx-rx*.06), int(cy+ry*.22))
        p.drawLine(int(cx-rx*.06), int(cy+ry*.22), int(cx+rx*.07), int(cy+ry*.25))

        # Animated mouth / speaking waveform.
        mouth_y = cy + ry*.47
        amp = (2 + 10*self.level) * scale
        p.setPen(QPen(QColor(80, 255, 225, 210), max(1.0, scale*1.4)))
        last = None
        for i in range(25):
            x = cx-rx*.23 + i*(rx*.46/24)
            y = mouth_y + math.sin(self.phase*2.2+i*.65)*amp*(.25 if self.state == "SLEEPING" else 1)
            if last:
                p.drawLine(int(last[0]), int(last[1]), int(x), int(y))
            last = (x,y)

        # State ring.
        p.setPen(QPen(QColor(65, 245, 230, 75), 1.4))
        rr = rx*1.05 + math.sin(self.phase*1.8)*5
        p.drawEllipse(QRectF(cx-rr, cy-rr*.92, rr*2, rr*1.84))
