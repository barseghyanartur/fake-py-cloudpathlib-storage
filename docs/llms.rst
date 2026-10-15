Project source-tree
===================

Below is the layout of the project (to 10 levels), followed by
the contents of each key file.

.. code-block:: text
   :caption: Project directory layout

   fake-py-cloudpathlib-storage/
   ├── docs
   │   ├── conf.py
   │   ├── contributor_guidelines.rst
   │   ├── fakepy.cloudpathlib_storage.rst
   │   ├── fakepy.cloudpathlib_storage.tests.rst
   │   ├── fakepy.rst
   │   ├── index.rst
   │   ├── llms.rst
   │   └── package.rst
   ├── fakepy
   │   └── cloudpathlib_storage
   │       ├── tests
   │       │   ├── __init__.py
   │       │   ├── data.py
   │       │   ├── test_cloudpathlib.py
   │       │   └── test_storages.py
   │       ├── __init__.py
   │       ├── aws_s3.py
   │       ├── azure_cloud_storage.py
   │       ├── cloud.py
   │       └── google_cloud_storage.py
   ├── conftest.py
   ├── CONTRIBUTING.rst
   ├── Makefile
   ├── pyproject.toml
   ├── README.rst
   └── uv.lock

README.rst
----------

.. literalinclude:: ../README.rst
   :language: rst
   :caption: README.rst

CONTRIBUTING.rst
----------------

.. literalinclude:: ../CONTRIBUTING.rst
   :language: rst
   :caption: CONTRIBUTING.rst

conftest.py
-----------

.. literalinclude:: ../conftest.py
   :language: python
   :caption: conftest.py

docs/conf.py
------------

.. literalinclude:: conf.py
   :language: python
   :caption: docs/conf.py

docs/contributor_guidelines.rst
-------------------------------

.. literalinclude:: contributor_guidelines.rst
   :language: rst
   :caption: docs/contributor_guidelines.rst

docs/fakepy.cloudpathlib_storage.rst
------------------------------------

.. literalinclude:: fakepy.cloudpathlib_storage.rst
   :language: rst
   :caption: docs/fakepy.cloudpathlib_storage.rst

docs/fakepy.cloudpathlib_storage.tests.rst
------------------------------------------

.. literalinclude:: fakepy.cloudpathlib_storage.tests.rst
   :language: rst
   :caption: docs/fakepy.cloudpathlib_storage.tests.rst

docs/fakepy.rst
---------------

.. literalinclude:: fakepy.rst
   :language: rst
   :caption: docs/fakepy.rst

docs/index.rst
--------------

.. literalinclude:: index.rst
   :language: rst
   :caption: docs/index.rst

docs/llms.rst
-------------

.. literalinclude:: llms.rst
   :language: rst
   :caption: docs/llms.rst

docs/package.rst
----------------

.. literalinclude:: package.rst
   :language: rst
   :caption: docs/package.rst

fakepy/cloudpathlib_storage/__init__.py
---------------------------------------

.. literalinclude:: ../fakepy/cloudpathlib_storage/__init__.py
   :language: python
   :caption: fakepy/cloudpathlib_storage/__init__.py

fakepy/cloudpathlib_storage/aws_s3.py
-------------------------------------

.. literalinclude:: ../fakepy/cloudpathlib_storage/aws_s3.py
   :language: python
   :caption: fakepy/cloudpathlib_storage/aws_s3.py

fakepy/cloudpathlib_storage/azure_cloud_storage.py
--------------------------------------------------

.. literalinclude:: ../fakepy/cloudpathlib_storage/azure_cloud_storage.py
   :language: python
   :caption: fakepy/cloudpathlib_storage/azure_cloud_storage.py

fakepy/cloudpathlib_storage/cloud.py
------------------------------------

.. literalinclude:: ../fakepy/cloudpathlib_storage/cloud.py
   :language: python
   :caption: fakepy/cloudpathlib_storage/cloud.py

fakepy/cloudpathlib_storage/google_cloud_storage.py
---------------------------------------------------

.. literalinclude:: ../fakepy/cloudpathlib_storage/google_cloud_storage.py
   :language: python
   :caption: fakepy/cloudpathlib_storage/google_cloud_storage.py

fakepy/cloudpathlib_storage/tests/__init__.py
---------------------------------------------

.. literalinclude:: ../fakepy/cloudpathlib_storage/tests/__init__.py
   :language: python
   :caption: fakepy/cloudpathlib_storage/tests/__init__.py

fakepy/cloudpathlib_storage/tests/data.py
-----------------------------------------

.. literalinclude:: ../fakepy/cloudpathlib_storage/tests/data.py
   :language: python
   :caption: fakepy/cloudpathlib_storage/tests/data.py

fakepy/cloudpathlib_storage/tests/test_cloudpathlib.py
------------------------------------------------------

.. literalinclude:: ../fakepy/cloudpathlib_storage/tests/test_cloudpathlib.py
   :language: python
   :caption: fakepy/cloudpathlib_storage/tests/test_cloudpathlib.py

fakepy/cloudpathlib_storage/tests/test_storages.py
--------------------------------------------------

.. literalinclude:: ../fakepy/cloudpathlib_storage/tests/test_storages.py
   :language: python
   :caption: fakepy/cloudpathlib_storage/tests/test_storages.py

pyproject.toml
--------------

.. literalinclude:: ../pyproject.toml
   :language: toml
   :caption: pyproject.toml
