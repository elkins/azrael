# Contributing to Azrael

Thanks for your interest in contributing! Azrael is now actively maintained and welcoming contributions.

## Quick Start

```bash
# Clone the repo
git clone https://github.com/elkins/azrael
cd azrael

# Install dependencies
pip install -r requirements.txt

# Run tests
./run_tests.sh

# Run a demo
python3 simple_demo.py
```

## Development Setup

### Prerequisites
- Python 3.10 or higher
- pip

### Install Development Dependencies
```bash
pip install -r requirements.txt
```

This includes:
- Core dependencies (numpy, pymongo, etc.)
- PyBullet (physics engine)
- Testing tools (pytest)
- Code quality tools (black, ruff, mypy)

## Running Tests

### Quick Test
```bash
./run_tests.sh
```

### Full Test Suite
```bash
pytest azrael/test/ -v
```

### Specific Test File
```bash
pytest azrael/test/test_aztypes.py -v
```

### With Coverage
```bash
pytest --cov=azrael --cov-report=html
```

## Code Style

We follow standard Python conventions:

### Formatting
```bash
# Format code
black azrael/

# Lint
ruff check azrael/

# Type check
mypy azrael/
```

### Guidelines
- Follow PEP 8
- Use type hints where possible
- Write docstrings for public functions
- Keep functions focused and testable

## Making Changes

### Workflow

1. **Fork the repository** on GitHub

2. **Create a branch** for your changes
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write code
   - Add tests
   - Update documentation

4. **Test your changes**
   ```bash
   ./run_tests.sh
   pytest azrael/test/
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** on GitHub

### Commit Messages

Write clear commit messages:
- Use present tense ("Add feature" not "Added feature")
- Be concise but descriptive
- Reference issues if applicable

Good examples:
- `Add support for mesh collision shapes`
- `Fix velocity calculation in RigidBody`
- `Update documentation for PyBullet wrapper`

## What to Contribute

### High Priority
- **More PyBullet wrapper features** - Constraints, compound shapes, etc.
- **More demos** - Showcase different Azrael features
- **Tests** - Increase coverage, especially for physics integration
- **Documentation** - Tutorials, examples, API docs
- **Bug fixes** - Check GitHub issues

### Medium Priority
- **Performance improvements** - Profile and optimize
- **New features** - From the roadmap (see evolution_roadmap.rst)
- **CI/CD improvements** - Better testing, deployment
- **Code quality** - Refactoring, type hints, cleanup

### Low Priority (but welcome!)
- **Examples** - More demo scenarios
- **Tooling** - Developer experience improvements
- **Packaging** - Better installation, distribution

## Areas of Focus

### 1. Physics Engine (azrael/bullet/)
The PyBullet wrapper is new and could use:
- More collision shape types
- Constraint support (P2P, 6DOF)
- Better error handling
- Performance testing

### 2. Core Services (azrael/)
- Clerk (API gateway)
- Leonard (physics manager)
- Datastore improvements
- Better async handling

### 3. Demos (demos/)
- More showcase scenarios
- Better documentation
- Performance benchmarks
- Educational examples

### 4. Testing
- Integration tests
- Performance tests
- Full stack tests (with MongoDB/RabbitMQ)
- Edge case coverage

### 5. Documentation
- API documentation
- Architecture guides
- Tutorial series
- Video demonstrations

## Getting Help

- **Issues**: Check [GitHub Issues](https://github.com/elkins/azrael/issues)
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: See [README_ANALYSIS.md](README_ANALYSIS.md) for overview

## Code Review Process

1. Automated tests must pass (GitHub Actions)
2. Code should follow style guidelines
3. Changes should include tests
4. Documentation should be updated
5. Maintainer reviews and provides feedback
6. Once approved, we'll merge!

## Current Status (December 2025)

Azrael just got a major update:
- ✅ Demos working with PyBullet wrapper
- ✅ Tests passing on Python 3.10+
- ✅ CI/CD set up
- ✅ Ready for contributions!

See [QUICK_WIN.md](QUICK_WIN.md) for recent progress.

## Evolution Roadmap

We're evolving Azrael into a multi-agent RL platform. See:
- [evolution_roadmap.rst](doc/evolution_roadmap.rst) - Long-term vision
- [QUICK_START_EVOLUTION.md](QUICK_START_EVOLUTION.md) - Next steps

Your contributions can help shape this future!

## Questions?

Feel free to:
- Open an issue
- Start a discussion
- Ask in pull request comments

We're friendly and welcoming to new contributors!

## License

By contributing, you agree that your contributions will be licensed under:
- AGPL v3 (for core `azrael/` code)
- Apache v2 (for demos and client code)

See [LICENSE](azrael/LICENSE) for details.

---

**Thank you for contributing to Azrael!** 🚀
