# All configuration goes here

import os
import wx
 
class Config:

    def __init__(self):

       self.debug = False
       self.version = '1.02.43'
       self.config = wx.Config()
       self.stdpaths = wx.StandardPaths.Get() 
       self.URL = "https://www.mytago.com/api"
       self.TILE_W = 150
       self.TILE_H = 113
       self.LIMIT_W = 800 
       self.LIMIT_H = 800
       self.TILE_BORDER = 20
       self.TMP_FILE = '_tmp_.jpg'

       self.LAST_PATH = self.get('path')
       if len(self.LAST_PATH) < 1:
          self.LAST_PATH = self.getHomeDir()

    def put(self, type, value):
       self.config.Write(type, value)

    def get(self, type):
       return self.config.Read(type, '')

    def setAPI(self, url):
       self.URL = url

    def getAPI(self):
       return self.URL

    def getLastPath(self):
       return self.LAST_PATH

    def setLastPath(self, newpath):
       self.LAST_PATH = newpath
       self.put('path', self.LAST_PATH)
	
    def getHomeDir(self):
       try:
           path1=os.path.expanduser("~")
       except:
           path1=""
       try:
           path2=os.environ["HOME"]
       except:
           path2=""
       try:
           path3=os.environ["USERPROFILE"]
       except:
           path3=""

       if not os.path.exists(path1):
           if not os.path.exists(path2):
               if not os.path.exists(path3):
                   return os.getcwd()
               else: return path3
           else: return path2
       else: return path1

    def fitSize(self, w, h, tw, th): # tw is tilewidth, th is  tileheight

       if w < 1 and h < 1:
           return (0, 0)

       if w < tw and h < th:
           return (w, h)

       nw = tw
       nh = th

       if w > h:
          factor = float(float(h) / float(w))
          nh =  (float(nw) *  float(factor))
       else:
          factor = float(float(w) / float(h))
          nw =  (float(nh) *  float(factor))

       return (int(round(nw)), int(round(nh)))

    def tileSize(self):
       return (self.TILE_W + self.TILE_BORDER, self.TILE_H + self.TILE_BORDER)

    def imgSize(self, w, h):
	return self.fitSize(w, h, self.TILE_W, self.TILE_H)

    def limitSize(self, w, h):
	return self.fitSize(w, h, self.LIMIT_W, self.LIMIT_H)

    def getUpTempFile(self):
        try:
           datapath = self.stdpaths.GetUserDataDir()
           if os.path.isdir(datapath):
              pass
           elif os.path.isfile(datapath):
              datapath = datapath + '-datafiles' #FIXME add a hash 
              if os.path.isfile(datapath):
                 datapath = ''
              else:
                 os.mkdir(datapath)
           else:
              os.mkdir(datapath)
        except:
           datapath = ''

        if len(datapath) > 0:
	   return self.portapath(datapath + '/' + self.TMP_FILE)
        else:
	   return self.TMP_FILE

    def portapath(self, path): # From wxPython Demo
        newpath = apply(os.path.join, tuple(path.split('/')))
        # HACK: on Linux, a leading / gets lost...
        if path.startswith('/'):
           newpath = '/' + newpath
        return newpath

