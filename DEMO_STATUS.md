# Demo Status Report

**Date:** December 10, 2025
**Tested By:** Claude Code

## Quick Answer

**Demos do NOT work out of the box** on modern Python without additional setup.

## What Works

✅ **Basic Python imports** - The azrael module can be imported
✅ **Most dependencies** - numpy, pymongo, tornado, pytest, jsonschema available
✅ **Code structure** - No obvious syntax errors or corruption

## What Doesn't Work

❌ **Bullet Physics bindings** - Custom Cython extensions not compiled
❌ **Docker demo** - Docker daemon not running (could work if started)
❌ **Direct Python tests** - Fail due to missing azBullet module
❌ **Full dependency chain** - Environment designed for Python 3.5, tested on 3.12

## Issues Found

### 1. Missing Compiled Extensions

The core issue is that the Bullet physics engine bindings need to be compiled:

```
ModuleNotFoundError: No module named 'azrael.bullet.azBullet'
```

These are Cython extensions (`.pyx` files) that wrap the C++ Bullet library.

**Location:** `azrael/bullet/`
**Build script:** `azrael/bullet/setup.py`

### 2. Environment Mismatch

The project was designed for:
- Python 3.5
- Specific conda packages from custom channel (`olitheolix`)
- Older versions of all dependencies

Current system:
- Python 3.12.10
- Modern pip packages
- Different library versions

### 3. Docker Image Availability

The Docker Compose files reference:
```yaml
image: olitheolix/azrael:latest
```

This image may or may not still exist on Docker Hub (couldn't test as Docker daemon wasn't running).

## What Would Be Needed to Run Demos

### Option 1: Docker (Easiest if image exists)

```bash
# Start Docker daemon
# Then run:
docker-compose -f demos/docker/asteroids_autopilot.yml up
# Open browser to http://localhost:8080
```

**Status:** Not tested (Docker daemon not running)
**Risk:** Docker image may be outdated or unavailable

### Option 2: Build from Source (Most reliable)

```bash
# Install system dependencies
sudo apt-get install build-essential  # Linux
# or
brew install cmake bullet  # macOS

# Create conda environment
conda env create --name azrael --file environment.yml
conda activate azrael

# Build Bullet bindings
cd azrael/bullet
python setup.py build_ext --inplace
cd ../..

# Run demo
python demos/demo_rosetta.py --noviewer
```

**Status:** Not attempted
**Risk:** Custom conda packages may no longer be available

### Option 3: Modernize First (Recommended for serious use)

1. Upgrade to Python 3.10+
2. Replace custom Bullet bindings with PyBullet
3. Update all dependencies
4. Fix compatibility issues
5. Then run demos

**Status:** Would require significant effort
**Time:** 1-2 weeks

## Test Results

### Dependencies Check

| Dependency | Status | Notes |
|------------|--------|-------|
| numpy | ✓ | Working |
| pymongo | ✓ | Working |
| pyzmq | ✓ | Working |
| tornado | ✓ | Working |
| pytest | ✓ | Working |
| jsonschema | ✓ | Working |
| networkx | ✓ | Installed during test |
| setproctitle | ✓ | Installed during test |
| pika | ✓ | Installed during test |
| azBullet | ✗ | Not compiled |

### Import Test

```python
import azrael  # ✓ Works
import azrael.aztypes  # ✗ Fails (needs azBullet)
import azrael.leonard  # ✗ Fails (needs azBullet)
```

### Pytest Run

```bash
pytest azrael/test/test_aztypes.py
# Result: Collection error due to missing azBullet
```

## Historical Context

Based on the README and git history:
- Last significant development: ~2016
- PyCon Australia 2015 presentation shows it working
- Docker demos were added and appear to have worked
- Environment.yml indicates Python 3.5 era

The demos **did work** at some point, but:
- Dependencies have evolved
- Docker images may be outdated
- Compiled extensions need rebuilding

## Recommendations

### For Quick Test

**Try Docker approach:**
```bash
# Start Docker Desktop
docker-compose -f demos/docker/asteroids_autopilot.yml up
```

If the Docker image still exists and works, this is the fastest way to see Azrael in action.

### For Development

**Follow the modernization path from QUICK_START_EVOLUTION.md:**

1. Update to Python 3.10+
2. Replace Bullet bindings with standard PyBullet
3. Update dependencies
4. Fix compatibility issues
5. Rebuild Docker images

This aligns with the evolution roadmap and makes the project maintainable.

### For Immediate Validation (Without Full Setup)

**Code Review Approach:**
- The code compiles and imports (basic Python)
- Architecture is sound (well-structured)
- Tests exist and follow pytest conventions
- Documentation is comprehensive

While we can't run the physics simulation without compiled Bullet bindings, the codebase appears solid from a code quality perspective.

## Conclusion

**Can the demos run?**

**In theory: YES** - The code is intact and architecture is sound.

**In practice: NOT OUT OF THE BOX** - Requires either:
- Docker setup (if images still exist), or
- Building Bullet bindings from source, or
- Modernization effort

**Estimated effort to get ONE demo working:**
- Docker route: 10-30 minutes (if image exists)
- Build from source: 2-4 hours (if all deps available)
- Modernization route: 1-2 weeks

**Bottom line:** This is a dormant but viable project. With modest effort (Docker) or significant effort (modernization), the demos could be brought back to life.

## Next Steps

If you want to verify the demos work:

1. **Quickest test:** Start Docker Desktop and try the Docker Compose demo
2. **If that fails:** Check if Docker image exists on Docker Hub
3. **If no image:** Would need to build Bullet bindings or modernize

For serious use, I'd recommend the modernization path outlined in the evolution documents rather than trying to resurrect the old environment.

---

**Note:** This assessment was done without Docker daemon running and without attempting to compile Bullet bindings. With Docker, results might be better.
