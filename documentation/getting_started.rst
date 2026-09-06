Getting Started
===============

To start using KivyDK, you must first
`install the Kivy framework <https://kivy.org/doc/stable/gettingstarted/installation.html>`_
on your system. Once Kivy is installed, you can proceed to install KivyDK.

.. caution::
    KivyDK depends on Kivy. Before using KivyDK, you should already be familiar
    `how to work with Kivy <https://kivy.org/doc/stable/>`_.

****

Installation
------------

.. tab-set::

    .. tab-item:: PyPI

        .. code-block:: doscon

            C:\> pip install kivydk

        The command above installs the most recent stable version of KivyDK from
        `PyPI <https://pypi.org/project/kivydk>`_.

    .. tab-item:: GitHub

        If you want to install the development version from `GitHub <https://github.com/kmcasi/kivydk>`_,
        use the ZIP archive:

        .. code-block:: doscon

            C:\> pip install https://github.com/kmcasi/KivyDK/archive/master.zip

First KivyDK application
------------------------

.. literalinclude:: {{ dir_examples }}/getting_started.py
    :language: python
    :linenos:

This small example demonstrates the hover and click system.
Each time the button is clicked, a message similar to the following will appear in the console:

.. code-block:: console
    :class: no-copybutton
    :caption: Terminal output

    Button clicked 01 times
    Button clicked 02 times
    Button clicked 03 times
