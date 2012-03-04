import httplib
import json

class MyRobots:

  conn = None

  def __init__(self, key="1647186ED7164FCE",url="bots.myrobots.com"):
    self.key=key
    self.url=url

  def write(self, newdict):
    self.conn = httplib.HTTPConnection(self.url)
    current=self.read()
    val=""
    for key in newdict.keys():
      current[key] = newdict[key]
    for key in current.keys():
      val+= "&" + key + "=" + str(current[key])
    self.conn.request("GET", "/update?key="+self.key+val)

  def read(self):
    self.conn = httplib.HTTPConnection(self.url)
    self.conn.request("GET","/channels/589/feed/last.json")
    return json.loads(self.conn.getresponse().read())

