#include "node_lidar_ros.h"
#include "calibration.h"
#include "node_lidar.h"

int main(int argc, char **argv)
{
    ros::init(argc, argv, "cspc_lidar");
	ros::NodeHandle n;
	ros::NodeHandle priv_nh("~");

    priv_nh.param("baud_rate", node_lidar.lidar_general_info.m_SerialBaudrate, 115200);
	priv_nh.param("frame_id", node_lidar.lidar_general_info.frame_id, std::string("base_link"));
	priv_nh.param("port", node_lidar.lidar_general_info.port, std::string("/dev/sc_mini"));
	priv_nh.param("version", node_lidar.lidar_general_info.version, 2);
	priv_nh.param("calib", node_lidar.data_calibration, false);
	priv_nh.param("rangemax", node_lidar.range_max, 10000.0f);

    calibration_params.origin_point.x = node_lidar.range_max;
	calibration_params.origin_point.y = node_lidar.range_max;

	priv_nh.param("dpd", calibration_params.distortion_processing_distance, 1000.0f);
	priv_nh.param("calib_type", calibration_params.calibration_type, 0);
	priv_nh.param("ljpn", calibration_params.line_judgment_point_num, 15);

    ros::Publisher laser_pub = n.advertise<sensor_msgs::LaserScan>("scan", 1);

	node_start();

	while(ros::ok())
	{
		LaserScan scan;
		if(data_handling(scan))
		{
			sensor_msgs::LaserScan scan_pub;
			scan_pub.ranges.resize(scan.points.size());
			scan_pub.intensities.resize(scan.points.size());
			scan_pub.angle_increment = (2.0*M_PI/scan.points.size());
			scan_pub.angle_min = 0;
			scan_pub.angle_max = 2*M_PI;
			scan_pub.range_min = 0.10;
			scan_pub.range_max = 10.0; //测量的最远距离是10m
			scan_pub.header.frame_id = node_lidar.lidar_general_info.frame_id;
			scan_pub.header.stamp = ros::Time::now();
			for(int i=0; i < scan.points.size(); i++) {
				scan_pub.ranges[i] = scan.points[i].range;
				scan_pub.intensities[i] = scan.points[i].intensity;
			}
			laser_pub.publish(scan_pub);
			
      	}
	}
}