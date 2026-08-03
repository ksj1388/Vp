import sys, numpy as np
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QRectF, QPointF, QTimer
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QPicture, QImage
import pyqtgraph as pg

class CandlestickItem(pg.GraphicsObject):
    def __init__(self):
        super().__init__()
        self.data = None
        self.picture = QPicture()
    def set_data(self, times, open_, high, low, close, spacing=None):
        self.data = (np.array(times, dtype=float), np.array(open_, dtype=float),
                     np.array(high, dtype=float), np.array(low, dtype=float),
                     np.array(close, dtype=float))
        self.spacing = spacing
        self.generate_picture()
        self.prepareGeometryChange()
        self.update()
    def generate_picture(self):
        self.picture = QPicture()
        if self.data is None: return
        times, open_, high, low, close = self.data
        n = len(times)
        if n == 0: return
        p = QPainter(self.picture)
        p.setRenderHint(QPainter.Antialiasing, False)
        candle_w = self.spacing * 0.7 if self.spacing else (times[-1] - times[0]) / n * 0.5
        half_w = candle_w / 2.0
        for i in range(n):
            t, o, hi, lo, cl = times[i], open_[i], high[i], low[i], close[i]
            is_up = cl >= o
            color = QColor("#00C850") if is_up else QColor("#DC3232")
            p.setPen(QPen(color, 0))
            p.drawLine(QPointF(t, lo), QPointF(t, hi))
            p.setBrush(QBrush(color))
            p.setPen(QPen(color, 0))
            if is_up:
                p.drawRect(QRectF(t - half_w, o, candle_w, cl - o))
            else:
                p.drawRect(QRectF(t - half_w, cl, candle_w, o - cl))
        p.end()
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
    def boundingRect(self):
        return QRectF(self.picture.boundingRect())

app = QApplication(sys.argv)

n = 50
base = 1700000000
times = np.arange(base, base + n * 60, 60, dtype=float)
np.random.seed(42)
o = 1.05000 + np.cumsum(np.random.uniform(-0.001, 0.001, n))
h = o + np.abs(np.random.normal(0.001, 0.0005, n))
l = o - np.abs(np.random.normal(0.001, 0.0005, n))
c = o + np.random.uniform(-0.002, 0.002, n)

win = pg.GraphicsLayoutWidget()
win.setBackground("#1e1e2e")
win.resize(800, 400)
plot = win.addPlot()
item = CandlestickItem()
item.set_data(times, o, h, l, c, spacing=60)
plot.addItem(item)
plot.setRange(QRectF(base - 100, 1.045, n * 60 + 200, 0.02))

def grab():
    img = win.grab().toImage()
    img.save("candle_test.png")
    print("Saved candle_test.png")
    app.quit()

QTimer.singleShot(500, grab)
app.exec_()
