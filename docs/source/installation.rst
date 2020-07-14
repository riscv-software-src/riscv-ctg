.. See LICENSE.incore for details

.. highlight:: shell

============
Installation
============

Install Python
==============

.. tabs::

   .. tab:: Ubuntu


      Ubuntu 17.10 and 18.04 by default come with python-3.6.9 which is sufficient for using riscv-config.
      
      If you are are Ubuntu 16.10 and 17.04 you can directly install python3.6 using the Universe
      repository
      
      .. code-block:: shell-session

        $ sudo apt-get install python3.6
        $ pip3 install --upgrade pip
      
      If you are using Ubuntu 14.04 or 16.04 you need to get python3.6 from a Personal Package Archive 
      (PPA)
      
      .. code-block:: shell-session

        $ sudo add-apt-repository ppa:deadsnakes/ppa
        $ sudo apt-get update
        $ sudo apt-get install python3.6 -y 
        $ pip3 install --upgrade pip
      
      You should now have 2 binaries: ``python3`` and ``pip3`` available in your $PATH. 
      You can check the versions as below
      
      .. code-block:: shell-session

        $ python3 --version
        Python 3.6.9
        $ pip3 --version
        pip 20.1 from <user-path>.local/lib/python3.6/site-packages/pip (python 3.6)

   .. tab:: CentOS7

      The CentOS 7 Linux distribution includes Python 2 by default. However, as of CentOS 7.7, Python 3 
      is available in the base package repository which can be installed using the following commands
      
      .. code-block:: shell-session

        $ sudo yum update -y
        $ sudo yum install -y python3
        $ pip3 install --upgrade pip
      
      For versions prior to 7.7 you can install python3.6 using third-party repositories, such as the 
      IUS repository
      
      .. code-block:: shell-session

        $ sudo yum update -y
        $ sudo yum install yum-utils
        $ sudo yum install https://centos7.iuscommunity.org/ius-release.rpm
        $ sudo yum install python36u
        $ pip3 install --upgrade pip
      
      You can check the versions
      
      .. code-block:: shell-session

        $ python3 --version
        Python 3.6.8
        $ pip --version
        pip 20.1 from <user-path>.local/lib/python3.6/site-packages/pip (python 3.6)

Install RISC-V CTG (From Git)
=============================================================

To install RISC-V Compliance Test Generator, run this command in your terminal:

.. code-block:: console

    $ python -m pip install git+https://gitlab.com/incoresemi/riscv-compliance/riscv_ctg.git

This is the preferred method to install RISC-V Compliance Test Generator, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

Install RISC-V CTG (via pip)
=====================================================

.. note:: If you are using `pyenv` as mentioned above, make sure to enable that environment before
 performing the following steps.

.. code-block:: bash

  $ pip3 install riscv_ctg

To update an already installed version of RISCOF to the latest version:

.. code-block:: bash

  $ pip3 install -U riscv_ctg

To checkout a specific version of riscv_ctg:

.. code-block:: bash

  $ pip3 install riscv_ctg==1.x.x

Install CTG for Dev
===================

The sources for RISC-V Compliance Test Generator can be downloaded from the `GitLab repo`_.

You can clone the repository:

.. code-block:: console

    $ git clone https://gitlab.com/incoresemi/riscv-compliance/riscv_ctg


Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Gitlab repo: https://gitlab.com/incoresemi/riscv-compliance/riscv_ctg
