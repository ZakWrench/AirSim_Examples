import airsim
import time
import math

# Connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()

# Set the timeout value for each command
client.timeout = 100

# Set the drone's initial position and orientation
client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(0, 0, -10), airsim.to_quaternion(0, 0, 0)), True)

# Wait for the drone to stabilize at the initial position
time.sleep(1)

# Take off to an altitude of 10 meters above ground
client.takeoffAsync().join()
client.hoverAsync().join()

# Move in a circular motion with a radius of 5 meters for 10 seconds
center = airsim.Vector3r(0, 0, -10)
radius = 5
speed = 10 # degrees per second
start_time = time.time()

while time.time() - start_time < 10:
    angle_degrees = (time.time() - start_time) * speed
    angle_radians = math.radians(angle_degrees)
    x = center.x_val + radius * math.cos(angle_radians)
    y = center.y_val + radius * math.sin(angle_radians)
    z = center.z_val
    client.moveToPositionAsync(x, y, z, 3).join()

# Perform a full pitch (flip from the back)
client.rotateToYawPitchRollAsync(0, -90, 0, 1).join()

# Perform another full flip but from the front
client.rotateToYawPitchRollAsync(0, 90, 0, 1).join()

# Maintain original position above
client.hoverAsync().join()

# Go down 5 meters
client.moveToZAsync(-15, 3).join()

# Perform both a full roll and a full pitch at the same time
client.rotateToYawPitchRollAsync(90, -90, 90, 1).join()

# Go back to the initial position
client.moveToPositionAsync(0, 0, -10, 3).join()

# Land safely
client.landAsync().join()
