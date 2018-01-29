#!/usr/bin/env python
"""""""""""""""""""""""""""""""""
Author: Dan Pierce
Date: 2018.01.28
"""""""""""""""""""""""""""""""""
import rospy
import os
import sys
import rosbag
from ros_sensor_msgs.msg import RawMeasurementsTagged,AssuranceLevel,GpsEphemerisTagged
from drtk.msg import DrtkOutput

# import rosmsg
# from rosmsg import rosmsg_cmd_list, MODE_MSG, MODE_SRV, list_types

# # thi = rosmsg_cmd_list(MODE_MSG, 'messages', ['list'])
# # print thi

# # print rosmsg.fullusage(MODE_MSG)

# print rosmsg.list_types('drtk', mode='.msg')


msg = RawMeasurementsTagged()
print msg._get_types



inMsg = DrtkOutput()

inMsg.rpvNorm = 5.0

val = getattr(inMsg,'rpvNorm')

print val

# --- 
outMsg = DrtkOutput()

# print DrtkOutput.__dict__.keys()
# print outMsg._get_types
# print outMsg.__slots__
# print outMsg._type
# setattr(outMsg, 'rpvNorm', 5)
# getattr(outMsg, 'rpvNorm')


for slot in outMsg.__slots__:
    val = getattr(inMsg,slot)
    setattr(outMsg, slot, val)

        # outMsg.slot = 2.0


print outMsg