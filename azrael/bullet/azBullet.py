"""
Minimal PyBullet wrapper to replace the custom Cython azBullet bindings.

This provides a compatibility layer so the existing code can work with PyBullet
instead of the custom compiled Bullet bindings.
"""
import pybullet as p
import numpy as np


class Vec3:
    """3D Vector wrapper."""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.value = (x, y, z)

    def __iter__(self):
        return iter([self.x, self.y, self.z])

    def __getitem__(self, idx):
        return [self.x, self.y, self.z][idx]

    def __str__(self):
        return f"Vec3({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"

    def __repr__(self):
        return str(self)


class Quaternion:
    """Quaternion wrapper."""
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.value = (x, y, z, w)

    def __iter__(self):
        return iter([self.x, self.y, self.z, self.w])

    def __getitem__(self, idx):
        return [self.x, self.y, self.z, self.w][idx]


class Transform:
    """Transform (position + orientation) wrapper."""
    def __init__(self, orientation=None, position=None):
        # Note: accepts either (orientation, position) or (position, orientation)
        # or single argument (checks type)
        if orientation is not None and isinstance(orientation, Vec3):
            # Called as Transform(position) or Transform(position, orientation)
            position, orientation = orientation, position

        if position is None:
            position = Vec3(0, 0, 0)
        if orientation is None:
            orientation = Quaternion(0, 0, 0, 1)
        self.position = position
        self.orientation = orientation

    def setOrigin(self, vec3):
        self.position = vec3

    def setRotation(self, quat):
        self.orientation = quat

    def getOrigin(self):
        return self.position

    def getRotation(self):
        return self.orientation


class RigidBodyConstructionInfo:
    """Construction info for rigid bodies."""
    def __init__(self, mass, motionState, collisionShape, localInertia=None):
        self.mass = mass
        self.motionState = motionState
        self.collisionShape = collisionShape
        self.localInertia = localInertia if localInertia else Vec3(0, 0, 0)


class MotionState:
    """Motion state for rigid bodies."""
    def __init__(self, transform=None):
        self.transform = transform if transform else Transform()

    def getWorldTransform(self):
        return self.transform

    def setWorldTransform(self, transform):
        self.transform = transform


class CollisionShape:
    """Base collision shape."""
    def __init__(self):
        self.pybullet_shape_id = None

    def calculateLocalInertia(self, mass):
        # PyBullet handles inertia automatically
        return Vec3(0, 0, 0)


class SphereShape(CollisionShape):
    """Sphere collision shape."""
    def __init__(self, radius):
        super().__init__()
        self.radius = radius
        self.pybullet_shape_id = p.createCollisionShape(p.GEOM_SPHERE, radius=radius)


class BoxShape(CollisionShape):
    """Box collision shape."""
    def __init__(self, halfExtents):
        super().__init__()
        self.halfExtents = halfExtents
        # PyBullet expects half extents directly
        he = [halfExtents.x, halfExtents.y, halfExtents.z]
        self.pybullet_shape_id = p.createCollisionShape(p.GEOM_BOX, halfExtents=he)


class PlaneShape(CollisionShape):
    """Plane collision shape."""
    def __init__(self, normal, constant):
        super().__init__()
        self.normal = normal
        self.constant = constant
        # PyBullet plane needs normal and offset
        n = [normal.x, normal.y, normal.z]
        self.pybullet_shape_id = p.createCollisionShape(
            p.GEOM_PLANE,
            planeNormal=n
        )


class StaticPlaneShape(PlaneShape):
    """Static plane shape (alias for PlaneShape)."""
    pass


class DefaultMotionState(MotionState):
    """Default motion state (alias for MotionState)."""
    pass


class RigidBody:
    """Rigid body wrapper around PyBullet."""
    def __init__(self, constructionInfo, bodyID=None):
        self.bodyID = bodyID if bodyID is not None else id(self)
        self.constructionInfo = constructionInfo
        self.pybullet_id = None
        self._world = None
        self._motionState = constructionInfo.motionState

    def setLinearVelocity(self, velocity):
        if self.pybullet_id is not None:
            p.resetBaseVelocity(self.pybullet_id,
                               linearVelocity=[velocity.x, velocity.y, velocity.z])

    def setAngularVelocity(self, velocity):
        if self.pybullet_id is not None:
            p.resetBaseVelocity(self.pybullet_id,
                               angularVelocity=[velocity.x, velocity.y, velocity.z])

    def getLinearVelocity(self):
        if self.pybullet_id is not None:
            vel, _ = p.getBaseVelocity(self.pybullet_id)
            return Vec3(*vel)
        return Vec3(0, 0, 0)

    def getAngularVelocity(self):
        if self.pybullet_id is not None:
            _, vel = p.getBaseVelocity(self.pybullet_id)
            return Vec3(*vel)
        return Vec3(0, 0, 0)

    def applyCentralForce(self, force):
        if self.pybullet_id is not None:
            p.applyExternalForce(self.pybullet_id, -1,
                                [force.x, force.y, force.z],
                                [0, 0, 0], p.WORLD_FRAME)

    def applyTorque(self, torque):
        if self.pybullet_id is not None:
            p.applyExternalTorque(self.pybullet_id, -1,
                                 [torque.x, torque.y, torque.z],
                                 p.WORLD_FRAME)

    def setWorldTransform(self, transform):
        if self.pybullet_id is not None:
            pos = [transform.position.x, transform.position.y, transform.position.z]
            orn = [transform.orientation.x, transform.orientation.y,
                   transform.orientation.z, transform.orientation.w]
            p.resetBasePositionAndOrientation(self.pybullet_id, pos, orn)

    def getWorldTransform(self):
        if self.pybullet_id is not None:
            pos, orn = p.getBasePositionAndOrientation(self.pybullet_id)
            transform = Transform()
            transform.position = Vec3(*pos)
            transform.orientation = Quaternion(*orn)
            # Update motion state
            self._motionState.setWorldTransform(transform)
            return transform
        return Transform()

    def getMotionState(self):
        """Get the motion state."""
        # Update it with current position
        if self.pybullet_id is not None:
            pos, orn = p.getBasePositionAndOrientation(self.pybullet_id)
            transform = Transform()
            transform.position = Vec3(*pos)
            transform.orientation = Quaternion(*orn)
            self._motionState.setWorldTransform(transform)
        return self._motionState

    def forceActivationState(self, state):
        # PyBullet doesn't need this - bodies are always active when forces applied
        pass

    def setDamping(self, linear, angular):
        if self.pybullet_id is not None:
            p.changeDynamics(self.pybullet_id, -1,
                           linearDamping=linear,
                           angularDamping=angular)

    def setFriction(self, friction):
        if self.pybullet_id is not None:
            p.changeDynamics(self.pybullet_id, -1, lateralFriction=friction)

    def setRestitution(self, restitution):
        if self.pybullet_id is not None:
            p.changeDynamics(self.pybullet_id, -1, restitution=restitution)


class BulletBase:
    """Main PyBullet world wrapper."""
    def __init__(self):
        # Connect in DIRECT mode (no GUI)
        self.physicsClient = p.connect(p.DIRECT)
        p.setGravity(0, 0, 0)
        self.bodies = {}
        self.body_id_map = {}  # Map Azrael IDs to PyBullet IDs

    def setGravity(self, gravity):
        p.setGravity(gravity.x, gravity.y, gravity.z)

    def addRigidBody(self, rigidBody):
        """Add a rigid body to the simulation."""
        if rigidBody.pybullet_id is not None:
            # Already added
            return

        ci = rigidBody.constructionInfo
        ms = ci.motionState
        shape = ci.collisionShape

        # Get initial transform
        transform = ms.getWorldTransform()
        pos = [transform.position.x, transform.position.y, transform.position.z]
        orn = [transform.orientation.x, transform.orientation.y,
               transform.orientation.z, transform.orientation.w]

        # Create the body in PyBullet
        if shape.pybullet_shape_id is not None:
            body_id = p.createMultiBody(
                baseMass=ci.mass,
                baseCollisionShapeIndex=shape.pybullet_shape_id,
                basePosition=pos,
                baseOrientation=orn
            )

            rigidBody.pybullet_id = body_id
            rigidBody._world = self
            self.bodies[rigidBody.bodyID] = rigidBody
            self.body_id_map[rigidBody.bodyID] = body_id

    def removeRigidBody(self, rigidBody):
        """Remove a rigid body from the simulation."""
        if rigidBody.pybullet_id is not None:
            p.removeBody(rigidBody.pybullet_id)
            if rigidBody.bodyID in self.bodies:
                del self.bodies[rigidBody.bodyID]
            if rigidBody.bodyID in self.body_id_map:
                del self.body_id_map[rigidBody.bodyID]
            rigidBody.pybullet_id = None

    def stepSimulation(self, timeStep=1./240., maxSubSteps=1):
        """Step the simulation forward."""
        # PyBullet's stepSimulation takes no arguments and uses fixed timestep
        for _ in range(maxSubSteps):
            p.stepSimulation()

    def azGetNarrowphaseContacts(self):
        """Get collision contacts (Azrael-specific method)."""
        contacts = []

        # Get all contact points
        for bodyA_id in self.body_id_map.values():
            contact_points = p.getContactPoints(bodyA_id)
            for cp in contact_points:
                # cp is a tuple with contact information
                # Find the Azrael IDs
                aid_a = None
                aid_b = None

                for azrael_id, pybullet_id in self.body_id_map.items():
                    if pybullet_id == cp[1]:  # bodyA
                        aid_a = azrael_id
                    if pybullet_id == cp[2]:  # bodyB
                        aid_b = azrael_id

                if aid_a is not None and aid_b is not None:
                    # cp[5] is contact position on A, cp[6] is position on B
                    contacts.append({
                        'aid_a': aid_a,
                        'aid_b': aid_b,
                        'point_a': cp[5],
                        'point_b': cp[6]
                    })

        return contacts

    def __del__(self):
        """Clean up PyBullet connection."""
        try:
            p.disconnect(self.physicsClient)
        except:
            pass
