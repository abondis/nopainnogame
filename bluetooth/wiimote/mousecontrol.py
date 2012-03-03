#!/usr/bin/python
#
# mousecontrol.py - Simple Xlib/win32 calls to move the mouse and simulate clicks. Can also get screen resolution.
#                   works on Windows and Linux
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

import sys
if sys.platform == 'win32':
    
    import win32api
    import win32con

    class MouseControl:
        def __init__(self):
            pass

        def mouse_click(self, button):
            if button in [4,5]:
                if button == 4:
                    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,0,0,win32con.WHEEL_DELTA)
                elif button == 5:
                    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,0,0,-win32con.WHEEL_DELTA)    
            else:
                self.mouse_down(button)
                self.mouse_up(button)
            
        def mouse_down(self, button):   #button= 1 left, 2 middle, 3 right, 4 and 5 are wheelup/down
            if button == 1:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            elif button == 2:
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0)
            elif button == 3:
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)    
            
        def mouse_up(self, button):
            if button == 1:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            elif button == 2:
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0)
            elif button == 3:
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)    

        def mouse_warp(self, x,y):
            res = self.get_screen_resolution()
            x = x*65535/res[0]
            y = y*65535/res[1]
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE|win32con.MOUSEEVENTF_ABSOLUTE, x,y)

        def get_screen_resolution(self,device=1):
            screeninfo = win32api.GetMonitorInfo(device)
            return screeninfo['Work'][2], screeninfo['Work'][3]
else:
    import Xlib.display
    import Xlib.ext.xtest

    class MouseControl:
        def __init__(self):
            self.display = Xlib.display.Display()
            self.screen = self.display.screen()
            self.root = self.screen.root

        def mouse_click(self, button):
            self.mouse_down(button)
            self.mouse_up(button)
            
        def mouse_down(self, button):   #button= 1 left, 2 middle, 3 right
            Xlib.ext.xtest.fake_input(self.display,Xlib.X.ButtonPress, button)
            self.display.sync()

        def mouse_up(self, button):
            Xlib.ext.xtest.fake_input(self.display,Xlib.X.ButtonRelease, button)
            self.display.sync() 

        def mouse_warp(self, x,y):
            self.root.warp_pointer(x,y)
            self.display.sync()
        
        def get_screen_resolution(self):
            return self.screen['width_in_pixels'], self.screen['height_in_pixels']
            


