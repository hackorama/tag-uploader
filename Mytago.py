import sys,os
import time
import cStringIO
import wx.lib.colourdb
import wx.lib.dialogs
import wx.lib.scrolledpanel as scrolled
import wx.lib.buttons  as  buttons
import wx.lib.hyperlink as hl
from wxPython.wx import *

from Config import Config 
from Login import LoginDialog
from About import AboutDialog
from Uploader import Uploader 
from Proxy import ProxyDialog 
from Connect import Connect 
from logo import getBitmap as getAppLogo
from icon import getBitmap as getAppIcon
from mask import getImage as getMask

class Mytago ( wxFrame ):

   def __init__ ( self ):
      wxFrame.__init__ ( self, None, -1, 'MYTAGO Uploader', size = ( 600, 445 ), 
          style = wx.DEFAULT_FRAME_STYLE ^ ( wx.MAXIMIZE_BOX | wx.RESIZE_BORDER  ) )
      self.SetBackgroundColour("WHITE")

      self.TESTING = False
      self.username = ''
      self.password = ''

      wx.lib.colourdb.updateColourDB()

      _icon = wx.IconFromBitmap(getAppIcon())
      self.SetIcon(_icon)

      self.panel = wxPanel ( self, -1, size=(580, 50) )
      self.panel.SetBackgroundColour('WHITE')

      self.addbutton = wxButton ( self.panel, -1, "+" )
      self.Bind(wx.EVT_BUTTON, self.OnAddButton, self.addbutton)
      self.addbutton.SetForegroundColour('CHARTREUSE2')
      self.addbutton.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD, False))
      self.addbutton.SetMaxSize((30,30))
      self.addbutton.SetMinSize((30,30))
      self.addbutton.SetToolTipString("Add Images")

      self.delbutton = wxButton ( self.panel, -1, "-" )
      self.Bind(wx.EVT_BUTTON, self.OnDelButton, self.delbutton)
      self.delbutton.Enable(False)
      self.delbutton.SetForegroundColour('ORANGE1')
      self.delbutton.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD, False))
      self.delbutton.SetMaxSize((30,30))
      self.delbutton.SetMinSize((30,30))
      self.delbutton.SetToolTipString("Remove Selected Images")

      self.progpanel = wxPanel(self, -1, size=(565, 10) )
      self.progpanel.SetBackgroundColour('GREY70')
      self.progress = wx.Gauge(self.progpanel, -1, 50, size =(565, 10))
      self.progress.Show(False)

      self.upbutton = wxButton ( self.panel, -1, "Upload" )
      self.Bind(wx.EVT_BUTTON, self.OnUpButton, self.upbutton)
      self.upbutton.Enable(False)
      self.upbutton.SetForegroundColour('GREY30')
      self.upbutton.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.BOLD, False))
      self.upbutton.SetMaxSize((120,30))
      self.upbutton.SetMinSize((120,30))
      self.upbutton.SetToolTipString("Upload Images")


      self.helpbutton = wxButton ( self.panel, -1, "i" )
      self.Bind(wx.EVT_BUTTON, self.OnHelpButton, self.helpbutton)
      self.helpbutton.SetForegroundColour('DEEPSKYBLUE')
      self.helpbutton.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.BOLD, False))
      self.helpbutton.SetMaxSize((30,30))
      self.helpbutton.SetMinSize((30,30))
      self.helpbutton.SetToolTipString("Help")

      self.imgpanel = scrolled.ScrolledPanel(self, -1, size=(560, 290),
                                 style = wx.TAB_TRAVERSAL|wx.NO_BORDER, name="imgpanel" )
      self.imgpanel.SetBackgroundColour("WHITE")

      logo = getAppLogo()
      if not self.TESTING:
         self.logoimg = wx.StaticBitmap(self.panel, -1, logo)

      self.scrollsizer = wx.FlexGridSizer(rows=1, cols=3,  vgap=10, hgap=10)
      self.imgpanel.SetSizer( self.scrollsizer )
      self.imgpanel.SetAutoLayout(1)
      self.imgpanel.SetupScrolling()

      self.footer = wxPanel ( self, -1, size=(580, 20) )
      self.footer.SetBackgroundColour("WHITE")

      self.message = wx.StaticText(self.footer, -1, "", size = (450, 10))
      font = wx.Font(8, wx.SWISS, wx.NORMAL,  wx.BOLD)
      self.message.SetFont(font)

      self.hyper1 = hl.HyperLinkCtrl(self.footer, wx.ID_ANY, "www.mytago.com",
                                        URL="http://www.mytago.com")
      self.hyper1.SetBold(True)
      self.hyper1.SetColours("STEELBLUE1", "STEELBLUE1", "STEELBLUE1")
      self.hyper1.SetUnderlines(False, False, False)
      self.hyper1.SetToolTip(wx.ToolTip("Mytago"))
      self.hyper1.UpdateLink()


      self.sizertop  = wxBoxSizer ( wxALIGN_CENTER_HORIZONTAL )
      self.sizerbot  = wxBoxSizer ( wxALIGN_CENTER_HORIZONTAL )
      self.sizermain = wxBoxSizer ( wx.VERTICAL )

      self.sizertop.Add ( (10, 40), 0, wx.EXPAND )
      if self.TESTING:
         self.sizertop.Add ( (230, 40), 0,  wx.ALIGN_TOP | wx.EXPAND )
      else:
         self.sizertop.Add ( self.logoimg, 0,  wx.ALIGN_TOP | wx.EXPAND )
      self.sizertop.Add ( (100, 40), 0, wx.EXPAND )
      self.sizertop.Add ( self.addbutton, 0 )
      self.sizertop.Add ( (5, 40), 0, wx.EXPAND )
      self.sizertop.Add ( self.delbutton, 0 )
      self.sizertop.Add ( (15, 40), 0, wx.EXPAND )
      self.sizertop.Add ( self.upbutton, 0)
      self.sizertop.Add ( (10, 40), 0, wx.EXPAND )
      self.sizertop.Add ( self.helpbutton, 0)

      self.sizerbot.Add ( (15, 10), 0, wx.EXPAND )
      self.sizerbot.Add ( self.message, 0,  wx.ALIGN_LEFT | wx.EXPAND )
      self.sizerbot.Add ( (10, 10), 0, wx.EXPAND )
      self.sizerbot.Add ( self.hyper1, 0,  wx.ALIGN_RIGHT | wx.EXPAND )
      self.sizerbot.Add ( (15, 10), 0, wx.EXPAND )

      self.sizermain.Add ((600, 10) )
      self.sizermain.Add ( self.panel, 0, wx.EXPAND | wx.FIXED_MINSIZE )
      self.sizermain.Add ((600, 10) )
      self.sizermain.Add ( self.progpanel, 0, wx.ALIGN_CENTER | wx.FIXED_MINSIZE )
      self.sizermain.Add ((600, 10) )
      self.sizermain.Add ( self.imgpanel, 0, wx.ALIGN_CENTER | wx.FIXED_MINSIZE )
      self.sizermain.Add ((600, 5) )
      self.sizermain.Add ( wx.StaticLine(self, -1, size=(565,-1)), 0, wx.TOP | wx.ALIGN_CENTER | wx.FIXED_MINSIZE )
      self.sizermain.Add ((600, 5) )
      self.sizermain.Add ( self.footer, 0, wx.EXPAND | wx.FIXED_MINSIZE )
      self.sizermain.Add ((600, 5) )


      self.panel.SetSizer ( self.sizertop )
      self.footer.SetSizer ( self.sizerbot )
      self.SetSizer(self.sizermain)
      self.Show ( True )

      self.maskimg  =  getMask() 

      self.lastsel = None 
      self.lastdesel = None 
      self.shifted = False 

      self.delimglist = []
      self.pathlist = []
      self.upimglist = []

      self.upcount = 0
      self.lastupcount = -1 
      self.uploading = False 
      self.cancelnow = False 

      # Catch all shift key presses 

      self.panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown, self.panel)
      self.panel.Bind(wx.EVT_KEY_UP, self.OnKeyUp, self.panel)

      self.imgpanel.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown, self.imgpanel)
      self.imgpanel.Bind(wx.EVT_KEY_UP, self.OnKeyUp, self.imgpanel)

      self.footer.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown, self.footer)
      self.footer.Bind(wx.EVT_KEY_UP, self.OnKeyUp, self.footer)


   def initConfig(self):
      self.conf = Config()
      if self.TESTING:
         self.conf.setAPI('http://localhost/api')
      self.message.SetForegroundColour('ROYALBLUE1')
      self.message.SetLabel("checking network connection...")

   def connectLogin(self):
      self.connect = Connect()
      self.connect.setConfig(self.conf)
      wx.BeginBusyCursor()
      if self.connect.testConnect():
         wx.EndBusyCursor()
         self.message.SetForegroundColour('ROYALBLUE1')
         self.message.SetLabel("network connected please login")
         self.tryLogin()
      else:
         wx.EndBusyCursor()
         self.message.SetForegroundColour(wxNamedColour('ORANGE1'))
         self.message.SetLabel("network failed. please try proxy")
         self.proxy = ProxyDialog(self)
         keeptrying = True
         while keeptrying:
            if self.proxy.showProxy(self):
               self.connect.setProxy(self.proxy.getProxyServer() + ':' + self.proxy.getProxyPort())
               wx.BeginBusyCursor()
               window.message.SetForegroundColour('ROYALBLUE1')
               window.message.SetLabel("checking network connection...")
               if self.connect.testConnect():
                  wx.EndBusyCursor()
                  self.message.SetForegroundColour('ROYALBLUE1')
                  self.message.SetLabel("network connected. please login")
                  if self.tryLogin():
                     keeptrying = False
               else:
                  wx.EndBusyCursor()
                  self.message.SetForegroundColour(wxNamedColour('ORANGE1'))
                  if len(self.proxy.getProxyServer()) > 0: #FIXME add proper check
                     self.message.SetLabel("proxy failed. please try again")
                  else:
                     self.message.SetLabel("network failed. please try proxy")
            else:
               self.Destroy() 
               sys.exit(0) 

   def tryLogin(self):
         wx.SafeYield()
         login = LoginDialog(self)
         if login.showLogin(self):
            self.username = login.getUser()
            self.password = login.getPassword()
            self.updateMessage()
            return True
         else:
            self.Destroy() 
            sys.exit(0) 

   def makeUploader(self):
      self.uploader = Uploader()
      self.uploader.setConfig(self.conf)
      self.uploader.setConnector(self.connect)
      self.uploader.setAccess(self.username, self.password)
      self.uploader.setWindow(self)

   def showUploadFailedMessage(self):
      self.message.SetForegroundColour('ORANGE1')
      if self.connect.getError() == '105' :
         self.showMessage( 'upload limit reached, ' + `len(self.upimglist)` + ' image(s) left to upload')
      elif self.connect.getError() == '106' :
         self.showMessage( 'server is busy, ' + `len(self.upimglist)` + ' image(s) left to upload')
      elif len(self.upimglist) == 1:
         self.showMessage( 'upload failed, ' + `len(self.upimglist)` + ' image left to upload')
      elif len(self.upimglist) > 1:
         self.showMessage( 'upload failed, ' + `len(self.upimglist)` + ' images left to upload')
      else:
         self.message.SetForegroundColour('GREY30')

   def showMessage(self, msg):
      self.message.SetForegroundColour('STEELBLUE1')
      if len(self.username) < 33: # prevent long username to overflow footer space
         self.message.SetLabel( self.username + ' | ' + msg )
      else:
         self.message.SetLabel( msg )

   def updateMessage(self):
      if len(self.upimglist) == 1:
         self.showMessage( `len(self.upimglist)` + ' image ready for upload')
      elif len(self.upimglist) > 1:
         self.showMessage( `len(self.upimglist)` + ' images ready for upload')
      else:
         self.showMessage( 'please add images to upload')

   def addImages(self, dlg):
      try:
         paths = dlg.GetPaths()
         self.conf.setLastPath(dlg.GetDirectory())
         wx.BeginBusyCursor()
         wx.Yield()
         self.panel.Update()
         #self.progress.Show(True)
         #self.progress.SetRange( len(paths) )
         i = 0
         if len(paths) > 0:
            tilesize = self.conf.tileSize()
            for path in paths:
               i += 1
               self.progress.SetValue(i)
               if path in self.pathlist:
                  if self.conf.debug: print "Skip: %s" % path
               else:
                  if self.conf.debug: print "Adding: %s" % path
                  self.showMessage('adding image ' + str(i) + ' of ' + `len(paths)`)
                  self.pathlist.append(path)
                  img  =  wx.Image(path, wx.BITMAP_TYPE_ANY)
                  imgtile = self.conf.imgSize(img.GetWidth(), img.GetHeight())
                  nw = imgtile[0]
                  nh = imgtile[1]
                  if nh and nw:
                     img.Rescale(nw,nh)
                     sizedimg = img.ConvertToBitmap()               
                     self.imgbutton =  buttons.GenBitmapToggleButton( self.imgpanel, -1, None, size=tilesize ) 
                     self.imgbutton.SetToolTipString(path);
                     self.imgbutton.SetBitmapLabel(sizedimg);

                     self.maskimg.Rescale(nw,nh)
                     maskbmp = self.maskimg.ConvertToBitmap()               
                     mask = wx.Mask(maskbmp, wx.BLACK)
                     sizedimgtoggle = img.ConvertToBitmap()			
                     sizedimgtoggle.SetMask(mask);
                     self.imgbutton.SetBitmapSelected(sizedimgtoggle)
                     self.imgbutton.SetBackgroundColour("WHITE")

                     #self.scrollsizer.Add( self.imgbutton )
                     #self.upimglist.append(self.imgbutton)

                     self.scrollsizer.Prepend(self.imgbutton)
                     self.upimglist.insert(0, self.imgbutton)

      	             self.Bind(wx.EVT_BUTTON, self.OnImgButton, self.imgbutton)
                     self.imgbutton.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown, self.imgbutton)
                     self.imgbutton.Bind(wx.EVT_KEY_UP, self.OnKeyUp, self.imgbutton)

                     #redraw
                     wx.Yield()
                     #self.scrollsizer.Layout()
                     #self.imgpanel.Layout()
                     self.imgpanel.SetupScrolling()
                     #self.imgpanel.Refresh()
                     self.imgpanel.Update()

         self.upbutton.Enable(True) #if its disabled by delbutton
         #self.progress.SetRange(0)
         #self.progress.Show(False)
         self.scrollsizer.Layout()
         self.imgpanel.Layout()
         self.imgpanel.SetupScrolling()
         self.imgpanel.Refresh()
         self.imgpanel.Update()
         self.panel.Update()
         wx.EndBusyCursor()
      except:
         self.upbutton.Enable(True) 
         #self.imgpanel.Show(True)
         self.progress.SetRange(0)
         self.progress.Show(False)
         self.imgpanel.SetupScrolling()
         self.imgpanel.Update()
         self.panel.Update()
         wx.EndBusyCursor()
         
   # All event handler functions

   def OnResult(self, event): # Gets events triggered from Uploader->Worker Thread
      if event.data is None:
         self.upimglist = self.upimglist[self.upcount:] #slice out uploaded
         self.uploader.closeThread()
	 if self.cancelnow:
            self.postUpload(False)
         else:
            self.postUpload(True)
      elif event.data == 0:
         self.uploader.closeThread()
         self.postUpload(False)
      else:
         count = int(event.data) - 1
         if(count == self.lastupcount): 
            button = self.upimglist[count]
            self.showMessage('uploading image ' + str(count+1) + ' of ' + `len(self.upimglist)`)
            self.progress.SetValue((count*2)+2)
            self.scrollsizer.Remove(button)
            self.pathlist.remove(button.GetToolTip().GetTip()) #clear pathlist
            button.Destroy() 
            self.scrollsizer.Layout()
            self.imgpanel.Layout()
            self.imgpanel.Refresh()
            self.imgpanel.Update()
            self.upcount += 1
         else: #hack for progess update using same event
            self.progress.SetValue((count*2)+1)
         self.lastupcount = count

   def OnAddButton(self, event):
      wildcard = "All Supported Images|*.gif;*.jpg;*.jpeg;*.png|" \
           "JPEG Images|*.jpg;*jpeg|"  \
           "GIF Images|*.gif|" \
           "PNG Images|*.png"   
       
      dlg = wx.FileDialog(
            self, message="Choose Images", defaultDir=self.conf.getLastPath(), 
            defaultFile="", wildcard=wildcard, style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)

      if dlg.ShowModal() == wx.ID_OK:

         self.imgpanel.Enable(False)
         self.imgpanel.Refresh()
         self.imgpanel.Update()

         self.addbutton.Enable(False)
         self.upbutton.Enable(False)
         self.delbutton.Enable(False)

         self.addImages(dlg)

         self.addbutton.Enable(True)
         self.upbutton.Enable(True)
         if len(self.delimglist) > 0:
           self.delbutton.Enable(True)

         self.imgpanel.Enable(True)
         self.imgpanel.Refresh()
         self.imgpanel.Update()

      self.updateMessage()
      dlg.Destroy()


   def OnDelButton(self, event):
      for button in self.delimglist:
         if self.conf.debug: print "Removing: %s" % button.GetToolTip().GetTip() 
         self.scrollsizer.Detach(button)
         self.pathlist.remove(button.GetToolTip().GetTip()) #clear pathlist
         self.upimglist.remove(button)
	 button.Destroy()

         #redraw
         wx.Yield()
         self.scrollsizer.Layout()
         self.imgpanel.Layout()
         self.imgpanel.Refresh()
         self.imgpanel.Update()
 
      self.imgpanel.SetupScrolling()

      self.delimglist = []
   
      if len(self.pathlist) > 0:
          self.upbutton.Enable(True)
          if not len(self.delimglist):
             self.delbutton.Enable(False)
      else:
          self.upbutton.Enable(False)
          self.delbutton.Enable(False)

      self.updateMessage()
   
   def OnUpButton(self, event):
      connectionbroke = False

      self.scrollsizer.Layout()
      self.imgpanel.Layout()
      self.imgpanel.SetupScrolling()

      self.imgpanel.Enable(False)
      self.imgpanel.Refresh()
      self.imgpanel.Update()

      if self.uploading:
         if self.conf.debug: print "Cancel"
	 self.cancelnow = True
         self.uploading = False
         self.upbutton.Enable(False)
         self.showMessage('cancelling upload..')
         self.uploader.abortUpload()
      else:
         for b in self.upimglist: # reset selected for delete
            b.SetBackgroundColour("WHITE")
            b.SetValue(False)
         self.upbutton.SetLabel("Cancel")
         self.upbutton.SetToolTipString("Cancel Upload")
         self.addbutton.Enable(False)
         self.delbutton.Enable(False)
         self.progress.Show(True)
         self.progress.SetRange(len(self.upimglist) * 2)
         self.upcount = 0
         self.lastupcount = -1 
         self.uploading = True
         self.showMessage('starting upload...')

         self.uploader.uploadFiles(self.upimglist)


   def postUpload(self, connectionbroke):
      if self.cancelnow:
         self.cancelnow = False
      elif len(self.upimglist) == self.upcount:
         self.upimglist = [] # all uploaded
      else:
         self.upimglist = self.upimglist[self.upcount:] #slice out uploaded

      if len(self.upimglist) > 0: # upload cancelled in middle
         for button in self.upimglist:
               button.Update()
         self.upbutton.Enable(True)
      else:
         self.upbutton.Enable(False)

      #reset control flags
      self.uploading = False 
      self.upcount = 0

      self.delimglist = [] #always reset delete list once in upload
      self.upbutton.SetLabel("Upload")
      self.upbutton.SetToolTipString("Upload Images")
      self.upbutton.Enable(True)
      self.addbutton.Enable(True)
      self.progress.SetRange(0)
      self.progress.Enable(False)

      self.imgpanel.Enable(True)
      self.scrollsizer.Layout()
      self.imgpanel.Layout()
      self.imgpanel.SetupScrolling()
      self.imgpanel.Refresh()
      self.imgpanel.Update()

      if connectionbroke:
         self.showUploadFailedMessage()
      else:
         self.updateMessage()

   def OnImgButton(self, event):
      self.delbutton.Enable(True)
      button = event.GetEventObject()
      if button in self.delimglist:
         self.delimglist.remove(button)
         button.SetBackgroundColour("WHITE")
         self.multiDesel(button)
         self.lastdesel = button
         self.lastsel = None 
      else:
         self.delimglist.append(button)
         button.SetBackgroundColour("ORANGE1")
         self.multiSel(button)
         self.lastsel = button
         self.lastdesel = None 

      if len(self.delimglist) > 0:
          self.delbutton.Enable(True)
      else:
          self.delbutton.Enable(False)
      self.updateMessage()

   def multiDesel(self, button):
      if not self.shifted:
         return
      if self.lastdesel == None:
         return
      if not self.lastdesel in self.upimglist:
         return
      x =  self.upimglist.index(self.lastdesel)
      y =  self.upimglist.index(button)
      if  x < 0 or y < 0:
         return
      if x < y:
         start = x
         end = y
      else:
         start = y
         end = x
      for i in range(len(self.upimglist)):
         if i > start and i < end:
            b = self.upimglist[i]
            if b in self.delimglist: # safe remove
               self.delimglist.remove(b)
            b.SetBackgroundColour("WHITE")
            b.SetValue(False)
            b.Update()
      wx.Yield()
      self.imgpanel.Refresh()
      self.imgpanel.Update()
	
   def multiSel(self, button):
      if not self.shifted:
         return
      if self.lastsel == None:
         return
      if not self.lastsel in self.upimglist:
         return
      x =  self.upimglist.index(self.lastsel)
      y =  self.upimglist.index(button)
      if x < 0 or y < 0:
         return
      if x < y:
         start = x 
         end = y
      else: 
         start = y 
         end = x
      for i in range(len(self.upimglist)):
         if i > start and i < end:
            b = self.upimglist[i]
            if not b in self.delimglist: # safe append 
               self.delimglist.append(b)
            b.SetBackgroundColour("ORANGE1")
            b.SetValue(True)
            b.Update()
      wx.Yield()
      self.imgpanel.Refresh()
      self.imgpanel.Update()
	
   def OnHelpButton(self, event):
      about = AboutDialog(self)
      about.showAbout(self.conf.version)
      about.Destroy()

   def OnKeyDown(self, evt):
      if evt.GetKeyCode() == wx.WXK_SHIFT:
        self.shifted = True

   def OnKeyUp(self, evt):
      if evt.GetKeyCode() == wx.WXK_SHIFT:
        self.shifted = False 

#application = wxPySimpleApp(1, 'my.log')
application = wxPySimpleApp()
application.SetAppName('mytagouploader')
application.SetVendorName('Mytago')
window = Mytago()
window.Show()
window.Refresh()
window.Update()
window.initConfig()
window.connectLogin()
window.makeUploader()
application.MainLoop()
