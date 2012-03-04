import robotLib
import myRobots
import time

#class RobotPoller:
r=robotLib.Robot()
mr=myRobots.MyRobots()
debug=True

while True:
  data=mr.read()
  if debug: print "read data from cloud: ", data
  if data['updated'] == "true" and data['field4'] != None: 
    r.write(str(data['field4']) + ';')
    if debug: print "wrote data to robot: ", data['field4'] + ';'
  
  robotdata=r.read()
  if debug: print "read data from robot: ", robotdata
  if robotdata != None:
    mr.write({'field1': robotdata})
    if debug: print "wrote data to cloud: ", {'field1': robotdata}
  time.sleep(2)
