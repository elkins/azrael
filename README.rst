================================================
For Rocket Scientists Who Cannot Afford a Rocket
================================================

The virtual world of the Internet has changed society. Smart innovations in the
non-virtual world, like self driving cars, city wide traffic control systems,
space exploration and more, may do it again. The difference: building and
launching a web service is considerably cheaper than building and launching a
space ship...

Put differently: everyone can contribute to the Internet but only a few
are privy to the resources for a space ship... and *you* are probably not one of
them. Azrael's purpose is to remove this barrier and simulate the (macroscopic)
physics for "stuff" you cannot afford in the real world.

Take the `Rosetta mission
<https://en.wikipedia.org/wiki/Rosetta_%28spacecraft%29>`_ as an example. The
total cost exceeded a Billion dollars and it took years to complete. On the
other hand, to reproduce it in its simplest form for your personal studies you
merely need to simulate the physics of two bodies: an asteroid and a space
probe. The probe has thruster, the asteroid does not. The challenge: write a
controller for the ship to reproduce the original `approach and manoeuvres
<https://en.wikipedia.org/wiki/Rosetta_%28spacecraft%29#Orbit_around_67P>`_.

Technology
==========
Azrael is an API to create bodies and modify their attributes (eg position or
geometry). This API is only accessible via the network. Clients can connect to
it from anywhere and use it to drive the simulation. For instance, they create objects,
control them (like the aforementioned Rosetta probe), render the scene,
progress a Newtonian physics simulation...

Azrael is written in Python yet the network API is language agnostic. The API
accepts Websockets (Java Script in browsers) and ZeroMQ sockets (everything but
Java Script).

To see Azrael in action you may try the demos, watch the `PyCon Australia
2015 <https://youtu.be/JG8-yurFBXM?list=PLs4CJRBY5F1IZYVBLXGX1DRYXHMjUjG8k>`_
presentation, or check out (the somewhat dated)
`demo videos <http://azrael.readthedocs.org/en/latest/demos.html>`_


Not A Game Engine
=================

Azrael does not schedule clients or callbacks - everything happens
asynchronously. It also stores all data in databases and fetching it may incur
unacceptable latency by the standards of a game.

Another point concerns visualisation: Azrael has none. A client may query
object geometries and render them (as seen in the demos) but Azrael itself
would neither know nor care.

That being said, some
`example scenarios <http://azrael.readthedocs.org/en/latest/demos.html>`_
appear reasonably smooth when served from an AWS C4 instance. This despite the
dumb polling used by the visualisation clients.



Project Status
==============

It is a usable work in progress. The emphasis remains on completing the feature
set to build large simulations. Performance optimisation comes afterwards.

The current API suffices to create objects, define and control boosters,
exert force, upload meshes and more. It also comes with a Newtonian physics
engine (based on `Bullet <http://bulletphysics.org>`_) to simulate elementary
motion. This is already enough for a basic Asteroids simulation.

The project also ships with two simple viewers to render the scene. One uses
PyQT/OpenGL whereas the other runs in the browser.


Demos and Documentation
=======================

The scripts in the `demos/` folder showcase various features of Azrael. They
are a good source of usage examples and complement the
`API documentation <http://azrael.readthedocs.org/en/latest/>`_.

Some of the demos also have dedicated docker-compose files in the
`demos/docker/` folder to simplify the setup.

Installation & Quick Start
==========================

**December 2025 Update:** Azrael now works out-of-the-box with modern Python!

Quick Demo (No Setup Required)
-------------------------------

The easiest way to see Azrael in action:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/elkins/azrael
   cd azrael

   # Install dependencies (if not already present)
   pip install pybullet pymongo pyzmq tornado jsonschema networkx setproctitle pika

   # Run a demo!
   python3 simple_demo.py

You should see a ball bouncing with visual progress bars showing the physics
simulation working. This demonstrates that Azrael's physics engine is fully
functional on modern Python (3.10+).

**What changed?** We created a pure-Python wrapper around PyBullet that replaces
the old Cython bindings. No compilation required! See `QUICK_WIN.md <QUICK_WIN.md>`_
for details.

Alternative: Classic Hello World
---------------------------------

.. code-block:: bash

   python3 azrael/bullet/hello.py

This shows the same bouncing ball physics in a simpler format.


From Source (Original Method - Now Optional)
---------------------------------------------

The original installation method with Docker and Anaconda still works but is
no longer necessary for basic demos. See the old instructions in git history
if needed.

For full Azrael stack (Clerk + Leonard + MongoDB), you'll still need:

.. code-block:: bash

   # Start auxiliary services
   docker-compose -f devtools/docker-compose-dev.yml up -d

   # Run full demos
   python demos/demo_default.py --noviewer --cubes 4,4,1


Current Status (December 2025)
==============================

✅ **Demos Working** - Physics simulations running on modern Python
✅ **Tests Passing** - Core functionality verified
✅ **No Compilation** - Pure Python implementation using PyBullet
✅ **Modern Python** - Compatible with Python 3.10+

See `QUICK_WIN.md <QUICK_WIN.md>`_ for how we got demos working in just 2 hours!


Evolution & Future Directions
=============================

**December 2025 Analysis:** This project has significant potential for evolution
into a modern multi-agent reinforcement learning platform for space robotics.

With working demos, the path forward is clear. See these documents for strategic guidance:

* `Evolution Roadmap <doc/evolution_roadmap.rst>`_ - Complete strategic vision
  and 3-year implementation plan for transforming Azrael into a leading RL platform

* `Quick Start Evolution <QUICK_START_EVOLUTION.md>`_ - Practical next steps,
  validation strategies, and immediate actions

* `Decision Matrix <EVOLUTION_DECISION_MATRIX.md>`_ - Framework for deciding
  which direction to take

* `Architecture Notes <doc/ARCHITECTURE_NOTES.md>`_ - Technical deep dive and
  modernization opportunities

**Key Opportunities:**

* Multi-agent RL platform for autonomous spacecraft
* Distributed swarm robotics testbed
* Collaborative digital twins for satellite operations
* Browser-based space physics education platform

The distributed, network-first architecture makes Azrael uniquely positioned
for these applications. No mature open-source competitors exist in this space.


Contribute to Azrael
====================

Pull requests are welcome. Please use best Python practices for documentation
and coding style (PEP8). Please add tests for bug fixes and new features -
thank you.

A rough road map of short- and medium term tasks is below (all skill levels). My
current tasks are also in a `Trello Board <https://trello.com/b/3XJRlgt9>`_.


Deployment
----------

* One click deployment (Kubernetes?) on AWS and other Clouds.
* Shrink the size of the Docker image (currently ~1GB).


Core Modules
------------

* Use the `ELK Stack <https://www.elastic.co/products>`_ for logging?
* Make `typecheck` decorator compatible with PEP484.
* Replace current annotations with PEP484 compatible ones.
* Log and visualise profiling information for all major functions calls.
* Expose event system via Tornado.
* Build a sensible grid engine.
* Better (and possibly faster) data validation and/or format, eg `JSON schema
  <http://json-schema.org>`_ or `CapNProto <https://capnproto.org/>`_.
* Wrap more of Bullet's collision shapes (convex and capsule in particular).


Rendering Frontend
-------------------

* New and clean Qt/JS viewers; current ones have become a (still working) mess.
* Support basic light and shadow effects to better gauge depth.
* Clients currently have to poll Azrael; how could a push based system work?


Accessibility
-------------

* Reformat existing doc-strings to `Google Style Docstring
  <https://pypi.python.org/pypi/sphinxcontrib-napoleon>`_.
* Spell check and proof read doc-strings.
* Homepage for Azrael.
* New/better 3D models.
* Import 3D models directly from Blender (see `demo_blender`).
* Support `ThreeJS Model Format 3/4 <https://github.com/mrdoob/three.js/wiki>`_.
* More and better demos.


License
=======

Azrael itself (everything under `azrael/`) is licensed under the terms of the
AGPL v3.

All other files, including `pyazrael` and the demos, are Apache v2 licensed.
