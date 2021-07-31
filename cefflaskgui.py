from cefpython3 import cefpython as cef
from flask import *
import threading
import platform
import sys

class thread_with_trace(threading.Thread): 
    def __init__(self, *args, **keywords): 
        threading.Thread.__init__(self, *args, **keywords) 
        self.killed = False
  
    def start(self): 
        self.__run_backup = self.run 
        self.run = self.__run       
        threading.Thread.start(self) 
  
    def __run(self): 
        sys.settrace(self.globaltrace) 
        self.__run_backup() 
        self.run = self.__run_backup 
  
    def globaltrace(self, frame, event, arg): 
        if event == 'call': 
            return self.localtrace 
        else: 
            return None

    def localtrace(self, frame, event, arg): 
        if self.killed: 
            if event == 'line': 
                raise SystemExit() 
        return self.localtrace 
  
    def kill(self): 
        self.killed = True

class cefflaskgui:
    app = None
    port = 5000
    title = "cefflaskgui"

    def run(app=None, title=None, port=None):
        if(title != None):
            cefflaskgui.title = title

        if(port != None):
            cefflaskgui.port = port

        if(app == None and cefflaskgui.app != None):
            flaskThread = thread_with_trace(target=cefflaskgui.app.run, kwargs={"port": cefflaskgui.port})
            flaskThread.start()
            main(fThread=flaskThread)
        elif(app != None):
            flaskThread = thread_with_trace(target=app.run, kwargs={"port": cefflaskgui.port})
            flaskThread.start()
            main(fThread=flaskThread)
        else:
            raise NameError("Flask App is needed to run (hint: cefflaskgui.app = flaskapp OR run(app=flaskapp))")

def main(fThread):
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    cef.CreateBrowserSync(url=f"http://127.0.0.1:{cefflaskgui.port}",
                          window_title=cefflaskgui.title)
    cef.MessageLoop()
    cef.Shutdown()
    fThread.kill()
    exit()
    