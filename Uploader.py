import sys
import wx
import urllib2, xml.dom.minidom
import MultipartPostHandler
from ProxyHTTPConnection import ProxyHTTPConnection, ConnectHTTPHandler, ConnectHTTPSHandler
import time
from threading import *

#apiurl = "http://localhost/api/usernam/password/upload?
#  u=http://localhost/img/147025813695-medium.jpg"
#apiurl = "http://localhost/api?user=usernam&password=password&
#  method=upload&u=http://localhost/img/147025813695-medium.jpg"

# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()

def EVT_RESULT(win, func):
   win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
   def __init__(self, data):
      """Init Result Event."""
      wx.PyEvent.__init__(self)
      self.SetEventType(EVT_RESULT_ID)
      self.data = data

class Uploader:
  
   def __init__ (self):
     self.user = '' 
     self.password = '' 
     self.win = None 
     self.config = None
     self.API_URL = None
     self.PROXY_STRING = ''
     self.result = False

   def setWindow(self, win):
      self.win = win
      # Set up event handler for any worker thread results
      EVT_RESULT(self.win, self.win.OnResult)
      # And indicate we don't have a worker thread yet
      self.worker = None

   def setAccess(self, user, password):
      self.user = user
      self.password = password
     
   def setApiurl(self, url):
      self.API_URL = url
     
   def setProxy(self, proxy):
      self.PROXY_STRING = proxy 

   def setConnector(self, connector):
      self.connector = connector 

   def setConfig(self, config):
      self.config = config 
      self.API_URL = self.config.getAPI()

   def abortUpload(self):
      self.worker.abort()

   def uploadFiles(self, files):
      self.result = False
      if not self.worker:
            self.worker = WorkerThread(self.win)
      self.worker.setData(self.config, self.connector, self.user, self.password, files)
      self.worker.start()

   def closeThread(self):
        self.worker = None

# Thread class that executes processing
class WorkerThread(Thread):
    def __init__(self, notify_window):
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0

        self.params = None
        self.connector = None
	self.user = None
        self.password = None
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this

        #self.start()

    def setData(self, config, connector, user, password, files):
        self.config = config
        self.connector = connector
	self.user = user
        self.password = password
        self.files = files 

    def run(self): 
        count = 1
        failed = False
        for button in self.files:
           wx.PostEvent(self._notify_window, ResultEvent(count))
           if self.uploadFile(button.GetToolTip().GetTip()):
              wx.PostEvent(self._notify_window, ResultEvent(count))
              count += 1
           else:
              wx.PostEvent(self._notify_window, ResultEvent(None))
              failed = True
              break

	if not failed:
        	wx.PostEvent(self._notify_window, ResultEvent(0))

    def uploadFile(self, file): 
        if self.config.debug: print "Uploading: %s" % file
        try:
            upfile = file
            if self._want_abort: return False

            img = wx.Image(file, wx.BITMAP_TYPE_ANY)
            if self._want_abort: return False

            limitsize = self.config.limitSize(img.GetWidth(), img.GetHeight())
            if limitsize[0] and limitsize[1]:
               if limitsize[0] != img.GetWidth() or limitsize[1] != img.GetHeight():

                  img.Rescale(limitsize[0], limitsize[1])

                  if self._want_abort: return False

                  upfile = self.config.getUpTempFile()

                  if self._want_abort: return False

                  if not img.SaveFile(upfile, wx.BITMAP_TYPE_JPEG): #FIXME ANY IMAGE TYPE
                     wx.PostEvent(self._notify_window, ResultEvent(None))
                     return False

            if self._want_abort: return False

            params = {'user':self.user,'password':self.password,'method':'upload','f':open(upfile, 'rb')}
            if self.connector.doConnect(params, 'status', 'OK'):
               return True
            else:
               if self.config.debug: print "Upload Error %s" % self.connector.getError()
               return False
        except:
            return False

        return False

    def abort(self):
        # Method for use by main thread to signal an abort
        self._want_abort = 1
