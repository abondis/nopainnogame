import bluetooth
import time

class Robot:
  """ 
  Data from robot: dest,dist,collision[:dest,dist,collision[:...]];
  Data to robot: dest,dist,contournement[:dest,dist,contournement[:...]];
   deg is actually a value from 0 to 3 for 90,180,270,360.
   collision is 1 if there is an object in front at that moment, 0 otherwise.
   contournement is 0,l or r, for the robot to go around an object.
   the closing ";" is not used outside this class.
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
    counter = 0
    while data[-1] != ";" and counter < 10:
      newdata = self.read()
      if newdata: data += newdata
      counter += 1
    return data[0:-1]

  def write(self, value):
      value += ";"
      self.client_socket.send(value)

