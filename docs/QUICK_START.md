# Azrael Quick Start

Get Azrael running in 5 minutes.

## Prerequisites

- Python 3.10 or higher
- pip

## Installation

```bash
# Clone the repository
git clone https://github.com/elkins/azrael
cd azrael

# Install dependencies
pip install -r requirements.txt
```

That's it! No compilation, Docker, or external services needed for basic demos.

## Run Your First Demo

### Option 1: Text-Based Demo

```bash
python demos/simple_demo.py
```

You'll see:
```
============================================================
AZRAEL PHYSICS DEMO - Ball Bouncing
============================================================

🌍 Creating physics world...
   ✓ Gravity set to -10 m/s²

🏔️  Creating ground plane...
   ✓ Ground plane at Y = -1
   ✓ Bounciness = 0.8

⚽ Creating ball...
   ✓ Radius = 1 meter
   ✓ Mass = 1 kg
   ✓ Starting height = 20 meters
   ✓ Bounciness = 0.9

🎬 Running simulation...
------------------------------------------------------------
  Step |   Height (m) |   Velocity | Visual
------------------------------------------------------------
     0 |        19.99 |     -0.42 | ███████████████████████████████████████↓
     1 |        19.96 |     -0.83 | ███████████████████████████████████████↓
     ...
```

### Option 2: Visual 3D Demo

```bash
python demos/visual_azrael_demo.py
```

Opens an OpenGL window showing:
- Red bouncing ball in 3D
- Ground plane with grid
- Interactive camera controls

**Controls:**
- Mouse drag: Rotate camera
- Mouse scroll: Zoom
- Ctrl + Mouse: Pan
- ESC: Exit

## What Just Happened?

You ran Azrael's physics simulation using:
- **Azrael's bullet wrapper** (`azrael.bullet.azBullet`)
- **PyBullet** physics engine (installed via pip)
- **No compilation** required

The demos prove that Azrael's physics layer works!

## Next Steps

### Run Tests

```bash
./run_tests.sh
```

Or use pytest directly:
```bash
pytest azrael/test/
```

### Try More Demos

Check the `demos/` directory for more examples:
```bash
ls demos/demo_*.py
```

**Note:** Most legacy demos require the full Azrael stack (MongoDB, RabbitMQ, services). We're working on updating them.

### Explore the Code

Key files to understand Azrael:

```
azrael/
├── bullet/
│   ├── azBullet.py      # PyBullet wrapper (334 lines)
│   └── hello.py         # Original demo
├── leonard.py           # Physics manager
├── clerk.py             # API gateway
└── aztypes.py           # Core data types

demos/
├── simple_demo.py           # Text-based demo
├── visual_azrael_demo.py    # 3D GUI demo
└── pybullet_only_demo.py    # Pure PyBullet (comparison)
```

## Troubleshooting

### Import Errors

If you get `ModuleNotFoundError`, make sure you installed dependencies:
```bash
pip install -r requirements.txt
```

### Graphics Issues (Visual Demo)

If the 3D window doesn't open:
- Your system needs OpenGL support
- Try the text demo instead: `python demos/simple_demo.py`
- Check PyBullet installation: `python -c "import pybullet; print('OK')"`

### Tests Failing

Make sure you're using Python 3.10+:
```bash
python --version
```

## Full Stack Setup (Advanced)

To run distributed multi-agent scenarios, you need:

1. **MongoDB** (state storage)
2. **RabbitMQ** (message queue)
3. **Azrael services** (Clerk, Leonard, etc.)

See [docs/FULL_STACK.md](FULL_STACK.md) for instructions.

## Questions?

- Check [docs/ARCHITECTURE.md](ARCHITECTURE.md) for system design
- See [CONTRIBUTING.md](../CONTRIBUTING.md) for how to contribute
- Open an issue on GitHub

## What's Next?

Now that you have Azrael running, you can:

1. **Explore demos** - See what Azrael can simulate
2. **Read architecture docs** - Understand how it works
3. **Write your own demo** - Create custom physics scenarios
4. **Contribute** - Help modernize and improve Azrael

Check out [docs/EVOLUTION.md](EVOLUTION.md) for the project's future direction!
