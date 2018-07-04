#!/usr/bin/env python
"""""""""""""""""""""""""""""""""
Author: Dan Pierce
Date: 2018.01.28

This script is used to fix the jumps in novatel timing that are due to serial buffering with 
the old propak models. 

Note: This assumes that there are no GPS outages in the whole data set.

"""""""""""""""""""""""""""""""""
import rospy
import os
import sys
import rosbag
import numpy as np
from nav_msgs.msg import Odometry

def fixTime(time):
    y = time.T
    k = np.array([range(time.shape[1])]).T
    G = np.append(k,k*0.0+1.0,axis=1)
    pinvG = np.linalg.pinv(G)
    theta = pinvG.dot(y)
    yhat = theta[0,0]*k + theta[1,0]
    timeSmoothed = yhat[:,0]
    return timeSmoothed.tolist()

def fixBagfile(inputBagfile,outputBagfile):

    gpsOdomTopic = '/novatel_rear/odom'

    " Get the original time vector "
    theBag = rosbag.Bag(inputBagfile)
    N = theBag.get_message_count(gpsOdomTopic) # number of measurement samples
    
    i = 0
    time = np.zeros((1,N))
    for topic, msg, t in theBag.read_messages(topics=gpsOdomTopic): # loop through all messages in bagfile
        time[0,i] = msg.header.stamp.to_sec()
        i+=1

    " Fix the time vector "
    tFix = fixTime(time)

    print 'number of GPS odom messages: ', N

    i=0
    with rosbag.Bag(outputBagfile, 'w') as outbag: # open output bagfile for writing
        for topic, msg, t in theBag.read_messages(): # loop through all messages in bagfile
            if (topic == gpsOdomTopic):
                outMsg = msg
                outMsg.header.stamp = rospy.Time.from_sec(tFix[i])

                outbag.write(topic, outMsg, t=outMsg.header.stamp)

                i += 1

            elif (topic!='/rosout') and (topic!='/can_bus_dbw/can_rx') and (topic!='/can_bus_dbw/can_tx'):            
                outbag.write(topic, msg, t=t)

def main(args):

    inpBag = args[1]


    outBag = args[1][0:-4] + '_gpsRosTimeFix.bag'

    # outBag

    print 'input bagfile: ' + inpBag
    print 'output bagfile: ' + outBag

    fixBagfile(inpBag,outBag)

if __name__ == '__main__':
  main(sys.argv)