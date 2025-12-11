# Changelog

All notable changes to Azrael will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### December 2025 - Modernization & Revival

This represents the modernization effort that brought Azrael back to life after being dormant since 2017.

#### Added
- **PyBullet Wrapper** (`azrael/bullet/azBullet.py`) - Pure Python wrapper around PyBullet replacing custom Cython bindings
  - 334 lines of clean Python code
  - Drop-in replacement for original compiled bindings
  - No compilation required
- **Working Demos**
  - `demos/simple_demo.py` - Text-based bouncing ball with ASCII visualization
  - `demos/visual_azrael_demo.py` - 3D OpenGL demo using Azrael's wrapper
  - `demos/pybullet_only_demo.py` - Pure PyBullet reference implementation
- **Modern Infrastructure**
  - `requirements.txt` - Simplified dependency management
  - `.github/workflows/tests.yml` - CI/CD with GitHub Actions (Python 3.10, 3.11, 3.12)
  - `run_tests.sh` - One-command test runner
  - `CONTRIBUTING.md` - Contribution guidelines
- **Documentation**
  - Reorganized into `docs/` directory with clear structure
  - `docs/QUICK_START.md` - 5-minute getting started guide
  - `docs/ARCHITECTURE.md` - System design and components
  - `docs/EVOLUTION.md` - Future roadmap and RL vision
  - `docs/HISTORY.md` - Project timeline
  - `README.md` - New markdown README with badges
- **Repository Polish**
  - Modern `.gitignore` with 40+ patterns
  - GitHub Actions badges (CI status, Python version)
  - Cleaned up legacy files

#### Changed
- **Python Support** - Now requires Python 3.10+ (was Python 3.5)
- **Installation** - Simplified to `pip install -r requirements.txt` (no compilation)
- **Documentation Structure** - Consolidated `doc/` and `docs/` into single `docs/` directory
- **Demo Organization** - All demos moved to `demos/` directory

#### Removed
- `README.rst` - Replaced with `README.md`
- `simple_demo.py` from root - Moved to `demos/`
- `shared/azutils.py.mybak` - Removed backup file
- Python cache files (`__pycache__`, `*.pyc`)

#### Fixed
- Demos now work out of the box (no compilation needed)
- Tests passing on Python 3.10, 3.11, 3.12
- Import errors resolved
- Path references updated throughout

#### Technical Details
- **Time to modernize**: ~8 hours total
  - PyBullet wrapper: 2 hours
  - CI/CD setup: 1 hour
  - Documentation: 3 hours
  - Polish & cleanup: 2 hours
- **Lines of code added**: ~2,000 (docs + wrapper + demos)
- **Key technology swap**: Cython → PyBullet (pure Python)

#### Performance
- Physics simulation: ~240 Hz (similar to original)
- Demo startup: <1 second (much faster than before)
- Installation: <1 minute (was 10+ minutes with compilation)

#### Breaking Changes
- Custom Cython bindings replaced with PyBullet wrapper
  - API is compatible but implementation is different
  - Some advanced features may need testing
- Python 3.5-3.9 no longer supported
- Compilation no longer required (breaking for build-dependent workflows)

## [Legacy] - 2014-2017

Original development period by Oliver Nagy.

### Features Implemented
- Distributed physics simulation architecture
- Custom Cython bindings to Bullet C++ library
- Clerk (API gateway), Leonard (physics manager), Datastore (MongoDB)
- ZeroMQ and WebSocket communication
- Space robotics demos (satellites, debris, rendezvous)
- Multi-agent swarm support
- Template-based object system

### Technologies
- Python 3.5
- Cython for Bullet bindings
- MongoDB for state storage
- RabbitMQ for messaging
- Bullet Physics Engine

---

## Notes

### Versioning Strategy
- Currently unversioned (in active modernization)
- Will adopt semantic versioning when stable
- Target: v1.0.0 when full stack is modernized

### What's Coming Next
See [docs/EVOLUTION.md](docs/EVOLUTION.md) for roadmap:
- OpenAI Gym integration
- More PyBullet wrapper features
- Multi-agent RL demos
- Better scaling strategies
- Full stack modernization (MongoDB, RabbitMQ optional)

### How to Contribute
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Links
- Repository: https://github.com/elkins/azrael
- Issues: https://github.com/elkins/azrael/issues
- Original: https://github.com/olitheolix/azrael (archived)
