Release history and notes
=========================
.. Internal references

.. _cloudpathlib: https://cloudpathlib.drivendata.org/
.. _fake-py-pathy-storage: https://github.com/barseghyanartur/fake-py-pathy-storage
.. _pytest-codeblock: https://github.com/barseghyanartur/pytest-codeblock
.. _uv: https://docs.astral.sh/uv/

`Sequence based identifiers
<http://en.wikipedia.org/wiki/Software_versioning#Sequence-based_identifiers>`_
are used for versioning (schema follows below):

.. code-block:: text

    major.minor[.revision]

- It's always safe to upgrade within the same minor version (for example, from
  0.3 to 0.3.4).
- Minor and major version changes might be backwards incompatible. Read the
  release notes carefully before upgrading (for example, when upgrading from
  0.3.4 to 0.4).
- All backwards incompatible changes are mentioned in this document.

0.1.1
-----
2026-10-16

- ``relpath()`` now returns POSIX-style paths on every OS. Previously,
  ``LocalFileSystemStorage`` returned backslash-separated paths on Windows.

0.1.0
-----
2026-10-16

- Initial beta release. Port of `fake-py-pathy-storage`_ 0.1.7 to
  `cloudpathlib`_ 0.26.
- Each storage owns its client (no global credentials state). Optional
  ``client`` and ``client_kwargs`` arguments.
- Local file system storage is based on ``pathlib.Path``. Azure uses the
  ``az://`` scheme.
- Cloud buckets/containers must already exist.
- Documentation code blocks are tested with `pytest-codeblock`_.
- Project uses `uv`_ for dependency management, building and running things.
