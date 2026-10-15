Contributor guidelines
======================

.. _documentation: https://fake-py-cloudpathlib-storage.readthedocs.io/#writing-documentation
.. _testing: https://fake-py-cloudpathlib-storage.readthedocs.io/#testing
.. _pre-commit: https://pre-commit.com/#installation
.. _uv: https://docs.astral.sh/uv/
.. _doc8: https://doc8.readthedocs.io/
.. _ruff: https://docs.astral.sh/ruff/
.. _pydoclint: https://jsh9.github.io/pydoclint/
.. _detect-secrets: https://github.com/Yelp/detect-secrets
.. _issues: https://github.com/barseghyanartur/fake-py-cloudpathlib-storage/issues
.. _discussions: https://github.com/barseghyanartur/fake-py-cloudpathlib-storage/discussions
.. _pull request: https://github.com/barseghyanartur/fake-py-cloudpathlib-storage/pulls
.. _support: https://fake-py-cloudpathlib-storage.readthedocs.io/#support
.. _installation: https://fake-py-cloudpathlib-storage.readthedocs.io/#installation
.. _features: https://fake-py-cloudpathlib-storage.readthedocs.io/#features
.. _prerequisites: https://fake-py-cloudpathlib-storage.readthedocs.io/#prerequisites

Developer prerequisites
-----------------------
uv
~~
The project uses `uv`_ for dependency management, installation and running
things. Refer to `uv`_ for installation instructions.

pre-commit
~~~~~~~~~~
Refer to `pre-commit`_ for more information. It's installed as a development
dependency.

TL;DR:

.. code-block:: sh

    make install  # uv sync --all-extras --all-groups
    make pre-commit-install  # uv run pre-commit install

Installing `pre-commit`_ will ensure you adhere to the project code quality
standards.

Code standards
--------------
`ruff`_, `doc8`_, `pydoclint`_ and `detect-secrets`_ will be automatically
triggered by `pre-commit`_. Still, if you want to run checks manually:

.. code-block:: sh

    make pre-commit
    make doc8
    make ruff
    make mypy

Requirements
------------
Dependencies are declared in ``pyproject.toml`` (development tools live in
dependency groups) and locked in ``uv.lock``.

.. code-block:: sh

    make lock  # uv lock
    make lock-upgrade  # uv lock --upgrade

Virtual environment
-------------------
`uv`_ manages the virtual environment (``.venv``) for you.

TL;DR:

.. code-block:: sh

    uv sync --all-extras

Documentation
-------------
Check `documentation`_.

Testing
-------
Check `testing`_.

If you introduce changes or fixes, make sure to test them locally using
all supported Python versions:

.. code-block:: sh

    uv run --python 3.10 pytest
    uv run --python 3.14 pytest

In any case, GitHub Actions will catch potential errors, but testing locally
speeds things up.

For a quick test of the package and all examples, use the following `Makefile`
command:

.. code-block:: sh

    make test-all

Pull requests
-------------
You can contribute to the project by making a `pull request`_.

For example:

- To fix documentation typos.
- To improve documentation (for instance, to add new recipe or fix
  an existing recipe that doesn't seem to work).
- To introduce a new feature (for instance, add support for a non-supported
  file type).

**General list to go through:**

- Does your change require documentation update?
- Does your change require update to tests?

**When fixing bugs (in addition to the general list):**

- Make sure to add regression tests.

**When adding a new feature (in addition to the general list):**

- Make sure to update the documentation.

Questions
---------
Questions can be asked on GitHub `discussions`_.

Issues
------
For reporting a bug or filing a feature request use GitHub `issues`_.

**Do not report security issues on GitHub**. Check the `support`_ section.
