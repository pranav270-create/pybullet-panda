# Minimal working example of grasping a box

import numpy as np
import time
import matplotlib.pyplot as plt

from panda_env import PandaEnv, plot_frame_pb
import pybullet as p

# Connect to PyBullet in GUI
p.connect(p.GUI, options="--width=2600 --height=1800")
p.resetDebugVisualizerCamera(0.8, 135, -30, [0.5, 0, 0])

# Initialize Panda environment
env = PandaEnv(
    mu=0.4,  # tangential friction coefficient
    sigma=0.03,  # torsional friction coefficient
    long_finger=False,
    wide_finger=False)
env.reset_env()


# Move to above the box - right now the position is for the end-effector (ee), which is defined at the joint between the arm and the gripper (see the image at the end this page https://frankaemika.github.io/docs/control_parameters.html).
env.move_pos(
    [0.7, 0.02, 0.20],
    absolute_global_euler=[np.pi / 2, np.pi,
                           0],  # usse yaw-pitch-roll; see utils_geom.py
    numSteps=300)
time.sleep(1)

# Show end-effector frame - You can also get pose of fingers etc. using helper functions in panda_env.
ee_pos, ee_orn = env.get_ee()
plot_frame_pb(ee_pos, ee_orn)
time.sleep(1)

# Get camera image at wrist camera
rgb, depth = env.get_wrist_camera_image(
    offset=[0.04, 0.1, 0.04],  # from ee
    img_H=320,
    img_W=320,
    camera_fov=90,
    camera_aspect=1)
f, axarr = plt.subplots(1, 2)
axarr[0].imshow(rgb)
axarr[1].imshow(depth, cmap='gray')
#plt.show()

# Move down
env.move_pos([0.7, 0.02, 0.15],
             absolute_global_euler=[np.pi / 2, np.pi, 0],
             numSteps=300)
time.sleep(1)

# Grasp - this only sets the gripper velocity, no simulation step; thus need to call move_pos again to the same position to allow finger closing
env.grasp(targetVel=-0.10)
env.move_pos([0.7, 0.02, 0.13],
             absolute_global_euler=[np.pi / 2, np.pi, 0],
             numSteps=100)
time.sleep(1)

# Lift
env.move_pos([0.7, 0.02, 0.20],
             absolute_global_euler=[np.pi / 2, np.pi, 0],
             numSteps=300)
time.sleep(1)