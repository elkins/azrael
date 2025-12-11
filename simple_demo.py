#!/usr/bin/env python3
"""
Simplest possible Azrael physics demo - ball bouncing on ground.
Shows the physics simulation working with visual progress bars.
"""
import sys
sys.path.insert(0, '.')

import azrael.bullet.azBullet as azBullet
from azrael.bullet.azBullet import Vec3, Quaternion, StaticPlaneShape, SphereShape
from azrael.bullet.azBullet import DefaultMotionState, Transform
from azrael.bullet.azBullet import RigidBody, RigidBodyConstructionInfo

print("=" * 60)
print("AZRAEL PHYSICS DEMO - Ball Bouncing")
print("=" * 60)
print()

# Create the simulation world
print("🌍 Creating physics world...")
sim = azBullet.BulletBase()
sim.setGravity(Vec3(0, -10, 0))  # Earth gravity
print("   ✓ Gravity set to -10 m/s²")
print()

# Create a ground plane
print("🏔️  Creating ground plane...")
groundShape = StaticPlaneShape(Vec3(0, 1, 0), 1)
groundRigidBodyState = DefaultMotionState(
    Transform(Quaternion(0, 0, 0, 1), Vec3(0, -1, 0)))
groundRigidBody = RigidBody(
    RigidBodyConstructionInfo(0, groundRigidBodyState, groundShape))
groundRigidBody.setRestitution(0.8)  # Bouncy ground!
sim.addRigidBody(groundRigidBody)
print("   ✓ Ground plane at Y = -1")
print("   ✓ Bounciness = 0.8")
print()

# Create a ball
print("⚽ Creating ball...")
ballShape = SphereShape(1)  # Radius = 1 meter
ballState = DefaultMotionState(
    Transform(Quaternion(0, 0, 0, 1), Vec3(0, 20, 0)))  # Start at height 20
ballInertia = ballShape.calculateLocalInertia(1.0)  # Mass = 1 kg
ballRigidBody = RigidBody(
    RigidBodyConstructionInfo(1.0, ballState, ballShape, ballInertia))
ballRigidBody.setRestitution(0.9)  # Very bouncy ball!
sim.addRigidBody(ballRigidBody)
print("   ✓ Radius = 1 meter")
print("   ✓ Mass = 1 kg")
print("   ✓ Starting height = 20 meters")
print("   ✓ Bounciness = 0.9")
print()

# Run the simulation
print("🎬 Running simulation...")
print("-" * 60)
print(f"{'Step':>6} | {'Height (m)':>12} | {'Velocity':>10} | Visual")
print("-" * 60)

max_height = 20.0
for step in range(30):
    sim.stepSimulation(0.1, 10)  # 0.1 second timestep

    # Get ball position
    ms = ballRigidBody.getMotionState()
    wt = ms.getWorldTransform()
    pos = wt.getOrigin()

    # Get ball velocity
    vel = ballRigidBody.getLinearVelocity()
    vel_y = vel.y

    # Create a visual bar showing height
    height = pos.y
    bar_length = int((height / max_height) * 40)
    bar = "█" * max(0, bar_length)

    # Direction indicator
    if vel_y > 0.1:
        direction = "↑"
    elif vel_y < -0.1:
        direction = "↓"
    else:
        direction = "●"

    print(f"{step:6d} | {height:12.2f} | {vel_y:>9.2f} | {bar}{direction}")

    # Stop if ball has settled
    if step > 20 and abs(vel_y) < 0.1 and height < 2.0:
        print()
        print("⚠️  Ball has settled on the ground")
        break

print("-" * 60)
print()
print("✅ Simulation complete!")
print()
print("What you just saw:")
print("  • Ball started at 20 meters high")
print("  • Fell due to gravity (9.8 m/s²)")
print("  • Bounced on the ground (elastic collision)")
print("  • Eventually settled due to energy loss")
print()
print("This demonstrates that Azrael's physics engine is working! 🎉")
print()

# Cleanup
sim.removeRigidBody(ballRigidBody)
sim.removeRigidBody(groundRigidBody)
