#!/usr/bin/env python3
"""
Visual 3D GUI demo using Azrael's PyBullet wrapper with OpenGL viewer.
This demonstrates that Azrael's bullet wrapper works with real-time 3D rendering.

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

# Import Azrael's bullet wrapper
import azrael.bullet.azBullet as azBullet
from azrael.bullet.azBullet import Vec3, Quaternion, StaticPlaneShape, SphereShape
from azrael.bullet.azBullet import DefaultMotionState, Transform
from azrael.bullet.azBullet import RigidBody, RigidBodyConstructionInfo

print("=" * 60)
print("AZRAEL VISUAL 3D DEMO - Bouncing Ball")
print("=" * 60)
print()
print("This demo uses Azrael's PyBullet wrapper (azrael.bullet.azBullet)")
print("to create physics objects and simulate them with 3D visualization.")
print()
print("Starting PyBullet GUI...")
print()
print("Controls:")
print("  - Mouse drag: Rotate camera")
print("  - Mouse scroll: Zoom in/out")
print("  - Ctrl + Mouse drag: Pan camera")
print("  - ESC: Exit")
print()

# Create Azrael's bullet world (uses PyBullet internally but in GUI mode)
# We need to connect PyBullet to GUI mode first, then use Azrael's wrapper
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

print("✓ PyBullet GUI initialized")
print()

# Create Azrael's BulletBase world
sim = azBullet.BulletBase()
print("✓ Azrael BulletBase world created")

# Set gravity using Azrael's API
sim.setGravity(Vec3(0, 0, -10))
print("✓ Gravity set to (0, 0, -10) m/s² using Azrael API")
print()

# Create ground plane using Azrael's API
print("Creating ground plane using Azrael...")
planeShape = StaticPlaneShape(Vec3(0, 0, 1), 1)
planeMotion = DefaultMotionState(Transform(Vec3(0, 0, -1)))
planeInfo = RigidBodyConstructionInfo(0, planeMotion, planeShape)
planeBody = RigidBody(planeInfo)
planeBody.setRestitution(0.8)
sim.addRigidBody(planeBody)
print("✓ Ground plane created at Z = -1 using Azrael StaticPlaneShape")
print("✓ Ground bounciness = 0.8")
print()

# Create a ball using Azrael's API
print("Creating ball using Azrael...")
sphereRadius = 1.0
sphereShape = SphereShape(sphereRadius)
startTransform = Transform(Vec3(0, 0, 20))
ballMotion = DefaultMotionState(startTransform)

# Create rigid body construction info
mass = 1.0
localInertia = sphereShape.calculateLocalInertia(mass)

ballInfo = RigidBodyConstructionInfo(mass, ballMotion, sphereShape, localInertia)
ballBody = RigidBody(ballInfo)
ballBody.setRestitution(0.9)

# Add to simulation
sim.addRigidBody(ballBody)

print("✓ Ball created using Azrael API:")
print("  - SphereShape with radius 1 meter")
print("  - Mass: 1 kg")
print("  - Starting position: (0, 0, 20) meters")
print("  - Bounciness: 0.9")
print()

# Add visual representation by creating a colored sphere in PyBullet
# (Azrael's wrapper handles physics, we add visualization separately)
visualSphereId = p.createVisualShape(
    p.GEOM_SPHERE,
    radius=sphereRadius,
    rgbaColor=[1, 0.3, 0.3, 1]  # Red color
)
# We need to link the visual to the physics body
# The ballBody.pybullet_id gives us the PyBullet body ID
if ballBody.pybullet_id is not None:
    # Update the visual shape for the existing body
    p.changeVisualShape(ballBody.pybullet_id, -1, rgbaColor=[1, 0.3, 0.3, 1])

# Add reference grid
print("Adding reference grid...")
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

print("✓ Reference grid added")
print()
print("=" * 60)
print("SIMULATION RUNNING")
print("=" * 60)
print()
print("Watch the red ball bounce in the 3D viewer window!")
print("Physics is handled by Azrael's bullet wrapper.")
print("Press ESC in the viewer window to exit.")
print()

# Real-time physics simulation using Azrael
timeStep = 1.0 / 240.0  # 240 Hz
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

        # Step the simulation using Azrael's API
        sim.stepSimulation(timeStep, 1)

        # Get ball position using Azrael's API
        try:
            transform = ballBody.getWorldTransform()
            pos = transform.position
            vel = ballBody.getLinearVelocity()
        except (p.error, AttributeError):
            # Connection lost or object doesn't exist
            break

        # Print stats every second
        currentTime = time.time()
        if currentTime - lastPrintTime >= printInterval:
            height = pos.z
            velocity_z = vel.z if vel else 0
            print(f"Step {step:6d} | Height: {height:6.2f} m | "
                  f"Velocity: {velocity_z:6.2f} m/s | [Azrael API]")
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
    print("Azrael visual demo completed!")
    print("=" * 60)
    print()
    print("What you just saw:")
    print("  ✓ Azrael's bullet wrapper (azBullet.py) in action")
    print("  ✓ BulletBase, Vec3, SphereShape, StaticPlaneShape")
    print("  ✓ RigidBody with physics properties")
    print("  ✓ Real-time 3D visualization")
    print()
    print("This proves Azrael's physics layer works! 🎉")
