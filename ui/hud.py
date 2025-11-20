# ui/hud.py — Iron-Man style Arc Reactor HUD with Acrylic blur
#
import sys
import math
import time
import ctypes
import numpy as np
from ctypes import wintypes
from PyQt6 import QtCore, QtGui, QtWidgets
import winsound


# ---------------------------------------------------------------------
# WINDOWS ACRYLIC BLUR ENABLE
# ---------------------------------------------------------------------
def enable_acrylic(hwnd):
    ACCENT_ENABLE_ACRYLICBLURBEHIND = 4

    class ACCENTPOLICY(ctypes.Structure):
        _fields_ = [
            ("AccentState", ctypes.c_int),
            ("AccentFlags", ctypes.c_int),
            ("GradientColor", ctypes.c_int),
            ("AnimationId", ctypes.c_int),
        ]

    class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
        _fields_ = [
            ("Attribute", ctypes.c_int),
            ("Data", ctypes.c_void_p),
            ("SizeOfData", ctypes.c_size_t),
        ]

    accent = ACCENTPOLICY()
    accent.AccentState = ACCENT_ENABLE_ACRYLICBLURBEHIND
    accent.GradientColor = 0xAA000000

    data = WINDOWCOMPOSITIONATTRIBDATA()
    data.Attribute = 19
    data.Data = ctypes.byref(accent)
    data.SizeOfData = ctypes.sizeof(accent)

    ctypes.windll.user32.SetWindowCompositionAttribute(
        wintypes.HWND(hwnd), ctypes.byref(data)
    )


# ---------------------------------------------------------------------
# ARC REACTOR CORE WIDGET
# ---------------------------------------------------------------------
class ArcReactorWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, size=420):
        super().__init__(parent)

        self.setFixedSize(size, size)
        self._angle = 0.0
        self._pulse = 0.0
        self._mode = 'ready'
        self._text = ''
        self._level = 0.0

        self._last_ts = time.time()

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.on_tick)
        self._timer.start(16)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground, True)

    def set_mode(self, mode, text=''):
        self._mode = mode
        self._text = text

    def set_level(self, lvl: float):
        self._level = max(0.0, min(1.0, lvl))

    def on_tick(self):
        now = time.time()
        dt = now - self._last_ts
        self._last_ts = now

        if self._mode == 'thinking':
            speed = 200
        elif self._mode == 'listening':
            speed = 90
        else:
            speed = 40

        self._angle = (self._angle + speed * dt) % 360

        if self._mode == 'listening':
            self._pulse = 0.5 + 0.5 * math.sin(now * 6)
        elif self._mode == 'thinking':
            self._pulse = 0.5 + 0.5 * math.sin(now * 12)
        elif self._mode == 'speaking':
            self._pulse = 0.6 + 0.4 * math.sin(now * 8)
        else:
            self._pulse = 0.25 + 0.15 * math.sin(now * 2)

        self.update()

    def paintEvent(self, e):
        p = QtGui.QPainter(self)
        p.setRenderHints(
            QtGui.QPainter.RenderHint.Antialiasing |
            QtGui.QPainter.RenderHint.HighQualityAntialiasing
        )

        w, h = self.width(), self.height()
        cx, cy = w/2, h/2
        r = min(w, h)/2 * 0.9

        self._paint_glow(p, cx, cy, r)
        self._paint_core(p, cx, cy, r*0.45, self._angle)
        self._paint_rings(p, cx, cy, r)
        self._paint_bars(p, cx, cy, r)
        self._paint_text(p, cx, cy, r)

    # background glow
    def _paint_glow(self, p, cx, cy, r):
        grad = QtGui.QRadialGradient(QtCore.QPointF(cx, cy), r*1.2)
        grad.setColorAt(0.0, QtGui.QColor(8,200,230,180))
        grad.setColorAt(0.7, QtGui.QColor(8,20,30,60))
        p.setBrush(QtGui.QBrush(grad))
        p.setPen(QtCore.Qt.PenStyle.NoPen)
        p.drawEllipse(QtCore.QPointF(cx, cy), r*1.05, r*1.05)

    # rotating core polygons
    def _paint_core(self, p, cx, cy, rr, angle):
        mode_colors = {
            'ready': QtGui.QColor(120,200,255,220),
            'listening': QtGui.QColor(0,255,200,255),
            'thinking': QtGui.QColor(255,170,80,230),
            'speaking': QtGui.QColor(150,255,150,250),
        }
        col = mode_colors.get(self._mode, QtGui.QColor(120,200,255,220))

        p.save()
        p.translate(cx, cy)
        p.rotate(angle)

        qp = QtGui.QPen(col)
        qp.setWidth(2)
        p.setPen(qp)

        for layer in range(3):
            poly = QtGui.QPolygonF()
            sides = 6 + layer
            for i in range(sides):
                a = math.radians(i * 360 / sides)
                x = math.cos(a) * rr * (0.4 + layer * 0.35)
                y = math.sin(a) * rr * (0.4 + layer * 0.35)
                poly.append(QtCore.QPointF(x,y))
            p.drawPolygon(poly)

        p.restore()

    # glowing rings
    def _paint_rings(self, p, cx, cy, r):
        base = QtGui.QColor(10,180,220)
        for i,m in enumerate([0.95,0.75,0.55]):
            alpha = int(80 + self._pulse*120 - i*20)
            c = QtGui.QColor(base.red(), base.green(), base.blue(), max(20,min(255,alpha)))
            pen = QtGui.QPen(c)
            pen.setWidth(6 - i*2)
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            p.setPen(pen)
            p.setBrush(QtCore.Qt.BrushStyle.NoBrush)
            p.drawEllipse(QtCore.QPointF(cx,cy), r*m, r*m)

    # voice level bars
    def _paint_bars(self, p, cx, cy, r):
        bars = 7
        gap = 6
        bw = (r*0.35 - (bars-1)*gap) / bars
        base_x = cx - (bars*bw + (bars-1)*gap)/2
        base_y = cy + r*0.45
        filled = int(self._level * bars + 0.0001)

        for i in range(bars):
            h = (i+1)/bars * (r*0.18)
            rect = QtCore.QRectF(base_x + i*(bw+gap), base_y - h, bw, h)
            col = QtGui.QColor(0,220,160,220) if i<filled else QtGui.QColor(80,100,120,80)

            p.setBrush(col)
            p.setPen(QtCore.Qt.PenStyle.NoPen)
            p.drawRoundedRect(rect,3,3)

    # status text
    def _paint_text(self, p, cx, cy, r):
        p.save()
        font = p.font()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        p.setFont(font)

        status = self._mode.capitalize()
        txt = status if self._mode!="speaking" else (self._text[:40]+"..." if len(self._text)>40 else self._text)

        rect_w, rect_h = r*1.1, r*0.22
        rect_x, rect_y = cx-rect_w/2, cy+r*0.58

        p.setBrush(QtGui.QColor(10,18,22,160))
        p.setPen(QtCore.Qt.PenStyle.NoPen)
        p.drawRoundedRect(rect_x,rect_y,rect_w,rect_h,10,10)

        p.setPen(QtGui.QColor(230,255,250,240))
        p.drawText(
            QtCore.QRectF(rect_x+8,rect_y+6,rect_w-16,rect_h-12),
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter,
            txt
        )
        p.restore()


# ---------------------------------------------------------------------
# FLOATING HUD WINDOW
# ---------------------------------------------------------------------
class FloatingHUD(QtWidgets.QWidget):
    def __init__(self, size=420):
        super().__init__(
            None,
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint)

        self.setFixedSize(size,size)
        self.setWindowTitle("Jarvis HUD")

        screen = QtGui.QGuiApplication.primaryScreen()
        geo = screen.availableGeometry()
        self.move(geo.width()-size-30, geo.height()-size-90)

        try:
            hwnd = self.winId().__int__()
            enable_acrylic(hwnd)
        except:
            pass

        self.arc = ArcReactorWidget(self,size=size)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.arc,0,QtCore.Qt.AlignmentFlag.AlignCenter)

        self._opacity = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._opacity)
        self._opacity.setOpacity(1.0)

        self._drag = None

    def play_sound(self, kind="wake"):
        try:
            if kind=="wake":
                winsound.Beep(1200,80)
            elif kind=="think":
                winsound.Beep(500,120)
            elif kind=="done":
                winsound.Beep(900,120)
            else:
                winsound.Beep(800,80)
        except:
            pass

    def fade_in(self):
        a = QtCore.QPropertyAnimation(self._opacity,b"opacity")
        a.setDuration(350)
        a.setStartValue(0.0)
        a.setEndValue(1.0)
        a.start(QtCore.QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    def fade_out(self):
        a = QtCore.QPropertyAnimation(self._opacity,b"opacity")
        a.setDuration(350)
        a.setStartValue(1.0)
        a.setEndValue(0.15)
        a.start(QtCore.QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    def show_listening(self): self.arc.set_mode("listening")
    def show_thinking(self): self.arc.set_mode("thinking")
    def show_speaking(self,text=""): self.arc.set_mode("speaking",text)
    def show_ready(self): self.arc.set_mode("ready")
    def set_voice_level(self,l): self.arc.set_level(l)

    def mousePressEvent(self,e):
        if e.button()==QtCore.Qt.MouseButton.LeftButton:
            self._drag = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self,e):
        if self._drag:
            self.move(e.globalPosition().toPoint() - self._drag)

    def mouseReleaseEvent(self,e):
        self._drag = None


# ---------------------------------------------------------------------
# JarvisHUD WRAPPER  (FIXED)
# ---------------------------------------------------------------------
class JarvisHUD(QtCore.QObject):
    def __init__(self,size=420):
        super().__init__()
        self._size = size
        self.app = None
        self._w = None

    def start(self,blocking=False):
        if QtWidgets.QApplication.instance() is None:
            self.app = QtWidgets.QApplication(sys.argv)
        else:
            self.app = QtWidgets.QApplication.instance()

        self._w = FloatingHUD(size=self._size)
        self._w.show()
        self._w.show_ready()

        if blocking:
            sys.exit(self.app.exec())
        else:
            t = QtCore.QTimer()
            t.start(100)
            t.timeout.connect(lambda:None)

    # WRAPPERS
    def show_listening(self): self._w.show_listening()
    def show_thinking(self): self._w.show_thinking()
    def show_speaking(self,txt): self._w.show_speaking(txt)
    def show_ready(self): self._w.show_ready()
    def fade_in(self): self._w.fade_in()
    def fade_out(self): self._w.fade_out()
    def set_voice_level(self,l): self._w.set_voice_level(l)

    # ⭐ FIX ADDED HERE ⭐
    def play_sound(self,kind="wake"):
        if self._w and hasattr(self._w,"play_sound"):
            self._w.play_sound(kind)

    def stop(self):
        try: self._w.close()
        except: pass


if __name__=="__main__":
    hud = JarvisHUD(420)
    hud.start(blocking=False)
    if QtWidgets.QApplication.instance() is not None:
        QtWidgets.QApplication.instance().exec()
