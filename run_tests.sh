#!/bin/bash
# Quick test runner for Azrael
# Tests core functionality without needing full stack

set -e

echo "================================"
echo "Azrael Quick Test Suite"
echo "================================"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python3 --version
echo ""

# Run pytest
echo "✓ Running unit tests..."
python3 -m pytest azrael/test/test_aztypes.py -v
echo ""

# Test imports
echo "✓ Testing core imports..."
python3 -c "
import azrael.aztypes
import azrael.bullet.azBullet
import azrael.bullet_api
import azrael.leonard
import azrael.clerk
print('  All core modules import successfully!')
"
echo ""

# Run simple physics test
echo "✓ Running physics demo..."
python3 azrael/bullet/hello.py | head -5
echo "  ... (physics simulation running)"
echo ""

echo "================================"
echo "✅ All tests passed!"
echo "================================"
echo ""
echo "Next steps:"
echo "  - Run text demo: python3 demos/simple_demo.py"
echo "  - Run visual demo: python3 demos/visual_azrael_demo.py"
echo "  - Run full test suite: pytest azrael/test/"
echo "  - See docs/QUICK_START.md for more information"
