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


from md5_fix import fixBagfile


commonPath = '/media/psf/Home/Google Drive/GAVLAB/data/mkz'

directories = ['dual_antenna_1_15_18','path_duplication_1_13_18','track_rtk_laps_1_13_18']


for directory in directories:
  print 'directory: ' + directory
  fullPath = commonPath + '/' + directory
  files = os.listdir(fullPath)
  for f in files:
    if (len(f)>3):
      end = len(f) - 1
      if f[(end-3):(end+1)] == '.bag':

        inputBagfile = fullPath + '/' + f
        outputBagfile = fullPath + '/' + 'z_md5_fix_' + f
        fixBagfile(inputBagfile,outputBagfile)
        print '\tfinished processing ' + f
  print '\n'




















# cnt = 0
#     for ch in inputBagfile:
#         if ch == '/':
#             idx = cnt+1
#         cnt += 1

#     outputBagfilePath = inputBagfile[0:idx]

#     outputBagfile = 'md5_fix_' + inputBagfile[idx:len(inputBagfile)]

    

#      os. listdir(path)

# test12('/media/psf/Home/Google Drive/GAVLAB/data/mkz/path_duplication_1_13_18/path_duplication_2018-01-13-18-35-49.bag')

# $(rospack find path_duplication_launch)/scripts/fix_bagfile_md5.py '/media/psf/Home/Google Drive/GAVLAB/data/mkz/path_duplication_1_13_18/path_duplication_2018-01-13-18-35-49.bag'

