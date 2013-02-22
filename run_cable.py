import wx
from wx import xrc
from PgData import PgData

class MyApp(wx.App):
    
    mIdx = 0
    mList = []
    mTotalRecs = 0

    def OnInit(self):
        self.db = PgData()
        self.res = xrc.XmlResource('gui.xrc')
        self.init_frame()
        return True

    def init_frame(self):
        self.frame = self.res.LoadFrame(None, 'frameMain')
        
        # Bind Controls
        self.cboSearch = xrc.XRCCTRL(self.frame, 'cboSearch')
        self.txtEmbassy = xrc.XRCCTRL(self.frame, 'txtEmbassy')
        self.txtDate = xrc.XRCCTRL(self.frame, 'txtDate')
        self.txtContent = xrc.XRCCTRL(self.frame, 'txtContent')
        self.btnPrev = xrc.XRCCTRL(self.frame, 'btnPrev')
        self.btnNext = xrc.XRCCTRL(self.frame, 'btnNext')
        self.statusBar = xrc.XRCCTRL(self.frame, 'statusBar')
        self.statusBar.SetStatusText("Ready")
        
        # Bind Events
        self.frame.Bind(wx.EVT_BUTTON, self.OnClose, id=xrc.XRCID('wxID_EXIT'))
        self.frame.Bind(wx.EVT_BUTTON, self.OnSearch, id=xrc.XRCID('btnSearch'))
        self.frame.Bind(wx.EVT_BUTTON, self.OnNext, id=xrc.XRCID('btnNext'))
        self.frame.Bind(wx.EVT_BUTTON, self.OnPrev, id=xrc.XRCID('btnPrev'))
        self.frame.Bind(wx.EVT_COMBOBOX, self.OnComboClick, id=xrc.XRCID('cboSearch'))
        
        self.btnPrev.Enable(False)
        self.btnNext.Enable(False)
        
        self.fillCombo()
        self.frame.Show()

    def OnSearch(self, evt):
        myCursor= wx.StockCursor(wx.CURSOR_WAIT)
        self.frame.SetCursor(myCursor)        
        
        self.clearText()
        
        embassy = self.cboSearch.GetValue()
        self.statusBar.SetStatusText("Searching ...")
        self.mList = self.db.doSearch(embassy)
        
        self.mIdx = 0
        self.mTotalRecs = len(self.mList)
        self.setStatus()
        
        if self.mTotalRecs > 0:
            self.btnPrev.Enable(False)
            self.btnNext.Enable(True)
            
            # Show first row
            self.txtEmbassy.Value = self.mList[self.mIdx][0]
            self.txtDate.Value = str(self.mList[self.mIdx][1])
            self.txtContent.Value = self.mList[self.mIdx][2]
        else:
            self.statusBar.SetStatusText(embassy + " not found", 0)
        
        myCursor= wx.StockCursor(wx.CURSOR_ARROW)
        self.frame.SetCursor(myCursor)        
        
    def OnClose(self, evt):
        self.db.doCloseConn()
        self.Exit()
        
    def OnNext(self, evt):
        self.mIdx += 1
        self.changeRec()
    
    def OnPrev(self, evt):
        self.mIdx -= 1
        self.changeRec()

    def OnComboClick(self, evt):
        self.clearText()
        
    def fillCombo(self):
        rows = self.db.getEmbassy()
        for embassy in rows:
            self.cboSearch.Append(embassy[0])        
            
    def clearText(self):
        self.txtEmbassy.Value = ""
        self.txtDate.Value = ""
        self.txtContent.Value = ""
        self.statusBar.SetStatusText("Ready")
        wx.Yield()        
        
    def setStatus(self):
        self.statusBar.SetStatusText(str(self.mIdx + 1) + " / " + str(self.mTotalRecs), 0)
    
    def changeRec(self):
        print self.mIdx
        if self.mIdx == 0:
            # Beginning of list
            self.btnPrev.Enable(False)
            self.btnNext.Enable(True)
        elif self.mIdx == len(self.mList) - 1:
            # End of list
            self.btnPrev.Enable(True)
            self.btnNext.Enable(False)
        else:
            self.btnPrev.Enable(True)
            self.btnNext.Enable(True)
            
        self.txtEmbassy.Value = self.mList[self.mIdx][0]
        self.txtDate.Value = str(self.mList[self.mIdx][1])
        self.txtContent.Value = self.mList[self.mIdx][2]
        
        self.setStatus()
        
if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
