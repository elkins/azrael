# Azrael

[![Tests](https://github.com/elkins/azrael/actions/workflows/tests.yml/badge.svg)](https://github.com/elkins/azrael/actions/workflows/tests.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A distributed physics simulation engine for space robotics, designed for multi-agent reinforcement learning.

**Status:** ✅ **Working!** Demos run on Python 3.10+ with no compilation required.

## Quick Start

```bash
# Clone and install
git clone https://github.com/elkins/azrael
cd azrael
pip install -r requirements.txt

# Run demos
python demos/simple_demo.py              # Text-based bouncing ball
python demos/visual_azrael_demo.py       # 3D GUI demo
```

That's it! No Docker, MongoDB, or RabbitMQ needed for basic demos.

## What is Azrael?

Azrael is a distributed physics simulation platform originally designed for space robotics research. It features:

- **Distributed architecture** - Stateless, network-first design
- **Realistic physics** - Bullet physics engine integration
- **Multi-agent support** - Designed for swarm robotics
- **Space scenarios** - Orbital mechanics, satellite servicing, debris

## Current Status (December 2025)

**Recent Updates:**
- ✅ Demos now working with PyBullet wrapper
- ✅ Python 3.10+ support
- ✅ CI/CD with GitHub Actions
- ✅ Simple pip install (no compilation)
- ✅ Visual 3D demos

**What Works:**
- Physics simulation (via PyBullet wrapper)
- Basic demos showing bouncing objects
- Core Azrael modules import successfully

**What Needs Full Stack:**
- Distributed multi-agent scenarios
- Network communication (ZeroMQ/WebSockets)
- State persistence (MongoDB)
- Message queuing (RabbitMQ)

## Documentation

- **[QUICK_START.md](docs/QUICK_START.md)** - Get running in 5 minutes
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design and components
- **[docs/EVOLUTION.md](docs/EVOLUTION.md)** - Future roadmap and vision

## Project Evolution

Azrael is evolving into a **multi-agent RL platform for space robotics**. See [docs/EVOLUTION.md](docs/EVOLUTION.md) for the vision.

**Potential applications:**
- Orbital rendezvous and docking
- Satellite servicing
- Space debris cleanup
- Swarm robotics research
- Multi-agent RL benchmarks

## Architecture

```
┌─────────────┐
│   Client    │  ← Your code (Python/any language)
└──────┬──────┘
       │ REST/WebSocket
┌──────▼──────┐
│    Clerk    │  ← API Gateway
└──────┬──────┘
       │
┌──────▼──────┐
│   Leonard   │  ← Physics Manager (Bullet)
└──────┬──────┘
       │
┌──────▼──────┐
│   MongoDB   │  ← State Database
└─────────────┘
```

**Key Services:**
- **Clerk** - API gateway, handles client requests
- **Leonard** - Physics simulation manager
- **Datastore** - MongoDB wrapper for state persistence

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for details.

## Requirements

**Minimal (demos only):**
- Python 3.10+
- Dependencies in `requirements.txt`

**Full stack:**
- MongoDB (state storage)
- RabbitMQ (message queue)

## Running Demos

### Simple Text Demo
```bash
python demos/simple_demo.py
```
Shows ball falling with ASCII progress bars.

### Visual 3D Demo
```bash
python demos/visual_azrael_demo.py
```
Opens OpenGL window with 3D bouncing ball simulation.

### Original Demo
```bash
python azrael/bullet/hello.py
```
Original Bullet "hello world" demo.

## Development

```bash
# Run tests
./run_tests.sh

# Or use pytest directly
pytest azrael/test/

# Code formatting
black azrael/
ruff check azrael/
```

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

**High Priority Areas:**
- More PyBullet wrapper features
- Additional demos
- Test coverage
- Documentation

## License

- **Core (`azrael/`)**: AGPL v3
- **Demos and clients**: Apache v2

See [LICENSE](azrael/LICENSE) for details.

## Links

- **Repository**: https://github.com/elkins/azrael
- **Original Author**: Oliver Nagy
- **Current Maintainer**: George Elkins

## History

Azrael was originally developed for space robotics research with custom Cython bindings to Bullet. In December 2025, it was modernized with:
- PyBullet wrapper (replacing custom Cython)
- Python 3.10+ support
- Modern CI/CD
- Simplified installation

See [docs/HISTORY.md](docs/HISTORY.md) for the full story.
