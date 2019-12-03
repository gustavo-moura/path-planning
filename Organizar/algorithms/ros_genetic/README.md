# Genetic Algorithm ROS Service Node

#### References
The following references were used to build this ROS node:

http://wiki.ros.org/ROS/Tutorials/CreatingMsgAndSrv#Creating_a_srv
http://wiki.ros.org/ROS/Tutorials/WritingServiceClient%28python%29

## TODO

There's one more step, though. We need to make sure that the srv files are turned into source code for C++, Python, and other languages.


Unless you have done so already, open package.xml, and make sure these two lines are in it and uncommented:
```
  <build_depend>message_generation</build_depend>
  <exec_depend>message_runtime</exec_depend>
```
As before, note that at build time, we need "message_generation", while at runtime, we only need "message_runtime".

Unless you have done so already for messages in the previous step, add the message_generation dependency to generate messages in CMakeLists.txt:

```
# Do not just add this line to your CMakeLists.txt, modify the existing line
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)
```
(Despite its name, message_generation works for both msg and srv.)

Also you need the same changes to package.xml for services as for messages, so look above for the additional dependencies required.

Remove # to uncomment the following lines:

```
# add_service_files(
#   FILES
#   Genetic.srv
# )
```

