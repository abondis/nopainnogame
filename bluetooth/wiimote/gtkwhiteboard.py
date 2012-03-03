#!/usr/bin/python
#
# Written by Stephane Duchesneau <stephane.duchesneau@gmail.com>
# 

# LICENSE:         MIT (X11) License which follows:
#
# Copyright (c) 2008 Stephane Duchesneau
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import wx
import time, sys, os
import thread
import wx.lib.newevent
import whiteboard

(WiimoteConnectedEvent, EVT_WIIMOTE_CONNECTED) = wx.lib.newevent.NewEvent()
(NoWiimoteFoundEvent, EVT_NO_WIIMOTE_FOUND) = wx.lib.newevent.NewEvent()
(WiimoteConnectingEvent, EVT_WIIMOTE_CONNECTING) = wx.lib.newevent.NewEvent()
(WiimoteDisconnectedEvent, EVT_WIIMOTE_DISCONNECTED) = wx.lib.newevent.NewEvent()
(WiimoteRunningEvent, EVT_WIIMOTE_RUNNING) = wx.lib.newevent.NewEvent()
(WiimoteStoppedEvent, EVT_WIIMOTE_STOPPED) = wx.lib.newevent.NewEvent()
(WiimoteCalibratedEvent, EVT_WIIMOTE_CALIBRATED) = wx.lib.newevent.NewEvent()
(WiimoteCalibratingEvent, EVT_WIIMOTE_CALIBRATING) = wx.lib.newevent.NewEvent()
(OptionsChangedEvent, EVT_OPTIONS_CHANGED) = wx.lib.newevent.NewEvent()
(LoggerEvent, EVT_LOGGER) = wx.lib.newevent.NewEvent()
#---------------------------------------------------------------------------
	
class WB(whiteboard.WhiteBoard):
	def __init__(self,parent):
		self._parent = parent
		whiteboard.WhiteBoard.__init__(self)
		
	def OnConnected(self):
		evt = WiimoteConnectedEvent()
		wx.PostEvent(self._parent, evt)
		
	def OnNoWiimoteFound(self):
		evt = NoWiimoteFoundEvent()
		wx.PostEvent(self._parent, evt)
		
	def OnConnecting(self):
		evt = WiimoteConnectingEvent()
		wx.PostEvent(self._parent, evt)
		
	def OnDisconnect(self):
		evt = WiimoteDisconnectedEvent()
		wx.PostEvent(self._parent, evt)
		
	def OnStop(self):
		evt = WiimoteStoppedEvent()
		wx.PostEvent(self._parent, evt)
	
	def OnRun(self):
		evt = WiimoteRunningEvent()
		wx.PostEvent(self._parent, evt)
		
	def OnCalibrated(self):
		evt = WiimoteCalibratedEvent()
		wx.PostEvent(self._parent, evt)
	def OnCalibrating(self):
		evt = WiimoteCalibratingEvent()
		wx.PostEvent(self._parent, evt)
	def OnOptionsChanged(self):
		evt = OptionsChangedEvent()
		wx.PostEvent(self._parent, evt)
		
	def printOut(self,strList,newLine=True): 
		"""all printOut() calls from whiteboard will send an event to the panel to show the text in logger"""
		evt = LoggerEvent(value = strList,newline=newLine)
		wx.PostEvent(self._parent, evt)

class SB(wx.StatusBar):
	def __init__(self,parent):
		wx.StatusBar.__init__(self,parent,-1)
		# This status bar has three fields
		self.SetFieldsCount(3)
		# Sets the three fields to be relative widths to each other.
		self.SetStatusWidths([-1, -1, -1])
		self.parent = parent
		
		# Field 0 ... just text
		self.SetStatusText("Not Running",0)
		self.SetStatusText("Disconnected", 1)
		


		# We're going to use a timer to drive the battery level.
		self.timer = wx.PyTimer(self.Notify)
		self.timer.Start(2000)
		self.Notify()
	
	
	def Notify(self):
				
		st = self.parent.GetBattery()
		if st: self.SetStatusText("Battery: "+ str(st)+"%", 2)
		else: self.SetStatusText("",2)

class DummyButton:
    def Enable(self,val):
        pass
        

class MainWindow(wx.Frame):
    w = None #for getbattery and stuff
    
    def __init__(self, parent,title):
        
        wx.Frame.__init__(self, parent, wx.ID_ANY,title)
        self.btnStart =wx.Button(self, -1, "Start")
        self.btnStop = wx.Button(self,-1, "Stop")
        if sys.platform == "win32":
            self.btnPause = DummyButton()
        else: self.btnPause = wx.Button(self,-1, "Pause")
        self.btnCal =wx.Button(self, -1, "Calibrate")
        self.cb1 = wx.CheckBox(self, -1, "Touchpad Mode")
        self.cbCalOnStart = wx.CheckBox(self, -1, "Calibrate on Start")
        self.cbSaveOnExit = wx.CheckBox(self, -1, "Save options on exit")
	self.cbSides = wx.CheckBox(self,-1,"Enable 'Side click'")

        OptionsList = ['Left Click', 'Right Click', 'Scroll', 'Toggle TouchPad','None','Double-click','Middle click']
        self.chllabel = wx.StaticText(self,-1,"Zones")
        self.chlnum = wx.Choice(self, -1 ,choices = ['1','2','3'])
        self.chrlabel = wx.StaticText(self,-1,"Zones")
        self.chrnum = wx.Choice(self, -1, choices = ['1','2','3'])
        chlsizer = wx.BoxSizer(wx.HORIZONTAL)
        chlsizer.AddMany((self.chllabel, (self.chlnum,0,wx.LEFT,10)))
        chrsizer = wx.BoxSizer(wx.HORIZONTAL)
        chrsizer.AddMany((self.chrlabel, (self.chrnum,0,wx.LEFT,10)))

        self.chl1 = wx.Choice(self, -1, choices = OptionsList)
        self.chl2 = wx.Choice(self, -1, choices = OptionsList)
        self.chl3 = wx.Choice(self, -1, choices = OptionsList)
        self.chr1 = wx.Choice(self, -1, choices = OptionsList)
        self.chr2 = wx.Choice(self, -1, choices = OptionsList)
        self.chr3 = wx.Choice(self, -1, choices = OptionsList)

        sizer = wx.BoxSizer(wx.VERTICAL)
        line = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL)
        self.logger = wx.TextCtrl(self,5, "",size=wx.Size(400,70),style=wx.TE_MULTILINE | wx.TE_READONLY)

        #bind events
        self.Bind(wx.EVT_CLOSE, self.EvtQuit)
	self.Bind(EVT_OPTIONS_CHANGED, self.EvtOptionsChanged)
        self.Bind(EVT_WIIMOTE_CALIBRATED, self.EvtWiimoteCalibrated)
        self.Bind(EVT_WIIMOTE_CALIBRATING, self.EvtWiimoteCalibrating)
        self.Bind(EVT_WIIMOTE_RUNNING, self.EvtWiimoteRunning)
        self.Bind(EVT_WIIMOTE_STOPPED, self.EvtWiimoteStopped)
        self.Bind(EVT_WIIMOTE_CONNECTED, self.EvtWiimoteConnected)
        self.Bind(EVT_NO_WIIMOTE_FOUND, self.EvtNoWiimoteFound)
        self.Bind(EVT_WIIMOTE_CONNECTING, self.EvtWiimoteConnecting)
        self.Bind(EVT_WIIMOTE_DISCONNECTED, self.EvtWiimoteDisconnected)

        self.Bind(EVT_LOGGER, self.EvtLogger)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCbSides, self.cbSides)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCbTP, self.cb1)
        self.Bind(wx.EVT_BUTTON,self.EvtBtnStart,self.btnStart)
        self.Bind(wx.EVT_BUTTON,self.EvtBtnStop,self.btnStop)
        self.Bind(wx.EVT_BUTTON,self.EvtBtnCal,self.btnCal)
        if sys.platform != "win32": self.Bind(wx.EVT_BUTTON,self.EvtBtnPause,self.btnPause)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCbCal, self.cbCalOnStart)
	self.Bind(wx.EVT_CHECKBOX, self.EvtCbSaveOnExit, self.cbSaveOnExit)
        self.Bind(wx.EVT_CHOICE, self.EvtChoiceLNum, self.chlnum)
        self.Bind(wx.EVT_CHOICE, self.EvtChoiceRNum, self.chrnum)
        self.Bind(wx.EVT_CHOICE, self.EvtChSides, self.chr1)
        self.Bind(wx.EVT_CHOICE, self.EvtChSides, self.chr2)
        self.Bind(wx.EVT_CHOICE, self.EvtChSides, self.chr3)
        self.Bind(wx.EVT_CHOICE, self.EvtChSides, self.chl1)
        self.Bind(wx.EVT_CHOICE, self.EvtChSides, self.chl2)
        self.Bind(wx.EVT_CHOICE, self.EvtChSides, self.chl3)

        #left option staticbox
        lbox = wx.StaticBox(self, -1, "Left side")
        bsizer = wx.StaticBoxSizer(lbox, wx.VERTICAL)
        bsizer.Add(chlsizer, 0, wx.TOP|wx.LEFT, 10)
        bsizer.Add(self.chl1, 0, wx.TOP|wx.LEFT, 10)
        bsizer.Add(self.chl2, 0, wx.TOP|wx.LEFT, 10)
        bsizer.Add(self.chl3, 0, wx.TOP|wx.LEFT, 10)

        #right option staticbox
        rbox = wx.StaticBox(self, -1, "Right side")
        bsizer2 = wx.StaticBoxSizer(rbox, wx.VERTICAL)
        bsizer2.Add(chrsizer, 0, wx.TOP|wx.LEFT, 10)
        bsizer2.Add(self.chr1, 0, wx.TOP|wx.LEFT, 10)
        bsizer2.Add(self.chr2, 0, wx.TOP|wx.LEFT, 10)
        bsizer2.Add(self.chr3, 0, wx.TOP|wx.LEFT, 10)

        self.optionBox = wx.BoxSizer(wx.HORIZONTAL)
        self.optionBox.Add(bsizer, 1, wx.EXPAND|wx.ALL, 5)
        self.optionBox.Add(bsizer2, 1, wx.EXPAND|wx.ALL, 5)

        butsizer = wx.BoxSizer(wx.HORIZONTAL)
        if sys.platform != "win32":
            butsizer.AddMany( [ self.btnStart, (self.btnStop,0,wx.LEFT,10),
                (self.btnPause,0,wx.LEFT,10),
                (self.btnCal,0,wx.LEFT,10)	] )
        else:
            butsizer.AddMany( [ self.btnStart, (self.btnStop,0,wx.LEFT,10),
                (self.btnCal,0,wx.LEFT,10)	] )
	
	optbox2 = wx.BoxSizer(wx.HORIZONTAL)
	optbox2.AddMany( [ (self.cbCalOnStart,0,wx.LEFT,10), (self.cbSaveOnExit,0,wx.LEFT,10)])
	sizer.AddMany( [ 
            self.cb1,
            self.cbSides,
            self.optionBox,
            (10,10),
            (line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL),
            (10,10),
            butsizer,
            optbox2,
            (10,10),
            self.logger
             ])

        self.border = wx.BoxSizer(wx.VERTICAL)
        self.border.Add(sizer, 0, wx.ALL, 15)
        self.SetSizer(self.border)

        #set statusbar
        self.sb = SB(self)#wx.StatusBar(self) #CustomStatusBar(self, log)
        self.SetStatusBar(self.sb)

        #open WhiteBoard object
        self.w = WB(self)

        #just logic! disable stop button before starting
        self.btnCal.Enable(False)
        self.btnStop.Enable(False)
        self.btnPause.Enable(False)

        #make sure the layout is OK
        self.SetAutoLayout(True)
        #self.border.Fit(self) #called by UpdateSideChoices...
        #self.Layout()
        self.SetBackgroundColour((236,233,216))
        iconFile = "gtkwhiteboard.ico"
        icon1 = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon1)
	
	self.cbSaveOnExit.SetValue(True)
	if not self.LoadOptions():
		self.cbCalOnStart.Enable(False) #enabled only if we have calib data
		self.cbCalOnStart.SetValue(True)
		self.ReadOptions()	
		self.UpdateSideChoices()
	
    def SaveOptions(self):
	d = {}
	d['SidesEnabled'] = self.cbSides.IsChecked()
	d['TouchPadEnabled'] = self.cb1.IsChecked()
	d['LeftZones'] = self.chlnum.GetSelection()
	d['LeftZone1'] = self.chl1.GetSelection()
	d['LeftZone2'] = self.chl2.GetSelection()
	d['LeftZone3'] = self.chl3.GetSelection()
	d['RightZones'] = self.chrnum.GetSelection()
	d['RightZone1'] = self.chr1.GetSelection()
	d['RightZone2'] = self.chr2.GetSelection()
	d['RightZone3'] = self.chr3.GetSelection()
	d['CalibrateOnStart'] = self.cbCalOnStart.IsChecked()
	d['CalibrationDots'] = self.w.perspective.srcdots
	f = open(os.path.join(os.path.expanduser('~'),'.gtkwhiteboard'), 'w')
	f.write(repr(d))
	f.close()
	
    def LoadOptions(self):
	try:
		f = open(os.path.join(os.path.expanduser('~'),'.gtkwhiteboard'), 'r')
		dstr = f.read()
		f.close()
		d = eval(dstr)    
		if d['SidesEnabled']: self.w.Options.EnableSides()
		else: self.w.Options.DisableSides()
		if d['TouchPadEnabled']: self.w.Options.EnableTouchPad()
		else: self.w.Options.DisableTouchPad()
		self.w.Options.LeftZones = d['LeftZones']
		self.w.Options.LeftZone1 = d['LeftZone1']
		self.w.Options.LeftZone2 = d['LeftZone2']
		self.w.Options.LeftZone3 = d['LeftZone3']
		self.w.Options.RightZones = d['RightZones']
		self.w.Options.RightZone1 = d['RightZone1']
		self.w.Options.RightZone2 = d['RightZone2']
		self.w.Options.RightZone3 = d['RightZone3']
		self.ReadOptions()		
		self.cbCalOnStart.SetValue(d['CalibrateOnStart'])
		self.UpdateSideChoices()
		self.w.perspective.setsrc(*d['CalibrationDots'])
		return True
	except IOError:
		self.printOut("No config file found")
		return False
		
    def ReadOptions(self):
		self.cbSides.SetValue( self.w.Options.SidesEnabled())
		self.cb1.SetValue( self.w.Options.TouchPadEnabled())
		self.chlnum.SetSelection(self.w.Options.LeftZones)
		self.chl1.SetSelection(self.w.Options.LeftZone1)
		self.chl2.SetSelection(self.w.Options.LeftZone2)
		self.chl3.SetSelection(self.w.Options.LeftZone3)
		self.chrnum.SetSelection(self.w.Options.RightZones)
		self.chr1.SetSelection(self.w.Options.RightZone1)
		self.chr2.SetSelection(self.w.Options.RightZone2)
		self.chr3.SetSelection(self.w.Options.RightZone3)

    def WriteOptions(self):
		if self.cbSides.IsChecked(): self.w.Options.EnableSides()
		else: self.w.Options.DisableSides()
		if self.cb1.IsChecked(): self.w.Options.EnableTouchPad()
		else: self.w.Options.DisableTouchPad()
		self.w.Options.LeftZones = self.chlnum.GetSelection()
		self.w.Options.LeftZone1 = self.chl1.GetSelection()
		self.w.Options.LeftZone2 = self.chl2.GetSelection()
		self.w.Options.LeftZone3 = self.chl3.GetSelection()
		self.w.Options.RightZones = self.chrnum.GetSelection()
		self.w.Options.RightZone1 = self.chr1.GetSelection()
		self.w.Options.RightZone2 = self.chr2.GetSelection()
		self.w.Options.RightZone3 = self.chr3.GetSelection()

    def EvtQuit(self,event):
		if self.cbSaveOnExit.IsChecked(): self.SaveOptions()
		self.Destroy()
    def EvtOptionsChanged(self,event):
	    self.ReadOptions()
	    self.UpdateSideChoices()
	    
    def GetBattery(self):
	    if self.w:
		    return self.w.GetBattery()
		    
    def printOut(self,strList,newLine=True): 
		"""send an event to the panel to show the text in logger"""
		evt = LoggerEvent(value = strList,newline = newLine)
		wx.PostEvent(self, evt)

    def EvtChoiceLNum(self, event):
		num = int(event.GetString())
		if num == 3:
			self.chl1.Show(True)
			self.chl2.Show(True)
			self.chl3.Show(True)
		elif num == 2:
			self.chl1.Show(True)
			self.chl2.Show(True)
			self.chl3.Show(False)
		else:
			self.chl1.Show(True)
			self.chl2.Show(False)
			self.chl3.Show(False)
		self.RefreshLayout()
		self.WriteOptions()
		
    def EvtChoiceRNum(self, event):
		num = int(event.GetString())
		if num == 3:
			self.chr1.Show(True)
			self.chr2.Show(True)
			self.chr3.Show(True)
		elif num == 2:
			self.chr1.Show(True)
			self.chr2.Show(True)
			self.chr3.Show(False)
		else:
			self.chr1.Show(True)
			self.chr2.Show(False)
			self.chr3.Show(False)
		self.RefreshLayout()
		self.WriteOptions()
    def UpdateSideChoices(self):
		if self.cbSides.IsChecked():
			num = int(self.chlnum.GetStringSelection())
			if num == 3:
				self.chl1.Show(True)
				self.chl2.Show(True)
				self.chl3.Show(True)
			elif num == 2:
				self.chl1.Show(True)
				self.chl2.Show(True)
				self.chl3.Show(False)
			else:
				self.chl1.Show(True)
				self.chl2.Show(False)
				self.chl3.Show(False)
			num = int(self.chrnum.GetStringSelection())
			if num == 3:
				self.chr1.Show(True)
				self.chr2.Show(True)
				self.chr3.Show(True)
			elif num == 2:
				self.chr1.Show(True)
				self.chr2.Show(True)
				self.chr3.Show(False)
			else:
				self.chr1.Show(True)
				self.chr2.Show(False)
				self.chr3.Show(False)
		else: self.optionBox.ShowItems(False)
		self.RefreshLayout()
		
		
    def EvtLogger(self,event):
	    for all in event.value:
		    self.logger.AppendText(str(all))
	    if event.newline: self.logger.AppendText('\n')
    
    def EvtBtnStart(self,event):
	    if not self.w.IsConnected(): 
		    print "running new thread self.w.connect"
		    thread.start_new_thread(self.w.Connect, ())
	    else: thread.start_new_thread(self.w.Run,())

    def EvtBtnStop(self,event):
		self.printOut(['Disconnecting Wiimote.'])
		thread.start_new_thread(self.w.Disconnect,())
    
    def EvtBtnCal(self,event):
		thread.start_new_thread(self.w.Calibrate,())
		
    def EvtBtnPause(self,event):
		self.w.Stop()
		
    def EvtWiimoteCalibrating(self,event):
	    self.sb.SetStatusText("Calibrating",0)
	    self.btnStop.Enable(True)
	    self.btnCal.Enable(False)
	    
    def EvtWiimoteCalibrated(self,event):
	    self.cbCalOnStart.Enable(True)
	    thread.start_new_thread(self.w.Run,())

    def EvtWiimoteRunning(self,event):
	    self.sb.SetStatusText("Running",0)
	    self.btnCal.Enable(True)
	    self.btnStop.Enable(True)
	    self.btnStart.Enable(False)
	    self.btnPause.Enable(True)
	    
    def EvtCbSaveOnExit(self, event):       
	if event.IsChecked():
		self.cbSaveOnExit.SetValue(True)
	else: self.cbSaveOnExit.SetValue(False)
		
    def EvtWiimoteStopped(self,event):
	    self.sb.SetStatusText("Paused",0)
	    self.btnStart.Enable(True)
	    self.btnPause.Enable(False)
	    
    def EvtWiimoteConnected(self, event):
	    print "evtwiimoteconnected"
	    if self.cbCalOnStart.IsChecked():    thread.start_new_thread(self.w.Calibrate,())
	    else: 
		    print "starting thread run"
		    thread.start_new_thread(self.w.Run,())
		    
	    self.sb.SetStatusText("Connected",1)
	    
    def EvtNoWiimoteFound(self,event):
	    self.sb.SetStatusText("Not Running",0)
	    self.printOut(["Couldn't find wiimote."])
	    self.btnStart.Enable(True)
	    
    def EvtWiimoteConnecting(self, event):
	    self.sb.SetStatusText("Connecting",0)
	    self.btnStart.Enable(False)
	    
    def EvtWiimoteDisconnected(self,event):
	    self.printOut(["Disconnected successfully"])
	    self.sb.SetStatusText("Disconnected",1)
	    self.sb.SetStatusText("Not Running",0)
	    self.btnStart.Enable(True)
	    self.btnStop.Enable(False)
	    self.btnCal.Enable(False)
	    
    def EvtCbTP(self, event):
	if event.IsChecked(): 
		self.w.Options.EnableTouchPad()
	else:
		self.w.Options.DisableTouchPad()
		
    def EvtCbCal(self, event):       
	if event.IsChecked():
		self.cbCalOnStart.SetValue(True)
	else: self.cbCalOnStart.SetValue(False)
		
    def EvtCbSides(self,event):
	if event.IsChecked():
		self.w.Options.EnableSides()
		self.optionBox.ShowItems(True)
		self.UpdateSideChoices()
	else:
		self.w.Options.DisableSides()
		self.optionBox.ShowItems(False)
		self.RefreshLayout()
	
    def EvtChSides(self,event):
	self.WriteOptions()
	
    def RefreshLayout(self):
	self.border.Fit(self)
	self.Layout()
#---------------------------------------------------------------------------

if __name__ == '__main__':
 
    app = wx.PySimpleApp()

    #frame = wx.Frame(None, -1, "Wiimote Whiteboard Control")
    #sb = frame.CreateStatusBar() # A Statusbar in the bottom of the window
    #sb.SetStatusText("Nothing")
    frame = MainWindow(None,"Wiimote Whiteboard Controller")
    frame.Show(1)
    app.MainLoop()
