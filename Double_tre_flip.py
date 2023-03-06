import airsim
import math

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()

# get the initial pose of the drone
init_pose = client.simGetVehiclePose()

# define the roll, pitch, and yaw angles and durations of the maneuver
roll_angle_deg = 720.0
pitch_angle_deg = 540.0
yaw_angle_deg = 360.0
maneuver_duration = 10.0

# convert angles to radians
roll_angle_rad = math.radians(roll_angle_deg)
pitch_angle_rad = math.radians(pitch_angle_deg)
yaw_angle_rad = math.radians(yaw_angle_deg)

# calculate the target orientation quaternions
init_quat = init_pose.orientation
target_quat1 = airsim.to_quaternion(roll_angle_rad, pitch_angle_rad, init_pose.orientation.yaw_val)
target_quat2 = airsim.to_quaternion(2*roll_angle_rad, pitch_angle_rad, init_pose.orientation.yaw_val + yaw_angle_rad)

# perform the double tre flip maneuver
client.rotateToOrientationAsync(target_quat1, maneuver_duration/2).join()
client.rotateToOrientationAsync(target_quat2, maneuver_duration/2).join()

# maintain the drone's initial position
client.moveToPositionAsync(init_pose.position.x_val, init_pose.position.y_val, init_pose.position.z_val, 2.0).join()
client.rotateToOrientationAsync(init_quat, 2.0).join()
