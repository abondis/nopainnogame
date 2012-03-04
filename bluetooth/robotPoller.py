import robotLib
import myRobots
import time

#class RobotPoller:
r=robotLib.Robot()
mr=myRobots.MyRobots()

while True:
  data=mr.read()
  if data['field5'] == u'0':
    r.write(data['field4'] + ';')
    data['field5'] = u'1'
    mr.write(data)
  time.sleep(2)
