设置串口别名：
sudo cp sc_mini.rules /etc/udev/rules.d


ROS1运行步骤：
1.catkin_make

2.roslaunch cspc_lidar start.launch

3.roslaunch cspc_lidar rviz.launch

非ROS版本包：
当前文件夹下sdk目录，可以独立作为非ROS版本包，具体使用情况参考sdk目录下的readme.txt文件

