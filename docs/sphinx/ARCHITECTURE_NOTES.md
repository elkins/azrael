# Architecture Notes & Technical Deep Dive

**Purpose:** Understanding Azrael's architecture for future evolution

## Current System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENTS                              │
│  (Python, JavaScript, Any ZMQ-capable language)              │
└─────────────┬───────────────────────────┬───────────────────┘
              │                           │
      ┌───────▼────────┐         ┌───────▼────────┐
      │   ZeroMQ       │         │   WebSocket    │
      │   Clients      │         │   (Browsers)   │
      └───────┬────────┘         └───────┬────────┘
              │                           │
              └──────────┬────────────────┘
                         │
              ┌──────────▼──────────┐
              │    Web Server       │  (Tornado)
              │  (WS→ZMQ Bridge)    │
              └──────────┬──────────┘
                         │
              ┌──────────▼──────────┐
              │       CLERK         │  ← Stateless API Gateway
              │  - Validate inputs  │     (Can scale horizontally)
              │  - Route requests   │
              │  - JSON ↔ Python    │
              └──────────┬──────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────▼────┐     ┌────▼────┐     ┌────▼────┐
   │ DIBBLER │     │  IGOR   │     │ LEONARD │
   │(Geometry)     │(Physics)│     │(Constraints)
   │Database │     │ Engine  │     │Database │
   └────┬────┘     └────┬────┘     └────┬────┘
        │               │                │
        └───────┬───────┴────────┬───────┘
                │                │
        ┌───────▼─────┐   ┌─────▼──────┐
        │  MongoDB    │   │ azBullet   │
        │  Datastore  │   │ (Cython)   │
        └─────────────┘   └─────┬──────┘
                                 │
                          ┌──────▼───────┐
                          │ Bullet       │
                          │ Physics      │
                          │ (C++)        │
                          └──────────────┘
```

## Component Breakdown

### Clerk (Gateway)
- **File:** `azrael/clerk.py`
- **Role:** Stateless API gateway
- **Responsibilities:**
  - Input validation and sanity checking
  - Protocol encoding/decoding (JSON ↔ Python types)
  - Request routing to appropriate services
  - Error handling and response formatting
- **Key Insight:** Multiple Clerk instances can run simultaneously (designed for horizontal scaling)

### Leonard (Physics Manager)
- **File:** `azrael/leonard.py`
- **Role:** Physics simulation orchestrator
- **Responsibilities:**
  - Manages Bullet physics world
  - Steps simulation forward
  - Handles collision detection
  - Applies forces and constraints
  - Updates object states
- **Key Insight:** Contains "sweeping" algorithm for AABB collision detection

### Igor (Constraint Manager)
- **File:** `azrael/igor.py`
- **Role:** Manages physical constraints between objects
- **Responsibilities:**
  - Point-to-point constraints
  - 6-DOF spring constraints
  - Constraint validation
- **Use Cases:** Chain links, joints, tethers between spacecraft

### Dibbler (Geometry Manager)
- **File:** `azrael/dibbler.py`
- **Role:** Geometry database interface
- **Responsibilities:**
  - Store/retrieve 3D mesh data
  - Template management (object blueprints)
  - Fragment geometry (visual parts)
- **Storage:** MongoDB GridFS for large mesh files

### Datastore
- **File:** `azrael/datastore.py`
- **Role:** Database abstraction layer
- **Collections:**
  - `Commands`: Force/torque commands for objects
  - `Constraints`: Physical constraints between objects
  - `Counters`: Unique ID generation
  - `ObjInstances`: Active object instances
  - `Templates`: Object blueprints
- **Key Insight:** Designed to be swappable (currently MongoDB, could be PostgreSQL)

### Event Store
- **File:** `azrael/eventstore.py`
- **Role:** Event logging and replay system
- **Potential:** Time-travel debugging, simulation replay, analytics

### Vector Grid
- **File:** `azrael/vectorgrid.py`
- **Role:** Spatial force field system
- **Use Cases:**
  - Gravity fields
  - Magnetic fields
  - Solar wind
  - Custom force fields for swarm behaviors
- **Key Feature:** Infinite grids with configurable granularity

### Protocol Layer
- **File:** `azrael/protocol.py`
- **Role:** Serialization codecs
- **Functions:**
  - `ToClerk_*_Decode`: JSON → Python types
  - `FromClerk_*_Encode`: Python types → JSON
- **Design:** Language-agnostic API via JSON

### Bullet Bindings
- **Directory:** `azrael/bullet/`
- **Files:** `*.pyx`, `*.pxd` (Cython)
- **Components:**
  - `basic.pyx`: Core Bullet wrapper
  - `rigid_body.pyx`: Rigid body dynamics
  - `collision_shapes.pyx`: Sphere, box, plane shapes
  - `transform.pyx`: Position/rotation math
  - `typed_constraint.pyx`: Constraint wrappers
- **Why Custom?** Better Python integration than stock PyBullet

## Data Flow Examples

### Spawning an Object

```
1. Client sends spawn request (JSON/ZMQ or WebSocket)
   ↓
2. Clerk validates template ID exists
   ↓
3. Clerk generates unique object ID
   ↓
4. Clerk inserts into ObjInstances database
   ↓
5. Leonard creates rigid body in Bullet world
   ↓
6. Client receives object ID
```

### Physics Step

```
1. Leonard queries Commands database for forces
   ↓
2. Applies forces to Bullet rigid bodies
   ↓
3. Calls Bullet stepSimulation()
   ↓
4. Reads back positions/velocities
   ↓
5. Updates ObjInstances database
   ↓
6. Emits events to EventStore
```

### Client Query

```
1. Client requests rigid body data (position, velocity)
   ↓
2. Clerk validates object IDs
   ↓
3. Queries ObjInstances database
   ↓
4. Encodes to JSON and returns
```

## Performance Characteristics

### Bottlenecks (Current)

1. **Database Latency**
   - Every query hits MongoDB
   - Network round-trips for each operation
   - No caching layer

2. **Single-Threaded Physics**
   - Leonard runs in one process
   - Bullet is single-threaded (CPU version)
   - No GPU acceleration

3. **Polling-Based Updates**
   - Clients poll for state changes
   - No push notifications
   - Wastes bandwidth

4. **JSON Serialization**
   - Overhead for large datasets
   - No binary protocol option

### Optimizations to Consider

1. **Add Redis Cache**
   - Cache frequently accessed objects
   - Reduce MongoDB load by 10-100x
   - TTL-based invalidation

2. **Use GPU Bullet**
   - 10-100x more rigid bodies
   - Parallel collision detection
   - CUDA/OpenCL support

3. **Event-Driven Updates**
   - Server-Sent Events (SSE) for browsers
   - ZMQ PUB/SUB for native clients
   - Only send changes, not full state

4. **Binary Protocol**
   - Protocol Buffers or MessagePack
   - 2-10x smaller payload
   - Faster serialization

5. **Horizontal Scaling**
   - Multiple Leonard instances with spatial partitioning
   - Load balancer for Clerk instances
   - Sharded database

## Key Design Patterns

### 1. Stateless Gateway Pattern
- Clerk has no persistent state
- All state in database
- Enables horizontal scaling
- Simplifies deployment

### 2. Template-Instance Pattern
- Templates = object blueprints
- Instances = spawned objects
- Reduces duplication
- Fast spawning of identical objects

### 3. Fragment-Based Geometry
- Objects composed of named fragments
- Each fragment has geometry + position
- Enables modular construction
- Good for compound shapes

### 4. Command Pattern
- Forces/torques as database commands
- Decouples client from physics engine
- Allows batch processing
- Enables replay

### 5. Event Sourcing (Partial)
- Events logged to EventStore
- Could reconstruct state from events
- Enables time-travel debugging
- Currently underutilized

## Technology Stack

### Core
- **Language:** Python 3.x (originally 2.7, transitioned)
- **Physics:** Bullet 2.x (via custom Cython bindings)
- **Database:** MongoDB 3.x+
- **Networking:** ZeroMQ, WebSockets (Tornado)
- **Serialization:** JSON (with Base64 for binary data)

### Frontend
- **3D Rendering:** Three.js (browser), PyQt + OpenGL (desktop)
- **Loaders:** ColladaLoader for .dae files
- **Controls:** FlyControls for camera navigation

### Development
- **Testing:** pytest
- **Type Checking:** Custom `@typecheck` decorator (pre-PEP 484)
- **Documentation:** Sphinx + reStructuredText
- **Containerization:** Docker, docker-compose

### Dependencies (Key)
```python
# From environment.yml
- numpy
- scipy
- pymongo
- pyzmq
- tornado
- jsonschema
- networkx
- cython
- pytest
- sphinx
```

## Security Considerations

### Current State
- ✗ No authentication/authorization
- ✗ No input rate limiting
- ✗ No encryption (plain ZMQ/WS)
- ✓ Input validation (JSON schema)
- ✓ Type checking

### For Production
- Add JWT or OAuth2 authentication
- TLS for all network communication
- Rate limiting per client
- Resource quotas (max objects per client)
- Audit logging

## Extensibility Points

### Adding New Object Types
1. Create collision shape in `azrael/bullet/`
2. Add geometry loading in `demolib.py`
3. Create template in demo script
4. No core changes needed

### Adding New Constraints
1. Extend `igor.py` with new constraint type
2. Add Bullet binding in `azrael/bullet/typed_constraint.pyx`
3. Update schema in `azrael/azschemas.py`

### Adding New Commands
1. Define schema in `azrael/azschemas.py`
2. Add codec in `azrael/protocol.py`
3. Implement handler in `azrael/clerk.py`
4. Update Leonard if physics-related

### Adding New Clients
1. Implement ZMQ socket connection
2. Follow JSON protocol from `protocol.py`
3. Examples: `pyazrael/client.py`, `pyazrael/wsclient.py`

## Testing Strategy

### Current Coverage
- Unit tests in `azrael/test/test_*.py`
- Integration tests in demos
- Manual testing via Qt/browser viewers

### Test Files
```
azrael/test/
├── test_azschemas.py       # Schema validation
├── test_aztypes.py         # Type system
├── test_bullet_api.py      # Physics wrapper
├── test_clerk.py           # API gateway
├── test_datastore.py       # Database layer
├── test_dibbler.py         # Geometry manager
├── test_eventstore.py      # Event logging
├── test_igor.py            # Constraints
├── test_leo_api.py         # Leonard API
├── test_leonard.py         # Physics manager
└── test_vectorgrid.py      # Force fields
```

### Gaps
- No load testing
- No property-based testing
- Limited integration tests
- No performance benchmarks
- No fuzzing

## Evolution Opportunities (Technical)

### 1. Modern Python (High Impact, Low Risk)
- Type hints (PEP 484)
- async/await for I/O
- dataclasses instead of namedtuples
- f-strings everywhere
- pathlib instead of os.path

### 2. Better Database (High Impact, Medium Risk)
- PostgreSQL + TimescaleDB
- Proper indexing strategy
- Connection pooling
- Query optimization
- Migrations with Alembic

### 3. gRPC API (Medium Impact, Medium Risk)
- Typed, versioned API
- Streaming support
- Better performance than JSON
- Code generation for clients
- Backward compatibility

### 4. GPU Physics (High Impact, High Risk)
- Requires Bullet GPU port
- Complex build process
- Platform-specific code
- But: 10-100x speedup

### 5. Kubernetes Deployment (Medium Impact, High Risk)
- Helm charts
- Auto-scaling
- Service mesh
- Monitoring integration
- Complex operations

## Code Quality Observations

### Strengths
- Consistent style
- Good separation of concerns
- Comprehensive type checking (custom decorator)
- RetVal pattern for error handling
- Test coverage on critical paths

### Areas for Improvement
- Some functions are very long (200+ lines)
- Limited documentation in complex algorithms
- Custom type system (pre-PEP 484)
- Global state in some modules
- Tight coupling to MongoDB

### Metrics
```bash
# Core codebase
$ wc -l azrael/*.py
  9011 total

# Tests
$ wc -l azrael/test/*.py
  ~7000 total

# Test-to-code ratio: ~0.77 (good!)
```

## Learning Resources

If you want to understand this codebase:

1. **Start Here:**
   - `README.rst` - Overview
   - `demos/demo_rosetta.py` - Simple complete example
   - `pyazrael/client.py` - Client API

2. **Core Architecture:**
   - `azrael/clerk.py` - Main API gateway
   - `azrael/protocol.py` - JSON format
   - `azrael/leonard.py` - Physics loop

3. **Physics Details:**
   - `azrael/bullet_api.py` - Bullet wrapper
   - `azrael/bullet/*.pyx` - Cython bindings

4. **Advanced Features:**
   - `azrael/vectorgrid.py` - Force fields
   - `azrael/eventstore.py` - Event sourcing
   - `azrael/igor.py` - Constraints

## Conclusion

Azrael has a well-designed architecture for a distributed physics simulation platform.
The key strengths are:
- Clean separation of concerns
- Stateless design enabling horizontal scaling
- Language-agnostic API
- Event sourcing foundation

The main limitations are:
- Performance (database latency, single-threaded physics)
- Dated technology stack
- Underutilized features (event store, vector grids)

With focused modernization and feature development (especially RL integration),
this could become a leading platform for multi-agent space robotics research.

---

**Next:** See [evolution_roadmap.rst](evolution_roadmap.rst) for strategic direction.
