#!/usr/bin/env python
"""""""""""""""""""""""""""""""""
Author: Dan Pierce
Date: 2018.1.29
"""""""""""""""""""""""""""""""""
import sys
import rospy

from nav_msgs.msg import Odometry
from drtk.msg import DrtkOutput
from dbw_mkz_msgs.msg import SteeringReport

# prm = # get parameters for vehicle

# --- Read steer messages
steerTopic = '/vehicle/wheel_speed_report'

prevTime = None
for topic, msg, t in rosbag.Bag(inputBagfile).read_messages(): # loop through all messages in bagfile
  if (topic == steerTopic):
    if prevTime is not None:
      dt = msgs.header.stamp.time.to_sec()-prevTime

      vel_ = msg.speed
      del_ = -msg.steering_wheel_angle/prm.Nsw

      propagateModel(vel_,del_,dt,prm)



    prevTime = msgs.header.stamp.time.to_sec()
    

    i++


# --- Loop through steer messages
k=1
while (k < len(steerMsgs)):
  vel = steerMsgs[i].speed
  delt = -steerMsgs[i].steering_wheel_angle/prm.Nsw

  steer

  k++

























rospy.init_node('base_drtk_to_odom')

pub = rospy.Publisher('~odom', Odometry, queue_size=1000)

drtkTopic = rospy.get_param('~drtk_topic','/drtk_node/drtkOutput')
dt = rospy.get_param('~sample_rate',0.5)

baseStationPosEcefX = 441110.4720
baseStationPosEcefY = -5360805.4003
baseStationPosEcefZ = 3416335.7718

global prevPosX, prevPosY, prevPosZ

prevPosX = None

def drtkCallback(msg):

  global prevPosX, prevPosY, prevPosZ

  posX = msg.rpvEcef.x + baseStationPosEcefX
  posY = msg.rpvEcef.y + baseStationPosEcefY
  posZ = msg.rpvEcef.z + baseStationPosEcefZ

  # Note: using this with estimation could cause problems
  if prevPosX is not None:
    velX = (posX - prevPosX)/dt
    velY = (posY - prevPosY)/dt
    velZ = (posZ - prevPosZ)/dt

  prevPosX = posX
  prevPosY = posY
  prevPosZ = posZ

  if (msg.outputState.state == 5):
      odom_msg = Odometry()

      odom_msg.header = msg.header
      odom_msg.header.frame_id = 'ecef'

      odom_msg.pose.pose.position.x = posX
      odom_msg.pose.pose.position.y = posY
      odom_msg.pose.pose.position.z = posZ

      odom_msg.pose.covariance[0] = 0.0005
      odom_msg.pose.covariance[7] = 0.0005
      odom_msg.pose.covariance[14] = 0.0005

      odom_msg.twist.twist.linear.x = velX
      odom_msg.twist.twist.linear.y = velY
      odom_msg.twist.twist.linear.z = velZ

      odom_msg.twist.covariance[0] = 1.0
      odom_msg.twist.covariance[7] = 1.0
      odom_msg.twist.covariance[14] = 1.0

      pub.publish(odom_msg)

def main():

  drtk_sub = rospy.Subscriber(drtkTopic,DrtkOutput,drtkCallback,queue_size=1000)

  # --- For control on odom callback
  rospy.spin()

if __name__ == '__main__':

  main()

