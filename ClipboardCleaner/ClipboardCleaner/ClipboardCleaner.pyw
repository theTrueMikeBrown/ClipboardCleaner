import os
import sys
import ctypes
from ctypes import wintypes
import win32con
import win32clipboard
import SysTrayIcon
try:
    import winxpgui as win32gui
except ImportError:
    import win32gui
    
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
    

if __name__ == '__main__':
  done = True
  def bye(sysTrayIcon):
    global done
    done = True    

  def quit(sysTrayIcon):
    global done
    done = True 
    user32.UnregisterHotKey (None, 1)   

  def run(sysTrayIcon):        
    global done
    if done == True:
      done = False
      print "turning on"    
      reg_hotkey ()
      try:
        msg = wintypes.MSG ()
        while user32.GetMessageA (byref (msg), None, 0, 0) != 0 and done == False:
          if msg.message == win32con.WM_HOTKEY and msg.wParam == hotkeyId:
            handle_hotkey ()  
      
          user32.TranslateMessage (byref (msg))
          user32.DispatchMessageA (byref (msg))
            
      finally:    
        print "finally"
    else:
      done = True
      print "turning off"   
      user32.UnregisterHotKey (None, 1)

  menu_options = (('Start', None, run),
                  ('Stop', None, quit), )
  SysTrayIcon.SysTrayIcon('clipboard.ico', 'Clipboard Cleaner', menu_options, on_quit=bye, default_menu_index=0)
