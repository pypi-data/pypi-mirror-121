.. image:: graphics/pydoni_logo_with_text.png

.. role:: raw-html(raw)
    :format: html

A Python module for custom-built tools designed and maintained by Andoni Sooklaris.

:raw-html:`<br />`

.. image:: https://img.shields.io/pypi/v/pydoni.svg
        :target: https://pypi.python.org/pypi/pydoni

:raw-html:`<br />`

🏁 Getting Started
==================

``pydoni`` is a multi-functional Python package that contains tools for handling OS/system and Python object operations, verbosity, shell command wrappers, prompting for user interactivity via commandline, Postgres database interaction and webscraping utilities.

🧿 Prerequisites
----------------

* ``pip``

⚙️ Installation
---------------

.. code-block:: bash

   pip install pydoni

It really is that simple ✨

🌈 Releasing
------------

``pydoni`` utilizes `versioneer <https://pypi.org/project/versioneer/>`_ for versioning. This requires the ``versioneer.py`` in the project's top-level directory, as well as some lines in the package's ``setup.cfg`` and ``__init__.py``.

1. Make your changes locally and push to ``develop`` or a different feature branch.

2. Tag the new version. This will be the version of the package once publication to PyPi is complete.

   .. code-block:: bash

      git tag {major}.{minor}.{patch}

3. Publish to PyPi.

   .. code-block:: bash

      rm -rf ./dist && python3 setup.py sdist && twine upload -r pypi dist/*

4. Install the new version of ``pydoni``.

   .. code-block:: bash

      pip install pydoni=={major}.{minor}.{patch}

5. Create a `pull request <https://github.com/tsouchlarakis/pydoni/pulls>`_.

⚓️ Changelog
=============

See `changelog <CHANGELOG.rst>`_.

📜 License
==========

See `license <LICENSE>`_.

.. raw:: html

🙏 Credits
----------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage