#!/usr/bin/env python
"""""""""""""""""""""""""""""""""
Author: Dan Pierce
Date: 2018.01.28
"""""""""""""""""""""""""""""""""
import rospy
import os
import sys
import rosbag
from ros_sensor_msgs.msg import RawMeasurementsTagged,AssuranceLevel,GpsEphemerisTagged,Tags
from drtk.msg import DrtkOutput

def fixBagfile(inputBagfile,outputBagfile):

    rawTopic1 = '/novatel_rear/rawMeasurementsTagged'
    rawTopic2 = '/novatel_front/rawMeasurementsTagged'
    ephemTopic = '/novatel_rear/gpsEphemerisTagged'
    drtkTopic = '/drtk_node/drtkOutput'

    t_init = 0.0
    t_final = 0.0

    with rosbag.Bag(outputBagfile, 'w') as outbag: # open output bagfile for writing

        for topic, msg, t in rosbag.Bag(inputBagfile).read_messages(): # loop through all messages in bagfile

            # print topic

            if (topic == rawTopic1) or (topic == rawTopic2):

                outMsg = RawMeasurementsTagged()

                for slot in msg.__slots__:
                    subMsg = getattr(msg,slot)
                        
                    if (slot=='tags'):
                        subOutMsg = Tags()
                        for subSlot in subMsg.__slots__:
                            val = getattr(subMsg,subSlot)
                            setattr(subOutMsg, subSlot, val)
                    else:
                        subOutMsg = subMsg

                    setattr(outMsg, slot, subOutMsg)
            
            elif topic == ephemTopic:

                outMsg = GpsEphemerisTagged()

                for slot in msg.__slots__:
                    subMsg = getattr(msg,slot)
                        
                    if (slot=='tags'):
                        subOutMsg = Tags()
                        for subSlot in subMsg.__slots__:
                            val = getattr(subMsg,subSlot)
                            setattr(subOutMsg, subSlot, val)
                    else:
                        subOutMsg = subMsg

                    setattr(outMsg, slot, subOutMsg)
            
            elif topic == drtkTopic:

                outMsg = DrtkOutput()
                
                for slot in msg.__slots__:
                    val = getattr(msg,slot)
                    setattr(outMsg, slot, val)
            
            else:
            
                outMsg = msg

            if (topic!='/rosout') and (topic!='/can_bus_dbw/can_rx') and (topic!='/can_bus_dbw/can_tx'):

                # if (t_init==0.0):
                #     t_init = t.to_sec()
                #     print 'From time = ',t_init
                # t_final = t.to_sec()
                
                outbag.write(topic, outMsg, msg.header.stamp if msg._has_header else t)

    # print 'To time = ',t_final,' (Duration = ',t_final-t_init,')'





# if __name__ == '__main__':
#   main(sys.argv)