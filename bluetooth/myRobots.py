import httplib
import json
import time

class MyRobots:

  conn = None

  def __init__(self, key="1647186ED7164FCE",url="bots.myrobots.com"):
    self.key=key
    self.url=url
    self.entry_id=0
    self.entry_id=self.read()["entry_id"]

  def write(self, newdict):
    self.conn = httplib.HTTPConnection(self.url)
    val=""
    for key in newdict.keys():
      val+= "&" + key + "=" + str(newdict[key])
    val+="&status=true"
    self.conn.request("GET", "/update?key="+self.key+val)
    returnid = self.conn.getresponse().read()
    while returnid == '0':
      time.sleep(2)
      self.conn.request("GET", "/update?key="+self.key+val)
      returnid = self.conn.getresponse().read()
    self.entry_id=int(returnid)

  def read(self):
    self.conn = httplib.HTTPConnection(self.url)
    self.conn.request("GET","/channels/589/feed/last.json")
    data = json.loads(self.conn.getresponse().read())
    if data["entry_id"] == self.entry_id: data["updated"] = "false"
    else: data["updated"] = "true"
    self.entry_id=data["entry_id"]
    return data

