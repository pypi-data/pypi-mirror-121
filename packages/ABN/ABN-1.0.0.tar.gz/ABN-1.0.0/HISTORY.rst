Release History
---------------

1.0.0 (2021-09-29)
++++++++++++++++++

 - Switch to setup.cfg.
 - Require Python 3.6.


0.4.2 (2018-09-06)
++++++++++++++++++

**Bug fixes**

 - Update CI testing to run on Python 3.5 (3.4 no longer available in testing
   environment).
 - Fix `acn_to_abn` for a single-digit remainder (nikicc).


0.4.0 (2018-05-01)
++++++++++++++++++

**Improvements**

 - Add GitLab continuous integration script to run tox tests.

**Bug fixes**

 - Treat an ABN with leading zero as invalid (Charley Peng).


0.3.7 (2016-08-03)
++++++++++++++++++

**Improvements**

 - Add test suite to `setup.py`. You can run with `python setup.py test`.


0.3.6 (2015-08-03)
++++++++++++++++++

**Bug fixes**

 - Enable tests for Python 2.7, 3.3 and 3.4.
