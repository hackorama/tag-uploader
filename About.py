from wxPython.wx import *
import wx.lib.hyperlink as link
from splash import getBitmap as getSplash

class AboutDialog(wxDialog):

    proxyServer = ''
    proxyPort = ''
    config = None

    def __init__(self, parent, id=-1, title="Mytago Uploader Information",
                 pos=wxDefaultPosition,
                 size=wxSize(350, 260)):

        self.config = wxConfig()
        self.proxyServer = self.config.Read('proxy', '')
        self.proxyPort  = self.config.Read('port', '')

        wxDialog.__init__(self, parent, id, title, pos, size)

        splash  = getSplash()
        self.splashimg = wxStaticBitmap(self, -1, splash)

        self.aboutText = wxStaticText(self, -1, 'Mytago Uploader 1.00.00')
        self.helpLink = link.HyperLinkCtrl(self, wxID_ANY, "Online Mytago Uploader Help",
                                        URL="http://www.mytago.com/uploader/help")
        self.titleText = wxStaticText(self, -1, 'Your Proxy Configuration')
        self.serverText = wxStaticText(self, -1, 'HTTP Proxy: ')
        self.proxyText = wxStaticText(self, -1, 'Port: ')
        self.proxyServerBox = wxTextCtrl(self, -1, self.proxyServer, size=(150, -1))
        self.proxyPortBox = wxTextCtrl(self, -1, self.proxyPort, size=(50, -1))
        self.okButton = wxButton(self, wxID_OK, ' OK ')
        self.cancelButton = wxButton(self, wxID_CANCEL, ' Cancel ')

	self.sizersubtitle  = wxBoxSizer (wxHORIZONTAL)
	self.sizerproxytitle  = wxBoxSizer (wxHORIZONTAL)
	self.sizerproxy  = wxBoxSizer (wxHORIZONTAL)
        self.sizerbot  = wxBoxSizer (wxHORIZONTAL)
        self.sizermain = wxBoxSizer (wxVERTICAL)

        self.sizersubtitle.Add( self.aboutText, 0,  wxALL | wxALIGN_LEFT | wxEXPAND, border=5)
        self.sizersubtitle.Add( (60, 5))
        self.sizersubtitle.Add( self.helpLink, 0,  wxALL | wxALIGN_RIGHT | wxEXPAND, border=5)

        self.sizerproxytitle.Add( self.titleText, 0, wxALL | wxALIGN_CENTER | wxFIXED_MINSIZE, border=5)
        self.sizerproxytitle.Add( wxStaticLine(self, -1, size=(200,-1)), 0, wxALL | wxALIGN_CENTER | wxFIXED_MINSIZE, border=5)

        self.sizerproxy.Add( self.serverText, 0, wxALL | wxALIGN_CENTER | wxFIXED_MINSIZE, border=5)
        self.sizerproxy.Add( self.proxyServerBox, 0, wxALL | wxALIGN_CENTER | wxFIXED_MINSIZE, border=5)
        self.sizerproxy.Add( self.proxyText, 0, wxALL | wxALIGN_CENTER | wxFIXED_MINSIZE, border=5)
        self.sizerproxy.Add( self.proxyPortBox, 0, wxALL | wxALIGN_CENTER | wxFIXED_MINSIZE, border=5)

        self.sizerbot.Add( self.okButton, 0, wxALL | wxALIGN_RIGHT, border=5)
        self.sizerbot.Add( self.cancelButton, 0, wxALL | wxALIGN_RIGHT, border=5)

        self.sizermain.Add( self.splashimg, 0)
        self.sizermain.Add( self.sizersubtitle, 0, wxALL, border=1)
        self.sizermain.Add( (350,20))
        self.sizermain.Add( self.sizerproxytitle, 0, wxALL, border=1)
        self.sizermain.Add( self.sizerproxy, 0, wxALL, border=5)
        self.sizermain.Add( (350,20))
        self.sizermain.Add( wxStaticLine(self, -1, size=(350,-1)), 0, wxALL , border=0)
        self.sizermain.Add( self.sizerbot, 0, wxALL | wxALIGN_RIGHT | wxFIXED_MINSIZE, border=5)

        self.SetSizer(self.sizermain)
        self.CenterOnParent(wxBOTH)

    def showAbout(self, version):
	self.aboutText.SetLabel('Mytago Uploader ' + version)
        self.proxyServerBox.SetValue(self.proxyServer)
        self.proxyPortBox.SetValue(self.proxyPort)
        val = self.ShowModal()
        if val == wxID_OK:
            self.proxyServer = self.proxyServerBox.GetValue()
            self.proxyPort = self.proxyPortBox.GetValue()
            self.config.Write('proxy', self.proxyServer)
            self.config.Write('port', self.proxyPort)
            return True
        else:
            return False

