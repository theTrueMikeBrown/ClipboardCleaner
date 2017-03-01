#add configuration
#make it work as a system tray thing
#pyw if it shows an unwanted window
import os
import sys
import ctypes
from ctypes import wintypes
import win32con
import win32clipboard

byref = ctypes.byref
user32 = ctypes.windll.user32
hotkeyId = 1

def handle_hotkey ():    
  win32clipboard.OpenClipboard()
  try:
    data = win32clipboard.GetClipboardData()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(data)
  finally:
    win32clipboard.CloseClipboard()

def reg_hotkey ():
  if not user32.RegisterHotKey (None, hotkeyId, win32con.MOD_SHIFT | win32con.MOD_CONTROL, 0x56):
    print "Unable to register id", id
    
reg_hotkey ()
try:
  msg = wintypes.MSG ()
  while user32.GetMessageA (byref (msg), None, 0, 0) != 0:
    if msg.message == win32con.WM_HOTKEY:            
      if msg.wParam == hotkeyId:
        handle_hotkey ()  

    user32.TranslateMessage (byref (msg))
    user32.DispatchMessageA (byref (msg))

finally:    
  user32.UnregisterHotKey (None, 1)