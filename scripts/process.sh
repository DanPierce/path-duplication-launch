#!/bin/bash

# DIRPATH='/media/psf/Home/Google Drive/GAVLAB/data/mkz/path_duplication_1_13_18'

# "$(DIRPATH)"

# foo=$bar
# bar=$(a command)
# logfile=$logdir/foo-$(date +%Y%m%d)

# roslaunch path_duplication_launch drtk_for_pd_truth.launch setId:=1
roslaunch path_duplication_launch drtk_for_pd_truth.launch setId:=4
roslaunch path_duplication_launch drtk_for_pd_truth.launch setId:=3
roslaunch path_duplication_launch drtk_for_pd_truth.launch setId:=2

