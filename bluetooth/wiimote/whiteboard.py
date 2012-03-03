#!/usr/bin/python
#
# whiteboard.py - Wiimote whiteboard tracking software 
# 
#	REQUIRED LIBRARIES: python-xlib, pybluez, (psyco: optional)
#
#		Other files: "linuxWiimoteLib.py", "mousecontrol.py" 
#				"perspective.py"
#
#	TROUBLESHOOTING:
#
#	If you get errors about bluetooth, make sure you have pybluez installed,
#	as well as pybluez-utils. then, restart your bluetooth service 
#	(/etc/init.d/bluetooth restart) or your computer.
#
#	Tested and working on Mandriva 2007.1
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


import time
from mousecontrol import MouseControl
from perspective import Perspective

import sys
if sys.platform == 'win32':
    import CLR
    from CLR.System.Reflection import Assembly
    Assembly.LoadFrom("WiimoteLib.dll")
    Wiimote = CLR.WiimoteLib.Wiimote
else:
    from linuxWiimoteLib import Wiimote

class Options:
	#constants
	LCLICK = 0
	RCLICK = 1
	SCROLL= 2
	TOGGLETOUCHPAD = 3
	NONE = 4
	DCLICK = 5
	MCLICK = 6
	
	_sidesEnabled = True #DEFAULT
	_touchPadMode = True
	
	LeftZones = 0 #0 means 1, 1 means 2, etc.
	LeftZone1 = SCROLL
	LeftZone2 = 0
	LeftZone3 = 0
	
	RightZones = 0 #0 means 1, 1 means 2, etc.
	RightZone1 = RCLICK
	RightZone2 = 0
	RightZone3 = 0
	
	def TouchPadEnabled(self):
		return self._touchPadMode
	def SidesEnabled(self):
		return self._sidesEnabled
	
	def EnableTouchPad(self):
		self._touchPadMode = True
	def DisableTouchPad(self):
		self._touchPadMode = False
	
	def DisableSides(self):
		self._sidesEnabled = False
	def EnableSides(self):
		self._sidesEnabled = True
	
class Cursor:
	"""Object that keeps track of the IR pointer and makes the mouse move accordingly"""
	whichbuttonisdown = 0
	lastwasclick = False
	clickonside = False
	startscroll = None
	scrolling = False
		
	def __init__(self, parent):
		self.mousecontrol = parent.mouse
		self.parent = parent
		
		
	def update(self,light,state_changed,oldpos, newpos, timer):
		""" Tell 'update' if we see a light and what's the new position """
		
		if (newpos[0] > 0 and newpos[0]<self.parent.XRES) and not self.clickonside:
			if self.parent.Options.TouchPadEnabled(): #touchpadmode
				
				if light: 
					self.mousemove(newpos)
				else:
					if state_changed:
						if timer < self.parent.CLICKMAXTIME: 
							self.click()
							self.lastwasclick = True
						else: self.lastwasclick = False
					else:
						if timer > self.parent.MAXTIMEBETWEENCLICKDRAG:
							self.unclick() #safe to call many times...
			else: #no touchpadmode
				
				if light:
					if timer > self.parent.CLICKMINTIME or state_changed: self.mousemove(newpos)
					if state_changed: self.click()
				else:
					if state_changed: self.unclick()
		
		else: #if we are on the sides or if the click started on the side...
			if light and state_changed:
				self.clickonside = True
				if self.parent.Options.SidesEnabled():
					
					if (newpos[0]>self.parent.XRES) :
						
						if self.parent.Options.RightZones == 0 : currentopt = self.parent.Options.RightZone1
						elif self.parent.Options.RightZones == 1:
							if newpos[1] < self.parent.YRES/2: currentopt = self.parent.Options.RightZone1
							else: currentopt = self.parent.Options.RightZone2
						elif self.parent.Options.RightZones == 2:
							if newpos[1] < self.parent.YRES/3: currentopt = self.parent.Options.RightZone1
							elif newpos[1] >= self.parent.YRES/3 and newpos[1] < self.parent.YRES*2/3: currentopt = self.parent.Options.RightZone2
							else: currentopt = self.parent.Options.RightZone3
					elif (newpos[0] <0) :
						
						if self.parent.Options.LeftZones == 0 : currentopt = self.parent.Options.LeftZone1
						elif self.parent.Options.LeftZones == 1:
							if newpos[1] < self.parent.YRES/2: currentopt = self.parent.Options.LeftZone1
							else: currentopt = self.parent.Options.LeftZone2
						elif self.parent.Options.LeftZones == 2:
							if newpos[1] < self.parent.YRES/3: currentopt = self.parent.Options.LeftZone1
							elif newpos[1] >= self.parent.YRES/3 and newpos[1] < self.parent.YRES*2/3: currentopt = self.parent.Options.LeftZone2
							else: currentopt = self.parent.Options.LeftZone3
								
					if currentopt == self.parent.Options.RCLICK:
						self.click_and_release(3)
					elif currentopt == self.parent.Options.LCLICK:
						self.click_and_release()
					elif currentopt == self.parent.Options.DCLICK:
						self.click_and_release()
						time.sleep(0.1)
						self.click_and_release()
					elif currentopt == self.parent.Options.MCLICK:
						self.click_and_release(2)	
					elif currentopt == self.parent.Options.SCROLL:
						self.startscroll = newpos[1]
						self.scrolling = True
					elif currentopt == self.parent.Options.TOGGLETOUCHPAD:					
						if self.parent.Options.TouchPadEnabled():
							self.parent.Options.DisableTouchPad()
						else:
							self.parent.Options.EnableTouchPad()
						self.parent.OnOptionsChanged()
								
				
				
			elif not light and state_changed:
				self.clickonside = False
				self.lastwasclick = False #just a precaution
				self.scrolling = False #precaution again
				
				self.unclick() #safe to call even if nothing was clicked
				
			elif light and self.scrolling: #scrolling is active until no-light, even if we quit the side.
					if newpos[1] - self.startscroll > 10:
						self.scroll_down()
						self.startscroll = newpos[1]
						
					elif newpos[1] - self.startscroll < -10:
						self.scroll_up()
						self.startscroll = newpos[1]
						
	def click_and_release(self,butnum=1):
		self.mousecontrol.mouse_click(butnum)

	def click(self, butnum=1):
		if not self.whichbuttonisdown: #so we don't click twice in case there is a problem!
			self.mousecontrol.mouse_down(butnum)
			self.whichbuttonisdown = butnum	
			
	def unclick(self):
		if self.whichbuttonisdown:
			self.mousecontrol.mouse_up(self.whichbuttonisdown)
			self.whichbuttonisdown = 0
	
	def scroll_up(self):
		self.mousecontrol.mouse_click(4)
	
	def scroll_down(self):
		self.mousecontrol.mouse_click(5)
	
	def mousemove(self,newpos):
		
		self.mousecontrol.mouse_warp(*newpos)
		
class WhiteBoard:
	running = False
	mouseclicked = False
	calibrating = False	
	
	KEEPLIGHTTIME = 3 #will not consider if we lose the light for x frames
	CLICKMAXTIME = 5 #longest that we will consider as a click for touchpad mode
	CLICKMINTIME = 3 # will not move the pointer for the first x frames after click to help a singleclic with shaky hand
	MAXTIMEBETWEENCLICKDRAG = 5 #...
	
	def __init__(self):
		self.mouse = MouseControl()
		self.XRES,self.YRES = self.mouse.get_screen_resolution()
		self.XRES, self.YRES = float(self.XRES), float(self.YRES)
		self.ABCD = [(0,0),(self.XRES-5,0),(0,self.YRES-5),(self.XRES-5,self.YRES-5)]
		self.perspective = Perspective()
		self.perspective.setdst((0.0,0.0),(self.XRES,0.0),(0.0,self.YRES),(self.XRES,self.YRES))
		self.cursor = Cursor(self)
		self.Options = Options()
		
	def printOut(self,strList,newLine = True):
		for all in strList:
			print all,
		#if newLine: print ""
		print ""
	
	def GetBattery(self):
		try:
			bat = self.wiimote.WiimoteState.Battery
		except AttributeError:
			return None
		if bat: return  bat*100/200
		else: return None
		
	def Connect(self):
		self.wiimote = Wiimote()
		self.OnConnecting()
		if sys.platform != 'win32': self.printOut(["Press 1 and 2 on wiimote"])
		#try:
		self.wiimote.Connect()
		#except:
		#	self.OnNoWiimoteFound()
		#	raise SystemExit
		self.OnConnected()
		self.wiimote.SetLEDs(True,False,False,False)
		self.wiimote.SetReportType(self.wiimote.InputReport.IRAccel,True)
	
	def IsConnected(self):
		try:
			cn = self.wiimote.running
		except:
			return False
		return cn
		
		
	def IsRunning(self):
		return self.running
	
	def OnRun(self): #to be overloaded
		pass
		
	def OnConnected(self): #to be overloaded
		self.printOut(["Battery: ", self.GetBattery(), "%"])
	
	def OnConnecting(self): #to be overloaded
		pass
	
	def OnDisconnect(self): #to be overloaded
		pass
	
	def OnStop(self): #to be overloaded
		pass
		
	def OnCalibrated(self): #to be overloaded
		pass
	
	def OnCalibrating(self):
		pass
		
	def OnNoWiimoteFound(self):
		print "No Wiimote or no Bluetooth found..."
		pass
		
	def OnOptionsChanged(self):
		pass
		
	def Run(self):
		
		self.running = True
		
		keep_light = self.KEEPLIGHTTIME
		x,y = (0,0)
		first_x, first_y = (0,0)
		light_state = False
		timer = 0
		
		self.OnRun()
		
		while self.running:
			if self.wiimote.WiimoteState.ButtonState.A:
				self.Stop()
				continue

			time.sleep(0.030)
			
			if self.wiimote.WiimoteState.IRState.Found1: 
				if not light_state: #if the light appears
					light_state = True
					first_x,first_y = map(int,self.perspective.warp(self.wiimote.WiimoteState.IRState.RawX1, self.wiimote.WiimoteState.IRState.RawY1))
					x,y = first_x, first_y
					timer = 0 #reset timer
					self.cursor.update(light_state, True, (first_x,first_y), (x,y), timer)
					
				else: #if the light is still lit
					x,y = map(int,self.perspective.warp(self.wiimote.WiimoteState.IRState.RawX1, self.wiimote.WiimoteState.IRState.RawY1))
					timer += 1
					keep_light = self.KEEPLIGHTTIME #keep it high while light is seen.
					self.cursor.update(light_state, False, (first_x,first_y), (x,y), timer)
			
			else:
				if keep_light and timer > self.KEEPLIGHTTIME: keep_light -= 1 #keep_light will not prevent cut-off if the light goes out quick
				else:
					if light_state:
						light_state = False
						self.cursor.update(light_state, True, (first_x,first_y), (x,y), timer)
						timer = self.KEEPLIGHTTIME - keep_light #this is the true delay since the light has gone off, not 0
					else:
						timer += 1
						self.cursor.update(light_state, False, (first_x,first_y), (x,y), timer)
						
					
			
	
	def Stop(self):
		self.running = False
		self.OnStop()
		
	def Disconnect(self):
		if self.IsRunning: self.Stop()
		self.wiimote.Disconnect()
		self.OnDisconnect()
		if self.calibrating: raise SystemExit
		del self.wiimote
		
	def Calibrate(self):
		self.Stop()
		self.calibrating = True
		self.OnCalibrating()
		self.printOut(["Point to the top left corner of the screen... "],False)
		self.ABCD[0] = self.WaitForLight()
		self.printOut(["OK"])
		
		self.WaitNoLight()
		self.printOut(["Point to the top right corner of the screen... "],False)
		self.ABCD[1] = self.WaitForLight()
		self.printOut([ "OK"])
		
		self.WaitNoLight()
		self.printOut([ "Point to the bottom left corner of the screen... "],False)
		self.ABCD[2] = self.WaitForLight()
		self.printOut([ "OK"])
		
		self.WaitNoLight()
		self.printOut([ "Point to the bottom right corner of the screen... "],False)
		self.ABCD[3] = self.WaitForLight()
		self.printOut([ "OK"])
	
		self.WaitNoLight()
		
		x0,y0 = self.ABCD[0]
		x1,y1 = self.ABCD[1]
		x2,y2 = self.ABCD[2]
		x3,y3 = self.ABCD[3]
		self.perspective.setsrc((x0,y0),(x1,y1),(x2,y2),(x3,y3))
		
		self.calibrating = False
		self.printOut([ "Calibration complete!"])
		self.OnCalibrated()
		
	def WaitForLight(self):
		dot = False
		while not dot:
			checkdot = self.wiimote.WiimoteState.IRState.RawX1, self.wiimote.WiimoteState.IRState.RawY1
			if self.wiimote.WiimoteState.IRState.Found1:
				dot = checkdot
				return dot
			time.sleep(0.030)
			
	def WaitNoLight(self):
		time.sleep(0.5)
		while 1:
			time.sleep(0.030)
			if self.wiimote.WiimoteState.IRState.Found1 == False:
				return


if __name__ == "__main__": 
	print "For graphical interface, please run 'gtkwhiteboard,py'"	
	whiteboard = WhiteBoard()	
	try:
		import psyco
		psyco.full()
	except:
		print "Not using psyco"
	whiteboard.Connect()
	whiteboard.Calibrate()
	print "Press A on wiimote to quit"	
	try:
		whiteboard.Run()
	except KeyboardInterrupt:
		whiteboard.Disconnect()
	time.sleep(5)
	whiteboard.Connect()
	whiteboard.Calibrate()
	try:
		whiteboard.Run()
	except KeyboardInterrupt:
		whiteboard.Disconnect()