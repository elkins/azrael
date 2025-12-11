# Azrael History

## December 2025 - Modernization

**Goal:** Get Azrael working again on modern Python

**What Happened:**
- Created PyBullet wrapper to replace Cython bindings (2 hours!)
- Added Python 3.10+ support
- Set up CI/CD with GitHub Actions
- Created simple demos
- Modernized documentation

**Result:** Demos work with `pip install` - no compilation needed!

**Key Files Added:**
- `azrael/bullet/azBullet.py` - Pure Python wrapper (334 lines)
- `demos/simple_demo.py` - Text-based demo
- `demos/visual_azrael_demo.py` - 3D GUI demo
- `requirements.txt` - Modern dependencies
- `.github/workflows/tests.yml` - CI/CD

**See:** `docs/archive/QUICK_WINS_SUMMARY.md` for full details

## 2014-2017 - Original Development

**Author:** Oliver Nagy

**Goal:** Distributed physics simulation for space robotics research

**Key Features Implemented:**
- Custom Cython bindings to Bullet C++
- Distributed architecture (Clerk, Leonard, MongoDB)
- WebSocket/REST APIs
- Space robotics demos (satellites, debris, rendezvous)
- Multi-agent support

**Technologies:**
- Python 3.5
- Cython for Bullet bindings
- MongoDB for state storage
- RabbitMQ for messaging
- ZeroMQ for communication

**Result:** Working research platform for space robotics

## 2017-2025 - Dormant Period

**What Happened:**
- Python ecosystem moved forward (3.6, 3.7, ..., 3.12)
- Compilation became difficult on modern systems
- Dependencies outdated
- Demos stopped working

**Status:** Project appeared abandoned but wasn't - just needed modernization

## Timeline

| Date | Event |
|------|-------|
| ~2014 | Initial development begins |
| 2015-2016 | Core features implemented |
| 2017 | Last major updates |
| 2017-2025 | Dormant (no active development) |
| Dec 10, 2025 | Modernization begins |
| Dec 10, 2025 | PyBullet wrapper created |
| Dec 10, 2025 | Demos working again! |
| Dec 11, 2025 | CI/CD, tests, docs updated |

## Original Vision

From the original README:

> Azrael is a physics engine for space, ships, and structures. It aims to be
> the platform for realistic space game environments and robotics research.
>
> Key features:
> - Distributed architecture for massive simulations
> - Realistic orbital mechanics
> - Multi-agent swarm robotics
> - Modular spacecraft assembly
> - Debris and collision modeling

This vision remains valid and is being revived!

## Lessons Learned

**What Worked:**
- Distributed architecture aged well
- Core design principles still sound
- Bullet physics was the right choice
- Template-based object system flexible

**What Didn't:**
- Cython bindings hard to maintain
- Compilation barrier too high
- Python 3.5 specific code
- Complex setup (Docker, MongoDB, etc.)

**Modern Approach:**
- PyBullet wrapper - much easier
- Python 3.10+ - modern features
- Simpler installation
- Better documentation
- CI/CD automation

## Looking Forward

See [EVOLUTION.md](EVOLUTION.md) for the future roadmap:
- Multi-agent RL platform
- OpenAI Gym integration
- Modern tooling
- Community building

The original vision of a distributed physics platform for space robotics
remains intact - we're just using modern tools to get there!

## Credits

**Original Author:** Oliver Nagy
- Designed and implemented Azrael (2014-2017)
- Created Cython bindings
- Built distributed architecture
- Developed space robotics demos

**Modernization (2025):** George Elkins
- Created PyBullet wrapper
- Updated to Python 3.10+
- Added CI/CD
- Modernized documentation
- Revived the project

**Community:** (future contributors welcome!)

## References

- Original repository: https://github.com/olitheolix/azrael (archived)
- Current repository: https://github.com/elkins/azrael
- Bullet Physics: https://pybullet.org
- PyBullet: https://pypi.org/project/pybullet/
