# Internal filename: 'SIGMA.py'
# Bytecode version: 3.14rc3 (3627)
# Hash: 9b447b457bdf8ed0aff5e2ef420cd1bd5abccefbba295154bebd387e31adfdda

import time
import ctypes
import sys
import threading
import os
import json
import random
import math

from ctypes import wintypes
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider, QComboBox, QLineEdit, QFrame, QScrollArea, QFileDialog, QSizePolicy, QTabWidget, QStackedWidget, QGridLayout, QSpacerItem, QToolTip
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QRect, QPoint, QSize, QPropertyAnimation, QEasingCurve, QObject
from PyQt5.QtGui import QPainter, QColor, QFont, QFontMetrics, QPen, QBrush, QPalette, QCursor, QIcon
from PyQt5.QtWidgets import QProxyStyle, QStyle

class InstantTooltipStyle(QProxyStyle):
    def styleHint(self, hint, option=None, widget=None, returnData=None):
        if hint == QStyle.SH_ToolTip_WakeUpDelay:
            return 1
        else:
            if hint == QStyle.SH_ToolTip_FallAsleepDelay:
                return 0
            else:
                return super().styleHint(hint, option, widget, returnData)
class TrackingTooltip(QWidget):
    """A tooltip window that follows the mouse cursor."""
    def __init__(self):
        super().__init__(None, Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self._lbl = QLabel(self)
        self._lbl.setFont(QFont('Consolas', 9))
        self._lbl.setStyleSheet('color: #EFEFF1; background: #1F1F23; padding: 4px 8px;')
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self._lbl)
        self.setStyleSheet('background: #1F1F23; border: 1px solid #444;')
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._show)
        self._text = ''
    def show_for(self, text, pos):
        self._text = text
        self._pos = pos
        self._timer.start(80)
    def move_to(self, pos):
        self._pos = pos
        if self.isVisible():
            self._reposition(pos)
    def _reposition(self, pos):
        # ***<module>.TrackingTooltip._reposition: Failure: Different bytecode
        offset_x, offset_y = (14, 18)
        screen = QApplication.screenAt(pos)
        if screen:
            sg = screen.geometry()
            x = pos.x() + offset_x
            y = pos.y() + offset_y
            if x + self.width() > sg.right():
                x = pos.x() - self.width() - 4
            if y + self.height() > sg.bottom():
                y = pos.y() - self.height() - 4
            self.move(x, y)
    def _show(self):
        if not self._text:
            return None
        else:
            self._lbl.setText(self._text)
            self.adjustSize()
            self._reposition(self._pos)
            self.show()
            self.raise_()
    def hide_tip(self):
        self._timer.stop()
        self.hide()
        self._text = ''
class TooltipFilter(QObject):
    """Event filter installed on QApplication to track mouse for tooltip following."""
    def __init__(self, tip_widget):
        super().__init__()
        self._tip = tip_widget
        self._current_widget = None
    def eventFilter(self, obj, event):
        # ***<module>.TooltipFilter.eventFilter: Failure: Different bytecode
        if event.type() == event.ToolTip:
            return True
        else:
            if event.type() == event.Enter and isinstance(obj, QWidget):
                tip_text = obj.toolTip()
                if tip_text:
                    self._current_widget = obj
                    pos = QCursor.pos()
                    self._tip.show_for(tip_text, pos)
                return False
            else:
                if event.type() == event.Leave:
                    if obj is self._current_widget:
                        self._tip.hide_tip()
                        self._current_widget = None
                    return False
                else:
                    if event.type() == event.MouseMove:
                        pos = QCursor.pos()
                        if self._current_widget and self._tip.isVisible():
                            self._tip.move_to(pos)
                            return False
                        else:
                            if self._current_widget:
                                self._tip.move_to(pos)
                    return False
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 2
KEYEVENTF_SCANCODE = 8
user32 = ctypes.WinDLL('user32', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
winmm = ctypes.WinDLL('winmm', use_last_error=True)
ntdll = ctypes.WinDLL('ntdll', use_last_error=True)
psapi = ctypes.WinDLL('psapi', use_last_error=True)
SetThreadPriority = kernel32.SetThreadPriority
SetThreadPriority.argtypes = [wintypes.HANDLE, ctypes.c_int]
SetThreadPriority.restype = wintypes.BOOL
GetCurrentThread = kernel32.GetCurrentThread
GetCurrentThread.restype = wintypes.HANDLE
SetPriorityClass = kernel32.SetPriorityClass
SetPriorityClass.argtypes = [wintypes.HANDLE, wintypes.DWORD]
SetPriorityClass.restype = wintypes.BOOL
GetCurrentProcess = kernel32.GetCurrentProcess
GetCurrentProcess.restype = wintypes.HANDLE
NtSetTimerResolution = ntdll.NtSetTimerResolution
NtSetTimerResolution.argtypes = [wintypes.ULONG, wintypes.BOOLEAN, ctypes.POINTER(wintypes.ULONG)]
NtSetTimerResolution.restype = ctypes.c_long
QueryPerformanceFrequency = kernel32.QueryPerformanceFrequency
QueryPerformanceFrequency.argtypes = [ctypes.POINTER(ctypes.c_int64)]
QueryPerformanceFrequency.restype = wintypes.BOOL
QueryPerformanceCounter = kernel32.QueryPerformanceCounter
QueryPerformanceCounter.argtypes = [ctypes.POINTER(ctypes.c_int64)]
QueryPerformanceCounter.restype = wintypes.BOOL
MapVirtualKeyW = user32.MapVirtualKeyW
MapVirtualKeyW.argtypes = [wintypes.UINT, wintypes.UINT]
MapVirtualKeyW.restype = wintypes.UINT
GetAsyncKeyState = user32.GetAsyncKeyState
GetAsyncKeyState.argtypes = [ctypes.c_int]
GetAsyncKeyState.restype = ctypes.c_short
GetForegroundWindow = user32.GetForegroundWindow
GetForegroundWindow.restype = wintypes.HWND
GetWindowTextW = user32.GetWindowTextW
GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
GetWindowTextW.restype = ctypes.c_int
GetWindowTextLengthW = user32.GetWindowTextLengthW
GetWindowTextLengthW.argtypes = [wintypes.HWND]
GetWindowTextLengthW.restype = ctypes.c_int
GetWindowThreadProcessId = user32.GetWindowThreadProcessId
GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
GetWindowThreadProcessId.restype = wintypes.DWORD
OpenProcess = kernel32.OpenProcess
OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
OpenProcess.restype = wintypes.HANDLE
CloseHandle = kernel32.CloseHandle
CloseHandle.argtypes = [wintypes.HANDLE]
CloseHandle.restype = wintypes.BOOL
GetModuleFileNameExW = psapi.GetModuleFileNameExW
GetModuleFileNameExW.argtypes = [wintypes.HANDLE, wintypes.HMODULE, wintypes.LPWSTR, wintypes.DWORD]
GetModuleFileNameExW.restype = wintypes.DWORD
SetCursorPos = user32.SetCursorPos
SetCursorPos.argtypes = [ctypes.c_int, ctypes.c_int]
SetCursorPos.restype = wintypes.BOOL
GetCursorPos = user32.GetCursorPos
GetCursorPos.argtypes = [ctypes.POINTER(wintypes.POINT)]
GetCursorPos.restype = wintypes.BOOL
GetSystemMetrics = user32.GetSystemMetrics
GetSystemMetrics.argtypes = [ctypes.c_int]
GetSystemMetrics.restype = ctypes.c_int
mouse_event = user32.mouse_event
mouse_event.argtypes = [wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(wintypes.ULONG)]
mouse_event.restype = None
class KEYBDINPUT(ctypes.Structure):
    # ***<module>.KEYBDINPUT: Failure: Different bytecode
    _fields_ = [('wVk', wintypes.WORD), ('wScan', wintypes.WORD), ('dwFlags', wintypes.DWORD), ('time', wintypes.DWORD), ('dwExtraInfo', ctypes.POINTER(wintypes.ULONG))]
class MOUSEINPUT(ctypes.Structure):
    # ***<module>.MOUSEINPUT: Failure: Different bytecode
    _fields_ = [('dx', wintypes.LONG), ('dy', wintypes.LONG), ('mouseData', wintypes.DWORD), ('dwFlags', wintypes.DWORD), ('time', wintypes.DWORD), ('dwExtraInfo', ctypes.POINTER(wintypes.ULONG))]
class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [('uMsg', wintypes.DWORD), ('wParamL', wintypes.WORD), ('wParamH', wintypes.WORD)]
class INPUT_UNION(ctypes.Union):
    _fields_ = [('ki', KEYBDINPUT), ('mi', MOUSEINPUT), ('hi', HARDWAREINPUT)]
class INPUT(ctypes.Structure):
    _fields_ = [('type', wintypes.DWORD), ('union', INPUT_UNION)]
SendInput = user32.SendInput
SendInput.argtypes = [wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int]
SendInput.restype = wintypes.UINT
38 = {0: 'Undefined', 1: 'LMouse', 2: 'RMouse', 3: 'Cancel', 4: 'MMouse', 5: 'X1Mouse', 6: 'X2Mouse', 8: 'Backspace', 9: 'Tab', 13: 'Enter', 16: 'Shift', 17: 'Ctrl', 18: 'Alt', 19: 'Pause', 20: 'CapsLock', 27: 'Esc', 32: 'Space', 33: 'PgUp', 34: 'PgDn', 35: 'End', 36: 'Home', 37: 'Left'}
for i in range(ord('A'), ord('Z') + 1):
    VK_NAMES[i] = chr(i)
for i in range(ord('0'), ord('9') + 1):
    VK_NAMES[i] = chr(i)
def get_key_name(vk):
    return VK_NAMES.get(vk, f'Key{vk:02X}')
ROBLOX_EXECUTABLES = {'robloxplayerbeta.exe', 'robloxplayer.exe', 'roblox.exe'}
def get_foreground_process_name():
    # irreducible cflow, using cdg fallback
    # ***<module>.get_foreground_process_name: Failure: Compilation Error
    hwnd = user32.GetForegroundWindow()
    pid = wintypes.DWORD(0)
    GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    h_proc = OpenProcess(1040, False, pid.value)
    if not h_proc:
        return ''
        buf = ctypes.create_unicode_buffer(260)
        GetModuleFileNameExW(h_proc, None, buf, 260)
        CloseHandle(h_proc)
        return os.path.basename(buf.value).lower()
            return ''
def is_roblox_game_window():
    # irreducible cflow, using cdg fallback
    # ***<module>.is_roblox_game_window: Failure: Compilation Error
    hwnd = user32.GetForegroundWindow()
    length = user32.GetWindowTextLengthW(hwnd)
    if length <= 0:
        return False
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        if 'roblox' not in buff.value.lower():
            return False
            return get_foreground_process_name() in ROBLOX_EXECUTABLES
                return False
THEMES = {'default': {'bg': '#111111', 'accent': '#FFFFFF', 'btn_bg': '#1E1E1E', 'hover': '#2A2A2A', 'text': '#FFFFFF', 'muted': '#888888', 'red': '#FF4444'}}
THEME_NAMES = {'default': 'Default'}
import base64 as _b64
from PyQt5.QtGui import QPixmap
_KEY_ICON_B64 = '/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCAIAAgADASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAj/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFAEBAAAAAAAAAAAAAAAAAAAAAP/EABQRAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwEAAhEDEQA/AIyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB//9k='
def _make_key_pixmap(size=24):
    # ***<module>._make_key_pixmap: Failure: Different bytecode
    data = _b64.b64decode(_KEY_ICON_B64)
    px = QPixmap()
    px.loadFromData(data)
    return px.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
class SnowWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.flakes = []
        self._bg = QColor('#202124')
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(16)
    def set_bg(self, color_str):
        self._bg = QColor(color_str)
        self.update()
    def _init_flakes(self):
        # ***<module>.SnowWidget._init_flakes: Failure: Different bytecode
        w, h = (self.width() or 620, self.height() or 480)
        self.flakes = []
        for _ in range(150):
            self.flakes.append({'x': float(random.randint(0, w)), 'y': float(random.randint((-800), 0)), 'speed': 0.5 + random.uniform(0, 2.5), 'size': 2 + random.uniform((-0.3), 0.3), 'color': random.choice(['#dbdee1', '#b5bac1', '#949ba4'])})
    def _tick(self):
        # ***<module>.SnowWidget._tick: Failure: Different bytecode
        if not self.flakes:
            self._init_flakes()
            return None
        else:
            w, h = (self.width() or 620, self.height() or 480)
            for f in self.flakes:
                f['y'] += f['speed']
                f['x'] += f['drift']
                f['drift'] += random.uniform((-0.05), 0.05)
                f['drift'] = max((-0.5), min(0.5, f['drift']))
                if f['y'] > h or f['x'] < (-10) or f['x'] > w + 10:
                    f['x'] = float(random.randint(0, w))
                    f['y'] = float(random.randint((-100), (-10)))
                    f['drift'] = random.uniform((-0.3), 0.3)
            self.update()
    def paintEvent(self, e):
        p = QPainter(self)
        p.fillRect(self.rect(), self._bg)
        for f in self.flakes:
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(f['color']))
            s = f['size']
            p.drawEllipse(int(f['x']), int(f['y']), s, s)
        p.end()
    def resizeEvent(self, e):
        self._init_flakes()
class StatusDot(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(28, 28)
        self._color = QColor('#FF0000')
    def set_color(self, color_str):
        self._color = QColor(color_str)
        self.update()
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        p.setBrush(self._color)
        p.drawEllipse(2, 2, 18, 18)
        p.end()
class FlatButton(QPushButton):
    def __init__(self, text='', parent=None, is_remove=False):
        super().__init__(text, parent)
        self._is_remove = is_remove
        self._bg = '#292A2D'
        self._hover = '#35363A'
        self._fg = '#E8EAED'
        self._pressed_bg = '#3A3B3E'
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFlat(True)
        self._apply_style()
    def _apply_style(self):
        # ***<module>.FlatButton._apply_style: Failure: Compilation Error
        if self._is_remove:
            self.setStyleSheet('\n                QPushButton {\n                    background: #3d2426; color: #f23f43;\n                    border: none; border-radius: 8px;\n                    font-family: Consolas; font-size: 9pt; font-weight: bold;\n                    padding: 4px 8px;\n                }\n                QPushButton:hover { background: #5c3739; }\n                QPushButton:pressed { background: #7a4b4e; }\n            ')
        else:
            self.setStyleSheet(f'\n                QPushButton {\n                    background: {self._bg}; color: {self._fg};\n                    border: none; border-radius: 8px;\n                    font-family: Consolas; font-size: 10pt;\n                    padding: 4px 10px;\n                }\n                QPushButton:hover { background: {self._hover}; }\n                QPushButton:pressed { background: {self._pressed_bg}; }\n            ')
    def set_theme(self, bg, hover, fg):
        self._bg = bg
        self._hover = hover
        self._fg = fg
        self._pressed_bg = hover
        if not self._is_remove:
            self._apply_style()
class KeyBindButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__('Set Key...', parent)
        self._accent = '#FFFFFF'
        self._bg = '#1E1E1E'
        self._hover = '#2A2A2A'
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFocusPolicy(Qt.NoFocus)
        self.setAttribute(Qt.WA_MacShowFocusRect, False)
        self._apply_style()
    def set_key_name(self, name):
        self.setText(name)
    def set_waiting(self, accent, hover):
        self.setText('...')
        self.setStyleSheet('QPushButton { background: #2A2A2A; color: #FFFFFF; border: 1px solid #FFFFFF; border-radius: 8px; font-family: Consolas; font-size: 10pt; font-weight: bold; padding: 10px; outline: none; }QPushButton:pressed { background: #333333; color: #FFFFFF; border: 1px solid #FFFFFF; outline: none; }QPushButton:focus { outline: none; }')
    def set_bound(self, name, accent):
        self.setText(name)
        self._apply_style(accent_override=accent)
    def _apply_style(self, accent_override=None):
        # ***<module>.KeyBindButton._apply_style: Failure: Compilation Error
        ac = accent_override or self._accent
        self.setStyleSheet(f'\n            QPushButton {\n                background: {self._bg}; color: {ac};\n                border: 1px solid #333333; border-radius: 6px;\n                font-family: Consolas; font-size: 10pt;\n                padding: 10px; outline: none;\n            }\n            QPushButton:hover { background: {self._hover}; color: #FFFFFF; border: 1px solid #FFFFFF; }\n            QPushButton:pressed { background: #333333; color: #FFFFFF; border: 1px solid #FFFFFF; outline: none; }\n            QPushButton:focus { outline: none; border: 1px solid #333333; }\n        ')
    def set_theme(self, bg, hover, accent):
        self._bg = bg
        self._hover = hover
        self._accent = accent
        self._apply_style()
class HoverSlider(QSlider):
    """QSlider that shows a floating bubble above the cursor with the current value."""
    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self._bubble = QLabel()
        self._bubble.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self._bubble.setAttribute(Qt.WA_TranslucentBackground, False)
        self._bubble.setFont(QFont('Consolas', 12, QFont.Bold))
        self._bubble.setStyleSheet('background: #1F1F23; color: #EFEFF1; border: 1px solid #555555; border-radius: 6px; padding: 4px 10px;')
        self._bubble.setAlignment(Qt.AlignCenter)
        self.setMouseTracking(True)
    def _show_bubble(self, global_pos):
        v = self.value()
        suffix = getattr(self, '_suffix', '')
        self._bubble.setText(f'{v}{suffix}')
        self._bubble.adjustSize()
        bw = self._bubble.width()
        bh = self._bubble.height()
        self._bubble.move(global_pos.x() - bw // 2, global_pos.y() - bh - 10)
        self._bubble.show()
        self._bubble.raise_()
    def enterEvent(self, e):
        # ***<module>.HoverSlider.enterEvent: Failure: Different bytecode
        self._show_bubble(QCursor.pos())
        super().enterEvent(e)
    def leaveEvent(self, e):
        self._bubble.hide()
        super().leaveEvent(e)
    def mouseMoveEvent(self, e):
        # ***<module>.HoverSlider.mouseMoveEvent: Failure: Different bytecode
        self._show_bubble(QCursor.pos())
        super().mouseMoveEvent(e)
    def valueChanged_update(self, v):
        # ***<module>.HoverSlider.valueChanged_update: Failure: Different bytecode
        if self._bubble.isVisible():
            self._show_bubble(QCursor.pos())
class PercentLineEdit(QLineEdit):
    # ***<module>.PercentLineEdit: Failure: Different bytecode
    """QLineEdit that always keeps a trailing \'%\' and only lets the user edit the number."""
    def __init__(self, value=25, parent=None):
        super().__init__(f'{value}%', parent)
    def keyPressEvent(self, e):
        # irreducible cflow, using cdg fallback
        # ***<module>.PercentLineEdit.keyPressEvent: Failure: Compilation Error
        text = self.text()
        num = text.rstrip('%')
        if e.key() in (Qt.Key_Delete, Qt.Key_Backspace):
            cursor = self.cursorPosition()
            if e.key() == Qt.Key_Backspace and cursor <= len(num):
                super().keyPressEvent(e)
                self._fix_percent()
                return None
            else:
                if e.key() == Qt.Key_Delete and cursor < len(num):
                        super().keyPressEvent(e)
                        self._fix_percent()
                return None
        else:
            if e.key() in [Qt.Key_Left, Qt.Key_Right, Qt.Key_Home, Qt.Key_End]:
                super().keyPressEvent(e)
                return None
            else:
                if e.text().isdigit():
                    cursor = self.cursorPosition()
                    if cursor <= len(num):
                        new_num = num[:cursor] + e.text() + num[cursor:]
        if int(new_num) > 100:
            self.blockSignals(True)
            self.setText('100%')
            self.setCursorPosition(3)
            self.blockSignals(False)
            self.textChanged.emit(self.text())
                return
                        super().keyPressEvent(e)
                        self._fix_percent()
                except ValueError:
                        pass
    def _fix_percent(self):
        text = self.text()
        if not text.endswith('%'):
            cursor = self.cursorPosition()
            self.blockSignals(True)
            self.setText(text.rstrip('%') + '%')
            self.setCursorPosition(min(cursor, len(self.text()) - 1))
            self.blockSignals(False)
            self.textChanged.emit(self.text())
    def focusInEvent(self, e):
        # ***<module>.PercentLineEdit.focusInEvent: Failure: Different bytecode
        super().focusInEvent(e)
        QTimer.singleShot(0, lambda: self.setCursorPosition(len(self.text()) - 1))
    def setValue(self, v):
        self.blockSignals(True)
        self.setText(f'{v}%')
        self.blockSignals(False)
    def numericValue(self):
        try:
            return int(self.text().replace('%', '').strip())
        except:
            return 0
def make_slider(min_val, max_val, value, bg, accent, trough, callback=None):
    # ***<module>.make_slider: Failure: Compilation Error
    sl = HoverSlider(Qt.Horizontal)
    sl.setRange(min_val, max_val)
    sl.setValue(value)
    sl.setFocusPolicy(Qt.NoFocus)
    sl.wheelEvent = lambda e: e.ignore()
    sl.setStyleSheet(f'\n        QSlider { background: transparent; }\n        QSlider::groove:horizontal {\n            background: #333333; height: 4px; border-radius: 2px;\n        }\n        QSlider::handle:horizontal {\n            background: {accent}; width: 14px; height: 14px;\n            margin: -5px 0; border-radius: 7px;\n        }\n        QSlider::sub-page:horizontal { background: {accent}; border-radius: 2px; }\n        QSlider::add-page:horizontal { background: #333333; border-radius: 2px; }\n    ')
    sl.valueChanged.connect(sl.valueChanged_update)
    if callback:
        sl.valueChanged.connect(callback)
    return sl
def styled_combo(items, bg, accent, hover, text):
    cb = QComboBox()
    cb.addItems(items)
    cb.setStyleSheet('\n        QComboBox {\n            background: #1E1E1E; color: #FFFFFF; border: 1px solid #FFFFFF;\n            font-family: Consolas; font-size: 9pt; padding: 3px 8px;\n            border-radius: 8px; min-width: 0px; outline: none;\n        }\n        QComboBox:hover { border: 1px solid #AAAAAA; }\n        QComboBox:focus { border: 1px solid #FFFFFF; outline: none; }\n        QComboBox:on { border: 1px solid #FFFFFF; }\n        QComboBox QAbstractItemView {\n            background: #1E1E1E; color: #FFFFFF;\n            selection-background-color: #FFFFFF;\n            selection-color: white;\n            border: 1px solid #FFFFFF; border-radius: 8px; outline: none;\n            padding: 4px;\n        }\n        QComboBox QAbstractItemView::item {\n            padding: 6px 10px;\n            border-radius: 4px;\n            min-height: 24px;\n        }\n        QComboBox QAbstractItemView::item:hover {\n            background: #FFFFFF; color: #000000; border: 1px solid #FFFFFF; border-radius: 4px;\n        }\n        QComboBox QAbstractItemView::item:selected {\n            background: #FFFFFF; color: #000000; border: 1px solid #FFFFFF; border-radius: 4px;\n        }\n        QComboBox::drop-down { border: none; width: 20px; }\n        QComboBox::down-arrow { width: 10px; height: 10px; }\n    ')
    return cb
class KeyListenerThread(QThread):
    status_changed = pyqtSignal(bool)
    key_captured = pyqtSignal(str, int)
    gui_hide_toggle = pyqtSignal()
    curve_triggered = pyqtSignal()
    mouse_lock_toggled = pyqtSignal(bool)
    macro_toggled = pyqtSignal(bool)
    def __init__(self, app_ref):
        super().__init__()
        self.app = app_ref
        self._running = True
    def stop(self):
        self._running = False
    def run(self):
        # ***<module>.KeyListenerThread.run: Failure: Different control flow
        pressed_keys = set()
        last_toggle = last_system = last_hide = last_curve = last_mouse_lock = False
        if self._running:
            app = self.app
            if app.waiting_for_key:
                for vk in range(256):
                    if GetAsyncKeyState(vk) & 32768 and vk not in pressed_keys:
                            if vk in [27]:
                                self.key_captured.emit(app.waiting_for_key, (-1))
                            else:
                                self.key_captured.emit(app.waiting_for_key, vk)
                            time.sleep(0.2)
                            break
            else:
                if app.system_toggle_key is not None:
                    sp = bool(GetAsyncKeyState(app.system_toggle_key) & 32768)
                    if sp and (not last_system):
                            new_state = not app.macro_system_enabled
                            app.macro_system_enabled = new_state
                            self.status_changed.emit(new_state)
                            if not new_state:
                                app.toggled = False
                                app.mouse_locked = False
                            try:
                                user32.MessageBeep(64 if new_state else 16)
                            except:
                                pass
                    last_system = sp
                if app.hide_gui_key is not None:
                    hp = bool(GetAsyncKeyState(app.hide_gui_key) & 32768)
                    if hp and (not last_hide):
                            self.gui_hide_toggle.emit()
                            time.sleep(0.2)
                    last_hide = hp
                if app.macro_system_enabled and app.curve_key is not None:
                        cp = bool(GetAsyncKeyState(app.curve_key) & 32768)
                        if cp and (not last_curve):
                                threading.Thread(target=app._do_camera_flick, daemon=True).start()
                                time.sleep(app.flick_cooldown or 0.01)
                        last_curve = cp
                if app.macro_system_enabled and app.mouse_lock_key is not None:
                        mlp = bool(GetAsyncKeyState(app.mouse_lock_key) & 32768)
                        if mlp and (not last_mouse_lock):
                                new_ml = not app.mouse_locked
                                app.mouse_locked = new_ml
                                self.mouse_lock_toggled.emit(new_ml)
                                time.sleep(0.2)
                        last_mouse_lock = mlp
                if app.macro_system_enabled and app.macro_key is not None:
                        tp = bool(GetAsyncKeyState(app.macro_key) & 32768)
                        win_ok = True
                        if app.window_mode == 'roblox':
                            win_ok = is_roblox_game_window()
                        if app.mode == 'toggle':
                            if tp and (not last_toggle) and win_ok:
                                        new_t = not app.toggled
                                        app.toggled = new_t
                                        self.macro_toggled.emit(new_t)
                            last_toggle = tp
                        else:
                            if app.mode == 'hold':
                                if tp and (not app.toggled) and win_ok:
                                    app.toggled = True
                                    self.macro_toggled.emit(True)
                                else:
                                    if not (tp and win_ok) and app.toggled:
                                            app.toggled = False
                                            self.macro_toggled.emit(False)
            current = set()
            for vk in range(256):
                if GetAsyncKeyState(vk) & 32768:
                    current.add(vk)
            pressed_keys = current
            time.sleep(0.01)
class SpamThread(QThread):
    def __init__(self, app_ref):
        super().__init__()
        self.app = app_ref
    def run(self):
        # irreducible cflow, using cdg fallback
        # ***<module>.SpamThread.run: Failure: Compilation Error
        SetThreadPriority(GetCurrentThread(), 2)
                app = self.app
                if app.cps <= 0:
                    return None
                else:
                    inputs = (INPUT * 2)()
                    check_window = app.window_mode == 'roblox'
                    if app.action_mode == 'kps':
                        if app.spam_key is None:
                            return None
                        else:
                            scan = MapVirtualKeyW(app.spam_key, 0)
                            inputs[0].type = INPUT_KEYBOARD
                            inputs[0].union.ki.wVk = app.spam_key
                            inputs[0].union.ki.wScan = scan
                            inputs[0].union.ki.dwFlags = KEYEVENTF_SCANCODE
                            inputs[0].union.ki.time = 0
                            inputs[0].union.ki.dwExtraInfo = None
                            inputs[1].type = INPUT_KEYBOARD
                            inputs[1].union.ki.wVk = app.spam_key
                            inputs[1].union.ki.wScan = scan
                            inputs[1].union.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP
                            inputs[1].union.ki.time = 0
                            inputs[1].union.ki.dwExtraInfo = None
                    else:
                        if app.spam_key is None or app.spam_key not in [1, 2, 4, 5, 6]:
                            return None
                        else:
                            if app.mouse_button == 'right':
                                down_flag, up_flag, md = (8, 16, 0)
                            else:
                                if app.mouse_button == 'middle':
                                    down_flag, up_flag, md = (32, 64, 0)
                                else:
                                    if app.mouse_button == 'x1':
                                        down_flag, up_flag, md = (128, 256, 1)
                                    else:
                                        if app.mouse_button == 'x2':
                                            down_flag, up_flag, md = (128, 256, 2)
                                        else:
                                            down_flag, up_flag, md = (2, 4, 0)
                            inputs[0].type = INPUT_MOUSE
                            inputs[0].union.mi.dx = 0
                            inputs[0].union.mi.dy = 0
                            inputs[0].union.mi.mouseData = md
                            inputs[0].union.mi.dwFlags = down_flag
                            inputs[0].union.mi.time = 0
                            inputs[0].union.mi.dwExtraInfo = None
                            inputs[1].type = INPUT_MOUSE
                            inputs[1].union.mi.dx = 0
                            inputs[1].union.mi.dy = 0
                            inputs[1].union.mi.mouseData = md
                            inputs[1].union.mi.dwFlags = up_flag
                            inputs[1].union.mi.time = 0
                            inputs[1].union.mi.dwExtraInfo = None
                    input_size = ctypes.sizeof(INPUT)
                    freq = ctypes.c_int64()
                    QueryPerformanceFrequency(ctypes.byref(freq))
                    freq_val = freq.value
                    counter = ctypes.c_int64()
                    QueryPerformanceCounter(ctypes.byref(counter))
                    target_interval = freq_val / max(1, app.cps)
                    next_time = counter.value + target_interval
                    if app.toggled and app.running:
                            if app.cps > 0:
                                target_interval = freq_val / max(1, app.cps)
                            should_spam = True
                            if check_window:
                                should_spam = is_roblox_game_window()
                            QueryPerformanceCounter(ctypes.byref(counter))
                            now = counter.value
                            if now >= next_time:
                                if should_spam:
                                    SendInput(2, inputs, input_size)
                                next_time += target_interval
                                if next_time < now:
                                    next_time = now + target_interval
                            else:
                                diff = (next_time - now) / freq_val
                                if diff > 0.002:
                                    time.sleep(diff - 0.001)
                pass
class MouseLockThread(QThread):
    def __init__(self, app_ref):
        super().__init__()
        self.app = app_ref
    def run(self):
        # irreducible cflow, using cdg fallback
        # ***<module>.MouseLockThread.run: Failure: Compilation Error
        SetThreadPriority(GetCurrentThread(), 2)
                sw = GetSystemMetrics(0)
                sh = GetSystemMetrics(1)
                cx, cy = (sw // 2, sh // 2)
                mouse_event(8, 0, 0, 0, None)
                app = self.app
                if app.mouse_locked and app.running:
                    ok = True
                    if app.window_mode == 'roblox':
                        ok = is_roblox_game_window()
                    if ok:
                        SetCursorPos(cx, cy)
                    time.sleep(0.001)
                else:
                    mouse_event(16, 0, 0, 0, None)
                pass
class SigmaWindow(QMainWindow):
    def __init__(self):
        # ***<module>.SigmaWindow.__init__: Failure: Different bytecode
        super().__init__()
        self.setWindowTitle('Sigma Macro')
        self.setMinimumSize(650, 350)
        self.resize(650, 350)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.running = True
        self.toggled = False
        self.macro_system_enabled = False
        self.gui_visible = True
        self.waiting_for_key = None
        self.system_toggle_key = None
        self.macro_key = None
        self.spam_key = None
        self.hide_gui_key = None
        self.curve_key = None
        self.mouse_lock_key = None
        self.mouse_locked = False
        self.randomize_angles = False
        self.curve_vertical_enabled = True
        self.curve_backward_enabled = True
        self.curve_lside_enabled = True
        self.curve_rside_enabled = True
        self.chance_vertical = 25
        self.chance_backward = 25
        self.chance_lside = 25
        self.chance_rside = 25
        self.fspeed_vertical = 0
        self.fspeed_backward = 0
        self.fspeed_lside = 0
        self.fspeed_rside = 0
        self.global_flick_speed = 0
        self.flick_cooldown = 0.0
        self.mode = 'toggle'
        self.action_mode = 'kps'
        self.mouse_button = 'left'
        self.cps = 0
        self.window_mode = 'roblox'
        self.current_theme = 'default'
        self._spam_thread = None
        self._lock_thread = None
        t = THEMES[self.current_theme]
        self.T = t
        try:
            SetPriorityClass(GetCurrentProcess(), 256)
            SetThreadPriority(GetCurrentThread(), 2)
            winmm.timeBeginPeriod(1)
            self.current_resolution = wintypes.ULONG()
            NtSetTimerResolution(5000, True, ctypes.byref(self.current_resolution))
        except:
            pass
        self._build_ui()
        self._key_thread = KeyListenerThread(self)
        self._key_thread.status_changed.connect(self._on_status_changed)
        self._key_thread.key_captured.connect(self._on_key_captured)
        self._key_thread.gui_hide_toggle.connect(self._toggle_gui_visibility)
        self._key_thread.curve_triggered.connect(self._do_camera_flick)
        self._key_thread.mouse_lock_toggled.connect(self._on_mouse_lock)
        self._key_thread.macro_toggled.connect(self._on_macro_toggle)
        self._key_thread.start()
    def _card(self, title=None):
        """Returns (card_frame, inner_layout). Optionally adds a section title."""
        frame = QFrame()
        frame.setObjectName('card')
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(14, 10, 14, 12)
        layout.setSpacing(8)
        if title:
            lbl = QLabel(title)
            lbl.setFont(QFont('Consolas', 7, QFont.Bold))
            lbl.setObjectName('card_title')
            layout.addWidget(lbl)
        return (frame, layout)
    def _divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setObjectName('divider')
        return line
    def _build_ui(self):
        t = self.T
        central = QWidget()
        self.setCentralWidget(central)
        central.setObjectName('central')
        self.snow = SnowWidget(central)
        self.snow.set_bg(t['bg'])
        self.snow.setGeometry(0, 0, self.width(), self.height())
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        self.sidebar = QWidget()
        self.sidebar.setObjectName('sidebar')
        self.sidebar.setFixedWidth(175)
        sb = QVBoxLayout(self.sidebar)
        sb.setContentsMargins(0, 0, 0, 0)
        sb.setSpacing(0)
        self.header_frame = QFrame()
        self.header_frame.setObjectName('header_frame')
        self.header_frame.setStyleSheet('QFrame#header_frame { border: 2px solid #888888; border-radius: 10px; background: transparent; }')
        hf_layout = QVBoxLayout(self.header_frame)
        hf_layout.setContentsMargins(0, 0, 0, 0)
        hf_layout.setSpacing(0)
        self.header_w = QWidget()
        self.header_w.setObjectName('sb_header')
        self.header_w.setFixedHeight(56)
        hbl = QHBoxLayout(self.header_w)
        hbl.setContentsMargins(14, 0, 14, 0)
        hbl.setSpacing(0)
        self.status_lbl = QLabel('INACTIVE')
        self.status_lbl.setFont(QFont('Consolas', 11, QFont.Bold))
        self.status_lbl.setAlignment(Qt.AlignCenter)
        self.status_lbl.setStyleSheet('background: transparent; color: white; letter-spacing: 3px;')
        hbl.addStretch()
        hbl.addWidget(self.status_lbl)
        hbl.addStretch()
        self.header_w.setStyleSheet('background: #7a1a1a; border-radius: 8px;')
        hf_layout.addWidget(self.header_w)
        sb.addWidget(self.header_frame)
        def _nav(icon, text, tab):
            btn = QPushButton(f'  {text}' if not icon else f'  {icon}  {text}')
            btn.setFont(QFont('Consolas', 9))
            btn.setFixedHeight(40)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setObjectName(f'nav_{tab}')
            btn.clicked.connect(lambda: self._switch_tab(tab))
            return btn
        self.tab_keybinds_btn = _nav('', 'Clash', 'keybinds')
        self.tab_keybinds_btn.setToolTip('CLASH')
        self.tab_curve_btn = _nav('', 'Curve', 'curve')
        self.tab_curve_btn.setToolTip('CURVE')
        sb.addWidget(self.tab_keybinds_btn)
        sb.addWidget(self.tab_curve_btn)
        sb.addSpacing(8)
        sb.addWidget(self._divider())
        qs_lbl = QLabel('  SETTINGS')
        qs_lbl.setFont(QFont('Consolas', 7, QFont.Bold))
        qs_lbl.setFixedHeight(28)
        qs_lbl.setObjectName('nav_section_lbl')
        sb.addWidget(qs_lbl)
        def _sb_row(label, widget):
            w = QWidget()
            hl = QHBoxLayout(w)
            hl.setContentsMargins(10, 2, 10, 2)
            hl.setSpacing(4)
            lbl = QLabel(label)
            lbl.setFont(QFont('Consolas', 7))
            lbl.setObjectName('qs_lbl')
            lbl.setFixedWidth(58)
            hl.addWidget(lbl)
            hl.addWidget(widget, 1)
            return w
        def make_cycle_btn(options, tooltip=''):
            btn = QPushButton(options[0])
            btn._options = options
            btn._index = 0
            btn.setFont(QFont('Consolas', 9))
            btn.setFixedHeight(26)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setToolTip(tooltip)
            btn.setStyleSheet('\n                QPushButton {\n                    background: #1E1E1E; color: #FFFFFF;\n                    border: 1px solid #555555; border-radius: 8px;\n                    padding: 2px 8px; text-align: center;\n                }\n                QPushButton:hover { background: #2A2A2A; border: 1px solid #888888; }\n                QPushButton:pressed { background: #333333; border: 1px solid #AAAAAA; }\n            ')
            def _cycle(b=btn):
                b._index = (b._index + 1) % len(b._options)
                b.setText(b._options[b._index])
                b.clicked.emit()
            btn._cycle = _cycle
            btn.clicked.connect(lambda checked=False, b=btn: None)
            return btn
        self.mode_combo = make_cycle_btn(['Toggle', 'Hold'], 'Toggle: Press to activate, Press again to Deactivate.\nHold: Hold macro key to activate.')
        def _mode_click():
            self.mode_combo._index = (self.mode_combo._index + 1) % len(self.mode_combo._options)
            self.mode_combo.setText(self.mode_combo._options[self.mode_combo._index])
            self.mode = self.mode_combo.text().lower()
        self.mode_combo.clicked.connect(_mode_click)
        self.action_combo = make_cycle_btn(['KPS', 'CPS'], 'KPS: Keypress Per Second (best if u have good pc).\nCPS: Click Per Second, Good if you want light clashes or if u have potato pc.')
        def _action_click():
            self.action_combo._index = (self.action_combo._index + 1) % len(self.action_combo._options)
            self.action_combo.setText(self.action_combo._options[self.action_combo._index])
            self.action_mode = self.action_combo.text().lower()
        self.action_combo.clicked.connect(_action_click)
        self.target_combo = make_cycle_btn(['Roblox', 'Global'], 'Roblox: Only Activates in roblox window.\nGlobal: Activates at all windows.')
        def _target_click():
            self.target_combo._index = (self.target_combo._index + 1) % len(self.target_combo._options)
            self.target_combo.setText(self.target_combo._options[self.target_combo._index])
            self.window_mode = 'roblox' if self.target_combo.text() == 'Roblox' else 'global'
        self.target_combo.clicked.connect(_target_click)
        def _make_set_text(btn):
            def setCurrentText(v):
                if v in btn._options:
                    btn._index = btn._options.index(v)
                    btn.setText(v)
            btn.setCurrentText = setCurrentText
            def currentText():
                return btn.text()
            btn.currentText = currentText
        for b in [self.mode_combo, self.action_combo, self.target_combo]:
            _make_set_text(b)
        self.theme_combo = QComboBox()
        self.theme_combo.hide()
        sb.addWidget(_sb_row('Mode', self.mode_combo))
        sb.addWidget(_sb_row('Method', self.action_combo))
        sb.addWidget(_sb_row('Target', self.target_combo))
        sb.addSpacing(8)
        sb.addWidget(self._divider())
        sb.addStretch()
        sl_row = QWidget()
        sl_hl = QHBoxLayout(sl_row)
        sl_hl.setContentsMargins(8, 4, 8, 4)
        sl_hl.setSpacing(6)
        self._save_btn = QPushButton('Save')
        self._save_btn.setFont(QFont('Consolas', 9))
        self._save_btn.setFixedHeight(30)
        self._save_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self._save_btn.setToolTip('Saves your whole settings.')
        self._save_btn.setStyleSheet('\n            QPushButton { background: #1E1E1E; color: #FFFFFF; border: 1px solid #333333; border-radius: 8px; }\n            QPushButton:hover { background: #222222; border: 1px solid #444444; color: #FFFFFF; }\n            QPushButton:pressed { background: #2a2a2a; border: 1px solid #555555; }\n        ')
        self._save_btn.clicked.connect(self._save_settings)
        self._load_btn = QPushButton('Load')
        self._load_btn.setFont(QFont('Consolas', 9))
        self._load_btn.setFixedHeight(30)
        self._load_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self._load_btn.setToolTip('Loads your saved settings.')
        self._load_btn.setStyleSheet('\n            QPushButton { background: #1E1E1E; color: #FFFFFF; border: 1px solid #333333; border-radius: 8px; }\n            QPushButton:hover { background: #222222; border: 1px solid #444444; color: #FFFFFF; }\n            QPushButton:pressed { background: #2a2a2a; border: 1px solid #555555; }\n        ')
        self._load_btn.clicked.connect(self._load_settings)
        sl_hl.addWidget(self._save_btn)
        sl_hl.addWidget(self._load_btn)
        sb.addWidget(sl_row)
        root.addWidget(self.sidebar)
        vline = QFrame()
        vline.setFrameShape(QFrame.VLine)
        vline.setObjectName('vline')
        root.addWidget(vline)
        content_wrap = QWidget()
        content_wrap.setObjectName('content_wrap')
        cv = QVBoxLayout(content_wrap)
        cv.setContentsMargins(0, 0, 0, 0)
        cv.setSpacing(0)
        topbar = QWidget()
        topbar.setObjectName('topbar')
        topbar.setFixedHeight(44)
        tbl = QHBoxLayout(topbar)
        tbl.setContentsMargins(18, 0, 18, 0)
        self.page_title = QLabel('CLASH')
        self.page_title.setFont(QFont('Consolas', 11, QFont.Bold))
        self.page_title.setStyleSheet('background: transparent; color: white; letter-spacing: 3px;')
        tbl.addWidget(self.page_title)
        tbl.addStretch()
        self.discord_btn = QPushButton('Discord')
        self.discord_btn.setFont(QFont('Consolas', 8))
        self.discord_btn.setFixedHeight(30)
        self.discord_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.discord_btn.setObjectName('discord_btn')
        self.discord_btn.setToolTip('Share our discord server!, or join us!.')
        self.discord_btn.clicked.connect(self._copy_discord)
        tbl.addWidget(self.discord_btn)
        cv.addWidget(topbar)
        cv.addWidget(self._divider())
        self.stack = QStackedWidget()
        self.stack.setObjectName('page_stack')
        cv.addWidget(self.stack, 1)
        root.addWidget(content_wrap, 1)
        kb_scroll = QScrollArea()
        kb_scroll.setWidgetResizable(True)
        kb_scroll.setStyleSheet('QScrollArea{border:none;} QScrollBar{width:0px;}')
        kb_inner = QWidget()
        kb_vbox = QVBoxLayout(kb_inner)
        kb_vbox.setContentsMargins(18, 16, 18, 16)
        kb_vbox.setSpacing(12)
        kb_scroll.setWidget(kb_inner)
        self.stack.addWidget(kb_scroll)
        kb_card, kb_cl = self._card('KEYBINDS')
        kb_grid = QGridLayout()
        kb_grid.setSpacing(8)
        kb_grid.setColumnStretch(0, 1)
        kb_grid.setColumnStretch(1, 1)
        self.system_toggle_btn = self._make_kb_btn('system', 'Prevents accidental activation.')
        self.macro_btn = self._make_kb_btn('macro', 'Key activation to activate the macro.')
        self.spam_btn = self._make_kb_btn('spam', 'Spams your setted keyboard key, (Make sure your blade ball block keybinds match to work!)')
        self.hide_gui_btn = self._make_kb_btn('hide_gui', 'Hides the whole gui.')
        kb_grid.addWidget(self._kb_cell(self.system_toggle_btn, 'System Toggle', 'system'), 0, 0)
        kb_grid.addWidget(self._kb_cell(self.macro_btn, 'Macro Key', 'macro'), 0, 1)
        kb_grid.addWidget(self._kb_cell(self.spam_btn, 'Key2Spam', 'spam'), 1, 0)
        kb_grid.addWidget(self._kb_cell(self.hide_gui_btn, 'Hide GUI', 'hide_gui'), 1, 1)
        kb_cl.addLayout(kb_grid)
        kb_vbox.addWidget(kb_card)
        kps_card, kps_cl = self._card('KPS / CPS')
        kps_row = QHBoxLayout()
        kps_row.setSpacing(8)
        self.kps_entry = QLineEdit(str(self.cps))
        self.kps_entry.setFixedWidth(56)
        self.kps_entry.setAlignment(Qt.AlignCenter)
        self.kps_entry.setFont(QFont('Consolas', 12, QFont.Bold))
        self.kps_entry.textChanged.connect(self._on_kps_entry)
        self.kps_entry.returnPressed.connect(self.kps_entry.clearFocus)
        kps_row.addWidget(self.kps_entry)
        self.kps_slider = make_slider(0, 5000, self.cps, t['bg'], t['accent'], t['bg'], callback=self._on_kps_slider)
        self.kps_slider.setToolTip('Adjusts the keypress per second / click per second.')
        kps_row.addWidget(self.kps_slider, 1)
        kps_cl.addLayout(kps_row)
        kb_vbox.addWidget(kps_card)
        kb_vbox.addStretch()
        cv_scroll = QScrollArea()
        cv_scroll.setWidgetResizable(True)
        cv_scroll.setStyleSheet('QScrollArea{border:none;} QScrollBar{width:0px;}')
        cv_inner = QWidget()
        cv_vbox = QVBoxLayout(cv_inner)
        cv_vbox.setContentsMargins(18, 16, 18, 16)
        cv_vbox.setSpacing(12)
        cv_scroll.setWidget(cv_inner)
        self.stack.addWidget(cv_scroll)
        rnd_card, rnd_cl = self._card('RANDOMIZER')
        self.randomize_btn = QPushButton('  Enable Randomizer')
        self.randomize_btn.setFont(QFont('Consolas', 9, QFont.Bold))
        self.randomize_btn.setFixedHeight(34)
        self.randomize_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.randomize_btn.setToolTip('Randomize camera angles on each flick.')
        self.randomize_btn.clicked.connect(self._toggle_randomize)
        rnd_cl.addWidget(self.randomize_btn)
        cv_vbox.addWidget(rnd_card)
        note_card, note_cl = self._card()
        note_card.setObjectName('note_card')
        note_lbl2_inner = QLabel('<span style=\'color:#FF9944;font-weight:bold;\'>NOTICE!:</span><span style=\'color:#AAAAAA;\'> Use 0.84 Roblox sensitivity for the curve macro or camera flick to work properly!</span>')
        note_lbl2_inner.setFont(QFont('Consolas', 7))
        note_lbl2_inner.setStyleSheet('background: transparent;')
        note_lbl2_inner.setWordWrap(True)
        note_cl.addWidget(note_lbl2_inner)
        cv_vbox.addWidget(note_card)
        self.chance_widgets = {}
        angle_tooltips = {'vertical': 'Camera flicks vertically.', 'backward': 'Camera flicks backwards.', 'lside': 'Camera flicks to right side.', 'rside': 'Camera flicks to left side.'}
        self._chance_bubble = QLabel('25%', self)
        self._chance_bubble.setFont(QFont('Consolas', 8, QFont.Bold))
        self._chance_bubble.setStyleSheet('background: #1F1F23; color: #EFEFF1; border: 1px solid #555555; border-radius: 4px; padding: 2px 6px;')
        self._chance_bubble.setAlignment(Qt.AlignCenter)
        self._chance_bubble.hide()
        self._chance_bubble.raise_()
        def _show_bubble(slider, value, key):
            setattr(self, f'chance_{key}', value)
        def _hide_bubble():
            return None
        self.chances_frame = QFrame()
        angles_container = QWidget()
        angles_vbox = QVBoxLayout(angles_container)
        angles_vbox.setContentsMargins(0, 0, 0, 0)
        angles_vbox.setSpacing(8)
        for name, key in [('VERTICAL', 'vertical'), ('BACKWARD', 'backward'), ('R-SIDE', 'lside'), ('L-SIDE', 'rside')]:
            sl_card, sl_cl = self._card()
            sl_cl.setContentsMargins(14, 8, 14, 8)
            sl_cl.setSpacing(4)
            lbl = QLabel(name)
            lbl.setFont(QFont('Consolas', 8))
            lbl.setObjectName('qs_lbl')
            lbl.setToolTip(angle_tooltips[key])
            row = QHBoxLayout()
            row.setSpacing(8)
            entry = PercentLineEdit(25)
            entry.setFixedWidth(58)
            entry.setAlignment(Qt.AlignCenter)
            entry.setFont(QFont('Consolas', 10, QFont.Bold))
            sl = make_slider(0, 100, 25, t['bg'], t['accent'], t['bg'])
            sl._suffix = '%'
            sl.setToolTip(angle_tooltips[key])
            def _on_slider(v, k=key, e=entry):
                setattr(self, f'chance_{k}', v)
                e.setValue(v)
            def _on_entry(text, k=key, s=sl, e=entry):
                try:
                    raw = int(text.replace('%', '').strip())
                    v = max(0, min(100, raw))
                    if raw > 100:
                        e.blockSignals(True)
                        e.setText('100%')
                        e.setCursorPosition(3)
                        e.blockSignals(False)
                    setattr(self, f'chance_{k}', v)
                    s.blockSignals(True)
                    s.setValue(v)
                    s.blockSignals(False)
                except:
                    return None
            sl.valueChanged.connect(_on_slider)
            entry.textChanged.connect(_on_entry)
            entry.returnPressed.connect(entry.clearFocus)
            chance_lbl = QLabel('Chance')
            chance_lbl.setFont(QFont('Consolas', 8))
            chance_lbl.setObjectName('qs_lbl')
            row.addWidget(entry)
            row.addWidget(chance_lbl)
            row.addWidget(sl, 1)
            sl_cl.addWidget(lbl)
            sl_cl.addLayout(row)
            angles_vbox.addWidget(sl_card)
            self.chance_widgets[key] = (sl, None)
        cv_vbox.addWidget(angles_container)
        self.fs_val_lbl = QLabel('0')
        self.fs_val_lbl.hide()
        self.fs_label = QPushButton()
        self.fs_label.hide()
        self.cooldown_label = QPushButton()
        self.cooldown_label.hide()
        self.cd_slider = QSlider()
        self.cd_slider.hide()
        self.cd_val_lbl = QLabel()
        self.cd_val_lbl.hide()
        fspd_card, fspd_cl = self._card('FLICK SPEED')
        fspd_cl.setContentsMargins(14, 6, 14, 6)
        fspd_cl.setSpacing(4)
        fspd_row = QHBoxLayout()
        fspd_row.setSpacing(8)
        fspd_lbl = QLabel('Speed')
        fspd_lbl.setFont(QFont('Consolas', 8))
        fspd_lbl.setFixedWidth(50)
        fspd_lbl.setObjectName('qs_lbl')
        self.fspd_entry = QLineEdit('0')
        self.fspd_entry.setFixedWidth(40)
        self.fspd_entry.setAlignment(Qt.AlignCenter)
        self.fspd_entry.setFont(QFont('Consolas', 10, QFont.Bold))
        self.fspd_entry.returnPressed.connect(self.fspd_entry.clearFocus)
        self.fspd_slider = make_slider(1, 5, 0, t['bg'], t['accent'], t['bg'])
        self.fspd_slider.setToolTip('Adjusts how fast the camera flicks. 1 = almost instant, 5 = slowest.')
        self.fs_entry = QLineEdit('0')
        self.fs_entry.hide()
        self.fs_slider = self.fspd_slider
        def _show_fspd_bubble(v):
            setattr(self, 'global_flick_speed', v)
            self.fspeed_vertical = self.fspeed_backward = self.fspeed_lside = self.fspeed_rside = v
            self.fspd_entry.blockSignals(True)
            self.fspd_entry.setText(str(v))
            self.fspd_entry.blockSignals(False)
        def _on_fspd_entry(text):
            try:
                v = max(1, min(5, int(text)))
                self.fspd_slider.blockSignals(True)
                self.fspd_slider.setValue(v)
                self.fspd_slider.blockSignals(False)
                _show_fspd_bubble(v)
            except:
                return None
        self.fspd_slider.valueChanged.connect(_show_fspd_bubble)
        self.fspd_slider.sliderReleased.connect(_hide_bubble)
        self.fspd_entry.textChanged.connect(_on_fspd_entry)
        fspd_row.addWidget(fspd_lbl)
        fspd_row.addWidget(self.fspd_entry)
        fspd_row.addWidget(self.fspd_slider, 1)
        fspd_cl.addLayout(fspd_row)
        cv_vbox.addWidget(fspd_card)
        ck_card, ck_cl = self._card('KEYBINDS')
        ck_grid = QGridLayout()
        ck_grid.setSpacing(8)
        ck_grid.setColumnStretch(0, 1)
        ck_grid.setColumnStretch(1, 1)
        self.curve_key_btn = self._make_kb_btn('curve', 'Triggers a camera flick')
        self.mouse_lock_btn = self._make_kb_btn('mouse_lock', 'Lock mouse + hold RMB')
        ck_grid.addWidget(self._kb_cell(self.curve_key_btn, 'Key2Trigger', 'curve'), 0, 0)
        ck_grid.addWidget(self._kb_cell(self.mouse_lock_btn, 'Focus Mode', 'mouse_lock'), 0, 1)
        ck_cl.addLayout(ck_grid)
        cv_vbox.addWidget(ck_card)
        note_card2, note_cl2 = self._card()
        note_card2.setObjectName('note_card')
        note_lbl = QLabel('<span style=\'color:#FF9944;font-weight:bold;\'>NOTICE!:</span><span style=\'color:#AAAAAA;\'> If your mouse gets locked to the center while using Focus Mode, press ESC on your keyboard to release it.</span>')
        note_lbl.setFont(QFont('Consolas', 7))
        note_lbl.setStyleSheet('background: transparent;')
        note_lbl.setWordWrap(True)
        note_cl2.addWidget(note_lbl)
        cv_vbox.addWidget(note_card2)
        cv_vbox.addStretch()
        self.active_tab = 'keybinds'
        self._switch_tab('keybinds')
        self._apply_theme(self.current_theme)
    def _make_kb_btn(self, key_type, tooltip=''):
        btn = KeyBindButton()
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        btn.setMinimumHeight(42)
        btn.setToolTip(tooltip)
        btn.clicked.connect(lambda _, kt=key_type: self._start_key_wait(kt))
        return btn
    def _kb_cell(self, btn, label_text, key_type):
        """Wrap a keybind button in a labeled mini-card cell."""
        # ***<module>.SigmaWindow._kb_cell: Failure: Different bytecode
        w = QWidget()
        w.setStyleSheet('QWidget { background: #1a1a1a; border-radius: 10px; border: 1px solid #2a2a2a; } QLabel { border: none; background: transparent; } QPushButton { border-radius: 8px; }')
        vbox = QVBoxLayout(w)
        vbox.setSpacing(3)
        row = QHBoxLayout()
        lbl = QLabel(label_text.upper())
        lbl.setFont(QFont('Consolas', 7, QFont.Bold))
        lbl.setObjectName('qs_lbl')
        row.addWidget(lbl)
        row.addStretch()
        rem = QPushButton('✕')
        rem.setFont(QFont('Consolas', 7))
        rem.setFixedSize(18, 18)
        rem.setCursor(QCursor(Qt.PointingHandCursor))
        rem.setObjectName('remove_btn')
        rem.setStyleSheet('QPushButton { background: #5a1a1a; color: #FF4444; border: none; border-radius: 4px; padding: 0; } QPushButton:hover { background: #7a2222; color: #FF6666; } QPushButton:pressed { background: #8a2a2a; }')
        rem.setToolTip('Clear Key')
        rem.clicked.connect(lambda _, kt=key_type: self._remove_key(kt))
        row.addWidget(rem)
        vbox.addLayout(row)
        vbox.addWidget(btn)
        return w
    def _switch_tab(self, name):
        # ***<module>.SigmaWindow._switch_tab: Failure: Compilation Error
        self.active_tab = name
        t = self.T
        active = 'QPushButton {\n            background: #2A2A2A; color: #FFFFFF;\n            border: 1px solid #555555; border-left: 3px solid #888888;\n            border-radius: 8px; padding: 0 14px; text-align: left;\n            font-family: Consolas; font-size: 9pt;\n        }'
        inactive = f'QPushButton {\n            background: transparent; color: {t['muted']};\n            border: 1px solid #333333; border-left: 3px solid transparent;\n            border-radius: 8px; padding: 0 14px; text-align: left;\n            font-family: Consolas; font-size: 9pt;\n        }\n        QPushButton:hover { background: #222222; color: #FFFFFF; border-color: #555555; }'
        if name == 'keybinds':
            self.stack.setCurrentIndex(0)
            self.page_title.setText('CLASH')
            self.tab_keybinds_btn.setStyleSheet(active)
            self.tab_curve_btn.setStyleSheet(inactive)
        else:
            self.stack.setCurrentIndex(1)
            self.page_title.setText('CURVE')
            self.tab_curve_btn.setStyleSheet(active)
            self.tab_keybinds_btn.setStyleSheet(inactive)
    def _on_theme_changed(self, display_name):
        for k, v in THEME_NAMES.items():
            if v == display_name:
                self._apply_theme(k)
                break
    def _apply_theme(self, theme_key):
        # ***<module>.SigmaWindow._apply_theme: Failure: Compilation Error
        if theme_key not in THEMES:
            return None
        else:
            self.current_theme = theme_key
            t = THEMES[theme_key]
            self.T = t
            self.snow.set_bg(t['bg'])
            self.setStyleSheet(f'\n            /* Base */\n            QWidget { background: {t['bg']}; color: {t['text']}; font-family: Consolas; font-size: 10pt; }\n            QScrollArea, QStackedWidget { background: {t['bg']}; border: none; }\n            QLabel { background: transparent; }\n\n            /* Sidebar */\n            QWidget#sidebar    { background: {t['btn_bg']}; }\n            QWidget#sb_status  { background: {t['btn_bg']}; }\n\n            /* Sidebar section labels */\n            QLabel#nav_section_lbl {\n                color: {t['muted']}; background: {t['muted']};\n                letter-spacing: 2px; padding-left: 14px;\n            }\n\n            /* Sidebar quick-set labels */\n            QLabel#qs_lbl { color: {t['btn_bg']}; background: transparent; }\n\n            /* Topbar */\n            QWidget#topbar { background: {t['muted']}; }\n\n            /* Dividers */\n            QFrame#vline  { background: {t['hover']}; max-width: 1px; border: none; }\n            QFrame.divider, QFrame[objectName=\"divider\"] {\n                background: {t['btn_bg']}; color: {t['text']}; max-height: 1px; border: none;\n            }\n\n            /* Cards */\n            QFrame#card { background: {t['muted']}; border-radius: 8px; border: 1px solid #333333; }\n            QFrame#note_card { background: {t['muted']}; border-radius: 8px; border: 1px solid #B8580A; }\n\n            /* Card titles */\n            QLabel#card_title {\n                color: {t['; background: transparent;\n                letter-spacing: 2px; font-size: 8pt; font-weight: bold;\n            }\n\n            /* Default buttons */\n            QPushButton {\n                background: ']};\n                border: none; border-radius: 8px; padding: 4px 10px;\n            }\n            QPushButton:hover { background: #2A2A2A; color: #FFFFFF; }\n            QPushButton:pressed { background: #333333; }\n\n            /* Sidebar nav (base — overridden per-tab by _switch_tab) */\n            QPushButton[objectName^=\"nav_\"] {\n                background: transparent; color: {t[';\n                border: 1px solid #333333; border-left: 3px solid transparent;\n                border-radius: 8px; text-align: left; padding: 0 14px;\n            }\n            QPushButton[objectName^=\"nav_\"]:hover {\n                background: ']}44; color: {t['; border-color: #555555;\n            }\n\n            /* Discord button */\n            QPushButton#discord_btn {\n                background: transparent; color: #5865F2;\n                border: 1px solid #5865F2; border-radius: 4px; padding: 0 12px;\n                font-weight: bold;\n            }\n            QPushButton#discord_btn:hover { color: #5865F2; background: transparent; border: 2px solid #5865F2; }\n            QPushButton#discord_btn:pressed { color: #5865F2; background: transparent; border: 2px solid #5865F2; }\n\n            /* Remove buttons */\n            QPushButton#remove_btn {\n                background: transparent; color: ']};\n                border: none; border-radius: 8px; padding: 0;\n            }\n            QPushButton#remove_btn:hover { background: {t['red']}33; color: {t['; }\n\n            /* Inputs */\n            QLineEdit {\n                background: ']}accent{t[';\n                border: 1px solid ']}; border-radius: 8px; padding: 3px 6px;\n            }\n            QLineEdit:focus { border-color: {t['; }\n\n            /* Combos */\n            QComboBox {\n                background: ']};\n                border: 1px solid #FFFFFF; border-radius: 8px; padding: 2px 6px;\n                outline: none;\n            }\n            QComboBox:hover { border: 1px solid #AAAAAA; }\n            QComboBox:focus { border: 1px solid #FFFFFF; outline: none; }\n            QComboBox:on { border: 1px solid #FFFFFF; }\n            QComboBox QAbstractItemView {\n                background: {t[';\n                selection-background-color: #FFFFFF;\n                selection-color: white; border: 1px solid #FFFFFF;\n                outline: none; padding: 4px;\n            }\n            QComboBox QAbstractItemView::item {\n                padding: 6px 10px;\n                border-radius: 4px;\n                min-height: 24px;\n            }\n            QComboBox QAbstractItemView::item:hover {\n                background: #FFFFFF; color: #000000; border: 1px solid #FFFFFF; border-radius: 4px;\n            }\n            QComboBox QAbstractItemView::item:selected {\n                background: #FFFFFF; color: #000000; border: 1px solid #FFFFFF; border-radius: 4px;\n            }\n            QComboBox::drop-down { border: none; width: 16px; }\n            QComboBox::down-arrow { image: none; width: 0px; }\n\n            /* Sliders */\n            QSlider { background: transparent; }\n            QSlider::groove:horizontal {\n                background: #333333; height: 4px; border-radius: 2px;\n            }\n            QSlider::handle:horizontal {\n                background: ']}; width: 12px; height: 12px;\n                margin: -4px 0; border-radius: 6px;\n            }\n            QSlider::sub-page:horizontal {\n                background: {t['; border-radius: 2px;\n            }\n            QSlider::add-page:horizontal {\n                background: #333333; border-radius: 2px;\n            }\n\n            /* Scrollbars hidden */\n            QScrollBar:vertical   { width: 0px; }\n            QScrollBar:horizontal { height: 0px; }\n        ']}PgDn{t['End']}Home{t['Left']}Up{t['Right']}Down')
            if self.macro_system_enabled:
                self.status_lbl.setText('ACTIVE')
                self.header_w.setStyleSheet('background: #1a4a2a; border-radius: 8px;')
                self.status_lbl.setStyleSheet('background:transparent; color:white; letter-spacing:3px;')
            else:
                self.status_lbl.setText('INACTIVE')
                self.header_w.setStyleSheet('background: #7a1a1a; border-radius: 8px;')
                self.status_lbl.setStyleSheet('background:transparent; color:white; letter-spacing:3px;')
            for btn in [self.system_toggle_btn, self.macro_btn, self.spam_btn, self.hide_gui_btn, self.curve_key_btn, self.mouse_lock_btn]:
                btn.set_theme(t['hover'], t['hover'], t['accent'])
            for _, vl in self.chance_widgets.values():
                if vl:
                    vl.setStyleSheet(f'color:{t['text']}; background:{t['hover']}; border-radius:3px; padding:1px 3px;')
            self.cd_val_lbl.setStyleSheet(f'color:{t['text']}; background:{t['hover']}; border-radius:3px; padding:1px 3px;')
            t = self.T
            if self.randomize_angles:
                self.randomize_btn.setStyleSheet('QPushButton { background: transparent; color: #FFFFFF; border: 2px solid #2ecc71; border-radius: 8px; font-family: Consolas; font-size: 9pt; font-weight: bold; }QPushButton:hover { background: transparent; border-color: #27ae60; }')
            else:
                self.randomize_btn.setStyleSheet('QPushButton { background: transparent; color: #FFFFFF; border: 2px solid #FF5555; border-radius: 8px; font-family: Consolas; font-size: 9pt; font-weight: bold; }QPushButton:hover { background: transparent; border-color: #cc3333; }')
            self._switch_tab(self.active_tab)
    def _start_key_wait(self, key_type):
        if self.waiting_for_key:
            return None
        else:
            self.waiting_for_key = key_type
            btn_map = {'system': self.system_toggle_btn, 'macro': self.macro_btn, 'spam': self.spam_btn, 'hide_gui': self.hide_gui_btn, 'curve': self.curve_key_btn, 'mouse_lock': self.mouse_lock_btn}
            btn_map[key_type].set_waiting('#FFFFFF', '#2A2A2A')
    def _on_key_captured(self, key_type, vk):
        # ***<module>.SigmaWindow._on_key_captured: Failure: Different bytecode
        self.waiting_for_key = None
        btn_map = {'system': (self.system_toggle_btn, 'system_toggle_key'), 'macro': (self.macro_btn, 'macro_key'), 'spam': (self.spam_btn, 'spam_key'), 'hide_gui': (self.hide_gui_btn, 'hide_gui_key'), 'curve': (self.curve_key_btn, 'curve_key'), 'mouse_lock': (self.mouse_lock_btn, 'mouse_lock_key')}
        attr_map = {'system': 'system_toggle_key', 'macro': 'macro_key', 'spam': 'spam_key', 'hide_gui': 'hide_gui_key', 'curve': 'curve_key', 'mouse_lock': 'mouse_lock_key'}
        btn, attr = btn_map[key_type]
        if vk == (-1):
            btn.set_bound('Set Key...', '#FFFFFF')
            return None
        else:
            keybind_group = {'system': 'system_toggle_key', 'macro': 'macro_key', 'spam': 'spam_key', 'hide_gui': 'hide_gui_key'}
            curve_group = {'curve': 'curve_key', 'mouse_lock': 'mouse_lock_key'}
            if key_type in keybind_group:
                group = keybind_group
            else:
                group = curve_group
            for other_type, other_attr in group.items():
                if other_type!= key_type and getattr(self, other_attr) == vk:
                        btn.setText('Key Already Binded!')
                        btn.setStyleSheet('QPushButton { background: #3a1a1a; color: #FF4444; border: 1px solid #FF4444; border-radius: 8px; font-family: Consolas; font-size: 9pt; font-weight: bold; padding: 10px; outline: none; }')
                        QTimer.singleShot(1500, lambda b=btn: b.set_bound('Set Key...', '#FFFFFF'))
                        return
            setattr(self, attr, vk)
            btn.set_bound(get_key_name(vk), '#FFFFFF')
    def _remove_key(self, key_type):
        btn_map = {'system': (self.system_toggle_btn, 'system_toggle_key'), 'macro': (self.macro_btn, 'macro_key'), 'spam': (self.spam_btn, 'spam_key'), 'hide_gui': (self.hide_gui_btn, 'hide_gui_key'), 'curve': (self.curve_key_btn, 'curve_key'), 'mouse_lock': (self.mouse_lock_btn, 'mouse_lock_key')}
        btn, attr = btn_map[key_type]
        setattr(self, attr, None)
        btn.set_bound('Set Key...', '#FFFFFF')
    def _on_status_changed(self, enabled):
        if enabled:
            self.status_lbl.setText('ACTIVE')
            self.header_w.setStyleSheet('background: #1a4a2a; border-radius: 8px;')
            self.status_lbl.setStyleSheet('background:transparent; color:white; letter-spacing:3px;')
        else:
            self.status_lbl.setText('INACTIVE')
            self.header_w.setStyleSheet('background: #7a1a1a; border-radius: 8px;')
            self.status_lbl.setStyleSheet('background:transparent; color:white; letter-spacing:3px;')
    def _toggle_gui_visibility(self):
        self.gui_visible = not self.gui_visible
        if self.gui_visible:
            self.show()
        else:
            self.hide()
    def _on_macro_toggle(self, state):
        if state:
            if self._spam_thread and self._spam_thread.isRunning():
                    return None
            self._spam_thread = SpamThread(self)
            self._spam_thread.start()
        else:
            self.toggled = False
    def _on_mouse_lock(self, state):
        if state:
            if self._lock_thread and self._lock_thread.isRunning():
                    return None
            self._lock_thread = MouseLockThread(self)
            self._lock_thread.start()
            try:
                user32.MessageBeep(64)
            except:
                return None
        else:
            self.mouse_locked = False
            try:
                user32.MessageBeep(16)
            except:
                return None
    def _do_camera_flick(self):
        # irreducible cflow, using cdg fallback
        # ***<module>.SigmaWindow._do_camera_flick: Failure: Compilation Error
        SetThreadPriority(GetCurrentThread(), 2)
                if self.window_mode == 'roblox' and (not is_roblox_game_window()):
                        return None
                try:
                    for key, (sl, _) in self.chance_widgets.items():
                        setattr(self, f'chance_{key}', sl.value())
                except RuntimeError:
                    pass
                enabled_angles = []
                if self.curve_vertical_enabled:
                    enabled_angles.append(('vertical', (-1), self.fspeed_vertical))
                if self.curve_backward_enabled:
                    enabled_angles.append(('backward', 1, self.fspeed_backward))
                if self.curve_lside_enabled:
                    enabled_angles.append(('lside', (-1), self.fspeed_lside))
                if self.curve_rside_enabled:
                    enabled_angles.append(('rside', 1, self.fspeed_rside))
                if not enabled_angles:
                    return None
                else:
                    if not self.randomize_angles:
                        return None
                    else:
                        angle_pool, weights = ([], [])
                        if self.curve_vertical_enabled and self.chance_vertical > 0:
                                angle_pool.append(('vertical', (-1), self.fspeed_vertical))
                                weights.append(self.chance_vertical)
                        if self.curve_backward_enabled and self.chance_backward > 0:
                                angle_pool.append(('backward', 1, self.fspeed_backward))
                                weights.append(self.chance_backward)
                        if self.curve_lside_enabled and self.chance_lside > 0:
                                angle_pool.append(('lside', (-1), self.fspeed_lside))
                                weights.append(self.chance_lside)
                        if self.curve_rside_enabled and self.chance_rside > 0:
                                angle_pool.append(('rside', 1, self.fspeed_rside))
                                weights.append(self.chance_rside)
                        if not angle_pool:
                            return None
                        else:
                            angles_to_use = [random.choices(angle_pool, weights=weights, k=1)[0]]
                            avg_fspeed = sum((fs for _, _, fs in angles_to_use)) / len(angles_to_use)
                            if avg_fspeed < 1:
                                avg_fspeed = 1
                            hold_duration = 0.005 + (avg_fspeed - 1) * 0.12375
                            pre_delay = hold_duration * 0.4
                            post_delay = hold_duration * 0.7
                            screen_width = user32.GetSystemMetrics(0)
                            screen_height = user32.GetSystemMetrics(1)
                            move_x, move_y = (0, 0)
                            has_vertical = False
                            for angle_type, direction, _ in angles_to_use:
                                if angle_type == 'vertical':
                                    move_y += int(screen_height * 0.35 * direction)
                                    has_vertical = True
                                else:
                                    if angle_type == 'backward':
                                        move_x += int(screen_width * 1.4)
                                    else:
                                        if angle_type == 'lside':
                                            move_x -= int(screen_width * 1.5)
                                        else:
                                            if angle_type == 'rside':
                                                move_x += int(screen_width * 1.5)
                            MOUSEEVENTF_MOVE = 1
                            MOUSEEVENTF_RIGHTDOWN = 8
                            MOUSEEVENTF_RIGHTUP = 16
                            VK_RBUTTON = 2
                            user_was_holding_rmb = GetAsyncKeyState(VK_RBUTTON) & 32768
                            try:
                                right_up_pre = INPUT()
                                right_up_pre.type = 0
                                right_up_pre.union.mi.dwFlags = MOUSEEVENTF_RIGHTUP
                                SendInput(1, ctypes.byref(right_up_pre), ctypes.sizeof(INPUT))
                                time.sleep(0.005)
                                right_down = INPUT()
                                right_down.type = 0
                                right_down.union.mi.dwFlags = MOUSEEVENTF_RIGHTDOWN
                                SendInput(1, ctypes.byref(right_down), ctypes.sizeof(INPUT))
                                time.sleep(pre_delay)
                                move_input = INPUT()
                                move_input.type = 0
                                move_input.union.mi.dx = move_x
                                move_input.union.mi.dy = move_y
                                move_input.union.mi.dwFlags = MOUSEEVENTF_MOVE
                                SendInput(1, ctypes.byref(move_input), ctypes.sizeof(INPUT))
                                time.sleep(hold_duration)
                                time.sleep(0.02)
                                return_input = INPUT()
                                return_input.type = 0
                                return_input.union.mi.dx = -move_x
                                return_input.union.mi.dy = -move_y
                                return_input.union.mi.dwFlags = MOUSEEVENTF_MOVE
                                SendInput(1, ctypes.byref(return_input), ctypes.sizeof(INPUT))
                                time.sleep(post_delay)
                            finally:
                                for _ in range(3):
                                    right_up = INPUT()
                                    right_up.type = 0
                                    right_up.union.mi.dwFlags = MOUSEEVENTF_RIGHTUP
                                    SendInput(1, ctypes.byref(right_up), ctypes.sizeof(INPUT))
                                    time.sleep(0.005)
                                if user_was_holding_rmb:
                                    time.sleep(0.01)
                                    right_down_restore = INPUT()
                                    right_down_restore.type = 0
                                    right_down_restore.union.mi.dwFlags = MOUSEEVENTF_RIGHTDOWN
                                    SendInput(1, ctypes.byref(right_down_restore), ctypes.sizeof(INPUT))
                pass
    def _toggle_randomize(self):
        self.randomize_angles = not self.randomize_angles
        t = self.T
        if self.randomize_angles:
            self.randomize_btn.setText('  Disable Randomizer')
            self.randomize_btn.setStyleSheet('QPushButton { background: transparent; color: #FFFFFF; border: 2px solid #2ecc71; border-radius: 8px; font-family: Consolas; font-size: 9pt; font-weight: bold; }QPushButton:hover { background: transparent; border-color: #27ae60; }')
        else:
            self.randomize_btn.setText('  Enable Randomizer')
            self.randomize_btn.setStyleSheet('QPushButton { background: transparent; color: #FFFFFF; border: 2px solid #FF5555; border-radius: 8px; font-family: Consolas; font-size: 9pt; font-weight: bold; }QPushButton:hover { background: transparent; border-color: #cc3333; }')
    def _on_fs_slider(self, v):
        self.global_flick_speed = v
        self.fspeed_vertical = self.fspeed_backward = self.fspeed_lside = self.fspeed_rside = v
    def _on_cd_slider(self, v):
        self.flick_cooldown = round(v * 0.01, 2)
        self.cd_val_lbl.setText(f'{self.flick_cooldown:.2f}s')
    def _adj_fs(self, delta):
        v = max(0, min(100, self.global_flick_speed + delta))
        self.fs_slider.setValue(v)
    def _edit_fs_inline(self):
        return None
    def _adj_cooldown(self, delta):
        v = max(0, min(500, self.cd_slider.value() + int(delta * 100)))
        self.cd_slider.setValue(v)
    def _inline_input(self, label_text, default_text):
        # ***<module>.SigmaWindow._inline_input: Failure: Different bytecode
        from PyQt5.QtWidgets import QInputDialog
        t = self.T
        dialog = QInputDialog(self)
        dialog.setWindowTitle('Edit Value')
        dialog.setLabelText(label_text)
        dialog.setTextValue(default_text)
        dialog.setStyleSheet(f'\n            QDialog { background: {t['btn_bg']}; color: {t['text']}; }\n            QLabel { color: {t['text']}; background: transparent; }\n            QLineEdit { background: {t['bg']}; color: {t['accent']}; border: 1px solid {t['accent']}55; border-radius: 8px; padding: 4px; }\n            QPushButton { background: {t['accent']}; color: white; border: none; border-radius: 8px; padding: 6px 16px; font-family: Consolas; }\n            QPushButton:hover { background: #2A2A2A; color: #FFFFFF; }\n        ')
        ok = dialog.exec_()
        return (dialog.textValue(), ok)
    def _on_kps_entry(self, text):
        # irreducible cflow, using cdg fallback
        # ***<module>.SigmaWindow._on_kps_entry: Failure: Compilation Error
        v = int(text)
        if v > 5000:
            v = 5000
            self.kps_entry.blockSignals(True)
            self.kps_entry.setText('5000')
            self.kps_entry.setCursorPosition(4)
            self.kps_entry.blockSignals(False)
        if 0 <= v <= 5000:
                self.cps = v
                self.kps_slider.blockSignals(True)
                self.kps_slider.setValue(v)
                self.kps_slider.blockSignals(False)
                    return None
    def _on_kps_slider(self, value):
        self.cps = value
        self.kps_entry.blockSignals(True)
        self.kps_entry.setText(str(value))
        self.kps_entry.blockSignals(False)
    def _copy_discord(self):
        # ***<module>.SigmaWindow._copy_discord: Failure: Different bytecode
        link = 'https://discord.gg/TNtw9MAShQ'
        QApplication.clipboard().setText(link)
        self.discord_btn.setText('Copied!')
        self.discord_btn.setStyleSheet('QPushButton { background: transparent; color: #27ae60; border: 2px solid #27ae60; border-radius: 4px; padding: 0 12px; font-weight: bold; }QPushButton:hover { background: transparent; color: #27ae60; border: 2px solid #27ae60; }')
        QTimer.singleShot(1500, lambda: (self.discord_btn.setText('Discord'), self.discord_btn.setStyleSheet('QPushButton { background: transparent; color: #5865F2; border: 1px solid #5865F2; border-radius: 4px; padding: 0 12px; font-weight: bold; } QPushButton:hover { color: #5865F2; background: transparent; border: 2px solid #5865F2; } QPushButton:pressed { color: #5865F2; background: transparent; border: 2px solid #5865F2; }')))
    def _save_settings(self):
        # irreducible cflow, using cdg fallback
        # ***<module>.SigmaWindow._save_settings: Failure: Compilation Error
        t = self.T
        path, _ = QFileDialog.getSaveFileName(self, 'Save Settings', '', 'JSON files (*.json)')
        if not path:
            return None
        else:
            return {'cps': self.cps, 'mode': self.mode, 'action_mode': self.action_mode, 'mouse_button': self.mouse_button, 'window_mode': self.window_mode, 'theme': self.current_theme, 'spam_key': self.macro_key, 'hide_gui_key': self.hide_gui_key, 'curve_key': self.curve_key, 'mouse_lock_key': self.mouse_lock_key, 'curve_vertical_enabled': self.curve_vertical_enabled, 'curve_backward_enabled': self.curve_backward_enabled, 'curve_lside_enabled': self.curve_lside_enabled, 'curve_rside_enabled': self.curve_rside_enabled, 'randomize_angles': self.randomize_angles, 'global_flick_speed': self.global_flick_speed, 'fspeed_vertical': self.fspeed_vertical, 'fspeed_backward': self.fspeed_backward, 'fspeed_lside': self.fspeed_lside, 'fspeed_rside': self.fspeed_rside, 'flick_cooldown': self.flick_cooldown, 'chance_vertical': self.chance_vertical, 'chance_backward': self.chance_backward, 'chance_lside': self.chance_lside, 'chance_rside': self.chance_rside, 'macro_system_enabled': self.macro_system_enabled,
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
            user32.MessageBeep(64)
                    return None
                            user32.MessageBeep(16)
                                    return None
    def _load_settings(self):
        # irreducible cflow, using cdg fallback
        # ***<module>.SigmaWindow._load_settings: Failure: Compilation Error
        path, _ = QFileDialog.getOpenFileName(self, 'Load Settings', '', 'JSON files (*.json)')
        if not path:
            return None
        with open(path, 'r') as f:
            data = json.load(f)
            if 'cps' in data:
                self.cps = data['cps']
            if 'mode' in data:
                self.mode = data['mode']
            if 'action_mode' in data:
                self.action_mode = data['action_mode']
            if 'window_mode' in data:
                self.window_mode = data['window_mode']
            if 'mouse_button' in data:
                self.mouse_button = data['mouse_button']
            if 'global_flick_speed' in data:
                self.global_flick_speed = data['global_flick_speed']
                self.fspeed_vertical = self.fspeed_backward = self.fspeed_lside = self.fspeed_rside = self.global_flick_speed
            if 'flick_cooldown' in data:
                self.flick_cooldown = data['flick_cooldown']
            for attr in ['fspeed_vertical', 'fspeed_backward', 'fspeed_lside', 'fspeed_rside']:
                if attr in data:
                    setattr(self, attr, data[attr])
            for key in ['chance_vertical', 'chance_backward', 'chance_lside', 'chance_rside']:
                if key in data:
                    setattr(self, key, data[key])
            if 'macro_system_enabled' in data:
                self.macro_system_enabled = data['macro_system_enabled']
            assert all((k in data for k in ('window_x', 'window_y', 'window_width', 'window_height') for k in ('window_x', 'window_y', 'window_width', 'window_height')))
                self.setGeometry(data['window_x'], data['window_y'], data['window_width'], data['window_height'])
            key_attrs = {'spam_key': 'spam_key', 'system_toggle_key': 'system_toggle_key', 'macro_key': 'macro_key', 'hide_gui_key': 'hide_gui_key', 'curve_key': 'curve_key', 'mouse_lock_key': 'mouse_lock_key'}
            for key, attr in key_attrs.items():
                if key in data:
                    setattr(self, attr, data[key])
            if 'randomize_angles' in data:
                self.randomize_angles = data['randomize_angles']
            QTimer.singleShot(0, lambda: self._apply_loaded_settings(data))
                user32.MessageBeep(16)
                        pass
                        return None
    def _apply_loaded_settings(self, data):
        """Update all widgets after state has been loaded."""
        # ***<module>.SigmaWindow._apply_loaded_settings: Failure: Different control flow
        def safe_set(fn):
            # irreducible cflow, using cdg fallback
            # ***<module>.SigmaWindow._apply_loaded_settings.safe_set: Failure: Compilation Error
            fn()
                except RuntimeError:
                        return None
        safe_set(lambda: self.kps_entry.setText(str(self.cps)))
        safe_set(lambda: self.kps_slider.setValue(int(self.cps)))
        safe_set(lambda: self.mode_combo.setCurrentText(self.mode.capitalize()))
        safe_set(lambda: self.action_combo.setCurrentText(self.action_mode.upper()))
        safe_set(lambda: self.target_combo.setCurrentText('Roblox' if self.window_mode == 'roblox' else 'Global'))
        btn_map = {'spam_key': self.spam_btn, 'system_toggle_key': self.system_toggle_btn, 'macro_key': self.macro_btn, 'hide_gui_key': self.hide_gui_btn, 'curve_key': self.curve_key_btn, 'mouse_lock_key': self.mouse_lock_btn}
        for attr, btn in btn_map.items():
            vk = getattr(self, attr, None)
            safe_set(lambda b=btn, v=vk: b.set_bound(get_key_name(v) if v is not None else 'Set Key...', '#FFFFFF'))
        self.randomize_angles = not self.randomize_angles
        try:
            self._toggle_randomize()
        except RuntimeError:
            pass
        safe_set(lambda: self.fs_slider.setValue(int(self.global_flick_speed)))
        safe_set(lambda: self.fspd_slider.setValue(int(self.global_flick_speed)))
        safe_set(lambda: self.cd_slider.setValue(int(self.flick_cooldown * 100)))
        for key in ['chance_vertical', 'chance_backward', 'chance_lside', 'chance_rside']:
            angle = key.replace('chance_', '')
            if angle in self.chance_widgets:
                sl, vl = self.chance_widgets[angle]
                v = getattr(self, key, 0)
                safe_set(lambda s=sl, val=v: s.setValue(val))
        safe_set(lambda: self._chance_bubble.hide())
        if self.macro_system_enabled:
            safe_set(lambda: self.status_lbl.setText('ACTIVE'))
            safe_set(lambda: self.header_w.setStyleSheet('background: #1a4a2a; border-radius: 8px;'))
            safe_set(lambda: self.status_lbl.setStyleSheet('background:transparent; color:white; letter-spacing:3px;'))
        else:
            safe_set(lambda: self.status_lbl.setText('INACTIVE'))
            safe_set(lambda: self.header_w.setStyleSheet('background: #7a1a1a; border-radius: 8px;'))
            safe_set(lambda: self.status_lbl.setStyleSheet('background:transparent; color:white; letter-spacing:3px;'))
        if 'active_tab' in data:
            pass
        safe_set(lambda: self._switch_tab(data['active_tab']))
        try:
            user32.MessageBeep(64)
        except:
            return None
    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'snow') and self.centralWidget():
                cw = self.centralWidget()
                self.snow.setGeometry(0, 0, cw.width(), cw.height())
    def closeEvent(self, e):
        # ***<module>.SigmaWindow.closeEvent: Failure: Different bytecode
        self.running = False
        self.toggled = False
        self.mouse_locked = False
        if hasattr(self, '_key_thread'):
            self._key_thread.stop()
            self._key_thread.wait(500)
        try:
            winmm.timeEndPeriod(1)
            NtSetTimerResolution(0, False, ctypes.byref(self.current_resolution))
        except:
            pass
        e.accept()
if __name__ == '__main__':
    if sys.platform!= 'win32':
        print('This script only works on Windows!')
        sys.exit(1)
    app = QApplication(sys.argv)
    app.setStyle(InstantTooltipStyle('Fusion'))
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor('#111111'))
    palette.setColor(QPalette.WindowText, QColor('#FFFFFF'))
    palette.setColor(QPalette.Base, QColor('#1E1E1E'))
    palette.setColor(QPalette.AlternateBase, QColor('#2A2A2A'))
    palette.setColor(QPalette.ToolTipBase, QColor('#1E1E1E'))
    palette.setColor(QPalette.ToolTipText, QColor('#FFFFFF'))
    palette.setColor(QPalette.Text, QColor('#FFFFFF'))
    palette.setColor(QPalette.Button, QColor('#1E1E1E'))
    palette.setColor(QPalette.ButtonText, QColor('#FFFFFF'))
    palette.setColor(QPalette.Highlight, QColor('#3A3A3A'))
    palette.setColor(QPalette.HighlightedText, QColor('#FFFFFF'))
    palette.setColor(QPalette.Link, QColor('#FFFFFF'))
    palette.setColor(QPalette.BrightText, QColor('#FFFFFF'))
    app.setPalette(palette)
    QToolTip.setFont(QFont('Consolas', 9))
    QApplication.setEffectEnabled(Qt.UI_AnimateTooltip, False)
    app.setStyleSheet('\n        QToolTip {\n            background: #1F1F23; color: #EFEFF1;\n            border: 1px solid #444;\n            font-family: Consolas; font-size: 9pt;\n            padding: 4px 8px;\n            opacity: 255;\n        }\n        QPushButton { outline: none; }\n        QPushButton:focus { outline: none; }\n        QPushButton:pressed { outline: none; }\n        *:focus { outline: none; }\n    ')
    win = SigmaWindow()
    win.show()
    _tip = TrackingTooltip()
    _filter = TooltipFilter(_tip)
    app.installEventFilter(_filter)
    sys.exit(app.exec_())
