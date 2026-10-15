============================
fake-py-cloudpathlib-storage
============================
.. External references

.. _fake.py: https://fakepy.readthedocs.io/
.. _cloudpathlib: https://cloudpathlib.drivendata.org/
.. _faker-file: https://faker-file.readthedocs.io/
.. _fake-py-pathy-storage: https://github.com/barseghyanartur/fake-py-pathy-storage/
.. _uv: https://docs.astral.sh/uv/

.. Internal references

.. _fake-py-cloudpathlib-storage: https://github.com/barseghyanartur/fake-py-cloudpathlib-storage/
.. _Read the Docs: http://fake-py-cloudpathlib-storage.readthedocs.io/
.. _Contributor guidelines: https://fake-py-cloudpathlib-storage.readthedocs.io/en/latest/contributor_guidelines.html

`cloudpathlib`_ storage for `fake.py`_.

.. image:: https://img.shields.io/pypi/v/fake-py-cloudpathlib-storage.svg
   :target: https://pypi.python.org/pypi/fake-py-cloudpathlib-storage
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/fake-py-cloudpathlib-storage.svg
    :target: https://pypi.python.org/pypi/fake-py-cloudpathlib-storage/
    :alt: Supported Python versions

.. image:: https://github.com/barseghyanartur/fake-py-cloudpathlib-storage/actions/workflows/test.yml/badge.svg?branch=main
   :target: https://github.com/barseghyanartur/fake-py-cloudpathlib-storage/actions
   :alt: Build Status

.. image:: https://readthedocs.org/projects/fake-py-cloudpathlib-storage/badge/?version=latest
    :target: http://fake-py-cloudpathlib-storage.readthedocs.io
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/docs-llms.txt-blue
    :target: http://fake-py-cloudpathlib-storage.readthedocs.io/en/latest/llms.txt
    :alt: llms.txt - documentation for LLMs

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/barseghyanartur/fake-py-cloudpathlib-storage/#License
   :alt: MIT

.. image:: https://coveralls.io/repos/github/barseghyanartur/fake-py-cloudpathlib-storage/badge.svg?branch=main&service=github
    :target: https://coveralls.io/github/barseghyanartur/fake-py-cloudpathlib-storage?branch=main
    :alt: Coverage

`fake-py-cloudpathlib-storage`_ is a `cloudpathlib`_ storage integration for
`fake.py`_ - a standalone, portable library designed for generating various
random data types for testing.

It is a sibling of (and a drop-in-minded successor to)
`fake-py-pathy-storage`_, built on the actively maintained `cloudpathlib`_.

Features
========
- Cloud storages integration includes support for AWS S3, Google Cloud Storage
  and Azure Blob Storage.
- Local file system storage with the same interface.
- Each storage owns its own client: no global credentials state.
- Works with `cloudpathlib`_'s local (mocked) clients for offline tests.

Prerequisites
=============
Python 3.10+

Installation
============

With `uv`_:

.. code-block:: sh

    uv add fake-py-cloudpathlib-storage

Or with pip:

.. code-block:: sh

    pip install fake-py-cloudpathlib-storage

Install the extras for the providers you need (``s3``, ``gcs``, ``azure`` or
``all``):

.. code-block:: sh

    uv add "fake-py-cloudpathlib-storage[s3]"
    uv add "fake-py-cloudpathlib-storage[gcs]"
    uv add "fake-py-cloudpathlib-storage[azure]"
    uv add "fake-py-cloudpathlib-storage[all]"

Documentation
=============
- Documentation is available on `Read the Docs`_.
- For guidelines on contributing check the `Contributor guidelines`_.

Usage
=====
Local cloud-alike file system storage
-------------------------------------
.. code-block:: python
    :name: test_cloudpathlib_file_system_storage

    from fake import FAKER
    from fakepy.cloudpathlib_storage.cloud import LocalFileSystemStorage

    STORAGE = LocalFileSystemStorage(
        bucket_name="bucket_name",
        root_path="tmp",  # Optional
        rel_path="sub-tmp",  # Optional
    )

    pdf_file = FAKER.pdf_file(storage=STORAGE)

    STORAGE.exists(pdf_file)

``LocalFileSystemStorage`` uses ``pathlib.Path``, since `cloudpathlib`_ has
no ``file://`` backend. Files are stored under ``local_storage_dir``
(defaults to the system temporary directory).
``CloudpathlibFileSystemStorage`` is an alias.
``abspath()`` returns a standard absolute ``file:///`` URI.

AWS S3
------
.. code-block:: python
    :name: test_cloudpathlib_aws_s3_storage

    from fake import FAKER
    from fakepy.cloudpathlib_storage.aws_s3 import AWSS3Storage

    STORAGE = AWSS3Storage(
        bucket_name="bucket_name",
        root_path="tmp",  # Optional
        rel_path="sub-tmp",  # Optional
        # Credentials are optional too. If your AWS credentials are properly
        # set in the ~/.aws/credentials, you don't need to send them
        # explicitly.
        credentials={
            "key_id": "YOUR KEY ID",
            "key_secret": "YOUR KEY SECRET"
        },
    )

    pdf_file = FAKER.pdf_file(storage=STORAGE)

    STORAGE.exists(pdf_file)

Additional ``S3Client`` options (session tokens, profiles, custom endpoints,
cache settings, etc.) go in ``client_kwargs``.

Google Cloud Storage
--------------------
.. code-block:: python
    :name: test_cloudpathlib_google_cloud_storage

    from fake import FAKER
    from fakepy.cloudpathlib_storage.google_cloud_storage import (
        GoogleCloudStorage,
    )

    STORAGE = GoogleCloudStorage(
        bucket_name="bucket_name",
        root_path="tmp",  # Optional
        rel_path="sub-tmp",  # Optional
        # Optional. Omit to use application default credentials.
        credentials={"json_file_path": "/path/to/service-account.json"},
    )

    pdf_file = FAKER.pdf_file(storage=STORAGE)

    STORAGE.exists(pdf_file)

``json_file_path`` maps to ``GSClient``'s ``application_credentials``.

Azure Cloud Storage
-------------------
.. code-block:: python
    :name: test_cloudpathlib_azure_cloud_storage

    from fake import FAKER
    from fakepy.cloudpathlib_storage.azure_cloud_storage import (
        AzureCloudStorage,
    )

    STORAGE = AzureCloudStorage(
        bucket_name="bucket_name",
        root_path="tmp",  # Optional
        rel_path="sub-tmp",  # Optional
        credentials={"connection_string": "YOUR CONNECTION STRING"},
    )

    pdf_file = FAKER.pdf_file(storage=STORAGE)

    STORAGE.exists(pdf_file)

Azure paths use `cloudpathlib`_'s ``az://`` scheme. Other ``AzureBlobClient``
options may be passed through ``client_kwargs``.

Shared API and path semantics
-----------------------------
.. code-block:: python
    :name: test_cloudpathlib_shared_api

    from fakepy.cloudpathlib_storage.cloud import LocalFileSystemStorage

    storage = LocalFileSystemStorage(bucket_name="bucket_name")

    filename = storage.generate_filename(extension="txt", prefix="sample_")
    storage.write_text(filename, "Lorem ipsum", encoding="utf-8")
    storage.write_bytes(filename, b"Lorem ipsum")
    assert storage.exists(filename)
    relative_name = storage.relpath(filename)
    absolute_uri = storage.abspath(filename)
    storage.unlink(filename)

- Generated paths are ``bucket/root_path/rel_path/basename.extension``.
- String relative filenames resolve against ``bucket/root_path`` (not
  ``bucket/root_path/rel_path``). Use ``relpath(filename)`` to obtain a
  round-trip relative name.
- ``None`` or empty ``root_path``/``rel_path`` omit that component.
- Path objects, their string representations and provider URIs are accepted.
- ``write_text`` returns characters written; ``write_bytes`` returns bytes
  written.
- An empty extension raises ``ValueError``.
- Unlinking a missing file raises ``FileNotFoundError``, consistently across
  providers.

Offline cloud tests
-------------------
Pass a `cloudpathlib`_ local client to test without touching real clouds:

.. code-block:: python
    :name: test_cloudpathlib_offline_s3

    from cloudpathlib.local import LocalS3Client
    from fakepy.cloudpathlib_storage.aws_s3 import AWSS3Storage

    client = LocalS3Client(local_storage_dir="/tmp/mock-cloud")
    storage = AWSS3Storage("example", client=client)
    filename = storage.generate_filename("txt", basename="sample")
    storage.write_text(filename, "offline")
    assert filename.read_text() == "offline"
    storage.unlink(filename)

``LocalGSClient`` and ``LocalAzureBlobClient`` work the same way. The latter
requires a non-empty dummy ``connection_string``.

Migrating from fake-py-pathy-storage
====================================
- Package: ``fake-py-cloudpathlib-storage``.
- Imports: ``fakepy.cloudpathlib_storage`` instead of
  ``fakepy.pathy_storage``.
- Same ``CloudStorage``, ``LocalFileSystemStorage``, ``AWSS3Storage``,
  ``GoogleCloudStorage`` and ``AzureCloudStorage`` classes.
  ``PathyFileSystemStorage`` becomes ``CloudpathlibFileSystemStorage``.
- Cloud paths are `cloudpathlib`_ ``CloudPath`` subclasses; local paths are
  ``pathlib.Path``.
- Each storage owns its client. Authentication no longer changes global
  provider settings. ``client`` and ``credentials``/``client_kwargs`` are
  mutually exclusive.
- Cloud buckets/containers must already exist. Initialization does not
  provision resources or perform network existence checks. Local bucket
  directories are still created automatically.
- Azure uses the ``az://`` scheme instead of Pathy's ``azure://``.
- Existing absolute path objects remain accepted, as in the original.
  This is not a sandbox for untrusted filenames.

Tests
=====
Project uses `uv`_ for dependency management and running things.

.. code-block:: sh

    uv sync --all-extras
    uv run pytest

Or, using the ``Makefile``:

.. code-block:: sh

    make install
    make test

Tests use isolated temporary directories and `cloudpathlib`_'s local clients
for AWS S3, Google Cloud Storage and Azure, so no real cloud accounts are
needed. Code blocks in the documentation are tested too.

Writing documentation
=====================

Keep the following hierarchy.

.. code-block:: text

    =====
    title
    =====

    header
    ======

    sub-header
    ----------

    sub-sub-header
    ~~~~~~~~~~~~~~

    sub-sub-sub-header
    ^^^^^^^^^^^^^^^^^^

    sub-sub-sub-sub-header
    ++++++++++++++++++++++

    sub-sub-sub-sub-sub-header
    **************************

License
=======

MIT

Support
=======
For security issues contact me at the e-mail given in the `Author`_ section.

For overall issues, go to `GitHub <https://github.com/barseghyanartur/fake-py-cloudpathlib-storage/issues>`_.

Author
======

Artur Barseghyan <artur.barseghyan@gmail.com>
