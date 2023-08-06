mrsphinxjson - Sphinx extension to include JSON-files in the documentation.
===========================================================================

Sphinx extension to include JSON-files in the documentation.

Usage
-----



License
-------

GNU AFFERO GENERAL PUBLIC LICENSE Version 3


Developer guide
---------------

Upgrade your setup tools and pip.
They are needed for development and testing only:

.. code:: bash

   pip install --upgrade setuptools pip wheel

Development steps for code changes

.. code:: bash

   git clone https://gitlab.com/anatas_ch/pyl_mrsphinxjson.git
   cd pyl_sphinxcontrib-json
   git switch develop
   pip install -r requirements_rnd.txt
   pip install -e .

`docs` folder contains the package documentantion.

.. code:: bash

   cd docs
   make clean; make html

Once you have finished your changes, please provide test case(s) and relevant documentation.
