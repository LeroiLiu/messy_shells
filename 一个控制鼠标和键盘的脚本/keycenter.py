#coding:utf-8
#随机移动鼠标操作，需使用到三方库为：pywin32、pyhook、PyMouse
# from pymouse import *
# from pykeyboard import *

# class TapRecord(PyKeyboardEvent):
#   def __init__(self):
#     PyKeyboardEvent.__init__(self)
 
#   def tap(self, keycode, character, press):
#   	try:
#   		if keycode==75:
# 			print(keycode)
# 			m = PyMouse()
# 			m.position()
# 			x_dim, y_dim = m.screen_size()
# 			m.move(x_dim/2, y_dim/2)
#   	except Exception as e:
#   		pass

# t = TapRecord()
# t.run()
from pymouse import *
import pyHook


def OnKeyboardEvent(event):
	if event.KeyID==75:
		m = PyMouse()
		m.position()
		x_dim, y_dim = m.screen_size()
		m.move(x_dim/2, y_dim/2)
  # print 'MessageName:',event.MessageName
  # print 'Message:',event.Message
  # print 'Time:',event.Time
  # print 'Window:',event.Window
  # print 'WindowName:',event.WindowName
  # print 'Ascii:', event.Ascii, chr(event.Ascii)
  # print 'Key:', event.Key
  # print 'KeyID:', event.KeyID
  # print 'ScanCode:', event.ScanCode
  # print 'Extended:', event.Extended
  # print 'Injected:', event.Injected
  # print 'Alt', event.Alt
  # print 'Transition', event.Transition
  # print '---'

  # return True to pass the event to other handlers
  # return False to stop the event from propagating
		return True

# create the hook mananger
hm = pyHook.HookManager()
# register two callbacks
hm.KeyDown = OnKeyboardEvent

# hook into the mouse and keyboard events
hm.HookKeyboard()

if __name__ == '__main__':
  import pythoncom
  pythoncom.PumpMessages()