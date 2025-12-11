#!/usr/bin/env python3
"""
Visual 3D GUI demo using PyBullet's OpenGL viewer.
Shows a bouncing ball with real-time 3D rendering.

Controls:
- Mouse: Rotate camera
- Scroll: Zoom in/out
- Ctrl+Mouse: Pan camera
- ESC: Exit
"""
import sys
sys.path.insert(0, '.')

import time
import pybullet as p
import pybullet_data

print("=" * 60)
print("AZRAEL VISUAL 3D DEMO - Bouncing Ball")
print("=" * 60)
print()
print("Starting PyBullet GUI...")
print()
print("Controls:")
print("  - Mouse drag: Rotate camera")
print("  - Mouse scroll: Zoom in/out")
print("  - Ctrl + Mouse drag: Pan camera")
print("  - ESC: Exit")
print()

# Connect to PyBullet with GUI
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Set up the camera view
p.resetDebugVisualizerCamera(
    cameraDistance=15,
    cameraYaw=45,
    cameraPitch=-30,
    cameraTargetPosition=[0, 0, 5]
)

# Configure the GUI
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 1)
p.configureDebugVisualizer(p.COV_ENABLE_SHADOWS, 1)

# Set gravity
p.setGravity(0, 0, -10)
print("✓ Physics world created")
print("✓ Gravity set to -10 m/s²")
print()

# Create ground plane
planeId = p.createCollisionShape(p.GEOM_PLANE)
groundId = p.createMultiBody(
    baseMass=0,
    baseCollisionShapeIndex=planeId,
    basePosition=[0, 0, -1]
)
p.changeDynamics(groundId, -1, restitution=0.8)
print("✓ Ground plane created at Z = -1")
print("✓ Ground bounciness = 0.8")
print()

# Create a colorful ball
sphereRadius = 1.0
colSphereId = p.createCollisionShape(p.GEOM_SPHERE, radius=sphereRadius)
visualSphereId = p.createVisualShape(
    p.GEOM_SPHERE,
    radius=sphereRadius,
    rgbaColor=[1, 0.3, 0.3, 1]  # Red color
)

ballId = p.createMultiBody(
    baseMass=1.0,
    baseCollisionShapeIndex=colSphereId,
    baseVisualShapeIndex=visualSphereId,
    basePosition=[0, 0, 20]
)
p.changeDynamics(ballId, -1, restitution=0.9)
print("✓ Ball created:")
print("  - Radius: 1 meter")
print("  - Mass: 1 kg")
print("  - Starting height: 20 meters")
print("  - Bounciness: 0.9")
print()

# Add some extra visual elements for reference
# Grid lines (create thin boxes)
print("✓ Adding reference grid...")
gridSize = 20
gridColor = [0.3, 0.3, 0.3, 0.5]
for i in range(-gridSize, gridSize + 1, 2):
    # Lines along X axis
    visualId = p.createVisualShape(
        p.GEOM_BOX,
        halfExtents=[gridSize, 0.01, 0.01],
        rgbaColor=gridColor
    )
    p.createMultiBody(
        baseMass=0,
        baseVisualShapeIndex=visualId,
        basePosition=[0, i, -1]
    )
    # Lines along Y axis
    visualId = p.createVisualShape(
        p.GEOM_BOX,
        halfExtents=[0.01, gridSize, 0.01],
        rgbaColor=gridColor
    )
    p.createMultiBody(
        baseMass=0,
        baseVisualShapeIndex=visualId,
        basePosition=[i, 0, -1]
    )

print()
print("=" * 60)
print("SIMULATION RUNNING")
print("=" * 60)
print()
print("Watch the red ball bounce in the 3D viewer window!")
print("Press ESC in the viewer window to exit.")
print()

# Real-time physics simulation
timeStep = 1.0 / 240.0  # 240 Hz
p.setTimeStep(timeStep)

step = 0
lastPrintTime = time.time()
printInterval = 1.0  # Print stats every second

try:
    while True:
        # Check if still connected (window not closed)
        if not p.isConnected():
            print()
            print("Viewer window closed")
            break

        # Step the simulation
        p.stepSimulation()

        # Get ball position for monitoring
        try:
            pos, orn = p.getBasePositionAndOrientation(ballId)
            vel, angVel = p.getBaseVelocity(ballId)
        except p.error:
            # Connection lost
            break

        # Print stats every second
        currentTime = time.time()
        if currentTime - lastPrintTime >= printInterval:
            height = pos[2]
            velocity_z = vel[2]
            print(f"Step {step:6d} | Height: {height:6.2f} m | "
                  f"Velocity: {velocity_z:6.2f} m/s")
            lastPrintTime = currentTime

        step += 1

        # Small sleep to avoid maxing out CPU
        time.sleep(timeStep)

except KeyboardInterrupt:
    print()
    print("Simulation stopped by user (Ctrl+C)")
finally:
    # Only disconnect if still connected
    if p.isConnected():
        p.disconnect()
    print()
    print("=" * 60)
    print("Demo completed!")
    print("=" * 60)
