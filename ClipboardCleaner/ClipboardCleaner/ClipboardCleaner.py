import os
import sys
import ctypes
from ctypes import wintypes
import win32con
import win32clipboard

byref = ctypes.byref
user32 = ctypes.windll.user32

HOTKEYS = {
  1 : (0x56, win32con.MOD_SHIFT | win32con.MOD_CONTROL)
}

def handle_hotkey ():
  win32clipboard.OpenClipboard()
  try:
    data = win32clipboard.GetClipboardData()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(data)
  finally:
    win32clipboard.CloseClipboard()
    raw_input()

HOTKEY_ACTIONS = {
  1 : handle_hotkey
}

for id, (vk, modifiers) in HOTKEYS.items ():
  print "Registering id", id, "for key", vk
  if not user32.RegisterHotKey (None, id, modifiers, vk):
    print "Unable to register id", id

try:
  msg = wintypes.MSG ()
  while user32.GetMessageA (byref (msg), None, 0, 0) != 0:
    if msg.message == win32con.WM_HOTKEY:
      action_to_take = HOTKEY_ACTIONS.get (msg.wParam)
      if action_to_take:
        action_to_take ()

    user32.TranslateMessage (byref (msg))
    user32.DispatchMessageA (byref (msg))

finally:
  for id in HOTKEYS.keys ():
    user32.UnregisterHotKey (None, id)