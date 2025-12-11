# Azrael Architecture

## Overview

Azrael is a distributed physics simulation engine with a stateless, network-first architecture.

```
┌──────────────────────────────────────────────────────────┐
│                        Clients                            │
│     (Python, JavaScript, any language via REST)           │
└────────────┬────────────────────────┬────────────────────┘
             │                        │
       REST/WebSocket           REST/WebSocket
             │                        │
┌────────────▼────────────────────────▼────────────────────┐
│                       Clerk (API Gateway)                 │
│  - Handles client requests                                │
│  - Validates input                                        │
│  - Routes to services                                     │
└────────────┬─────────────────────────────────────────────┘
             │
        Internal API
             │
┌────────────▼─────────────────────────────────────────────┐
│                    Leonard (Physics Manager)              │
│  - Manages Bullet physics simulation                      │
│  - Steps simulation forward                               │
│  - Handles collisions                                     │
│  - Updates object states                                  │
└────────────┬─────────────────────────────────────────────┘
             │
      State Updates
             │
┌────────────▼─────────────────────────────────────────────┐
│                MongoDB (State Database)                   │
│  - Stores object states                                   │
│  - Persists simulation data                               │
│  - Provides queries                                       │
└──────────────────────────────────────────────────────────┘

         (Optional: RabbitMQ for async messaging)

## Core Components

### Clerk (API Gateway)
**File:** `azrael/clerk.py`

The main entry point for all client interactions.

**Responsibilities:**
- REST API endpoints
- WebSocket connections
- Request validation
- Authentication/authorization
- Routing to backend services

**Key Methods:**
- `spawn()` - Create new objects
- `getObjectStates()` - Query object positions/states
- `setForce()` - Apply forces to objects
- `removeObjects()` - Delete objects

### Leonard (Physics Manager)
**File:** `azrael/leonard.py`

Manages the Bullet physics simulation.

**Responsibilities:**
- Physics simulation stepping
- Collision detection
- Force/torque application
- State synchronization with database

**Key Features:**
- Runs Bullet physics engine
- Handles rigid body dynamics
- Processes constraints (joints, springs)
- Computes collisions

### Bullet Wrapper
**Files:** `azrael/bullet/azBullet.py` (new), `azrael/bullet/azBullet.pyx` (original)

Python interface to Bullet physics.

**Current Implementation (December 2025):**
- Pure Python wrapper around PyBullet
- Drop-in replacement for compiled Cython bindings
- 334 lines, no compilation required

**Key Classes:**
- `BulletBase` - Physics world
- `Vec3`, `Quaternion`, `Transform` - Math types
- `SphereShape`, `BoxShape`, `PlaneShape` - Collision shapes
- `RigidBody` - Physics bodies
- `Constraint` classes - Joints and springs

### Datastore
**File:** `azrael/datastore.py`

MongoDB wrapper for state persistence.

**Responsibilities:**
- Store object states
- Handle queries
- Manage templates
- Cache frequently accessed data

## Data Flow

### Spawning an Object

```
Client
  │
  │ spawn(template_id, position, ...)
  │
  ▼
Clerk
  │
  │ validate request
  │
  ▼
Datastore
  │
  │ store object metadata
  │
  ▼
Leonard
  │
  │ create rigid body in Bullet
  │
  ▼
Simulation Running
```

### Simulation Loop

```
┌─────────────────────────────────────────┐
│                                         │
│  1. Read forces/commands from DB        │
│                                         │
│  2. Apply to Bullet rigid bodies        │
│                                         │
│  3. Step Bullet simulation              │
│                                         │
│  4. Read updated positions from Bullet  │
│                                         │
│  5. Write back to DB                    │
│                                         │
│  6. Compute collisions                  │
│                                         │
│  7. Notify clients of events            │
│                                         │
└─────────────┬───────────────────────────┘
              │
              │ Loop at ~60 Hz
              │
              └─────────────────────────────┐
                                            │
                                            ▼
                                         Repeat
```

## Design Principles

### 1. Stateless Services

Services (Clerk, Leonard) don't store state internally. All state lives in MongoDB.

**Benefits:**
- Easy to scale horizontally
- Services can crash and restart
- Multiple instances can run simultaneously

### 2. Network-First

Everything communicates over the network, even locally.

**Benefits:**
- Services can run on different machines
- Easy to distribute workload
- Clean separation of concerns

### 3. Template-Based

Objects are created from templates (blueprints).

**Benefits:**
- Reuse common object definitions
- Consistent object creation
- Easy to modify object types

### 4. Event-Driven

Services communicate via events (collisions, state changes, etc.).

**Benefits:**
- Loose coupling
- Easy to add new event handlers
- Supports asynchronous processing

## Key Files

```
azrael/
├── clerk.py              # API gateway (1500 lines)
├── leonard.py            # Physics manager (1300 lines)
├── datastore.py          # MongoDB wrapper (800 lines)
├── aztypes.py            # Core data types (400 lines)
├── bullet/
│   ├── azBullet.py       # PyBullet wrapper (334 lines, NEW)
│   ├── azBullet.pyx      # Original Cython bindings (800 lines)
│   ├── hello.py          # Demo script
│   └── *.pxd             # Cython definitions
└── test/
    ├── test_aztypes.py   # Type tests
    ├── test_leonard.py   # Physics tests
    └── test_clerk.py     # API tests
```

## Scaling

### Horizontal Scaling

Multiple instances of services can run simultaneously:

```
    Client1 ──┐
              ├──> Clerk1 ──┐
    Client2 ──┘              │
                             ├──> MongoDB
    Client3 ──┐              │
              ├──> Clerk2 ──┘
    Client4 ──┘

    Leonard1 ──┐
               ├──> MongoDB
    Leonard2 ──┘
```

### Partitioning

Large simulations can be partitioned spatially:

```
┌─────────────┬─────────────┐
│             │             │
│  Leonard1   │  Leonard2   │
│  (sector A) │  (sector B) │
│             │             │
├─────────────┼─────────────┤
│             │             │
│  Leonard3   │  Leonard4   │
│  (sector C) │  (sector D) │
│             │             │
└─────────────┴─────────────┘
```

Objects moving between sectors are handed off between Leonard instances.

## Performance

**Typical Numbers (single machine):**
- 60 Hz simulation rate
- 1000+ objects
- 10,000+ collision checks per second
- <50ms latency for API calls

**Bottlenecks:**
- MongoDB queries (can be cached)
- Network latency (minimize cross-service calls)
- Bullet simulation (scales with object count)

## Future Architecture

See [EVOLUTION.md](EVOLUTION.md) for planned improvements:
- OpenAI Gym integration
- Better scaling strategies  
- Improved state synchronization
- GPU acceleration options

## Questions?

- See [QUICK_START.md](QUICK_START.md) to get running
- Check [CONTRIBUTING.md](../CONTRIBUTING.md) to help improve Azrael
- Review `azrael/*.py` for implementation details
