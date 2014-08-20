import sys
from wxPython.wx import *
import wx.lib.hyperlink as link

class LoginDialog(wxDialog):

    username = ""
    password = ""
    connect = None
    message = None

    def __init__(self, parent, id=-1, title="Login to Mytago",
                 pos=wxDefaultPosition,
                 size=wxSize(290, 185)):
        wxDialog.__init__(self, parent, id, title, pos, size)
        wxStaticText(self, -1, 'Please Enter Your Mytago User Name and Password',
                     wxPoint(15, 5))
        wxStaticText(self, -1, 'User Name: ', wxPoint(20, 30))
        wxStaticText(self, -1, 'Password: ', wxPoint(20, 55))
        self.nameBox = wxTextCtrl(self, -1, '', wxPoint(80,30),
                                  wxSize(160, -1))
        self.passwordBox = wxTextCtrl(self, -1, '', wxPoint(80,55),
                                 wxSize(160, -1), style=wxTE_PASSWORD)

        self.helpLink = link.HyperLinkCtrl(self, -1, "New Users, Please Join for Free",
                 URL="http://www.mytago.com/login", pos=wxPoint(20, 85))

        wxStaticLine(self, -1, pos=wxPoint(0, 110), size=(290,-1))

        wxButton(self, wxID_OK, ' OK ', wxPoint(110, 120),
                 wxDefaultSize).SetDefault()
        wxButton(self, wxID_CANCEL, ' Cancel ', wxPoint(195, 120),
                 wxDefaultSize)

        self.CenterOnParent(wxBOTH)

    def showLogin(self, mainwin):
        #h = sha.new(self.passwordBox.GetValue()) #password = h.hexdigest()
        self.connect = mainwin.connect
        self.message = mainwin.message
        val = self.ShowModal()
        if val == wxID_OK:
            self.username = self.nameBox.GetValue()
            self.password = self.passwordBox.GetValue()
            while not self.validUser():
               val = self.ShowModal()
               if val == wxID_OK:
                  self.username = self.nameBox.GetValue()
                  self.password = self.passwordBox.GetValue()
               else:
                  return False
            return True
        else:
            return False

    def getUser(self):
       return self.username

    def getPassword(self):
      return self.password
  
    def validUser(self):
      #return True #TEST ONLY
      wxBeginBusyCursor()
      self.message.SetForegroundColour('STEELBLUE2')
      self.message.SetLabel('logging in as ' + self.username)
      self.connect.setAccess(self.username, self.password)
      if self.connect.testAccess():
         self.message.SetForegroundColour('GREY30')
         self.message.SetLabel('welcome ' + self.username)
         wxEndBusyCursor()
         return True
      else:
         self.message.SetForegroundColour(wxNamedColour('ORANGE1'))
         if len(self.username) > 0:
            self.message.SetLabel('failed to login as ' + self.username )
         else:
            self.message.SetLabel('please enter a username' )
         wxEndBusyCursor()
         return False

