import bluetooth
import time

class Robot:
  """ 
  Data from robot: f|l|r|b,millimeters_or_deg,0|1
  Data to robot: f|l|r|b,millimeters_or_deg;
   deg is actually a value from 0 to 3 for 90,180,270,360
  """

  client_socket=None

  def __init__(self, hwaddress="00:19:5D:EE:24:1C", channel=1):
    self.client_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    self.client_socket.connect((hwaddress,channel))
    self.client_socket.setblocking(False)
  
  def read(self):
    try: 
      data=self.client_socket.recv(1)
    except bluetooth.BluetoothError: 
      time.sleep(.05)
      return None
    # We got data, let's read until we get a ";" 
    while data[-1] != ";":
      newdata = self.read()
      if newdata: data += newdata
    return data

  def write(self, value):
      self.client_socket.send(value)
    

