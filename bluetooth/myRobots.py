import httplib
import json
import copy
import time

class MyRobots:

  conn = None

  def __init__(self, key="1647186ED7164FCE",url="bots.myrobots.com"):
    self.key=key
    self.url=url

  def write(self, newdict, noReadFirst=False):
    self.conn = httplib.HTTPConnection(self.url)
    val=""
    if noReadFirst:
      current=newdict
    else:
      current=self.read()
      for key in newdict.keys():
        current[key] = newdict[key]
    for key in current.keys():
      val+= "&" + key + "=" + str(current[key])
    val+="&status=true"
    self.conn.request("GET", "/update?key="+self.key+val)
    while self.conn.getresponse().read() == '0':
      time.sleep(2)
      self.conn.request("GET", "/update?key="+self.key+val)

  def read(self):
    self.conn = httplib.HTTPConnection(self.url)
    self.conn.request("GET","/channels/589/feed/last.json")
    data = json.loads(self.conn.getresponse().read())
    return data

