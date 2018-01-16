#!/usr/bin/env python
import sys
import rospy

from math import atan2,pi,sin,cos

from drtk.msg import DrtkOutput
from geometry_msgs.msg import Vector3Stamped

from wgs_conversions.srv import WgsConversion

import numpy as np

rospy.init_node('dual_antenna_attitude')

pub = rospy.Publisher('~euler', Vector3Stamped, queue_size=1)

ref_lat = rospy.get_param('latitude_reference', 32.5955)  
ref_lon = rospy.get_param('longitude_reference', -85.2954)  
ref_alt = 0.0

rospy.wait_for_service('xyz2enu_vel')

xyz2enu_vel = rospy.ServiceProxy('xyz2enu_vel', WgsConversion)

# --- wrap angles
def wrapToPi(psi):
  return ( psi + pi) % (2 * pi ) - pi

def drtkCallback(msg):

  # Note: this only works well for a ground vehicle where roll and pitch are small

  dx = -msg.rpvEcef.x
  dy = -msg.rpvEcef.y
  dz = -msg.rpvEcef.z

  rsp = xyz2enu_vel(xyz=(dx,dy,dz),ref_lla=(ref_lat,ref_lon,ref_alt))
  (dE,dN,dU)=rsp.enu

  psi = wrapToPi(atan2(dE,dN) - pi/2.0) # note: subtract pi/2 because of mounting locations of antennas

  r_lr_n = np.array([[dN],[dE],[-dU]])

  Cn1 = np.matrix([[ cos(psi), sin(psi), 0.0],
                   [-sin(psi), cos(psi), 0.0], 
                   [      0.0,      0.0, 1.0]])

  r_lr_1 = Cn1*r_lr_n

  phi = atan2(r_lr_1[2],r_lr_1[1])

  att_msg = Vector3Stamped()
  
  att_msg.header.stamp = msg.header.stamp
  
  att_msg.vector.x = phi
  att_msg.vector.y = 0.0
  att_msg.vector.z = psi

  pub.publish(att_msg)

def main():

  drtk_sub = rospy.Subscriber("/drtk_node/drtkOutput",DrtkOutput,drtkCallback,queue_size=100)

  rospy.spin()


if __name__ == '__main__':
  main()

