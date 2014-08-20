import sys
from wxPython.wx import wxConfig
import urllib2, xml.dom.minidom
import MultipartPostHandler
from ProxyHTTPConnection import ConnectHTTPSHandler

#apiurl = "http://localhost/api/usernam/password/upload?
#  u=http://localhost/img/147025813695-medium.jpg"
#apiurl = "http://localhost/api?user=usernam&password=password&
#  method=upload&u=http://localhost/img/147025813695-medium.jpg"

#class Callable:
#    def __init__(self, anycallable):
#        self.__call__ = anycallable

class Connect:
  
   def __init__ (self):
     self.user = '' 
     self.password = '' 
     self.error = 0 
     self.config = None
     self.API_URL = None
     self.PROXY_STRING = ''

     self.sysconfig = wxConfig()
     proxy = self.sysconfig.Read('proxy', '')
     port  = self.sysconfig.Read('port', '')
     if len(proxy) > 0 or len(port) > 0:
        self.setProxy(proxy + ':' + port)


   def setAccess(self, user, password):
      self.user = user
      self.password = password
     
   def setConfig(self, config):
      self.config = config
      self.API_URL = self.config.getAPI()
     
   def setProxy(self, proxy):
      if len(proxy) > 2: 	#FIXME add proper check
         self.PROXY_STRING = proxy 

   def doConnect(self, params, type, value):

      uploader = 'Mytago Uploader ' + self.config.version;
      headers = { 'User-Agent' : uploader }
      connected = False
      self.error = 0 

      params["uploader"] = self.config.version

      try:
         opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
         urllib2.install_opener(opener)
         req = urllib2.Request(self.API_URL, params, headers)
         response = urllib2.urlopen(req).read().strip()
         connected = True
      except:
         self.error = 1001

      if not connected and len(self.PROXY_STRING) > 2: #FIXME add proper check
         try:
            opener = urllib2.build_opener(ConnectHTTPSHandler, MultipartPostHandler.MultipartPostHandler)
            urllib2.install_opener(opener)
            req = urllib2.Request(self.API_URL, params, headers)
            req.set_proxy(self.PROXY_STRING, 'https')
            response = urllib2.urlopen(req).read().strip()
            connected = True
         except:
            self.error = 1002

      #print response 

      if not connected:
         return False 
      elif len(response) < 1:
         self.error = 1003
         return False 
      else:
         try:
            xdom = xml.dom.minidom.parseString(response)
            tagids = xdom.getElementsByTagName(type)
            if tagids.length > 0: 
      	      for tagid in tagids:
	         for element in tagid.childNodes:
	            if element.nodeValue == value:
                       return True 
            else:
               self.error = 1004
               errors = xdom.getElementsByTagName('error')
               if errors.length > 0: 
                   for error in errors:
                      for element in error.childNodes:
                          self.error =  element.nodeValue
         except:
            self.error = 1005
      return False 


   def testConnect(self):
      params = {'method':'ping'}
      return self.doConnect(params, 'ping', 'pong')


   def testAccess(self):
      if len(self.user) < 1 or len(self.password) < 1:
         self.error = 1001
         return False  

      params = {'user':self.user,'password':self.password,'method':'ping'}
      return self.doConnect(params, 'ping', 'pong')

   
   def getError(self):
      return self.error
