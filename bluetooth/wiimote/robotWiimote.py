import robotLib
import linuxWiimoteLib

class robotWiimote(robotLib.Robot):
  def __init__(self):
    robotLib.Robot.__init__(self)
    try:
      self.wiimote = linuxWiimoteLib.Wiimote()
    except:
      self.wiimote = linuxWiimoteLib.Wiimote()
    self.wiimote.SetLEDs(True,False,False,False)
    self.wiimote.SetReportType(self.wiimote.InputReport.IRAccel,True)
    
  def getXMiddle()
    X2=self.wiimote.WiimoteState.IRState.RawX2
    X1=self.wiimote.WiimoteState.IRState.RawX1
    if X1 != 1023 and X2 != 1023:
      return (X1+X2/2)
    else:
      return -1

  def barVisible()
    if self.getXMiddle() == -1: return false
    else: return true
    
  def findBar()
    while self.getXMiddle() == -1: self.goLeft()

  def getInPosition()
