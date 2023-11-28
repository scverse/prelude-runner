|pypi| |tests|

.. |pypi| image:: https://img.shields.io/pypi/v/prelude-runner
   :target: https://pypi.org/project/prelude-runner/
   :alt: PyPI Version

.. |tests| image:: https://github.com/scverse/prelude-runner/actions/workflows/test.yml/badge.svg
   :target: https://github.com/scverse/prelude-runner/actions/workflows/test.yml
   :alt: Unit Tests

prelude-runner
==============

1. Create a `prelude_cell.py` and `prelude_notebook.py` in a directory.
2. Running your notebooks with the prelude runner to execute the prelude code
   before each notebook / cell.

.. code:: bash

   echo 'import random; random.seed(0)' >./config/prelude_cell.py
   echo '' >./config/prelude_notebook.py
   prelude-runner --preludes=./config ./notebooks
