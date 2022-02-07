.. See LICENSE.incore for details

.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/riscv-software-src/riscv-ctg/issues/.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/riscv-software-src/riscv-ctg/issues/.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `riscv_ctg` for local development.

1. Fork the `riscv_ctg` repo on GitHub.
2. Clone your fork locally::

    $ git clone  https://github.com/riscv-software-src/riscv-ctg.git

3. Create an issue and WIP merge request that creates a working branch for you::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

4. When you're done making changes, check that your changes pass pytest
   tests, including testing other Python versions with tox::

    $ cd tests
    $ pytest test_riscv_ctg.py -v

5. Commit your changes and push your branch to GitLab::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

6. Submit a merge request through the GitHub website.

Merge Request Guidelines
----------------------------

Before you submit a merge request, check that it meets these guidelines:

1. The merge request should include tests.
2. If the merge request adds functionality, the docs should be updated. 
3. The merge request should work for Python 3.6, 3.7 and 3.8, and for PyPy. 
   and make sure that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests::

    $ pytest tests.test_riscv_ctg


Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed.
Then run::

$ bumpversion --no-tag --config-file setup.cfg patch  # possible: major / minor / patch
$ git push origin name-of-your-branch

