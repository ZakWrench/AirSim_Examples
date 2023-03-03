#APi for communicating with AirSim Sim
import airsim
import math

# connect to the AirSim simulator

#Create a new instance of the "MultirotorClient" class, used to communicate with airsim simulator.
client = airsim.MultirotorClient()

#Establish Connection with sim
client.confirmConnection()

# Tell the drone to take off and then waits for the command to complete before moving on to the next line
client.takeoffAsync().join()
# Tell the drone to hover at a specified altitude(5 meters) and wait for the commend to complete before moving on to the next line
client.hoverAsync(z=5).join()

# Rotate to a yaw angle of 180 degrees(full yaw)
client.rotateToYawAsync(180).join()
# Rotate to a pitch angle of -30 degrees(full pitch)
client.rotateToPitchAsync(-30).join()
# Rotate to a roll angle of 30 degrees(full roll)
client.rotateToRollAsync(30).join()

# perform a quarter yaw, with a degree of 30
client.rotateToYawAsync(225).join()

#Get the current pose of drone
current_pose = client.simGetVehiclePose()

#Define the roll angle and duration of the maneuvre (varial roll)
roll_angle_deg = 45.0
maneuver_duration = 5.0

#convert roll angle to radians
roll_angle_rad = math_radians(roll_angle_deg)

# Calculate the target orientation quaterion
init_quat = current_pose.orentiation
target_quat = airsim.to_quaternion(roll_angle_rad, 0, 0)

#perform the roll maneuvre
client.rotateToOrientationAsync(target_quat, maneuver_duration).join()

#maintain the drone's initial position
client.moveToPositionAsync(current_pose.position.x_val, current_pose.position.y_val, current_pose.position.z_val, 2.0).join()
client.rotateToOrientationAsync(init_quat, 2.0).join()

# land the drone
client.landAsync().join()
