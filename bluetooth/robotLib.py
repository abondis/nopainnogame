import bluetooth

class Robot:

  client_socket=None

  def __init__(self, hwaddress="00:19:5D:EE:24:1C", channel=1):
    self.client_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    self.client_socket.connect((hwaddress,channel))
  
  def goLeft(self, inc=1):
    self.client_socket.send("a" + str(inc))

  def goRight(self, inc=1):
    self.client_socket.send("d" + str(inc))

  def goForward(self, inc=1):
    self.client_socket.send("w" + str(inc))

  def goBackward(self, inc=1):
    self.client_socket.send("s" + str(inc))

  def read(self):
    return self.client_socket.recv(1024)
