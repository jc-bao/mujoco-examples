"""
Example of how bodies interact with each other. For a body to be able to
move it needs to have joints. In this example, the "robot" is a red ball
with X and Y slide joints (and a Z slide joint that isn't controlled).
On the floor, there's a cylinder with X and Y slide joints, so it can
be pushed around with the robot. There's also a box without joints. Since
the box doesn't have joints, it's fixed and can't be pushed around.
"""
from mujoco_py import load_model_from_xml, MjSim, MjViewer
import math
import os

MODEL_XML = """
<?xml version="1.0" ?>
<mujoco>
	<option timestep="0.005" />
	<worldbody>
		<body name="box" pos="0 0 0.2">
			<geom name="box" mass="0.1" size="0.15 0.15 0.15" type="box"/>
			<joint axis="1 0 0" name="slidex" type="slide"/>
			<joint axis="0 1 0" name="slidey" type="slide"/>
			<joint axis="0 0 1" name="slidez" type="slide"/>
		</body>
		<body name="floor" pos="0 0 0.025">
			<geom name="floor" condim="3" size="3.0 3.0 0.02" rgba="0 1 0 1" type="box"/>
		</body>
	</worldbody>
	<actuator>
		<motor gear="1.0" joint="slidex"/>
		<motor gear="1.0" joint="slidey"/>
	</actuator>
</mujoco>
"""

model = load_model_from_xml(MODEL_XML)
sim = MjSim(model)
viewer = MjViewer(sim)
sim.reset()
t = 0
box_id = sim.model.geom_name2id('box')
floor_id = sim.model.geom_name2id('floor')
while True:
	sim.data.ctrl[0] = math.cos(t / 100.) * 1.5
	t += 1
	sim.step()
	for data in sim.data.contact:
		if (data.geom1 == floor_id and data.geom2 == box_id) or (data.geom1 == box_id and data.geom2 == floor_id):
			print(data.frame)
	viewer.render()
	if t > 100 and os.getenv('TESTING') is not None:
		break
