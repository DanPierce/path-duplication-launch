#!/bin/bash

# DIRPATH='/media/psf/Home/Google Drive/GAVLAB/data/mkz/path_duplication_1_13_18'

# "$(DIRPATH)"

# foo=$bar
# bar=$(a command)
# logfile=$logdir/foo-$(date +%Y%m%d)


DIRPATH=/home/danpierce/

BASEBAGNAME='base_station_2018-01-13-17-31-40.bag'

rosparam set /merge_gps_bagfiles/base_station_gps_raw_topic /novatel_base/rawMeasurementsTagged
rosparam set /merge_gps_bagfiles/base_station_gps_odom_topic /novatel_base/odom
rosparam set /merge_gps_bagfiles/rover_gps_raw_topic /novatel_rear/rawMeasurementsTagged

rosparam set /merge_gps_bagfiles/directory_path $DIRPATH
rosparam set /merge_gps_bagfiles/base_station_bagfile_name $BASEBAGNAME

rosparam set /md5_fix/directory_path $DIRPATH

# --- 1
BAGFILENAME='path_duplication_1.bag'

rosparam set /merge_gps_bagfiles/rover_bagfile_name $BAGFILENAME
rosparam set /merge_gps_bagfiles/merged_bagfile_name merged_$BAGFILENAME

rosparam set /md5_fix/input_bag merged_$BAGFILENAME
# rosparam set /md5_fix/input_bag $BAGFILENAME
rosparam set /md5_fix/output_bag fixed_merged_$BAGFILENAME

# rosrun drtk merge_gps_bagfiles.py
# rosrun path_duplication_launch md5_fix.py

echo 'dont forget about ROS core!!!' | sed "s/dont/\'dont\'/"

# --- 2
BAGFILENAME='path_duplication_2.bag'

rosparam set /merge_gps_bagfiles/rover_bagfile_name $BAGFILENAME
rosparam set /merge_gps_bagfiles/merged_bagfile_name merged_$BAGFILENAME

rosparam set /md5_fix/input_bag merged_$BAGFILENAME
# rosparam set /md5_fix/input_bag $BAGFILENAME
rosparam set /md5_fix/output_bag fixed_merged_$BAGFILENAME

rosrun drtk merge_gps_bagfiles.py
rosrun path_duplication_launch md5_fix.py

# --- 3
BAGFILENAME='path_duplication_3.bag'

rosparam set /merge_gps_bagfiles/rover_bagfile_name $BAGFILENAME
rosparam set /merge_gps_bagfiles/merged_bagfile_name merged_$BAGFILENAME

rosparam set /md5_fix/input_bag merged_$BAGFILENAME
# rosparam set /md5_fix/input_bag $BAGFILENAME
rosparam set /md5_fix/output_bag fixed_merged_$BAGFILENAME

rosrun drtk merge_gps_bagfiles.py
rosrun path_duplication_launch md5_fix.py

# --- 4
BAGFILENAME='path_duplication_4.bag'

rosparam set /merge_gps_bagfiles/rover_bagfile_name $BAGFILENAME
rosparam set /merge_gps_bagfiles/merged_bagfile_name merged_$BAGFILENAME

rosparam set /md5_fix/input_bag merged_$BAGFILENAME
# rosparam set /md5_fix/input_bag $BAGFILENAME
rosparam set /md5_fix/output_bag fixed_merged_$BAGFILENAME

rosrun drtk merge_gps_bagfiles.py
rosrun path_duplication_launch md5_fix.py

