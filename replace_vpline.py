import re

with open(r'C:\Users\ksj1388\OneDrive\Desktop\VPTRADEBOT\vptradebot.py', 'r', encoding='utf-8') as f:
    content = f.read()

start = 57433
end = 90884

replacement = '''
# ============================================================
#      VP Line Indicator - Volume Profile Auto [line] v2
# ============================================================

class VPLineIndicator:
    def __init__(self, plot):
        self.plot = plot
        self._items = []
        self._a_lines = []
        self._a_vol = []
        self._a_box = []
        self._l_poc = None
        
        self.parts = 25
        self.max_width = 15
        self.max_lines = 500
        self.c_vol_h = "#ff8800"
        self.c_vol = "#0088ff"
        self.c_poc = "#ff0000"
        
        self._t_h = 86400000
        self._t_l = 3600000

    @staticmethod
    def _get_xy(ln):
        if not hasattr(ln, 'getData'):
            return np.array([0]), np.array([0])
        try:
            x_data = ln.getData()[0]
            y_data = ln.getData()[1]
            if x_data is None or y_data is None:
                return np.array([0]), np.array([0])
            return np.array(x_data), np.array(y_data)
        except:
            return np.array([0]), np.array([0])

    def clear_all(self):
        for item in self._items:
            self.plot.removeItem(item)
        self._items.clear()
        self._a_lines.clear()
        self._a_vol.clear()
        self._a_box.clear()
        if self._l_poc:
            self.plot.removeItem(self._l_poc)
            self._l_poc = None

    def _tf_to_ms(self, tf_str):
        mapping = {
            '1': 60000, '3': 180000, '5': 300000, '10': 600000,
            '15': 900000, '30': 1800000, '60': 3600000, '120': 7200000,
            '180': 10800000, '240': 14400000, '360': 21600000, '720': 43200000,
            '1D': 86400000, '3D': 259200000, '1W': 604800000,
            '1M': 2592000000, '1Y': 31536000000,
            'M1': 60000, 'M5': 300000, 'M15': 900000, 'M30': 1800000,
            'H1': 3600000, 'H4': 14400000, 'D1': 86400000,
            'W1': 604800000, 'MN': 2592000000,
        }
        return mapping.get(tf_str, 3600000)

    def _auto_htf(self, current_tf):
        if current_tf in ['MN', 'W1']: return '1M'
        if current_tf in ['D1']: return '1W'
        if current_tf in ['H1', 'H4']: return '1D'
        if current_tf in ['M5', 'M15', 'M30']: return '60'
        if current_tf in ['M1']: return '1'
        return '60'

    def _auto_ltf(self, current_tf):
        if current_tf in ['MN', 'W1', 'D1']: return 'D'
        if current_tf in ['H1', 'H4']: return 'H1'
        if current_tf in ['M5', 'M15', 'M30']: return '60'
        if current_tf in ['M1']: return '1'
        return '60'

    def update_settings(self, parts, max_width, ltf_str, htf_str, current_tf, is_auto=True):
        self.parts = parts
        self.max_width = max_width
        self.is_auto = is_auto
        self.ltf_str = ltf_str
        self.htf_str = htf_str
        self.current_tf = current_tf
        self.is_auto = is_auto
        if is_auto:
            self._t_h = self._tf_to_ms(self._auto_htf(current_tf))
            self._t_l = self._tf_to_ms(self._auto_ltf(current_tf))
        else:
            self._t_h = self._tf_to_ms(htf_str if htf_str != 'Auto' else self._auto_htf(current_tf))
            self._t_l = self._tf_to_ms(ltf_str if ltf_str != 'Auto' else self._auto_ltf(current_tf))

    def draw(self, times, high, low, close, volume, bar_index):
        if len(times) < 2:
            return
            
        cur_high = high[-1]
        cur_low = low[-1]
        cur_vol = volume[-1]
        
        if self._t_l == 0:
            return
        
        i_size = self.parts
        aMax = self.max_lines
        
        if not self._a_lines:
            self._a_lines = []
            self._a_vol = []
            self._a_box = []
        
        # Check for HTF change (simplified)
        chT_H = len(self._a_lines) > 0 and len(times) > len(self._a_lines)
        
        if not self._a_lines:
            hi = high[-1]
            lo = low[-1]
            if hi > lo:
                step = (hi - lo) / self.parts
                for j in range(self.parts):
                    y1 = hi - step * j
                    y2 = hi - step * (j + 1)
                    ln = pg.PlotDataItem([times[-1], times[-1]], [y1, y2], 
                                         pen=pg.mkPen(self.c_vol, width=1))
                    self.plot.addItem(ln, ignoreBounds=True)
                    self._a_lines.insert(0, ln)
                    self._items.append(ln)
                    self._a_vol.insert(0, 0.0)
                
                from PyQt5.QtWidgets import QGraphicsRectItem
                from PyQt5.QtCore import QRectF
                box = QGraphicsRectItem()
                box.setRect(QRectF(times[-1], self._a_lines[0].getData()[1][1] if len(self._a_lines[0].getData()[1]) > 1 else low[-1], 0, 
                                  self._a_lines[0].getData()[1][0] - self._a_lines[0].getData()[1][1] if len(self._a_lines[0].getData()[1]) > 1 else 1))
                box.setBrush(pg.mkBrush(0, 0, 255, 20))
                box.setPen(pg.mkPen(None))
                self.plot.addItem(box, ignoreBounds=True)
                self._a_box.insert(0, box)
                self._items.append(box)
                
                while len(self._a_lines) > self.max_lines:
                    old = self._a_lines.pop()
                    self.plot.removeItem(old)
                    self._a_vol.pop()
                while len(self._a_box) > int(self.max_lines / self.parts) + 1:
                    old_box = self._a_box.pop()
                    self.plot.removeItem(old_box)
        
        if not self._a_lines:
            return
        
        hi = self._a_lines[0].getData()[1][0] if len(self._a_lines[0].getData()[1]) > 0 else high[-1]
        lo = self._a_lines[-1].getData()[1][1] if len(self._a_lines[-1].getData()[1]) > 1 else low[-1]
        
        if self._a_box:
            box = self._a_box[0]
            box.setRect(box.rect().x(), box.rect().y(), 
                       times[-1] - box.rect().x(), box.rect().height())
        
        if self._l_poc:
            x_poc, y_poc = self._get_xy(self._l_poc)
            if len(x_poc) > 0 and len(y_poc) > 0:
                self._l_poc.setData([float(x_poc[0]), times[-1]], 
                                    [float(y_poc[0]), float(y_poc[0])])
        
        if high[-1] > hi:
            for j in range(self.parts):
                if j < len(self._a_lines):
                    ln = self._a_lines[j]
                    x_data, _ = self._get_xy(ln)
                    if len(x_data) > 0:
                        ln.setData([float(x_data[0]), times[-1]], [high[-1], high[-1]])
                hi = high[-1]
                if self._a_box:
                    box = self._a_box[0]
                    box.setRect(box.rect().x(), box.rect().y(), box.rect().width(), high[-1] - box.rect().y())
        if low[-1] < lo:
            for j in range(self.parts):
                if j < len(self._a_lines):
                    ln = self._a_lines[j]
                    x_data, _ = self._get_xy(ln)
                    if len(x_data) > 0:
                        ln.setData([float(x_data[0]), times[-1]], [low[-1], low[-1]])
                lo = low[-1]
                if self._a_box:
                    box = self._a_box[0]
                    box.setRect(box.rect().x(), low[-1], box.rect().width(), hi - low[-1])
        
        # Accumulate volume
        for j in range(min(self.parts, len(self._a_lines))):
            ln = self._a_lines[j]
            x_data, y_data = self._get_xy(ln)
            if len(y_data) < 2:
                continue
            y1 = float(y_data[0])
            y2 = float(y_data[1])
            if high[-1] >= y1 and low[-1] <= y2:
                self._a_vol[j] += volume[-1]
                width = max(1, int(self.max_width * self._a_vol[j] / max(self._a_vol) if max(self._a_vol) > 0 else 1))
                ln.setPen(pg.mkPen(self.c_vol, width=width))
        
        self._draw_poc()
    
    def _draw_poc(self):
        if not self._a_vol:
            return
        max_vol = max(self._a_vol)
        idx = self._a_vol.index(max_vol)
        
        if idx >= len(self._a_lines) - 1:
            return
        
        if self._l_poc:
            self.plot.removeItem(self._l_poc)
        
        ln1 = self._a_lines[idx]
        ln2 = self._a_lines[idx + 1]
        
        x1, y1 = self._get_xy(self._a_lines[idx])
        x2, y2 = self._get_xy(self._a_lines[idx + 1])
        
        if len(y1) == 0 or len(y2) == 0:
            return
        
        poc_y = (y1[0] + y2[0]) / 2
        
        if len(x1) == 0:
            return
        
        x1 = x1[0]
        x2 = (x1[-1] if len(x1) > 1 else x1[0]) + 100
        
        self._l_poc = pg.PlotDataItem([x1, x2], [poc_y, poc_y], 
                                      pen=pg.mkPen(self.c_poc, width=2))
        self.plot.addItem(self._l_poc, ignoreBounds=True)
        self._items.append(self._l_poc)

    @staticmethod
    def _get_xy(ln):
        if not hasattr(ln, 'getData'):
            return np.array([0]), np.array([0])
        try:
            x_data = ln.getData()[0]
            y_data = ln.getData()[1]
            if x_data is None or y_data is None:
                return np.array([0]), np.array([0])
            return np.array(x_data), np.array(y_data)
        except:
            return np.array([0]), np.array([0])


class ChartWidget(QWidget):
'''

with open(r'C:\Users\ksj1388\OneDrive\Desktop\VPTRADEBOT\vptradebot.py', 'r', encoding='utf-8') as f:
    content = f.read()

start = 57433
end = 90884

new_content = content[:57433] + replacement + content[90884:]

with open(r'C:\Users\ksj1388\OneDrive\Desktop\VPTRADEBOT\vptradebot.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Replacement done')
"