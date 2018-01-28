#!/usr/bin/env python
import sys
import rospy

from math import atan2,pi,sin,cos

from drtk.msg import DrtkOutput
from tdcp.msg import TdcpOutput
from path_duplication_launch.msg import DualAntennaOutput

from wgs_conversions.srv import WgsConversion

import numpy as np

rospy.init_node('dual_antenna')

pub = rospy.Publisher('~dualAntennaOutput', DualAntennaOutput, queue_size=1000)

ref_lat = rospy.get_param('latitude_reference', 32.5955)  
ref_lon = rospy.get_param('longitude_reference', -85.2954)  
ref_alt = 0.0

gpsDt = 0.5

rospy.wait_for_service('xyz2enu_vel')

tdcp2enu = rospy.ServiceProxy('xyz2enu_vel', WgsConversion)
drtk2enu = rospy.ServiceProxy('xyz2enu_vel', WgsConversion)

global tdcp_data, drtk_data

#           [data @ (k-1),data @ (k)]
tdcp_data = [DualAntennaOutput()]*2
drtk_data = [DualAntennaOutput()]*2

tdcp_data[0].gps_seconds = 1.0

# --- unwrap angles
def averageAngles(ang1,ang2):
  return atan2((sin(ang1)+sin(ang2))/2,(cos(ang1)+cos(ang2))/2)

# --- wrap angles
def wrapToPi(yaw):
  return ( yaw + pi) % (2 * pi ) - pi

def syncAndPub():
  global tdcp_data, drtk_data

  if (tdcp_data[0].gps_seconds!=drtk_data[0].gps_seconds):
    return

  yaw = drtk_data[0].yaw
  roll = drtk_data[0].roll

  speed = (tdcp_data[0].speed + tdcp_data[1].speed)/2
  course = averageAngles(tdcp_data[0].course,tdcp_data[1].course)

  slip = wrapToPi(course - yaw)

  vx = speed*cos(slip)
  vy = speed*sin(slip)

  msg = DualAntennaOutput()

  msg = drtk_data[0]

  msg.speed = speed
  msg.course = course
  msg.vx = vx
  msg.vy = vy
  
  pub.publish(msg)

def tdcpCallback(msg):
  global tdcp_data

  data = DualAntennaOutput()

  # --- time
  data.gps_seconds = msg.gpsTime.gps_seconds
  data.header.stamp = msg.header.stamp
  
  # --- rpv
  dx=msg.rpvEcef.x
  dy=msg.rpvEcef.y
  dz=msg.rpvEcef.z
  rsp = tdcp2enu(xyz=(dx,dy,dz),ref_lla=(ref_lat,ref_lon,ref_alt))
  (dE,dN,dU)=rsp.enu
  dD=-dU

  # --- data
  data.speed = pow(pow(dN,2) + pow(dE,2),0.5)/gpsDt

  data.course = atan2(dE,dN) # not course exactly, delayed by half a step

  # --- queue
  tdcp_data[0] = tdcp_data[1]
  tdcp_data[1] = data

  syncAndPub()

def drtkCallback(msg):
  global drtk_data

  if (msg.outputState.state!=4):
    return

  data = DualAntennaOutput()

  # --- time
  data.gps_seconds = msg.gpsTime.gps_seconds
  data.header.stamp = msg.header.stamp

  # --- rpv
  # Note: this only works well for a ground vehicle where roll and pitch are small
  dx=msg.rpvEcef.x
  dy=msg.rpvEcef.y
  dz=msg.rpvEcef.z
  rsp = drtk2enu(xyz=(dx,dy,dz),ref_lla=(ref_lat,ref_lon,ref_alt))
  (dE,dN,dU)=rsp.enu
  dD=-dU
  
  # --- data
  data.yaw = wrapToPi(atan2(-dE,-dN) - pi/2.0) # note: subtract pi/2 because of mounting locations of antennas, also DRTK is from lead to follower, so make negative

  r_lr_n = -np.array([[dN],[dE],[dD]])

  Cn1 = np.matrix([[ cos(data.yaw), sin(data.yaw), 0.0],
                   [-sin(data.yaw), cos(data.yaw), 0.0], 
                   [      0.0,      0.0, 1.0]])

  r_lr_1 = Cn1*r_lr_n

  data.roll = atan2(r_lr_1[2],r_lr_1[1])

  # --- queue
  drtk_data[0] = drtk_data[1]
  drtk_data[1] = data

  syncAndPub()
  
def main():

  drtk_sub = rospy.Subscriber("/drtk_node/drtkOutput",DrtkOutput,drtkCallback,queue_size=1000)
  tdcp_sub = rospy.Subscriber("/tdcp_node/tdcpOutput",TdcpOutput,tdcpCallback,queue_size=1000)

  rospy.spin()


if __name__ == '__main__':
  main()

