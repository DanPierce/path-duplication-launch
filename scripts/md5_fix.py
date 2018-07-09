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

rospy.init_node('md5_fix')

dirPath = rospy.get_param('~directory_path','/home/parallels/Desktop/uwb_path_6_6_18')
inpBagName = rospy.get_param('~input_bag','village_no_wire_3.bag')
outBagName = rospy.get_param('~output_bag','md5/village_no_wire_3.bag')

def fixBagfile(inputBagfile,outputBagfile):

    rawTopic1 = '/novatel_rear/rawMeasurementsTagged'
    rawTopic2 = '/novatel_front/rawMeasurementsTagged'
    rawTopic3 = '/novatel_base/rawMeasurementsTagged'
    ephemTopic1 = '/novatel_rear/gpsEphemerisTagged'
    ephemTopic2 = '/novatel_front/gpsEphemerisTagged'
    ephemTopic3 = '/novatel_base/gpsEphemerisTagged'
    drtkTopic = '/drtk_node/drtkOutput'

    t_init = 0.0
    t_final = 0.0

    with rosbag.Bag(outputBagfile, 'w') as outbag: # open output bagfile for writing

        for topic, msg, t in rosbag.Bag(inputBagfile).read_messages(): # loop through all messages in bagfile

            # print topic

            if (topic == rawTopic1) or (topic == rawTopic2) or (topic == rawTopic3):

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
            
            elif (topic == ephemTopic1) or (topic == ephemTopic2) or (topic == ephemTopic3):

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

def getFullPath(dirPath,bagfileName):
    # Fix directory path
    end = len(dirPath) - 1
    if dirPath[end] is not '/':
        dirPath = dirPath + '/'

    # Fix bagfile name
    end = len(bagfileName) - 1
    if bagfileName[(end-3):(end+1)] != '.bag':
        bagfileName = bagfileName + '.bag'

    return dirPath + bagfileName

def main(args):

    if (len(args)>1):
        inpBag = args[1]
        outBag = args[2]
    else:
        inpBag = getFullPath(dirPath,inpBagName)
        outBag = getFullPath(dirPath,outBagName)

    print 'input bagfile: ' + inpBag
    print 'output bagfile: ' + outBag

    fixBagfile(inpBag,outBag)

if __name__ == '__main__':
  main(sys.argv)