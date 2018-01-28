cmake_minimum_required(VERSION 2.8.3)
project(path_duplication_launch)

find_package(catkin REQUIRED COMPONENTS std_msgs message_generation)

##########################
## Declare ROS messages ##
##########################
add_message_files(
  FILES
    DualAntennaOutput.msg
)

generate_messages(
  DEPENDENCIES
    std_msgs
)

catkin_package( )

#############
## Install ##
#############

## For python scripts
install(
  DIRECTORY
    scripts
  USE_SOURCE_PERMISSIONS
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY
  launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
