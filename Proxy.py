from wxPython.wx import *
import wx.lib.hyperlink as link

class ProxyDialog(wxDialog):

    proxyServer = ''
    proxyPort = ''
    config = None

    def __init__(self, parent, id=-1, title="Connection Failed",
                 pos=wxDefaultPosition,
                 size=wxSize(250, 185)):

        self.config = wxConfig()
        self.proxyServer = self.config.Read('proxy', '')
        self.proxyPort  = self.config.Read('port', '')

        wxDialog.__init__(self, parent, id, title, pos, size)

	dlgmsg = 'Do You Use a Proxy Server ?'
	if len(self.proxyServer) > 0 or len(self.proxyPort) > 0:
           dlgmsg = 'Please Check Your Proxy Server'

        wxStaticText(self, -1, dlgmsg, wxPoint(15, 5))
        wxStaticText(self, -1, 'Server: ', wxPoint(20, 30))
        wxStaticText(self, -1, 'Port: ', wxPoint(20, 55))
        self.proxyServerBox = wxTextCtrl(self, -1, self.proxyServer, wxPoint(80,30),
                                  wxSize(120, -1))
        self.proxyPortBox = wxTextCtrl(self, -1, self.proxyPort, wxPoint(80,55),
                                 wxSize(120, -1))

        self.helpLink = link.HyperLinkCtrl(self, -1, "Network Connection Help",
                 URL="http://www.mytago.com/uploader/help", pos=wxPoint(20, 85))

        wxStaticLine(self, -1, pos=wxPoint(0, 110), size=(250,-1))

        wxButton(self, wxID_OK,     ' Try Again ', wxPoint(75, 120),
                 wxDefaultSize).SetDefault()
        wxButton(self, wxID_CANCEL, ' Cancel ', wxPoint(160, 120),
                 wxDefaultSize)

        self.CenterOnParent(wxBOTH)

    def showProxy(self, mainwin):
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

    def setProxy(self, server, port):
       self.proxyServer = server
       self.proxyPort = port

    def getProxyServer(self):
       return self.proxyServer

    def getProxyPort(self):
       return self.proxyPort

