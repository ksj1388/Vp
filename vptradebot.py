"""
VPTradeBot - پیشرفته متاتریدر ۵ داشبورد
MetaTrader 5 Advanced Trading Dashboard
"""

import sys
import json
import os
import datetime
import time
import traceback
import subprocess
import winreg
from datetime import timedelta

import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QSplitter, QFrame, QTextEdit, QTabWidget, QMessageBox,
    QHeaderView, QAbstractItemView, QApplication, QCheckBox,
    QSizePolicy, QGroupBox, QGridLayout, QToolTip,
    QSpinBox, QDoubleSpinBox, QScrollArea, QComboBox,
    QDialog, QColorDialog
)
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette, QBrush, QPen

# ============================================================
#                    پیکربندی و ثابت‌ها
# ============================================================

DARK_STYLE = """
QMainWindow, QWidget {
    background-color: #0a0a1a;
    color: #e0e0f0;
    font-family: 'Segoe UI Variable', 'Segoe UI', 'SF Pro Display', 'Tahoma', 'Arial';
    font-size: 12px;
}

QMainWindow {
    border: none;
}

QWidget#centralWidget {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #0a0a1a, stop:0.5 #0d1117, stop:1.0 #0a0a1a);
}

QLabel {
    color: #e0e0f0;
    font-size: 12px;
}
QLabel#title_label {
    font-size: 18px;
    font-weight: 700;
    color: #7aa2f7;
    letter-spacing: 1px;
}
QLabel#section_title {
    font-size: 13px;
    font-weight: 700;
    color: #9ece6a;
    padding: 5px 8px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(158,206,106,0.08), stop:1 rgba(158,206,106,0));
    border-left: 3px solid #9ece6a;
    border-radius: 0 4px 4px 0;
}
QLabel#account_value {
    font-size: 14px;
    font-weight: 700;
    color: #e0af68;
}
QLabel#profit_positive {
    font-size: 14px;
    font-weight: 700;
    color: #9ece6a;
}
QLabel#profit_negative {
    font-size: 14px;
    font-weight: 700;
    color: #f7768e;
}

QPushButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1e2030, stop:1 #16161e);
    color: #c0caf5;
    border: 1px solid #33467c;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 11px;
    font-weight: 500;
    min-height: 22px;
}
QPushButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #292e42, stop:1 #1e2030);
    border-color: #7aa2f7;
    color: #e0f0ff;
}
QPushButton:pressed {
    background-color: #1a1b26;
    border-color: #7dcfff;
}
QPushButton:disabled {
    background-color: #15151f;
    color: #565f89;
    border-color: #0a0a1a;
}

QPushButton#timeframe_btn {
    padding: 5px 8px;
    font-size: 10px;
    font-weight: 600;
    min-height: 22px;
    min-width: 36px;
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1e2030, stop:1 #16161e);
    border: 1px solid #292e42;
    border-radius: 6px;
    color: #7aa2f7;
}
QPushButton#timeframe_btn:hover {
    background-color: #292e42;
    border-color: #7aa2f7;
    color: #a9b1d6;
}
QPushButton#timeframe_btn_active {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #7aa2f7, stop:1 #3d59a1);
    color: #1a1b26;
    font-weight: 700;
    padding: 5px 8px;
    font-size: 10px;
    min-height: 22px;
    min-width: 36px;
    border: 1px solid #7aa2f7;
    border-radius: 6px;
    border-bottom: 2px solid #2ac3de;
}
QPushButton#timeframe_btn_active:hover {
    background-color: #7aa2f7;
    border-color: #7dcfff;
}

QPushButton#refresh_btn {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #7aa2f7, stop:1 #3d59a1);
    color: #1a1b26;
    font-weight: 700;
    border-radius: 6px;
}
QPushButton#refresh_btn:hover {
    background-color: #7aa2f7;
    border-color: #7dcfff;
}

QLineEdit {
    background-color: #1a1b26;
    color: #c0caf5;
    border: 1.5px solid #292e42;
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 12px;
    selection-background-color: #3d59a1;
}
QLineEdit:focus {
    border-color: #7aa2f7;
    background-color: #16161e;
}

QTableWidget {
    background-color: #0f0f1a;
    alternate-background-color: #141420;
    color: #c0caf5;
    border: 1px solid #1e2030;
    gridline-color: #1a1b26;
    font-size: 11px;
    selection-background-color: rgba(122,162,247,0.15);
    border-radius: 6px;
}
QTableWidget::item {
    padding: 4px 6px;
    border-bottom: 1px solid #141420;
}
QTableWidget::item:selected {
    background-color: rgba(122,162,247,0.12);
    color: #a9d0ff;
}
QHeaderView::section {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1e2030, stop:1 #16161e);
    color: #7aa2f7;
    border: none;
    border-bottom: 2px solid #33467c;
    padding: 6px 8px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

QTextEdit {
    background-color: #0a0a14;
    color: #9ece6a;
    border: 1px solid #1e2030;
    border-radius: 6px;
    font-family: 'Cascadia Code', 'Consolas', 'Courier New';
    font-size: 11px;
    padding: 4px;
}
QTextEdit:focus {
    border-color: #33467c;
}

QGroupBox {
    border: 1px solid #292e42;
    border-radius: 8px;
    margin-top: 14px;
    font-weight: 700;
    color: #7aa2f7;
    background-color: rgba(30,32,48,0.4);
    padding-top: 16px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: #7aa2f7;
    font-size: 11px;
    letter-spacing: 0.5px;
}

QTabWidget::pane {
    border: 1px solid #292e42;
    background-color: #0f0f1a;
    border-radius: 8px;
}
QTabBar::tab {
    background-color: #1a1b26;
    color: #565f89;
    padding: 8px 18px;
    border: 1px solid #292e42;
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-size: 11px;
    font-weight: 600;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: #0f0f1a;
    color: #7aa2f7;
    border-bottom: 2px solid #7aa2f7;
}
QTabBar::tab:hover:!selected {
    background-color: #292e42;
    color: #a9b1d6;
}

QScrollBar:vertical {
    background-color: #0a0a14;
    width: 8px;
    border: none;
    border-radius: 4px;
    margin: 2px;
}
QScrollBar::handle:vertical {
    background-color: #33467c;
    border-radius: 4px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover {
    background-color: #7aa2f7;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar:horizontal {
    background-color: #0a0a14;
    height: 8px;
    border: none;
    border-radius: 4px;
    margin: 2px;
}
QScrollBar::handle:horizontal {
    background-color: #33467c;
    border-radius: 4px;
    min-width: 24px;
}
QScrollBar::handle:horizontal:hover {
    background-color: #7aa2f7;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QCheckBox {
    color: #c0caf5;
    font-size: 11px;
    spacing: 6px;
}
QCheckBox::indicator {
    width: 14px;
    height: 14px;
    border: 2px solid #33467c;
    border-radius: 4px;
    background-color: #1a1b26;
}
QCheckBox::indicator:checked {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #7aa2f7, stop:1 #2ac3de);
    border-color: #7aa2f7;
}
QCheckBox::indicator:hover {
    border-color: #7aa2f7;
}

QSplitter::handle {
    background-color: #292e42;
    width: 3px;
    border-radius: 1px;
}
QSplitter::handle:hover {
    background-color: #7aa2f7;
}

QComboBox {
    background-color: #1a1b26;
    color: #c0caf5;
    border: 1.5px solid #292e42;
    border-radius: 6px;
    padding: 4px 8px;
    font-size: 11px;
    min-height: 20px;
}
QComboBox:hover {
    border-color: #7aa2f7;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #7aa2f7;
    margin-right: 6px;
}
QComboBox QAbstractItemView {
    background-color: #1a1b26;
    color: #c0caf5;
    border: 1px solid #292e42;
    border-radius: 6px;
    selection-background-color: #33467c;
    outline: none;
    padding: 2px;
}

QSpinBox, QDoubleSpinBox {
    background-color: #1a1b26;
    color: #c0caf5;
    border: 1.5px solid #292e42;
    border-radius: 6px;
    padding: 3px 6px;
    font-size: 11px;
}
QSpinBox:focus, QDoubleSpinBox:focus {
    border-color: #7aa2f7;
}
QSpinBox::up-button, QDoubleSpinBox::up-button,
QSpinBox::down-button, QDoubleSpinBox::down-button {
    background-color: #292e42;
    border: none;
    width: 16px;
}
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {
    border-left: 3px solid transparent;
    border-right: 3px solid transparent;
    border-bottom: 4px solid #7aa2f7;
}
QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {
    border-left: 3px solid transparent;
    border-right: 3px solid transparent;
    border-top: 4px solid #7aa2f7;
}

QToolTip {
    background-color: #1a1b26;
    color: #c0caf5;
    border: 1px solid #33467c;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 11px;
}

QMenu {
    background-color: #1a1b26;
    color: #c0caf5;
    border: 1px solid #292e42;
    border-radius: 8px;
    padding: 4px;
}
QMenu::item {
    padding: 6px 20px;
    border-radius: 4px;
}
QMenu::item:selected {
    background-color: #33467c;
}
"""

TIMEFRAMES = {
    "M1": mt5.TIMEFRAME_M1,
    "M2": mt5.TIMEFRAME_M2,
    "M3": mt5.TIMEFRAME_M3,
    "M5": mt5.TIMEFRAME_M5,
    "M10": mt5.TIMEFRAME_M10,
    "M15": mt5.TIMEFRAME_M15,
    "M30": mt5.TIMEFRAME_M30,
    "H1": mt5.TIMEFRAME_H1,
    "H4": mt5.TIMEFRAME_H4,
    "D1": mt5.TIMEFRAME_D1,
}

TF_INTERVAL = {
    "M1": 60,
    "M2": 120,
    "M3": 180,
    "M5": 300,
    "M10": 600,
    "M15": 900,
    "M30": 1800,
    "H1": 3600,
    "H4": 14400,
    "D1": 86400,
}

MIN_CANDLES = 2000
TIMEFRAME_RANGE = {}
for _tf, _sec in TF_INTERVAL.items():
    TIMEFRAME_RANGE[_tf] = timedelta(seconds=MIN_CANDLES * _sec * 2)

SYMBOLS_FILTER = [".c", ".d", "_EMP", ".rts", ".index", "BTC", "ETH", "XRP",
                  "USDRUB", "EURRUB", "CNYRUB"]

# ============================================================
#                    کلاس مدیریت لاگ
# ============================================================

class Logger:
    _instance = None
    callbacks = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def subscribe(cls, callback):
        cls.callbacks.append(callback)

    @classmethod
    def log(cls, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{timestamp}] {message}"
        print(formatted)
        for cb in cls.callbacks:
            try:
                cb(formatted)
            except Exception:
                pass

    @classmethod
    def info(cls, message):
        cls.log(f"INFO  | {message}")

    @classmethod
    def warning(cls, message):
        cls.log(f"WARN  | {message}")

    @classmethod
    def error(cls, message):
        cls.log(f"ERROR | {message}")

    @classmethod
    def success(cls, message):
        cls.log(f"OK    | {message}")

# ============================================================
#                کلاس اتصال به متاتریدر ۵
# ============================================================

class MT5Connector:
    _connected = False
    _account_info = None

    @classmethod
    def _find_mt5_path(cls):
        paths = [
            os.environ.get("PROGRAMFILES", "C:\\Program Files"),
            os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)"),
        ]
        for base in paths:
            candidates = [
                os.path.join(base, "MetaTrader 5", "terminal64.exe"),
                os.path.join(base, "MetaTrader 5", "terminal.exe"),
                os.path.join(base, "MetaTrader 5", "metatrader.exe"),
            ]
            for p in candidates:
                if os.path.exists(p):
                    return p
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            )
            i = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    try:
                        display_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                        if "MetaTrader 5" in display_name:
                            install_loc, _ = winreg.QueryValueEx(
                                subkey, "InstallLocation"
                            )
                            winreg.CloseKey(subkey)
                            winreg.CloseKey(key)
                            exe = os.path.join(install_loc, "terminal64.exe")
                            if os.path.exists(exe):
                                return exe
                            exe = os.path.join(install_loc, "terminal.exe")
                            if os.path.exists(exe):
                                return exe
                    except FileNotFoundError:
                        pass
                    winreg.CloseKey(subkey)
                    i += 1
                except WindowsError:
                    break
            winreg.CloseKey(key)
        except Exception:
            pass
        return None

    @classmethod
    def _launch_mt5(cls):
        path = cls._find_mt5_path()
        if path is None:
            Logger.warning("MetaTrader 5 not found on system")
            return False
        Logger.info(f"Launching MetaTrader 5 from: {path}")
        try:
            subprocess.Popen([path], shell=False)
            import time
            time.sleep(5)
            return True
        except Exception as e:
            Logger.error(f"Error launching MetaTrader: {e}")
            return False

    @classmethod
    def initialize(cls):
        Logger.info("Connecting to MetaTrader 5...")
        initialized = mt5.initialize()
        if not initialized:
            Logger.warning("MetaTrader 5 not running. Attempting to launch...")
            if cls._launch_mt5():
                initialized = mt5.initialize()
        if not initialized:
            error = mt5.last_error()
            Logger.error(f"Error connecting to MetaTrader: {error}")
            cls._connected = False
            return False

        Logger.success("Connected to MetaTrader 5")
        cls._connected = True

        info = mt5.account_info()
        if info:
            cls._account_info = info
            Logger.success(f"Account {info.login} - {info.server}")
        else:
            Logger.warning("MetaTrader not connected to any server")
        return True

    @classmethod
    def is_connected(cls):
        return cls._connected and mt5.terminal_info() is not None

    @classmethod
    def get_account_info(cls):
        if cls.is_connected():
            cls._account_info = mt5.account_info()
        return cls._account_info

    @classmethod
    def get_symbols(cls, market_watch_only=True):
        if not cls.is_connected():
            return []
        all_symbols = mt5.symbols_get() or []
        if not market_watch_only:
            return all_symbols
        result = []
        for s in all_symbols:
            if s.name.startswith("#"):
                continue
            tick = mt5.symbol_info_tick(s.name)
            if tick is not None and tick.bid > 0 and tick.ask > 0:
                result.append(s)
        return result

    @classmethod
    def get_symbol_tick(cls, symbol):
        if not cls.is_connected():
            return None
        return mt5.symbol_info_tick(symbol)

    @classmethod
    def get_symbol_info(cls, symbol):
        if not cls.is_connected():
            return None
        return mt5.symbol_info(symbol)

    @classmethod
    def get_rates(cls, symbol, timeframe, from_date, to_date):
        if not cls.is_connected():
            return None
        mt5.symbol_select(symbol, True)
        rates = mt5.copy_rates_range(symbol, timeframe, from_date, to_date)
        if rates is None or len(rates) == 0:
            return None
        df = pd.DataFrame(rates)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        return df

    @classmethod
    def get_rates_from_pos(cls, symbol, timeframe, count):
        if not cls.is_connected():
            return None
        mt5.symbol_select(symbol, True)
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
        if rates is None or len(rates) == 0:
            return None
        df = pd.DataFrame(rates)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        return df

    @classmethod
    def get_last_tick(cls, symbol):
        if not cls.is_connected():
            return None
        return mt5.symbol_info_tick(symbol)

    @classmethod
    def shutdown(cls):
        Logger.info("Disconnected from MetaTrader 5")
        try:
            mt5.shutdown()
        except Exception:
            pass
        cls._connected = False

# ============================================================
#                   اجرای معاملات در متاتریدر
# ============================================================

class MT5Executor:
    def __init__(self):
        self.magic = 123456
        self.on_trade_callback = None

    def _notify_trade(self):
        if self.on_trade_callback:
            try:
                self.on_trade_callback()
            except Exception:
                pass

    def send_market(self, symbol, side, lot, sl=None, tp=None, comment="Manual"):
        try:
            mt5.symbol_select(symbol, True)
        except Exception:
            pass
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return None, "Cannot get tick"
        if tick.time == 0 or (tick.ask == 0 and tick.bid == 0):
            return None, "No live prices for symbol"
        order_type = mt5.ORDER_TYPE_BUY if side == "buy" else mt5.ORDER_TYPE_SELL
        price = tick.ask if side == "buy" else tick.bid

        info = mt5.symbol_info(symbol)
        if info:
            vs = info.volume_step if info.volume_step > 0 else 0.01
            vol_min = info.volume_min if info.volume_min > 0 else 0.01
            vol_max = info.volume_max if info.volume_max > 0 else 100.0
            lot = round(lot / vs) * vs
            lot = max(vol_min, min(lot, vol_max))
            lot = round(lot, 8)
            point = info.point
            digits = info.digits
            min_stop = info.trade_stops_level * point if info.trade_stops_level > 0 else 0
            if sl:
                if side == "buy":
                    if price - sl < min_stop:
                        sl = round(price - min_stop - point, digits)
                        Logger.info(f"[ORDER] SL adjusted (buy): new_sl={sl} min_stop={min_stop}")
                else:
                    if sl - price < min_stop:
                        sl = round(price + min_stop + point, digits)
                        Logger.info(f"[ORDER] SL adjusted (sell): new_sl={sl} min_stop={min_stop}")

        request = {
            "action": mt5.TRADE_ACTION_DEAL, "symbol": symbol, "volume": lot,
            "type": order_type, "price": price, "deviation": 10,
            "magic": self.magic, "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
        }
        if sl: request["sl"] = self._norm(symbol, sl)
        if tp: request["tp"] = self._norm(symbol, tp)
        for fill in [mt5.ORDER_FILLING_FOK, mt5.ORDER_FILLING_IOC, mt5.ORDER_FILLING_RETURN]:
            request["type_filling"] = fill
            Logger.info(f"ORDER REQUEST: {symbol} {side} vol={lot} price={price} sl={request.get('sl','-')} tp={request.get('tp','-')} fill={fill}")
            result = mt5.order_send(request)
            if result is not None and result.retcode == mt5.TRADE_RETCODE_DONE:
                self._notify_trade()
                return result, "OK"
        if result is not None and result.retcode == 10030:
            request.pop("type_filling", None)
            Logger.info(f"ORDER RETRY (no fill mode): {symbol} {side} vol={lot} price={price}")
            result = mt5.order_send(request)
            if result is not None and result.retcode == mt5.TRADE_RETCODE_DONE:
                self._notify_trade()
                return result, "OK"
        if result is None:
            return None, "order_send returned None"
        return None, f"Error: {result.retcode} ({result.comment})"

    def send_limit(self, symbol, side, lot, entry, sl=None, tp=None, comment="Manual"):
        order_type = mt5.ORDER_TYPE_BUY_LIMIT if side == "buy" else mt5.ORDER_TYPE_SELL_LIMIT
        return self._send_pending(symbol, order_type, lot, entry, sl, tp, comment)

    def send_stop(self, symbol, side, lot, entry, sl=None, tp=None, comment="Manual"):
        order_type = mt5.ORDER_TYPE_BUY_STOP if side == "buy" else mt5.ORDER_TYPE_SELL_STOP
        return self._send_pending(symbol, order_type, lot, entry, sl, tp, comment)

    def _send_pending(self, symbol, order_type, lot, entry, sl, tp, comment):
        try:
            mt5.symbol_select(symbol, True)
        except Exception:
            pass
        info = mt5.symbol_info(symbol)
        if info:
            vs = info.volume_step if info.volume_step > 0 else 0.01
            vol_min = info.volume_min if info.volume_min > 0 else 0.01
            vol_max = info.volume_max if info.volume_max > 0 else 100.0
            lot = round(lot / vs) * vs
            lot = max(vol_min, min(lot, vol_max))
            lot = round(lot, 8)
        request = {
            "action": mt5.TRADE_ACTION_PENDING, "symbol": symbol, "volume": lot,
            "type": order_type, "price": self._norm(symbol, entry),
            "deviation": 10, "magic": self.magic, "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
        }
        if sl: request["sl"] = self._norm(symbol, sl)
        if tp: request["tp"] = self._norm(symbol, tp)
        for fill in [mt5.ORDER_FILLING_FOK, mt5.ORDER_FILLING_IOC, mt5.ORDER_FILLING_RETURN]:
            request["type_filling"] = fill
            result = mt5.order_send(request)
            if result is not None and result.retcode == mt5.TRADE_RETCODE_DONE:
                self._notify_trade()
                return result, "OK"
        if result is not None and result.retcode == 10030:
            request.pop("type_filling", None)
            result = mt5.order_send(request)
            if result is not None and result.retcode == mt5.TRADE_RETCODE_DONE:
                self._notify_trade()
                return result, "OK"
        if result is None:
            return None, "order_send returned None"
        return None, f"Error {result.retcode}: {result.comment}"

    def close_position(self, ticket):
        pos = mt5.positions_get(ticket=ticket)
        if not pos: return None, "Position not found"
        pos = pos[0]
        tick = mt5.symbol_info_tick(pos.symbol)
        if tick is None: return None, "Cannot get tick"
        order_type = mt5.ORDER_TYPE_SELL if pos.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
        price = tick.bid if pos.type == mt5.ORDER_TYPE_BUY else tick.ask
        request = {
            "action": mt5.TRADE_ACTION_DEAL, "symbol": pos.symbol,
            "volume": pos.volume, "type": order_type, "position": ticket,
            "price": price, "deviation": 20, "magic": self.magic,
            "comment": "Close Manual", "type_time": mt5.ORDER_TIME_GTC,
        }
        for fill in [mt5.ORDER_FILLING_FOK, mt5.ORDER_FILLING_IOC, mt5.ORDER_FILLING_RETURN]:
            request["type_filling"] = fill
            result = mt5.order_send(request)
            if result is not None and result.retcode == mt5.TRADE_RETCODE_DONE:
                self._notify_trade()
                return result, "OK"
        if result is not None and result.retcode == 10030:
            request.pop("type_filling", None)
            result = mt5.order_send(request)
            if result is not None and result.retcode == mt5.TRADE_RETCODE_DONE:
                self._notify_trade()
                return result, "OK"
        if result is None:
            return None, "order_send returned None"
        return None, f"Error: {result.retcode}"

    def close_all(self):
        positions = mt5.positions_get()
        if not positions: return 0, "No positions"
        count = 0
        for p in positions:
            self.close_position(p.ticket)
            count += 1
        return count, f"Closed {count} positions"

    def close_profit(self):
        positions = mt5.positions_get()
        if not positions: return 0, "No positions"
        count = 0
        for p in positions:
            if p.profit > 0:
                self.close_position(p.ticket)
                count += 1
        return count, f"Closed {count} profitable positions"

    def close_loss(self):
        positions = mt5.positions_get()
        if not positions: return 0, "No positions"
        count = 0
        for p in positions:
            if p.profit <= 0:
                self.close_position(p.ticket)
                count += 1
        return count, f"Closed {count} losing positions"

    def cancel_order(self, ticket):
        order = mt5.orders_get(ticket=ticket)
        if not order: return None, "Order not found"
        request = {"action": mt5.TRADE_ACTION_REMOVE, "order": ticket}
        result = mt5.order_send(request)
        if result is None: return None, "order_send returned None"
        if result.retcode != mt5.TRADE_RETCODE_DONE: return None, f"Error: {result.retcode}"
        return result, "OK"

    def get_positions(self):
        p = mt5.positions_get()
        return list(p) if p else []

    def get_orders(self):
        o = mt5.orders_get()
        return list(o) if o else []

    def _norm(self, symbol, price):
        info = mt5.symbol_info(symbol)
        return round(price, info.digits) if info else price

    def _norm_price(self, symbol, price):
        return self._norm(symbol, price)

    def modify_position(self, ticket, sl=None, tp=None):
        pos = mt5.positions_get(ticket=ticket)
        if not pos:
            return None, "Position not found"
        pos = pos[0]
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "symbol": pos.symbol,
        }
        if sl is not None:
            request["sl"] = self._norm_price(pos.symbol, sl)
        else:
            request["sl"] = pos.sl if pos.sl else 0.0
        if tp is not None:
            request["tp"] = self._norm_price(pos.symbol, tp)
        else:
            request["tp"] = pos.tp if pos.tp else 0.0
        result = mt5.order_send(request)
        if result is None:
            return None, "order_send returned None"
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return None, f"Error {result.retcode}: {result.comment}"
        return result, "OK"

    def close_position_partial(self, ticket, volume):
        position = mt5.positions_get(ticket=ticket)
        if not position:
            return None, "Position not found"
        pos = position[0]
        info = mt5.symbol_info(pos.symbol)
        if info:
            vs = info.volume_step if info.volume_step > 0 else 0.01
            vol_min = info.volume_min if info.volume_min > 0 else 0.01
        else:
            vs = 0.01
            vol_min = 0.01
        vol = round(volume / vs) * vs
        vol = max(vol_min, min(vol, pos.volume))
        if vol <= 0:
            return None, "Invalid volume"
        tick = mt5.symbol_info_tick(pos.symbol)
        if tick is None:
            return None, "Cannot get tick"
        if pos.type == mt5.ORDER_TYPE_BUY:
            order_type = mt5.ORDER_TYPE_SELL
            price = tick.bid
        else:
            order_type = mt5.ORDER_TYPE_BUY
            price = tick.ask
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": pos.symbol,
            "volume": vol,
            "type": order_type,
            "position": ticket,
            "price": price,
            "deviation": 20,
            "magic": self.magic,
            "comment": "Partial Close",
            "type_time": mt5.ORDER_TIME_GTC,
        }
        for fill in [mt5.ORDER_FILLING_FOK, mt5.ORDER_FILLING_IOC, mt5.ORDER_FILLING_RETURN]:
            request["type_filling"] = fill
            result = mt5.order_send(request)
            if result is not None and result.retcode == mt5.TRADE_RETCODE_DONE:
                self._notify_trade()
                return result, "OK"
        if result is not None and result.retcode == 10030:
            request.pop("type_filling", None)
            result = mt5.order_send(request)
            if result is not None and result.retcode == mt5.TRADE_RETCODE_DONE:
                self._notify_trade()
                return result, "OK"
        if result is None:
            return None, "order_send returned None"
        return None, f"Error: {result.retcode} - {result.comment}" if result else "order_send returned None"

# ============================================================
#                سیستم خروج حرفه‌ای
# ============================================================

class ExitManager:
    def __init__(self, executor):
        self.executor = executor
        self.enabled = False

        self.trail_use_algoman = False
        self.trail_algoman_act = "50%"
        self.trail_atr_mult = 0.5
        self._lead52_values = {}
        self._atr_values = {}

        self.be_enabled = True
        self.be_tp_pct = 1.0
        self.be_sl_pct = 1.00

        self.tp_levels_enabled = True
        self.tp_levels = [
            {"ratio": 1.0, "volume_pct": 25},
            {"ratio": 2.0, "volume_pct": 25},
            {"ratio": 3.0, "volume_pct": 50},
        ]

        self.time_exit_enabled = False
        self.time_exit_minutes = 60

        self._position_cache = {}
        self._symbol_cache = {}
        self._managed_tickets = set()
        self._exit_disabled_tickets = set()
        self.auto_manage_enabled = True
        self._lead52_calc_cache = {}

    def set_enabled(self, enabled):
        self.enabled = enabled
        if not enabled:
            self._position_cache.clear()

    def set_managed_tickets(self, tickets):
        self._managed_tickets = set(tickets)
        stale = [t for t in self._position_cache if t not in self._managed_tickets]
        for t in stale:
            del self._position_cache[t]

    def get_config(self):
        return {
            "trail_use_algoman": self.trail_use_algoman,
            "trail_algoman_act": self.trail_algoman_act,
            "trail_atr_mult": self.trail_atr_mult,
            "be_enabled": self.be_enabled,
            "be_tp_pct": self.be_tp_pct,
            "be_sl_pct": self.be_sl_pct,
            "tp_levels_enabled": self.tp_levels_enabled,
            "tp_levels": self.tp_levels[:],
            "time_exit_enabled": self.time_exit_enabled,
            "time_exit_minutes": self.time_exit_minutes,
        }

    def set_config(self, cfg):
        self.trail_use_algoman = cfg.get("trail_use_algoman", False)
        self.trail_algoman_act = cfg.get("trail_algoman_act", "50%")
        self.trail_atr_mult = cfg.get("trail_atr_mult", 0.5)
        self.be_enabled = cfg.get("be_enabled", True)
        self.be_tp_pct = cfg.get("be_tp_pct", 1.0)
        self.be_sl_pct = cfg.get("be_sl_pct", 1.00)
        self.tp_levels_enabled = cfg.get("tp_levels_enabled", True)
        self.tp_levels = cfg.get("tp_levels", [
            {"ratio": 1.0, "volume_pct": 25},
            {"ratio": 2.0, "volume_pct": 25},
            {"ratio": 3.0, "volume_pct": 50},
        ])
        self.time_exit_enabled = cfg.get("time_exit_enabled", False)
        self.time_exit_minutes = cfg.get("time_exit_minutes", 60)

    def _sym_digits(self, symbol):
        if symbol not in self._symbol_cache:
            info = mt5.symbol_info(symbol)
            self._symbol_cache[symbol] = info.digits if info else 5
        return self._symbol_cache[symbol]

    def _pip_size(self, symbol):
        if symbol not in self._symbol_cache:
            info = mt5.symbol_info(symbol)
            self._symbol_cache[symbol] = info.digits if info else 5
        info_digits = self._symbol_cache[symbol]
        point = 10 ** -info_digits
        return point * 10 if info_digits >= 4 else point

    def _point(self, symbol):
        if symbol not in self._symbol_cache:
            info = mt5.symbol_info(symbol)
            self._symbol_cache[symbol] = info.digits if info else 5
        return 10 ** -self._symbol_cache[symbol]

    def _get_algoman_act_ratio(self):
        act_map = {"10% TP": 0.10, "25% TP": 0.25, "50% TP": 0.50, "TP1": 1.0, "TP1.5": 1.5, "TP2": 2.0}
        return act_map.get(self.trail_algoman_act, 0.50)

    def _ensure_lead52(self, symbol):
        now = time.time()
        if symbol in self._lead52_calc_cache and now - self._lead52_calc_cache[symbol] < 30:
            return
        try:
            rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, 0, 100)
            if rates is None or len(rates) < 60:
                return
            highs = np.array([r['high'] for r in rates], dtype=float)
            lows = np.array([r['low'] for r in rates], dtype=float)
            closes = np.array([r['close'] for r in rates], dtype=float)
            period = 52
            n = len(closes)
            lead52_val = (np.min(lows[n - period:]) + np.max(highs[n - period:])) / 2.0
            tr = np.zeros(n)
            tr[0] = highs[0] - lows[0]
            for i in range(1, n):
                tr[i] = max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1]))
            atr_val = float(np.mean(tr[-14:])) if n >= 14 else 0
            self._lead52_values[symbol] = lead52_val
            self._atr_values[symbol] = atr_val
            self._lead52_calc_cache[symbol] = now
        except Exception as e:
            Logger.error(f"[ExitMgr] _ensure_lead52 error {symbol}: {e}")

    def process_positions(self):
        if not self.enabled:
            return
        positions = self.executor.get_positions()
        if positions:
            Logger.info(f"[ExitMgr] enabled={self.enabled} trail_lead52={self.trail_use_algoman} act={self.trail_algoman_act} lead52_syms={list(self._lead52_values.keys())} pos_count={len(positions)} managed={len(self._managed_tickets)}")

        for pos in positions:
            ticket = pos.ticket
            if ticket in self._exit_disabled_tickets:
                continue
            if ticket not in self._managed_tickets:
                if self.auto_manage_enabled:
                    self._managed_tickets.add(ticket)
                else:
                    continue
            symbol = pos.symbol
            digits = self._sym_digits(symbol)
            pip_size = self._pip_size(symbol)
            point = self._point(symbol)

            if self.trail_use_algoman:
                self._ensure_lead52(symbol)

            if ticket not in self._position_cache:
                self._position_cache[ticket] = {
                    "be_activated": False,
                    "tp_hit": set(),
                    "tp_sl_dist": None,
                }
                if pos.sl and pos.sl > 0:
                    self._position_cache[ticket]["tp_sl_dist"] = abs(pos.price_open - pos.sl)
            cache = self._position_cache[ticket]
            current_price = pos.price_current
            is_buy = pos.type == mt5.ORDER_TYPE_BUY

            if self.time_exit_enabled:
                now_tick = mt5.symbol_info_tick(symbol)
                if now_tick:
                    elapsed = now_tick.time - pos.time
                    if elapsed >= self.time_exit_minutes * 60:
                        Logger.info(f"[ExitMgr] Time exit: closing #{ticket} (held {elapsed//60}m)")
                        self.executor.close_position(ticket)
                        continue

            if self.be_enabled and not cache["be_activated"]:
                if pos.sl and pos.sl > 0:
                    sl_dist_pips = abs(pos.price_open - pos.sl) / pip_size
                    if sl_dist_pips > 0:
                        tp1_dist = sl_dist_pips / 4.0
                        be_act_pips = tp1_dist * self.be_tp_pct
                        be_act_price = pos.price_open + (be_act_pips * pip_size) if is_buy else pos.price_open - (be_act_pips * pip_size)
                        remain = max(1.0 - self.be_sl_pct, 0.0)
                        be_sl_price = pos.price_open - (sl_dist_pips * remain * pip_size) if is_buy else pos.price_open + (sl_dist_pips * remain * pip_size)
                        hit = (is_buy and current_price >= be_act_price) or (not is_buy and current_price <= be_act_price)
                        if hit:
                            be_sl_price = self.executor._norm_price(symbol, be_sl_price)
                            res, msg = self.executor.modify_position(ticket, sl=be_sl_price)
                            if res:
                                cache["be_activated"] = True
                                new_sl_dist = abs(be_sl_price - pos.price_open) / pip_size
                                Logger.info(f"[ExitMgr] BE on #{ticket} @ {be_sl_price:.{digits}f} (SL {sl_dist_pips:.0f}p -> {new_sl_dist:.0f}p, TP%={self.be_tp_pct*100:.0f}%, SL%={self.be_sl_pct*100:.0f}%)")

            if self.trail_use_algoman and symbol in self._lead52_values:
                lead52 = self._lead52_values[symbol]
                atr_val = self._atr_values.get(symbol, 0)
                offset = atr_val * self.trail_atr_mult
                if pos.sl and pos.sl > 0:
                    sl_dist = abs(pos.price_open - pos.sl)
                else:
                    sl_dist = abs(pos.price_open - current_price) * 0.5
                act_ratio = self._get_algoman_act_ratio()
                act_dist = sl_dist * act_ratio
                if is_buy:
                    act_price = pos.price_open + act_dist
                    activated = current_price >= act_price
                    trail_level = lead52 - offset
                    if activated and trail_level < current_price:
                        new_sl = self.executor._norm_price(symbol, trail_level)
                        if pos.sl is None or new_sl > pos.sl + point:
                            res, msg = self.executor.modify_position(ticket, sl=new_sl)
                            if res:
                                Logger.info(f"[ExitMgr] Lead52 Trail #{ticket} BUY -> {new_sl:.{digits}f} (entry={pos.price_open:.{digits}f} cur={current_price:.{digits}f} L52={lead52:.{digits}f} -{self.trail_atr_mult}ATR={offset:.{digits}f})")
                        else:
                            Logger.info(f"[ExitMgr] Lead52 Trail skip #{ticket} BUY (trail={trail_level:.{digits}f} <= sl={pos.sl:.{digits}f})")
                    else:
                        Logger.info(f"[ExitMgr] Lead52 Trail skip #{ticket} BUY (act={activated} act_p={act_price:.{digits}f} cur={current_price:.{digits}f} trail={trail_level:.{digits}f} L52={lead52:.{digits}f} ATR={atr_val:.{digits}f})")
                else:
                    act_price = pos.price_open - act_dist
                    activated = current_price <= act_price
                    trail_level = lead52 + offset
                    if activated and trail_level > current_price:
                        new_sl = self.executor._norm_price(symbol, trail_level)
                        if pos.sl is None or new_sl < pos.sl - point:
                            res, msg = self.executor.modify_position(ticket, sl=new_sl)
                            if res:
                                Logger.info(f"[ExitMgr] Lead52 Trail #{ticket} SELL -> {new_sl:.{digits}f} (entry={pos.price_open:.{digits}f} cur={current_price:.{digits}f} L52={lead52:.{digits}f} +{self.trail_atr_mult}ATR={offset:.{digits}f})")
                        else:
                            Logger.info(f"[ExitMgr] Lead52 Trail skip #{ticket} SELL (trail={trail_level:.{digits}f} >= sl={pos.sl:.{digits}f})")
                    else:
                        Logger.info(f"[ExitMgr] Lead52 Trail skip #{ticket} SELL (act={activated} act_p={act_price:.{digits}f} cur={current_price:.{digits}f} trail={trail_level:.{digits}f} L52={lead52:.{digits}f} ATR={atr_val:.{digits}f})")

            if self.tp_levels_enabled:
                fixed_sl_dist = cache.get("tp_sl_dist")
                if fixed_sl_dist is None or fixed_sl_dist <= 0:
                    if pos.sl and pos.sl > 0:
                        fixed_sl_dist = abs(pos.price_open - pos.sl)
                        cache["tp_sl_dist"] = fixed_sl_dist
                    else:
                        tick_info = mt5.symbol_info_tick(symbol)
                        if tick_info:
                            spread = abs(tick_info.ask - tick_info.bid)
                            fixed_sl_dist = spread * 5 if spread > 0 else pip_size * 50
                            cache["tp_sl_dist"] = fixed_sl_dist
                for i, level in enumerate(self.tp_levels):
                    if i in cache["tp_hit"]:
                        continue
                    if not fixed_sl_dist or fixed_sl_dist <= 0:
                        continue
                    ratio = level["ratio"]
                    tp_price = (
                        pos.price_open + fixed_sl_dist * ratio
                        if is_buy else pos.price_open - fixed_sl_dist * ratio
                    )
                    tp_price = self.executor._norm_price(symbol, tp_price)
                    hit = (
                        (is_buy and current_price >= tp_price) or
                        (not is_buy and current_price <= tp_price)
                    )
                    if hit:
                        vol_pct = level["volume_pct"] / 100.0
                        close_vol = round(pos.volume * vol_pct, 2)
                        if close_vol > 0:
                            res, msg = self.executor.close_position_partial(ticket, close_vol)
                            if res:
                                cache["tp_hit"].add(i)
                                Logger.info(f"[ExitMgr] TP{i+1} hit on #{ticket} (vol={close_vol})")
                            else:
                                Logger.error(f"[ExitMgr] TP{i+1} close FAILED on #{ticket}: {msg}")

        active_tickets = {p.ticket for p in positions}
        for t in list(self._position_cache.keys()):
            if t not in active_tickets:
                del self._position_cache[t]

# ============================================================
#                پنل معامله دستی
# ============================================================

class ManualTradePanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.symbol = "EURUSD"
        self.executor = MT5Executor()
        self.entry_price = None
        self.sl_price = None
        self.tp_price = None
        self._sl_manually_set = False
        self.risk_mode = "% Balance"
        self.risk_value = 1.0
        self.rr_value = 3.0

        self.setFixedWidth(260)
        self.setVisible(False)
        self._build_ui()

    def _build_ui(self):
        self.setStyleSheet("""
            ManualTradePanel {
                background-color: #0f0f1a; border: 2px solid #1a4a7a;
                border-radius: 10px;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        header = QLabel("\u26A1  Manual Trade")
        header.setStyleSheet("color: #e0f0ff; font-size: 14px; font-weight: bold;")
        layout.addWidget(header)

        sep = QFrame(); sep.setFrameShape(QFrame.HLine); sep.setStyleSheet("color: #1a2a3a;")
        layout.addWidget(sep)

        sf = QHBoxLayout()
        self.btn_buy = QPushButton("BUY")
        self.btn_buy.setMinimumHeight(38)
        self.btn_buy.setStyleSheet("""QPushButton{background-color:#1e6f3f;color:white;border:2px solid #1a5a3a;border-radius:6px;font-size:14px;font-weight:bold}
            QPushButton:hover{background-color:#2a8f5f} QPushButton:checked{border-color:#44ff88;background-color:#166534}""")
        self.btn_buy.setCheckable(True)
        self.btn_buy.setChecked(True)
        self.btn_buy.clicked.connect(lambda: self._set_side("buy"))
        sf.addWidget(self.btn_buy)

        self.btn_sell = QPushButton("SELL")
        self.btn_sell.setMinimumHeight(38)
        self.btn_sell.setStyleSheet("""QPushButton{background-color:#8f2a2a;color:white;border:2px solid #6a1a1a;border-radius:6px;font-size:14px;font-weight:bold}
            QPushButton:hover{background-color:#5a1a1a} QPushButton:checked{border-color:#f7768e;background-color:#3d1515}""")
        self.btn_sell.setCheckable(True)
        self.btn_sell.clicked.connect(lambda: self._set_side("sell"))
        sf.addWidget(self.btn_sell)
        layout.addLayout(sf)

        self.order_type = QtWidgets.QComboBox()
        self.order_type.addItems(["Market", "Buy Limit", "Sell Limit", "Buy Stop", "Sell Stop"])
        self.order_type.currentTextChanged.connect(self._on_type_changed)
        self.order_type.setStyleSheet("QComboBox{background:#1a1b26;color:#c0caf5;border:1.5px solid #292e42;border-radius:6px;padding:4px;font-size:11px}")
        layout.addWidget(self.order_type)

        gf = QGroupBox("Parameters")
        gf.setStyleSheet("QGroupBox{color:#8899aa;font-size:10px;font-weight:bold;border:1px solid #1a2a3a;border-radius:4px;margin-top:6px;padding-top:10px} QGroupBox::title{subcontrol-origin:margin;left:6px;padding:0 4px}")
        g = QGridLayout(gf)
        g.setContentsMargins(6, 4, 6, 4)
        g.setSpacing(4)

        g.addWidget(QLabel("Volume:"), 0, 0)
        self.vol_spin = QtWidgets.QDoubleSpinBox()
        self.vol_spin.setRange(0.01, 100); self.vol_spin.setDecimals(2)
        self.vol_spin.setValue(0.10); self.vol_spin.setSingleStep(0.01)
        self.vol_spin.setStyleSheet("background:#1a1b26;color:#c0caf5;border:1.5px solid #292e42;border-radius:6px;padding:2px 4px;font-size:11px")
        g.addWidget(self.vol_spin, 0, 1)

        g.addWidget(QLabel("Entry:"), 1, 0)
        self.entry_lbl = QLabel("MKT")
        self.entry_lbl.setStyleSheet("color:#9ece6a;font-size:11px;font-weight:bold;font-family:Consolas")
        g.addWidget(self.entry_lbl, 1, 1)
        self.entry_btn = QPushButton("\u270E")
        self.entry_btn.setFixedSize(22, 22)
        self.entry_btn.setStyleSheet("background:#1a1b26;color:#8899aa;border:1.5px solid #292e42;border-radius:6px")
        self.entry_btn.clicked.connect(self._manual_entry)
        g.addWidget(self.entry_btn, 1, 2)

        g.addWidget(QLabel("Stop Loss:"), 2, 0)
        self.sl_lbl = QLabel("---")
        self.sl_lbl.setStyleSheet("color:#f7768e;font-size:11px;font-weight:bold;font-family:Consolas")
        g.addWidget(self.sl_lbl, 2, 1)
        self.sl_btn = QPushButton("\u270E")
        self.sl_btn.setFixedSize(22, 22)
        self.sl_btn.setStyleSheet("background:#1a1b26;color:#8899aa;border:1.5px solid #292e42;border-radius:6px")
        self.sl_btn.clicked.connect(self._manual_sl)
        g.addWidget(self.sl_btn, 2, 2)

        g.addWidget(QLabel("Take Profit:"), 3, 0)
        self.tp_lbl = QLabel("---")
        self.tp_lbl.setStyleSheet("color:#7dcfff;font-size:11px;font-weight:bold;font-family:Consolas")
        g.addWidget(self.tp_lbl, 3, 1, 1, 2)

        self.risk_lbl = QLabel("")
        self.risk_lbl.setStyleSheet("color:#ffaa44;font-size:8px;font-family:Consolas")
        g.addWidget(self.risk_lbl, 4, 0, 1, 3)
        layout.addWidget(gf)

        self.send_btn = QPushButton("\u26A1  SEND ORDER")
        self.send_btn.setMinimumHeight(38)
        self.send_btn.setStyleSheet("QPushButton{background:#1a4a8a;color:white;border:none;border-radius:6px;font-size:13px;font-weight:bold} QPushButton:hover{background:#1a3a6a} QPushButton:disabled{background:#2a3a3a;color:#666}")
        self.send_btn.clicked.connect(self._send_order)
        layout.addWidget(self.send_btn)

        sep2 = QFrame(); sep2.setFrameShape(QFrame.HLine); sep2.setStyleSheet("color:#1a2a3a;")
        layout.addWidget(sep2)

        # per-trade exit checkbox
        self.exit_on_trade = QCheckBox("Enable Exit")
        self.exit_on_trade.setStyleSheet("color:#7aa2f7;font-size:8px")
        layout.addWidget(self.exit_on_trade)

        pg = QGroupBox("Positions")
        pg.setStyleSheet("QGroupBox{color:#8899aa;font-size:10px;font-weight:bold;border:1px solid #1a2a3a;border-radius:4px;margin-top:6px;padding-top:10px} QGroupBox::title{subcontrol-origin:margin;left:6px;padding:0 4px}")
        pl = QVBoxLayout(pg); pl.setContentsMargins(4, 4, 4, 4); pl.setSpacing(4)
        self.pos_info = QLabel("No open positions")
        self.pos_info.setStyleSheet("color:#8899aa;font-size:10px;font-family:Consolas")
        pl.addWidget(self.pos_info)
        br = QHBoxLayout()
        for txt, h in [("CLOSE ALL", self._close_all), ("+PROFIT", self._close_profit), ("-LOSS", self._close_loss)]:
            b = QPushButton(txt)
            b.setStyleSheet("background:#1a1b26;color:#8899aa;border:1.5px solid #292e42;border-radius:6px;padding:4px;font-size:8px;font-weight:bold")
            b.clicked.connect(h); br.addWidget(b)
        pl.addLayout(br)
        layout.addWidget(pg)

    def _set_side(self, side):
        self._sl_manually_set = False
        self.btn_buy.setChecked(side == "buy")
        self.btn_sell.setChecked(side == "sell")
        ec = "#9ece6a" if side == "buy" else "#f7768e"
        self.entry_lbl.setStyleSheet(f"color:{ec};font-size:11px;font-weight:bold;font-family:Consolas")
        if not self.entry_price:
            tick = MT5Connector.get_last_tick(self.symbol)
            if tick:
                self.entry_price = tick.ask if side == "buy" else tick.bid
                self.entry_lbl.setText(f"{self.entry_price:.5f}")
        if self.entry_price:
            pip_size = self._pip_size(self.symbol)
            sl_pips = self._default_sl_pips(self.symbol)
            if side == "buy":
                self.sl_price = self.entry_price - pip_size * sl_pips
            else:
                self.sl_price = self.entry_price + pip_size * sl_pips
            self.sl_lbl.setText(f"{self.sl_price:.5f}")
        self._recalc_tp()
        cw = self._find_chart()
        if cw:
            cw._update_trade_lines(entry=self.entry_price, sl=self.sl_price, tp=self.tp_price, side=side)

    def _on_type_changed(self, txt):
        is_limit_stop = txt in ("Buy Limit", "Sell Limit", "Buy Stop", "Sell Stop")
        self.entry_btn.setEnabled(is_limit_stop)
        self.entry_price = None
        self.sl_price = None
        self.tp_price = None
        cw = self._find_chart()
        if cw:
            cw._show_trade_lines()

    def _manual_entry(self):
        val, ok = QtWidgets.QInputDialog.getDouble(self, "Entry Price", "Enter price:", self.entry_price or 0, 0, 100000, 5)
        if ok: self._set_entry(val)

    def _manual_sl(self):
        val, ok = QtWidgets.QInputDialog.getDouble(self, "Stop Loss", "Enter SL price:", self.sl_price or 0, 0, 100000, 5)
        if ok: self._set_sl(val)

    def _set_entry(self, price):
        self.entry_price = price
        is_buy = self.btn_buy.isChecked()
        c = "#9ece6a" if is_buy else "#f7768e"
        self.entry_lbl.setText(f"{price:.5f}")
        self.entry_lbl.setStyleSheet(f"color:{c};font-size:11px;font-weight:bold;font-family:Consolas")
        self._calc_risk()

    def _set_sl(self, price, manual=True):
        self.sl_price = price
        if manual:
            self._sl_manually_set = True
        self.sl_lbl.setText(f"{price:.5f}")
        self._calc_risk()
        cw = self._find_chart()
        if cw and self.isVisible():
            side = "buy" if self.btn_buy.isChecked() else "sell"
            cw._update_trade_lines(entry=self.entry_price, sl=self.sl_price, tp=self.tp_price, side=side)

    def _find_chart(self):
        return getattr(self, '_chart_widget', None)

    def _pip_size(self, symbol):
        info = mt5.symbol_info(symbol)
        if info:
            return info.point * 10 if info.point <= 0.001 else info.point
        return 0.0001

    def _default_sl_pips(self, symbol):
        return 3

    def _recalc_tp(self):
        if self.entry_price and self.sl_price and self.rr_value > 0:
            diff = abs(self.entry_price - self.sl_price) * self.rr_value
            if self.btn_buy.isChecked():
                self.tp_price = self.entry_price + diff
            else:
                self.tp_price = self.entry_price - diff
            self.tp_lbl.setText(f"{self.tp_price:.5f}")
        else:
            self.tp_price = None
            self.tp_lbl.setText("---")

    def _calc_risk(self):
        if not self.entry_price or not self.sl_price:
            self._last_risk_amt = 0
            return
        diff = abs(self.entry_price - self.sl_price)
        info = mt5.symbol_info(self.symbol)
        if not info: return
        pip_val = info.trade_tick_value * (10 if info.point <= 0.001 else 1)
        stop_pips = diff / (info.point * 10 if info.point <= 0.001 else info.point)
        if pip_val <= 0 or stop_pips <= 0: return
        acct = mt5.account_info()
        balance = acct.balance if acct else 10000
        if self.risk_mode == "% Balance":
            risk_amt = self.risk_value / 100 * balance
        elif self.risk_mode == "$ Fixed":
            risk_amt = self.risk_value
        else:
            lot = self.risk_value
            self.vol_spin.setValue(lot)
            risk_text = f"Fixed {lot:.2f} Lots"
            self.risk_lbl.setText(risk_text)
            diff = abs(self.entry_price - self.sl_price) if self.entry_price and self.sl_price else 0
            info = mt5.symbol_info(self.symbol)
            if info and diff > 0:
                pv = info.trade_tick_value * (10 if info.point <= 0.001 else 1)
                stop_p = diff / (info.point * 10 if info.point <= 0.001 else info.point)
                self._last_risk_amt = stop_p * pv * lot if pv > 0 else 0
            else:
                self._last_risk_amt = 0
            return
        lot = max(0.01, round(risk_amt / (stop_pips * pip_val), 2))
        vs = info.volume_step if info.volume_step > 0 else 0.01
        lot = round(lot / vs) * vs
        lot = max(info.volume_min if info.volume_min > 0 else 0.01, min(lot, info.volume_max if info.volume_max > 0 else 100))
        self.vol_spin.setValue(lot)
        self.risk_lbl.setText(f"Risk: ${risk_amt:.2f} | Lot: {lot:.2f}")
        self._last_risk_amt = risk_amt

    def set_risk_params(self, mode, value, rr):
        self.risk_mode = mode
        self.risk_value = value
        self.rr_value = rr
        self._recalc_tp()
        self._calc_risk()
        cw = self._find_chart()
        if cw and self.isVisible():
            side = "buy" if self.btn_buy.isChecked() else "sell"
            cw._update_trade_lines(entry=self.entry_price, sl=self.sl_price, tp=self.tp_price, side=side)

    def set_symbol(self, symbol):
        self.symbol = symbol

    def _send_order(self):
        otype = self.order_type.currentText()
        side = "buy" if self.btn_buy.isChecked() else "sell"
        vol = self.vol_spin.value()
        is_market = otype == "Market"
        is_limit = "Limit" in otype
        is_stop = "Stop" in otype
        entry = self.entry_price if not is_market else None
        sl = self.sl_price
        tp = self.tp_price
        self.send_btn.setEnabled(False)
        self.send_btn.setText("Sending...")

        if is_market:
            tick = MT5Connector.get_symbol_tick(self.symbol)
            if tick is None:
                Logger.error("Cannot get tick for market order")
                self.send_btn.setEnabled(True)
                self.send_btn.setText("\u26A1 SEND ORDER")
                return
            real_price = tick.ask if side == "buy" else tick.bid
            if self.entry_price and self.sl_price:
                sl_dist = abs(self.entry_price - self.sl_price)
                if side == "buy":
                    sl = real_price - sl_dist
                    tp = real_price + sl_dist * self.rr_value if self.rr_value > 0 else self.tp_price
                else:
                    sl = real_price + sl_dist
                    tp = real_price - sl_dist * self.rr_value if self.rr_value > 0 else self.tp_price
                info = MT5Connector.get_symbol_info(self.symbol)
                if info:
                    sl = round(sl, info.digits)
                    tp = round(tp, info.digits)
            result, msg = self.executor.send_market(self.symbol, side, vol, sl, tp)
        elif is_limit:
            result, msg = self.executor.send_limit(self.symbol, side, vol, entry, sl, tp)
        elif is_stop:
            result, msg = self.executor.send_stop(self.symbol, side, vol, entry, sl, tp)
        else:
            result, msg = None, "Unknown order type"

        self.send_btn.setEnabled(True)
        self.send_btn.setText("\u26A1 SEND ORDER")
        if result:
            Logger.success(f"Order sent: {side} {vol} {self.symbol}")
            mw = self.window()
            if mw and hasattr(mw, 'account_panel'):
                mw.account_panel.refresh()
            if mw and hasattr(mw, 'strategy_panel'):
                sp = mw.strategy_panel
                if hasattr(sp, 'exit_mgr') and sp.exit_mgr:
                    if hasattr(result, 'order'):
                        sp.exit_mgr._exit_disabled_tickets.add(result.order)
                        Logger.info(f"[ExitMgr] Exit disabled for ticket #{result.order}")
            cw = getattr(self, '_chart_widget', None)
            if cw:
                cw._hide_trade_lines()
                cw._update_pos_lines()
            self.hide()
        else:
            Logger.error(f"Order failed: {msg}")

    def _close_all(self):
        c, msg = self.executor.close_all()
        Logger.info(msg)

    def _close_profit(self):
        c, msg = self.executor.close_profit()
        Logger.info(msg)

    def _close_loss(self):
        c, msg = self.executor.close_loss()
        Logger.info(msg)

    def refresh_positions(self):
        try:
            positions = self.executor.get_positions()
            orders = self.executor.get_orders()
            count = len(positions) + len(orders)
            if count == 0:
                self.pos_info.setText("No positions / orders")
            else:
                texts = []
                for p in positions:
                    s = "BUY" if p.type == 0 else "SELL"
                    texts.append(f"#{p.ticket} {s} {p.volume:.2f} ${p.profit:+.2f}")
                self.pos_info.setText("\n".join(texts) if texts else f"{count} open")
        except Exception:
            pass

# ============================================================
#           ویجت رسم کندل استیک (CandlestickChart)
# ============================================================

class CandlestickItem:
    def __init__(self, plot):
        self.pi = plot.plotItem if hasattr(plot, 'plotItem') else plot
        self.items = []
        self.n = 0
        self.open_ = None
        self.high = None
        self.low = None
        self.close = None
        self._mode = "candle"
        self._brick_size = None

    def set_mode(self, mode):
        self._mode = mode

    def set_brick_size(self, size):
        self._brick_size = size

    def set_data(self, times, open_, high, low, close, spacing=None):
        for it in self.items:
            self.pi.removeItem(it)
        self.items = []
        self.open_ = np.array(open_, dtype=np.float64)
        self.high = np.array(high, dtype=np.float64)
        self.low = np.array(low, dtype=np.float64)
        self.close = np.array(close, dtype=np.float64)
        self.n = len(self.open_)
        if self._mode == "line":
            self._draw_line()
        elif self._mode == "rinko":
            self._draw_rinko()
        else:
            self._draw_candles()

    def _draw_rinko(self):
        closes = self.close.tolist()
        highs_arr = self.high.tolist()
        lows_arr = self.low.tolist()
        if len(closes) < 2:
            return
        brick_size = self._brick_size
        lookback = min(len(closes), 500)
        start = len(closes) - lookback
        sub_closes = closes[start:]
        sub_highs = highs_arr[start:]
        sub_lows = lows_arr[start:]
        if brick_size is None or brick_size <= 0:
            trs = []
            for i in range(1, len(sub_closes)):
                tr = max(sub_highs[i] - sub_lows[i],
                         abs(sub_highs[i] - sub_closes[i - 1]),
                         abs(sub_lows[i] - sub_closes[i - 1]))
                trs.append(tr)
            atr = float(np.mean(trs)) if trs else 0.0001
            brick_size = round(atr * 0.5, 8)
            if brick_size <= 0:
                brick_size = 0.0001
        bricks = []
        last = sub_closes[0]
        for i in range(1, len(sub_closes)):
            c = sub_closes[i]
            while c - last >= brick_size:
                bricks.append(("up", last, last + brick_size))
                last += brick_size
            while last - c >= brick_size:
                bricks.append(("down", last - brick_size, last))
                last -= brick_size
        if not bricks:
            bricks.append(("up", sub_closes[-1] - brick_size, sub_closes[-1]))
        self._rinko_bricks = bricks
        self._rinko_brick_size = brick_size
        bw = 0.8
        half = bw / 2.0
        for brick_idx, (direction, low, high) in enumerate(bricks):
            color = "#26a69a" if direction == "up" else "#ef5350"
            rect = QtWidgets.QGraphicsRectItem(float(brick_idx) - half, low, bw, brick_size)
            rect.setBrush(pg.mkBrush(color))
            rect.setPen(pg.mkPen(color, width=1))
            self.pi.addItem(rect)
            self.items.append(rect)
        nb = len(bricks)
        if nb > 0:
            self.pi.vb.setXRange(-1, nb, padding=0)

    def _draw_line(self):
        x = list(range(self.n))
        y = self.close.tolist()
        line = pg.PlotDataItem(x, y, pen=pg.mkPen("#7aa2f7", width=2))
        self.pi.addItem(line)
        self.items.append(line)

    def _draw_candles(self):
        bw = 0.6
        half = bw / 2.0
        for i in range(self.n):
            o = float(self.open_[i])
            h = float(self.high[i])
            l = float(self.low[i])
            c = float(self.close[i])
            is_bull = c >= o
            color = "#26a69a" if is_bull else "#ef5350"
            wick = QtWidgets.QGraphicsLineItem(float(i), l, float(i), h)
            wick.setPen(pg.mkPen(color, width=1))
            self.pi.addItem(wick)
            self.items.append(wick)
            body_top = max(o, c)
            body_bot = min(o, c)
            body_h = body_top - body_bot
            if body_h < 1e-10:
                body_h = 1e-10
            rect = QtWidgets.QGraphicsRectItem(
                float(i) - half, body_bot, bw, body_h
            )
            rect.setBrush(pg.mkBrush(color))
            rect.setPen(pg.mkPen(color, width=1))
            self.pi.addItem(rect)
            self.items.append(rect)

    def update_last(self, idx, o, h, l, c):
        if idx < 0 or idx >= self.n:
            return
        self.open_[idx] = o
        self.high[idx] = h
        self.low[idx] = l
        self.close[idx] = c
        if self._mode == "line":
            for it in self.items:
                self.pi.removeItem(it)
            self.items = []
            self._draw_line()
        elif self._mode == "rinko":
            return
        else:
            start = idx * 2
            end = min(start + 2, len(self.items))
            for it in self.items[start:end]:
                self.pi.removeItem(it)
            self.items[start:end] = []
            bw = 0.6
            half = bw / 2.0
            is_bull = c >= o
            color = "#26a69a" if is_bull else "#ef5350"
            wick = QtWidgets.QGraphicsLineItem(float(idx), l, float(idx), h)
            wick.setPen(pg.mkPen(color, width=1))
            self.pi.addItem(wick)
            body_top = max(o, c)
            body_bot = min(o, c)
            body_h = body_top - body_bot
            if body_h < 1e-10:
                body_h = 1e-10
            rect = QtWidgets.QGraphicsRectItem(
                float(idx) - half, body_bot, bw, body_h
            )
            rect.setBrush(pg.mkBrush(color))
            rect.setPen(pg.mkPen(color, width=1))
            self.pi.addItem(rect)
            self.items.insert(start, wick)
            self.items.insert(start + 1, rect)

    def clear(self):
        for it in self.items:
            self.pi.removeItem(it)
        self.items = []

class IchimokuCloudIndicator:
    def __init__(self, plot_item):
        self.plot = plot_item
        self._drawn = []
        self.conversionPeriods = 9
        self.basePeriods = 26
        self.laggingSpan2Periods = 52
        self.displacement = 26
        self.conv_color = "#2962FF"
        self.base_color = "#B71C1C"
        self.lag_color = "#43A047"
        self.lead1_color = "#A5D6A7"
        self.lead2_color = "#EF9A9A"
        self.bull_cloud_alpha = 90
        self.bear_cloud_alpha = 90
        self.lead52_periods = 52
        self.lead52_color = "#FFD700"
        self.show_lead52 = True
        self._cloud_top = None
        self._cloud_bot = None
        self._conv = None
        self._base = None
        self._lead52 = None
        self.show_lagging = True
        self.show_conversion = True
        self.show_base = True
        self.show_lead1 = True
        self.show_lead2 = True
        self.show_cloud = True

    def set_config(self, cfg):
        self.conversionPeriods = cfg.get("ichimoku_conversion", 9)
        self.basePeriods = cfg.get("ichimoku_base", 26)
        self.laggingSpan2Periods = cfg.get("ichimoku_span2", 52)
        self.displacement = cfg.get("ichimoku_displacement", 26)
        self.conv_color = cfg.get("ichimoku_conv_color", "#2962FF")
        self.base_color = cfg.get("ichimoku_base_color", "#B71C1C")
        self.lag_color = cfg.get("ichimoku_lag_color", "#43A047")
        self.lead1_color = cfg.get("ichimoku_lead1_color", "#A5D6A7")
        self.lead2_color = cfg.get("ichimoku_lead2_color", "#EF9A9A")
        self.bull_cloud_alpha = cfg.get("ichimoku_bull_alpha", 90)
        self.bear_cloud_alpha = cfg.get("ichimoku_bear_alpha", 90)
        self.show_lagging = cfg.get("ichimoku_show_lag", True)
        self.show_conversion = cfg.get("ichimoku_show_conversion", True)
        self.show_base = cfg.get("ichimoku_show_base", True)
        self.show_lead1 = cfg.get("ichimoku_show_lead1", True)
        self.show_lead2 = cfg.get("ichimoku_show_lead2", True)
        self.show_cloud = cfg.get("ichimoku_show_cloud", True)
        self.lead52_periods = cfg.get("ichimoku_lead52_periods", 52)
        self.lead52_color = cfg.get("ichimoku_lead52_color", "#FFD700")
        self.show_lead52 = cfg.get("ichimoku_show_lead52", True)
        self.conv_width = cfg.get("ichimoku_conv_width", 1.5)
        self.base_width = cfg.get("ichimoku_base_width", 1.5)
        self.lag_width = cfg.get("ichimoku_lag_width", 1.0)
        self.lead1_width = cfg.get("ichimoku_lead1_width", 1.0)
        self.lead2_width = cfg.get("ichimoku_lead2_width", 1.0)
        self.lead52_width = cfg.get("ichimoku_lead52_width", 1.5)

    def get_config(self):
        return {
            "ichimoku_conversion": self.conversionPeriods,
            "ichimoku_base": self.basePeriods,
            "ichimoku_span2": self.laggingSpan2Periods,
            "ichimoku_displacement": self.displacement,
            "ichimoku_conv_color": self.conv_color,
            "ichimoku_base_color": self.base_color,
            "ichimoku_lag_color": self.lag_color,
            "ichimoku_lead1_color": self.lead1_color,
            "ichimoku_lead2_color": self.lead2_color,
            "ichimoku_bull_alpha": self.bull_cloud_alpha,
            "ichimoku_bear_alpha": self.bear_cloud_alpha,
            "ichimoku_show_lag": self.show_lagging,
            "ichimoku_show_conversion": self.show_conversion,
            "ichimoku_show_base": self.show_base,
            "ichimoku_show_lead1": self.show_lead1,
            "ichimoku_show_lead2": self.show_lead2,
            "ichimoku_show_cloud": self.show_cloud,
            "ichimoku_lead52_periods": self.lead52_periods,
            "ichimoku_lead52_color": self.lead52_color,
            "ichimoku_show_lead52": self.show_lead52,
            "ichimoku_conv_width": self.conv_width,
            "ichimoku_base_width": self.base_width,
            "ichimoku_lag_width": self.lag_width,
            "ichimoku_lead1_width": self.lead1_width,
            "ichimoku_lead2_width": self.lead2_width,
            "ichimoku_lead52_width": self.lead52_width,
        }

    def clear(self):
        for item in self._drawn:
            try:
                self.plot.removeItem(item)
            except Exception:
                pass
        self._drawn.clear()

    def draw(self, highs, lows, closes, x_indices):
        self.clear()
        n = len(closes)
        cp = self.conversionPeriods
        bp = self.basePeriods
        sp2 = self.laggingSpan2Periods
        disp = self.displacement

        if n < max(cp, bp, sp2, self.lead52_periods) + 1:
            return

        highs = np.array(highs, dtype=float)
        lows = np.array(lows, dtype=float)
        closes = np.array(closes, dtype=float)
        x_arr = np.array(x_indices, dtype=float)

        def donchian(length):
            result = np.full(n, np.nan)
            for i in range(length - 1, n):
                w_low = np.min(lows[i - length + 1:i + 1])
                w_high = np.max(highs[i - length + 1:i + 1])
                result[i] = (w_low + w_high) / 2.0
            return result

        conv = donchian(cp)
        base = donchian(bp)
        lead1 = np.where(~np.isnan(conv) & ~np.isnan(base),
                         (conv + base) / 2.0, np.nan)
        lead2 = donchian(sp2)
        lead52 = donchian(self.lead52_periods)

        lag_y = np.full(n, np.nan)
        for i in range(n):
            src = i + disp - 1
            if 0 <= src < n:
                lag_y[i] = closes[src]

        cloud_top = np.full(n, np.nan)
        cloud_bot = np.full(n, np.nan)
        for i in range(n):
            src = i - disp + 1
            if 0 <= src < n and not np.isnan(lead1[src]) and not np.isnan(lead2[src]):
                cloud_top[i] = max(lead1[src], lead2[src])
                cloud_bot[i] = min(lead1[src], lead2[src])

        self._conv = conv
        self._base = base
        self._lead1 = lead1
        self._lead2 = lead2
        self._lead52 = lead52
        self._lag_y = lag_y
        self._cloud_top = cloud_top
        self._cloud_bot = cloud_bot
        self._close = closes
        self._high = highs
        self._low = lows
        self._x_arr = x_arr
        self._disp = disp
        self._n = n

        pen_conv = pg.mkPen(self.conv_color, width=self.conv_width)
        pen_base = pg.mkPen(self.base_color, width=self.base_width)
        pen_lag = pg.mkPen(self.lag_color, width=self.lag_width)
        pen_lead1 = pg.mkPen(self.lead1_color, width=self.lead1_width)
        pen_lead2 = pg.mkPen(self.lead2_color, width=self.lead2_width)

        if self.show_conversion:
            conv_plot = pg.PlotDataItem()
            conv_plot.setData(x_arr, conv, pen=pen_conv)
            conv_plot.setZValue(10)
            self.plot.addItem(conv_plot)
            self._drawn.append(conv_plot)

        if self.show_base:
            base_plot = pg.PlotDataItem()
            base_plot.setData(x_arr, base, pen=pen_base)
            base_plot.setZValue(10)
            self.plot.addItem(base_plot)
            self._drawn.append(base_plot)

        if self.show_lagging:
            lag_plot = pg.PlotDataItem()
            lag_plot.setData(x_arr, lag_y, pen=pen_lag)
            lag_plot.setZValue(9)
            self.plot.addItem(lag_plot)
            self._drawn.append(lag_plot)

        lead_x = x_arr + (disp - 1)

        if self.show_lead1:
            lead1_plot = pg.PlotDataItem()
            lead1_plot.setData(lead_x, lead1, pen=pen_lead1)
            lead1_plot.setZValue(8)
            self.plot.addItem(lead1_plot)
            self._drawn.append(lead1_plot)

        if self.show_lead2:
            lead2_plot = pg.PlotDataItem()
            lead2_plot.setData(lead_x, lead2, pen=pen_lead2)
            lead2_plot.setZValue(8)
            self.plot.addItem(lead2_plot)
            self._drawn.append(lead2_plot)

        if self.show_lead52:
            pen_lead52 = pg.mkPen(self.lead52_color, width=self.lead52_width)
            lead52_plot = pg.PlotDataItem()
            lead52_plot.setData(x_arr, lead52, pen=pen_lead52)
            lead52_plot.setZValue(10)
            self.plot.addItem(lead52_plot)
            self._drawn.append(lead52_plot)

        if not self.show_cloud:
            return

        bull_a = int(255 * self.bull_cloud_alpha / 100)

        bull_a = int(255 * self.bull_cloud_alpha / 100)
        bear_a = int(255 * self.bear_cloud_alpha / 100)

        valid = [i for i in range(n) if not np.isnan(lead1[i]) and not np.isnan(lead2[i])]
        if len(valid) < 2:
            return

        from PyQt5.QtGui import QColor, QPen as QPenCls, QBrush
        from PyQt5.QtCore import Qt

        seg_start = 0
        while seg_start < len(valid) - 1:
            si = valid[seg_start]
            is_bull = lead1[si] > lead2[si]
            seg_end = seg_start + 1

            while seg_end < len(valid):
                ni = valid[seg_end]
                cur_bull = lead1[ni] > lead2[ni]
                if cur_bull != is_bull:
                    break
                seg_end += 1

            seg_indices = valid[seg_start:seg_end]
            if len(seg_indices) >= 2:
                sx = lead_x[seg_indices]
                sy1 = lead1[seg_indices]
                sy2 = lead2[seg_indices]

                if is_bull:
                    fill_color = QColor(67, 160, 71, bull_a)
                else:
                    fill_color = QColor(244, 67, 54, bear_a)

                brush = QBrush(fill_color)
                c1 = pg.PlotDataItem(sx, sy1)
                c2 = pg.PlotDataItem(sx, sy2)
                fill = pg.FillBetweenItem(c1, c2)
                fill.setBrush(brush)
                fill.setPen(QPenCls(Qt.NoPen))
                fill.setZValue(7)
                self.plot.addItem(c1)
                self.plot.addItem(c2)
                self.plot.addItem(fill)
                self._drawn.append(c1)
                self._drawn.append(c2)
                self._drawn.append(fill)

            seg_start = max(seg_start + 1, seg_end - 1)

Z = 1e18

# ============================================================
#              Candle Pattern Detection Functions
# ============================================================

def is_bullish_pin_bar(o, h, l, c):
    body = abs(c - o)
    if body < 1e-10:
        return False
    if c <= o:
        return False
    upper_wick = h - c
    lower_wick = o - l
    return lower_wick > body * 2.0 and upper_wick < body * 0.3

def is_bearish_pin_bar(o, h, l, c):
    body = abs(c - o)
    if body < 1e-10:
        return False
    if c >= o:
        return False
    upper_wick = h - o
    lower_wick = c - l
    return upper_wick > body * 2.0 and lower_wick < body * 0.3

def is_bullish_engulfing(o1, h1, l1, c1, o2, h2, l2, c2):
    if c2 <= o2:
        return False
    if c1 >= o1:
        return False
    body1 = abs(c1 - o1)
    body2 = abs(c2 - o2)
    return body2 > body1 and o2 < c1 and c2 > o1

def is_bearish_engulfing(o1, h1, l1, c1, o2, h2, l2, c2):
    if c2 >= o2:
        return False
    if c1 <= o1:
        return False
    body1 = abs(c1 - o1)
    body2 = abs(c2 - o2)
    return body2 > body1 and o2 > c1 and c2 < o1

def _calc_ichimoku_cloud(opens, highs, lows, closes, cp=9, bp=26, disp=26, span2=52):
    n = len(closes)
    def _donchian(arr_h, arr_l, length):
        res = np.full(n, np.nan)
        for i in range(length - 1, n):
            res[i] = (np.min(arr_l[i - length + 1:i + 1]) + np.max(arr_h[i - length + 1:i + 1])) / 2.0
        return res
    conv = _donchian(highs, lows, cp)
    base = _donchian(highs, lows, bp)
    lead1 = np.where(~np.isnan(conv) & ~np.isnan(base), (conv + base) / 2.0, np.nan)
    lead2 = _donchian(highs, lows, span2)
    cloud_top = np.full(n, np.nan)
    cloud_bot = np.full(n, np.nan)
    for i in range(n):
        src = i - disp + 1
        if 0 <= src < n and not np.isnan(lead1[src]) and not np.isnan(lead2[src]):
            cloud_top[i] = max(lead1[src], lead2[src])
            cloud_bot[i] = min(lead1[src], lead2[src])
    return cloud_top, cloud_bot, base

class MAIndicator:
    def __init__(self, plot_item):
        self.plot = plot_item
        self._items = []
        self._cfg = {}

    def set_config(self, cfg):
        self._cfg = cfg or {}

    def clear(self):
        for item in self._items:
            try:
                self.plot.removeItem(item)
            except Exception:
                pass
        self._items.clear()

    def draw(self, closes, x_indices):
        self.clear()
        cfg = self._cfg
        period = cfg.get("ma_period", 20)
        src = cfg.get("ma_source", "close")
        col = cfg.get("ma_color", "#e0af68")
        width = cfg.get("ma_width", 1.5)
        shift = cfg.get("ma_shift", 0)
        ma_type = cfg.get("ma_type", "SMA")

        n = len(closes)
        if n < period + 1:
            return

        prices = closes  # default to close
        # source not needed here since we just pass closes from outside

        if ma_type == "SMA":
            ma = np.full(n, np.nan)
            for i in range(period - 1, n):
                ma[i] = np.mean(closes[i - period + 1 : i + 1])
        elif ma_type == "EMA":
            ma = np.full(n, np.nan)
            mul = 2.0 / (period + 1)
            ma[period - 1] = np.mean(closes[:period])
            for i in range(period, n):
                ma[i] = (closes[i] - ma[i - 1]) * mul + ma[i - 1]
        else:
            return

        if shift != 0:
            shifted = np.full(n, np.nan)
            if shift > 0:
                shifted[shift:] = ma[:-shift]
            else:
                shifted[:shift] = ma[-shift:]
            ma = shifted

        valid = np.where(~np.isnan(ma))[0]
        if len(valid) < 2:
            return

        pen = pg.mkPen(color=col, width=width)
        curve = pg.PlotCurveItem(x_indices[valid], ma[valid], pen=pen)
        self.plot.addItem(curve)
        self._items.append(curve)

class MomentumEngine:
    TF_MAP = {
        "M1": mt5.TIMEFRAME_M1,
        "M2": mt5.TIMEFRAME_M2,
        "M3": mt5.TIMEFRAME_M3,
        "M5": mt5.TIMEFRAME_M5,
        "M10": mt5.TIMEFRAME_M10,
        "M15": mt5.TIMEFRAME_M15,
        "M30": mt5.TIMEFRAME_M30,
        "H1": mt5.TIMEFRAME_H1,
        "H4": mt5.TIMEFRAME_H4,
        "D1": mt5.TIMEFRAME_D1,
    }
    TF_WEIGHTS = {
        "M1": 0.03, "M2": 0.03, "M3": 0.04, "M5": 0.06, "M10": 0.08,
        "M15": 0.10, "M30": 0.12, "H1": 0.18, "H4": 0.20, "D1": 0.16,
    }

    @classmethod
    def _ema(cls, arr, period):
        alpha = 2.0 / (period + 1)
        out = np.empty_like(arr, dtype=np.float64)
        out[0] = arr[0]
        for i in range(1, len(arr)):
            out[i] = alpha * arr[i] + (1 - alpha) * out[i - 1]
        return out

    @classmethod
    def _rsi(cls, close, period=14):
        delta = np.diff(close)
        gain = np.where(delta > 0, delta, 0.0)
        loss = np.where(delta < 0, -delta, 0.0)
        avg_gain = np.empty(len(delta), dtype=np.float64)
        avg_loss = np.empty(len(delta), dtype=np.float64)
        avg_gain[period - 1] = np.mean(gain[:period])
        avg_loss[period - 1] = np.mean(loss[:period])
        for i in range(period, len(delta)):
            avg_gain[i] = (avg_gain[i - 1] * (period - 1) + gain[i]) / period
            avg_loss[i] = (avg_loss[i - 1] * (period - 1) + loss[i]) / period
        safe_loss = np.where(avg_loss > 0, avg_loss, 1.0)
        with np.errstate(over='ignore', divide='ignore'):
            rs = np.where(avg_loss > 0, np.clip(avg_gain / safe_loss, 0, 10000.0), 100.0)
        rsi = 100.0 - 100.0 / (1.0 + rs)
        return rsi

    @classmethod
    def calculate(cls, symbol, tf_name):
        tf = cls.TF_MAP.get(tf_name)
        if tf is None:
            return {"score": 0.0, "direction": "NEUTRAL"}
        try:
            tick = mt5.symbol_info_tick(symbol)
            to_date = datetime.datetime.fromtimestamp(tick.time, tz=datetime.timezone.utc)
        except Exception:
            to_date = datetime.datetime.now(datetime.timezone.utc)
        from_date = to_date - datetime.timedelta(days=30)
        rates = MT5Connector.get_rates(symbol, tf, from_date, to_date)
        if rates is None or len(rates) < 30:
            return {"score": 0.0, "direction": "NEUTRAL"}
        df = pd.DataFrame(rates)
        df.columns = [c.lower() for c in df.columns]
        close = df["close"].values.astype(np.float64)
        high = df["high"].values.astype(np.float64)
        low = df["low"].values.astype(np.float64)
        rsi_arr = cls._rsi(close, 14)
        rsi_val = float(rsi_arr[-1]) if len(rsi_arr) > 0 else 50.0
        rsi_score = ((rsi_val - 50) / 50) * 10
        ema20 = cls._ema(close, 20)
        ema50 = cls._ema(close, 50) if len(close) >= 50 else ema20
        if len(ema20) > 5 and ema20[-5] > 0:
            ema_slope = (ema20[-1] - ema20[-5]) / ema20[-5] * 100
        else:
            ema_slope = 0.0
        ema_score = np.clip(ema_slope * 10, -10, 10)
        ema12 = cls._ema(close, 12)
        ema26 = cls._ema(close, 26)
        macd_line = ema12 - ema26
        signal_line = cls._ema(macd_line, 9)
        macd_diff = float(macd_line[-1] - signal_line[-1]) if len(macd_line) > 0 else 0.0
        price_range = float(np.max(close[-20:]) - np.min(close[-20:])) if len(close) >= 20 else 1.0
        if price_range < 1e-10:
            price_range = 1.0
        macd_score = np.clip(macd_diff / price_range * 400, -10, 10)
        if len(close) >= 6:
            roc = (close[-1] - close[-6]) / close[-6] * 100
        else:
            roc = 0.0
        roc_score = np.clip(roc * 5, -10, 10)
        atr_period = min(14, len(high) - 1)
        if atr_period >= 1:
            tr_arr = np.maximum(high[1:] - low[1:],
                     np.maximum(np.abs(high[1:] - close[:-1]),
                                np.abs(low[1:] - close[:-1])))
            atr = float(np.mean(tr_arr[-atr_period:])) if len(tr_arr) >= atr_period else price_range
        else:
            atr = price_range
        body = close[-1] - df["open"].values[-1]
        candle_strength = body / atr * 10 if atr > 1e-10 else 0.0
        candle_score = np.clip(candle_strength, -10, 10)
        score = (rsi_score * 0.25) + (macd_score * 0.25) + (ema_score * 0.25) + \
                (roc_score * 0.15) + (candle_score * 0.10)
        score = float(np.clip(score, -10, 10))
        above_ema20 = close[-1] > ema20[-1] if len(ema20) > 0 else True
        above_ema50 = close[-1] > ema50[-1] if len(ema50) > 0 else True
        ema_bullish = above_ema20 and above_ema50
        ema_bearish = not above_ema20 and not above_ema50
        if score > 1 and (ema_bullish or above_ema20):
            direction = "BUY"
        elif score < -1 and (ema_bearish or not above_ema20):
            direction = "SELL"
        else:
            direction = "NEUTRAL"
        return {"score": round(score, 2), "direction": direction,
                "rsi": round(rsi_val, 1), "ema_slope": round(ema_slope, 3),
                "roc": round(roc, 3)}

    @classmethod
    def calculate_all(cls, symbol):
        result = {}
        for tf_name in cls.TF_MAP:
            result[tf_name] = cls.calculate(symbol, tf_name)
        combined = 0.0
        total_w = 0.0
        buy_votes = 0.0
        sell_votes = 0.0
        total_votes = 0.0
        for tf_name, w in cls.TF_WEIGHTS.items():
            s = result.get(tf_name, {}).get("score", 0.0)
            d = result.get(tf_name, {}).get("direction", "NEUTRAL")
            combined += s * w
            total_w += w
            if d == "BUY":
                buy_votes += w
            elif d == "SELL":
                sell_votes += w
            total_votes += w
        if total_w > 0:
            combined /= total_w
        combined = round(float(np.clip(combined, -10, 10)), 2)
        if total_votes > 0:
            buy_pct = buy_votes / total_votes
            sell_pct = sell_votes / total_votes
        else:
            buy_pct = sell_pct = 0.0
        if combined > 2 and buy_pct > 0.25:
            overall_dir = "BUY"
        elif combined < -2 and sell_pct > 0.25:
            overall_dir = "SELL"
        else:
            overall_dir = "NEUTRAL"
        result["combined"] = {"score": combined, "direction": overall_dir,
                              "buy_pct": round(buy_pct * 100, 1),
                              "sell_pct": round(sell_pct * 100, 1)}
        result["scenario"] = cls._build_scenario(result, overall_dir, combined,
                                                 buy_pct, sell_pct)
        return result

    @classmethod
    def _build_scenario(cls, scores, direction, combined, buy_pct, sell_pct):
        bullish_tfs = []
        bearish_tfs = []
        neutral_tfs = []
        for tf_name in cls.TF_MAP:
            d = scores.get(tf_name, {}).get("direction", "NEUTRAL")
            s = scores.get(tf_name, {}).get("score", 0.0)
            if d == "BUY":
                bullish_tfs.append((tf_name, s))
            elif d == "SELL":
                bearish_tfs.append((tf_name, s))
            else:
                neutral_tfs.append((tf_name, s))
        if direction == "BUY":
            main = "BUY (Long)"
            color = "green"
        elif direction == "SELL":
            main = "SELL (Short)"
            color = "red"
        else:
            main = "NEUTRAL - Wait"
            color = "yellow"
        lines = []
        lines.append(f"{'='*35}")
        lines.append(f"SCENARIO: {main}")
        lines.append(f"Score: {combined:+.1f} | BUY: {buy_pct*100:.0f}% | SELL: {sell_pct*100:.0f}%")
        lines.append(f"{'='*35}")
        if bullish_tfs:
            names = ", ".join([f"{n}({s:+.1f})" for n, s in bullish_tfs])
            lines.append(f"BUY Trend: {names}")
        if bearish_tfs:
            names = ", ".join([f"{n}({s:+.1f})" for n, s in bearish_tfs])
            lines.append(f"SELL Trend: {names}")
        if neutral_tfs:
            names = ", ".join([f"{n}({s:+.1f})" for n, s in neutral_tfs])
            lines.append(f"Neutral: {names}")
        lines.append(f"{'-'*35}")
        if direction == "BUY":
            if buy_pct >= 70:
                strength = "STRONG"
            elif buy_pct >= 50:
                strength = "MODERATE"
            else:
                strength = "WEAK"
            lines.append(f"Strength: {strength} BUY")
            lines.append(f"Entry: Market Price (above EMA20)")
            lines.append(f"SL: Below recent swing low")
            lines.append(f"TP: +1:1 risk-reward ratio")
            lines.append(f"Note: {len(bullish_tfs)}/10 TFs bullish")
        elif direction == "SELL":
            if sell_pct >= 70:
                strength = "STRONG"
            elif sell_pct >= 50:
                strength = "MODERATE"
            else:
                strength = "WEAK"
            lines.append(f"Strength: {strength} SELL")
            lines.append(f"Entry: Market Price (below EMA20)")
            lines.append(f"SL: Above recent swing high")
            lines.append(f"TP: +1:1 risk-reward ratio")
            lines.append(f"Note: {len(bearish_tfs)}/10 TFs bearish")
        else:
            lines.append(f"Strength: NO SIGNAL")
            lines.append(f"Action: WAIT for alignment")
            if len(bullish_tfs) > len(bearish_tfs):
                lines.append(f"Watch: {len(bullish_tfs)} buy vs {len(bearish_tfs)} sell")
                lines.append(f"Possible shift to BUY if more TFs align")
            elif len(bearish_tfs) > len(bullish_tfs):
                lines.append(f"Watch: {len(bearish_tfs)} sell vs {len(bullish_tfs)} buy")
                lines.append(f"Possible shift to SELL if more TFs align")
            else:
                lines.append(f"Mixed signals - no clear direction")
        lines.append(f"{'='*35}")
        return "\n".join(lines)

class SignalPopup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFixedWidth(340)
        self._opacity = 1.0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._fade_out)
        self._fade_timer = QTimer(self)
        self._fade_timer.timeout.connect(self._reduce_opacity)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        self._bg_label = QLabel()
        self._bg_label.setStyleSheet("background:rgba(15,15,30,240);border:2px solid #565f89;border-radius:10px;")
        bg_layout = QVBoxLayout(self._bg_label)
        bg_layout.setContentsMargins(14, 10, 14, 10)
        self._title_label = QLabel()
        self._title_label.setAlignment(QtCore.Qt.AlignCenter)
        self._title_label.setStyleSheet("color:#c0caf5;font-size:14px;font-weight:bold;background:transparent;border:none;")
        bg_layout.addWidget(self._title_label)
        self._signal_label = QLabel()
        self._signal_label.setAlignment(QtCore.Qt.AlignCenter)
        self._signal_label.setStyleSheet("font-size:22px;font-weight:bold;background:transparent;border:none;")
        bg_layout.addWidget(self._signal_label)
        self._score_label = QLabel()
        self._score_label.setAlignment(QtCore.Qt.AlignCenter)
        self._score_label.setStyleSheet("color:#565f89;font-size:11px;background:transparent;border:none;")
        bg_layout.addWidget(self._score_label)
        sep = QLabel()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color:#565f89;border:none;")
        bg_layout.addWidget(sep)
        self._detail_label = QLabel()
        self._detail_label.setStyleSheet("color:#a9b1d6;font-size:10px;background:transparent;border:none;")
        self._detail_label.setWordWrap(True)
        bg_layout.addWidget(self._detail_label)
        layout.addWidget(self._bg_label)
        self.setLayout(layout)

    def show_signal(self, direction, score, scenario):
        if direction == "BUY":
            self._title_label.setText("SIGNAL DETECTED")
            self._signal_label.setText("▲ BUY")
            self._signal_label.setStyleSheet("color:#26a69a;font-size:22px;font-weight:bold;background:transparent;border:none;")
            self._signal_label.setStyleSheet("color:#26a69a;font-size:22px;font-weight:bold;background:transparent;border:none;")
        elif direction == "SELL":
            self._title_label.setText("SIGNAL DETECTED")
            self._signal_label.setText("▼ SELL")
            self._signal_label.setStyleSheet("color:#ef5350;font-size:22px;font-weight:bold;background:transparent;border:none;")
        else:
            return
        self._score_label.setText(f"Score: {score:+.1f}")
        lines = scenario.split("\n")
        detail_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("BUY Trend:") or stripped.startswith("SELL Trend:"):
                detail_lines.append(stripped)
            elif stripped.startswith("Strength:"):
                detail_lines.append(stripped)
            elif stripped.startswith("Entry:"):
                detail_lines.append(stripped)
            elif stripped.startswith("SL:"):
                detail_lines.append(stripped)
            elif stripped.startswith("TP:"):
                detail_lines.append(stripped)
            elif stripped.startswith("Note:"):
                detail_lines.append(stripped)
        self._detail_label.setText("\n".join(detail_lines))
        self.adjustSize()
        self._opacity = 1.0
        self.setWindowOpacity(1.0)
        self.show()
        self.raise_()
        self.activateWindow()
        if self.parent():
            pg = self.parent().mapToGlobal(self.parent().rect().topRight())
            self.move(pg.x() - self.width() - 20, pg.y() + 60)
        self._timer.start(5000)
        self._fade_timer.stop()

    def _fade_out(self):
        self._timer.stop()
        self._fade_timer.start(30)

    def _reduce_opacity(self):
        self._opacity -= 0.05
        if self._opacity <= 0:
            self._fade_timer.stop()
            self.hide()
        else:
            self.setWindowOpacity(self._opacity)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 0)))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRect(self.rect())
        painter.end()

class MomentumBarWidget(QWidget):
    TF_ORDER = ["M1", "M2", "M3", "M5", "M10", "M15", "M30", "H1", "H4", "D1"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setMinimumWidth(420)
        self._score = 0.0
        self._direction = "NEUTRAL"
        self._scores_tf = {}
        self._directions_tf = {}
        self._scenario = ""
        self._buy_pct = 0.0
        self._sell_pct = 0.0
        self._signal_strength = "NONE"

    def set_scores(self, scores_dict):
        self._scores_tf = dict(scores_dict)
        self._score = scores_dict.get("BIA", 0.0)
        combined = scores_dict.get("_combined", {})
        self._direction = combined.get("direction", "NEUTRAL")
        self._buy_pct = combined.get("buy_pct", 0)
        self._sell_pct = combined.get("sell_pct", 0)
        self._scenario = combined.get("scenario", "")
        for k in self.TF_ORDER:
            if k in scores_dict:
                v = scores_dict[k]
                if isinstance(v, dict):
                    self._scores_tf[k] = v.get("score", 0.0)
                    self._directions_tf[k] = v.get("direction", "NEUTRAL")
                else:
                    self._scores_tf[k] = float(v)
                    self._directions_tf[k] = "BUY" if v > 0.5 else ("SELL" if v < -0.5 else "NEUTRAL")
        buy_tfs = sum(1 for d in self._directions_tf.values() if d == "BUY")
        sell_tfs = sum(1 for d in self._directions_tf.values() if d == "SELL")
        if self._direction == "BUY" and self._buy_pct >= 70:
            self._signal_strength = "STRONG BUY"
        elif self._direction == "BUY":
            self._signal_strength = "MOD BUY"
        elif self._direction == "SELL" and self._sell_pct >= 70:
            self._signal_strength = "STRONG SELL"
        elif self._direction == "SELL":
            self._signal_strength = "MOD SELL"
        else:
            self._signal_strength = "NO SIGNAL"
        tip_lines = [self._scenario]
        self.setToolTip("\n".join(tip_lines))
        self.update()

    @staticmethod
    def _score_color(score):
        if score > 5:
            return "#26a69a"
        elif score > 2:
            return "#4db6ac"
        elif score > -2:
            return "#d4ac0d"
        elif score > -5:
            return "#e57373"
        else:
            return "#ef5350"

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        w = self.width()
        h = self.height()
        mid_y = h // 2
        tf_area_w = min(w * 0.55, 250)
        tf_start_x = 4
        tf_w = max(18, tf_area_w / len(self.TF_ORDER) - 2)
        for i, tf_name in enumerate(self.TF_ORDER):
            x = tf_start_x + i * (tf_w + 2)
            s = self._scores_tf.get(tf_name, 0.0)
            d = self._directions_tf.get(tf_name, "NEUTRAL")
            color = QtGui.QColor(self._score_color(s))
            bar_h = max(2, abs(s) / 10.0 * 10)
            if s >= 0:
                bar_rect = QtCore.QRectF(x, mid_y - bar_h, tf_w, bar_h)
            else:
                bar_rect = QtCore.QRectF(x, mid_y, tf_w, bar_h)
            painter.setBrush(QtGui.QBrush(color))
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawRect(bar_rect)
            painter.setPen(QtGui.QPen(QtGui.QColor("#565f89")))
            painter.setFont(QtGui.QFont("Segoe UI", 5))
            painter.drawText(QtCore.QRectF(x - 1, h - 10, tf_w + 2, 10),
                             QtCore.Qt.AlignHCenter, tf_name)
            if d == "BUY":
                painter.setPen(QtGui.QPen(QtGui.QColor("#26a69a")))
                painter.setFont(QtGui.QFont("Segoe UI", 6, QtGui.QFont.Bold))
                painter.drawText(QtCore.QRectF(x - 1, 0, tf_w + 2, 9),
                                 QtCore.Qt.AlignHCenter, "▲")
            elif d == "SELL":
                painter.setPen(QtGui.QPen(QtGui.QColor("#ef5350")))
                painter.setFont(QtGui.QFont("Segoe UI", 6, QtGui.QFont.Bold))
                painter.drawText(QtCore.QRectF(x - 1, 0, tf_w + 2, 9),
                                 QtCore.Qt.AlignHCenter, "▼")
        candle_area_x = tf_start_x + tf_area_w + 12
        candle_w = max(w * 0.12, 20)
        candle_mid_x = candle_area_x + candle_w / 2
        score = self._score
        body_half_h = 6
        max_wick = candle_w * 0.8
        body_w = max(3, abs(score) / 10.0 * max_wick)
        color = QtGui.QColor(self._score_color(score))
        vals = [self._scores_tf.get(k, 0) for k in self.TF_ORDER if k in self._scores_tf]
        if vals:
            wr = max(vals)
            wl = min(vals)
            scale = max_wick / 10.0
            wr_x = candle_mid_x + wr * scale
            wl_x = candle_mid_x + wl * scale
        else:
            wr_x = candle_mid_x + body_w
            wl_x = candle_mid_x
        painter.setPen(QtGui.QPen(color, 1.2))
        painter.drawLine(QtCore.QPointF(wl_x, mid_y), QtCore.QPointF(wr_x, mid_y))
        if score >= 0:
            body_rect = QtCore.QRectF(candle_mid_x, mid_y - body_half_h, body_w, body_half_h * 2)
        else:
            body_rect = QtCore.QRectF(candle_mid_x - body_w, mid_y - body_half_h, body_w, body_half_h * 2)
        painter.setBrush(QtGui.QBrush(color))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRect(body_rect)
        painter.setPen(QtGui.QPen(QtGui.QColor("#c0caf5")))
        painter.setFont(QtGui.QFont("Segoe UI", 6, QtGui.QFont.Bold))
        painter.drawText(QtCore.QRectF(candle_area_x - 5, 0, candle_w + 10, 9),
                         QtCore.Qt.AlignHCenter, "MOM")
        painter.setPen(QtGui.QPen(QtGui.QColor("#565f89")))
        painter.setFont(QtGui.QFont("Segoe UI", 6))
        painter.drawText(QtCore.QRectF(candle_area_x - 5, h - 10, candle_w + 10, 10),
                         QtCore.Qt.AlignHCenter, f"{score:+.1f}")
        dir_x = candle_area_x + candle_w + 8
        dir = self._direction
        if dir == "BUY":
            bg = "#26a69a"
            label = self._signal_strength
            painter.setPen(QtGui.QPen(QtGui.QColor("#000000"), 1))
            painter.setBrush(QtGui.QBrush(QtGui.QColor(bg)))
            painter.setFont(QtGui.QFont("Segoe UI", 9, QtGui.QFont.Bold))
            tw = painter.fontMetrics().horizontalAdvance(label) + 10
            painter.drawRoundedRect(QtCore.QRectF(dir_x, mid_y - 10, tw, 20), 3, 3)
            painter.setPen(QtGui.QPen(QtGui.QColor("#000000")))
            painter.drawText(QtCore.QRectF(dir_x, mid_y - 10, tw, 20),
                             QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter, label)
        elif dir == "SELL":
            bg = "#ef5350"
            label = self._signal_strength
            painter.setPen(QtGui.QPen(QtGui.QColor("#000000"), 1))
            painter.setBrush(QtGui.QBrush(QtGui.QColor(bg)))
            painter.setFont(QtGui.QFont("Segoe UI", 9, QtGui.QFont.Bold))
            tw = painter.fontMetrics().horizontalAdvance(label) + 10
            painter.drawRoundedRect(QtCore.QRectF(dir_x, mid_y - 10, tw, 20), 3, 3)
            painter.setPen(QtGui.QPen(QtGui.QColor("#ffffff")))
            painter.drawText(QtCore.QRectF(dir_x, mid_y - 10, tw, 20),
                             QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter, label)
        else:
            painter.setPen(QtGui.QPen(QtGui.QColor("#565f89")))
            painter.setFont(QtGui.QFont("Segoe UI", 7))
            painter.drawText(QtCore.QRectF(dir_x, mid_y - 10, w - dir_x, 20),
                             QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft, "WAIT")
        painter.end()


class SignalNotifyWidget(QtWidgets.QFrame):
    """Popup notification for multi-symbol signals"""
    symbol_clicked = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool |
            QtCore.Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
        self.setFixedWidth(360)
        self.setFixedHeight(80)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self._current_symbol = ""
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)
        self._icon = QtWidgets.QLabel("🔔")
        self._icon.setStyleSheet("font-size: 28px; background: transparent;")
        self._icon.setFixedWidth(36)
        layout.addWidget(self._icon)
        text_layout = QtWidgets.QVBoxLayout()
        text_layout.setSpacing(2)
        self._title = QtWidgets.QLabel("")
        self._title.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 13px; background: transparent;")
        text_layout.addWidget(self._title)
        self._detail = QtWidgets.QLabel("")
        self._detail.setStyleSheet("color: #b2b5be; font-size: 10px; background: transparent;")
        text_layout.addWidget(self._detail)
        layout.addLayout(text_layout, stretch=1)
        self._pos = None
        self._hide_timer = QtCore.QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self.hide)

    def show_alert(self, symbol, direction, price, tf="", msg=""):
        self._current_symbol = symbol
        color = "#26a641" if "buy" in direction.lower() else "#f5222d"
        arrow = "▲ BUY" if "buy" in direction.lower() else "▼ SELL"
        self._icon.setText("🟢" if "buy" in direction.lower() else "🔴")
        self._title.setText(f"{symbol}  {arrow}")
        self._title.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 14px; background: transparent;")
        detail = f"Price: {price:.5f}"
        if tf:
            detail += f"  |  TF: {tf}"
        if msg:
            detail += f"  |  {msg}"
        self._detail.setText(detail)
        self.setStyleSheet(f"""
            SignalNotifyWidget {{
                background: #1a1b2e;
                border: 2px solid {color};
                border-radius: 10px;
            }}
        """)
        self.show()
        self.raise_()
        self.activateWindow()
        self._hide_timer.start(8000)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._pos and event.buttons() & QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self._pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if self._pos:
            new_pos = event.globalPos()
            start_pos = self._pos + self.frameGeometry().topLeft()
            if (new_pos - start_pos).manhattanLength() < 5 and self._current_symbol:
                self.symbol_clicked.emit(self._current_symbol)
        self._pos = None

    def mouseDoubleClickEvent(self, event):
        if self._current_symbol:
            self.symbol_clicked.emit(self._current_symbol)
            self.hide()


class MultiSymbolScanner(QtCore.QTimer):
    """Background scanner - monitors watchlist for zone-level signals (Weekly/Daily/H4/H1)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setInterval(5000)
        self.timeout.connect(self._scan_tick)
        self._last_signals = {}
        self._enabled = False
        self._symbols = []
        self._callbacks = []
        self._scan_tf = "M15"
        self._zone_cfg = {}
        self._zone_checkboxes = {}

    def configure(self, symbols, enabled=True, scan_tf="M15", zone_cfg=None, zone_checkboxes=None, scan_interval=5, signal_tfs=None, chart_tfs=None, sound_alarm=True, popup_notify=True):
        self._symbols = list(symbols)
        self._enabled = enabled
        self._scan_tf = scan_tf
        self._zone_cfg = zone_cfg or {}
        self._zone_checkboxes = zone_checkboxes or {}
        self._signal_tfs = signal_tfs or {"Weekly": True, "Daily": True, "H4": True, "H1": True}
        self._chart_tfs = chart_tfs or {"M15": True}
        self._sound_alarm = sound_alarm
        self._popup_notify = popup_notify
        self.setInterval(scan_interval * 1000)
        if enabled and self._symbols:
            if not self.isActive():
                self.start()
        else:
            self.stop()

    def add_callback(self, cb):
        self._callbacks.append(cb)

    def _scan_tick(self):
        if not self._enabled or not self._symbols:
            return
        import MetaTrader5 as mt5
        zone_tfs = {
            "Weekly": mt5.TIMEFRAME_W1,
            "Daily": mt5.TIMEFRAME_D1,
            "H4": mt5.TIMEFRAME_H4,
            "H1": mt5.TIMEFRAME_H1,
        }
        for symbol in self._symbols:
            try:
                self._check_symbol(symbol, zone_tfs)
            except Exception:
                continue

    @staticmethod
    def _find_level_candle(rates):
        if rates is None or len(rates) < 3:
            return rates[-2] if rates is not None and len(rates) >= 2 else None
        n = len(rates)
        for i in range(n - 2, 0, -1):
            close_i = float(rates[i]['close'])
            high_prev = float(rates[i - 1]['high'])
            low_prev = float(rates[i - 1]['low'])
            if close_i > high_prev or close_i < low_prev:
                return rates[i]
        return rates[-2]

    def _check_symbol(self, symbol, zone_tfs):
        import MetaTrader5 as mt5

        info = mt5.symbol_info(symbol)
        if not info:
            return
        pip = info.point * 10 if info.point <= 0.001 else info.point

        chart_tf_map = {
            "M1": mt5.TIMEFRAME_M1, "M2": mt5.TIMEFRAME_M2, "M3": mt5.TIMEFRAME_M3,
            "M5": mt5.TIMEFRAME_M5, "M10": mt5.TIMEFRAME_M10, "M15": mt5.TIMEFRAME_M15,
            "M30": mt5.TIMEFRAME_M30,
        }

        enabled_chart_tfs = [tf for tf, on in self._chart_tfs.items() if on and tf in chart_tf_map]
        if not enabled_chart_tfs:
            enabled_chart_tfs = ["M15"]

        for zone_name in ["Weekly", "Daily", "H4", "H1"]:
            if not self._signal_tfs.get(zone_name, True):
                continue
            if not self._zone_checkboxes.get(zone_name, False):
                continue

            zone_tf = zone_tfs[zone_name]
            zone_rates = mt5.copy_rates_from_pos(symbol, zone_tf, 0, 50)
            if zone_rates is None or len(zone_rates) < 3:
                continue
            level_candle = self._find_level_candle(zone_rates)
            if level_candle is None:
                continue
            zone_high = float(level_candle['high'])
            zone_low = float(level_candle['low'])

            if zone_high <= 0 or zone_low <= 0:
                continue

            for ctf_name in enabled_chart_tfs:
                ctf_code = chart_tf_map[ctf_name]
                chart_rates = mt5.copy_rates_from_pos(symbol, ctf_code, 0, 5)
                if chart_rates is None or len(chart_rates) < 3:
                    continue

                last_closed = chart_rates[-2]
                c_high = float(last_closed['high'])
                c_low = float(last_closed['low'])
                c_close = float(last_closed['close'])

                is_long = False
                is_short = False

                if c_high >= zone_high and c_close < zone_high:
                    is_short = True
                elif c_low <= zone_low and c_close > zone_low:
                    is_long = True
                else:
                    continue

                direction = "buy" if is_long else "sell"
                sig_key = f"{symbol}_{zone_name}_{ctf_name}"
                prev = self._last_signals.get(sig_key, None)
                if prev == direction:
                    continue
                self._last_signals[sig_key] = direction

                if is_long:
                    msg = f"{symbol} closed above {zone_name} Low ({zone_low:.5f}) on {ctf_name} -> BUY"
                else:
                    msg = f"{symbol} closed below {zone_name} High ({zone_high:.5f}) on {ctf_name} -> SELL"
                for cb in self._callbacks:
                    cb(symbol, direction, c_close, ctf_name, msg)


class CandleTimerWidget(QtWidgets.QFrame):
    """Floating panel showing time remaining until candle close"""
    TF_SECONDS = {
        "D1": 86400, "H4": 14400, "H1": 3600,
        "M30": 1800, "M15": 900, "M10": 600, "M5": 300,
    }
    TF_LABELS = {
        "D1": "Daily", "H4": "4 Hour", "H1": "1 Hour",
        "M30": "30 Min", "M15": "15 Min", "M10": "10 Min", "M5": "5 Min",
    }
    COLORS = {
        "D1": "#e0af68", "H4": "#bb9af7", "H1": "#7aa2f7",
        "M30": "#9ece6a", "M15": "#f7768e", "M10": "#ff9e64", "M5": "#73daca",
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            CandleTimerWidget {
                background: #1a1b2e;
                border: 2px solid #363A45;
                border-radius: 10px;
            }
        """)
        self.setFixedWidth(460)
        self.setMinimumHeight(280)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(0)
        title = QtWidgets.QLabel("CANDLE TIMER")
        title.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 15px; padding: 8px; background: #24283b; border-radius: 6px; margin-bottom: 6px;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)
        header = QtWidgets.QHBoxLayout()
        header.setContentsMargins(70, 0, 75, 0)
        for lbl_text in ["Prev", "Curr"]:
            h = QtWidgets.QLabel(lbl_text)
            h.setStyleSheet("color:#565f89;font-size:9px;font-weight:bold;background:transparent;")
            h.setAlignment(QtCore.Qt.AlignCenter)
            h.setFixedWidth(28)
            header.addWidget(h)
        layout.addLayout(header)
        self._labels = {}
        self._candle_dots = {}
        for tf in ["D1", "H4", "H1", "M30", "M15", "M10", "M5"]:
            frame = QtWidgets.QFrame()
            frame.setStyleSheet("QFrame { background: #1a1b2e; border: none; }")
            row = QtWidgets.QHBoxLayout(frame)
            row.setContentsMargins(4, 6, 4, 6)
            row.setSpacing(6)
            name_lbl = QtWidgets.QLabel(self.TF_LABELS[tf])
            name_lbl.setStyleSheet(f"color: {self.COLORS[tf]}; font-size: 13px; font-weight: bold; background: transparent;")
            name_lbl.setFixedWidth(60)
            row.addWidget(name_lbl)
            prev_dot = QtWidgets.QLabel()
            prev_dot.setFixedSize(20, 20)
            prev_dot.setStyleSheet("background:#292e42;border:1px solid #363A45;border-radius:10px;")
            prev_dot.setAlignment(QtCore.Qt.AlignCenter)
            row.addWidget(prev_dot)
            curr_dot = QtWidgets.QLabel()
            curr_dot.setFixedSize(20, 20)
            curr_dot.setStyleSheet("background:#292e42;border:1px solid #363A45;border-radius:10px;")
            curr_dot.setAlignment(QtCore.Qt.AlignCenter)
            row.addWidget(curr_dot)
            bar = QtWidgets.QProgressBar()
            bar.setFixedHeight(20)
            bar.setRange(0, 100)
            bar.setTextVisible(False)
            bar.setStyleSheet(f"""
                QProgressBar {{ background: #24283b; border: 1px solid #292e42; border-radius: 5px; }}
                QProgressBar::chunk {{ background: {self.COLORS[tf]}; border-radius: 4px; }}
            """)
            row.addWidget(bar, stretch=1)
            time_lbl = QtWidgets.QLabel("00:00")
            time_lbl.setStyleSheet(f"color: {self.COLORS[tf]}; font-size: 14px; font-weight: bold; font-family: monospace; background: transparent;")
            time_lbl.setFixedWidth(65)
            time_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            row.addWidget(time_lbl)
            layout.addWidget(frame)
            self._labels[tf] = (bar, time_lbl)
            self._candle_dots[tf] = (prev_dot, curr_dot)
        self._pos = None

    def update_timers(self, now_ts):
        for tf, tf_sec in self.TF_SECONDS.items():
            bar, time_lbl = self._labels[tf]
            seconds_into = now_ts % tf_sec
            remaining = tf_sec - seconds_into
            pct = int((1 - remaining / tf_sec) * 100)
            bar.setValue(pct)
            h = int(remaining) // 3600
            m = (int(remaining) % 3600) // 60
            s = int(remaining) % 60
            if h > 0:
                time_lbl.setText(f"{h:02d}:{m:02d}:{s:02d}")
            else:
                time_lbl.setText(f"{m:02d}:{s:02d}")

    def update_candle_colors(self, tf, prev_bullish, curr_bullish):
        if tf not in self._candle_dots:
            return
        prev_dot, curr_dot = self._candle_dots[tf]
        prev_color = "#26a641" if prev_bullish else "#f5222d"
        curr_color = "#26a641" if curr_bullish else "#f5222d"
        prev_icon = "\u25B2" if prev_bullish else "\u25BC"
        curr_icon = "\u25B2" if curr_bullish else "\u25BC"
        prev_dot.setText(prev_icon)
        prev_dot.setStyleSheet(f"color:{prev_color};background:#1a1b2e;border:2px solid {prev_color};border-radius:10px;font-size:10px;font-weight:bold;")
        curr_dot.setText(curr_icon)
        curr_dot.setStyleSheet(f"color:{curr_color};background:#1a1b2e;border:2px solid {curr_color};border-radius:10px;font-size:10px;font-weight:bold;")

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._pos and event.buttons() & QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self._pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._pos = None


class AlgomanDashboardWidget(QtWidgets.QFrame):
    """Floating dashboard for AlgoMan indicator - matching Pine Script colors"""
    BG = "#2A2E39"
    FRAME = "#2A2E39"
    BORDER = "#363A45"
    BULL = "#00DD00"
    BEAR = "#DD0000"
    NEUTRAL = "#B2B5BE"
    WARN = "#FF9800"
    TXT = "#FFFFFF"
    TXT_DIM = "#B2B5BE"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet(f"background: rgba(42, 46, 57, 240); border: 1px solid {self.BORDER}; border-radius: 6px;")
        self.setFixedWidth(230)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(2)
        self.title = QtWidgets.QLabel("ALGOMAN NEXT")
        self.title.setStyleSheet(f"color: {self.TXT}; font-weight: bold; font-size: 11px; padding: 3px; background: #1a1b2e; border-radius: 4px;")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.title)
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["", ""])
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(False)
        self.table.verticalHeader().setDefaultSectionSize(20)
        self.table.verticalHeader().setMinimumSectionSize(20)
        self.table.setColumnWidth(0, 115)
        self.table.setColumnWidth(1, 95)
        self.table.setStyleSheet(f"""
            QTableWidget {{ background: transparent; color: {self.TXT_DIM}; font-size: 10px; border: none; }}
            QTableWidget::item {{ padding: 1px 4px; }}
        """)
        layout.addWidget(self.table)
        self._pos = None

    def _make_item(self, text, bg=None, fg="#c0caf5", bold=False):
        item = QtWidgets.QTableWidgetItem(text)
        item.setForeground(QtGui.QColor(fg))
        if bg:
            item.setBackground(QtGui.QColor(bg))
        if bold:
            font = item.font()
            font.setBold(True)
            item.setFont(font)
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        return item

    def _status_bg(self, val, bull_color=None, bear_color=None, warn_color=None):
        bc = bull_color or self.BULL
        rc = bear_color or self.BEAR
        wc = warn_color or self.WARN
        if val in ("Bullish", "Buy", "Trending"):
            return bc
        elif val in ("Bearish", "Sell"):
            return rc
        elif val in ("Ranging",):
            return wc
        return None

    def update_data(self, data):
        rows = []
        rows.append(("Strategy", data.get("strategy", "Normal"), None, self.TXT_DIM, False, None))
        rows.append(("Sensitivity", str(data.get("sensitivity", 1.8)), None, self.TXT_DIM, False, None))
        pos = data.get("position", "Sell")
        rows.append(("Position", pos, self._status_bg(pos), self.TXT, True, None))
        trend = data.get("trend", "Bearish")
        rows.append(("Trend", trend, self._status_bg(trend), self.TXT, True, None))
        strength = data.get("strength", 0)
        s_color = self.BULL if strength > 0 else self.BEAR
        rows.append(("Strength", f"{strength:.1f} %", None, s_color, True, None))
        vol = data.get("volume", "Bearish")
        rows.append(("Volume", vol, self._status_bg(vol), self.TXT, False, None))
        volat = data.get("volatility", "Ranging")
        rows.append(("Volatility", volat, self._status_bg(volat), self.TXT, False, None))
        mom = data.get("momentum", "Bearish")
        rows.append(("Momentum", mom, self._status_bg(mom), self.TXT, False, None))
        rows.append(("", "", self.BORDER, None, False, None))
        rows.append(("TF TREND", "", "#1a1b2e", self.TXT, True, None))
        rows.append(("", "", self.BORDER, None, False, None))
        tfs = ["M1", "M3", "M5", "M10", "M15", "M30", "H1", "H2", "H4", "H12", "D1"]
        tf_keys = ["TF1", "TF3", "TF5", "TF10", "TF15", "TF30", "TF60", "TF120", "TF240", "TF720", "TFD"]
        for tf_name, tf_key in zip(tfs, tf_keys):
            val = data.get(tf_key, "N/A")
            if val == "Bullish":
                bg, fg = "#0a2e0a", self.BULL
                icon = "▲"
            elif val == "Bearish":
                bg, fg = "#2e0a0a", self.BEAR
                icon = "▼"
            else:
                bg, fg = "#1a1b2e", self.NEUTRAL
                icon = "—"
            rows.append((tf_name, f"{icon} {val}", bg, fg, True, "tf"))
        self.table.setRowCount(len(rows))
        for i, (label, value, bg, fg, bold, rtype) in enumerate(rows):
            left_bg = None
            if rtype == "tf" and bg:
                left_bg = bg
            elif bg and bg not in (self.BORDER,):
                left_bg = bg
            self.table.setItem(i, 0, self._make_item(label, bg=left_bg, fg=fg or self.TXT_DIM, bold=bold))
            self.table.setItem(i, 1, self._make_item(value, bg=bg, fg=fg or self.TXT_DIM, bold=bold))
        self.adjustSize()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._pos and event.buttons() & QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self._pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._pos = None


class AlgomanEngine:
    """AlgoMan NEXT indicator engine - converts Pine Script to Python"""
    def __init__(self):
        self.dashboard = None
        self._items = []
        self._prev_bull = False
        self._prev_bear = False
        self._count_bull = 0
        self._count_bear = 0

    def calculate(self, df, cfg):
        if df is None or len(df) < 250:
            return {}
        n = len(df)
        closes = df["close"].values.astype(float)
        opens = df["open"].values.astype(float)
        highs = df["high"].values.astype(float)
        lows = df["low"].values.astype(float)
        volumes = df["volume"].values.astype(float) if "volume" in df.columns else np.ones(n)

        sensitivity = cfg.get("sensitivity", 1.8)
        strategy = cfg.get("strategy", "Normal")
        smartSignalsOnly = cfg.get("smartSignalsOnly", False)
        consSignalsFilter = cfg.get("consSignalsFilter", False)
        highVolSignals = cfg.get("highVolSignals", False)
        signalsTrendCloud = cfg.get("signalsTrendCloud", False)
        periodTrendCloud = cfg.get("periodTrendCloud", "New")

        atr = self._atr(highs, lows, closes, 14)
        supertrend, st_dir = self._supertrend(closes, highs, lows, sensitivity, 10)
        rsi = self._rsi(closes, 14)
        macd_line, signal_line, hist = self._macd(closes, 12, 26, 9)
        ema200 = self._ema(closes, 200)
        ema150 = self._ema(closes, 150)
        ema250 = self._ema(closes, 250)
        hma55 = self._hma(closes, 55)
        maintrend = self._dchannel(highs, lows, closes, 30)
        adx = self._adx(highs, lows, closes, 14, 14)
        obv = self._obv(closes, volumes)
        vosc = obv - self._ema(obv, 20)
        bs = self._ema(np.abs((opens - closes) / np.where((highs - lows) < 1e-10, 1e-10, highs - lows) * 100), 3)
        ema_bull = closes > ema200

        conf_bull = np.zeros(n, dtype=bool)
        conf_bear = np.zeros(n, dtype=bool)
        for i in range(1, n):
            cross_up = (closes[i] > supertrend[i] and closes[i-1] <= supertrend[i-1])
            cross_dn = (closes[i] < supertrend[i] and closes[i-1] >= supertrend[i-1])
            conf_bull[i] = (cross_up or (i >= 2 and closes[i-1] > supertrend[i-1] and maintrend[i-1] < 0 and maintrend[i] > 0)) and \
                           macd_line[i] > 0 and (i > 0 and macd_line[i] > macd_line[i-1]) and \
                           ema150[i] > ema250[i] and hma55[i] > (hma55[i-2] if i >= 2 else hma55[i]) and maintrend[i] > 0
            conf_bear[i] = (cross_dn or (i >= 2 and closes[i-1] < supertrend[i-1] and maintrend[i-1] > 0 and maintrend[i] < 0)) and \
                           macd_line[i] < 0 and (i > 0 and macd_line[i] < macd_line[i-1]) and \
                           ema150[i] < ema250[i] and hma55[i] < (hma55[i-2] if i >= 2 else hma55[i]) and maintrend[i] < 0

        trendcloud_val = self._supertrend_raw(closes, highs, lows, 4 if periodTrendCloud != "Long term" else 7, 10)
        smart_filter = self._ema(closes, 200)
        vol_filter = np.zeros(n, dtype=bool)
        ema_vol25 = self._ema(volumes, 25)
        ema_vol26 = self._ema(volumes, 26)
        for i in range(n):
            vol_filter[i] = (ema_vol25[i] - ema_vol26[i]) / (ema_vol26[i] if abs(ema_vol26[i]) > 1e-10 else 1e-10) > 0

        bull = np.zeros(n, dtype=bool)
        bear = np.zeros(n, dtype=bool)
        for i in range(1, n):
            if strategy == "Trend scalper":
                continue
            cross_up = closes[i] > supertrend[i] and closes[i-1] <= supertrend[i-1]
            cross_dn = closes[i] < supertrend[i] and closes[i-1] >= supertrend[i-1]
            if strategy == "Normal":
                b = cross_up
                s = cross_dn
            else:
                b = conf_bull[i] and not conf_bull[i-1]
                s = conf_bear[i] and not conf_bear[i-1]
            if smartSignalsOnly:
                b = b and closes[i] > smart_filter[i]
                s = s and closes[i] < smart_filter[i]
            if consSignalsFilter:
                b = b and adx[i] > 20
                s = s and adx[i] > 20
            if highVolSignals:
                b = b and vol_filter[i]
                s = s and vol_filter[i]
            if signalsTrendCloud:
                if periodTrendCloud == "New":
                    b = b and ema150[i] > ema250[i]
                    s = s and ema150[i] < ema250[i]
                else:
                    b = b and closes[i] > trendcloud_val[i]
                    s = s and closes[i] < trendcloud_val[i]
            bull[i] = b
            bear[i] = s

        count_bull = np.zeros(n, dtype=int)
        count_bear = np.zeros(n, dtype=int)
        last_bull = -1
        last_bear = -1
        for i in range(n):
            if bull[i]:
                last_bull = i
            if bear[i]:
                last_bear = i
            count_bull[i] = i - last_bull if last_bull >= 0 else i
            count_bear[i] = i - last_bear if last_bear >= 0 else i

        trigger = np.zeros(n, dtype=int)
        for i in range(n):
            trigger[i] = 1 if count_bull[i] < count_bear[i] else 0

        smart_buy = bull & (closes <= smart_filter)
        smart_sell = bear & (closes >= smart_filter)
        normal_buy = bull & (closes > smart_filter)
        normal_sell = bear & (closes < smart_filter)

        last_close = closes[-1]
        last_ema_bull = bool(ema_bull[-1])
        last_vosc = vosc[-1]
        last_adx = adx[-1]
        last_rsi = rsi[-1]
        last_bs = float(bs[-1])
        last_trigger = int(trigger[-1])
        last_trend = "Bullish" if last_ema_bull else "Bearish"

        auto_trendlines = []
        if cfg.get("enableAutoTrend", False):
            lookback = int(cfg.get("lenTrendChannel", 200))
            piv = max(5, lookback // 20)
            swing_highs = []
            swing_lows = []
            for i in range(piv, n - piv):
                if highs[i] == np.max(highs[i - piv:i + piv + 1]):
                    swing_highs.append((i, highs[i]))
                if lows[i] == np.min(lows[i - piv:i + piv + 1]):
                    swing_lows.append((i, lows[i]))
            if len(swing_highs) >= 2:
                sh1, sh2 = swing_highs[-2], swing_highs[-1]
                slope = (sh2[1] - sh1[1]) / (sh2[0] - sh1[0]) if sh2[0] != sh1[0] else 0
                ext_x = n + 20
                ext_y = sh2[1] + slope * (ext_x - sh2[0])
                auto_trendlines.append({"x1": sh1[0], "y1": sh1[1], "x2": ext_x, "y2": ext_y, "color": "#f7768e"})
            if len(swing_lows) >= 2:
                sl1, sl2 = swing_lows[-2], swing_lows[-1]
                slope = (sl2[1] - sl1[1]) / (sl2[0] - sl1[0]) if sl2[0] != sl1[0] else 0
                ext_x = n + 20
                ext_y = sl2[1] + slope * (ext_x - sl2[0])
                auto_trendlines.append({"x1": sl1[0], "y1": sl1[1], "x2": ext_x, "y2": ext_y, "color": "#9ece6a"})

        auto_sr = []
        if cfg.get("enableSR", False):
            lookback = int(cfg.get("lenTrendChannel", 200))
            piv = max(5, lookback // 20)
            sr_levels = []
            for i in range(piv, n - piv):
                if highs[i] == np.max(highs[i - piv:i + piv + 1]):
                    sr_levels.append(highs[i])
                if lows[i] == np.min(lows[i - piv:i + piv + 1]):
                    sr_levels.append(lows[i])
            clustered = []
            used = set()
            for lv in sr_levels:
                if any(abs(lv - c) < lv * 0.001 for c in clustered):
                    continue
                count = sum(1 for lv2 in sr_levels if abs(lv - lv2) < lv * 0.001)
                if count >= 2:
                    clustered.append(lv)
            auto_sr = clustered[-6:]

        return {
            "trigger": trigger,
            "bull": bull,
            "bear": bear,
            "smart_buy": smart_buy,
            "smart_sell": smart_sell,
            "normal_buy": normal_buy,
            "normal_sell": normal_sell,
            "supertrend": supertrend,
            "st_dir": st_dir,
            "rsi": rsi,
            "macd": macd_line,
            "signal": signal_line,
            "ema200": ema200,
            "ema150": ema150,
            "ema250": ema250,
            "hma55": hma55,
            "atr": atr,
            "adx": adx,
            "maintrend": maintrend,
            "trendcloud": trendcloud_val,
            "smart_filter": smart_filter,
            "count_bull": count_bull,
            "count_bear": count_bear,
            "position": "Buy" if last_trigger == 1 else "Sell",
            "trend": last_trend,
            "strength": last_bs,
            "volume": "Bullish" if last_vosc > 0 else "Bearish",
            "volatility": "Trending" if last_adx > 20 else "Ranging",
            "momentum": "Bullish" if last_rsi > 50 else "Bearish",
            "auto_trendlines": auto_trendlines,
            "auto_sr": auto_sr,
        }

    def _ema(self, data, period):
        result = np.full(len(data), np.nan)
        if len(data) < period:
            return result
        result[period - 1] = np.mean(data[:period])
        multiplier = 2.0 / (period + 1)
        for i in range(period, len(data)):
            result[i] = (data[i] - result[i - 1]) * multiplier + result[i - 1]
        return result

    def _sma(self, data, period):
        result = np.full(len(data), np.nan)
        for i in range(period - 1, len(data)):
            result[i] = np.mean(data[i - period + 1:i + 1])
        return result

    def _hma(self, data, period):
        wma_half = self._wma(data, period // 2)
        wma_full = self._wma(data, period)
        diff = np.full(len(data), np.nan)
        for i in range(len(data)):
            if not np.isnan(wma_half[i]) and not np.isnan(wma_full[i]):
                diff[i] = 2 * wma_half[i] - wma_full[i]
        valid = ~np.isnan(diff)
        if np.sum(valid) < int(np.sqrt(period)):
            return np.full(len(data), np.nan)
        return self._wma(diff, int(np.sqrt(period)))

    def _wma(self, data, period):
        result = np.full(len(data), np.nan)
        weights = np.arange(1, period + 1, dtype=float)
        for i in range(period - 1, len(data)):
            window = data[i - period + 1:i + 1]
            if np.any(np.isnan(window)):
                continue
            result[i] = np.sum(window * weights) / np.sum(weights)
        return result

    def _rsi(self, data, period):
        result = np.full(len(data), 50.0)
        if len(data) < period + 1:
            return result
        deltas = np.diff(data)
        gains = np.where(deltas > 0, deltas, 0.0)
        losses = np.where(deltas < 0, -deltas, 0.0)
        avg_gain = np.mean(gains[:period])
        avg_loss = np.mean(losses[:period])
        for i in range(period, len(deltas)):
            avg_gain = (avg_gain * (period - 1) + gains[i]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i]) / period
            rs = avg_gain / avg_loss if avg_loss > 1e-10 else 100.0
            result[i + 1] = 100.0 - (100.0 / (1.0 + rs))
        return result

    def _macd(self, data, fast, slow, signal):
        ema_fast = self._ema(data, fast)
        ema_slow = self._ema(data, slow)
        macd_line = ema_fast - ema_slow
        signal_line = self._ema(macd_line[~np.isnan(macd_line)], signal)
        full_signal = np.full(len(data), np.nan)
        start = np.sum(np.isnan(macd_line))
        if start + len(signal_line) <= len(data):
            full_signal[start:start + len(signal_line)] = signal_line
        hist = macd_line - full_signal
        return macd_line, full_signal, hist

    def _atr(self, highs, lows, closes, period):
        n = len(closes)
        tr = np.zeros(n)
        tr[0] = highs[0] - lows[0]
        for i in range(1, n):
            tr[i] = max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1]))
        atr = np.zeros(n)
        atr[0] = tr[0]
        for i in range(1, n):
            atr[i] = (atr[i - 1] * (period - 1) + tr[i]) / period
        return atr

    def _supertrend(self, closes, highs, lows, factor, period):
        atr = self._atr(highs, lows, closes, period)
        n = len(closes)
        upper = np.zeros(n)
        lower = np.zeros(n)
        direction = np.zeros(n, dtype=int)
        st = np.full(n, np.nan)
        for i in range(n):
            upper[i] = closes[i] + factor * atr[i]
            lower[i] = closes[i] - factor * atr[i]
        for i in range(1, n):
            lower[i] = lower[i] if lower[i] > lower[i - 1] or closes[i - 1] < lower[i - 1] else lower[i - 1]
            upper[i] = upper[i] if upper[i] < upper[i - 1] or closes[i - 1] > upper[i - 1] else upper[i - 1]
        for i in range(1, n):
            prev_st = st[i - 1]
            prev_upper = upper[i - 1]
            prev_lower = lower[i - 1]
            if prev_st == prev_upper:
                direction[i] = 1 if closes[i] > upper[i] else -1
            else:
                direction[i] = -1 if closes[i] < lower[i] else 1
            st[i] = lower[i] if direction[i] == 1 else upper[i] if direction[i] == -1 else np.nan
        if n > 0:
            direction[0] = 1
            st[0] = lower[0]
        return st, direction

    def _supertrend_raw(self, closes, highs, lows, factor, period):
        atr = self._atr(highs, lows, closes, period)
        n = len(closes)
        upper = np.zeros(n)
        lower = np.zeros(n)
        st = np.full(n, np.nan)
        for i in range(n):
            upper[i] = closes[i] + factor * atr[i]
            lower[i] = closes[i] - factor * atr[i]
        for i in range(1, n):
            lower[i] = lower[i] if lower[i] > lower[i - 1] or closes[i - 1] < lower[i - 1] else lower[i - 1]
            upper[i] = upper[i] if upper[i] < upper[i - 1] or closes[i - 1] > upper[i - 1] else upper[i - 1]
        direction = np.zeros(n, dtype=int)
        for i in range(1, n):
            prev_st = st[i - 1] if not np.isnan(st[i - 1]) else 0
            prev_upper = upper[i - 1]
            prev_lower = lower[i - 1]
            if prev_st == prev_upper:
                direction[i] = 1 if closes[i] > upper[i] else -1
            else:
                direction[i] = -1 if closes[i] < lower[i] else 1
            st[i] = lower[i] if direction[i] == 1 else upper[i] if direction[i] == -1 else np.nan
        if n > 0:
            direction[0] = 1
            st[0] = lower[0]
        return st

    def _dchannel(self, highs, lows, closes, period):
        n = len(closes)
        hh = np.full(n, np.nan)
        ll = np.full(n, np.nan)
        for i in range(period - 1, n):
            hh[i] = np.max(highs[i - period + 1:i + 1])
            ll[i] = np.min(lows[i - period + 1:i + 1])
        trend = np.zeros(n, dtype=int)
        for i in range(1, n):
            if np.isnan(hh[i - 1]) or np.isnan(ll[i - 1]):
                trend[i] = trend[i - 1]
                continue
            if closes[i] > hh[i - 1]:
                trend[i] = 1
            elif closes[i] < ll[i - 1]:
                trend[i] = -1
            else:
                trend[i] = trend[i - 1]
        return trend

    def _adx(self, highs, lows, closes, di_period, adx_period):
        n = len(closes)
        plus_dm = np.zeros(n)
        minus_dm = np.zeros(n)
        tr = np.zeros(n)
        tr[0] = highs[0] - lows[0]
        for i in range(1, n):
            up = highs[i] - highs[i - 1]
            down = lows[i - 1] - lows[i]
            plus_dm[i] = up if up > down and up > 0 else 0
            minus_dm[i] = down if down > up and down > 0 else 0
            tr[i] = max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1]))
        atr_s = np.zeros(n)
        plus_dm_s = np.zeros(n)
        minus_dm_s = np.zeros(n)
        atr_s[di_period] = np.mean(tr[1:di_period + 1])
        plus_dm_s[di_period] = np.mean(plus_dm[1:di_period + 1])
        minus_dm_s[di_period] = np.mean(minus_dm[1:di_period + 1])
        for i in range(di_period + 1, n):
            atr_s[i] = (atr_s[i - 1] * (di_period - 1) + tr[i]) / di_period
            plus_dm_s[i] = (plus_dm_s[i - 1] * (di_period - 1) + plus_dm[i]) / di_period
            minus_dm_s[i] = (minus_dm_s[i - 1] * (di_period - 1) + minus_dm[i]) / di_period
        with np.errstate(divide='ignore', invalid='ignore'):
            plus_di = np.where(atr_s > 0, 100 * plus_dm_s / atr_s, 0)
            minus_di = np.where(atr_s > 0, 100 * minus_dm_s / atr_s, 0)
            dx = np.where(plus_di + minus_di > 0, 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di), 0)
        adx = np.zeros(n)
        start = di_period + adx_period
        if start < n:
            adx[start] = np.mean(dx[di_period:start + 1])
            for i in range(start + 1, n):
                adx[i] = (adx[i - 1] * (adx_period - 1) + dx[i]) / adx_period
        return adx

    def _obv(self, closes, volumes):
        n = len(closes)
        obv = np.zeros(n)
        for i in range(1, n):
            if closes[i] > closes[i - 1]:
                obv[i] = obv[i - 1] + volumes[i]
            elif closes[i] < closes[i - 1]:
                obv[i] = obv[i - 1] - volumes[i]
            else:
                obv[i] = obv[i - 1]
        return obv

    def _pivothigh(self, highs, left, right):
        n = len(highs)
        result = np.full(n, np.nan)
        for i in range(right, n - left):
            is_ph = True
            for j in range(1, right + 1):
                if highs[i] < highs[i - j]:
                    is_ph = False
                    break
            if is_ph:
                for j in range(1, left + 1):
                    if highs[i] < highs[i + j]:
                        is_ph = False
                        break
            if is_ph:
                result[i] = highs[i]
        return result

    def _pivotlow(self, lows, left, right):
        n = len(lows)
        result = np.full(n, np.nan)
        for i in range(right, n - left):
            is_pl = True
            for j in range(1, right + 1):
                if lows[i] > lows[i - j]:
                    is_pl = False
                    break
            if is_pl:
                for j in range(1, left + 1):
                    if lows[i] > lows[i + j]:
                        is_pl = False
                        break
            if is_pl:
                result[i] = lows[i]
        return result

class DraggableHLine(QtWidgets.QGraphicsItem):
    """خط افقی قابل کشیدن - رویداد موس رو خودش میگیره"""

    def __init__(self, price, color, label="", digits=5, on_release=None):
        super().__init__()
        self._price = price
        self._color = color
        self._label = label
        self._digits = digits
        self._dragging = False
        self._y_offset = 0
        self._on_release = on_release
        self.setZValue(200)
        self.setAcceptHoverEvents(True)
        self.setCursor(Qt.SizeVerCursor)

    def boundingRect(self):
        return QtCore.QRectF(-50000, self._price - 0.005, 100000, 0.01)

    def shape(self):
        path = QtGui.QPainterPath()
        path.addRect(-50000, self._price - 0.003, 100000, 0.006)
        return path

    def paint(self, painter, option, widget):
        view = self.scene().views()[0] if self.scene() and self.scene().views() else None
        if view:
            vb = view.plotItem.vb
            r = vb.viewRect()
            x_left = r.left() if r else -50000
            x_right = r.right() if r else 50000
        else:
            x_left, x_right = -50000, 50000

        pen = pg.mkPen(self._color, width=2, style=QtCore.Qt.DashLine)
        if self._dragging:
            pen = pg.mkPen(self._color, width=3, style=QtCore.Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(QtCore.QPointF(x_left, self._price), QtCore.QPointF(x_right, self._price))

        if self._label:
            painter.setPen(QtGui.QColor(self._color))
            painter.setFont(QtGui.QFont("Segoe UI", 8, QtGui.QFont.Bold))
            painter.drawText(QtCore.QPointF(x_right + 5, self._price + 4), self._label)

    def hoverEnterEvent(self, event):
        self.update()

    def hoverLeaveEvent(self, event):
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._y_offset = event.pos().y() - self._price
            event.accept()
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        if self._dragging:
            view = self.scene().views()[0] if self.scene() and self.scene().views() else None
            if view:
                new_pos = view.plotItem.vb.mapSceneToView(event.scenePos())
                self._price = round(new_pos.y() - self._y_offset, self._digits)
                self.prepareGeometryChange()
                self.update()
                event.accept()
                return
        event.ignore()

    def mouseReleaseEvent(self, event):
        if self._dragging:
            self._dragging = False
            self.update()
            if self._on_release:
                self._on_release(self, self._price)
            event.accept()
            return
        event.ignore()

    def get_price(self):
        return self._price

    def set_price(self, price):
        self._price = price
        self.prepareGeometryChange()
        self.update()

class VWAPEngine:
    def __init__(self):
        self.cfg = {
            "use_ses": False, "use_wk": True, "use_mo": False,
            "use_sh": False, "use_sl": False, "use_hv": False, "use_sw": False,
            "prim": "Week Open", "show_band": True,
            "band_m1": 1.0, "band_m2": 2.0, "piv_len": 10, "hv_lb": 200,
            "show_sigs": True, "sig_cool": 8, "keep_sigs": 8,
            "show_clus": True, "clus_tol": 0.5,
            "c_ses": "#d99b1e", "c_wk": "#3b82f6", "c_mo": "#8b5cf6",
            "c_sh": "#e8365f", "c_sl": "#00a89d", "c_hv": "#d97706",
            "c_sw": "#0ea5e9", "silv": "#5c6b80",
        }
        self._vwap_items = []
        self._prev_vwaps = [None] * 7

    def compute(self, opens, highs, lows, closes, volumes):
        n = len(closes)
        if n < 2:
            return None
        hlc3 = (highs + lows + closes) / 3.0
        pv = hlc3 * volumes
        pv2 = hlc3 * hlc3 * volumes
        piv_len = int(self.cfg["piv_len"])
        hv_lb = min(int(self.cfg["hv_lb"]), n)
        cum_pv = [0.0] * 7
        cum_v = [0.0] * 7
        cum_pv2 = [0.0] * 7
        vwap = np.full(n, np.nan)
        vwap_bands_u1 = np.full(n, np.nan)
        vwap_bands_d1 = np.full(n, np.nan)
        vwap_bands_u2 = np.full(n, np.nan)
        vwap_bands_d2 = np.full(n, np.nan)
        all_vwaps = np.full((7, n), np.nan)
        vol_max = 0.0
        for i in range(n):
            vol_max = max(vol_max, volumes[i])
        last_ph = np.nan
        last_pl = np.nan
        ph_swept = False
        pl_swept = False
        sweep_side = 0
        is_high = highs >= np.roll(highs, 1)
        is_low = lows <= np.roll(lows, 1)
        is_high[0] = False
        is_low[0] = False
        reset = [False] * 7
        reset[0] = (opens[i] != opens[i-1]) if i > 0 else False
        if n > 1:
            new_week = False
            new_month = False
            for i in range(1, n):
                pass
        dates = np.arange(n)
        if n > 1:
            reset = [False] * 7
        else:
            reset = [True] * 7
        for i in range(n):
            new_ses = (i == 0) or (i > 0 and opens[i] != opens[i-1])
            new_wk = False
            new_mo = False
            if i > 0:
                try:
                    import datetime as _dt
                    t0 = _dt.datetime.fromtimestamp(opens[i-1]) if opens[i-1] > 1e9 else None
                    t1 = _dt.datetime.fromtimestamp(opens[i]) if opens[i] > 1e9 else None
                    if t0 and t1:
                        new_wk = t0.isocalendar()[1] != t1.isocalendar()[1]
                        new_mo = t0.month != t1.month
                except Exception:
                    pass
            new_hv = False
            if i >= hv_lb:
                seg = volumes[max(0, i-hv_lb+1):i+1]
                if len(seg) > 0 and volumes[i] == np.max(seg) and volumes[i] > 0:
                    new_hv = True
            new_ph = False
            if i >= piv_len:
                seg_h = highs[i-piv_len:i+1]
                if len(seg_h) == piv_len + 1 and highs[i-piv_len] == np.max(seg_h):
                    new_ph = True
                    last_ph = highs[i-piv_len]
                    ph_swept = False
            new_pl = False
            if i >= piv_len:
                seg_l = lows[i-piv_len:i+1]
                if len(seg_l) == piv_len + 1 and lows[i-piv_len] == np.min(seg_l):
                    new_pl = True
                    last_pl = lows[i-piv_len]
                    pl_swept = False
            sweep_buy = False
            sweep_sell = False
            if i > 0 and not np.isnan(last_ph) and not ph_swept:
                if highs[i] > last_ph and closes[i] < last_ph:
                    sweep_buy = True
                    ph_swept = True
                    sweep_side = -1
            if i > 0 and not np.isnan(last_pl) and not pl_swept:
                if lows[i] < last_pl and closes[i] > last_pl:
                    sweep_sell = True
                    pl_swept = True
                    sweep_side = 1
            new_sw = sweep_buy or sweep_sell
            resets = [new_ses, new_wk, new_mo, new_ph, new_pl, new_hv, new_sw]
            for j in range(7):
                if resets[j] or cum_v[j] == 0:
                    cum_pv[j] = pv[i]
                    cum_v[j] = volumes[i]
                    cum_pv2[j] = pv2[i]
                else:
                    cum_pv[j] += pv[i]
                    cum_v[j] += volumes[i]
                    cum_pv2[j] += pv2[i]
            for j in range(7):
                if cum_v[j] > 0:
                    all_vwaps[j, i] = cum_pv[j] / cum_v[j]
                else:
                    all_vwaps[j, i] = np.nan
            if new_ph and i >= piv_len:
                s = i - piv_len
                cpv = np.sum(pv[s:i+1])
                cv = np.sum(volumes[s:i+1])
                cpv2 = np.sum(pv2[s:i+1])
                cum_pv[3] = cpv
                cum_v[3] = cv
                cum_pv2[3] = cpv2
                all_vwaps[3, i] = cpv / cv if cv > 0 else np.nan
            if new_pl and i >= piv_len:
                s = i - piv_len
                cpv = np.sum(pv[s:i+1])
                cv = np.sum(volumes[s:i+1])
                cpv2 = np.sum(pv2[s:i+1])
                cum_pv[4] = cpv
                cum_v[4] = cv
                cum_pv2[4] = cpv2
                all_vwaps[4, i] = cpv / cv if cv > 0 else np.nan
            pidx = {"Session Open": 0, "Week Open": 1, "Month Open": 2, "Swing High": 3, "Swing Low": 4, "Highest Volume Bar": 5, "Liquidity Sweep": 6}.get(self.cfg["prim"], 1)
            if cum_v[pidx] > 0:
                vwap[i] = cum_pv[pidx] / cum_v[pidx]
                variance = max(cum_pv2[pidx] / cum_v[pidx] - vwap[i] ** 2, 0.0)
                sig = np.sqrt(variance)
                atr_val = 0.0
                if i >= 14:
                    tr_arr = np.maximum(highs[i-13:i+1] - lows[i-13:i+1],
                                        np.maximum(np.abs(highs[i-13:i+1] - closes[i-14:i]),
                                                   np.abs(lows[i-13:i+1] - closes[i-14:i])))
                    atr_val = np.mean(tr_arr) if len(tr_arr) > 0 else 0.001
                elif i > 0:
                    atr_val = highs[i] - lows[i]
                else:
                    atr_val = 0.001
                if atr_val > 0 and self.cfg["show_band"]:
                    vwap_bands_u1[i] = vwap[i] + sig * self.cfg["band_m1"]
                    vwap_bands_d1[i] = vwap[i] - sig * self.cfg["band_m1"]
                    vwap_bands_u2[i] = vwap[i] + sig * self.cfg["band_m2"]
                    vwap_bands_d2[i] = vwap[i] - sig * self.cfg["band_m2"]
        en = [self.cfg["use_ses"], self.cfg["use_wk"], self.cfg["use_mo"],
              self.cfg["use_sh"], self.cfg["use_sl"], self.cfg["use_hv"], self.cfg["use_sw"]]
        pidx = {"Session Open": 0, "Week Open": 1, "Month Open": 2, "Swing High": 3, "Swing Low": 4, "Highest Volume Bar": 5, "Liquidity Sweep": 6}.get(self.cfg["prim"], 1)
        sig_cool = int(self.cfg.get("sig_cool", 8))
        keep_sigs = int(self.cfg.get("keep_sigs", 8))
        band_m2 = float(self.cfg.get("band_m2", 2.0))
        sigs = []
        last_sig_bar = -10000
        if not self.cfg.get("show_sigs", True):
            pass
        else:
            for i in range(n):
                if not en[pidx]:
                    continue
                pV = vwap[i]
                u2 = vwap_bands_u2[i]
                d2 = vwap_bands_d2[i]
                if np.isnan(pV) or np.isnan(u2) or np.isnan(d2):
                    continue
                if i - last_sig_bar < sig_cool:
                    continue
                if d2 > 0 and lows[i] <= d2 and closes[i] > d2 and closes[i] < pV:
                    sigs.append((i, "bull", lows[i], f"Outer band rejection ▲ · -{band_m2:.2f}σ · reversion to VWAP"))
                    last_sig_bar = i
                elif u2 > 0 and highs[i] >= u2 and closes[i] < u2 and closes[i] > pV:
                    sigs.append((i, "bear", highs[i], f"Outer band rejection ▼ · +{band_m2:.2f}σ · reversion to VWAP"))
                    last_sig_bar = i
        sigs = sigs[-keep_sigs:] if len(sigs) > keep_sigs else sigs
        return {
            "vwap": vwap, "bands_u1": vwap_bands_u1, "bands_d1": vwap_bands_d1,
            "bands_u2": vwap_bands_u2, "bands_d2": vwap_bands_d2,
            "all_vwaps": all_vwaps, "enabled": en, "n": n, "sigs": sigs,
        }


class ChartWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_symbol = "EURUSD"
        self.current_tf = "H1"
        self.data_df = None
        self._raw_times = []
        self._symbol_index = 0
        self._play_interval = 5000
        self._trade_entry = None
        self._x_tick_logged = False
        self._last_scan_time = 0
        self._prep_log_ts = 0
        self._prep_log2_ts = 0
        self._prep_log_matched = False
        self._chart_mode = "candle"
        self._user_zoomed = False
        self._prep_cfg_logged = False
        self._broker_offset_cache = {}
        self._week_hl_items = []
        self._day_hl_items = []
        self._h4_hl_items = []
        self._h1_hl_items = []
        self._open_day_items = []
        self._level_reject_items = []
        self._yesterday_candle_items = []
        self._session_break_items = []
        self._algoman_items = []
        self._algoman_dashboard = None
        self._algoman_engine = AlgomanEngine()
        self._vwap_items = []
        self._vwap_engine = VWAPEngine()
        self._candle_timer_widget = CandleTimerWidget()
        self._candle_timer_visible = False
        self._zone_arrows = []
        self._signal_popup = SignalPopup(self)
        self._last_signal_dir = "NEUTRAL"
        self._last_signal_score = 0.0

        self._pos_lines = []
        self._trendline_mode = False
        self._trendline_points = []
        self._trendline_items = []
        self._trendline_temp = None
        self._trendline_color = "#ff9e64"
        self._trendline_width = 2.0

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(6, 4, 6, 4)
        toolbar.setSpacing(3)

        tf_btn_style = (
            "QPushButton{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #1e2030,stop:1 #181825);"
            "border:1px solid #292e42;border-radius:6px;font-size:11px;font-weight:bold;color:#7aa2f7;"
            "padding:4px 6px;min-width:34px}"
            "QPushButton:hover{background:#292e42;border-color:#7aa2f7}"
            "QPushButton:checked{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #7aa2f7,stop:1 #565f89);"
            "color:#0a0a1a;border-color:#7aa2f7;font-weight:bold}"
        )

        self.tf_btn_map = {}
        for tf_name in ["M1", "M2", "M3", "M5", "M10", "M15", "M30", "H1", "H4", "D1"]:
            btn = QPushButton(tf_name)
            btn.setCheckable(True)
            btn.setFixedHeight(30)
            btn.setFixedWidth(42)
            btn.setStyleSheet(tf_btn_style)
            if tf_name == self.current_tf:
                btn.setChecked(True)
            btn.clicked.connect(lambda checked, name=tf_name: self.change_timeframe(name))
            setattr(self, f"btn_tf_{tf_name}", btn)
            self.tf_btn_map[tf_name] = btn
            toolbar.addWidget(btn)

        toolbar.addSpacing(4)

        self.btn_toggle_indicators = QPushButton("⚡IND")
        self.btn_toggle_indicators.setFixedHeight(30)
        self.btn_toggle_indicators.setFixedWidth(48)
        self.btn_toggle_indicators.setCheckable(True)
        self.btn_toggle_indicators.setToolTip("Toggle ALL indicators ON/OFF")
        self.btn_toggle_indicators.setStyleSheet(
            "QPushButton{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #1e2030,stop:1 #181825);"
            "border:1px solid #292e42;border-radius:6px;font-size:10px;font-weight:bold;color:#e0af68;"
            "padding:4px 2px}"
            "QPushButton:hover{background:#292e42;border-color:#e0af68}"
            "QPushButton:checked{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #e0af68,stop:1 #565f89);"
            "color:#0a0a1a;border-color:#e0af68;font-weight:bold}"
        )
        self.btn_toggle_indicators.clicked.connect(self._toggle_all_indicators)
        toolbar.addWidget(self.btn_toggle_indicators)

        self.btn_toggle_timer = QPushButton("⏰")
        self.btn_toggle_timer.setFixedHeight(30)
        self.btn_toggle_timer.setFixedWidth(36)
        self.btn_toggle_timer.setCheckable(True)
        self.btn_toggle_timer.setToolTip("Toggle Candle Timer")
        self.btn_toggle_timer.setStyleSheet(
            "QPushButton{background:#24283b;border:1px solid #292e42;border-radius:6px;font-size:14px;color:#e0af68;padding:2px}"
            "QPushButton:hover{background:#292e42;border-color:#e0af68}"
            "QPushButton:checked{background:#e0af68;color:#0a0a1a;border-color:#e0af68;font-weight:bold}"
        )
        self.btn_toggle_timer.clicked.connect(self._toggle_candle_timer)
        toolbar.addWidget(self.btn_toggle_timer)

        self.btn_bg_color = QPushButton("\u25CF")
        self.btn_bg_color.setFixedHeight(30)
        self.btn_bg_color.setFixedWidth(36)
        self.btn_bg_color.setToolTip("Chart Background Color")
        self.btn_bg_color.setStyleSheet(
            "QPushButton{background:#24283b;border:1px solid #292e42;border-radius:6px;font-size:16px;color:#7aa2f7;padding:2px}"
            "QPushButton:hover{background:#292e42;border-color:#7aa2f7}"
        )
        self.btn_bg_color.clicked.connect(self._pick_bg_color)
        toolbar.addWidget(self.btn_bg_color)

        toolbar.addSpacing(8)

        sep = QLabel("|")
        sep.setFixedHeight(48)
        sep.setStyleSheet("color:#292e42;font-size:18px;padding:0 4px;border:none;background:transparent;")
        toolbar.addWidget(sep)

        act_btn_style = (
            "QPushButton{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #24283b,stop:1 #1a1e30);"
            "border:1px solid #292e42;border-radius:8px;font-size:16px;color:#c0caf5;"
            "padding:4px;min-width:38px;min-height:38px}"
            "QPushButton:hover{background:#292e42;border-color:#7aa2f7;color:#7aa2f7}"
            "QPushButton:pressed{background:#1a1e30;border-color:#565f89}"
        )
        self._act_btn_style = act_btn_style

        self.btn_prev = QPushButton("❮")
        self.btn_prev.setFixedSize(40, 40)
        self.btn_prev.setToolTip("Previous Symbol")
        self.btn_prev.setStyleSheet(act_btn_style)
        self.btn_prev.clicked.connect(self._prev_symbol)
        toolbar.addWidget(self.btn_prev)

        self.btn_next = QPushButton("❯")
        self.btn_next.setFixedSize(40, 40)
        self.btn_next.setToolTip("Next Symbol")
        self.btn_next.setStyleSheet(act_btn_style)
        self.btn_next.clicked.connect(self._next_symbol)
        toolbar.addWidget(self.btn_next)

        self.btn_play = QPushButton("▶")
        self.btn_play.setCheckable(True)
        self.btn_play.setFixedSize(40, 40)
        self.btn_play.setToolTip("Auto Scan")
        self.btn_play.setStyleSheet(act_btn_style)
        self.btn_play.clicked.connect(self._toggle_play)
        toolbar.addWidget(self.btn_play)

        self.btn_trade = QPushButton("⚔")
        self.btn_trade.setFixedSize(40, 40)
        self.btn_trade.setToolTip("Manual Trade")
        self.btn_trade.setStyleSheet(act_btn_style)
        self.btn_trade.clicked.connect(self._toggle_trade_panel)
        toolbar.addWidget(self.btn_trade)

        self.btn_normalize = QPushButton("↺")
        self.btn_normalize.setFixedSize(40, 40)
        self.btn_normalize.setToolTip("Reset View")
        self.btn_normalize.setStyleSheet(act_btn_style)
        self.btn_normalize.clicked.connect(self.reset_view)
        toolbar.addWidget(self.btn_normalize)

        self.btn_trendline = QPushButton("📐")
        self.btn_trendline.setFixedSize(40, 40)
        self.btn_trendline.setToolTip("Draw Trendline (click 2 points)")
        self.btn_trendline.setStyleSheet(act_btn_style)
        self.btn_trendline.clicked.connect(self._toggle_trendline_mode)
        toolbar.addWidget(self.btn_trendline)

        self._tl_color_btn = QPushButton()
        self._tl_color_btn.setFixedSize(20, 20)
        self._tl_color_btn.setToolTip("Trendline Color")
        self._tl_color_btn.setStyleSheet(f"background:{self._trendline_color};border:1px solid #565f89;border-radius:4px;")
        self._tl_color_btn.clicked.connect(self._pick_trendline_color)
        toolbar.addWidget(self._tl_color_btn)

        self._tl_width_spin = QtWidgets.QDoubleSpinBox()
        self._tl_width_spin.setRange(0.5, 5.0)
        self._tl_width_spin.setSingleStep(0.5)
        self._tl_width_spin.setValue(self._trendline_width)
        self._tl_width_spin.setDecimals(1)
        self._tl_width_spin.setFixedSize(45, 22)
        self._tl_width_spin.setToolTip("Trendline Width")
        self._tl_width_spin.setStyleSheet("background:#1a1b26;color:#c0caf5;border:1px solid #292e42;border-radius:3px;padding:1px;font-size:8px;")
        toolbar.addWidget(self._tl_width_spin)

        self.btn_clear_trends = QPushButton("✕")
        self.btn_clear_trends.setFixedSize(40, 40)
        self.btn_clear_trends.setToolTip("Clear Trendlines")
        self.btn_clear_trends.setStyleSheet(act_btn_style)
        self.btn_clear_trends.clicked.connect(self._clear_trendlines)
        toolbar.addWidget(self.btn_clear_trends)

        self.bias_lamp = QLabel()
        self.bias_lamp.setFixedSize(22, 22)
        self.bias_lamp.setStyleSheet(
            "background-color:#565f89;border:2px solid #292e42;border-radius:11px;"
        )
        self.bias_lamp.setToolTip("Market Bias: Loading...")
        toolbar.addWidget(self.bias_lamp)

        toolbar.addStretch()
        layout.addLayout(toolbar)

        self.momentum_bars = MomentumBarWidget()
        layout.addWidget(self.momentum_bars)

        self.symbol_label = QLabel("")
        self.symbol_label.setStyleSheet(
            "color:#c0caf5;font-size:13px;font-weight:bold;padding:2px 8px;"
            "background:transparent;border:none;"
        )
        layout.addWidget(self.symbol_label)

        self.candle_plot = pg.PlotWidget()
        self.candle_plot.setBackground("#0a0a1a")
        self.candle_plot.setMenuEnabled(False)
        self.candle_plot.showGrid(x=False, y=True, alpha=0.15)
        self.candle_plot.getAxis('left').setTextPen(pg.mkPen("#565f89"))
        self.candle_plot.getAxis('bottom').setTextPen(pg.mkPen("#565f89"))
        self.candle_plot.getAxis('left').setPen(pg.mkPen("#292e42"))
        self.candle_plot.getAxis('bottom').setPen(pg.mkPen("#292e42"))
        self.candle_plot.setLimits(xMin=-5)
        self.candle_plot.scene().sigMouseMoved.connect(self.on_mouse_moved)
        self.candle_plot.scene().sigMouseClicked.connect(self.on_mouse_click)
        self.candle_plot.sigRangeChangedManually.connect(self._on_range_changed)
        layout.addWidget(self.candle_plot, stretch=1)

        self.v_line = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen("#565f89", width=1, style=Qt.DashLine))
        self.h_line = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen("#565f89", width=1, style=Qt.DashLine))
        self.v_line.hide()
        self.h_line.hide()
        self.candle_plot.addItem(self.v_line, ignoreBounds=True)
        self.candle_plot.addItem(self.h_line, ignoreBounds=True)

        self.crosshair_label = pg.TextItem("", anchor=(0, 1), color="#c0caf5")
        self.crosshair_label.setFont(QFont("Segoe UI", 8))
        self.crosshair_label.hide()
        self.candle_plot.addItem(self.crosshair_label, ignoreBounds=True)

        self._trade_lines_setup()
        self._ichimoku_indicator = IchimokuCloudIndicator(self.candle_plot)
        self._ma_indicator = MAIndicator(self.candle_plot)
        self.executor = MT5Executor()
        self.exit_mgr = ExitManager(self.executor)
        self._play_timer = QTimer()
        self._play_timer.timeout.connect(self._auto_scan_tick)
        self._trade_pos_timer = QTimer()
        self._trade_pos_timer.timeout.connect(self._refresh_trade_positions)
        self._trade_pos_timer.start(3000)
        self.trade_panel = None

        self._tick_timer = QTimer()
        self._tick_timer.timeout.connect(self._on_tick)

        self._momentum_timer = QTimer()
        self._momentum_timer.timeout.connect(self._update_momentum)

        self._load_bg_color()

        self.setLayout(layout)

    def _trade_lines_setup(self):
        self.entry_line = pg.InfiniteLine(angle=0, movable=True, pen=pg.mkPen("#9ece6a", width=1.5, style=Qt.DashLine))
        self.sl_line = pg.InfiniteLine(angle=0, movable=True, pen=pg.mkPen("#f7768e", width=1.5, style=Qt.DashLine))
        self.tp_line = pg.InfiniteLine(angle=0, movable=True, pen=pg.mkPen("#7aa2f7", width=1.5, style=Qt.DashLine))
        self.tp1_line = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen("#3cb371", width=1, style=Qt.DashLine))
        self.real_sl_line = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen("#ff9e64", width=3, style=QtCore.Qt.SolidLine))
        self.real_sl_label = pg.TextItem("REAL SL", color="#ff9e64", anchor=(0, 1))
        self._real_sl_blink = True
        self._real_sl_blink_timer = QTimer()
        self._real_sl_blink_timer.timeout.connect(self._blink_real_sl)
        self._real_sl_blink_timer.start(500)
        self.entry_label = pg.TextItem("Entry", anchor=(0, 1), color="#9ece6a")
        self.sl_label = pg.TextItem("SL", anchor=(0, 1), color="#f7768e")
        self.tp_label = pg.TextItem("TP", anchor=(0, 1), color="#7aa2f7")
        self.tp1_label = pg.TextItem("TP1", anchor=(0, 1), color="#3cb371")
        self.entry_line.hide()
        self.sl_line.hide()
        self.tp_line.hide()
        self.tp1_line.hide()
        self.real_sl_line.hide()
        self.real_sl_label.hide()
        self.entry_label.hide()
        self.sl_label.hide()
        self.tp_label.hide()
        self.tp1_label.hide()
        self.candle_plot.addItem(self.entry_line, ignoreBounds=True)
        self.candle_plot.addItem(self.sl_line, ignoreBounds=True)
        self.candle_plot.addItem(self.tp_line, ignoreBounds=True)
        self.candle_plot.addItem(self.tp1_line, ignoreBounds=True)
        self.candle_plot.addItem(self.real_sl_line, ignoreBounds=True)
        self.candle_plot.addItem(self.real_sl_label, ignoreBounds=True)
        self.candle_plot.addItem(self.entry_label, ignoreBounds=True)
        self.candle_plot.addItem(self.sl_label, ignoreBounds=True)
        self.candle_plot.addItem(self.tp_label, ignoreBounds=True)
        self.candle_plot.addItem(self.tp1_label, ignoreBounds=True)
        self.entry_line.sigDragged.connect(self._on_entry_dragged)
        self.sl_line.sigDragged.connect(self._on_sl_dragged)
        self._sl_dragging = False

    def _on_entry_dragged(self, line):
        new_entry = line.value()
        tp = self.trade_panel
        if tp and tp.isVisible():
            tp._set_entry(new_entry)
            tp._recalc_tp()
            side = "buy" if tp.btn_buy.isChecked() else "sell"
            self._update_trade_lines(entry=new_entry, sl=tp.sl_price, tp=tp.tp_price, side=side)

    def _on_sl_dragged(self, line):
        new_sl = line.value()
        tp = self.trade_panel
        if tp and tp.isVisible():
            tp._set_sl(new_sl)
            tp._recalc_tp()
            side = "buy" if tp.btn_buy.isChecked() else "sell"
            self._update_trade_lines(entry=tp.entry_price, sl=tp.sl_price, tp=tp.tp_price, side=side)

    def set_symbol(self, symbol):
        if symbol == self.current_symbol:
            return
        self._tick_timer.stop()
        self._momentum_timer.stop()
        self.current_symbol = symbol
        self.load_data()

    def change_timeframe(self, tf_name):
        if tf_name == self.current_tf:
            return
        self._tick_timer.stop()
        self._momentum_timer.stop()
        self.current_tf = tf_name
        for tf in ["M1", "M2", "M3", "M5", "M10", "M15", "M30", "H1", "H4", "D1"]:
            btn = getattr(self, f"btn_tf_{tf}", None)
            if btn:
                btn.setChecked(tf == tf_name)
        self.load_data()

    def load_data(self, reset_view=True):
        try:
            tf = TIMEFRAMES.get(self.current_tf, mt5.TIMEFRAME_H1)
            rates = mt5.copy_rates_from_pos(self.current_symbol, tf, 0, 2000)
            if rates is None or len(rates) < 2:
                Logger.warning(f"No data for {self.current_symbol} {self.current_tf}")
                return
            self.data_ltf = rates
            self._last_candle_ts = int(rates[-1]["time"])
            o = np.array([float(r["open"]) for r in rates], dtype=float)
            h = np.array([float(r["high"]) for r in rates], dtype=float)
            lo = np.array([float(r["low"]) for r in rates], dtype=float)
            c = np.array([float(r["close"]) for r in rates], dtype=float)
            v = np.array([float(r["tick_volume"]) for r in rates], dtype=float)
            times = np.array([int(r["time"]) for r in rates], dtype=int)
            self.data_df = pd.DataFrame({
                "open": o, "high": h, "low": lo, "close": c, "volume": v,
                "time": [pd.Timestamp(t, unit="s") for t in times]
            })
            self._raw_times = list(times)
            n = len(rates)
            if not hasattr(self, '_candle_item'):
                self._candle_item = CandlestickItem(self.candle_plot)
            self._candle_item.set_mode(self._chart_mode)
            self._candle_item.set_data(np.arange(n), o, h, lo, c)
            is_rinko = (self._chart_mode == "rinko")
            # clear zone arrows on data reload
            if hasattr(self, '_zone_arrows'):
                for item in self._zone_arrows:
                    try:
                        self.candle_plot.removeItem(item)
                    except Exception:
                        pass
                self._zone_arrows.clear()
            self.symbol_label.setText(f"  {self.current_symbol}  |  {self.current_tf}  ")
            if not is_rinko:
                self._update_indicator_state()
                self._update_x_ticks()
                self._update_bias_lamp(c)
                self._update_pos_lines()
            if not self._tick_timer.isActive():
                self._tick_timer.start(200)
            if not self._momentum_timer.isActive():
                self._momentum_timer.start(30000)
            if reset_view and not is_rinko:
                self._user_zoomed = False
                self.goto_last_candle()
        except Exception as e:
            Logger.error(f"load_data error: {e}")
            traceback.print_exc()

    def _update_momentum(self):
        try:
            self._update_level_rejections()
            scores = MomentumEngine.calculate_all(self.current_symbol)
            combined = scores.get("combined", {})
            bias = combined.get("score", 0.0)
            bars = {
                "M1": scores.get("M1", {}).get("score", 0.0),
                "M2": scores.get("M2", {}).get("score", 0.0),
                "M3": scores.get("M3", {}).get("score", 0.0),
                "M5": scores.get("M5", {}).get("score", 0.0),
                "M10": scores.get("M10", {}).get("score", 0.0),
                "M15": scores.get("M15", {}).get("score", 0.0),
                "M30": scores.get("M30", {}).get("score", 0.0),
                "H1": scores.get("H1", {}).get("score", 0.0),
                "H4": scores.get("H4", {}).get("score", 0.0),
                "D1": scores.get("D1", {}).get("score", 0.0),
                "BIA": round(bias, 2),
                "_combined": combined,
            }
            for tf_name in MomentumEngine.TF_MAP:
                if tf_name in scores:
                    bars[tf_name] = {
                        "score": scores[tf_name].get("score", 0.0),
                        "direction": scores[tf_name].get("direction", "NEUTRAL"),
                    }
            self.momentum_bars.set_scores(bars)
            new_dir = combined.get("direction", "NEUTRAL")
            new_score = combined.get("score", 0.0)
            scenario = combined.get("scenario", "")
            if new_dir in ("BUY", "SELL") and new_dir != self._last_signal_dir:
                self._signal_popup.show_signal(new_dir, new_score, scenario)
            elif new_dir in ("BUY", "SELL") and abs(new_score - self._last_signal_score) > 2:
                self._signal_popup.show_signal(new_dir, new_score, scenario)
            if new_dir != "NEUTRAL":
                self._last_signal_dir = new_dir
                self._last_signal_score = new_score
            self._update_tf_trends()
        except Exception as e:
            Logger.error(f"_update_momentum error: {e}")

    def _update_indicator_state(self):
        try:
            sp = self.window().findChild(StrategyPanel)
            if sp:
                self._update_ichimoku()
                self._update_ma()
                self._update_week_hl()
                self._update_day_hl()
                self._update_yesterday_candle()
                self._update_h4_hl()
                self._update_h1_hl()
                self._update_open_day()
                self._update_session_break()
                self._update_algoman()
                self._update_vwap()
        except Exception:
            pass

    def _update_ichimoku(self):
        sp = self.window().findChild(StrategyPanel)
        if not sp or not sp.ichimoku_cb.isChecked():
            self._ichimoku_indicator.clear()
            return
        if self.data_df is None or len(self.data_df) < 30:
            return
        if hasattr(sp, 'ichimoku_cfg'):
            self._ichimoku_indicator.set_config(sp.ichimoku_cfg)
        bg_color = "#0a0a1a"
        try:
            bg_brush = self.candle_plot.backgroundBrush()
            if bg_brush.style() != QtCore.Qt.NoBrush:
                bg_color = bg_brush.color().name()
        except Exception:
            pass
        try:
            r = int(bg_color[1:3], 16)
            g = int(bg_color[3:5], 16)
            b = int(bg_color[5:7], 16)
            luminance = 0.299 * r + 0.587 * g + 0.114 * b
        except Exception:
            luminance = 30
        if luminance < 80:
            self._ichimoku_indicator.lead52_color = "#ffffff"
        else:
            self._ichimoku_indicator.lead52_color = "#1a1b26"
        df = self.data_df
        opens = df["open"].values.astype(float)
        highs = df["high"].values.astype(float)
        lows = df["low"].values.astype(float)
        closes = df["close"].values.astype(float)
        x_indices = np.arange(len(df))
        self._ichimoku_indicator.draw(highs, lows, closes, x_indices)
        lead52 = self._ichimoku_indicator._lead52
        if lead52 is not None and len(lead52) > 0 and not np.isnan(lead52[-1]):
            mw = self.window()
            if hasattr(mw, 'exit_mgr') and mw.exit_mgr:
                mw.exit_mgr._lead52_values[self.current_symbol] = float(lead52[-1])
                atr = self._calc_atr(highs, lows, closes, 14)
                if atr is not None and len(atr) > 0 and not np.isnan(atr[-1]):
                    mw.exit_mgr._atr_values[self.current_symbol] = float(atr[-1])

    def _push_lead52_atr(self):
        if self.data_df is None or len(self.data_df) < 60:
            return
        df = self.data_df
        highs = df["high"].values.astype(float)
        lows = df["low"].values.astype(float)
        closes = df["close"].values.astype(float)
        n = len(closes)
        period = 52
        if n < period + 1:
            return
        lead52 = np.full(n, np.nan)
        for i in range(period - 1, n):
            w_low = np.min(lows[i - period + 1:i + 1])
            w_high = np.max(highs[i - period + 1:i + 1])
            lead52[i] = (w_low + w_high) / 2.0
        if not np.isnan(lead52[-1]):
            mw = self.window()
            if hasattr(mw, 'exit_mgr') and mw.exit_mgr:
                mw.exit_mgr._lead52_values[self.current_symbol] = float(lead52[-1])
                atr = self._calc_atr(highs, lows, closes, 14)
                if atr is not None and len(atr) > 0 and not np.isnan(atr[-1]):
                    mw.exit_mgr._atr_values[self.current_symbol] = float(atr[-1])

    def _calc_atr(self, highs, lows, closes, period=14):
        n = len(closes)
        if n < period + 1:
            return np.full(n, np.nan)
        tr = np.zeros(n)
        tr[0] = highs[0] - lows[0]
        for i in range(1, n):
            tr[i] = max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1]))
        atr = np.full(n, np.nan)
        atr[period] = np.mean(tr[1:period+1])
        mult = 2.0 / (period + 1)
        for i in range(period + 1, n):
            atr[i] = (tr[i] - atr[i-1]) * mult + atr[i-1]
        return atr

    def _update_ma(self):
        sp = self.window().findChild(StrategyPanel)
        if not sp or not sp.ma_cb.isChecked():
            self._ma_indicator.clear()
            return
        if self.data_df is None or len(self.data_df) < 20:
            return
        df = self.data_df
        closes = df["close"].values.astype(float)
        x_indices = np.arange(len(df))
        self._ma_indicator.set_config(sp.ma_cfg if hasattr(sp, 'ma_cfg') else {})
        self._ma_indicator.draw(closes, x_indices)

    def _update_bias_lamp(self, closes):
        if len(closes) < 50 or not hasattr(self, 'bias_lamp'):
            return
        ema20 = closes[-20:].mean()
        ema50 = closes[-50:].mean()
        price = closes[-1]
        ema20_prev = closes[-21:-1].mean()
        ema50_prev = closes[-51:-1].mean()
        score = 0
        if ema20 > ema50:
            score += 1
        else:
            score -= 1
        if ema20 > ema20_prev:
            score += 1
        else:
            score -= 1
        if ema50 > ema50_prev:
            score += 1
        else:
            score -= 1
        if price > ema20:
            score += 1
        else:
            score -= 1
        if score >= 2:
            color = "#9ece6a"
            glow = "#2d5a3a"
            tip = "Bullish Bias"
        elif score <= -2:
            color = "#f7768e"
            glow = "#5a2d33"
            tip = "Bearish Bias"
        else:
            color = "#e0af68"
            glow = "#4a3d2a"
            tip = "Neutral Bias"
        self.bias_lamp.setStyleSheet(
            f"background-color:{color};border:2px solid {glow};border-radius:10px;"
            f"box-shadow:0 0 8px {color};"
        )
        self.bias_lamp.setToolTip(f"{tip} ({score}/4)")

    def _calc_setup_lot(self, entry, sl, sp):
        try:
            risk_mode_idx = sp.risk_combo.currentIndex()
            risk_val = sp.risk_input.value()
            modes = ["% Balance", "$ Fixed", "Fixed Lot"]
            mode = modes[risk_mode_idx]
            if mode == "Fixed Lot":
                return max(0.01, risk_val)
            info = mt5.symbol_info(self.current_symbol)
            if not info:
                return 0.01
            sl_dist = abs(entry - sl)
            if sl_dist < 1e-10:
                return 0.01
            tick_val = info.trade_tick_value
            tick_size = info.trade_tick_size
            if tick_size < 1e-10:
                return 0.01
            sl_ticks = sl_dist / tick_size
            sl_cost = sl_ticks * tick_val
            if sl_cost < 1e-10:
                return 0.01
            if mode == "% Balance":
                acc = MT5Connector.get_account_info()
                bal = acc.balance if acc else 10000
                risk_amt = bal * risk_val / 100.0
            else:
                risk_amt = risk_val
            lot = risk_amt / sl_cost
            lot = round(lot, 2)
            vs = info.volume_step if info.volume_step > 0 else 0.01
            lot = round(lot / vs) * vs
            lot = max(info.volume_min if info.volume_min > 0 else 0.01, min(lot, info.volume_max if info.volume_max > 0 else 100))
            return lot
        except Exception:
            return 0.01

    def _count_symbol_positions(self, symbol):
        try:
            positions = mt5.positions_get(symbol=symbol)
            return len(positions) if positions else 0
        except Exception:
            return 0

    def _compute_atr(self, highs, lows, closes, period):
        n = len(closes)
        if n < 2 or period < 1:
            return np.full(n, np.nan)
        tr = np.zeros(n)
        tr[0] = highs[0] - lows[0]
        for i in range(1, n):
            tr[i] = max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1]))
        out = np.full(n, np.nan)
        out[0] = tr[0]
        alpha = 1.0 / period
        for i in range(1, n):
            out[i] = out[i - 1] * (1 - alpha) + tr[i] * alpha
        return out

    def _on_tick(self):
        try:
            try:
                tick = mt5.symbol_info_tick(self.current_symbol)
            except Exception:
                tick = None
            if tick is None or tick.bid is None:
                return
            bid = float(tick.bid)
            if len(self.data_df) == 0:
                return
            last_idx = len(self.data_df) - 1
            cur_high = float(self.data_df.at[last_idx, "high"])
            cur_low = float(self.data_df.at[last_idx, "low"])
            if bid > cur_high:
                self.data_df.at[last_idx, "high"] = bid
                cur_high = bid
            if bid < cur_low:
                self.data_df.at[last_idx, "low"] = bid
                cur_low = bid
            self.data_df.at[last_idx, "close"] = bid
            if self._chart_mode != "rinko":
                self._candle_item.update_last(last_idx, float(self.data_df.at[last_idx, "open"]), cur_high, cur_low, bid)
            if not hasattr(self, '_sync_tick_count'):
                self._sync_tick_count = 0
            self._sync_tick_count += 1
            if self._sync_tick_count >= 10:
                self._sync_tick_count = 0
                self._sync_from_mt5()
            if not hasattr(self, '_pos_line_tick_count'):
                self._pos_line_tick_count = 0
            self._pos_line_tick_count += 1
            if self._pos_line_tick_count >= 25:
                self._pos_line_tick_count = 0
                self._update_pos_lines()
            if self.trade_panel and self.trade_panel.isVisible():
                is_market = self.trade_panel.order_type.currentText() == "Market"
                if is_market and self.entry_line.isVisible():
                    side = "buy" if self.trade_panel.btn_buy.isChecked() else "sell"
                    entry = float(tick.ask) if side == "buy" else bid
                    info = mt5.symbol_info(self.current_symbol)
                    digits = info.digits if info else 5
                    entry = round(entry, digits)
                    self.entry_line.setValue(entry)
                    nudge = self._get_label_x()
                    self.entry_label.setText(f"Entry {entry:.{digits}f}")
                    self.entry_label.setPos(nudge, entry)
                    self.trade_panel.entry_price = entry
            if not hasattr(self, '_algoman_tick_count'):
                self._algoman_tick_count = 0
            self._algoman_tick_count += 1
            if self._algoman_tick_count >= 50:
                self._algoman_tick_count = 0
                sp = self.window().findChild(StrategyPanel)
                if sp and sp.algoman_cb.isChecked():
                    self._update_algoman()
            if not hasattr(self, '_ichimoku_tick_count'):
                self._ichimoku_tick_count = 0
            self._ichimoku_tick_count += 1
            if self._ichimoku_tick_count >= 50:
                self._ichimoku_tick_count = 0
                sp = self.window().findChild(StrategyPanel)
                if sp and sp.ichimoku_cb.isChecked():
                    self._update_ichimoku()
                elif sp and hasattr(sp, 'trail_algoman_cb') and sp.trail_algoman_cb.isChecked():
                    self._push_lead52_atr()
            if self._candle_timer_visible:
                self._candle_timer_widget.update_timers(int(tick.time))
                self._update_candle_colors()
        except Exception as e:
            Logger.error(f"_on_tick error: {e}")

    def _sync_from_mt5(self):
        try:
            tf = TIMEFRAMES.get(self.current_tf, mt5.TIMEFRAME_H1)
            rates = mt5.copy_rates_from_pos(self.current_symbol, tf, 0, 3)
            if rates is None or len(rates) < 1:
                return
            last_rate = rates[-1]
            mt5_last_ts = int(last_rate[0])
            our_last_ts = self._raw_times[-1] if self._raw_times else 0
            if mt5_last_ts > our_last_ts:
                if len(rates) >= 2:
                    prev_rate = rates[-2]
                    prev_ts = int(prev_rate[0])
                    last_idx = len(self.data_df) - 1
                    if last_idx >= 0 and prev_ts == our_last_ts:
                        self.data_df.at[last_idx, "open"] = float(prev_rate[1])
                        self.data_df.at[last_idx, "high"] = float(prev_rate[2])
                        self.data_df.at[last_idx, "low"] = float(prev_rate[3])
                        self.data_df.at[last_idx, "close"] = float(prev_rate[4])
                new_row = pd.DataFrame([{
                    "time": pd.Timestamp(mt5_last_ts, unit="s"),
                    "open": float(last_rate[1]),
                    "high": float(last_rate[2]),
                    "low": float(last_rate[3]),
                    "close": float(last_rate[4]),
                }])
                self.data_df = pd.concat([self.data_df, new_row], ignore_index=True)
                self._raw_times.append(mt5_last_ts)
                n = len(self.data_df)
                o = self.data_df["open"].to_numpy(dtype=float)
                h = self.data_df["high"].to_numpy(dtype=float)
                lo = self.data_df["low"].to_numpy(dtype=float)
                c = self.data_df["close"].to_numpy(dtype=float)
                self._candle_item.set_data(np.arange(n), o, h, lo, c)
                self._update_x_ticks()
                if not self._user_zoomed:
                    self.goto_last_candle()
            elif mt5_last_ts == our_last_ts:
                last_idx = len(self.data_df) - 1
                if last_idx >= 0:
                    self.data_df.at[last_idx, "open"] = float(last_rate[1])
                    self.data_df.at[last_idx, "high"] = float(last_rate[2])
                    self.data_df.at[last_idx, "low"] = float(last_rate[3])
                    self.data_df.at[last_idx, "close"] = float(last_rate[4])
                    if self._chart_mode != "rinko":
                        self._candle_item.update_last(
                            last_idx, float(last_rate[1]), float(last_rate[2]),
                            float(last_rate[3]), float(last_rate[4]),
                        )
        except Exception:
            pass

    def _update_level_rejections(self):
        Logger.info("[LevelRej] === START ===")
        for item in self._level_reject_items:
            try:
                self.candle_plot.removeItem(item)
            except Exception:
                pass
        self._level_reject_items.clear()
        sp = self.window().findChild(StrategyPanel)
        if not sp:
            return
        if self.data_df is None or len(self.data_df) < 5:
            return
        n = len(self.data_df)
        highs = self.data_df["high"].values.astype(float)
        lows = self.data_df["low"].values.astype(float)
        opens = self.data_df["open"].values.astype(float)
        closes = self.data_df["close"].values.astype(float)
        raw_times = getattr(self, '_raw_times', None)
        if not raw_times or len(raw_times) != n:
            return
        import datetime as _dt
        levels = []
        try:
            if sp.week_hl_cb.isChecked():
                d1_rates = mt5.copy_rates_from_pos(self.current_symbol, mt5.TIMEFRAME_D1, 0, 200)
                if d1_rates is not None and len(d1_rates) >= 2:
                    tick = mt5.symbol_info_tick(self.current_symbol)
                    if tick:
                        now_ts = int(tick.time)
                        now_dt = _dt.datetime.utcfromtimestamp(now_ts)
                        week_ago = now_ts - 7 * 86400
                        prev_week = [r for r in d1_rates if week_ago <= r['time'] < now_ts - (now_dt.weekday() + 1) * 86400]
                        if len(prev_week) < 2:
                            prev_week = d1_rates[-7:-1] if len(d1_rates) >= 7 else d1_rates[:-1]
                        w_ceil = max(r['high'] for r in prev_week)
                        w_floor = min(r['low'] for r in prev_week)
                        w_ts = prev_week[0]['time']
                        levels.append(("W1", w_ceil, w_floor, w_ts))
        except Exception:
            pass
        try:
            if sp.day_hl_cb.isChecked():
                d1_rates = mt5.copy_rates_from_pos(self.current_symbol, mt5.TIMEFRAME_D1, 0, 5)
                if d1_rates is not None and len(d1_rates) >= 2:
                    yesterday = d1_rates[-2]
                    levels.append(("D1", yesterday['high'], yesterday['low'], yesterday['time']))
        except Exception:
            pass
        try:
            if sp.h4_hl_cb.isChecked():
                h4_rates = mt5.copy_rates_from_pos(self.current_symbol, mt5.TIMEFRAME_H4, 0, 50)
                if h4_rates is not None and len(h4_rates) >= 3:
                    tick = mt5.symbol_info_tick(self.current_symbol)
                    if tick:
                        now_ts = tick.time
                        h4_sec = 4 * 3600
                        prev_h4 = None
                        for r in reversed(h4_rates):
                            if r['time'] + h4_sec <= now_ts:
                                prev_h4 = r
                                break
                        if prev_h4 is not None:
                            levels.append(("H4", prev_h4['high'], prev_h4['low'], prev_h4['time']))
        except Exception:
            pass
        try:
            if sp.h1_hl_cb.isChecked():
                h1_rates = mt5.copy_rates_from_pos(self.current_symbol, mt5.TIMEFRAME_H1, 0, 50)
                if h1_rates is not None and len(h1_rates) >= 3:
                    tick = mt5.symbol_info_tick(self.current_symbol)
                    if tick:
                        now_ts = tick.time
                        h1_sec = 3600
                        prev_h1 = None
                        for r in reversed(h1_rates):
                            if r['time'] + h1_sec <= now_ts:
                                prev_h1 = r
                                break
                        if prev_h1 is not None:
                            levels.append(("H1", prev_h1['high'], prev_h1['low'], prev_h1['time']))
        except Exception:
            pass
        try:
            info = mt5.symbol_info(self.current_symbol)
        except Exception:
            info = None
        if info:
            pip = info.point * 10 if info.point <= 0.001 else info.point
        else:
            pip = 0.0001
        half = pip / 2.0
        for tf_name, level_high, level_low, level_ts in levels:
            start_idx = 0
            for i, rt in enumerate(raw_times):
                if rt >= level_ts:
                    start_idx = i
                    break
            if start_idx < 0 or start_idx >= n:
                Logger.info(f"[LevelRej] {tf_name} skip: start_idx={start_idx} n={n}")
                continue
            Logger.info(f"[LevelRej] {tf_name}: ceil={level_high:.5f} floor={level_low:.5f} ts={level_ts} start={start_idx} n={n}")
            marked = 0
            for i in range(start_idx, n - 1):
                o, h, l, c = opens[i], highs[i], lows[i], closes[i]
                candle_range = h - l
                if candle_range <= 0:
                    continue
                body = abs(c - o)
                body_top = max(o, c)
                body_bot = min(o, c)
                lower_shadow = body_bot - l
                upper_shadow = h - body_top
                is_bullish = c > o
                is_bearish = c < o
                is_reject = False
                side = ''
                if l <= level_low + half and c > level_low + half and c > o and upper_shadow <= body:
                    is_reject = True
                    if i > 0 and is_bullish and o < closes[i-1] and c > opens[i-1]:
                        side = 'support_bull_engulf'
                    elif lower_shadow >= body:
                        side = 'support_long_shadow'
                    elif c > (h + l) / 2:
                        side = 'support_close_away'
                    else:
                        side = 'support_break'
                if not is_reject and h >= level_high - half and c < level_high - half and c < o and lower_shadow <= body:
                    is_reject = True
                    if i > 0 and is_bearish and o > closes[i-1] and c < opens[i-1]:
                        side = 'resist_bear_engulf'
                    elif upper_shadow >= body:
                        side = 'resist_long_shadow'
                    elif c < (h + l) / 2:
                        side = 'resist_close_away'
                    else:
                        side = 'resist_break'
                if is_reject:
                    marked += 1
            Logger.info(f"[LevelRej] {tf_name}: {marked} rejections")

    def _find_stm_order(self, symbol, direction, entry, tol=0.001):
        try:
            orders = mt5.orders_get(symbol=symbol)
            if not orders:
                return None
            for o in orders:
                if abs(o.price_open - entry) / max(entry, 1e-8) < tol:
                    return o.ticket
        except Exception:
            pass
        return None

    def _adjust_stops(self, symbol, direction, entry, sl, tp):
        try:
            info = mt5.symbol_info(symbol)
            if not info:
                return sl, tp
            stops = info.trade_stops_level
            if stops <= 0:
                return sl, tp
            pt = info.point
            dg = info.digits
            if direction == "buy":
                min_sl = round(entry - stops * pt, dg)
                if sl > min_sl:
                    sl = min_sl
                min_tp = round(entry + stops * pt, dg)
                if tp < min_tp:
                    tp = min_tp
                if sl >= entry or tp <= entry:
                    return None, None
            else:
                min_sl = round(entry + stops * pt, dg)
                if sl < min_sl:
                    sl = min_sl
                min_tp = round(entry - stops * pt, dg)
                if tp > min_tp:
                    tp = min_tp
                if sl <= entry or tp >= entry:
                    return None, None
        except Exception:
            pass
        return sl, tp

    def _get_digits(self):
        try:
            info = mt5.symbol_info(self.current_symbol)
            return info.digits if info else 5
        except Exception:
            return 5

    def _alpha_hex(self, hex_color, alpha_pct):
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        a = int(255 * (1 - alpha_pct / 100))
        return r, g, b, a

    @staticmethod
    def _find_level_candle(rates):
        """Find the decisive breakout candle for zone level detection.

        Walk backwards from the last closed candle. A candle is "decisive" if:
        - close > previous candle's high  (bullish breakout)
        - close < previous candle's low   (bearish breakout)
        If close is inside the previous candle's range (neutral), keep going back.

        Returns the decisive candle dict, or last closed candle as fallback.
        """
        if rates is None or len(rates) < 3:
            return rates[-2] if rates is not None and len(rates) >= 2 else None
        n = len(rates)
        for i in range(n - 2, 0, -1):
            close_i = float(rates[i]['close'])
            high_prev = float(rates[i - 1]['high'])
            low_prev = float(rates[i - 1]['low'])
            if close_i > high_prev or close_i < low_prev:
                return rates[i]
        return rates[-2]

    def _update_week_hl(self):
        for item in self._week_hl_items:
            try:
                self.candle_plot.removeItem(item)
            except Exception:
                pass
        self._week_hl_items.clear()
        sp = self.window().findChild(StrategyPanel)
        if not sp or not sp.week_hl_cb.isChecked():
            return
        try:
            rates = mt5.copy_rates_from_pos(self.current_symbol, mt5.TIMEFRAME_W1, 0, 20)
            if rates is None or len(rates) < 3:
                return
            level_candle = self._find_level_candle(rates)
            if level_candle is None:
                return
            ceiling = float(level_candle['high'])
            floor_val = float(level_candle['low'])
            open_val = float(level_candle['open'])
            level_ts = int(level_candle['time'])
            n = len(self.data_df) if self.data_df is not None else 0
            if n < 2:
                return
            x0 = -0.5
            for i in range(n):
                if self._raw_times[i] >= level_ts:
                    x0 = float(i) - 0.5
                    break
            x1 = float(n) - 0.5
            info = mt5.symbol_info(self.current_symbol)
            if info:
                pip = info.point * 10 if info.point <= 0.001 else info.point
            else:
                pip = 0.0001
            half = pip / 2.0
            ceil_brush = pg.mkBrush(247, 118, 142, 50)
            floor_brush = pg.mkBrush(115, 218, 202, 50)
            ceil_rect = QtWidgets.QGraphicsRectItem(
                QtCore.QRectF(x0, ceiling - half, x1 - x0, pip))
            ceil_rect.setBrush(ceil_brush)
            ceil_rect.setPen(pg.mkPen("#f7768e", width=1))
            ceil_rect.setZValue(3)
            floor_rect = QtWidgets.QGraphicsRectItem(
                QtCore.QRectF(x0, floor_val - half, x1 - x0, pip))
            floor_rect.setBrush(floor_brush)
            floor_rect.setPen(pg.mkPen("#73daca", width=1))
            floor_rect.setZValue(3)
            self.candle_plot.addItem(ceil_rect)
            self.candle_plot.addItem(floor_rect)
            self._week_hl_items.extend([ceil_rect, floor_rect])
            import pyqtgraph as _pg
            ceil_lbl = _pg.TextItem(f"WEEK CEIL  {ceiling:.5f}", color="#f7768e", anchor=(0, 1))
            ceil_lbl.setFont(_pg.QtGui.QFont("Arial", 9, _pg.QtGui.QFont.Bold))
            ceil_lbl.setPos(x0, ceiling)
            floor_lbl = _pg.TextItem(f"WEEK FLOOR  {floor_val:.5f}", color="#73daca", anchor=(0, 0))
            floor_lbl.setFont(_pg.QtGui.QFont("Arial", 9, _pg.QtGui.QFont.Bold))
            floor_lbl.setPos(x0, floor_val)
            self.candle_plot.addItem(ceil_lbl)
            self.candle_plot.addItem(floor_lbl)
            self._week_hl_items.extend([ceil_lbl, floor_lbl])
            open_pen = pg.mkPen("#e0af68", width=1, style=QtCore.Qt.DashLine)
            open_line = pg.PlotCurveItem(x=[x0, x1], y=[open_val, open_val], pen=open_pen)
            open_line.setZValue(4)
            self.candle_plot.addItem(open_line)
            open_lbl = _pg.TextItem(f"WEEK OPEN  {open_val:.5f}", color="#e0af68", anchor=(0, 1))
            open_lbl.setFont(_pg.QtGui.QFont("Arial", 9, _pg.QtGui.QFont.Bold))
            open_lbl.setPos(x0, open_val)
            self.candle_plot.addItem(open_lbl)
            self._week_hl_items.extend([open_line, open_lbl])
        except Exception as e:
            Logger.error(f"WeekHL error: {e}")

    def _update_day_hl(self):
        for item in self._day_hl_items:
            try:
                self.candle_plot.removeItem(item)
            except Exception:
                pass
        self._day_hl_items.clear()
        sp = self.window().findChild(StrategyPanel)
        if not sp or not sp.day_hl_cb.isChecked():
            return
        try:
            rates = mt5.copy_rates_from_pos(self.current_symbol, mt5.TIMEFRAME_D1, 0, 20)
            if rates is None or len(rates) < 3:
                return
            level_candle = self._find_level_candle(rates)
            if level_candle is None:
                return
            ceiling = float(level_candle['high'])
            floor_val = float(level_candle['low'])
            open_val = float(level_candle['open'])
            day_start_ts = int(level_candle['time'])
            n = len(self.data_df) if self.data_df is not None else 0
            if n < 2:
                return
            x0 = -0.5
            for i in range(n):
                if self._raw_times[i] >= day_start_ts:
                    x0 = float(i) - 0.5
                    break
            x1 = float(n) - 0.5
            info = mt5.symbol_info(self.current_symbol)
            if info:
                pip = info.point * 10 if info.point <= 0.001 else info.point
            else:
                pip = 0.0001
            half = pip / 2.0
            ceil_brush = pg.mkBrush(255, 158, 100, 50)
            floor_brush = pg.mkBrush(187, 154, 247, 50)
            ceil_rect = QtWidgets.QGraphicsRectItem(
                QtCore.QRectF(x0, ceiling - half, x1 - x0, pip))
            ceil_rect.setBrush(ceil_brush)
            ceil_rect.setPen(pg.mkPen("#ff9e64", width=1))
            ceil_rect.setZValue(3)
            floor_rect = QtWidgets.QGraphicsRectItem(
                QtCore.QRectF(x0, floor_val - half, x1 - x0, pip))
            floor_rect.setBrush(floor_brush)
            floor_rect.setPen(pg.mkPen("#bb9af7", width=1))
            floor_rect.setZValue(3)
            self.candle_plot.addItem(ceil_rect)
            self.candle_plot.addItem(floor_rect)
            self._day_hl_items.extend([ceil_rect, floor_rect])
            import pyqtgraph as _pg
            ceil_lbl = _pg.TextItem(f"DAY CEIL  {ceiling:.5f}", color="#ff9e64", anchor=(0, 1))
            ceil_lbl.setFont(_pg.QtGui.QFont("Arial", 9, _pg.QtGui.QFont.Bold))
            ceil_lbl.setPos(x0, ceiling)
            floor_lbl = _pg.TextItem(f"DAY FLOOR  {floor_val:.5f}", color="#bb9af7", anchor=(0, 0))
            floor_lbl.setFont(_pg.QtGui.QFont("Arial", 9, _pg.QtGui.QFont.Bold))
            floor_lbl.setPos(x0, floor_val)
            self.candle_plot.addItem(ceil_lbl)
            self.candle_plot.addItem(floor_lbl)
            self._day_hl_items.extend([ceil_lbl, floor_lbl])
            open_pen = pg.mkPen("#e0af68", width=1, style=QtCore.Qt.DashLine)
            open_line = pg.PlotCurveItem(x=[x0, x1], y=[open_val, open_val], pen=open_pen)
            open_line.setZValue(4)
            self.candle_plot.addItem(open_line)
            open_lbl = _pg.TextItem(f"DAY OPEN  {open_val:.5f}", color="#e0af68", anchor=(0, 1))
            open_lbl.setFont(_pg.QtGui.QFont("Arial", 9, _pg.QtGui.QFont.Bold))
            open_lbl.setPos(x0, open_val)
            self.candle_plot.addItem(open_lbl)
            self._day_hl_items.extend([open_line, open_lbl])
        except Exception as e:
            Logger.error(f"DayHL error: {e}")

    def _update_yesterday_candle(self):
        for item in self._yesterday_candle_items:
            try:
                self.candle_plot.removeItem(item)
            except Exception:
                pass
        self._yesterday_candle_items.clear()
        sp = self.window().findChild(StrategyPanel)
        if not sp or not sp.yesterday_candle_cb.isChecked():
            return
        try:
            rates = mt5.copy_rates_from_pos(self.current_symbol, mt5.TIMEFRAME_D1, 0, 10)
            if rates is None or len(rates) < 3:
                return
            yesterday = rates[-2]
            high_val = float(yesterday['high'])
            low_val = float(yesterday['low'])
            open_val = float(yesterday['open'])
            close_val = float(yesterday['close'])
            candle_ts = int(yesterday['time'])
            n = len(self.data_df) if self.data_df is not None else 0
            if n < 2:
                return
            x0 = -0.5
            for i in range(n):
                if self._raw_times[i] >= candle_ts:
                    x0 = float(i) - 0.5
                    break
            x1 = float(n) - 0.5
            box_height = high_val - low_val
            if box_height <= 0:
                return
            is_bull = close_val >= open_val
            body = abs(close_val - open_val)
            ratio = min(body / box_height, 1.0) if box_height > 0 else 0.5
            g_r, g_g, g_b = 38, 166, 154
            r_r, r_g, r_b = 239, 83, 80
            if is_bull:
                hex_color = "#26a69a"
            else:
                hex_color = "#ef5350"
            base_alpha = int(40 + ratio * 80)
            q1 = low_val + box_height * 0.25
            q2 = low_val + box_height * 0.50
            q3 = low_val + box_height * 0.75
            if is_bull:
                colors = [
                    (g_r, g_g, g_b),
                    (int(g_r * 0.75 + r_r * 0.25), int(g_g * 0.75 + r_g * 0.25), int(g_b * 0.75 + r_b * 0.25)),
                    (int(g_r * 0.50 + r_r * 0.50), int(g_g * 0.50 + r_g * 0.50), int(g_b * 0.50 + r_b * 0.50)),
                    (int(g_r * 0.25 + r_r * 0.75), int(g_g * 0.25 + r_g * 0.75), int(g_b * 0.25 + r_b * 0.75)),
                ]
                alphas = [base_alpha, int(base_alpha * 0.80), int(base_alpha * 0.60), int(base_alpha * 0.40)]
            else:
                colors = [
                    (int(r_r * 0.25 + g_r * 0.75), int(r_g * 0.25 + g_g * 0.75), int(r_b * 0.25 + g_b * 0.75)),
                    (int(r_r * 0.50 + g_r * 0.50), int(r_g * 0.50 + g_g * 0.50), int(r_b * 0.50 + g_b * 0.50)),
                    (int(r_r * 0.75 + g_r * 0.25), int(r_g * 0.75 + g_g * 0.25), int(r_b * 0.75 + g_b * 0.25)),
                    (r_r, r_g, r_b),
                ]
                alphas = [int(base_alpha * 0.40), int(base_alpha * 0.60), int(base_alpha * 0.80), base_alpha]
            zones = [
                (low_val, q1, colors[0], alphas[0]),
                (q1, q2, colors[1], alphas[1]),
                (q2, q3, colors[2], alphas[2]),
                (q3, high_val, colors[3], alphas[3]),
            ]
            for z_bot, z_top, z_col, z_alpha in zones:
                rect = QtWidgets.QGraphicsRectItem(
                    QtCore.QRectF(x0, z_bot, x1 - x0, z_top - z_bot))
                rect.setBrush(pg.mkBrush(z_col[0], z_col[1], z_col[2], z_alpha))
                rect.setPen(pg.mkPen(hex_color, width=1, style=QtCore.Qt.DashLine))
                rect.setZValue(2)
                self.candle_plot.addItem(rect)
                self._yesterday_candle_items.append(rect)
            for qy, qlbl in [(q1, "25%"), (q2, "50%"), (q3, "75%")]:
                q_line = pg.PlotDataItem([x0, x1], [qy, qy],
                                        pen=pg.mkPen(hex_color, width=1, style=QtCore.Qt.DotLine))
                q_line.setZValue(3)
                self.candle_plot.addItem(q_line)
                self._yesterday_candle_items.append(q_line)
            import pyqtgraph as _pg
            hi_lbl = _pg.TextItem(f"YD HIGH  {high_val:.5f}", color=hex_color, anchor=(0, 1))
            hi_lbl.setFont(_pg.QtGui.QFont("Arial", 9, _pg.QtGui.QFont.Bold))
            hi_lbl.setPos(x0, high_val)
            lo_lbl = _pg.TextItem(f"YD LOW  {low_val:.5f}", color=hex_color, anchor=(0, 0))
            lo_lbl.setFont(_pg.QtGui.QFont("Arial", 9, _pg.QtGui.QFont.Bold))
            lo_lbl.setPos(x0, low_val)
            mid_lbl = _pg.TextItem(f"YD 50%  {q2:.5f}", color=hex_color, anchor=(0, 0.5))
            mid_lbl.setFont(_pg.QtGui.QFont("Arial", 9, _pg.QtGui.QFont.Bold))
            mid_lbl.setPos(x0, q2)
            self.candle_plot.addItem(hi_lbl)
            self.candle_plot.addItem(lo_lbl)
            self.candle_plot.addItem(mid_lbl)
            self._yesterday_candle_items.extend([hi_lbl, lo_lbl, mid_lbl])
        except Exception as e:
            Logger.error(f"YesterdayCandle error: {e}")

    def _update_h4_hl(self):
        for item in self._h4_hl_items:
            try:
                self.candle_plot.removeItem(item)
            except Exception:
                pass
        self._h4_hl_items.clear()
        sp = self.window().findChild(StrategyPanel)
        if not sp or not sp.h4_hl_cb.isChecked():
            return
        try:
            rates = mt5.copy_rates_from_pos(self.current_symbol, mt5.TIMEFRAME_H4, 0, 50)
            if rates is None or len(rates) < 3:
                return
            level_candle = self._find_level_candle(rates)
            if level_candle is None:
                return
            ceiling = float(level_candle['high'])
            floor_val = float(level_candle['low'])
            open_val = float(level_candle['open'])
            h4_start_ts = int(level_candle['time'])
            n = len(self.data_df) if self.data_df is not None else 0
            if n < 2:
                return
            x0 = -0.5
            for i in range(n):
                if self._raw_times[i] >= h4_start_ts:
                    x0 = float(i) - 0.5
                    break
            x1 = float(n) - 0.5
            info = mt5.symbol_info(self.current_symbol)
            if info:
                pip = info.point * 10 if info.point <= 0.001 else info.point
            else:
                pip = 0.0001
            half = pip / 2.0
            ceil_brush = pg.mkBrush(247, 118, 142, 50)
            floor_brush = pg.mkBrush(115, 218, 202, 50)
            ceil_rect = QtWidgets.QGraphicsRectItem(
                QtCore.QRectF(x0, ceiling - half, x1 - x0, pip))
            ceil_rect.setBrush(ceil_brush)
            ceil_rect.setPen(pg.mkPen("#f7768e", width=1))
            ceil_rect.setZValue(3)
            floor_rect = QtWidgets.QGraphicsRectItem(
                QtCore.QRectF(x0, floor_val - half, x1 - x0, pip))
            floor_rect.setBrush(floor_brush)
            floor_rect.setPen(pg.mkPen("#73daca", width=1))
            floor_rect.setZValue(3)
            self.candle_plot.addItem(ceil_rect)
            self.candle_plot.addItem(floor_rect)
            self._h4_hl_items.extend([ceil_rect, floor_rect])
            import pyqtgraph as _pg
            ceil_lbl = _pg.TextItem(f"H4 CEIL  {ceiling:.5f}", color="#f7768e", anchor=(0, 1))
            ceil_lbl.setFont(_pg.QtGui.QFont("Arial", 9, _pg.QtGui.QFont.Bold))
            ceil_lbl.setPos(x0, ceiling)
            floor_lbl = _pg.TextItem(f"H4 FLOOR  {floor_val:.5f}", color="#73daca", anchor=(0, 0))
            floor_lbl.setFont(_pg.QtGui.QFont("Arial", 9, _pg.QtGui.QFont.Bold))
            floor_lbl.setPos(x0, floor_val)
            self.candle_plot.addItem(ceil_lbl)
            self.candle_plot.addItem(floor_lbl)
            self._h4_hl_items.extend([ceil_lbl, floor_lbl])
            open_pen = pg.mkPen("#e0af68", width=1, style=QtCore.Qt.DashLine)
            open_line = pg.PlotCurveItem(x=[x0, x1], y=[open_val, open_val], pen=open_pen)
            open_line.setZValue(4)
            self.candle_plot.addItem(open_line)
            open_lbl = _pg.TextItem(f"H4 OPEN  {open_val:.5f}", color="#e0af68", anchor=(0, 1))
            open_lbl.setFont(_pg.QtGui.QFont("Arial", 9, _pg.QtGui.QFont.Bold))
            open_lbl.setPos(x0, open_val)
            self.candle_plot.addItem(open_lbl)
            self._h4_hl_items.extend([open_line, open_lbl])
        except Exception as e:
            Logger.error(f"H4HL error: {e}")

    def _update_h1_hl(self):
        for item in self._h1_hl_items:
            try:
                self.candle_plot.removeItem(item)
            except Exception:
                pass
        self._h1_hl_items.clear()
        sp = self.window().findChild(StrategyPanel)
        if not sp or not sp.h1_hl_cb.isChecked():
            return
        try:
            rates = mt5.copy_rates_from_pos(self.current_symbol, mt5.TIMEFRAME_H1, 0, 50)
            if rates is None or len(rates) < 3:
                return
            level_candle = self._find_level_candle(rates)
            if level_candle is None:
                return
            ceiling = float(level_candle['high'])
            floor_val = float(level_candle['low'])
            open_val = float(level_candle['open'])
            h1_start_ts = int(level_candle['time'])
            n = len(self.data_df) if self.data_df is not None else 0
            if n < 2:
                return
            x0 = -0.5
            for i in range(n):
                if self._raw_times[i] >= h1_start_ts:
                    x0 = float(i) - 0.5
                    break
            x1 = float(n) - 0.5
            info = mt5.symbol_info(self.current_symbol)
            if info:
                pip = info.point * 10 if info.point <= 0.001 else info.point
            else:
                pip = 0.0001
            half = pip / 2.0
            ceil_brush = pg.mkBrush(247, 118, 142, 50)
            floor_brush = pg.mkBrush(115, 218, 202, 50)
            ceil_rect = QtWidgets.QGraphicsRectItem(
                QtCore.QRectF(x0, ceiling - half, x1 - x0, pip))
            ceil_rect.setBrush(ceil_brush)
            ceil_rect.setPen(pg.mkPen("#f7768e", width=1))
            ceil_rect.setZValue(3)
            floor_rect = QtWidgets.QGraphicsRectItem(
                QtCore.QRectF(x0, floor_val - half, x1 - x0, pip))
            floor_rect.setBrush(floor_brush)
            floor_rect.setPen(pg.mkPen("#73daca", width=1))
            floor_rect.setZValue(3)
            self.candle_plot.addItem(ceil_rect)
            self.candle_plot.addItem(floor_rect)
            self._h1_hl_items.extend([ceil_rect, floor_rect])
            import pyqtgraph as _pg
            ceil_lbl = _pg.TextItem(f"H1 CEIL  {ceiling:.5f}", color="#f7768e", anchor=(0, 1))
            ceil_lbl.setFont(_pg.QtGui.QFont("Arial", 9, _pg.QtGui.QFont.Bold))
            ceil_lbl.setPos(x0, ceiling)
            floor_lbl = _pg.TextItem(f"H1 FLOOR  {floor_val:.5f}", color="#73daca", anchor=(0, 0))
            floor_lbl.setFont(_pg.QtGui.QFont("Arial", 9, _pg.QtGui.QFont.Bold))
            floor_lbl.setPos(x0, floor_val)
            self.candle_plot.addItem(ceil_lbl)
            self.candle_plot.addItem(floor_lbl)
            self._h1_hl_items.extend([ceil_lbl, floor_lbl])
            open_pen = pg.mkPen("#e0af68", width=1, style=QtCore.Qt.DashLine)
            open_line = pg.PlotCurveItem(x=[x0, x1], y=[open_val, open_val], pen=open_pen)
            open_line.setZValue(4)
            self.candle_plot.addItem(open_line)
            open_lbl = _pg.TextItem(f"H1 OPEN  {open_val:.5f}", color="#e0af68", anchor=(0, 1))
            open_lbl.setFont(_pg.QtGui.QFont("Arial", 9, _pg.QtGui.QFont.Bold))
            open_lbl.setPos(x0, open_val)
            self.candle_plot.addItem(open_lbl)
            self._h1_hl_items.extend([open_line, open_lbl])
        except Exception as e:
            Logger.error(f"H1HL error: {e}")

    def _update_open_day(self):
        for item in self._open_day_items:
            try:
                self.candle_plot.removeItem(item)
            except Exception:
                pass
        self._open_day_items.clear()
        sp = self.window().findChild(StrategyPanel)
        if not sp or not sp.open_day_cb.isChecked():
            return
        try:
            rates = mt5.copy_rates_from_pos(self.current_symbol, mt5.TIMEFRAME_D1, 0, 2)
            if rates is None or len(rates) < 2:
                return
            open_price = float(rates[-1]['open'])
            n = len(self.data_df) if self.data_df is not None else 0
            if n < 2 or not self._raw_times:
                return
            today_ts = int(rates[-1]['time'])
            x0 = 0.0
            raw_times = self._raw_times
            for i, rt in enumerate(raw_times):
                if rt >= today_ts:
                    x0 = float(i) - 0.5
                    break
            x1 = float(n) - 0.5
            info = mt5.symbol_info(self.current_symbol)
            if info:
                pip = info.point * 10 if info.point <= 0.001 else info.point
            else:
                pip = 0.0001
            half = pip / 2.0
            rect = QtWidgets.QGraphicsRectItem(
                QtCore.QRectF(x0, open_price - half, x1 - x0, pip))
            rect.setBrush(pg.mkBrush(255, 255, 255, 60))
            rect.setPen(pg.mkPen("#ffffff", width=1))
            rect.setZValue(3)
            self.candle_plot.addItem(rect)
            self._open_day_items.append(rect)
            lbl = pg.TextItem(f"OPEN {open_price:.5f}", color="#ffffff", anchor=(0, 1))
            lbl.setFont(pg.QtGui.QFont("Arial", 9, pg.QtGui.QFont.Bold))
            lbl.setPos(x0, open_price)
            self.candle_plot.addItem(lbl)
            self._open_day_items.append(lbl)
        except Exception as e:
            Logger.error(f"OpenDay error: {e}")

    def _update_algoman(self):
        sp = self.window().findChild(StrategyPanel)
        if not sp or not sp.algoman_cb.isChecked():
            if self._algoman_dashboard:
                self._algoman_dashboard.hide()
            for item in self._algoman_items:
                try:
                    self.candle_plot.removeItem(item)
                except Exception:
                    pass
            self._algoman_items.clear()
            return
        cfg = getattr(sp, 'algoman_cfg', {})
        if not cfg.get("enableDashboard", True):
            if self._algoman_dashboard:
                self._algoman_dashboard.hide()
        if self.data_df is None or len(self.data_df) < 250:
            return
        try:
            for item in self._algoman_items:
                try:
                    self.candle_plot.removeItem(item)
                except Exception:
                    pass
            self._algoman_items.clear()
            result = self._algoman_engine.calculate(self.data_df, cfg)
            if not result:
                return
            if cfg.get("enableDashboard", True):
                if self._algoman_dashboard is None:
                    self._algoman_dashboard = AlgomanDashboardWidget(self.window())
                self._algoman_dashboard.update_data(result)
                if not self._algoman_dashboard.isVisible():
                    self._algoman_dashboard.show()
            for tl in result.get("auto_trendlines", []):
                pen = pg.mkPen(tl["color"], width=2, style=QtCore.Qt.SolidLine)
                line = pg.PlotDataItem([tl["x1"], tl["x2"]], [tl["y1"], tl["y2"]], pen=pen)
                line.setZValue(10)
                self.candle_plot.addItem(line)
                self._algoman_items.append(line)
            for lv in result.get("auto_sr", []):
                pen = pg.mkPen("#bb9af7", width=1, style=QtCore.Qt.DashDotLine)
                line = pg.InfiniteLine(pos=lv, angle=0, movable=False, pen=pen)
                line.setZValue(9)
                self.candle_plot.addItem(line)
                self._algoman_items.append(line)
        except Exception as e:
            Logger.error(f"Algoman error: {e}")

    def _update_session_break(self):
        for item in self._session_break_items:
            try:
                self.candle_plot.removeItem(item)
            except Exception:
                pass
        self._session_break_items.clear()
        sp = self.window().findChild(StrategyPanel)
        if not sp or not sp.session_break_cb.isChecked():
            return
        cfg = getattr(sp, 'session_break_cfg', {})
        sessions = cfg.get("sessions", {})
        if not sessions:
            return
        if self.data_df is None or len(self.data_df) < 2:
            return
        try:
            now = datetime.datetime.now()
            n = len(self.data_df)
            x_now = float(n) - 0.5
            for name, s in sessions.items():
                if not s.get("enabled", True):
                    continue
                sh = s.get("start_h", 0)
                sm = s.get("start_m", 0)
                eh = s.get("end_h", 23)
                em = s.get("end_m", 59)
                color = s.get("color", "#565f89")
                start_x = x_now - ((now.hour * 60 + now.minute) - (sh * 60 + sm)) / 1440.0 * 200
                end_x = x_now - ((now.hour * 60 + now.minute) - (eh * 60 + em)) / 1440.0 * 200
                if start_x < -0.5:
                    start_x = -0.5
                if end_x > x_now:
                    end_x = x_now
                if end_x <= start_x:
                    continue
                rect = QtWidgets.QGraphicsRectItem(
                    QtCore.QRectF(start_x, 0, end_x - start_x, 1))
                rect.setBrush(pg.mkBrush(QtGui.QColor(color)))
                rect.setPen(pg.mkPen(QtGui.QColor(color), width=0))
                rect.setOpacity(0.08)
                rect.setZValue(1)
                rect.setRect(rect.rect().x(), 0, rect.rect().width(), 10000)
                self.candle_plot.addItem(rect)
                self._session_break_items.append(rect)
                if cfg.get("show_labels", True):
                    lbl = pg.TextItem(name, color=color, anchor=(0.5, 1))
                    lbl.setFont(pg.QtGui.QFont("Arial", 8, pg.QtGui.QFont.Bold))
                    lbl.setPos((start_x + end_x) / 2, 0)
                    lbl.setZValue(12)
                    self.candle_plot.addItem(lbl)
                    self._session_break_items.append(lbl)
        except Exception as e:
            Logger.error(f"SessionBreak error: {e}")

    def _update_vwap(self):
        for item in self._vwap_items:
            try:
                self.candle_plot.removeItem(item)
            except Exception:
                pass
        self._vwap_items.clear()
        sp = self.window().findChild(StrategyPanel)
        if not sp or not sp.vwap_cb.isChecked():
            return
        if self.data_df is None or len(self.data_df) < 10:
            return
        try:
            self._vwap_engine.cfg = dict(sp.vwap_cfg)
            df = self.data_df
            o = df["open"].values.astype(float)
            h = df["high"].values.astype(float)
            l = df["low"].values.astype(float)
            c = df["close"].values.astype(float)
            v = df["volume"].values.astype(float) if "volume" in df.columns else np.ones(len(df))
            result = self._vwap_engine.compute(o, h, l, c, v)
            if result is None:
                Logger.info("[VWAP] compute returned None")
                return
            n = result["n"]
            en = result["enabled"]
            Logger.info(f"[VWAP] n={n} enabled={en} prim={self._vwap_engine.cfg.get('prim')}")
            x = np.arange(n, dtype=float)
            cfg = self._vwap_engine.cfg
            c_map = {
                0: str(cfg.get("c_ses", "#d99b1e")),
                1: str(cfg.get("c_wk", "#3b82f6")),
                2: str(cfg.get("c_mo", "#8b5cf6")),
                3: str(cfg.get("c_sh", "#e8365f")),
                4: str(cfg.get("c_sl", "#00a89d")),
                5: str(cfg.get("c_hv", "#d97706")),
                6: str(cfg.get("c_sw", "#0ea5e9")),
            }
            for k2 in c_map:
                if not c_map[k2].startswith("#"):
                    c_map[k2] = "#888888"
            names = ["Session", "Week", "Month", "Swing High", "Swing Low", "High Volume", "Sweep"]
            for j in range(7):
                if not result["enabled"][j]:
                    continue
                arr = result["all_vwaps"][j]
                mask = ~np.isnan(arr)
                if not np.any(mask):
                    continue
                color = c_map[j]
                pi = pg.PlotDataItem(x[mask], arr[mask], pen=pg.mkPen(color, width=2))
                pi.setZValue(8)
                self.candle_plot.addItem(pi)
                self._vwap_items.append(pi)
            if cfg.get("show_band", True):
                bu1 = result["bands_u1"]
                bd1 = result["bands_d1"]
                bu2 = result["bands_u2"]
                bd2 = result["bands_d2"]
                bv = result["vwap"]
                silv = str(cfg.get("silv", "#5c6b80"))
                if not silv.startswith("#"):
                    silv = "#5c6b80"
                mask = ~np.isnan(bv) & ~np.isnan(bu1) & ~np.isnan(bd1) & ~np.isnan(bu2) & ~np.isnan(bd2)
                if np.any(mask):
                    xm = x[mask]
                    upper1 = bu1[mask]
                    lower1 = bd1[mask]
                    upper2 = bu2[mask]
                    lower2 = bd2[mask]
                    line_w = pg.mkPen(silv, width=1, style=QtCore.Qt.DashLine)
                    pi_u1 = pg.PlotDataItem(xm, upper1, pen=line_w)
                    pi_d1 = pg.PlotDataItem(xm, lower1, pen=line_w)
                    pi_u2 = pg.PlotDataItem(xm, upper2, pen=pg.mkPen(silv, width=1))
                    pi_d2 = pg.PlotDataItem(xm, lower2, pen=pg.mkPen(silv, width=1))
                    pi_vw = pg.PlotDataItem(xm, bv[mask], pen=pg.mkPen("#ffffff", width=2, style=QtCore.Qt.DashDotLine))
                    for pi in [pi_u1, pi_d1, pi_u2, pi_d2, pi_vw]:
                        pi.setZValue(7)
                        self.candle_plot.addItem(pi)
                        self._vwap_items.append(pi)
                    fill_upper = pg.graphicsItems.FillBetweenItem.FillBetweenItem(pi_u1, pi_u2)
                    fill_lower = pg.graphicsItems.FillBetweenItem.FillBetweenItem(pi_d1, pi_d2)
                    fill_upper.setBrush(pg.mkBrush(QtGui.QColor("#e8365f")))
                    _no_pen = QtGui.QPen(); _no_pen.setStyle(QtCore.Qt.NoPen)
                    fill_upper.setPen(_no_pen)
                    fill_upper.setOpacity(0.07)
                    fill_lower.setBrush(pg.mkBrush(QtGui.QColor("#00a89d")))
                    fill_lower.setPen(_no_pen)
                    fill_lower.setOpacity(0.07)
                    fill_upper.setZValue(6)
                    fill_lower.setZValue(6)
                    self.candle_plot.addItem(fill_upper)
                    self.candle_plot.addItem(fill_lower)
                    self._vwap_items.extend([fill_upper, fill_lower])
            sigs = result.get("sigs", [])
            h_range = float(np.nanmax(h)) - float(np.nanmin(l)) if len(h) > 0 else 0.001
            sig_gap = h_range * 0.03
            for idx, side, price, tooltip in sigs:
                try:
                    if side == "bull":
                        arrow = pg.TextItem("\u25B2", color="#00a89d", anchor=(0.5, 1))
                        arrow.setFont(pg.QtGui.QFont("Arial", 16, pg.QtGui.QFont.Bold))
                        arrow.setPos(idx, price - sig_gap)
                        arrow.setZValue(20)
                        self.candle_plot.addItem(arrow)
                        self._vwap_items.append(arrow)
                        lbl = pg.TextItem("\u03C3", color="#06222b", anchor=(0.5, 0.5))
                        lbl.setFont(pg.QtGui.QFont("Arial", 10, pg.QtGui.QFont.Bold))
                        lbl.setPos(idx, price - sig_gap)
                        lbl.setZValue(21)
                        bg = QtWidgets.QGraphicsRectItem(QtCore.QRectF(float(idx - 0.4), float(price - sig_gap - h_range * 0.008), 0.8, float(h_range * 0.016)))
                        bg.setBrush(pg.mkBrush(QtGui.QColor("#00a89d")))
                        pen = QtGui.QPen(); pen.setStyle(QtCore.Qt.NoPen); bg.setPen(pen)
                        bg.setZValue(20)
                        self.candle_plot.addItem(bg)
                        self.candle_plot.addItem(lbl)
                        self._vwap_items.extend([bg, lbl])
                    else:
                        arrow = pg.TextItem("\u25BC", color="#e8365f", anchor=(0.5, 0))
                        arrow.setFont(pg.QtGui.QFont("Arial", 16, pg.QtGui.QFont.Bold))
                        arrow.setPos(idx, price + sig_gap)
                        arrow.setZValue(20)
                        self.candle_plot.addItem(arrow)
                        self._vwap_items.append(arrow)
                        lbl = pg.TextItem("\u03C3", color="#2b0612", anchor=(0.5, 0.5))
                        lbl.setFont(pg.QtGui.QFont("Arial", 10, pg.QtGui.QFont.Bold))
                        lbl.setPos(idx, price + sig_gap)
                        lbl.setZValue(21)
                        bg = QtWidgets.QGraphicsRectItem(QtCore.QRectF(float(idx - 0.4), float(price + sig_gap - h_range * 0.008), 0.8, float(h_range * 0.016)))
                        bg.setBrush(pg.mkBrush(QtGui.QColor("#e8365f")))
                        pen = QtGui.QPen(); pen.setStyle(QtCore.Qt.NoPen); bg.setPen(pen)
                        bg.setZValue(20)
                        self.candle_plot.addItem(bg)
                        self.candle_plot.addItem(lbl)
                        self._vwap_items.extend([bg, lbl])
                except Exception as e2:
                    Logger.error(f"VWAP sig draw error: {e2}")
        except Exception as e:
            import traceback
            Logger.error(f"VWAP error: {e}\n{traceback.format_exc()}")

    def _detect_broker_offset(self, symbol):
        if not hasattr(self, '_broker_offset_cache'):
            self._broker_offset_cache = {}
        if symbol in self._broker_offset_cache:
            return self._broker_offset_cache[symbol]
        try:
            d1 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, 0, 2)
            if d1 is not None and len(d1) >= 2:
                prev_daily = d1[-2]
                midnight_utc = datetime.datetime.utcfromtimestamp(prev_daily['time'])
                offset = (24 - midnight_utc.hour) % 24
                if offset > 12:
                    offset -= 24
                self._broker_offset_cache[symbol] = offset
                return offset
        except Exception:
            pass
        self._broker_offset_cache[symbol] = 3
        return 3

    def _calc_prep_atr(self, symbol, tf, length=20):
        try:
            rates = mt5.copy_rates_from_pos(symbol, tf, 0, length + 1)
            if rates is None or len(rates) < length:
                return 0.001
            highs = np.array([r['high'] for r in rates], dtype=float)
            lows = np.array([r['low'] for r in rates], dtype=float)
            closes = np.array([r['close'] for r in rates], dtype=float)
            tr = np.maximum(highs[1:] - lows[1:],
                           np.maximum(np.abs(highs[1:] - closes[:-1]),
                                      np.abs(lows[1:] - closes[:-1])))
            atr = np.mean(tr[-length:])
            return atr if atr > 0 else 0.001
        except Exception:
            return 0.001

    def _update_tf_trends(self):
        for tf_name in ["M1", "M2", "M3", "M5", "M10", "M15", "M30", "H1", "H4", "D1"]:
            btn = self.tf_btn_map.get(tf_name)
            if btn is None:
                continue
            try:
                tf = TIMEFRAMES.get(tf_name)
                if tf is None:
                    continue
                rates = mt5.copy_rates_from_pos(self.current_symbol, tf, 0, 30)
                if rates is None or len(rates) < 21:
                    btn.setStyleSheet(self._tf_btn_style_for(tf_name, "neutral"))
                    continue
                closes = np.array([r["close"] for r in rates])
                ema20 = np.mean(closes[-20:])
                ema20_prev = np.mean(closes[-21:-1])
                diff = closes[-1] - ema20
                slope = ema20 - ema20_prev
                if slope > 0 and diff > 0:
                    trend = "bull"
                elif slope < 0 and diff < 0:
                    trend = "bear"
                else:
                    trend = "neutral"
                btn.setStyleSheet(self._tf_btn_style_for(tf_name, trend))
            except Exception:
                btn.setStyleSheet(self._tf_btn_style_for(tf_name, "neutral"))

    def _tf_btn_style_for(self, tf_name, trend):
        is_active = tf_name == self.current_tf
        if trend == "bull":
            border_c = "#26a69a"
            bg_grad = "stop:0 #1a3d38,stop:1 #132e2a"
            hover_bg = "#1a3d38"
        elif trend == "bear":
            border_c = "#ef5350"
            bg_grad = "stop:0 #3d1a1a,stop:1 #2e1313"
            hover_bg = "#3d1a1a"
        else:
            border_c = "#e0a030"
            bg_grad = "stop:0 #3d3018,stop:1 #2e230f"
            hover_bg = "#3d3018"
        if is_active:
            if trend == "bull":
                active_bg = "stop:0 #26a69a,stop:1 #1a7a6e"
            elif trend == "bear":
                active_bg = "stop:0 #ef5350,stop:1 #b33b3b"
            else:
                active_bg = "stop:0 #e0a030,stop:1 #b38020"
            return (
                f"QPushButton{{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,{active_bg});"
                f"border:2px solid {border_c};border-radius:6px;font-size:11px;font-weight:bold;"
                f"color:#0a0a1a;padding:4px 8px}}"
            )
        else:
            return (
                f"QPushButton{{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,{bg_grad});"
                f"border:2px solid {border_c};border-radius:6px;font-size:11px;font-weight:bold;color:#c0caf5;"
                f"padding:4px 8px}}"
                f"QPushButton:hover{{background:{hover_bg};border-color:{border_c}}}"
            )

    def _get_watchlist_symbols(self):
        mw = self.window()
        if mw and hasattr(mw, 'watchlist_panel'):
            symbols = mw.watchlist_panel.all_symbols
            if symbols:
                return list(symbols)
        return [self.current_symbol]

    def _navigate_symbol(self, direction):
        symbols = self._get_watchlist_symbols()
        if not symbols:
            return
        if self.current_symbol in symbols:
            self._symbol_index = symbols.index(self.current_symbol)
        self._symbol_index = (self._symbol_index + direction) % len(symbols)
        new_sym = symbols[self._symbol_index]
        self.set_symbol(new_sym)
        mw = self.window()
        if mw and hasattr(mw, 'watchlist_panel'):
            mw.watchlist_panel.highlight_symbol(new_sym)

    def _prev_symbol(self):
        self._navigate_symbol(-1)

    def _next_symbol(self):
        self._navigate_symbol(1)

    def _toggle_candle_timer(self):
        self._candle_timer_visible = not self._candle_timer_visible
        if self._candle_timer_visible:
            try:
                import MetaTrader5 as mt5
                tick = mt5.symbol_info_tick(self.current_symbol)
                if tick:
                    self._candle_timer_widget.update_timers(int(tick.time))
                pos = self.mapToGlobal(QtCore.QPoint(self.width() - 480, 60))
                self._candle_timer_widget.move(pos)
                self._candle_timer_widget.show()
            except Exception:
                pass
        else:
            self._candle_timer_widget.hide()

    def _pick_bg_color(self):
        current = self.candle_plot.backgroundBrush().color().name() if not self.candle_plot.backgroundBrush().isOpaque() else "#0a0a1a"
        try:
            br = self.candle_plot.backgroundBrush()
            if br.style() != QtCore.Qt.NoBrush:
                current = br.color().name()
            else:
                current = "#0a0a1a"
        except Exception:
            current = "#0a0a1a"
        color = QtWidgets.QColorDialog.getColor(QtGui.QColor(current), self, "Chart Background Color", QtWidgets.QColorDialog.ShowAlphaChannel)
        if color.isValid():
            hex_c = color.name()
            self.candle_plot.setBackground(hex_c)
            self._save_bg_color(hex_c)
            self.btn_bg_color.setStyleSheet(
                f"QPushButton{{background:#24283b;border:1px solid #292e42;border-radius:6px;font-size:16px;color:{hex_c};padding:2px}}"
                "QPushButton:hover{background:#292e42;border-color:#7aa2f7}"
            )
            sp = self.window().findChild(StrategyPanel)
            if sp and sp.ichimoku_cb.isChecked():
                self._update_ichimoku()

    def _save_bg_color(self, hex_c):
        try:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
            config = {}
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    config = json.load(f)
            if "settings" not in config:
                config["settings"] = {}
            config["settings"]["chart_bg_color"] = hex_c
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            Logger.error(f"Failed to save bg color: {e}")

    def _load_bg_color(self):
        try:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    config = json.load(f)
                hex_c = config.get("settings", {}).get("chart_bg_color", "")
                if hex_c:
                    self.candle_plot.setBackground(hex_c)
                    self.btn_bg_color.setStyleSheet(
                        f"QPushButton{{background:#24283b;border:1px solid #292e42;border-radius:6px;font-size:16px;color:{hex_c};padding:2px}}"
                        "QPushButton:hover{background:#292e42;border-color:#7aa2f7}"
                    )
        except Exception:
            pass

    def _update_candle_colors(self):
        try:
            import MetaTrader5 as mt5
            tf_map = {
                "D1": mt5.TIMEFRAME_D1, "H4": mt5.TIMEFRAME_H4, "H1": mt5.TIMEFRAME_H1,
                "M30": mt5.TIMEFRAME_M30, "M15": mt5.TIMEFRAME_M15, "M10": mt5.TIMEFRAME_M10, "M5": mt5.TIMEFRAME_M5,
            }
            for tf_name, tf_const in tf_map.items():
                rates = mt5.copy_rates_from_pos(self.current_symbol, tf_const, 0, 3)
                if rates is None or len(rates) < 2:
                    continue
                prev = rates[-2]
                curr = rates[-1]
                prev_bull = float(prev['close']) > float(prev['open'])
                curr_bull = float(curr['close']) > float(curr['open'])
                self._candle_timer_widget.update_candle_colors(tf_name, prev_bull, curr_bull)
        except Exception:
            pass
            self._candle_timer_widget.hide()

    def _toggle_all_indicators(self):
        sp = self.window().findChild(StrategyPanel) if self.window() else None
        if not sp:
            return
        checkboxes = [
            sp.ichimoku_cb, sp.week_hl_cb, sp.day_hl_cb, sp.h4_hl_cb,
            sp.h1_hl_cb, sp.open_day_cb, sp.ma_cb,
            sp.zone_setup_cb, sp.session_break_cb, sp.algoman_cb,
        ]
        any_on = any(cb.isChecked() for cb in checkboxes)
        new_state = QtCore.Qt.Unchecked if any_on else QtCore.Qt.Checked
        for cb in checkboxes:
            cb.blockSignals(True)
            cb.setChecked(new_state == QtCore.Qt.Checked)
            cb.blockSignals(False)
        sp._on_indicator_toggled()
        if self.btn_toggle_indicators.isChecked():
            self.btn_toggle_indicators.setStyleSheet(
                "QPushButton{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #e0af68,stop:1 #565f89);"
                "border:1px solid #e0af68;border-radius:6px;font-size:10px;font-weight:bold;color:#0a0a1a;"
                "padding:4px 2px}"
            )
        else:
            self.btn_toggle_indicators.setStyleSheet(
                "QPushButton{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #1e2030,stop:1 #181825);"
                "border:1px solid #292e42;border-radius:6px;font-size:10px;font-weight:bold;color:#e0af68;"
                "padding:4px 2px}"
                "QPushButton:hover{background:#292e42;border-color:#e0af68}"
            )

    def _toggle_play(self):
        act_norm = (
            "QPushButton{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #24283b,stop:1 #1a1e30);"
            "border:1px solid #292e42;border-radius:8px;font-size:16px;color:#c0caf5;"
            "padding:4px;min-width:38px;min-height:38px}"
            "QPushButton:hover{background:#292e42;border-color:#7aa2f7;color:#7aa2f7}"
            "QPushButton:pressed{background:#1a1e30;border-color:#565f89}"
        )
        act_red = (
            "QPushButton{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #cc3333,stop:1 #991111);"
            "border:1px solid #cc3333;border-radius:8px;font-size:16px;color:white;"
            "padding:4px;min-width:38px;min-height:38px}"
            "QPushButton:hover{background:#dd4444;border-color:#ff5555}"
        )
        if self.btn_play.isChecked():
            self.btn_play.setText("\u23F8")
            self.btn_play.setStyleSheet(act_red)
            self._play_timer.start(self._play_interval)
        else:
            self.btn_play.setText("\u25B6")
            self.btn_play.setStyleSheet(act_norm)
            self._play_timer.stop()

    def _auto_scan_tick(self):
        try:
            sp = self.window().findChild(StrategyPanel)
            scan_sec = sp.scan_speed.value() if sp else 5
            now = time.time()
            if not hasattr(self, '_last_scan_time'):
                self._last_scan_time = 0
            if now - self._last_scan_time < scan_sec:
                return
            self._last_scan_time = now
            symbols = self._get_watchlist_symbols()
            if len(symbols) <= 1:
                return
            self._symbol_index = (self._symbol_index + 1) % len(symbols)
            new_sym = symbols[self._symbol_index]
            self.set_symbol(new_sym)
            mw = self.window()
            if mw and hasattr(mw, 'watchlist_panel'):
                mw.watchlist_panel.highlight_symbol(new_sym)
        except Exception as e:
            Logger.error(f"Auto scan error: {e}")

    def _get_tf_trend(self, tf_name):
        try:
            tf = TIMEFRAMES.get(tf_name)
            if tf is None:
                return 0
            rates = mt5.copy_rates_from_pos(self.current_symbol, tf, 0, 30)
            if rates is None or len(rates) < 21:
                return 0
            closes = np.array([r["close"] for r in rates])
            ema20 = np.mean(closes[-20:])
            ema20_prev = np.mean(closes[-21:-1])
            slope = ema20 - ema20_prev
            diff = closes[-1] - ema20
            if slope > 0 and diff > 0:
                return 1
            elif slope < 0 and diff < 0:
                return -1
            return 0
        except Exception:
            return 0

    def _clear_pos_lines(self):
        for item in self._pos_lines:
            try:
                scene = self.candle_plot.scene()
                if scene:
                    scene.removeItem(item)
            except Exception:
                pass
        self._pos_lines.clear()

    def _update_pos_lines(self):
        if getattr(self, '_pos_dragging', False):
            return
        if self.trade_panel and self.trade_panel.isVisible():
            return
        self._clear_pos_lines()
        if self.data_df is None or len(self.data_df) == 0:
            return
        if not self._raw_times:
            return
        n = len(self._raw_times)

        items_to_draw = []

        positions = mt5.positions_get()
        if positions:
            for pos in positions:
                if pos.symbol != self.current_symbol:
                    continue
                is_buy = pos.type == mt5.ORDER_TYPE_BUY
                entry = pos.price_open
                sl = pos.sl if pos.sl and pos.sl > 0 else None
                tp = pos.tp if pos.tp and pos.tp > 0 else None
                side_txt = "BUY" if is_buy else "SELL"
                side_color = "#9ece6a" if is_buy else "#f7768e"
                pos_sec = int(pos.time)
                x_start = 0
                for i in range(n - 1, -1, -1):
                    if self._raw_times[i] <= pos_sec:
                        x_start = i
                        break
                info = mt5.symbol_info(pos.symbol)
                items_to_draw.append({
                    "ticket": pos.ticket, "type": "POS",
                    "side_txt": side_txt, "side_color": side_color,
                    "entry": entry, "sl": sl, "tp": tp,
                    "volume": pos.volume, "x_start": x_start, "x_end": n - 1,
                    "symbol": pos.symbol, "digits": info.digits if info else 5,
                })

        orders = mt5.orders_get()
        if orders:
            order_type_map = {0: "BUY LMT", 1: "SELL LMT", 2: "BUY STP", 3: "SELL STP"}
            for o in orders:
                if o.symbol != self.current_symbol:
                    continue
                entry = o.price_open
                sl = o.sl if o.sl and o.sl > 0 else None
                tp = o.tp if o.tp and o.tp > 0 else None
                otype = order_type_map.get(o.type, str(o.type))
                is_buy = o.type in (0, 2)
                side_color = "#9ece6a" if is_buy else "#f7768e"
                ot = o.time_setup
                if isinstance(ot, (int, float)):
                    order_sec = int(ot)
                elif hasattr(ot, 'timestamp'):
                    order_sec = int(ot.timestamp())
                else:
                    order_sec = int(time.time())
                x_start = 0
                for i in range(n - 1, -1, -1):
                    if self._raw_times[i] <= order_sec:
                        x_start = i
                        break
                items_to_draw.append({
                    "ticket": o.ticket, "type": "ORD",
                    "side_txt": otype, "side_color": side_color,
                    "entry": entry, "sl": sl, "tp": tp,
                    "volume": o.volume_current, "x_start": x_start, "x_end": n - 1,
                })

        for item in items_to_draw:
            entry = item["entry"]
            sl = item["sl"]
            tp = item["tp"]
            x_start = item["x_start"]
            x_end = item["x_end"]
            side_color = item["side_color"]
            is_order = item["type"] == "ORD"

            if is_order and sl and sl > 0 and tp and tp > 0:
                box_top = max(entry, sl, tp)
                box_bot = min(entry, sl, tp)
                box_pen = pg.mkPen(side_color, width=2, style=QtCore.Qt.DashLine)
                box_rect = QtWidgets.QGraphicsRectItem(x_start, box_bot, x_end - x_start, box_top - box_bot)
                box_rect.setBrush(pg.mkBrush((0, 0, 0, 0)))
                box_rect.setPen(box_pen)
                self.candle_plot.addItem(box_rect)
                self._pos_lines.append(box_rect)

                sl_zone_top = max(entry, sl)
                sl_zone_bot = min(entry, sl)
                tp_zone_top = max(entry, tp)
                tp_zone_bot = min(entry, tp)

                sl_rect = QtWidgets.QGraphicsRectItem(x_start, sl_zone_bot, x_end - x_start, sl_zone_top - sl_zone_bot)
                sl_rect.setBrush(pg.mkBrush(255, 50, 50, 50))
                sl_rect.setPen(pg.mkPen((0, 0, 0, 0)))
                self.candle_plot.addItem(sl_rect)
                self._pos_lines.append(sl_rect)

                sl_dist = abs(entry - sl)
                tp_ratio = abs(tp - entry) / sl_dist if sl_dist > 0 else 0
                ratios = [r for r in self._get_tp_levels_from_config() if r <= tp_ratio]
                is_buy_ord = entry < tp
                all_zone_prices = []
                all_zone_names = []
                all_zone_colors_rgba = [
                    (0, 230, 118, 40),
                    (0, 200, 83, 50),
                    (34, 180, 80, 55),
                    (50, 210, 100, 50),
                    (80, 230, 140, 45),
                ]
                all_zone_pen_colors = ["#00E676", "#00C853", "#00C853", "#69F0AE", "#B9F6CA"]
                all_zone_names_txt = ["TP50%", "TP1", "TP2", "TP3", "TP4"]
                if ratios:
                    tp50_p = entry + sl_dist * 0.5 if is_buy_ord else entry - sl_dist * 0.5
                    all_zone_prices.append(round(tp50_p, 5))
                    all_zone_names.append("TP50%")
                    for i, r in enumerate(ratios):
                        p = entry + sl_dist * r if is_buy_ord else entry - sl_dist * r
                        all_zone_prices.append(round(p, 5))
                        all_zone_names.append(f"TP{i+1}")
                else:
                    tp50_p = entry + (tp - entry) * 0.5
                    all_zone_prices = [round(tp50_p, 5), round(tp, 5)]
                    all_zone_names = ["TP50%", "TP1"]
                n_zones = min(len(all_zone_prices), len(all_zone_colors_rgba))
                prev = entry
                for i in range(n_zones):
                    tv = all_zone_prices[i]
                    tc = all_zone_colors_rgba[i]
                    tpc = all_zone_pen_colors[i] if i < len(all_zone_pen_colors) else "#81C783"
                    tname = all_zone_names[i] if i < len(all_zone_names) else f"TP{i+1}"
                    r = QtWidgets.QGraphicsRectItem(x_start, min(prev, tv), x_end - x_start, abs(tv - prev))
                    r.setBrush(pg.mkBrush(*tc))
                    r.setPen(pg.mkPen((0, 0, 0, 0)))
                    self.candle_plot.addItem(r)
                    self._pos_lines.append(r)
                    ln = pg.PlotDataItem([x_start, x_end], [tv, tv], pen=pg.mkPen(tpc, width=1.5, style=QtCore.Qt.DashLine))
                    self.candle_plot.addItem(ln)
                    self._pos_lines.append(ln)
                    lbl = pg.TextItem(f"{tname}: {tv:.5f}", color=tpc,
                                      fill=pg.mkBrush(14, 22, 36, 200))
                    lbl.setFont(QtGui.QFont("Segoe UI", 8, QtGui.QFont.Bold))
                    lbl.setPos(x_start, tv)
                    self.candle_plot.addItem(lbl)
                    self._pos_lines.append(lbl)
                    prev = tv

                e_pen = pg.mkPen(side_color, width=2.5)
                e_line = pg.PlotDataItem([x_start, x_end], [entry, entry], pen=e_pen)
                self.candle_plot.addItem(e_line)
                self._pos_lines.append(e_line)

                e_lbl = pg.TextItem(f"[ORD] #{item['ticket']} {item['side_txt']} Entry: {entry:.5f} ({item['volume']:.2f} Lot)",
                                    color=side_color, fill=pg.mkBrush(14, 22, 36, 220))
                e_lbl.setFont(QtGui.QFont("Segoe UI", 7, QtGui.QFont.Bold))
                e_lbl.setPos(x_start, entry)
                self.candle_plot.addItem(e_lbl)
                self._pos_lines.append(e_lbl)

                sl_lbl = pg.TextItem(f"SL: {sl:.5f}", color="#f7768e",
                                     fill=pg.mkBrush(14, 22, 36, 200))
                sl_lbl.setFont(QtGui.QFont("Segoe UI", 7))
                sl_lbl.setPos(x_start, sl)
                self.candle_plot.addItem(sl_lbl)
                self._pos_lines.append(sl_lbl)

                tp_lbl = pg.TextItem(f"TP: {tp:.5f}", color="#7dcfff",
                                     fill=pg.mkBrush(14, 22, 36, 200))
                tp_lbl.setFont(QtGui.QFont("Segoe UI", 7))
                tp_lbl.setPos(x_start, tp)
                self.candle_plot.addItem(tp_lbl)
                self._pos_lines.append(tp_lbl)

            else:
                if sl and sl > 0:
                    sl_top = max(entry, sl)
                    sl_bot = min(entry, sl)
                    sl_rect = QtWidgets.QGraphicsRectItem(x_start, sl_bot, x_end - x_start, sl_top - sl_bot)
                    sl_rect.setBrush(pg.mkBrush(255, 50, 50, 60))
                    sl_rect.setPen(pg.mkPen((0, 0, 0, 0)))
                    self.candle_plot.addItem(sl_rect)
                    self._pos_lines.append(sl_rect)

                if tp and tp > 0:
                    sl_dist_pos = abs(entry - sl) if sl and sl > 0 else abs(tp - entry)
                    tp_ratio_pos = abs(tp - entry) / sl_dist_pos if sl_dist_pos > 0 else 0
                    ratios_pos = [r for r in self._get_tp_levels_from_config() if r <= tp_ratio_pos]
                    is_buy_pos = item["side_txt"] == "BUY"
                    all_zone_prices_pos = []
                    all_zone_names_pos = []
                    zone_colors_rgba = [
                        (0, 230, 118, 40),
                        (0, 200, 83, 50),
                        (34, 180, 80, 55),
                        (50, 210, 100, 50),
                        (80, 230, 140, 45),
                    ]
                    zone_pen_colors = ["#00E676", "#00C853", "#00C853", "#69F0AE", "#B9F6CA"]
                    if ratios_pos:
                        tp50_p = entry + sl_dist_pos * 0.5 if is_buy_pos else entry - sl_dist_pos * 0.5
                        all_zone_prices_pos.append(round(tp50_p, 5))
                        all_zone_names_pos.append("TP50%")
                        for i, r in enumerate(ratios_pos):
                            p = entry + sl_dist_pos * r if is_buy_pos else entry - sl_dist_pos * r
                            all_zone_prices_pos.append(round(p, 5))
                            all_zone_names_pos.append(f"TP{i+1}")
                    else:
                        tp50_p = entry + (tp - entry) * 0.5 if is_buy_pos else entry - (entry - tp) * 0.5
                        all_zone_prices_pos = [round(tp50_p, 5), round(tp, 5)]
                        all_zone_names_pos = ["TP50%", "TP1"]
                    n_zones = min(len(all_zone_prices_pos), len(zone_colors_rgba))
                    prev = entry
                    for i in range(n_zones):
                        tv = all_zone_prices_pos[i]
                        tc = zone_colors_rgba[i]
                        tpc = zone_pen_colors[i] if i < len(zone_pen_colors) else "#81C783"
                        tname = all_zone_names_pos[i] if i < len(all_zone_names_pos) else f"TP{i+1}"
                        r = QtWidgets.QGraphicsRectItem(x_start, min(prev, tv), x_end - x_start, abs(tv - prev))
                        r.setBrush(pg.mkBrush(*tc))
                        r.setPen(pg.mkPen((0, 0, 0, 0)))
                        self.candle_plot.addItem(r)
                        self._pos_lines.append(r)
                        ln = pg.PlotDataItem([x_start, x_end], [tv, tv], pen=pg.mkPen(tpc, width=1.5, style=QtCore.Qt.DashLine))
                        self.candle_plot.addItem(ln)
                        self._pos_lines.append(ln)
                        lbl = pg.TextItem(f"{tname}: {tv:.5f}", color=tpc,
                                          fill=pg.mkBrush(14, 22, 36, 200))
                        lbl.setFont(QtGui.QFont("Segoe UI", 8, QtGui.QFont.Bold))
                        lbl.setPos(x_start, tv)
                        self.candle_plot.addItem(lbl)
                        self._pos_lines.append(lbl)
                        prev = tv

                pen_e = pg.mkPen(side_color, width=2)
                e_line = pg.PlotDataItem([x_start, x_end], [entry, entry], pen=pen_e)
                self.candle_plot.addItem(e_line)
                self._pos_lines.append(e_line)
                e_lbl = pg.TextItem(f"[{item['type']}] #{item['ticket']} {item['side_txt']} Entry: {entry:.5f} ({item['volume']:.2f} Lot)",
                                    color=side_color, fill=pg.mkBrush(14, 22, 36, 220))
                e_lbl.setFont(QtGui.QFont("Segoe UI", 7, QtGui.QFont.Bold))
                e_lbl.setPos(x_start, entry)
                self.candle_plot.addItem(e_lbl)
                self._pos_lines.append(e_lbl)

                if sl and sl > 0:
                    digits = item.get('digits', 5)
                    sl_pen = pg.mkPen("#f7768e", width=1.5, style=QtCore.Qt.DashLine)
                    sl_line = pg.PlotDataItem([x_start, x_end], [sl, sl], pen=sl_pen)
                    self.candle_plot.addItem(sl_line)
                    self._pos_lines.append(sl_line)
                    sl_lbl = pg.TextItem(f"SL: {sl:.{digits}f}", color="#f7768e",
                                         fill=pg.mkBrush(14, 22, 36, 200))
                    sl_lbl.setFont(QtGui.QFont("Segoe UI", 7))
                    sl_lbl.setPos(x_start, sl)
                    self.candle_plot.addItem(sl_lbl)
                    self._pos_lines.append(sl_lbl)

                if tp and tp > 0:
                    digits = item.get('digits', 5)
                    tp_pen = pg.mkPen("#7dcfff", width=1.5, style=QtCore.Qt.DashLine)
                    tp_line = pg.PlotDataItem([x_start, x_end], [tp, tp], pen=tp_pen)
                    self.candle_plot.addItem(tp_line)
                    self._pos_lines.append(tp_line)
                    tp_lbl = pg.TextItem(f"TP: {tp:.{digits}f}", color="#7dcfff",
                                         fill=pg.mkBrush(14, 22, 36, 200))
                    tp_lbl.setFont(QtGui.QFont("Segoe UI", 7))
                    tp_lbl.setPos(x_start, tp)
                    self.candle_plot.addItem(tp_lbl)
                    self._pos_lines.append(tp_lbl)
                    self.candle_plot.addItem(tp_lbl)
                    self._pos_lines.append(tp_lbl)

    def goto_last_candle(self, n_visible=200):
        if self.data_df is None or len(self.data_df) == 0:
            return
        vb = self.candle_plot.plotItem.vb
        n = len(self.data_df)
        n_visible = min(n_visible, n)
        x_start = n - n_visible - 1
        x_end = n + 3
        tail = self.data_df.tail(n_visible)
        y_min = float(tail["low"].min())
        y_max = float(tail["high"].max())
        y_pad = (y_max - y_min) * 0.05 or 0.01
        vb.setRange(
            QtCore.QRectF(x_start, y_min - y_pad, x_end - x_start, y_max - y_min + y_pad * 2),
            padding=0
        )

    def reset_view(self):
        self.goto_last_candle(n_visible=200)

    def _update_x_ticks(self):
        if self.data_df is None or len(self.data_df) == 0:
            return
        times = self.data_df["time"].values
        n = len(times)
        ticks = []
        step = max(1, n // 12)
        prev_date = None
        for i in range(0, n, step):
            ts = pd.to_datetime(times[i])
            cur_date = ts.strftime('%Y-%m-%d')
            if cur_date != prev_date:
                label = ts.strftime('%d %b %H:%M')
                prev_date = cur_date
            else:
                label = ts.strftime('%H:%M')
            ticks.append((i, label))
        if n > 0:
            ts = pd.to_datetime(times[n - 1])
            ticks.append((n - 1, ts.strftime('%H:%M')))
        self.candle_plot.getAxis('bottom').setTicks([ticks])

    def _index_to_time(self, x_idx):
        if self.data_df is None or len(self.data_df) == 0:
            return ""
        idx = int(round(x_idx))
        if idx < 0:
            idx = 0
        if idx >= len(self.data_df):
            idx = len(self.data_df) - 1
        return pd.to_datetime(self.data_df["time"].iloc[idx]).strftime('%Y-%m-%d %H:%M')

    def on_mouse_moved(self, evt):
        pos = evt if isinstance(evt, QtCore.QPointF) else evt[0]
        if self.data_df is None or len(self.data_df) == 0:
            self.v_line.hide()
            self.h_line.hide()
            self.crosshair_label.hide()
            return
        if not self.candle_plot.sceneBoundingRect().contains(pos):
            self.v_line.hide()
            self.h_line.hide()
            self.crosshair_label.hide()
            return

        mouse_point = self.candle_plot.plotItem.vb.mapSceneToView(pos)
        x, y = mouse_point.x(), mouse_point.y()

        n = len(self.data_df)
        if x < 0 or x >= n:
            self.v_line.hide()
            self.h_line.hide()
            self.crosshair_label.hide()
            return

        self.v_line.setPos(x)
        self.h_line.setPos(y)
        self.v_line.show()
        self.h_line.show()
        self.crosshair_label.show()

        dt = self._index_to_time(x)
        self.crosshair_label.setText(
            f"  {dt}  |  Price: {y:.5f}  "
        )
        self.crosshair_label.setPos(x, y)

        if self._trendline_mode and len(self._trendline_points) == 1:
            self._draw_trendline_temp(x, y)

    def on_mouse_click(self, evt):
        if evt.button() == QtCore.Qt.LeftButton:
            if self._trendline_mode:
                pos = evt.scenePos()
                vb = self.candle_plot.plotItem.vb
                point = vb.mapSceneToView(pos)
                self._trendline_points.append((point.x(), point.y()))
                if self._trendline_temp:
                    try:
                        self.candle_plot.removeItem(self._trendline_temp)
                    except Exception:
                        pass
                    self._trendline_temp = None
                if len(self._trendline_points) == 2:
                    self._draw_trendline_final()
                    self._trendline_mode = False
                    self._trendline_points = []
                    self.btn_trendline.setStyleSheet(self._act_btn_style)
                    self.setCursor(Qt.ArrowCursor)
                else:
                    self._draw_trendline_temp(point.x(), point.y())
                return

        if evt.button() != QtCore.Qt.RightButton:
            return
        positions = mt5.positions_get()
        if not positions:
            return
        my_pos = None
        for p in positions:
            if p.symbol == self.current_symbol:
                my_pos = p
                break
        if my_pos is None:
            return

        pos = evt.scenePos()
        vb = self.candle_plot.plotItem.vb
        point = vb.mapSceneToView(pos)
        click_price = point.y()
        info = mt5.symbol_info(self.current_symbol)
        digits = info.digits if info else 5
        click_price = round(click_price, digits)

        menu = QtWidgets.QMenu(self)
        menu.setStyleSheet("""
            QMenu { background: #1a1b26; color: #c0caf5; border: 1px solid #292e42; }
            QMenu::item:selected { background: #292e42; }
        """)

        side = "BUY" if my_pos.type == mt5.ORDER_TYPE_BUY else "SELL"

        act_sl = menu.addAction(f"Set SL: {click_price:.{digits}f}  [{side}]")
        act_tp = menu.addAction(f"Set TP: {click_price:.{digits}f}  [{side}]")

        action = menu.exec_(evt.screenPos().toPoint())
        if action == act_sl:
            res, msg = self.executor.modify_position(my_pos.ticket, sl=click_price)
            if res:
                Logger.info(f"[Chart] SL #{my_pos.ticket} -> {click_price:.{digits}f}")
                self._update_pos_lines()
            else:
                Logger.info(f"[Chart] SL failed #{my_pos.ticket}: {msg}")
        elif action == act_tp:
            res, msg = self.executor.modify_position(my_pos.ticket, tp=click_price)
            if res:
                Logger.info(f"[Chart] TP #{my_pos.ticket} -> {click_price:.{digits}f}")
                self._update_pos_lines()
            else:
                Logger.info(f"[Chart] TP failed #{my_pos.ticket}: {msg}")

    def _toggle_trendline_mode(self):
        self._trendline_mode = not self._trendline_mode
        if self._trendline_mode:
            self._trendline_points = []
            self.btn_trendline.setStyleSheet(
                "QPushButton{background:#292e42;color:#7aa2f7;border:2px solid #7aa2f7;border-radius:6px;font-size:18px;}"
            )
            self.setCursor(Qt.CrossCursor)
        else:
            self._trendline_points = []
            self.btn_trendline.setStyleSheet(act_btn_style)
            self.setCursor(Qt.ArrowCursor)
            if self._trendline_temp:
                try:
                    self.candle_plot.removeItem(self._trendline_temp)
                except Exception:
                    pass
                self._trendline_temp = None

    def _draw_trendline_temp(self, x2, y2):
        if self._trendline_temp:
            try:
                self.candle_plot.removeItem(self._trendline_temp)
            except Exception:
                pass
        x1, y1 = self._trendline_points[0]
        pen = pg.mkPen(self._trendline_color, width=max(0.5, self._trendline_width * 0.7), style=QtCore.Qt.DashLine)
        self._trendline_temp = pg.PlotDataItem([x1, x2], [y1, y2], pen=pen)
        self._trendline_temp.setZValue(150)
        self.candle_plot.addItem(self._trendline_temp, ignoreBounds=True)

    def _draw_trendline_final(self):
        x1, y1 = self._trendline_points[0]
        x2, y2 = self._trendline_points[1]
        self._trendline_width = self._tl_width_spin.value()
        pen = pg.mkPen(self._trendline_color, width=self._trendline_width, style=QtCore.Qt.SolidLine)
        line_item = pg.PlotDataItem([x1, x2], [y1, y2], pen=pen)
        line_item.setZValue(150)
        self.candle_plot.addItem(line_item, ignoreBounds=True)
        self._trendline_items.append(line_item)

    def _pick_trendline_color(self):
        from PyQt5.QtWidgets import QColorDialog
        color = QColorDialog.getColor()
        if color.isValid():
            self._trendline_color = color.name()
            self._tl_color_btn.setStyleSheet(f"background:{self._trendline_color};border:1px solid #565f89;border-radius:4px;")

    def _clear_trendlines(self):
        for item in self._trendline_items:
            try:
                self.candle_plot.removeItem(item)
            except Exception:
                pass
        self._trendline_items.clear()
        if self._trendline_mode:
            self._toggle_trendline_mode()

    def _get_pip_info(self, price=None):
        info = mt5.symbol_info(self.current_symbol)
        if not info:
            point = 0.0001 if price is None or price > 1 else 0.01
            return point, point * 10, 1
        point = info.point
        pip_size = point * 10 if point <= 0.001 else point
        pip_val = info.trade_tick_value * (10 if point <= 0.001 else 1)
        digits = info.digits
        return point, pip_size, pip_val, digits

    def _get_tp_levels_from_config(self):
        sp = self.window().findChild(StrategyPanel) if hasattr(self, 'window') else None
        if not sp:
            return []
        text = sp.tp_levels_edit.text().strip()
        if not text:
            return []
        ratios = []
        for part in text.split(","):
            part = part.strip()
            if ":" in part:
                r, v = part.split(":")
                ratios.append(float(r.strip()))
        return sorted(ratios)

    def _update_trade_lines(self, entry=None, sl=None, tp=None, side="buy"):
        nudge = self._get_label_x()
        is_market = self.trade_panel and self.trade_panel.order_type.currentText() == "Market"
        self.entry_line.setMovable(not is_market)
        if entry is not None:
            self._trade_entry = entry
            self.entry_line.setValue(entry)
            self.entry_line.show()
            ec = "#9ece6a" if side == "buy" else "#f7768e"
            self.entry_line.setPen(pg.mkPen(ec, width=1.5, style=Qt.DashLine))
            self.entry_label.setColor(ec)
        elif self.entry_line.isVisible():
            entry = self._trade_entry
        point, pip_size, pip_val, digs = self._get_pip_info(entry)
        fmt = f".{digs}f" if digs else ".5f"
        vol = round(self.trade_panel.vol_spin.value(), 2) if self.trade_panel else 0.01
        if entry is not None:
            pos = self.entry_line.value()
            entry_text = f"Entry {pos:{fmt}}"
            self.entry_label.setText(entry_text)
            self.entry_label.setPos(nudge, pos)
            self.entry_label.show()
        else:
            self.entry_label.setPos(nudge, self.entry_line.value())
        if sl is not None:
            self.sl_line.setValue(sl)
            self.sl_line.show()
            if entry is not None:
                sl_pips = abs(entry - sl) / pip_size
                sl_dollar = sl_pips * pip_val * vol
                self.sl_label.setText(f"SL {sl:{fmt}}  ({sl_pips:.0f}p | -${sl_dollar:.2f} | {vol}Lot)")
            else:
                self.sl_label.setText(f"SL {sl:{fmt}}")
            self.sl_label.setPos(nudge, sl)
            self.sl_label.show()
        elif self.sl_line.isVisible():
            self.sl_label.setPos(nudge, self.sl_line.value())
        if tp is not None:
            self.tp_line.setValue(tp)
            self.tp_line.show()
            if entry is not None and sl is not None:
                tp_pips = abs(entry - tp) / pip_size
                tp_dollar = tp_pips * pip_val * vol
                self.tp_label.setText(f"TP {tp:{fmt}}  ({tp_pips:.0f}p | +${tp_dollar:.2f} | {vol}Lot)")
                tp1 = entry + (tp - entry) * 0.5 if side == "buy" else entry - (entry - tp) * 0.5
                tp1 = round(tp1, digs if digs else 5)
                self.tp1_line.setValue(tp1)
                self.tp1_line.show()
                tp1_pips = abs(tp1 - entry) / pip_size
                tp1_dollar = tp1_pips * pip_val * vol
                self.tp1_label.setText(f"TP1 {tp1:{fmt}}  ({tp1_pips:.0f}p | +${tp1_dollar:.2f})")
                self.tp1_label.setPos(nudge, tp1)
                self.tp1_label.show()
            else:
                self.tp_label.setText(f"TP {tp:{fmt}}")
            self.tp_label.setPos(nudge, tp)
            self.tp_label.show()
        else:
            self.tp1_line.hide()
            self.tp1_label.hide()
        if not tp and self.tp_line.isVisible():
            self.tp_label.setPos(nudge, self.tp_line.value())

    def _hide_trade_lines(self):
        self.entry_line.hide()
        self.sl_line.hide()
        self.tp_line.hide()
        self.tp1_line.hide()
        self.entry_label.hide()
        self.sl_label.hide()
        self.tp_label.hide()
        self.tp1_label.hide()

    def _get_label_x(self):
        vb = self.candle_plot.plotItem.vb
        r = vb.viewRect()
        return r.right() if r else 0

    def _reset_pos_dragging(self):
        self._pos_dragging = False
        self._update_pos_lines()

    def _on_range_changed(self):
        self._user_zoomed = True
        if self.trade_panel and self.trade_panel.isVisible():
            self._update_trade_lines()

    def _init_trade_panel(self):
        self.trade_panel = None
        self.executor = MT5Executor()
        self.exit_mgr = ExitManager(self.executor)
        self._trade_pos_timer = QTimer()
        self._trade_pos_timer.timeout.connect(self._refresh_trade_positions)
        self._trade_pos_timer.start(3000)

    def _toggle_trade_panel(self):
        if self.trade_panel is None:
            self.trade_panel = ManualTradePanel()
            self.trade_panel.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool)
            self.trade_panel._chart_widget = self
        visible = not self.trade_panel.isVisible()
        self.trade_panel.setVisible(visible)
        if visible:
            self.trade_panel.set_symbol(self.current_symbol)
            gw = self.window()
            px = gw.x() + 10
            py = gw.y() + 80
            self.trade_panel.move(px, py)
            self.trade_panel.raise_()
            self.trade_panel.activateWindow()
            self._sync_risk_params()
            self.trade_panel.refresh_positions()
        else:
            self._hide_trade_lines()
            self._update_pos_lines()

    def _show_trade_lines(self):
        tick = MT5Connector.get_last_tick(self.current_symbol)
        if tick is None:
            return
        side = "buy" if self.trade_panel.btn_buy.isChecked() else "sell"
        entry = tick.ask if side == "buy" else tick.bid
        info = mt5.symbol_info(self.current_symbol)
        pip_size = info.point * 10 if info and info.point <= 0.001 else (info.point if info else 0.0001)
        sl = entry - pip_size * 3 if side == "buy" else entry + pip_size * 3
        rr = self.trade_panel.rr_value
        diff = abs(entry - sl)
        tp = entry + diff * rr if side == "buy" else entry - diff * rr
        self.trade_panel._set_entry(entry)
        self.trade_panel.sl_price = sl
        self.trade_panel.sl_lbl.setText(f"{sl:.5f}")
        self.trade_panel._calc_risk()
        self.trade_panel._recalc_tp()
        self._update_trade_lines(entry, sl, tp, side)

    def _sync_risk_params(self):
        sp = self.window().findChild(StrategyPanel)
        if sp:
            idx = sp.risk_combo.currentIndex()
            modes = ["% Balance", "$ Fixed", "Fixed Lot"]
            mode = modes[idx]
            val = sp.risk_input.value()
            rr = sp.rr_input.value()
            self.trade_panel.set_risk_params(mode, val, rr)

    def _refresh_trade_positions(self):
        if self.trade_panel is not None and self.trade_panel.isVisible():
            self.trade_panel.refresh_positions()
        mw = self.window()
        if mw and hasattr(mw, 'positions_panel'):
            mw.positions_panel.refresh()
        if hasattr(self, 'exit_mgr'):
            sp = self.window().findChild(StrategyPanel)
            if sp:
                cfg = sp.get_exit_config()
                self.exit_mgr.enabled = cfg["enabled"]
                self.exit_mgr.trail_use_algoman = cfg["trail_use_algoman"]
                self.exit_mgr.trail_algoman_act = cfg["trail_algoman_act"]
                self.exit_mgr.trail_atr_mult = cfg["trail_atr_mult"]
                self.exit_mgr.be_enabled = cfg["be_enabled"]
                self.exit_mgr.be_tp_pct = cfg["be_tp_pct"]
                self.exit_mgr.be_sl_pct = cfg["be_sl_pct"]
                self.exit_mgr.tp_levels_enabled = cfg["tp_levels_enabled"]
                self.exit_mgr.tp_levels = cfg["tp_levels"]
                self.exit_mgr.time_exit_enabled = cfg["time_exit_enabled"]
                self.exit_mgr.time_exit_minutes = cfg["time_exit_minutes"]
            self.exit_mgr.process_positions()
        try:
            self._update_real_sl_marker()
        except Exception:
            pass

    def _update_real_sl_marker(self):
        try:
            import MetaTrader5 as _mt5
            positions = _mt5.positions_get()
            if not positions:
                self.real_sl_line.hide()
                self.real_sl_label.hide()
                return
            sym = self.current_symbol
            pos = None
            for p in positions:
                if p.symbol == sym:
                    pos = p
                    break
            if pos is None or not pos.sl or pos.sl <= 0:
                self.real_sl_line.hide()
                self.real_sl_label.hide()
                return
            info = _mt5.symbol_info(sym)
            digs = info.digits if info else 5
            fmt = f".{digs}f"
            self.real_sl_line.setPos(pos.sl)
            self.real_sl_line.show()
            side = "BUY" if pos.type == _mt5.ORDER_TYPE_BUY else "SELL"
            self.real_sl_label.setText(f"REAL SL {pos.sl:{fmt}} ({side})")
            self.real_sl_label.setPos(self._get_label_x(), pos.sl)
            self.real_sl_label.show()
        except Exception:
            self.real_sl_line.hide()
            self.real_sl_label.hide()

    def _blink_real_sl(self):
        self._real_sl_blink = not self._real_sl_blink
        if self.real_sl_line.isVisible():
            if self._real_sl_blink:
                self.real_sl_line.setPen(pg.mkPen("#ff9e64", width=3, style=QtCore.Qt.SolidLine))
                self.real_sl_label.setColor("#ff9e64")
            else:
                self.real_sl_line.setPen(pg.mkPen("#ff9e64", width=1, style=QtCore.Qt.SolidLine))
                self.real_sl_label.setColor("#ff9e6480")

# ============================================================
#                   پنل اطلاعات اکانت
# ============================================================

class AccountInfoPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("account_panel")
        self.setFixedHeight(60)
        self.setStyleSheet("""
            QFrame#account_panel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0f1117, stop:0.3 #141828, stop:0.7 #141828, stop:1.0 #0f1117);
                border-bottom: 1px solid #292e42;
                border-radius: 0px;
            }
        """)
        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 6, 16, 6)

        self.title = QLabel("\U0001F4CA  MetaTrader 5 Dashboard")
        self.title.setObjectName("title_label")

        self.lbl_account = QLabel("Account: ---")
        self.lbl_account.setObjectName("account_value")
        self.lbl_balance = QLabel("Balance: ---")
        self.lbl_balance.setObjectName("account_value")
        self.lbl_equity = QLabel("Equity: ---")
        self.lbl_equity.setObjectName("account_value")
        self.lbl_margin = QLabel("Margin: ---")
        self.lbl_margin.setObjectName("account_value")
        self.lbl_free_margin = QLabel("Free: ---")
        self.lbl_free_margin.setObjectName("account_value")
        self.lbl_profit = QLabel("P/L: ---")
        self.lbl_profit.setObjectName("account_value")

        self.conn_indicator = QLabel()
        self.conn_indicator.setFixedSize(12, 12)
        self.conn_indicator.setStyleSheet(
            "background-color: #f7768e; border-radius: 6px; border: 1px solid rgba(247,118,142,0.3);"
        )
        self.conn_label = QLabel("Offline")
        self.conn_label.setStyleSheet("color: #f7768e; font-weight: bold; font-size: 10px;")

        self.btn_chart_mode = QPushButton("Candle")
        self.btn_chart_mode.setFixedSize(60, 24)
        self.btn_chart_mode.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_chart_mode.setStyleSheet(
            "QPushButton{background:#1e2030;border:1px solid #292e42;border-radius:4px;"
            "color:#7aa2f7;font-size:9px;font-weight:bold;padding:2px}"
            "QPushButton:hover{background:#292e42;border-color:#7aa2f7}"
        )
        self.btn_chart_mode.clicked.connect(self._toggle_chart_mode)

        self.btn_rinko = QPushButton("Rinko")
        self.btn_rinko.setFixedSize(55, 24)
        self.btn_rinko.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_rinko.setStyleSheet(
            "QPushButton{background:#1e2030;border:1px solid #292e42;border-radius:4px;"
            "color:#565f89;font-size:9px;font-weight:bold;padding:2px}"
            "QPushButton:hover{background:#292e42;border-color:#7aa2f7}"
        )
        self.btn_rinko.clicked.connect(self._toggle_rinko_mode)

        self.btn_refresh = QPushButton("\U0001F504 Refresh")
        self.btn_refresh.setObjectName("refresh_btn")
        self.btn_refresh.clicked.connect(self.refresh)

        sep = lambda: QLabel("\u2502", styleSheet="color: #292e42; font-size: 10px;")

        layout.addWidget(self.title)
        layout.addSpacing(12)
        layout.addWidget(sep())
        layout.addSpacing(8)
        layout.addWidget(self.lbl_account)
        layout.addSpacing(10)
        layout.addWidget(self.lbl_balance)
        layout.addSpacing(10)
        layout.addWidget(self.lbl_equity)
        layout.addSpacing(10)
        layout.addWidget(self.lbl_margin)
        layout.addSpacing(10)
        layout.addWidget(self.lbl_free_margin)
        layout.addSpacing(10)
        layout.addWidget(self.lbl_profit)
        layout.addSpacing(6)
        layout.addWidget(sep())
        layout.addSpacing(6)
        layout.addWidget(self.conn_indicator)
        layout.addWidget(self.conn_label)
        layout.addSpacing(8)
        layout.addWidget(self.btn_chart_mode)
        layout.addWidget(self.btn_rinko)
        layout.addStretch()
        layout.addWidget(self.btn_refresh)

    def refresh(self):
        connected = MT5Connector.is_connected()

        if connected:
            self.conn_indicator.setStyleSheet(
                "background-color: #9ece6a; border-radius: 6px; border: 1px solid rgba(158,206,106,0.3);"
            )
            self.conn_label.setText("Connected")
            self.conn_label.setStyleSheet(
                "color: #9ece6a; font-weight: bold; font-size: 10px;"
            )

            info = MT5Connector.get_account_info()
            if info:
                self.lbl_account.setText(f"Account: {info.login}")
                self.lbl_balance.setText(f"Balance: {info.balance:.2f}")
                self.lbl_equity.setText(f"Equity: {info.equity:.2f}")
                self.lbl_margin.setText(f"Margin: {info.margin:.2f}")
                self.lbl_free_margin.setText(f"Free: {info.margin_free:.2f}")
                profit = info.profit
                self.lbl_profit.setText(f"P/L: {profit:.2f}")
                if profit >= 0:
                    self.lbl_profit.setStyleSheet(
                        "color: #9ece6a; font-weight: bold; font-size: 13px;"
                    )
                else:
                    self.lbl_profit.setStyleSheet(
                        "color: #f7768e; font-weight: bold; font-size: 13px;"
                    )
        else:
            self.conn_indicator.setStyleSheet(
                "background-color: #f7768e; border-radius: 6px; border: 1px solid rgba(247,118,142,0.3);"
            )
            self.conn_label.setText("Offline")
            self.conn_label.setText("Offline")
            self.conn_label.setStyleSheet(
                "color: #f7768e; font-weight: bold; font-size: 10px;"
            )
            self.lbl_account.setText("Account: ---")
            self.lbl_balance.setText("Balance: ---")
            self.lbl_equity.setText("Equity: ---")
            self.lbl_margin.setText("Margin: ---")
            self.lbl_free_margin.setText("Free: ---")
            self.lbl_profit.setText("P/L: ---")

    def _toggle_chart_mode(self):
        mw = self.window()
        if mw and hasattr(mw, 'chart_widget'):
            chart = mw.chart_widget
            if not hasattr(chart, '_chart_mode'):
                chart._chart_mode = "candle"
            if chart._chart_mode == "rinko":
                chart._chart_mode = "candle"
            elif chart._chart_mode == "candle":
                chart._chart_mode = "line"
            else:
                chart._chart_mode = "candle"
            if chart._chart_mode == "line":
                self.btn_chart_mode.setText("Line")
            else:
                self.btn_chart_mode.setText("Candle")
            self.btn_rinko.setStyleSheet(
                "QPushButton{background:#1e2030;border:1px solid #292e42;border-radius:4px;"
                "color:#565f89;font-size:9px;font-weight:bold;padding:2px}"
                "QPushButton:hover{background:#292e42;border-color:#7aa2f7}"
            )
            if hasattr(chart, '_candle_item') and chart._candle_item:
                chart._candle_item.set_mode(chart._chart_mode)
                chart.load_data()

    def _toggle_rinko_mode(self):
        mw = self.window()
        if mw and hasattr(mw, 'chart_widget'):
            chart = mw.chart_widget
            if not hasattr(chart, '_chart_mode'):
                chart._chart_mode = "candle"
            if chart._chart_mode == "rinko":
                chart._chart_mode = "candle"
                self.btn_rinko.setStyleSheet(
                    "QPushButton{background:#1e2030;border:1px solid #292e42;border-radius:4px;"
                    "color:#565f89;font-size:9px;font-weight:bold;padding:2px}"
                    "QPushButton:hover{background:#292e42;border-color:#7aa2f7}"
                )
                self.btn_chart_mode.setText("Candle")
            else:
                chart._chart_mode = "rinko"
                self.btn_rinko.setStyleSheet(
                    "QPushButton{background:#44475a;border:1px solid #7aa2f7;border-radius:4px;"
                    "color:#7aa2f7;font-size:9px;font-weight:bold;padding:2px}"
                )
                self.btn_chart_mode.setText("Candle")
            if hasattr(chart, '_candle_item') and chart._candle_item:
                chart._candle_item.set_mode(chart._chart_mode)
                chart.load_data()

# ============================================================
#              StratifyTrade OB Settings Dialog
# ============================================================

# ============================================================
#              Ichimoku Cloud Settings Dialog
# ============================================================

class IchimokuSettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ichimoku Cloud Settings")
        self.setMinimumWidth(320)
        self.setMinimumHeight(400)
        self.setMaximumHeight(600)
        self.setStyleSheet("QDialog{background:#0a0a1a;color:#c0caf5} QLabel{color:#c0caf5;font-size:10px} QSpinBox,QDoubleSpinBox,QComboBox{background:#1a1b26;color:#c0caf5;border:1px solid #292e42;border-radius:4px;font-size:10px;padding:2px 4px} QCheckBox{color:#c0caf5;font-size:10px} QPushButton{background:#1a1b26;color:#7aa2f7;border:1px solid #292e42;border-radius:4px;padding:4px 12px;font-size:10px} QPushButton:hover{background:#292e42}")
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(6)
        main_layout.setContentsMargins(0, 0, 0, 0)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea{background:#0a0a1a;border:none}")
        content = QtWidgets.QWidget()
        content.setStyleSheet("background:#0a0a1a")
        layout = QVBoxLayout(content)
        layout.setSpacing(6)
        sp = parent if isinstance(parent, StrategyPanel) else None
        cfg = sp.ichimoku_cfg if sp else {}

        g = QGroupBox("Parameters")
        g.setStyleSheet("QGroupBox{color:#7aa2f7;font-weight:bold;border:1px solid #292e42;border-radius:6px;margin-top:6px;padding-top:8px} QGroupBox::title{subcontrol-origin:margin;left:6px;padding:0 3px}")
        gl = QGridLayout(g); gl.setSpacing(4)

        gl.addWidget(QLabel("Conversion (Tenkan):"), 0, 0)
        self.conversion = QtWidgets.QSpinBox(); self.conversion.setRange(1, 200)
        self.conversion.setValue(cfg.get("ichimoku_conversion", 9)); self.conversion.setFixedWidth(50)
        gl.addWidget(self.conversion, 0, 1)

        gl.addWidget(QLabel("Base (Kijun):"), 1, 0)
        self.base = QtWidgets.QSpinBox(); self.base.setRange(1, 200)
        self.base.setValue(cfg.get("ichimoku_base", 26)); self.base.setFixedWidth(50)
        gl.addWidget(self.base, 1, 1)

        gl.addWidget(QLabel("Span 2 Periods:"), 2, 0)
        self.span2 = QtWidgets.QSpinBox(); self.span2.setRange(1, 200)
        self.span2.setValue(cfg.get("ichimoku_span2", 52)); self.span2.setFixedWidth(50)
        gl.addWidget(self.span2, 2, 1)

        gl.addWidget(QLabel("Displacement:"), 3, 0)
        self.displacement = QtWidgets.QSpinBox(); self.displacement.setRange(1, 200)
        self.displacement.setValue(cfg.get("ichimoku_displacement", 26)); self.displacement.setFixedWidth(50)
        gl.addWidget(self.displacement, 3, 1)

        self.show_lagging = QCheckBox("Show Lagging Span")
        self.show_lagging.setChecked(cfg.get("ichimoku_show_lag", True))
        gl.addWidget(self.show_lagging, 4, 0, 1, 2)

        self.show_conversion = QCheckBox("Show Conversion (Tenkan)")
        self.show_conversion.setChecked(cfg.get("ichimoku_show_conversion", True))
        gl.addWidget(self.show_conversion, 7, 0, 1, 2)

        self.show_base = QCheckBox("Show Base (Kijun)")
        self.show_base.setChecked(cfg.get("ichimoku_show_base", True))
        gl.addWidget(self.show_base, 8, 0, 1, 2)

        self.show_lead1 = QCheckBox("Show Lead 1 (Senkou A)")
        self.show_lead1.setChecked(cfg.get("ichimoku_show_lead1", True))
        gl.addWidget(self.show_lead1, 9, 0, 1, 2)

        self.show_lead2 = QCheckBox("Show Lead 2 (Senkou B)")
        self.show_lead2.setChecked(cfg.get("ichimoku_show_lead2", True))
        gl.addWidget(self.show_lead2, 10, 0, 1, 2)

        self.show_cloud = QCheckBox("Show Cloud")
        self.show_cloud.setChecked(cfg.get("ichimoku_show_cloud", True))
        gl.addWidget(self.show_cloud, 11, 0, 1, 2)

        self.show_lead52 = QCheckBox("Show Lead 52")
        self.show_lead52.setChecked(cfg.get("ichimoku_show_lead52", True))
        gl.addWidget(self.show_lead52, 12, 0, 1, 2)

        gl.addWidget(QLabel("Lead 52 Period:"), 13, 0)
        self.lead52_periods = QtWidgets.QSpinBox(); self.lead52_periods.setRange(1, 500)
        self.lead52_periods.setValue(cfg.get("ichimoku_lead52_periods", 52)); self.lead52_periods.setFixedWidth(60)
        gl.addWidget(self.lead52_periods, 13, 1)

        self.check_base_flat = QCheckBox("Check Base Not Flat")
        self.check_base_flat.setChecked(cfg.get("ichimoku_check_base_flat", False))
        gl.addWidget(self.check_base_flat, 5, 0, 1, 2)

        gl.addWidget(QLabel("Crossover Lookback:"), 6, 0)
        self.validity = QtWidgets.QSpinBox(); self.validity.setRange(3, 500)
        self.validity.setValue(cfg.get("ichimoku_validity", 200)); self.validity.setFixedWidth(50)
        gl.addWidget(self.validity, 6, 1)

        layout.addWidget(g)

        gc = QGroupBox("Colors")
        gc.setStyleSheet("QGroupBox{color:#e0af68;font-weight:bold;border:1px solid #292e42;border-radius:6px;margin-top:6px;padding-top:8px} QGroupBox::title{subcontrol-origin:margin;left:6px;padding:0 3px}")
        gcl = QGridLayout(gc); gcl.setSpacing(4)

        gcl.addWidget(QLabel("Conversion:"), 0, 0)
        self.conv_color = QtWidgets.QLineEdit(cfg.get("ichimoku_conv_color", "#2962FF"))
        self.conv_color.setFixedWidth(70); self.conv_color.setStyleSheet("background:#1a1b26;color:#2962FF;border:1px solid #292e42;border-radius:4px")
        gcl.addWidget(self.conv_color, 0, 1)

        gcl.addWidget(QLabel("Base:"), 0, 2)
        self.base_color = QtWidgets.QLineEdit(cfg.get("ichimoku_base_color", "#B71C1C"))
        self.base_color.setFixedWidth(70); self.base_color.setStyleSheet("background:#1a1b26;color:#B71C1C;border:1px solid #292e42;border-radius:4px")
        gcl.addWidget(self.base_color, 0, 3)

        gcl.addWidget(QLabel("Lagging:"), 1, 0)
        self.lag_color = QtWidgets.QLineEdit(cfg.get("ichimoku_lag_color", "#43A047"))
        self.lag_color.setFixedWidth(70); self.lag_color.setStyleSheet("background:#1a1b26;color:#43A047;border:1px solid #292e42;border-radius:4px")
        gcl.addWidget(self.lag_color, 1, 1)

        gcl.addWidget(QLabel("Lead 1:"), 1, 2)
        self.lead1_color = QtWidgets.QLineEdit(cfg.get("ichimoku_lead1_color", "#A5D6A7"))
        self.lead1_color.setFixedWidth(70); self.lead1_color.setStyleSheet("background:#1a1b26;color:#A5D6A7;border:1px solid #292e42;border-radius:4px")
        gcl.addWidget(self.lead1_color, 1, 3)

        gcl.addWidget(QLabel("Lead 2:"), 2, 0)
        self.lead2_color = QtWidgets.QLineEdit(cfg.get("ichimoku_lead2_color", "#EF9A9A"))
        self.lead2_color.setFixedWidth(70); self.lead2_color.setStyleSheet("background:#1a1b26;color:#EF9A9A;border:1px solid #292e42;border-radius:4px")
        gcl.addWidget(self.lead2_color, 2, 1)

        gcl.addWidget(QLabel("Lead 52:"), 2, 2)
        self.lead52_color = QtWidgets.QLineEdit(cfg.get("ichimoku_lead52_color", "#FFD700"))
        self.lead52_color.setFixedWidth(70); self.lead52_color.setStyleSheet("background:#1a1b26;color:#FFD700;border:1px solid #292e42;border-radius:4px")
        gcl.addWidget(self.lead52_color, 2, 3)

        layout.addWidget(gc)

        ga = QGroupBox("Cloud Alpha")
        ga.setStyleSheet("QGroupBox{color:#bb9af7;font-weight:bold;border:1px solid #292e42;border-radius:6px;margin-top:6px;padding-top:8px} QGroupBox::title{subcontrol-origin:margin;left:6px;padding:0 3px}")
        gal = QGridLayout(ga); gal.setSpacing(4)

        gal.addWidget(QLabel("Bull Cloud:"), 0, 0)
        self.bull_alpha = QtWidgets.QSpinBox(); self.bull_alpha.setRange(0, 100)
        self.bull_alpha.setValue(cfg.get("ichimoku_bull_alpha", 90)); self.bull_alpha.setFixedWidth(50)
        gal.addWidget(self.bull_alpha, 0, 1)

        gal.addWidget(QLabel("Bear Cloud:"), 0, 2)
        self.bear_alpha = QtWidgets.QSpinBox(); self.bear_alpha.setRange(0, 100)
        self.bear_alpha.setValue(cfg.get("ichimoku_bear_alpha", 90)); self.bear_alpha.setFixedWidth(50)
        gal.addWidget(self.bear_alpha, 0, 3)

        layout.addWidget(ga)

        gw = QGroupBox("Line Widths")
        gw.setStyleSheet("QGroupBox{color:#e0af68;font-weight:bold;border:1px solid #292e42;border-radius:6px;margin-top:6px;padding-top:8px} QGroupBox::title{subcontrol-origin:margin;left:6px;padding:0 3px}")
        gwl = QGridLayout(gw); gwl.setSpacing(4)

        gwl.addWidget(QLabel("Conversion:"), 0, 0)
        self.conv_width = QtWidgets.QDoubleSpinBox(); self.conv_width.setRange(0.5, 5.0); self.conv_width.setSingleStep(0.5)
        self.conv_width.setValue(cfg.get("ichimoku_conv_width", 1.5)); self.conv_width.setFixedWidth(60)
        gwl.addWidget(self.conv_width, 0, 1)

        gwl.addWidget(QLabel("Base:"), 0, 2)
        self.base_width = QtWidgets.QDoubleSpinBox(); self.base_width.setRange(0.5, 5.0); self.base_width.setSingleStep(0.5)
        self.base_width.setValue(cfg.get("ichimoku_base_width", 1.5)); self.base_width.setFixedWidth(60)
        gwl.addWidget(self.base_width, 0, 3)

        gwl.addWidget(QLabel("Lagging:"), 1, 0)
        self.lag_width = QtWidgets.QDoubleSpinBox(); self.lag_width.setRange(0.5, 5.0); self.lag_width.setSingleStep(0.5)
        self.lag_width.setValue(cfg.get("ichimoku_lag_width", 1.0)); self.lag_width.setFixedWidth(60)
        gwl.addWidget(self.lag_width, 1, 1)

        gwl.addWidget(QLabel("Lead 1:"), 1, 2)
        self.lead1_width = QtWidgets.QDoubleSpinBox(); self.lead1_width.setRange(0.5, 5.0); self.lead1_width.setSingleStep(0.5)
        self.lead1_width.setValue(cfg.get("ichimoku_lead1_width", 1.0)); self.lead1_width.setFixedWidth(60)
        gwl.addWidget(self.lead1_width, 1, 3)

        gwl.addWidget(QLabel("Lead 2:"), 2, 0)
        self.lead2_width = QtWidgets.QDoubleSpinBox(); self.lead2_width.setRange(0.5, 5.0); self.lead2_width.setSingleStep(0.5)
        self.lead2_width.setValue(cfg.get("ichimoku_lead2_width", 1.0)); self.lead2_width.setFixedWidth(60)
        gwl.addWidget(self.lead2_width, 2, 1)

        gwl.addWidget(QLabel("Lead 52:"), 2, 2)
        self.lead52_width = QtWidgets.QDoubleSpinBox(); self.lead52_width.setRange(0.5, 5.0); self.lead52_width.setSingleStep(0.5)
        self.lead52_width.setValue(cfg.get("ichimoku_lead52_width", 1.5)); self.lead52_width.setFixedWidth(60)
        gwl.addWidget(self.lead52_width, 2, 3)

        layout.addWidget(gw)

        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.accept)
        btn_layout.addWidget(btn_ok)
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    def get_settings(self):
        return {
            "ichimoku_conversion": self.conversion.value(),
            "ichimoku_base": self.base.value(),
            "ichimoku_span2": self.span2.value(),
            "ichimoku_displacement": self.displacement.value(),
            "ichimoku_show_lag": self.show_lagging.isChecked(),
            "ichimoku_show_conversion": self.show_conversion.isChecked(),
            "ichimoku_show_base": self.show_base.isChecked(),
            "ichimoku_show_lead1": self.show_lead1.isChecked(),
            "ichimoku_show_lead2": self.show_lead2.isChecked(),
            "ichimoku_show_cloud": self.show_cloud.isChecked(),
            "ichimoku_conv_color": self.conv_color.text(),
            "ichimoku_base_color": self.base_color.text(),
            "ichimoku_lag_color": self.lag_color.text(),
            "ichimoku_lead1_color": self.lead1_color.text(),
            "ichimoku_lead2_color": self.lead2_color.text(),
            "ichimoku_bull_alpha": self.bull_alpha.value(),
            "ichimoku_bear_alpha": self.bear_alpha.value(),
            "ichimoku_check_base_flat": self.check_base_flat.isChecked(),
            "ichimoku_validity": self.validity.value(),
            "ichimoku_show_lead52": self.show_lead52.isChecked(),
            "ichimoku_lead52_periods": self.lead52_periods.value(),
            "ichimoku_lead52_color": self.lead52_color.text(),
            "ichimoku_conv_width": self.conv_width.value(),
            "ichimoku_base_width": self.base_width.value(),
            "ichimoku_lag_width": self.lag_width.value(),
            "ichimoku_lead1_width": self.lead1_width.value(),
            "ichimoku_lead2_width": self.lead2_width.value(),
            "ichimoku_lead52_width": self.lead52_width.value(),
        }

# ============================================================
#           Range Filter Settings Dialog
# ============================================================

# ============================================================
#                   Setup Prep Pass Settings Dialog
# ============================================================

class MASettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Moving Average Settings")
        self.setMinimumWidth(300)
        self.setStyleSheet("""
            QDialog{background:#0a0a1a;color:#c0caf5}
            QGroupBox{color:#7aa2f7;font-weight:bold;border:1px solid #292e42;border-radius:6px;margin-top:6px;padding-top:8px}
            QGroupBox::title{subcontrol-origin:margin;left:6px;padding:0 3px}
            QLabel{color:#c0caf5;font-size:10px}
            QSpinBox,QDoubleSpinBox,QComboBox{background:#1a1b26;color:#c0caf5;border:1px solid #292e42;border-radius:4px;font-size:10px;padding:2px 4px}
            QLineEdit{background:#1a1b26;color:#c0caf5;border:1px solid #292e42;border-radius:4px;padding:2px 6px;font-size:10px}
            QPushButton{background:#1a1b26;color:#7aa2f7;border:1px solid #292e42;border-radius:4px;padding:4px 12px;font-size:10px}
            QPushButton:hover{background:#292e42}
        """)
        layout = QVBoxLayout(self)
        sp = parent if isinstance(parent, StrategyPanel) else None
        cfg = sp.ma_cfg if sp else {}

        g = QGroupBox("Parameters")
        gl = QGridLayout(g); gl.setSpacing(4)

        gl.addWidget(QLabel("Period:"), 0, 0)
        self.ma_period = QtWidgets.QSpinBox()
        self.ma_period.setRange(1, 500)
        self.ma_period.setValue(cfg.get("ma_period", 20))
        self.ma_period.setFixedWidth(60)
        gl.addWidget(self.ma_period, 0, 1)

        gl.addWidget(QLabel("Type:"), 1, 0)
        self.ma_type = QtWidgets.QComboBox()
        self.ma_type.addItems(["SMA", "EMA"])
        saved_type = cfg.get("ma_type", "SMA")
        idx = self.ma_type.findText(saved_type)
        if idx >= 0:
            self.ma_type.setCurrentIndex(idx)
        self.ma_type.setFixedWidth(70)
        gl.addWidget(self.ma_type, 1, 1)

        gl.addWidget(QLabel("Shift:"), 2, 0)
        self.ma_shift = QtWidgets.QSpinBox()
        self.ma_shift.setRange(-100, 100)
        self.ma_shift.setValue(cfg.get("ma_shift", 0))
        self.ma_shift.setFixedWidth(60)
        gl.addWidget(self.ma_shift, 2, 1)

        gl.addWidget(QLabel("Line Width:"), 3, 0)
        self.ma_width = QtWidgets.QDoubleSpinBox()
        self.ma_width.setRange(0.5, 10.0)
        self.ma_width.setSingleStep(0.5)
        self.ma_width.setValue(cfg.get("ma_width", 1.5))
        self.ma_width.setFixedWidth(60)
        gl.addWidget(self.ma_width, 3, 1)

        layout.addWidget(g)

        gc = QGroupBox("Color")
        gcl = QGridLayout(gc); gcl.setSpacing(4)
        gcl.addWidget(QLabel("Line Color:"), 0, 0)
        self.ma_color = QtWidgets.QLineEdit(cfg.get("ma_color", "#e0af68"))
        self.ma_color.setFixedWidth(80)
        self.ma_color.setStyleSheet("background:#1a1b26;color:#e0af68;border:1px solid #292e42;border-radius:4px")
        gcl.addWidget(self.ma_color, 0, 1)
        layout.addWidget(gc)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        btn_row.addWidget(ok_btn)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        layout.addLayout(btn_row)

    def get_settings(self):
        return {
            "ma_period": self.ma_period.value(),
            "ma_type": self.ma_type.currentText(),
            "ma_shift": self.ma_shift.value(),
            "ma_width": self.ma_width.value(),
            "ma_color": self.ma_color.text(),
        }


# ============================================================
#                   Session Break Settings Dialog
# ============================================================


class MultiScanSettingsDialog(QtWidgets.QDialog):
    def __init__(self, cfg=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Multi-Symbol Scan Settings")
        self.setFixedSize(380, 480)
        self.setStyleSheet("""
            QDialog{background:#0a0a1a}
            QLabel{color:#c0caf5;font-size:11px}
            QCheckBox{color:#c0caf5;font-size:11px;font-weight:bold}
            QCheckBox::indicator{width:16px;height:16px}
            QSpinBox{background:#1a1b26;color:#c0caf5;border:1px solid #292e42;border-radius:4px;padding:4px;font-size:11px}
            QPushButton{background:#292e42;color:#7aa2f7;border:1px solid #33467c;border-radius:6px;padding:6px 16px;font-size:11px;font-weight:bold}
            QPushButton:hover{background:#33467c}
        """)
        self._cfg = cfg or {}
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        title = QLabel("Multi-Symbol Scan Settings")
        title.setStyleSheet("color:#bb9af7;font-size:14px;font-weight:bold")
        layout.addWidget(title)

        layout.addWidget(self._separator())

        lbl = QLabel("Scan Interval:")
        layout.addWidget(lbl)
        self.spin_interval = QtWidgets.QSpinBox()
        self.spin_interval.setRange(1, 60)
        self.spin_interval.setValue(self._cfg.get("scan_interval", 5))
        self.spin_interval.setSuffix(" sec")
        self.spin_interval.setFixedWidth(90)
        layout.addWidget(self.spin_interval)

        layout.addWidget(self._separator())

        lbl2 = QLabel("Signal Levels (zone source):")
        lbl2.setStyleSheet("color:#bb9af7;font-size:11px;font-weight:bold")
        layout.addWidget(lbl2)
        lbl2_desc = QLabel("Check which levels to detect signals on:")
        lbl2_desc.setStyleSheet("color:#565f89;font-size:9px;font-style:italic")
        layout.addWidget(lbl2_desc)

        signal_tfs = self._cfg.get("signal_tfs", {"Weekly": True, "Daily": True, "H4": True, "H1": True})
        self.tf_checks = {}
        for tf_name in ["Weekly", "Daily", "H4", "H1"]:
            cb = QCheckBox(tf_name)
            cb.setChecked(signal_tfs.get(tf_name, True))
            cb.setStyleSheet("color:#c0caf5;font-size:11px;font-weight:bold")
            layout.addWidget(cb)
            self.tf_checks[tf_name] = cb

        layout.addWidget(self._separator())

        lbl3 = QLabel("Chart Timeframes to Scan:")
        lbl3.setStyleSheet("color:#bb9af7;font-size:11px;font-weight:bold")
        layout.addWidget(lbl3)
        lbl3_desc = QLabel("Last candle checked on these TFs for each symbol:")
        lbl3_desc.setStyleSheet("color:#565f89;font-size:9px;font-style:italic")
        layout.addWidget(lbl3_desc)

        chart_tfs = self._cfg.get("chart_tfs", {"M15": True, "M30": True, "H1": True, "H4": True, "D1": True})
        self.chart_tf_checks = {}
        chart_tf_grid = QtWidgets.QGridLayout()
        chart_tf_grid.setSpacing(4)
        all_chart_tfs = ["M1", "M3", "M5", "M10", "M15", "M30"]
        for idx, tf_name in enumerate(all_chart_tfs):
            cb = QCheckBox(tf_name)
            cb.setChecked(chart_tfs.get(tf_name, False))
            cb.setStyleSheet("color:#c0caf5;font-size:10px")
            row = idx // 3
            col = idx % 3
            chart_tf_grid.addWidget(cb, row, col)
            self.chart_tf_checks[tf_name] = cb
        layout.addLayout(chart_tf_grid)

        layout.addWidget(self._separator())

        self.popup_cb = QCheckBox("Show Popup Notification")
        self.popup_cb.setChecked(self._cfg.get("popup_notify", True))
        self.popup_cb.setStyleSheet("color:#7aa2f7;font-size:12px;font-weight:bold")
        layout.addWidget(self.popup_cb)

        self.sound_cb = QCheckBox("Sound Alarm")
        self.sound_cb.setChecked(self._cfg.get("sound_alarm", True))
        self.sound_cb.setStyleSheet("color:#e0af68;font-size:12px;font-weight:bold")
        layout.addWidget(self.sound_cb)

        layout.addStretch()

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        btn_row.addWidget(btn_cancel)
        btn_save = QPushButton("Save")
        btn_save.setStyleSheet("QPushButton{background:#26a641;color:#ffffff;border-color:#26a641} QPushButton:hover{background:#2b8a3a}")
        btn_save.clicked.connect(self.accept)
        btn_row.addWidget(btn_save)
        layout.addLayout(btn_row)

    def _separator(self):
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setStyleSheet("color:#292e42")
        return line

    def get_settings(self):
        return {
            "scan_interval": self.spin_interval.value(),
            "signal_tfs": {tf: cb.isChecked() for tf, cb in self.tf_checks.items()},
            "chart_tfs": {tf: cb.isChecked() for tf, cb in self.chart_tf_checks.items()},
            "popup_notify": self.popup_cb.isChecked(),
            "sound_alarm": self.sound_cb.isChecked(),
        }


class AlgomanSettingsDialog(QtWidgets.QDialog):
    def __init__(self, cfg=None, parent=None):
        super().__init__(parent)
        if cfg is None:
            cfg = {}
        self.setWindowTitle("AlgoMan Settings")
        self.setMinimumWidth(500)
        self.setMinimumHeight(650)
        self.setStyleSheet("QDialog{background:#1a1b26} QLabel{color:#c0caf5;font-size:11px} QCheckBox{color:#c0caf5;font-size:11px} QComboBox{background:#24283b;color:#c0caf5;border:1px solid #292e42;border-radius:3px;padding:3px} QSpinBox,QDoubleSpinBox{background:#24283b;color:#c0caf5;border:1px solid #292e42;border-radius:3px;padding:3px} QPushButton{background:#292e42;color:#7aa2f7;border:1px solid #33467c;border-radius:4px;padding:5px 12px;font-weight:bold} QPushButton:hover{background:#33467c}")

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(scroll_widget)
        layout.setSpacing(6)

        # DASHBOARD SETTINGS
        g1 = QtWidgets.QGroupBox("Dashboard Settings")
        g1.setStyleSheet("QGroupBox{color:#7aa2f7;font-weight:bold;border:1px solid #292e42;border-radius:5px;margin-top:5px} QGroupBox::title{subcontrol-origin:margin;left:8px;padding:0 4px}")
        g1l = QtWidgets.QGridLayout(g1)
        self.enableDashboard = QtWidgets.QCheckBox("Enable Dashboard")
        self.enableDashboard.setChecked(cfg.get("enableDashboard", True))
        g1l.addWidget(self.enableDashboard, 0, 0)
        g1l.addWidget(QtWidgets.QLabel("Location"), 1, 0)
        self.locationDashboard = QtWidgets.QComboBox()
        self.locationDashboard.addItems(["Top right", "Top left", "Middle right", "Middle left", "Bottom right", "Bottom left"])
        self.locationDashboard.setCurrentText(cfg.get("locationDashboard", "Middle right"))
        g1l.addWidget(self.locationDashboard, 1, 1)
        g1l.addWidget(QtWidgets.QLabel("Size"), 2, 0)
        self.sizeDashboard = QtWidgets.QComboBox()
        self.sizeDashboard.addItems(["Tiny", "Small", "Normal"])
        self.sizeDashboard.setCurrentText(cfg.get("sizeDashboard", "Tiny"))
        g1l.addWidget(self.sizeDashboard, 2, 1)
        layout.addWidget(g1)

        # BUY AND SELL SIGNALS SETTINGS
        g2 = QtWidgets.QGroupBox("Buy and Sell Signals")
        g2.setStyleSheet(g1.styleSheet())
        g2l = QtWidgets.QGridLayout(g2)
        self.showSignals = QtWidgets.QCheckBox("Show Signals")
        self.showSignals.setChecked(cfg.get("showSignals", True))
        g2l.addWidget(self.showSignals, 0, 0, 1, 2)
        g2l.addWidget(QtWidgets.QLabel("Strategy"), 1, 0)
        self.strategy = QtWidgets.QComboBox()
        self.strategy.addItems(["Normal", "Confirmed", "Trend scalper"])
        self.strategy.setCurrentText(cfg.get("strategy", "Normal"))
        g2l.addWidget(self.strategy, 1, 1)
        g2l.addWidget(QtWidgets.QLabel("Sensitivity"), 2, 0)
        self.sensitivity = QtWidgets.QDoubleSpinBox()
        self.sensitivity.setRange(0.1, 10.0)
        self.sensitivity.setSingleStep(0.1)
        self.sensitivity.setValue(cfg.get("sensitivity", 1.8))
        g2l.addWidget(self.sensitivity, 2, 1)
        self.consSignalsFilter = QtWidgets.QCheckBox("Consolidation signals filter")
        self.consSignalsFilter.setChecked(cfg.get("consSignalsFilter", False))
        g2l.addWidget(self.consSignalsFilter, 3, 0, 1, 2)
        self.smartSignalsOnly = QtWidgets.QCheckBox("Smart signals only")
        self.smartSignalsOnly.setChecked(cfg.get("smartSignalsOnly", False))
        g2l.addWidget(self.smartSignalsOnly, 4, 0, 1, 2)
        self.candleColors = QtWidgets.QCheckBox("Candle colors")
        self.candleColors.setChecked(cfg.get("candleColors", False))
        g2l.addWidget(self.candleColors, 5, 0, 1, 2)
        self.momentumCandles = QtWidgets.QCheckBox("Momentum candles")
        self.momentumCandles.setChecked(cfg.get("momentumCandles", False))
        g2l.addWidget(self.momentumCandles, 6, 0, 1, 2)
        self.highVolSignals = QtWidgets.QCheckBox("High volume signals only")
        self.highVolSignals.setChecked(cfg.get("highVolSignals", False))
        g2l.addWidget(self.highVolSignals, 7, 0, 1, 2)
        layout.addWidget(g2)

        # RISK MANAGEMENT
        g3 = QtWidgets.QGroupBox("Risk Management")
        g3.setStyleSheet(g1.styleSheet())
        g3l = QtWidgets.QGridLayout(g3)
        self.enableTrailingSL = QtWidgets.QCheckBox("Enable Trailing Stop-Loss")
        self.enableTrailingSL.setChecked(cfg.get("enableTrailingSL", False))
        g3l.addWidget(self.enableTrailingSL, 0, 0, 1, 2)
        self.usePercSL = QtWidgets.QCheckBox("% Trailing SL")
        self.usePercSL.setChecked(cfg.get("usePercSL", False))
        g3l.addWidget(self.usePercSL, 1, 0)
        self.percTrailingSL = QtWidgets.QDoubleSpinBox()
        self.percTrailingSL.setRange(0.0, 100.0)
        self.percTrailingSL.setSingleStep(0.1)
        self.percTrailingSL.setValue(cfg.get("percTrailingSL", 1.0))
        g3l.addWidget(self.percTrailingSL, 1, 1)
        self.enableSwings = QtWidgets.QCheckBox("Enable Swing High/Low")
        self.enableSwings.setChecked(cfg.get("enableSwings", False))
        g3l.addWidget(self.enableSwings, 2, 0)
        self.periodSwings = QtWidgets.QSpinBox()
        self.periodSwings.setRange(2, 50)
        self.periodSwings.setValue(cfg.get("periodSwings", 10))
        g3l.addWidget(self.periodSwings, 2, 1)
        self.enableTpSlAreas = QtWidgets.QCheckBox("Enable TP/SL Areas")
        self.enableTpSlAreas.setChecked(cfg.get("enableTpSlAreas", False))
        g3l.addWidget(self.enableTpSlAreas, 3, 0, 1, 2)
        g3l.addWidget(QtWidgets.QLabel("TP 1 Multi"), 4, 0)
        self.multTP1 = QtWidgets.QDoubleSpinBox()
        self.multTP1.setRange(0.0, 20.0)
        self.multTP1.setSingleStep(0.5)
        self.multTP1.setValue(cfg.get("multTP1", 1.0))
        g3l.addWidget(self.multTP1, 4, 1)
        g3l.addWidget(QtWidgets.QLabel("TP 2 Multi"), 5, 0)
        self.multTP2 = QtWidgets.QDoubleSpinBox()
        self.multTP2.setRange(0.0, 20.0)
        self.multTP2.setSingleStep(0.5)
        self.multTP2.setValue(cfg.get("multTP2", 2.0))
        g3l.addWidget(self.multTP2, 5, 1)
        g3l.addWidget(QtWidgets.QLabel("TP 3 Multi"), 6, 0)
        self.multTP3 = QtWidgets.QDoubleSpinBox()
        self.multTP3.setRange(0.0, 20.0)
        self.multTP3.setSingleStep(0.5)
        self.multTP3.setValue(cfg.get("multTP3", 3.0))
        g3l.addWidget(self.multTP3, 6, 1)
        self.tpLabels = QtWidgets.QCheckBox("TP Labels")
        self.tpLabels.setChecked(cfg.get("tpLabels", True))
        g3l.addWidget(self.tpLabels, 7, 0, 1, 2)
        layout.addWidget(g3)

        # TREND CLOUD
        g4 = QtWidgets.QGroupBox("Trend Cloud")
        g4.setStyleSheet(g1.styleSheet())
        g4l = QtWidgets.QGridLayout(g4)
        self.showTrendCloud = QtWidgets.QCheckBox("Show Trend Cloud")
        self.showTrendCloud.setChecked(cfg.get("showTrendCloud", True))
        g4l.addWidget(self.showTrendCloud, 0, 0, 1, 2)
        g4l.addWidget(QtWidgets.QLabel("Period"), 1, 0)
        self.periodTrendCloud = QtWidgets.QComboBox()
        self.periodTrendCloud.addItems(["Short term", "Long term", "New"])
        self.periodTrendCloud.setCurrentText(cfg.get("periodTrendCloud", "New"))
        g4l.addWidget(self.periodTrendCloud, 1, 1)
        self.signalsTrendCloud = QtWidgets.QCheckBox("Trend only signals")
        self.signalsTrendCloud.setChecked(cfg.get("signalsTrendCloud", False))
        g4l.addWidget(self.signalsTrendCloud, 2, 0, 1, 2)
        self.fastTrendCloud = QtWidgets.QCheckBox("Fast trend cloud")
        self.fastTrendCloud.setChecked(cfg.get("fastTrendCloud", False))
        g4l.addWidget(self.fastTrendCloud, 3, 0)
        self.fastTrendCloudLen = QtWidgets.QSpinBox()
        self.fastTrendCloudLen.setRange(2, 200)
        self.fastTrendCloudLen.setValue(cfg.get("fastTrendCloudLen", 55))
        g4l.addWidget(self.fastTrendCloudLen, 3, 1)
        layout.addWidget(g4)

        # AUTO TRENDLINES
        g5 = QtWidgets.QGroupBox("Auto Trendlines")
        g5.setStyleSheet(g1.styleSheet())
        g5l = QtWidgets.QGridLayout(g5)
        self.enableAutoTrend = QtWidgets.QCheckBox("Enable Auto Trendlines")
        self.enableAutoTrend.setChecked(cfg.get("enableAutoTrend", False))
        g5l.addWidget(self.enableAutoTrend, 0, 0, 1, 2)
        g5l.addWidget(QtWidgets.QLabel("Loopback"), 1, 0)
        self.lenTrendChannel = QtWidgets.QSpinBox()
        self.lenTrendChannel.setRange(10, 500)
        self.lenTrendChannel.setValue(cfg.get("lenTrendChannel", 200))
        g5l.addWidget(self.lenTrendChannel, 1, 1)
        layout.addWidget(g5)

        # AUTO SUPPORT AND RESISTANCE
        g6 = QtWidgets.QGroupBox("Support and Resistance")
        g6.setStyleSheet(g1.styleSheet())
        g6l = QtWidgets.QGridLayout(g6)
        self.enableSR = QtWidgets.QCheckBox("Enable S/R")
        self.enableSR.setChecked(cfg.get("enableSR", False))
        g6l.addWidget(self.enableSR, 0, 0, 1, 2)
        g6l.addWidget(QtWidgets.QLabel("Line Style"), 1, 0)
        self.lineSrStyle = QtWidgets.QComboBox()
        self.lineSrStyle.addItems(["Solid", "Dotted", "Dashed"])
        self.lineSrStyle.setCurrentText(cfg.get("lineSrStyle", "Dashed"))
        g6l.addWidget(self.lineSrStyle, 1, 1)
        g6l.addWidget(QtWidgets.QLabel("Line Width"), 2, 0)
        self.lineSrWidth = QtWidgets.QSpinBox()
        self.lineSrWidth.setRange(1, 4)
        self.lineSrWidth.setValue(cfg.get("lineSrWidth", 2))
        g6l.addWidget(self.lineSrWidth, 2, 1)
        layout.addWidget(g6)

        # CONSOLIDATION ZONES
        g7 = QtWidgets.QGroupBox("Consolidation Zones")
        g7.setStyleSheet(g1.styleSheet())
        g7l = QtWidgets.QGridLayout(g7)
        self.showCons = QtWidgets.QCheckBox("Show Consolidation")
        self.showCons.setChecked(cfg.get("showCons", False))
        g7l.addWidget(self.showCons, 0, 0, 1, 2)
        g7l.addWidget(QtWidgets.QLabel("Loopback"), 1, 0)
        self.lbPeriod = QtWidgets.QSpinBox()
        self.lbPeriod.setRange(2, 50)
        self.lbPeriod.setValue(cfg.get("lbPeriod", 10))
        g7l.addWidget(self.lbPeriod, 1, 1)
        g7l.addWidget(QtWidgets.QLabel("Min Length"), 2, 0)
        self.lenCons = QtWidgets.QSpinBox()
        self.lenCons.setRange(2, 20)
        self.lenCons.setValue(cfg.get("lenCons", 5))
        g7l.addWidget(self.lenCons, 2, 1)
        self.paintCons = QtWidgets.QCheckBox("Paint Area")
        self.paintCons.setChecked(cfg.get("paintCons", True))
        g7l.addWidget(self.paintCons, 3, 0, 1, 2)
        layout.addWidget(g7)

        # ORDER BLOCK
        g8 = QtWidgets.QGroupBox("Order Block")
        g8.setStyleSheet(g1.styleSheet())
        g8l = QtWidgets.QGridLayout(g8)
        self.box_ob = QtWidgets.QCheckBox("Enable Order Block")
        self.box_ob.setChecked(cfg.get("box_ob", False))
        g8l.addWidget(self.box_ob, 0, 0, 1, 2)
        self.box_sv = QtWidgets.QCheckBox("Plot demand boxes")
        self.box_sv.setChecked(cfg.get("box_sv", True))
        g8l.addWidget(self.box_sv, 1, 0, 1, 2)
        self.box_hide_gray = QtWidgets.QCheckBox("Hide gray boxes")
        self.box_hide_gray.setChecked(cfg.get("box_hide_gray", False))
        g8l.addWidget(self.box_hide_gray, 2, 0, 1, 2)
        g8l.addWidget(QtWidgets.QLabel("MSB Trigger"), 3, 0)
        self.bos_type = QtWidgets.QComboBox()
        self.bos_type.addItems(["High and Low", "Close and Open"])
        self.bos_type.setCurrentText(cfg.get("bos_type", "High and Low"))
        g8l.addWidget(self.bos_type, 3, 1)
        g8l.addWidget(QtWidgets.QLabel("Test Delay"), 4, 0)
        self.box_test_delay = QtWidgets.QSpinBox()
        self.box_test_delay.setRange(1, 20)
        self.box_test_delay.setValue(cfg.get("box_test_delay", 3))
        g8l.addWidget(self.box_test_delay, 4, 1)
        g8l.addWidget(QtWidgets.QLabel("Fill Delay"), 5, 0)
        self.box_fill_delay = QtWidgets.QSpinBox()
        self.box_fill_delay.setRange(1, 20)
        self.box_fill_delay.setValue(cfg.get("box_fill_delay", 3))
        g8l.addWidget(self.box_fill_delay, 5, 1)
        self.box_test_sv = QtWidgets.QCheckBox("Dim tested boxes")
        self.box_test_sv.setChecked(cfg.get("box_test_sv", True))
        g8l.addWidget(self.box_test_sv, 6, 0, 1, 2)
        self.box_stop_sv = QtWidgets.QCheckBox("Stop plotting filled")
        self.box_stop_sv.setChecked(cfg.get("box_stop_sv", True))
        g8l.addWidget(self.box_stop_sv, 7, 0, 1, 2)
        layout.addWidget(g8)

        # VOLUME PROFILE
        g9 = QtWidgets.QGroupBox("Volume Profile")
        g9.setStyleSheet(g1.styleSheet())
        g9l = QtWidgets.QGridLayout(g9)
        self.algomanVP = QtWidgets.QCheckBox("Enable Volume Profile")
        self.algomanVP.setChecked(cfg.get("algomanVP", False))
        g9l.addWidget(self.algomanVP, 0, 0, 1, 2)
        g9l.addWidget(QtWidgets.QLabel("Offset"), 1, 0)
        self.offset = QtWidgets.QSpinBox()
        self.offset.setRange(2, 20)
        self.offset.setValue(cfg.get("offset", 2))
        g9l.addWidget(self.offset, 1, 1)
        g9l.addWidget(QtWidgets.QLabel("Lookback"), 2, 0)
        self.lookback = QtWidgets.QSpinBox()
        self.lookback.setRange(14, 10000)
        self.lookback.setValue(cfg.get("lookback", 100))
        g9l.addWidget(self.lookback, 2, 1)
        g9l.addWidget(QtWidgets.QLabel("Levels"), 3, 0)
        self.levelNum = QtWidgets.QSpinBox()
        self.levelNum.setRange(10, 1000)
        self.levelNum.setValue(cfg.get("levelNum", 100))
        g9l.addWidget(self.levelNum, 3, 1)
        g9l.addWidget(QtWidgets.QLabel("Level Width"), 4, 0)
        self.levelWidth = QtWidgets.QSpinBox()
        self.levelWidth.setRange(2, 100)
        self.levelWidth.setValue(cfg.get("levelWidth", 50))
        g9l.addWidget(self.levelWidth, 4, 1)
        layout.addWidget(g9)

        layout.addStretch()
        scroll.setWidget(scroll_widget)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(scroll)

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.addStretch()
        ok_btn = QtWidgets.QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        btn_row.addWidget(ok_btn)
        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        main_layout.addLayout(btn_row)

    def get_settings(self):
        return {
            "enableDashboard": self.enableDashboard.isChecked(),
            "locationDashboard": self.locationDashboard.currentText(),
            "sizeDashboard": self.sizeDashboard.currentText(),
            "showSignals": self.showSignals.isChecked(),
            "strategy": self.strategy.currentText(),
            "sensitivity": self.sensitivity.value(),
            "consSignalsFilter": self.consSignalsFilter.isChecked(),
            "smartSignalsOnly": self.smartSignalsOnly.isChecked(),
            "candleColors": self.candleColors.isChecked(),
            "momentumCandles": self.momentumCandles.isChecked(),
            "highVolSignals": self.highVolSignals.isChecked(),
            "enableTrailingSL": self.enableTrailingSL.isChecked(),
            "usePercSL": self.usePercSL.isChecked(),
            "percTrailingSL": self.percTrailingSL.value(),
            "enableSwings": self.enableSwings.isChecked(),
            "periodSwings": self.periodSwings.value(),
            "enableTpSlAreas": self.enableTpSlAreas.isChecked(),
            "multTP1": self.multTP1.value(),
            "multTP2": self.multTP2.value(),
            "multTP3": self.multTP3.value(),
            "tpLabels": self.tpLabels.isChecked(),
            "showTrendCloud": self.showTrendCloud.isChecked(),
            "periodTrendCloud": self.periodTrendCloud.currentText(),
            "signalsTrendCloud": self.signalsTrendCloud.isChecked(),
            "fastTrendCloud": self.fastTrendCloud.isChecked(),
            "fastTrendCloudLen": self.fastTrendCloudLen.value(),
            "enableAutoTrend": self.enableAutoTrend.isChecked(),
            "lenTrendChannel": self.lenTrendChannel.value(),
            "enableSR": self.enableSR.isChecked(),
            "lineSrStyle": self.lineSrStyle.currentText(),
            "lineSrWidth": self.lineSrWidth.value(),
            "showCons": self.showCons.isChecked(),
            "lbPeriod": self.lbPeriod.value(),
            "lenCons": self.lenCons.value(),
            "paintCons": self.paintCons.isChecked(),
            "box_ob": self.box_ob.isChecked(),
            "box_sv": self.box_sv.isChecked(),
            "box_hide_gray": self.box_hide_gray.isChecked(),
            "bos_type": self.bos_type.currentText(),
            "box_test_delay": self.box_test_delay.value(),
            "box_fill_delay": self.box_fill_delay.value(),
            "box_test_sv": self.box_test_sv.isChecked(),
            "box_stop_sv": self.box_stop_sv.isChecked(),
            "algomanVP": self.algomanVP.isChecked(),
            "offset": self.offset.value(),
            "lookback": self.lookback.value(),
            "levelNum": self.levelNum.value(),
            "levelWidth": self.levelWidth.value(),
        }


class SessionBreakSettingsDialog(QtWidgets.QDialog):
    TF_LIST = ["M1", "M5", "M15", "M30", "H1", "H4", "D1"]

    def __init__(self, cfg, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Session Break Settings")
        self.setMinimumWidth(620)
        self.setStyleSheet("""
            QDialog{background:#0a0a1a;color:#c0caf5}
            QLabel{color:#c0caf5;font-size:9px}
            QCheckBox{color:#c0caf5;font-size:9px}
            QPushButton{background:#1a1b26;color:#7aa2f7;border:1px solid #292e42;border-radius:4px;padding:4px 12px;font-size:10px}
            QPushButton:hover{background:#292e42}
            QGroupBox{color:#e0af68;font-weight:bold;border:1px solid #292e42;border-radius:6px;margin-top:6px;padding-top:8px}
            QGroupBox::title{subcontrol-origin:margin;left:6px;padding:0 3px}
            QSpinBox{background:#1a1b26;color:#c0caf5;border:1px solid #292e42;border-radius:4px;font-size:10px;padding:2px}
            QComboBox{background:#1a1b26;color:#c0caf5;border:1px solid #292e42;border-radius:4px;font-size:10px;padding:2px 4px}
            QComboBox::drop-down{border:none}
            QLineEdit{background:#1a1b26;color:#c0caf5;border:1px solid #292e42;border-radius:4px;font-size:10px;padding:2px 4px}
        """)
        self.cfg = cfg
        layout = QVBoxLayout(self)
        layout.setSpacing(6)

        g = QGroupBox("Sessions")
        gl = QGridLayout(g)
        gl.setSpacing(5)
        gl.addWidget(QLabel(""), 0, 0)
        gl.addWidget(QLabel("Start"), 0, 1, QtCore.Qt.AlignCenter)
        gl.addWidget(QLabel(""), 0, 2)
        gl.addWidget(QLabel("End"), 0, 3, QtCore.Qt.AlignCenter)
        gl.addWidget(QLabel(""), 0, 4)
        gl.addWidget(QLabel("Timeframe"), 0, 5, QtCore.Qt.AlignCenter)
        gl.addWidget(QLabel("Color"), 0, 6, QtCore.Qt.AlignCenter)

        saved = cfg.get("sessions", {})
        sessions_def = [
            ("Daily", "#e0af68", 0, 0, 23, 59, "D1"),
            ("Asian", "#565f89", 0, 0, 8, 0, "H1"),
            ("London", "#7aa2f7", 8, 0, 16, 0, "H1"),
            ("New York", "#bb9af7", 13, 0, 21, 0, "H1"),
        ]
        self.session_widgets = {}
        for idx, (name, default_color, d_sh, d_sm, d_eh, d_em, d_tf) in enumerate(sessions_def):
            row = idx + 1
            cb = QCheckBox(name)
            cb.setChecked(saved.get(name, {}).get("enabled", False) if isinstance(saved.get(name), dict) else (name in saved if isinstance(saved.get(name), str) else False))
            gl.addWidget(cb, row, 0)

            sh = QtWidgets.QSpinBox(); sh.setRange(0, 23); sh.setFixedWidth(38)
            sh.setValue(saved.get(name, {}).get("start_h", d_sh) if isinstance(saved.get(name), dict) else d_sh)
            gl.addWidget(sh, row, 1)

            sm = QtWidgets.QSpinBox(); sm.setRange(0, 59); sm.setFixedWidth(38)
            sm.setValue(saved.get(name, {}).get("start_m", d_sm) if isinstance(saved.get(name), dict) else d_sm)
            gl.addWidget(sm, row, 2)

            eh = QtWidgets.QSpinBox(); eh.setRange(0, 23); eh.setFixedWidth(38)
            eh.setValue(saved.get(name, {}).get("end_h", d_eh) if isinstance(saved.get(name), dict) else d_eh)
            gl.addWidget(eh, row, 3)

            em = QtWidgets.QSpinBox(); em.setRange(0, 59); em.setFixedWidth(38)
            em.setValue(saved.get(name, {}).get("end_m", d_em) if isinstance(saved.get(name), dict) else d_em)
            gl.addWidget(em, row, 4)

            tf_combo = QtWidgets.QComboBox(); tf_combo.addItems(self.TF_LIST)
            tf_val = saved.get(name, {}).get("timeframe", d_tf) if isinstance(saved.get(name), dict) else d_tf
            tf_idx = tf_combo.findText(tf_val)
            if tf_idx >= 0: tf_combo.setCurrentIndex(tf_idx)
            tf_combo.setFixedWidth(60)
            gl.addWidget(tf_combo, row, 5)

            color_edit = QtWidgets.QLineEdit(saved.get(name, {}).get("color", default_color) if isinstance(saved.get(name), dict) else default_color)
            color_edit.setFixedWidth(70)
            gl.addWidget(color_edit, row, 6)

            self.session_widgets[name] = {
                "cb": cb, "start_h": sh, "start_m": sm,
                "end_h": eh, "end_m": em, "tf": tf_combo, "color": color_edit,
            }

        layout.addWidget(g)

        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.accept)
        btn_layout.addWidget(btn_ok)
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

    def get_settings(self):
        sessions = {}
        for name, w in self.session_widgets.items():
            sessions[name] = {
                "enabled": w["cb"].isChecked(),
                "start_h": w["start_h"].value(),
                "start_m": w["start_m"].value(),
                "end_h": w["end_h"].value(),
                "end_m": w["end_m"].value(),
                "timeframe": w["tf"].currentText(),
                "color": w["color"].text(),
            }
        return {"sessions": sessions, "show_labels": True}

# ============================================================
#                   Zone Setup Settings Dialog
# ============================================================


class VWAPSettingsDialog(QtWidgets.QDialog):
    def __init__(self, cfg, parent=None):
        super().__init__(parent)
        self.cfg = dict(cfg)
        self.setWindowTitle("VWAP Settings")
        self.setMinimumWidth(450)
        self.setStyleSheet("""QDialog{background:#1a1b26;color:#c0caf5}
QLabel{color:#c0caf5;font-size:10px}QGroupBox{color:#7aa2f7;font-weight:bold;border:1px solid #292e42;border-radius:6px;margin-top:6px;padding-top:8px}
QGroupBox::title{subcontrol-origin:margin;left:6px;padding:0 3px}
QCheckBox{color:#c0caf5;font-size:10px}QComboBox{background:#24283b;color:#c0caf5;border:1px solid #292e42;border-radius:3px;padding:2px 4px;font-size:10px}
QDoubleSpinBox,QSpinBox{background:#24283b;color:#c0caf5;border:1px solid #292e42;border-radius:3px;padding:2px;font-size:10px}
QPushButton{background:#292e42;color:#7aa2f7;border:1px solid #3b4261;border-radius:4px;padding:5px 14px;font-size:10px;font-weight:bold}
QPushButton:hover{background:#3b4261}""")
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        inner = QWidget()
        form = QVBoxLayout(inner)
        form.setSpacing(8)
        grp_a = QGroupBox("Anchors")
        gl = QGridLayout(grp_a)
        gl.setSpacing(4)
        self.use_ses = QCheckBox("Session Open"); self.use_ses.setChecked(cfg.get("use_ses", False)); gl.addWidget(self.use_ses, 0, 0)
        self.use_wk = QCheckBox("Week Open"); self.use_wk.setChecked(cfg.get("use_wk", True)); gl.addWidget(self.use_wk, 0, 1)
        self.use_mo = QCheckBox("Month Open"); self.use_mo.setChecked(cfg.get("use_mo", False)); gl.addWidget(self.use_mo, 0, 2)
        self.use_sh = QCheckBox("Swing High"); self.use_sh.setChecked(cfg.get("use_sh", False)); gl.addWidget(self.use_sh, 1, 0)
        self.use_sl = QCheckBox("Swing Low"); self.use_sl.setChecked(cfg.get("use_sl", False)); gl.addWidget(self.use_sl, 1, 1)
        self.use_hv = QCheckBox("Highest Volume"); self.use_hv.setChecked(cfg.get("use_hv", False)); gl.addWidget(self.use_hv, 1, 2)
        self.use_sw = QCheckBox("Liquidity Sweep"); self.use_sw.setChecked(cfg.get("use_sw", False)); gl.addWidget(self.use_sw, 2, 0)
        self.piv_len = QSpinBox(); self.piv_len.setRange(3, 40); self.piv_len.setValue(cfg.get("piv_len", 10)); gl.addWidget(QLabel("Swing Pivot Length:"), 3, 0); gl.addWidget(self.piv_len, 3, 1)
        self.hv_lb = QSpinBox(); self.hv_lb.setRange(20, 480); self.hv_lb.setValue(cfg.get("hv_lb", 200)); gl.addWidget(QLabel("Highest Volume Lookback:"), 4, 0); gl.addWidget(self.hv_lb, 4, 1)
        form.addWidget(grp_a)
        grp_p = QGroupBox("Primary Stream & Bands")
        gl2 = QGridLayout(grp_p); gl2.setSpacing(4)
        gl2.addWidget(QLabel("Primary Stream:"), 0, 0)
        self.prim = QComboBox(); self.prim.addItems(["Session Open","Week Open","Month Open","Swing High","Swing Low","Highest Volume Bar","Liquidity Sweep"]); self.prim.setCurrentText(cfg.get("prim","Week Open")); gl2.addWidget(self.prim, 0, 1)
        self.show_band = QCheckBox("Show Deviation Bands"); self.show_band.setChecked(cfg.get("show_band", True)); gl2.addWidget(self.show_band, 1, 0, 1, 2)
        gl2.addWidget(QLabel("Inner Band:"), 2, 0); self.band_m1 = QDoubleSpinBox(); self.band_m1.setRange(0.25, 5.0); self.band_m1.setSingleStep(0.25); self.band_m1.setValue(cfg.get("band_m1", 1.0)); gl2.addWidget(self.band_m1, 2, 1)
        gl2.addWidget(QLabel("Outer Band:"), 3, 0); self.band_m2 = QDoubleSpinBox(); self.band_m2.setRange(0.5, 10.0); self.band_m2.setSingleStep(0.25); self.band_m2.setValue(cfg.get("band_m2", 2.0)); gl2.addWidget(self.band_m2, 3, 1)
        form.addWidget(grp_p)
        grp_s = QGroupBox("Signals")
        gl3 = QGridLayout(grp_s); gl3.setSpacing(4)
        self.show_sigs = QCheckBox("Show Band Rejection Signals"); self.show_sigs.setChecked(cfg.get("show_sigs", True)); gl3.addWidget(self.show_sigs, 0, 0, 1, 2)
        gl3.addWidget(QLabel("Cooldown (bars):"), 1, 0); self.sig_cool = QSpinBox(); self.sig_cool.setRange(1, 50); self.sig_cool.setValue(cfg.get("sig_cool", 8)); gl3.addWidget(self.sig_cool, 1, 1)
        gl3.addWidget(QLabel("Signals to Keep:"), 2, 0); self.keep_sigs = QSpinBox(); self.keep_sigs.setRange(2, 30); self.keep_sigs.setValue(cfg.get("keep_sigs", 8)); gl3.addWidget(self.keep_sigs, 2, 1)
        form.addWidget(grp_s)
        grp_cl = QGroupBox("Confluence Clusters")
        gl4 = QGridLayout(grp_cl); gl4.setSpacing(4)
        self.show_clus = QCheckBox("Highlight Cluster Zones"); self.show_clus.setChecked(cfg.get("show_clus", True)); gl4.addWidget(self.show_clus, 0, 0, 1, 2)
        gl4.addWidget(QLabel("Tolerance (ATR ratio):"), 1, 0); self.clus_tol = QDoubleSpinBox(); self.clus_tol.setRange(0.1, 3.0); self.clus_tol.setSingleStep(0.1); self.clus_tol.setValue(cfg.get("clus_tol", 0.5)); gl4.addWidget(self.clus_tol, 1, 1)
        form.addWidget(grp_cl)
        grp_v = QGroupBox("Colors")
        gl5 = QGridLayout(grp_v); gl5.setSpacing(4)
        self._color_btns = {}
        colors = [("c_ses","Session","#d99b1e"),("c_wk","Week","#3b82f6"),("c_mo","Month","#8b5cf6"),
                  ("c_sh","Swing High","#e8365f"),("c_sl","Swing Low","#00a89d"),("c_hv","Highest Volume","#d97706"),
                  ("c_sw","Sweep","#0ea5e9"),("silv","Neutral","#5c6b80")]
        for r, (key, label, default) in enumerate(colors):
            btn = QPushButton(); btn.setFixedSize(24, 24); btn.setStyleSheet(f"background:{cfg.get(key,default)};border:1px solid #292e42;border-radius:3px")
            gl5.addWidget(QLabel(label+":"), r, 0); gl5.addWidget(btn, r, 1)
            self._color_btns[key] = (btn, default)
            def _make_pick(b, k, d=default):
                def pick():
                    from PyQt5.QtWidgets import QColorDialog as _QCD
                    c = _QCD.getColor(QtGui.QColor(self.cfg.get(k, d)), self)
                    if c.isValid():
                        self.cfg[k] = c.name()
                        b.setStyleSheet(f"background:{c.name()};border:1px solid #292e42;border-radius:3px")
                return pick
            btn.clicked.connect(_make_pick(btn, key))
        form.addWidget(grp_v)
        scroll.setWidget(inner)
        layout.addWidget(scroll)
        btn_row = QHBoxLayout()
        ok = QPushButton("OK"); cancel = QPushButton("Cancel")
        ok.clicked.connect(self.accept); cancel.clicked.connect(self.reject)
        btn_row.addStretch(); btn_row.addWidget(ok); btn_row.addWidget(cancel)
        layout.addLayout(btn_row)

    def get_settings(self):
        self.cfg["use_ses"] = self.use_ses.isChecked()
        self.cfg["use_wk"] = self.use_wk.isChecked()
        self.cfg["use_mo"] = self.use_mo.isChecked()
        self.cfg["use_sh"] = self.use_sh.isChecked()
        self.cfg["use_sl"] = self.use_sl.isChecked()
        self.cfg["use_hv"] = self.use_hv.isChecked()
        self.cfg["use_sw"] = self.use_sw.isChecked()
        self.cfg["prim"] = self.prim.currentText()
        self.cfg["show_band"] = self.show_band.isChecked()
        self.cfg["band_m1"] = self.band_m1.value()
        self.cfg["band_m2"] = self.band_m2.value()
        self.cfg["piv_len"] = self.piv_len.value()
        self.cfg["hv_lb"] = self.hv_lb.value()
        self.cfg["show_sigs"] = self.show_sigs.isChecked()
        self.cfg["sig_cool"] = self.sig_cool.value()
        self.cfg["keep_sigs"] = self.keep_sigs.value()
        self.cfg["show_clus"] = self.show_clus.isChecked()
        self.cfg["clus_tol"] = self.clus_tol.value()
        for key, (btn, _) in self._color_btns.items():
            ss = btn.styleSheet()
            if "background:" in ss:
                bg = ss.split("background:")[1].split(";")[0]
                self.cfg[key] = bg
        return self.cfg


class ZoneSetupSettingsDialog(QtWidgets.QDialog):
    def __init__(self, cfg, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Zone Setup Settings")
        self.setMinimumWidth(750)
        self.setMinimumHeight(300)
        self.setStyleSheet("""
            QDialog{background:#0a0a1a;color:#c0caf5}
            QLabel{color:#c0caf5;font-size:10px}
            QGroupBox{color:#7aa2f7;font-weight:bold;border:1px solid #292e42;border-radius:6px;margin-top:6px;padding-top:8px}
            QGroupBox::title{subcontrol-origin:margin;left:6px;padding:0 3px}
            QTableWidget{background:#1a1b26;color:#c0caf5;border:1px solid #292e42;border-radius:4px;font-size:10px;gridline-color:#292e42}
            QTableWidget::item{padding:2px 4px}
            QHeaderView::section{background:#1a1b26;color:#7aa2f7;border:1px solid #292e42;padding:4px;font-size:10px;font-weight:bold}
            QDoubleSpinBox,QSpinBox{background:#1a1b26;color:#c0caf5;border:1px solid #292e42;border-radius:4px;font-size:10px;padding:2px 4px}
            QCheckBox{color:#c0caf5;font-size:10px}
            QCheckBox::indicator{width:14px;height:14px}
            QPushButton{background:#1a1b26;color:#7aa2f7;border:1px solid #292e42;border-radius:4px;padding:6px 16px;font-size:10px;font-weight:bold}
            QPushButton:hover{background:#292e42}
            QPushButton#ok_btn{background:#264d2b;color:#9ece6a;border:1px solid #3d5c3a}
            QPushButton#ok_btn:hover{background:#3d5c3a}
            QPushButton#cancel_btn{background:#4d2626;color:#f7768e;border:1px solid #5c3a3a}
            QPushButton#cancel_btn:hover{background:#5c3a3a}
        """)

        self.rows = []
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(10, 10, 10, 10)

        title = QLabel("Zone Setup Configuration")
        title.setStyleSheet("color:#f7768e;font-size:13px;font-weight:bold;padding:4px 0")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        table = QTableWidget(4, 6)
        table.setHorizontalHeaderLabels(["Active", "Zone Type", "Risk %", "RR", "ATR SL", "Exit: Advanced"])
        zone_types = ["Weekly", "Daily", "H4", "H1"]
        for i in range(4):
            enabled_cb = QCheckBox()
            enabled_cb.setChecked(cfg.get(f"zone_enabled_{i}", False))
            table.setCellWidget(i, 0, enabled_cb)

            type_combo = QtWidgets.QComboBox()
            type_combo.addItems(zone_types)
            idx = type_combo.findText(cfg.get(f"zone_type_{i}", ""))
            if idx >= 0:
                type_combo.setCurrentIndex(idx)
            table.setCellWidget(i, 1, type_combo)

            risk_spin = QDoubleSpinBox()
            risk_spin.setRange(0.1, 100.0)
            risk_spin.setDecimals(1)
            risk_spin.setValue(cfg.get(f"zone_risk_{i}", 1.0))
            risk_spin.setSuffix(" %")
            risk_spin.setFixedWidth(90)
            table.setCellWidget(i, 2, risk_spin)

            rr_spin = QDoubleSpinBox()
            rr_spin.setRange(0.1, 50.0)
            rr_spin.setDecimals(1)
            rr_spin.setValue(cfg.get(f"zone_rr_{i}", 2.0))
            rr_spin.setFixedWidth(80)
            table.setCellWidget(i, 3, rr_spin)

            atr_spin = QDoubleSpinBox()
            atr_spin.setRange(0.1, 10.0)
            atr_spin.setDecimals(1)
            atr_spin.setValue(cfg.get(f"zone_atr_sl_{i}", 1.5))
            atr_spin.setFixedWidth(80)
            table.setCellWidget(i, 4, atr_spin)

            exit_cb = QCheckBox()
            exit_cb.setChecked(cfg.get(f"zone_exit_{i}", False))
            table.setCellWidget(i, 5, exit_cb)

            self.rows.append({"enabled": enabled_cb, "zone_type": type_combo, "risk": risk_spin, "rr": rr_spin, "atr_sl": atr_spin, "exit": exit_cb})

        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(True)
        layout.addWidget(table)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("cancel_btn")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        ok_btn = QPushButton("Save")
        ok_btn.setObjectName("ok_btn")
        ok_btn.clicked.connect(self.accept)
        btn_row.addWidget(ok_btn)
        layout.addLayout(btn_row)

    def get_settings(self):
        s = {}
        for i, row in enumerate(self.rows):
            s[f"zone_enabled_{i}"] = row["enabled"].isChecked() and row["zone_type"].currentText() != ""
            s[f"zone_type_{i}"] = row["zone_type"].currentText()
            s[f"zone_risk_{i}"] = row["risk"].value()
            s[f"zone_rr_{i}"] = row["rr"].value()
            s[f"zone_atr_sl_{i}"] = row["atr_sl"].value()
            s[f"zone_exit_{i}"] = row["exit"].isChecked()
        return s


# ============================================================
#                   Strategy Panel (left side)
# ============================================================

class StrategyPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(180)
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0f1117, stop:1 #0c0e16);
                border-right: 1px solid #1e2030;
            }
        """)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet(
            "QScrollArea{background:transparent;border:none}"
            "QScrollBar:vertical{width:6px;background:#0a0a1a}"
            "QScrollBar::handle:vertical{background:#292e42;border-radius:3px}"
        )

        content = QWidget()
        content.setStyleSheet("background:transparent")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(3)

        title = QLabel("\U0001F4C8 Strategy")
        title.setObjectName("section_title")
        layout.addWidget(title)

        group = QGroupBox("RISK")
        group.setStyleSheet("QGroupBox{color:#e0af68;font-weight:bold;border:1px solid #292e42;border-radius:6px;margin-top:8px;padding-top:10px;background:rgba(224,175,104,0.03)} QGroupBox::title{subcontrol-origin:margin;left:8px;padding:0 4px;color:#e0af68}")
        form = QVBoxLayout(group)
        form.setSpacing(2)
        form.setContentsMargins(4, 2, 4, 2)

        self.risk_combo = QtWidgets.QComboBox()
        self.risk_combo.addItems(["% Balance", "$ Fixed", "Fixed Lot"])
        self.risk_combo.currentIndexChanged.connect(self.on_risk_mode_changed)
        form.addWidget(self.risk_combo)

        self.lbl_risk_value = QLabel("Risk %:")
        form.addWidget(self.lbl_risk_value)
        self.risk_input = QtWidgets.QDoubleSpinBox()
        self.risk_input.setDecimals(2)
        self.risk_input.setRange(0.01, 100)
        self.risk_input.setValue(1.0)
        self.risk_input.setSuffix(" %")
        form.addWidget(self.risk_input)

        rr_row = QHBoxLayout(); rr_row.setSpacing(2)
        rr_row.addWidget(QLabel("RR:"))
        self.rr_input = QtWidgets.QDoubleSpinBox()
        self.rr_input.setDecimals(1)
        self.rr_input.setRange(0.1, 50)
        self.rr_input.setValue(3.0)
        self.rr_input.setSingleStep(0.5)
        self.rr_input.setFixedWidth(50)
        rr_row.addWidget(self.rr_input)
        rr_row.addStretch()
        form.addLayout(rr_row)

        self.auto_live_cb = QCheckBox("Auto Live Trade")
        self.auto_live_cb.setStyleSheet("color:#c0caf5;font-size:10px")
        form.addWidget(self.auto_live_cb)

        pos_row = QHBoxLayout(); pos_row.setSpacing(2)
        pos_row.addWidget(QLabel("Max Pos:"))
        self.max_positions = QtWidgets.QSpinBox()
        self.max_positions.setRange(0, 100)
        self.max_positions.setValue(5)
        self.max_positions.setFixedWidth(50)
        self.max_positions.setToolTip("0 = unlimited")
        pos_row.addWidget(self.max_positions)
        pos_row.addWidget(QLabel("Per Symbol:"))
        self.max_per_symbol = QtWidgets.QSpinBox()
        self.max_per_symbol.setRange(0, 100)
        self.max_per_symbol.setValue(2)
        self.max_per_symbol.setFixedWidth(50)
        self.max_per_symbol.setToolTip("0 = unlimited")
        pos_row.addWidget(self.max_per_symbol)
        pos_row.addStretch()
        form.addLayout(pos_row)

        layout.addWidget(group)

        # ---- Professional Exit System ----
        self.exit_group = QGroupBox("EXIT")
        self.exit_group.setStyleSheet("QGroupBox{color:#7aa2f7;font-weight:bold;border:1px solid #292e42;border-radius:6px;margin-top:8px;padding-top:10px;background:rgba(122,162,247,0.03)} QGroupBox::title{subcontrol-origin:margin;left:8px;padding:0 4px;color:#7aa2f7}")
        ef = QVBoxLayout(self.exit_group)
        ef.setSpacing(2)
        ef.setContentsMargins(3, 2, 3, 2)

        self.exit_master = QCheckBox("Exit Master")
        self.exit_master.setStyleSheet("color:#c0caf5;font-size:10px")
        ef.addWidget(self.exit_master)

        tr = QHBoxLayout(); tr.setContentsMargins(0, 0, 0, 0); tr.setSpacing(4)
        self.trail_algoman_cb = QCheckBox("Trailing SL (Lead52)")
        self.trail_algoman_cb.setStyleSheet("color:#bb9af7;font-size:9px;font-weight:bold")
        self.trail_algoman_cb.setToolTip("SL follows Ichimoku Lead 52 line with ATR offset")
        tr.addWidget(self.trail_algoman_cb)
        lbl_start = QLabel("Start:")
        lbl_start.setStyleSheet("color:#bb9af7;font-size:8px;font-weight:bold")
        tr.addWidget(lbl_start)
        self.trail_algoman_act = QtWidgets.QComboBox()
        self.trail_algoman_act.addItems(["10% TP", "25% TP", "50% TP", "TP1", "TP1.5", "TP2"])
        self.trail_algoman_act.setCurrentIndex(1)
        self.trail_algoman_act.setFixedWidth(75)
        self.trail_algoman_act.setStyleSheet("background:#1a1b26;color:#bb9af7;border:1px solid #292e42;border-radius:3px;padding:2px;font-size:9px;font-weight:bold")
        tr.addWidget(self.trail_algoman_act)
        tr.addStretch()
        ef.addLayout(tr)
        tr2 = QHBoxLayout(); tr2.setContentsMargins(16, 0, 0, 0); tr2.setSpacing(4)
        lbl_atr = QLabel("ATR:")
        lbl_atr.setStyleSheet("color:#bb9af7;font-size:8px;font-weight:bold")
        tr2.addWidget(lbl_atr)
        self.trail_atr_mult = QtWidgets.QDoubleSpinBox()
        self.trail_atr_mult.setRange(0.1, 10.0)
        self.trail_atr_mult.setSingleStep(0.1)
        self.trail_atr_mult.setValue(0.5)
        self.trail_atr_mult.setDecimals(1)
        self.trail_atr_mult.setFixedWidth(50)
        self.trail_atr_mult.setStyleSheet("background:#1a1b26;color:#bb9af7;border:1px solid #292e42;border-radius:3px;padding:2px;font-size:9px;font-weight:bold")
        tr2.addWidget(self.trail_atr_mult)
        lbl_atr_info = QLabel("(offset from Lead52)")
        lbl_atr_info.setStyleSheet("color:#565f89;font-size:7px;font-style:italic")
        tr2.addWidget(lbl_atr_info)
        tr2.addStretch()
        ef.addLayout(tr2)

        self.be_cb = QCheckBox("Breakeven")
        self.be_cb.setStyleSheet("color:#7aa2f7;font-size:8px")
        ef.addWidget(self.be_cb)
        br = QHBoxLayout(); br.setContentsMargins(0, 0, 0, 0); br.setSpacing(2)
        br.addWidget(QLabel("TP%:"))
        self.be_act = QtWidgets.QComboBox()
        self.be_act.addItems(["50%", "75%", "100%", "125%", "150%", "175%", "200%"])
        self.be_act.setCurrentText("100%")
        self.be_act.setFixedWidth(46)
        self.be_act.setStyleSheet("background:#1a1b26;color:#c0caf5;border:1.5px solid #292e42;border-radius:6px;font-size:8px")
        br.addWidget(self.be_act)
        br.addWidget(QLabel("SL%:"))
        self.be_lock = QtWidgets.QComboBox()
        self.be_lock.addItems(["25%", "50%", "75%", "100%"])
        self.be_lock.setCurrentText("100%")
        self.be_lock.setFixedWidth(46)
        self.be_lock.setStyleSheet("background:#1a1b26;color:#c0caf5;border:1.5px solid #292e42;border-radius:6px;font-size:8px")
        br.addWidget(self.be_lock)
        ef.addLayout(br)

        self.tp_levels_cb = QCheckBox("Partial TP")
        self.tp_levels_cb.setStyleSheet("color:#7aa2f7;font-size:8px")
        ef.addWidget(self.tp_levels_cb)
        self.tp_levels_edit = QLineEdit("1.0:25, 2.0:25, 3.0:50")
        self.tp_levels_edit.setStyleSheet("background:#1a1b26;color:#c0caf5;border:1.5px solid #292e42;border-radius:6px;padding:2px 4px;font-size:8px")
        ef.addWidget(self.tp_levels_edit)

        self.time_cb = QCheckBox("Time Exit")
        self.time_cb.setStyleSheet("color:#7aa2f7;font-size:8px")
        ef.addWidget(self.time_cb)
        tm = QHBoxLayout(); tm.setContentsMargins(0, 0, 0, 0); tm.setSpacing(2)
        tm.addWidget(QLabel("Min:"))
        self.time_min = QtWidgets.QSpinBox()
        self.time_min.setRange(5, 1440); self.time_min.setValue(60)
        self.time_min.setSuffix("m"); self.time_min.setFixedWidth(48)
        self.time_min.setStyleSheet("background:#1a1b26;color:#c0caf5;border:1.5px solid #292e42;border-radius:6px")
        tm.addWidget(self.time_min)
        ef.addLayout(tm)

        layout.addWidget(self.exit_group)

        # ---- INDICATORS ----
        self.ind_group = QGroupBox("IND")
        self.ind_group.setStyleSheet("QGroupBox{color:#9ece6a;font-weight:bold;border:1px solid #292e42;border-radius:6px;margin-top:8px;padding-top:10px;background:rgba(158,206,106,0.03)} QGroupBox::title{subcontrol-origin:margin;left:8px;padding:0 4px;color:#9ece6a}")
        indf = QVBoxLayout(self.ind_group)
        indf.setSpacing(2)
        indf.setContentsMargins(3, 2, 3, 2)

        ichimoku_row = QHBoxLayout()
        ichimoku_row.setSpacing(4)
        self.ichimoku_cb = QCheckBox("Ichimoku Cloud")
        self.ichimoku_cb.setStyleSheet("color:#c0caf5;font-size:10px")
        ichimoku_row.addWidget(self.ichimoku_cb)
        self.ichimoku_gear = QPushButton("\u2699")
        self.ichimoku_gear.setFixedSize(20, 20)
        self.ichimoku_gear.setStyleSheet("QPushButton{background:#1a1b26;color:#7aa2f7;border:1px solid #292e42;border-radius:4px;font-size:12px} QPushButton:hover{background:#292e42}")
        self.ichimoku_gear.clicked.connect(self._open_ichimoku_settings)
        ichimoku_row.addWidget(self.ichimoku_gear)
        ichimoku_row.addStretch()
        indf.addLayout(ichimoku_row)

        ma_row = QHBoxLayout()
        ma_row.setSpacing(4)
        self.ma_cb = QCheckBox("Moving Average")
        self.ma_cb.setStyleSheet("color:#c0caf5;font-size:10px")
        ma_row.addWidget(self.ma_cb)
        self.ma_gear = QPushButton("\u2699")
        self.ma_gear.setFixedSize(20, 20)
        self.ma_gear.setStyleSheet("QPushButton{background:#1a1b26;color:#7aa2f7;border:1px solid #292e42;border-radius:4px;font-size:12px} QPushButton:hover{background:#292e42}")
        self.ma_gear.clicked.connect(self._open_ma_settings)
        ma_row.addWidget(self.ma_gear)
        ma_row.addStretch()
        indf.addLayout(ma_row)

        self.week_hl_cb = QCheckBox("Last week's ceiling and floor")
        self.week_hl_cb.setStyleSheet("color:#c0caf5;font-size:10px")
        indf.addWidget(self.week_hl_cb)

        self.day_hl_cb = QCheckBox("Last Day's ceiling and floor")
        self.day_hl_cb.setStyleSheet("color:#c0caf5;font-size:10px")
        indf.addWidget(self.day_hl_cb)

        self.h4_hl_cb = QCheckBox("Last H4's ceiling and floor")
        self.h4_hl_cb.setStyleSheet("color:#c0caf5;font-size:10px")
        indf.addWidget(self.h4_hl_cb)

        self.h1_hl_cb = QCheckBox("Important H1 Level")
        self.h1_hl_cb.setStyleSheet("color:#c0caf5;font-size:10px")
        indf.addWidget(self.h1_hl_cb)

        self.open_day_cb = QCheckBox("Open Day Candle")
        self.open_day_cb.setStyleSheet("color:#e0af68;font-size:10px;font-weight:bold")
        indf.addWidget(self.open_day_cb)

        self.yesterday_candle_cb = QCheckBox("Yesterday Candle Zone")
        self.yesterday_candle_cb.setStyleSheet("color:#73daca;font-size:10px;font-weight:bold")
        indf.addWidget(self.yesterday_candle_cb)

        vwap_row = QHBoxLayout()
        vwap_row.setSpacing(4)
        self.vwap_cb = QCheckBox("VWAP")
        self.vwap_cb.setStyleSheet("color:#d99b1e;font-size:10px;font-weight:bold")
        vwap_row.addWidget(self.vwap_cb)
        self.vwap_gear = QPushButton("\u2699")
        self.vwap_gear.setFixedSize(20, 20)
        self.vwap_gear.setStyleSheet("QPushButton{background:#1a1b26;color:#7aa2f7;border:1px solid #292e42;border-radius:4px;font-size:12px} QPushButton:hover{background:#292e42}")
        self.vwap_gear.clicked.connect(self._open_vwap_settings)
        vwap_row.addWidget(self.vwap_gear)
        vwap_row.addStretch()
        indf.addLayout(vwap_row)

        algoman_row = QHBoxLayout()
        algoman_row.setSpacing(4)
        self.algoman_cb = QCheckBox("AlgoMan")
        self.algoman_cb.setStyleSheet("color:#c0caf5;font-size:10px;font-weight:bold")
        algoman_row.addWidget(self.algoman_cb)
        self.algoman_gear = QPushButton("\u2699")
        self.algoman_gear.setFixedSize(20, 20)
        self.algoman_gear.setStyleSheet("QPushButton{background:#1a1b26;color:#7aa2f7;border:1px solid #292e42;border-radius:4px;font-size:12px} QPushButton:hover{background:#292e42}")
        self.algoman_gear.clicked.connect(self._open_algoman_settings)
        algoman_row.addWidget(self.algoman_gear)
        algoman_row.addStretch()
        indf.addLayout(algoman_row)

        session_break_row = QHBoxLayout()
        session_break_row.setSpacing(4)
        self.session_break_cb = QCheckBox("Session Break")
        self.session_break_cb.setStyleSheet("color:#c0caf5;font-size:10px;font-weight:bold")
        session_break_row.addWidget(self.session_break_cb)
        self.session_break_gear = QPushButton("\u2699")
        self.session_break_gear.setFixedSize(20, 20)
        self.session_break_gear.setStyleSheet("QPushButton{background:#1a1b26;color:#7aa2f7;border:1px solid #292e42;border-radius:4px;font-size:12px} QPushButton:hover{background:#292e42}")
        self.session_break_gear.clicked.connect(self._open_session_break_settings)
        session_break_row.addWidget(self.session_break_gear)
        session_break_row.addStretch()
        indf.addLayout(session_break_row)

        layout.addWidget(self.ind_group)

        # ---- SCAN SPEED ----
        self.scan_group = QGroupBox("Scan Speed")
        self.scan_group.setStyleSheet("QGroupBox{color:#bb9af7;font-weight:bold;border:1px solid #292e42;border-radius:6px;margin-top:8px;padding-top:10px;background:rgba(187,154,247,0.03)} QGroupBox::title{subcontrol-origin:margin;left:8px;padding:0 4px;color:#bb9af7}")
        sg = QGridLayout(self.scan_group)
        sg.setSpacing(4)
        sg.setContentsMargins(4, 2, 4, 2)

        sg.addWidget(QLabel("Scan Speed (sec):"), 0, 0)
        self.scan_speed = QtWidgets.QSpinBox()
        self.scan_speed.setRange(1, 300)
        self.scan_speed.setValue(5)
        self.scan_speed.setSuffix(" s")
        self.scan_speed.setFixedWidth(55)
        self.scan_speed.setStyleSheet("background:#1a1b26;color:#c0caf5;border:1px solid #292e42;border-radius:4px;font-size:10px")
        sg.addWidget(self.scan_speed, 0, 1)

        ms_scan_row = QHBoxLayout()
        ms_scan_row.setSpacing(4)
        self.ms_scan_cb = QCheckBox("Multi-Symbol Scan")
        self.ms_scan_cb.setStyleSheet("color:#c0caf5;font-size:10px;font-weight:bold")
        ms_scan_row.addWidget(self.ms_scan_cb)
        self.ms_scan_gear = QPushButton("\u2699")
        self.ms_scan_gear.setFixedSize(20, 20)
        self.ms_scan_gear.setStyleSheet("QPushButton{background:#1a1b26;color:#7aa2f7;border:1px solid #292e42;border-radius:4px;font-size:12px} QPushButton:hover{background:#292e42}")
        self.ms_scan_gear.clicked.connect(self._open_ms_scan_settings)
        ms_scan_row.addWidget(self.ms_scan_gear)
        ms_scan_row.addStretch()
        sg.addLayout(ms_scan_row, 1, 0, 1, 2)

        sg.addWidget(QLabel("Scan TF:"), 2, 0)
        self.ms_scan_tf = QComboBox()
        self.ms_scan_tf.addItems(["M1", "M3", "M5", "M10", "M15", "M30", "H1", "H4", "D1"])
        self.ms_scan_tf.setCurrentText("M15")
        self.ms_scan_tf.setFixedWidth(65)
        self.ms_scan_tf.setStyleSheet("background:#1a1b26;color:#c0caf5;border:1px solid #292e42;border-radius:4px;font-size:10px")
        sg.addWidget(self.ms_scan_tf, 2, 1)

        self.ms_scan_cfg = {
            "scan_interval": 5,
            "signal_tfs": {"Weekly": True, "Daily": True, "H4": True, "H1": True},
            "chart_tfs": {"M15": True, "M30": True},
            "sound_alarm": True,
        }

        layout.addWidget(self.scan_group)

        # ---- SETUP ----
        self.setup_group = QGroupBox("Setup")
        self.setup_group.setStyleSheet("QGroupBox{color:#f7768e;font-weight:bold;border:1px solid #292e42;border-radius:6px;margin-top:8px;padding-top:10px;background:rgba(247,118,142,0.03)} QGroupBox::title{subcontrol-origin:margin;left:8px;padding:0 4px;color:#f7768e}")
        stl = QVBoxLayout(self.setup_group)
        stl.setSpacing(6)
        stl.setContentsMargins(4, 2, 4, 2)

        # Zone Setup
        zone_row = QHBoxLayout()
        zone_row.setSpacing(4)
        self.zone_setup_cb = QCheckBox("Zone Setup")
        self.zone_setup_cb.setStyleSheet("color:#c0caf5;font-size:10px;font-weight:bold")
        zone_row.addWidget(self.zone_setup_cb)
        self.zone_setup_gear = QPushButton("\u2699")
        self.zone_setup_gear.setFixedSize(20, 20)
        self.zone_setup_gear.setStyleSheet("QPushButton{background:#1a1b26;color:#7aa2f7;border:1px solid #292e42;border-radius:4px;font-size:12px} QPushButton:hover{background:#292e42}")
        self.zone_setup_gear.clicked.connect(self._open_zone_setup_settings)
        zone_row.addWidget(self.zone_setup_gear)
        zone_row.addStretch()
        stl.addLayout(zone_row)

        self.zone_setup_cfg = {}
        self.zone_setup_status = QLabel("")
        self.zone_setup_status.setStyleSheet("color:#565f89;font-size:8px;padding:2px 4px")
        self.zone_setup_status.setAlignment(Qt.AlignCenter)
        stl.addWidget(self.zone_setup_status)

        self.zone_checklist = QFrame()
        self.zone_checklist.setStyleSheet("QFrame{background:rgba(247,118,142,0.05);border:1px solid #292e42;border-radius:4px;padding:4px}")
        zcl = QVBoxLayout(self.zone_checklist)
        zcl.setSpacing(2)
        zcl.setContentsMargins(6, 4, 6, 4)

        self.zone_dir_title = QLabel("")
        self.zone_dir_title.setAlignment(Qt.AlignCenter)
        zcl.addWidget(self.zone_dir_title)

        self.zone_items = []
        zone_labels = [
            ("zone_chk_fakebreak", "Trade Type (Rejection/FakeBreak)"),
            ("zone_chk_touched", "Zone Touched"),
            ("zone_chk_engulfing", "Close Beyond Prev Candle"),
            ("zone_chk_lower_shadow", "Lower Shadow (Small/Large)"),
            ("zone_chk_upper_shadow", "Upper Shadow (Small/Large)"),
            ("zone_chk_strong_body", "Strong Full Body Candle"),
            ("zone_chk_close_beyond", "Close Beyond Zone"),
            ("zone_chk_next_candle", "Next Candle Confirmation"),
            ("zone_chk_rr", "Risk:Reward Valid"),
        ]
        for key, label_text in zone_labels:
            row = QHBoxLayout()
            row.setSpacing(4)
            lbl = QLabel(label_text)
            lbl.setStyleSheet("color:#c0caf5;font-size:9px")
            row.addWidget(lbl)
            row.addStretch()
            status_lbl = QLabel("\u2717")
            status_lbl.setStyleSheet("color:#f7768e;font-size:11px;font-weight:bold")
            status_lbl.setFixedWidth(18)
            row.addWidget(status_lbl)
            zcl.addLayout(row)
            self.zone_items.append({"label": lbl, "status": status_lbl, "key": key})

        self.zone_trade_info = QLabel("")
        self.zone_trade_info.setStyleSheet("color:#7aa2f7;font-size:9px;font-weight:bold;padding:4px 2px")
        self.zone_trade_info.setWordWrap(True)
        zcl.addWidget(self.zone_trade_info)

        self._zone_last_signal = {}

        stl.addWidget(self.zone_checklist)
        self.zone_checklist.setVisible(False)

        def _toggle_zone_checklist(state):
            self.zone_checklist.setVisible(state == Qt.Checked)
        self.zone_setup_cb.stateChanged.connect(_toggle_zone_checklist)

        layout.addWidget(self.setup_group)

        scroll.setWidget(content)
        outer.addWidget(scroll)

        # trigger chart refresh when indicator checkboxes / settings change
        self.ichimoku_cb.stateChanged.connect(self._on_indicator_toggled)
        self.week_hl_cb.stateChanged.connect(self._on_indicator_toggled)
        self.day_hl_cb.stateChanged.connect(self._on_indicator_toggled)
        self.h4_hl_cb.stateChanged.connect(self._on_indicator_toggled)
        self.h1_hl_cb.stateChanged.connect(self._on_indicator_toggled)
        self.open_day_cb.stateChanged.connect(self._on_indicator_toggled)
        self.yesterday_candle_cb.stateChanged.connect(self._on_indicator_toggled)
        self.vwap_cb.stateChanged.connect(self._on_indicator_toggled)
        self.ma_cb.stateChanged.connect(self._on_indicator_toggled)
        self.session_break_cb.stateChanged.connect(self._on_indicator_toggled)
        self.zone_setup_cb.stateChanged.connect(self._on_indicator_toggled)
        self.algoman_cb.stateChanged.connect(self._on_indicator_toggled)
        self.zone_setup_cb.stateChanged.connect(self._on_zone_setup_toggled)

        # connect all widgets to save_settings
        self._connect_save(self.risk_combo, "currentIndexChanged")
        self._connect_save(self.risk_input, "valueChanged")
        self._connect_save(self.rr_input, "valueChanged")

        self._connect_save(self.exit_master, "stateChanged")
        self._connect_save(self.trail_algoman_cb, "stateChanged")
        self._connect_save(self.trail_algoman_act, "currentIndexChanged")
        self._connect_save(self.trail_atr_mult, "valueChanged")
        self._connect_save(self.be_cb, "stateChanged")
        self._connect_save(self.be_act, "currentTextChanged")
        self._connect_save(self.be_lock, "currentTextChanged")
        self._connect_save(self.tp_levels_cb, "stateChanged")
        self._connect_save(self.time_cb, "stateChanged")
        self._connect_save(self.time_min, "valueChanged")
        self._connect_save(self.tp_levels_edit, "textChanged")
        self._connect_save(self.ichimoku_cb, "stateChanged")
        self._connect_save(self.week_hl_cb, "stateChanged")
        self._connect_save(self.day_hl_cb, "stateChanged")
        self._connect_save(self.h4_hl_cb, "stateChanged")
        self._connect_save(self.h1_hl_cb, "stateChanged")
        self._connect_save(self.open_day_cb, "stateChanged")
        self._connect_save(self.yesterday_candle_cb, "stateChanged")
        self._connect_save(self.vwap_cb, "stateChanged")
        self._connect_save(self.scan_speed, "valueChanged")
        self._connect_save(self.max_positions, "valueChanged")
        self._connect_save(self.max_per_symbol, "valueChanged")
        self._connect_save(self.auto_live_cb, "stateChanged")
        self._connect_save(self.session_break_cb, "stateChanged")
        self._connect_save(self.zone_setup_cb, "stateChanged")

        self.config_path = "config.json"
        self.ichimoku_cfg = {}
        self.ma_cfg = {}
        self.algoman_cfg = {}
        self.vwap_cfg = {
            "use_ses": False, "use_wk": True, "use_mo": False,
            "use_sh": False, "use_sl": False, "use_hv": False, "use_sw": False,
            "prim": "Week Open", "show_band": True,
            "band_m1": 1.0, "band_m2": 2.0, "piv_len": 10, "hv_lb": 200,
            "show_sigs": True, "sig_cool": 8, "keep_sigs": 8,
            "show_clus": True, "clus_tol": 0.5,
            "c_ses": "#d99b1e", "c_wk": "#3b82f6", "c_mo": "#8b5cf6",
            "c_sh": "#e8365f", "c_sl": "#00a89d", "c_hv": "#d97706",
            "c_sw": "#0ea5e9", "silv": "#5c6b80",
        }
        self.session_break_cfg = {
            "sessions": {
                "Daily": {"enabled": True, "start_h": 0, "start_m": 0, "end_h": 23, "end_m": 59, "timeframe": "D1", "color": "#e0af68"},
                "Asian": {"enabled": True, "start_h": 0, "start_m": 0, "end_h": 8, "end_m": 0, "timeframe": "H1", "color": "#565f89"},
                "London": {"enabled": True, "start_h": 8, "start_m": 0, "end_h": 16, "end_m": 0, "timeframe": "H1", "color": "#7aa2f7"},
                "New York": {"enabled": True, "start_h": 13, "start_m": 0, "end_h": 21, "end_m": 0, "timeframe": "H1", "color": "#bb9af7"},
            },
            "show_labels": True,
        }
        self.zone_setup_cfg = {}
        self._loading_settings = True
        self.load_settings()
        self._loading_settings = False

    def _connect_save(self, widget, signal_name):
        signal = getattr(widget, signal_name, None)
        if signal:
            signal.connect(self._on_any_setting_changed)

    def _on_any_setting_changed(self, *_):
        if self._loading_settings:
            return
        self.save_settings()

    def _on_indicator_toggled(self):
        cw = self.window().findChild(ChartWidget)
        if cw:
            if hasattr(cw, '_zone_arrows'):
                for item in cw._zone_arrows:
                    try:
                        cw.candle_plot.removeItem(item)
                    except Exception:
                        pass
                cw._zone_arrows.clear()
            cw._update_ichimoku()
            cw._update_ma()
            cw._update_week_hl()
            cw._update_day_hl()
            cw._update_yesterday_candle()
            cw._update_h4_hl()
            cw._update_h1_hl()
            cw._update_open_day()
            cw._update_level_rejections()
            cw._update_session_break()
            cw._update_algoman()
            cw._update_vwap()
        mw = self.window()
        if hasattr(mw, '_ms_scan_active') and mw._ms_scan_active:
            zcbs = {
                "Weekly": self.week_hl_cb.isChecked() if hasattr(self, 'week_hl_cb') else False,
                "Daily": self.day_hl_cb.isChecked() if hasattr(self, 'day_hl_cb') else False,
                "H4": self.h4_hl_cb.isChecked() if hasattr(self, 'h4_hl_cb') else False,
                "H1": self.h1_hl_cb.isChecked() if hasattr(self, 'h1_hl_cb') else False,
            }
            mw._multi_scanner._zone_checkboxes = zcbs

    def _open_ichimoku_settings(self):
        dlg = IchimokuSettingsDialog(self)
        if dlg.exec_():
            self.ichimoku_cfg = dlg.get_settings()
            self.save_settings()
            cw = self.window().findChild(ChartWidget)
            if cw:
                cw._update_ichimoku()

    def _open_ma_settings(self):
        dlg = MASettingsDialog(self)
        if dlg.exec_():
            self.ma_cfg = dlg.get_settings()
            self.save_settings()
            cw = self.window().findChild(ChartWidget)
            if cw:
                cw._update_ma()

    def _open_ms_scan_settings(self):
        dlg = MultiScanSettingsDialog(self.ms_scan_cfg, self)
        if dlg.exec_():
            self.ms_scan_cfg = dlg.get_settings()
            self.save_settings()

    def _open_algoman_settings(self):
        dlg = AlgomanSettingsDialog(self.algoman_cfg, self)
        if dlg.exec_():
            self.algoman_cfg = dlg.get_settings()
            self.save_settings()
            cw = self.window().findChild(ChartWidget)
            if cw:
                cw._update_algoman()

    def _open_vwap_settings(self):
        dlg = VWAPSettingsDialog(self.vwap_cfg, self)
        if dlg.exec_():
            self.vwap_cfg = dlg.get_settings()
            self.save_settings()
            cw = self.window().findChild(ChartWidget)
            if cw:
                cw._update_vwap()

    def _open_session_break_settings(self):
        dlg = SessionBreakSettingsDialog(self.session_break_cfg, self)
        if dlg.exec_():
            self.session_break_cfg = dlg.get_settings()
            self.save_settings()
            cw = self.window().findChild(ChartWidget)
            if cw:
                cw._update_session_break()

    def _on_zone_setup_toggled(self):
        self._update_zone_setup_status()
        if not self.zone_setup_cb.isChecked():
            cw = self.window().findChild(ChartWidget)
            if cw and hasattr(cw, '_zone_arrows'):
                for item in cw._zone_arrows:
                    try:
                        cw.candle_plot.removeItem(item)
                    except Exception:
                        pass
                cw._zone_arrows.clear()

    def _open_zone_setup_settings(self):
        dlg = ZoneSetupSettingsDialog(self.zone_setup_cfg, self)
        if dlg.exec_():
            self.zone_setup_cfg = dlg.get_settings()
            self.save_settings()
            self._update_zone_setup_status()
            self._update_zone_checklist()

    def _update_zone_setup_status(self):
        cfg = self.zone_setup_cfg
        entries = []
        for i in range(4):
            enabled = cfg.get(f"zone_enabled_{i}", False)
            zone_type = cfg.get(f"zone_type_{i}", "")
            risk = cfg.get(f"zone_risk_{i}", 1.0)
            rr = cfg.get(f"zone_rr_{i}", 2.0)
            atr_sl = cfg.get(f"zone_atr_sl_{i}", 1.5)
            exit_adv = cfg.get(f"zone_exit_{i}", False)
            if enabled and zone_type:
                exit_tag = " | Exit:Adv" if exit_adv else ""
                entries.append(f"#{i+1} {zone_type} R:{risk}% RR:{rr} ATR:{atr_sl}{exit_tag}")
        if entries:
            self.zone_setup_status.setText(" | ".join(entries))
            self.zone_setup_status.setStyleSheet("color:#7aa2f7;font-size:8px;padding:2px 4px")
        else:
            self.zone_setup_status.setText("No zone entries configured")
            self.zone_setup_status.setStyleSheet("color:#565f89;font-size:8px;padding:2px 4px")

    def _update_zone_checklist(self):
        import bisect
        sp = self if hasattr(self, 'zone_items') else self.window().findChild(StrategyPanel)
        cw = self.window().findChild(ChartWidget)
        if cw and hasattr(cw, '_zone_arrows'):
            for item in cw._zone_arrows:
                try:
                    cw.candle_plot.removeItem(item)
                except Exception:
                    pass
            cw._zone_arrows.clear()
        if not sp or not sp.zone_setup_cb.isChecked():
            return
        cfg = sp.zone_setup_cfg
        if not cfg:
            return
        cw = self.window().findChild(ChartWidget)
        if cw is None or cw.data_df is None or len(cw.data_df) < 10:
            return
        df = cw.data_df
        n = len(df)
        info = mt5.symbol_info(cw.current_symbol)
        if not info:
            return
        pip = info.point * 10 if info.point <= 0.001 else info.point

        tf_map = {
            0: mt5.TIMEFRAME_W1,
            1: mt5.TIMEFRAME_D1,
            2: mt5.TIMEFRAME_H4,
            3: mt5.TIMEFRAME_H1,
        }

        closes = df["close"].values.astype(float)
        opens_arr = df["open"].values.astype(float)
        highs_arr = df["high"].values.astype(float)
        lows_arr = df["low"].values.astype(float)
        chart_times = cw._raw_times

        atr_val = pip
        try:
            atr_rates = mt5.copy_rates_from_pos(cw.current_symbol, cw.current_tf, 0, 20)
            if atr_rates is not None and len(atr_rates) >= 15:
                ar_h = np.array([r['high'] for r in atr_rates])
                ar_l = np.array([r['low'] for r in atr_rates])
                ar_c = np.array([r['close'] for r in atr_rates])
                tr_arr = np.maximum(ar_h[1:] - ar_l[1:], np.maximum(np.abs(ar_h[1:] - ar_c[:-1]), np.abs(ar_l[1:] - ar_c[:-1])))
                atr_val = float(np.mean(tr_arr[-14:])) if len(tr_arr) >= 14 else float(np.mean(tr_arr))
        except Exception:
            pass

        lookback_start = max(10, n - 100)
        last_signal = None

        for i in range(4):
            if not cfg.get(f"zone_enabled_{i}", False):
                continue
            zt = cfg.get(f"zone_type_{i}", "")
            if not zt:
                continue
            risk_pct = cfg.get(f"zone_risk_{i}", 1.0)
            rr_val = cfg.get(f"zone_rr_{i}", 2.0)
            atr_sl_mult = cfg.get(f"zone_atr_sl_{i}", 1.5)
            use_exit = cfg.get(f"zone_exit_{i}", False)

            # Parse zone type to get timeframe index
            zt_lower = zt.lower()
            if "weekly" in zt_lower:
                zone_idx = 0
                zone_tf = mt5.TIMEFRAME_W1
            elif "daily" in zt_lower:
                zone_idx = 1
                zone_tf = mt5.TIMEFRAME_D1
            elif "h4" in zt_lower:
                zone_idx = 2
                zone_tf = mt5.TIMEFRAME_H4
            elif "h1" in zt_lower:
                zone_idx = 3
                zone_tf = mt5.TIMEFRAME_H1
            else:
                continue

            hl_cbs = [sp.week_hl_cb, sp.day_hl_cb, sp.h4_hl_cb, sp.h1_hl_cb]
            hl_items = [cw._week_hl_items, cw._day_hl_items, cw._h4_hl_items, cw._h1_hl_items]
            if not hl_cbs[zone_idx].isChecked() or not hl_items[zone_idx]:
                continue

            zone_rates = mt5.copy_rates_from_pos(cw.current_symbol, zone_tf, 0, 500)
            if zone_rates is None or len(zone_rates) < 3:
                continue

            zone_times_list = []
            zone_high_list = []
            zone_low_list = []
            for j in range(1, len(zone_rates)):
                zone_times_list.append(int(zone_rates[j]['time']))
                zone_high_list.append(zone_rates[j-1]['high'])
                zone_low_list.append(zone_rates[j-1]['low'])

            Logger.info(f"[ZoneSetup] {zt} scanning candles {lookback_start}..{n-2}")

            for sig_i in range(lookback_start, n - 1):
                t = chart_times[sig_i]
                idx = bisect.bisect_right(zone_times_list, t) - 1
                if idx < 0:
                    continue

                zone_high = zone_high_list[idx]
                zone_low = zone_low_list[idx]

                min_pen = pip

                o = opens_arr[sig_i]
                h = highs_arr[sig_i]
                lo = lows_arr[sig_i]
                c = closes[sig_i]

                pen_up = h - zone_high
                pen_down = zone_low - lo
                touch_high = h >= zone_high
                touch_low = lo <= zone_low
                fb_both = pen_up >= min_pen and pen_down >= min_pen

                is_long = False
                is_short = False
                signal_type = ""

                if fb_both:
                    if c >= zone_low:
                        is_long = True
                        signal_type = "Fake Break"
                        zone_level = zone_low
                    elif c <= zone_high:
                        is_short = True
                        signal_type = "Fake Break"
                        zone_level = zone_high
                elif touch_low and not touch_high:
                    if c > zone_low:
                        is_long = True
                        signal_type = "Rejection"
                        zone_level = zone_low
                elif touch_high and not touch_low:
                    if c < zone_high:
                        is_short = True
                        signal_type = "Rejection"
                        zone_level = zone_high

                if not is_long and not is_short:
                    continue

                if signal_type == "Fake Break":
                    conf_i = sig_i + 1
                    if conf_i >= n:
                        continue
                    next_o = opens_arr[conf_i]
                    next_c = closes[conf_i]
                    next_h = highs_arr[conf_i]
                    next_lo = lows_arr[conf_i]
                    if is_long:
                        next_confirmed = next_c > next_o
                    else:
                        next_confirmed = next_c < next_o
                    if not next_confirmed:
                        continue
                    arrow_idx = conf_i
                    arrow_o = next_o
                    arrow_h = next_h
                    arrow_lo = next_lo
                    arrow_c = next_c
                else:
                    conf_i = sig_i + 1
                    if conf_i >= n:
                        continue
                    next_c = closes[conf_i]
                    next_o = opens_arr[conf_i]
                    next_h = highs_arr[conf_i]
                    next_lo = lows_arr[conf_i]
                    if is_long:
                        next_confirmed = next_c > h
                    else:
                        next_confirmed = next_c < lo
                    if not next_confirmed:
                        continue
                    arrow_idx = conf_i
                    arrow_o = next_o
                    arrow_h = next_h
                    arrow_lo = next_lo
                    arrow_c = next_c

                entry = arrow_c
                if is_long:
                    sl = zone_level - atr_val * atr_sl_mult
                    tp = entry + (entry - sl) * rr_val
                else:
                    sl = zone_level + atr_val * atr_sl_mult
                    tp = entry - (sl - entry) * rr_val

                Logger.info(f"[ZoneSetup] {zt} {signal_type} {'LONG' if is_long else 'SHORT'} @idx={arrow_idx} fb@idx={sig_i} (level={zone_level:.5f})")

                last_signal = (arrow_idx, is_long, signal_type, zt, zone_level, arrow_o, arrow_h, arrow_lo, arrow_c, risk_pct, rr_val, atr_sl_mult, use_exit)

                if signal_type == "Fake Break":
                    sig_i = conf_i

        if last_signal:
            sig_i, is_long, signal_type, zt, zone_level, o, h, lo, c, risk_pct, rr_val, atr_sl_mult, use_exit = last_signal
            entry = c
            if is_long:
                sl = zone_level - atr_val * atr_sl_mult
                tp = entry + (entry - sl) * rr_val
            else:
                sl = zone_level + atr_val * atr_sl_mult
                tp = entry - (sl - entry) * rr_val
            actual_rr = abs(tp - entry) / abs(entry - sl) if abs(entry - sl) > 0 else 0

            dir_color = "#9ece6a" if is_long else "#f7768e"
            sp.zone_dir_title.setText(f"{'LONG' if is_long else 'SHORT'} {signal_type} - {zt} Zone")
            sp.zone_dir_title.setStyleSheet(f"color:{dir_color};font-size:10px;font-weight:bold;padding:2px 4px")

            exit_tag = " | Exit:Adv" if use_exit else ""
            info_text = (
                f"Zone: {zt} ({zone_level:.5f})\n"
                f"Entry: {entry:.5f} | SL: {sl:.5f} | TP: {tp:.5f}\n"
                f"RR: {actual_rr:.1f} | Risk: {risk_pct}% | ATR SL: {atr_sl_mult}x{exit_tag}"
            )
            sp.zone_trade_info.setText(info_text)
            sp.zone_trade_info.setStyleSheet("color:#7aa2f7;font-size:9px;font-weight:bold;padding:4px 2px")
            sp.zone_checklist.repaint()

            if sp.auto_live_cb.isChecked():
                sig_key = f"{cw.current_symbol}_{zt}_{'L' if is_long else 'S'}_{sig_i}"
                if sig_key not in sp._zone_last_signal:
                    sp._zone_last_signal[sig_key] = True
                    side = "buy" if is_long else "sell"
                    max_pos = sp.max_positions.value()
                    max_sym = sp.max_per_symbol.value()
                    all_pos = mt5.positions_get()
                    total_pos = len(all_pos) if all_pos else 0
                    sym_pos = cw._count_symbol_positions(cw.current_symbol)
                    can_trade = True
                    if max_pos > 0 and total_pos >= max_pos:
                        can_trade = False
                    if max_sym > 0 and sym_pos >= max_sym:
                        can_trade = False
                    if can_trade:
                        lot = cw._calc_setup_lot(entry, sl, sp)
                        digits = info.digits
                        sl_n = round(sl, digits)
                        tp_n = round(tp, digits)
                        result, msg = cw.executor.send_market(cw.current_symbol, side, lot, sl_n, tp_n, comment="ZoneSetup")
                        if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                            Logger.info(f"[ZoneSetup] TRADE OPENED: {side.upper()} {lot} lots @ {result.price:.{digits}f}")
                            sp.zone_trade_info.setText(f"{info_text}\nTRADE OPENED: {side.upper()} {lot} lots @ {result.price:.{digits}f}")
                            sp.zone_trade_info.setStyleSheet("color:#9ece6a;font-size:9px;font-weight:bold;padding:4px 2px")
                        else:
                            Logger.info(f"[ZoneSetup] TRADE FAILED: {msg}")
        else:
            sp.zone_dir_title.setText("No Zone Signal Detected")
            sp.zone_dir_title.setStyleSheet("color:#565f89;font-size:10px;font-weight:bold;padding:2px 4px")
            sp.zone_trade_info.setText("Waiting for zone touch...")

    def on_risk_mode_changed(self, idx):
        modes = ["% Balance", "$ Fixed", "Fixed Lot"]
        mode = modes[idx]
        if mode == "% Balance":
            self.lbl_risk_value.setText("Risk % of Balance:")
            self.risk_input.setDecimals(2)
            self.risk_input.setRange(0.01, 100)
            self.risk_input.setSuffix(" %")
            self.risk_input.setValue(1.0)
        elif mode == "$ Fixed":
            self.lbl_risk_value.setText("Risk Amount ($):")
            self.risk_input.setDecimals(0)
            self.risk_input.setRange(1, 100000)
            self.risk_input.setSuffix(" $")
            self.risk_input.setValue(10)
        else:
            self.lbl_risk_value.setText("Lot Size:")
            self.risk_input.setDecimals(2)
            self.risk_input.setRange(0.01, 1000)
            self.risk_input.setSuffix(" Lots")
            self.risk_input.setValue(0.01)

    def save_settings(self):
        try:
            config = {}
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    config = json.load(f)
            cw = self.window().findChild(ChartWidget) if self.window() else None
            old_settings = config.get("settings", {})
            config["settings"] = {
                "last_symbol": cw.current_symbol if cw else old_settings.get("last_symbol", "EURUSD"),
                "last_tf": cw.current_tf if cw else old_settings.get("last_tf", "H1"),
                "risk_mode": self.risk_combo.currentIndex(),
                "risk_value": self.risk_input.value(),
                "rr": self.rr_input.value(),
                "exit_master": self.exit_master.isChecked(),
                "trail_algoman": self.trail_algoman_cb.isChecked(),
                "trail_algoman_act": self.trail_algoman_act.currentText(),
                "trail_atr_mult": self.trail_atr_mult.value(),
                "be_cb": self.be_cb.isChecked(),
                "be_act": self.be_act.currentText(),
                "be_lock": self.be_lock.currentText(),
                "tp_levels_cb": self.tp_levels_cb.isChecked(),
                "tp_levels_edit": self.tp_levels_edit.text(),
                "time_cb": self.time_cb.isChecked(),
                "time_min": self.time_min.value(),
                "ichimoku_enabled": self.ichimoku_cb.isChecked(),
                "ichimoku_cfg": self.ichimoku_cfg,
                "ma_enabled": self.ma_cb.isChecked(),
                "ma_cfg": self.ma_cfg,
                "week_hl_enabled": self.week_hl_cb.isChecked(),
                "day_hl_enabled": self.day_hl_cb.isChecked(),
                "h4_hl_enabled": self.h4_hl_cb.isChecked(),
                "h1_hl_enabled": self.h1_hl_cb.isChecked(),
                "open_day_enabled": self.open_day_cb.isChecked(),
                "yesterday_candle_enabled": self.yesterday_candle_cb.isChecked(),
                "zone_setup_enabled": self.zone_setup_cb.isChecked(),
                "zone_setup_cfg": self.zone_setup_cfg,
                "algoman_enabled": self.algoman_cb.isChecked(),
                "algoman_cfg": self.algoman_cfg,
                "vwap_enabled": self.vwap_cb.isChecked(),
                "vwap_cfg": self.vwap_cfg,
                "session_break_enabled": self.session_break_cb.isChecked(),
                "session_break_cfg": self.session_break_cfg,
                "scan_speed": self.scan_speed.value(),
                "ms_scan_enabled": self.ms_scan_cb.isChecked(),
                "ms_scan_tf": self.ms_scan_tf.currentText(),
                "ms_scan_cfg": self.ms_scan_cfg,
                "max_positions": self.max_positions.value(),
                "max_per_symbol": self.max_per_symbol.value(),
                "auto_live_trade": self.auto_live_cb.isChecked(),
            }
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            Logger.error(f"Error saving settings: {e}")

    def load_settings(self):
        try:
            if not os.path.exists(self.config_path):
                return
            with open(self.config_path, "r") as f:
                config = json.load(f)
            s = config.get("settings", {})
            if not s:
                return
            self.risk_combo.setCurrentIndex(s.get("risk_mode", 0))
            self.risk_input.setValue(s.get("risk_value", 1.0))
            self.rr_input.setValue(s.get("rr", 2.0))
            self.exit_master.setChecked(s.get("exit_master", False))
            self.trail_algoman_cb.setChecked(s.get("trail_algoman", False))
            act_text = s.get("trail_algoman_act", "50%")
            idx = self.trail_algoman_act.findText(act_text)
            if idx >= 0:
                self.trail_algoman_act.setCurrentIndex(idx)
            self.trail_atr_mult.setValue(s.get("trail_atr_mult", 0.5))
            self.be_cb.setChecked(s.get("be_cb", False))
            be_act_text = s.get("be_act", "100%")
            idx = self.be_act.findText(str(be_act_text))
            if idx >= 0:
                self.be_act.setCurrentIndex(idx)
            be_lock_text = s.get("be_lock", "100%")
            idx = self.be_lock.findText(str(be_lock_text))
            if idx >= 0:
                self.be_lock.setCurrentIndex(idx)
            self.tp_levels_cb.setChecked(s.get("tp_levels_cb", False))
            self.tp_levels_edit.setText(s.get("tp_levels_edit", "1.0:25, 2.0:25, 3.0:50"))
            self.time_cb.setChecked(s.get("time_cb", False))
            self.time_min.setValue(s.get("time_min", 60))
            self.ichimoku_cb.setChecked(s.get("ichimoku_enabled", False))
            self.ichimoku_cfg = s.get("ichimoku_cfg", {})
            self.ma_cb.setChecked(s.get("ma_enabled", False))
            self.ma_cfg = s.get("ma_cfg", {})
            self.week_hl_cb.setChecked(s.get("week_hl_enabled", False))
            self.day_hl_cb.setChecked(s.get("day_hl_enabled", False))
            self.h4_hl_cb.setChecked(s.get("h4_hl_enabled", False))
            self.h1_hl_cb.setChecked(s.get("h1_hl_enabled", False))
            self.open_day_cb.setChecked(s.get("open_day_enabled", False))
            self.yesterday_candle_cb.setChecked(s.get("yesterday_candle_enabled", False))
            self.zone_setup_cb.setChecked(s.get("zone_setup_enabled", False))
            self.zone_setup_cfg = s.get("zone_setup_cfg", {})
            self._update_zone_setup_status()
            self.algoman_cb.setChecked(s.get("algoman_enabled", False))
            if "algoman_cfg" in s:
                self.algoman_cfg = s["algoman_cfg"]
            self.vwap_cb.setChecked(s.get("vwap_enabled", False))
            if "vwap_cfg" in s:
                self.vwap_cfg.update(s["vwap_cfg"])
            self.session_break_cb.setChecked(s.get("session_break_enabled", False))
            if "session_break_cfg" in s:
                self.session_break_cfg = s["session_break_cfg"]
            self.scan_speed.setValue(s.get("scan_speed", 5))
            self.ms_scan_cb.setChecked(s.get("ms_scan_enabled", False))
            self.ms_scan_tf.setCurrentText(s.get("ms_scan_tf", "M15"))
            if "ms_scan_cfg" in s:
                self.ms_scan_cfg = s["ms_scan_cfg"]
            self.max_positions.setValue(s.get("max_positions", 5))
            self.max_per_symbol.setValue(s.get("max_per_symbol", 2))
            self.auto_live_cb.setChecked(s.get("auto_live_trade", False))
        except Exception as e:
            Logger.error(f"Error loading settings: {e}")

    def get_exit_config(self):
        levels = []
        for part in self.tp_levels_edit.text().split(","):
            part = part.strip()
            if ":" in part:
                r, v = part.split(":")
                levels.append({"ratio": float(r.strip()), "volume_pct": float(v.strip())})
        if not levels:
            levels = [{"ratio": 1.0, "volume_pct": 25}, {"ratio": 2.0, "volume_pct": 25}, {"ratio": 3.0, "volume_pct": 50}]
        return {
            "enabled": self.exit_master.isChecked(),
            "trail_use_algoman": self.trail_algoman_cb.isChecked(),
            "trail_algoman_act": self.trail_algoman_act.currentText(),
            "trail_atr_mult": self.trail_atr_mult.value(),
            "be_enabled": self.be_cb.isChecked(),
            "be_tp_pct": float(self.be_act.currentText().replace("%", "")) / 100.0,
            "be_sl_pct": float(self.be_lock.currentText().replace("%", "")) / 100.0,
            "tp_levels_enabled": self.tp_levels_cb.isChecked(),
            "tp_levels": levels,
            "time_exit_enabled": self.time_cb.isChecked(),
            "time_exit_minutes": self.time_min.value(),
        }

# ============================================================
#               پنل واچ لیست (سمت راست)
# ============================================================

class WatchlistPanel(QFrame):
    STAR_COLORS = [
        ("", "بدون رنگ"),
        ("#ffdd57", "زرد"),
        ("#ff5555", "قرمز"),
        ("#50fa7b", "سبز"),
        ("#ffb86c", "نارنجی"),
        ("#bd93f9", "بنفش"),
        ("#8be9fd", "آبی روشن"),
        ("#7aa2f7", "آبی"),
        ("#f7768e", "صورتی"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(200)
        self.all_symbols = []
        self.star_colors = {}
        self._signal_star_overrides = {}
        self.config_path = "config.json"
        self._color_popup = None

        self.setup_ui()
        self.load_star_colors()
        self.refresh_symbols()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        title = QLabel("\u2B50  Watchlist")
        title.setObjectName("section_title")
        title.setCursor(Qt.PointingHandCursor)
        title.mousePressEvent = lambda e: self._reset_all_stars()
        layout.addWidget(title)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Symbol...")
        self.search_input.textChanged.connect(self.filter_symbols)
        self.btn_refresh_wl = QPushButton("🔄")
        self.btn_refresh_wl.setFixedWidth(30)
        self.btn_refresh_wl.clicked.connect(self.refresh_symbols)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.btn_refresh_wl)
        layout.addLayout(search_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["\u2605", "Symbol", "Bid"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        self.table.setColumnWidth(0, 18)
        self.table.setColumnWidth(2, 65)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.cellClicked.connect(self.on_cell_clicked)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)
        self.table.setShowGrid(False)
        self.table.setSortingEnabled(False)
        self.table.verticalHeader().setDefaultSectionSize(22)
        self.table.setStyleSheet("""
            QTableWidget { font-size: 11px; color: #e0e0ff; background: #0a0a1a; gridline-color: #1e2030; font-weight: bold; }
            QTableWidget::item { padding: 1px 2px; }
            QHeaderView::section { font-size: 10px; padding: 2px; color: #ffffff; background: #1a1b2e; font-weight: bold; }
        """)

        layout.addWidget(self.table, stretch=1)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._sync_and_update)
        self.update_timer.start(1000)

    def _sync_and_update(self):
        self._sync_market_watch()
        self.update_prices()

    def _sync_market_watch(self):
        if not MT5Connector.is_connected():
            return
        try:
            import MetaTrader5 as mt5
            all_syms = mt5.symbols_get() or []
            current = [s.name for s in all_syms if s.visible and not s.name.startswith('.')]
            if set(current) != set(self.all_symbols):
                self.all_symbols = current
                self.all_symbols.sort(key=lambda x: (x not in self.star_colors, x))
                self.filter_symbols()
        except Exception:
            pass

    def update_prices(self):
        if not MT5Connector.is_connected():
            return
        for row in range(self.table.rowCount()):
            sym = self.table.item(row, 1)
            if sym is None:
                continue
            symbol_name = sym.text()
            tick = MT5Connector.get_symbol_tick(symbol_name)
            if tick is None:
                continue

            bid = tick.bid
            ask = tick.ask

            bid_item = self.table.item(row, 2)
            if bid_item:
                bid_item.setText(f"{bid:.5f}" if bid < 100 else f"{bid:.2f}")
                bid_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

    def refresh_symbols(self):
        if not MT5Connector.is_connected():
            return
        try:
            import MetaTrader5 as mt5
            all_syms = mt5.symbols_get() or []
            self.all_symbols = [s.name for s in all_syms if s.visible and not s.name.startswith('.')]
        except Exception:
            self.all_symbols = []
        self.all_symbols.sort(key=lambda x: (x not in self.star_colors, x))
        self.filter_symbols()

    def display_symbols(self, symbols):
        self.table.setRowCount(len(symbols))
        for i, symbol in enumerate(symbols):
            tick = MT5Connector.get_symbol_tick(symbol)
            bid = tick.bid if tick else 0

            color_idx = self.star_colors.get(symbol, 0)
            star_color = self.STAR_COLORS[color_idx][0]

            fav_item = QTableWidgetItem("\u2605" if color_idx > 0 else "\u2606")
            fav_item.setData(Qt.UserRole, symbol)
            fav_item.setData(Qt.UserRole + 1, color_idx)
            fav_item.setTextAlignment(Qt.AlignCenter)
            if star_color:
                fav_item.setForeground(QBrush(QColor(star_color)))
            else:
                fav_item.setForeground(QBrush(QColor("#33467c")))
            self.table.setItem(i, 0, fav_item)

            sym_item = QTableWidgetItem(symbol)
            sym_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            sym_item.setForeground(QBrush(QColor("#ffffff")))
            self.table.setItem(i, 1, sym_item)

            bid_item = QTableWidgetItem(f"{bid:.5f}" if bid < 100 else f"{bid:.2f}")
            bid_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            bid_item.setForeground(QBrush(QColor("#ffffff")))
            self.table.setItem(i, 2, bid_item)

    def filter_symbols(self):
        search = self.search_input.text().strip().upper()
        if search:
            display = [s for s in self.all_symbols if search in s.upper()]
        else:
            display = self.all_symbols
        self.display_symbols(display)

    def on_cell_clicked(self, row, col):
        item = self.table.item(row, 0)
        if item is None:
            return
        symbol = item.data(Qt.UserRole)
        if col == 0:
            self._show_color_popup(symbol, item)

    def _show_color_popup(self, symbol, star_item):
        if self._color_popup is not None:
            self._color_popup.close()

        popup = QFrame(self, QtCore.Qt.Popup)
        popup.setStyleSheet("QFrame { background: #1a1b2e; border: 1px solid #33467c; border-radius: 6px; }")
        gl = QGridLayout(popup)
        gl.setContentsMargins(6, 6, 6, 6)
        gl.setSpacing(3)

        lbl = QLabel(f"{symbol}")
        lbl.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 11px; padding: 2px;")
        gl.addWidget(lbl, 0, 0, 1, 3)

        cur_idx = star_item.data(Qt.UserRole + 1) or 0
        for idx, (hex_color, name) in enumerate(self.STAR_COLORS):
            btn = QPushButton()
            btn.setFixedSize(28, 28)
            if hex_color:
                btn.setStyleSheet(
                    f"QPushButton {{ background: {hex_color}; border: 2px solid {'#ffffff' if idx == cur_idx else '#33467c'}; border-radius: 4px; }}"
                    f"QPushButton:hover {{ border: 2px solid #ffffff; }}"
                )
            else:
                btn.setStyleSheet(
                    f"QPushButton {{ background: #0a0a1a; border: 2px solid {'#ffffff' if idx == cur_idx else '#33467c'}; border-radius: 4px; }}"
                    f"QPushButton:hover {{ border: 2px solid #ffffff; }}"
                )
            btn.clicked.connect(lambda checked, i=idx, s=symbol, si=star_item, p=popup: self._apply_star_color(i, s, si, p))
            r, c = 1 + idx // 3, idx % 3
            gl.addWidget(btn, r, c)

        pos = self.table.viewport().mapToGlobal(self.table.visualItemRect(star_item).center())
        popup.move(pos.x() - 50, pos.y() + 15)
        popup.show()
        self._color_popup = popup

    def _apply_star_color(self, idx, symbol, star_item, popup):
        star_item.setData(Qt.UserRole + 1, idx)
        hex_color = self.STAR_COLORS[idx][0]
        star_item.setText("\u2605" if idx > 0 else "\u2606")
        if hex_color:
            star_item.setForeground(QBrush(QColor(hex_color)))
        else:
            star_item.setForeground(QBrush(QColor("#33467c")))
        if idx > 0:
            self.star_colors[symbol] = idx
        else:
            self.star_colors.pop(symbol, None)
        self.save_star_colors()
        popup.close()

    def set_signal_color(self, symbol, direction):
        if symbol not in self._signal_star_overrides:
            self._signal_star_overrides[symbol] = self.star_colors.get(symbol, 0)
        color_idx = 3 if direction == "buy" else 2
        self.star_colors[symbol] = color_idx
        self.save_star_colors()
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and item.data(Qt.UserRole) == symbol:
                hex_color = self.STAR_COLORS[color_idx][0]
                item.setText("\u2605")
                item.setData(Qt.UserRole + 1, color_idx)
                if hex_color:
                    item.setForeground(QBrush(QColor(hex_color)))
                break

    def reset_signal_stars(self):
        for symbol, orig_idx in self._signal_star_overrides.items():
            if orig_idx == 0:
                self.star_colors.pop(symbol, None)
            else:
                self.star_colors[symbol] = orig_idx
            for row in range(self.table.rowCount()):
                item = self.table.item(row, 0)
                if item and item.data(Qt.UserRole) == symbol:
                    hex_color = self.STAR_COLORS[orig_idx][0]
                    item.setText("\u2605" if orig_idx > 0 else "\u2606")
                    item.setData(Qt.UserRole + 1, orig_idx)
                    if hex_color:
                        item.setForeground(QBrush(QColor(hex_color)))
                    else:
                        item.setForeground(QBrush(QColor("#33467c")))
                    break
        self._signal_star_overrides.clear()
        self.save_star_colors()

    def _reset_all_stars(self):
        self.star_colors.clear()
        self._signal_star_overrides.clear()
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item:
                item.setText("\u2606")
                item.setData(Qt.UserRole + 1, 0)
                item.setForeground(QBrush(QColor("#33467c")))
        self.save_star_colors()

    def on_cell_double_clicked(self, row, col):
        item = self.table.item(row, 1)
        if item is None:
            return
        symbol = item.text()
        Logger.info(f"تغییر نماد چارت به {symbol}")
        parent = self.parent()
        while parent and not hasattr(parent, "chart_widget"):
            parent = parent.parent()
        if parent and hasattr(parent, "chart_widget"):
            parent.chart_widget.set_symbol(symbol)

    def highlight_symbol(self, symbol):
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)
            if item and item.text() == symbol:
                self.table.selectRow(row)
                self.table.scrollToItem(item)
                break

    def load_star_colors(self):
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)
                self.star_colors = config.get("star_colors", {})
        except Exception:
            self.star_colors = {}

    def save_star_colors(self):
        try:
            config = {}
            try:
                with open(self.config_path, "r") as f:
                    config = json.load(f)
            except Exception:
                pass
            config["star_colors"] = self.star_colors
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=2)
        except Exception:
            pass

# ============================================================
#              پنل پوزیشن‌ها و اوردرها
# ============================================================

class PositionsPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._cards = []
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        # top summary bar
        top = QHBoxLayout()
        title = QLabel("Positions")
        title.setStyleSheet("color:#9ece6a;font-weight:bold;font-size:12px")
        self.total_lbl = QLabel("P/L: $0.00")
        self.total_lbl.setStyleSheet("color:#7aa2f7;font-weight:bold;font-size:11px")
        self.count_lbl = QLabel("0 positions")
        self.count_lbl.setStyleSheet("color:#7aa2f7;font-size:10px")
        self.btn_close_all = QPushButton("Close All")
        self.btn_close_all.setFixedHeight(28)
        self.btn_close_all.setStyleSheet("QPushButton{background:#f7768e;color:#0a0a1a;border:none;border-radius:8px;font-weight:bold;font-size:10px;padding:4px 10px} QPushButton:hover{background:#ffaa5c}")
        self.btn_close_all.clicked.connect(self.close_all)
        self.btn_close_profit = QPushButton("Close Profit")
        self.btn_close_profit.setFixedHeight(28)
        self.btn_close_profit.setStyleSheet("QPushButton{background:#9ece6a;color:#0a0a1a;border:none;border-radius:8px;font-weight:bold;font-size:10px;padding:4px 10px} QPushButton:hover{background:#b8eab3}")
        self.btn_close_profit.clicked.connect(self.close_profit)
        self.btn_close_loss = QPushButton("Close Loss")
        self.btn_close_loss.setFixedHeight(28)
        self.btn_close_loss.setStyleSheet("QPushButton{background:#e0af68;color:#0a0a1a;border:none;border-radius:8px;font-weight:bold;font-size:10px;padding:4px 10px} QPushButton:hover{background:#ffaa5c}")
        self.btn_close_loss.clicked.connect(self.close_loss)
        self.btn_refresh = QPushButton("\U0001f504")
        self.btn_refresh.setFixedSize(24, 24)
        self.btn_refresh.setStyleSheet("QPushButton{background:#1a1b26;color:#c0caf5;border:1.5px solid #292e42;border-radius:6px;font-size:12px} QPushButton:hover{background:#292e42}")
        self.btn_refresh.clicked.connect(self.refresh)
        top.addWidget(title)
        top.addSpacing(10)
        top.addWidget(self.count_lbl)
        top.addSpacing(10)
        top.addWidget(self.total_lbl)
        top.addStretch()
        top.addWidget(self.btn_close_all)
        top.addWidget(self.btn_close_profit)
        top.addWidget(self.btn_close_loss)
        top.addWidget(self.btn_refresh)
        layout.addLayout(top)

        # scroll area for cards
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet("QScrollArea{background:transparent;border:none} QScrollBar:vertical{width:6px;background:#0a0a1a} QScrollBar::handle:vertical{background:#292e42;border-radius:3px}")
        self.cards_container = QWidget()
        self.cards_container.setStyleSheet("background:transparent")
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(4)
        self.cards_layout.addStretch()
        self.scroll.setWidget(self.cards_container)
        layout.addWidget(self.scroll)

        self.refresh()

    def refresh(self):
        try:
            executor = MT5Executor()
            positions = executor.get_positions()
        except Exception:
            positions = []

        total_profit = sum(p.profit for p in positions)
        total_color = "#9ece6a" if total_profit >= 0 else "#f7768e"
        self.total_lbl.setText(f"P/L: {total_profit:+.2f} $")
        self.total_lbl.setStyleSheet(f"color:{total_color};font-weight:bold;font-size:11px")
        self.count_lbl.setText(f"{len(positions)} positions")

        # preserve checkbox states
        old_states = {}
        for card_data in self._cards:
            key = card_data["ticket"]
            old_states[key] = {
                "exit": card_data["exit_cb"].isChecked(),
            }

        # clear old cards
        for card_data in self._cards:
            card_data["widget"].deleteLater()
        self._cards.clear()

        # remove old stretch
        count = self.cards_layout.count()
        if count > 0:
            item = self.cards_layout.itemAt(count - 1)
            if item and item.spacerItem():
                self.cards_layout.removeItem(item)

        for p in positions:
            card = self._build_card(p, old_states.get(p.ticket, {}))
            self._cards.append(card)
            self.cards_layout.addWidget(card["widget"])

        self.cards_layout.addStretch()

    def close_all(self):
        self._close_positions(lambda p: True)

    def close_profit(self):
        self._close_positions(lambda p: p.profit >= 0)

    def close_loss(self):
        self._close_positions(lambda p: p.profit < 0)

    def _close_single(self, ticket):
        try:
            executor = MT5Executor()
            result = executor.close_position(ticket)
            if result:
                Logger.success(f"[Positions] #{ticket} closed")
            else:
                Logger.error(f"[Positions] Failed to close #{ticket}")
            self.refresh()
        except Exception as e:
            Logger.error(f"[Positions] close #{ticket} error: {e}")

    def _close_positions(self, filter_fn):
        try:
            executor = MT5Executor()
            positions = executor.get_positions()
            if not positions:
                return
            tickets = [p.ticket for p in positions if filter_fn(p)]
            if not tickets:
                return
            for ticket in tickets:
                executor.close_position(ticket)
            Logger.success(f"Closed {len(tickets)} position(s)")
            self.refresh()
        except Exception as e:
            Logger.error(f"Error closing positions: {e}")

    def _build_card(self, pos, old):
        ticket = pos.ticket
        type_str = "BUY" if pos.type == 0 else "SELL"
        type_color = "#9ece6a" if pos.type == 0 else "#f7768e"
        profit = pos.profit
        profit_color = "#9ece6a" if profit >= 0 else "#f7768e"

        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: #0a0a1a;
                border: 1px solid #1e2030;
                border-radius: 6px;
                padding: 4px;
            }}
        """)

        main_v = QVBoxLayout(card)
        main_v.setContentsMargins(8, 6, 8, 6)
        main_v.setSpacing(3)

        # row 1: symbol, type, volume, profit
        r1 = QHBoxLayout()
        r1.setSpacing(6)
        sym_lbl = QLabel(f"<b>{pos.symbol}</b>")
        sym_lbl.setStyleSheet("color:#c0caf5;font-size:11px")
        type_lbl = QLabel(type_str)
        type_lbl.setStyleSheet(f"color:{type_color};font-weight:bold;font-size:10px")
        vol_lbl = QLabel(f"{pos.volume:.2f}")
        vol_lbl.setStyleSheet("color:#7aa2f7;font-size:10px")
        ticket_lbl = QLabel(f"#{ticket}")
        ticket_lbl.setStyleSheet("color:#33467c;font-size:8px")
        profit_lbl = QLabel(f"{profit:+.2f} $")
        profit_lbl.setStyleSheet(f"color:{profit_color};font-weight:bold;font-size:11px")
        r1.addWidget(sym_lbl)
        r1.addWidget(type_lbl)
        r1.addWidget(vol_lbl)
        r1.addWidget(ticket_lbl)
        r1.addStretch()
        r1.addWidget(profit_lbl)
        main_v.addLayout(r1)

        # row 2: open, current, SL, TP
        r2 = QHBoxLayout()
        r2.setSpacing(8)
        for label, value in [("Open", f"{pos.price_open:.5f}"),
                             ("Current", f"{pos.price_current:.5f}"),
                             ("SL", f"{pos.sl:.5f}" if pos.sl else "-"),
                             ("TP", f"{pos.tp:.5f}" if pos.tp else "-")]:
            lbl_text = QLabel(f"<span style='color:#33467c;font-size:8px'>{label}</span> "
                              f"<span style='color:#c0caf5;font-size:10px'>{value}</span>")
            r2.addWidget(lbl_text)
        r2.addStretch()
        main_v.addLayout(r2)

        # row 3: checkboxes + close button
        r3 = QHBoxLayout()
        r3.setSpacing(12)
        exit_cb = QCheckBox("Exit")
        if "exit" in old:
            exit_cb.setChecked(old["exit"])
        else:
            mw = self.window()
            exit_disabled = True
            if mw and hasattr(mw, 'strategy_panel'):
                sp = mw.strategy_panel
                if hasattr(sp, 'exit_mgr') and sp.exit_mgr:
                    if ticket in sp.exit_mgr._exit_disabled_tickets:
                        exit_disabled = True
            exit_cb.setChecked(not exit_disabled)
        exit_cb.setStyleSheet("color:#e0af68;font-size:8px")

        def _on_exit_cb_changed(state, tk=ticket):
            mw = self.window()
            if mw and hasattr(mw, 'strategy_panel'):
                sp = mw.strategy_panel
                if hasattr(sp, 'exit_mgr') and sp.exit_mgr:
                    if state == Qt.Checked:
                        sp.exit_mgr._exit_disabled_tickets.discard(tk)
                        Logger.info(f"[ExitMgr] Exit enabled for ticket #{tk}")
                    else:
                        sp.exit_mgr._exit_disabled_tickets.add(tk)
                        Logger.info(f"[ExitMgr] Exit disabled for ticket #{tk}")
        exit_cb.stateChanged.connect(_on_exit_cb_changed)
        btn_close = QPushButton("Close")
        btn_close.setFixedSize(50, 22)
        btn_close.setStyleSheet("QPushButton{background:#3d1515;color:#f7768e;border:1px solid #f7768e;border-radius:4px;font-size:8px;font-weight:bold} QPushButton:hover{background:#8b2a2a}")
        btn_close.clicked.connect(lambda checked=False, tk=ticket: self._close_single(tk))
        r3.addWidget(exit_cb)
        r3.addStretch()
        r3.addWidget(btn_close)
        main_v.addLayout(r3)

        return {"ticket": ticket, "widget": card, "exit_cb": exit_cb}

class OrdersPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        header = QHBoxLayout()
        title = QLabel("📋 Orders")
        title.setStyleSheet("color:#e0af68;font-weight:bold;font-size:12px")
        self.btn_refresh = QPushButton("\U0001f504")
        self.btn_refresh.setFixedSize(24, 24)
        self.btn_refresh.setStyleSheet("QPushButton{background:#1a1b26;color:#c0caf5;border:1.5px solid #292e42;border-radius:6px;font-size:12px} QPushButton:hover{background:#292e42}")
        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_cancel_all = QPushButton("Cancel All")
        self.btn_cancel_all.setFixedHeight(24)
        self.btn_cancel_all.setStyleSheet("QPushButton{background:#3d1515;color:#f7768e;border:1px solid rgba(247,118,142,0.3);border-radius:8px;font-size:10px;font-weight:bold;padding:2px 8px} QPushButton:hover{background:#5a1a1a}")
        self.btn_cancel_all.clicked.connect(self.cancel_all)
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.btn_cancel_all)
        header.addWidget(self.btn_refresh)
        layout.addLayout(header)

        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(["Ticket", "Symbol", "Type", "Volume", "Price", "SL", "TP", "Status", "Time", "Cancel"])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setColumnWidth(0, 70)
        self.table.setColumnWidth(9, 60)
        self.table.setStyleSheet("""
            QTableWidget{background:#0a0a1a;color:#c0caf5;border:none;font-size:10px;gridline-color:#1e2030}
            QHeaderView::section{background:#16161e;color:#7aa2f7;border:1px solid #1e2030;padding:4px;font-size:10px}
            QTableWidget::item:selected{background:#292e42}
            QPushButton{background:#45213a;color:#f7768e;border:1px solid #f7768e;border-radius:4px;font-size:8px;font-weight:bold}
            QPushButton:hover{background:#6b2d4a}
        """)
        layout.addWidget(self.table)

        self.refresh()

    def _send_cancel(self, ticket):
        try:
            req = {"action": mt5.TRADE_ACTION_REMOVE, "order": ticket}
            result = mt5.order_send(req)
            if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                Logger.success(f"[OrdersPanel] Order #{ticket} canceled")
                return True
            else:
                err = result.comment if result else "No response"
                Logger.error(f"[OrdersPanel] Failed to cancel #{ticket}: {err}")
                return False
        except Exception as e:
            Logger.error(f"[OrdersPanel] cancel #{ticket} error: {e}")
            return False

    def cancel_all(self):
        try:
            result = mt5.orders_get()
            if not result:
                Logger.warning("[OrdersPanel] No orders to cancel")
                return
            orders = list(result)
            Logger.info(f"[OrdersPanel] Canceling all {len(orders)} orders...")
            count = 0
            for o in orders:
                if self._send_cancel(o.ticket):
                    count += 1
            Logger.info(f"[OrdersPanel] Canceled {count}/{len(orders)} orders")
        except Exception as e:
            Logger.error(f"[OrdersPanel] cancel_all error: {e}")
        self.refresh()

    def refresh(self):
        try:
            if not mt5.terminal_info():
                Logger.warning("[OrdersPanel] MT5 not connected")
                self.table.setRowCount(0)
                return

            result = mt5.orders_get()

            if result is None:
                err = mt5.last_error()
                Logger.warning(f"[OrdersPanel] orders_get returned None, error: {err}")
                self.table.setRowCount(0)
                return

            try:
                orders = list(result)
            except Exception as e:
                Logger.error(f"[OrdersPanel] Cannot convert result to list: {e}")
                self.table.setRowCount(0)
                return

            self.table.setRowCount(len(orders))
            order_types = {
                0: "BUY LMT", 1: "SELL LMT", 2: "BUY STP", 3: "SELL STP",
                6: "BUY STPLMT", 7: "SELL STPLMT",
            }
            status_map = {0: "Started", 1: "Placed", 2: "Canceled", 3: "PartFilled", 4: "Filled", 5: "Rejected"}
            for i, o in enumerate(orders):
                try:
                    ticket_val = getattr(o, 'ticket', getattr(o, 'order', 0))
                    ts = o.time_setup
                    if isinstance(ts, (int, float)):
                        t = datetime.datetime.fromtimestamp(ts).strftime("%m-%d %H:%M")
                    elif hasattr(ts, 'strftime'):
                        t = ts.strftime("%m-%d %H:%M")
                    else:
                        t = str(ts) if ts else "-"
                    sl_val = getattr(o, 'sl', None)
                    tp_val = getattr(o, 'tp', None)
                    sl_txt = f"{sl_val:.5f}" if sl_val and sl_val > 0 else "-"
                    tp_txt = f"{tp_val:.5f}" if tp_val and tp_val > 0 else "-"
                    vol_val = getattr(o, 'volume_current', getattr(o, 'volume', 0))
                    price_val = getattr(o, 'price_open', 0)
                    otype = order_types.get(o.type, str(o.type))
                    is_buy = "BUY" in otype
                    row_color = "#9ece6a" if is_buy else "#f7768e"
                    ostate = getattr(o, 'state', 0)

                    items = [
                        str(ticket_val),
                        o.symbol,
                        otype,
                        f"{vol_val:.2f}",
                        f"{price_val:.5f}",
                        sl_txt,
                        tp_txt,
                        status_map.get(ostate, str(ostate)),
                        t,
                    ]
                    for j, val in enumerate(items):
                        item = QTableWidgetItem(val)
                        item.setTextAlignment(Qt.AlignCenter)
                        if j == 2:
                            item.setForeground(QtGui.QColor(row_color))
                            font = item.font()
                            font.setBold(True)
                            item.setFont(font)
                        self.table.setItem(i, j, item)

                    btn_cancel = QPushButton("Cancel")
                    btn_cancel.setFixedHeight(22)
                    btn_cancel.setStyleSheet("QPushButton{background:#45213a;color:#f7768e;border:1px solid #f7768e;border-radius:4px;font-size:8px;font-weight:bold} QPushButton:hover{background:#6b2d4a}")
                    btn_cancel.clicked.connect(lambda checked=False, tk=ticket_val: self._on_row_cancel(tk))
                    self.table.setCellWidget(i, 9, btn_cancel)

                except Exception as e2:
                    Logger.error(f"[OrdersPanel] row {i} error: {e2}")

        except Exception as e:
            Logger.error(f"[OrdersPanel] refresh error: {type(e).__name__}: {e}")
            self.table.setRowCount(0)

    def _on_row_cancel(self, ticket):
        self._send_cancel(ticket)
        self.refresh()

    def cancel_selected(self):
        rows = set(idx.row() for idx in self.table.selectedIndexes())
        if not rows:
            Logger.warning("[OrdersPanel] No order selected to cancel")
            return
        for row in rows:
            ticket_item = self.table.item(row, 0)
            if not ticket_item:
                continue
            ticket = int(ticket_item.text())
            self._send_cancel(ticket)
        self.refresh()

# ============================================================
#                  پنل لاگ (پایین)
# ============================================================

class LogPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(160)
        self.setup_ui()
        Logger.subscribe(self.add_log)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 4)
        layout.setSpacing(4)

        header = QHBoxLayout()
        title = QLabel("\U0001F4CB  Log")
        title.setObjectName("section_title")
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.clicked.connect(self.clear_log)
        self.btn_save = QPushButton("Save to File")
        self.btn_save.clicked.connect(self.save_log)
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.btn_save)
        header.addWidget(self.btn_clear)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        layout.addLayout(header)
        layout.addWidget(self.log_output)

    def add_log(self, message):
        self.log_output.append(message)
        scrollbar = self.log_output.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def clear_log(self):
        self.log_output.clear()
        Logger.info("Log cleared")

    def save_log(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"log_{timestamp}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.log_output.toPlainText())
            Logger.success(f"Log saved to {filename}")
        except Exception as e:
            Logger.error(f"Error saving log: {e}")

# ============================================================
#                  پنل سیگنال‌ها (پایین)
# ============================================================

class SignalsPanel(QFrame):
    symbol_clicked = QtCore.pyqtSignal(str)
    signals_cleared = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(160)
        self._signal_symbols = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 4)
        layout.setSpacing(4)

        header = QHBoxLayout()
        title = QLabel("Signals")
        title.setObjectName("section_title")
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.clicked.connect(self.clear_signals)
        self.btn_count = QLabel("0")
        self.btn_count.setStyleSheet("color:#7aa2f7;font-size:10px;font-weight:bold;background:transparent;")
        header.addWidget(title)
        header.addWidget(self.btn_count)
        header.addStretch()
        header.addWidget(self.btn_clear)

        self.signals_output = QtWidgets.QListWidget()
        self.signals_output.setAlternatingRowColors(True)
        self.signals_output.setCursor(QtCore.Qt.PointingHandCursor)
        self.signals_output.setStyleSheet("""
            QListWidget{background:#0a0a1a;color:#c0caf5;font-size:11px;border:1px solid #1e2030;border-radius:4px;padding:4px}
            QListWidget::item{padding:4px;border-bottom:1px solid #1e2030}
            QListWidget::item:selected{background:#292e42}
            QListWidget::item:hover{background:#1e2030}
        """)
        self.signals_output.itemDoubleClicked.connect(self._on_double_click)

        layout.addLayout(header)
        layout.addWidget(self.signals_output)
        self._count = 0

    def _on_double_click(self, item):
        row = self.signals_output.row(item)
        if 0 <= row < len(self._signal_symbols):
            symbol = self._signal_symbols[row]
            self.symbol_clicked.emit(symbol)

    def add_signal(self, symbol, direction, price, tf, msg=""):
        arrow = "▲ BUY" if direction == "buy" else "▼ SELL"
        color = "#26a641" if direction == "buy" else "#f5222d"
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        if msg:
            text = f"[{timestamp}] {symbol} {arrow} @ {price:.5f} | {tf} | {msg}"
        else:
            text = f"[{timestamp}] {symbol} {arrow} @ {price:.5f} | {tf}"
        item = QtWidgets.QListWidgetItem(text)
        item.setForeground(QtGui.QColor(color))
        item.setData(QtCore.Qt.UserRole, symbol)
        self.signals_output.addItem(item)
        self._signal_symbols.append(symbol)
        self._count += 1
        self.btn_count.setText(str(self._count))
        self.signals_output.scrollToBottom()

    def clear_signals(self):
        self.signals_output.clear()
        self._signal_symbols.clear()
        self._count = 0
        self.btn_count.setText("0")
        self.signals_cleared.emit()


# ============================================================
#                   پنجره اصلی برنامه
# ============================================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VPTradeBot - MetaTrader 5 Dashboard")
        self.setWindowState(Qt.WindowMaximized)

        self.setup_ui()
        self.setup_connections()
        self._restore_chart_state()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # header
        self.account_panel = AccountInfoPanel()
        main_layout.addWidget(self.account_panel)

        # middle: splitter with left, center, right
        middle_splitter = QSplitter(Qt.Horizontal)

        self.strategy_panel = StrategyPanel()
        self.chart_widget = ChartWidget()
        self.watchlist_panel = WatchlistPanel()

        middle_splitter.addWidget(self.strategy_panel)
        middle_splitter.addWidget(self.chart_widget)
        middle_splitter.addWidget(self.watchlist_panel)
        middle_splitter.setHandleWidth(3)
        middle_splitter.setStretchFactor(0, 0)
        middle_splitter.setStretchFactor(1, 1)
        middle_splitter.setStretchFactor(2, 0)

        # vertical splitter: middle + bottom
        self.main_splitter = QSplitter(Qt.Vertical)
        self.main_splitter.addWidget(middle_splitter)
        self.middle_splitter = middle_splitter

        # bottom tabs: Positions, Orders, Log
        self.bottom_tabs = QTabWidget()
        self.bottom_tabs.setStyleSheet("""
            QTabWidget::pane{border:1px solid #1e2030;background:#0a0a1a}
            QTabBar::tab{background:#16161e;color:#7aa2f7;padding:6px 16px;border:1px solid #1e2030;border-bottom:none;border-top-left-radius:4px;border-top-right-radius:4px;margin-right:2px;font-size:10px}
            QTabBar::tab:selected{background:#0a0a1a;color:#c0caf5;font-weight:bold}
            QTabBar::tab:hover{background:#1e2030}
        """)
        self.positions_panel = PositionsPanel()
        self.orders_panel = OrdersPanel()
        self.log_panel = LogPanel()
        self.signals_panel = SignalsPanel()
        self.bottom_tabs.addTab(self.positions_panel, "Positions")
        self.bottom_tabs.addTab(self.orders_panel, "Orders")
        self.bottom_tabs.addTab(self.signals_panel, "Signals")
        self.bottom_tabs.addTab(self.log_panel, "Log")
        self.main_splitter.addWidget(self.bottom_tabs)
        self.main_splitter.setHandleWidth(3)

        self._load_panel_sizes()
        main_layout.addWidget(self.main_splitter, stretch=1)

        self._multi_scanner = MultiSymbolScanner(self)
        self._multi_scanner.add_callback(self._on_ms_signal)
        self._signal_notify = SignalNotifyWidget(self)
        self.signals_panel.symbol_clicked.connect(self._on_signal_symbol_clicked)
        self.signals_panel.signals_cleared.connect(self.watchlist_panel.reset_signal_stars)
        self._ms_scan_active = False
        self._scan_syncing = False

    def setup_connections(self):
        self.strategy_panel.ms_scan_cb.toggled.connect(self._toggle_multi_scan)
        self._ms_refresh_timer = QTimer()
        self._ms_refresh_timer.timeout.connect(self._refresh_ms_symbols)
        self._ms_refresh_timer.start(15000)
        if self.strategy_panel.ms_scan_cb.isChecked():
            QTimer.singleShot(3000, lambda: self._toggle_multi_scan(True))

    def _restore_chart_state(self):
        try:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    config = json.load(f)
                s = config.get("settings", {})
                last_sym = s.get("last_symbol", "")
                last_tf = s.get("last_tf", "H1")
                if last_sym:
                    self.chart_widget.current_symbol = last_sym
                if last_tf:
                    self.chart_widget.current_tf = last_tf
                    for tf in ["M1", "M2", "M3", "M5", "M10", "M15", "M30", "H1", "H4", "D1"]:
                        btn = getattr(self.chart_widget, f"btn_tf_{tf}", None)
                        if btn:
                            btn.setChecked(tf == last_tf)
                self.chart_widget.load_data()
        except Exception as e:
            Logger.error(f"Failed to restore chart state: {e}")

    def _toggle_multi_scan(self, checked):
        if self._scan_syncing:
            return
        self._scan_syncing = True
        if checked:
            self._start_multi_scan()
        else:
            self._multi_scanner.stop()
            self._ms_scan_active = False
            Logger.info("[SCAN] Multi scan stopped")
        sp = self.strategy_panel
        if sp.ms_scan_cb.isChecked() != checked:
            sp.ms_scan_cb.setChecked(checked)
        self._scan_syncing = False

    def _refresh_ms_symbols(self):
        if not self._ms_scan_active:
            return
        sp = self.strategy_panel
        wl = self.watchlist_panel
        symbols = list(wl.all_symbols) if wl else []
        current = self.chart_widget.current_symbol if self.chart_widget else ""
        scan_symbols = [s for s in symbols if s != current]
        tf = sp.ms_scan_tf.currentText()
        zcfg = sp.zone_setup_cfg if hasattr(sp, 'zone_setup_cfg') else {}
        zcbs = {
            "Weekly": sp.week_hl_cb.isChecked() if hasattr(sp, 'week_hl_cb') else False,
            "Daily": sp.day_hl_cb.isChecked() if hasattr(sp, 'day_hl_cb') else False,
            "H4": sp.h4_hl_cb.isChecked() if hasattr(sp, 'h4_hl_cb') else False,
            "H1": sp.h1_hl_cb.isChecked() if hasattr(sp, 'h1_hl_cb') else False,
        }
        mcfg = sp.ms_scan_cfg if hasattr(sp, 'ms_scan_cfg') else {}
        self._multi_scanner.configure(
            scan_symbols, enabled=True, scan_tf=tf,
            zone_cfg=zcfg, zone_checkboxes=zcbs,
            scan_interval=mcfg.get("scan_interval", 5),
            signal_tfs=mcfg.get("signal_tfs", {"Weekly": True, "Daily": True, "H4": True, "H1": True}),
            chart_tfs=mcfg.get("chart_tfs", {"M15": True}),
            sound_alarm=mcfg.get("sound_alarm", True),
            popup_notify=mcfg.get("popup_notify", True),
        )

    def _start_multi_scan(self):
        sp = self.strategy_panel
        wl = self.watchlist_panel
        symbols = list(wl.all_symbols) if wl else []
        current = self.chart_widget.current_symbol if self.chart_widget else ""
        scan_symbols = [s for s in symbols if s != current]
        tf = sp.ms_scan_tf.currentText()
        zcfg = sp.zone_setup_cfg if hasattr(sp, 'zone_setup_cfg') else {}
        zcbs = {
            "Weekly": sp.week_hl_cb.isChecked() if hasattr(sp, 'week_hl_cb') else False,
            "Daily": sp.day_hl_cb.isChecked() if hasattr(sp, 'day_hl_cb') else False,
            "H4": sp.h4_hl_cb.isChecked() if hasattr(sp, 'h4_hl_cb') else False,
            "H1": sp.h1_hl_cb.isChecked() if hasattr(sp, 'h1_hl_cb') else False,
        }
        mcfg = sp.ms_scan_cfg if hasattr(sp, 'ms_scan_cfg') else {}
        Logger.info(f"[SCAN] Starting: {len(scan_symbols)} symbols, cfg={mcfg}")
        self._multi_scanner.configure(
            scan_symbols, enabled=True, scan_tf=tf,
            zone_cfg=zcfg, zone_checkboxes=zcbs,
            scan_interval=mcfg.get("scan_interval", 5),
            signal_tfs=mcfg.get("signal_tfs", {"Weekly": True, "Daily": True, "H4": True, "H1": True}),
            chart_tfs=mcfg.get("chart_tfs", {"M15": True}),
            sound_alarm=mcfg.get("sound_alarm", True),
            popup_notify=mcfg.get("popup_notify", True),
        )
        self._ms_scan_active = True
        Logger.info(f"[SCAN] Multi-symbol scan started: {len(scan_symbols)} symbols, TF={tf}")

    def _on_ms_signal(self, symbol, direction, price, tf, msg=""):
        try:
            arrow = "▲ BUY" if direction == "buy" else "▼ SELL"
            Logger.info(f"[SCAN] {symbol} {arrow} @ {price:.5f} on {tf} | {msg}")
            self.signals_panel.add_signal(symbol, direction, price, tf, msg)
            if self.watchlist_panel:
                self.watchlist_panel.set_signal_color(symbol, direction)
            popup_on = getattr(self._multi_scanner, '_popup_notify', True)
            if popup_on:
                screen = QtWidgets.QApplication.primaryScreen().geometry()
                self._signal_notify.move(screen.left() + screen.width() - 390, screen.top() + 80)
                self._signal_notify.show_alert(symbol, direction, price, tf, msg)
            sound_on = getattr(self._multi_scanner, '_sound_alarm', True)
            if sound_on:
                try:
                    import threading
                    def _beep():
                        try:
                            import winsound
                            winsound.Beep(1200, 300)
                            winsound.Beep(1600, 300)
                        except Exception:
                            pass
                    threading.Thread(target=_beep, daemon=True).start()
                except Exception:
                    try:
                        QtWidgets.QApplication.beep()
                    except Exception:
                        pass
        except Exception as e:
            Logger.error(f"Signal notify error: {e}")

    def _on_signal_symbol_clicked(self, symbol):
        try:
            Logger.info(f"[SCAN] Switching chart to {symbol}")
            self.chart_widget.set_symbol(symbol)
        except Exception as e:
            Logger.error(f"Signal symbol click error: {e}")

    def _connect_trade_callbacks(self):
        cb = self.account_panel.refresh
        cw = self.chart_widget
        if hasattr(cw, 'executor'):
            cw.executor.on_trade_callback = cb
        if hasattr(cw, 'exit_mgr'):
            cw.exit_mgr.executor.on_trade_callback = cb
        if hasattr(cw, '_trade_executor'):
            cw._trade_executor.on_trade_callback = cb
        sp = getattr(self, 'strategy_panel', None)
        if sp and hasattr(sp, 'executor'):
            sp.executor.on_trade_callback = cb
        tp = getattr(cw, 'trade_panel', None)
        if tp and hasattr(tp, 'executor'):
            tp.executor.on_trade_callback = cb

    def _refresh_pos_ord(self):
        self.positions_panel.refresh()
        self.orders_panel.refresh()
        self.account_panel.refresh()

    def refresh_all(self):
        self.account_panel.refresh()
        self.chart_widget.load_data()
        self.watchlist_panel.refresh_symbols()
        Logger.info("تمام اطلاعات به‌روزرسانی شد")

    def _load_panel_sizes(self):
        try:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    cfg = json.load(f)
                ps = cfg.get("settings", {}).get("panel_sizes", {})
                if ps.get("middle"):
                    self.middle_splitter.setSizes(ps["middle"])
                if ps.get("main"):
                    self.main_splitter.setSizes(ps["main"])
        except Exception:
            pass

    def _save_panel_sizes(self):
        try:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
            cfg = {}
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    cfg = json.load(f)
            if "settings" not in cfg:
                cfg["settings"] = {}
            cfg["settings"]["panel_sizes"] = {
                "middle": self.middle_splitter.sizes(),
                "main": self.main_splitter.sizes(),
            }
            with open(config_path, "w") as f:
                json.dump(cfg, f, indent=2)
        except Exception:
            pass

    def closeEvent(self, event):
        self._save_panel_sizes()
        self._save_chart_state()
        MT5Connector.shutdown()
        event.accept()

    def _save_chart_state(self):
        try:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
            cfg = {}
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    cfg = json.load(f)
            if "settings" not in cfg:
                cfg["settings"] = {}
            cfg["settings"]["last_symbol"] = self.chart_widget.current_symbol
            cfg["settings"]["last_tf"] = self.chart_widget.current_tf
            cfg["settings"]["chart_mode"] = getattr(self.chart_widget, '_chart_mode', 'candle')
            with open(config_path, "w") as f:
                json.dump(cfg, f, indent=2)
        except Exception:
            pass

# ============================================================
#                   نقطه ورود برنامه
# ============================================================

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLE)

    Logger.info("=" * 50)
    Logger.info("VPTradeBot - Starting application")
    Logger.info("=" * 50)

    MT5Connector.initialize()

    window = MainWindow()
    window.show()

    Logger.success("Application started successfully")

    try:
        exit_code = app.exec_()
    except KeyboardInterrupt:
        pass
    finally:
        MT5Connector.shutdown()

    sys.exit(exit_code if 'exit_code' in dir() else 0)

if __name__ == "__main__":
    main()
