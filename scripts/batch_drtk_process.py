#!/usr/bin/env python
"""""""""""""""""""""""""""""""""
Author: Dan Pierce
Date: 2018.01.28
"""""""""""""""""""""""""""""""""
import rospy
import os
import sys

import time



commonPath = '/media/psf/Home/Google Drive/GAVLAB/data/mkz'
commonPath2 = '/media/psf/Home/Google\ Drive/GAVLAB/data/mkz'

directories = ['dual_antenna_1_15_18','path_duplication_1_13_18','track_rtk_laps_1_13_18']



for directory in directories:
  print 'directory: ' + directory
  fullPath = commonPath + '/' + directory + '/md5_fix'
  files = os.listdir(fullPath)
  fullPath = commonPath2 + '/' + directory + '/md5_fix'
  for f in files:
    if (len(f)>3):
      end = len(f) - 1
      if f[(end-3):(end+1)] == '.bag':
        f2 = f[0:(end-3)]

        if (f[0:3] != 'base'):

          osCmd = 'roslaunch path_duplication_launch drtk_playback.launch bagpath:=\'' + fullPath + '\' filename:=\'' + f2 + '\''

          os.system(osCmd)

          print 'Done processing ' + f





# commonPath = '/media/psf/Home/Google Drive/GAVLAB/data/mkz'

# directories = ['dual_antenna_1_15_18','path_duplication_1_13_18','track_rtk_laps_1_13_18']


# for directory in directories:
#   print 'directory: ' + directory
#   fullPath = commonPath + '/' + directory
#   files = os.listdir(fullPath)
#   for f in files:
#     if (len(f)>3):
#       end = len(f) - 1
#       if f[(end-3):(end+1)] == '.bag':

#         inputBagfile = fullPath + '/' + f
#         outputBagfile = fullPath + '/' + 'z_md5_fix_' + f
#         fixBagfile(inputBagfile,outputBagfile)
#         print '\tfinished processing ' + f
#   print '\n'




















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

