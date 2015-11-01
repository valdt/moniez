#http://www.google.com/finance/info?q=NASDAQ%3aSTO:VOLV-B
import time,sys,socket,nmap, pyHook

def OnKeyboardEvent:
	
	
	
h = pyHook.HookManager()
h.keyDown = onKeyboardEvent
h.hookKeyboard()
pythoncom.PumpMessages