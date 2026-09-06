:hide-toc:

KivyDK documentation
====================

Overview
--------

**KivyDK (Kivy Desktop Kit)** is a collection of desktop‑oriented widgets and behaviors built on top of the
`Kivy framework <https://kivy.org>`_, designed for cross‑platform, touch‑enabled graphical applications.

The goal of this project is to extend **Kivy** with features that feel natural on desktop environments such as
hover detection, click and double‑click handling and other interaction patterns that are not available by default.
KivyDK also provides ready‑to‑use examples and tools to make building desktop applications faster and more intuitive.

If you are looking for UI components and behaviors that feel natural on mobile platforms, we strongly recommend using
the `KivyMD framework <https://kivymd.readthedocs.io>`_ instead. While it is technically possible to combine KivyDK
with KivyMD is recommended to not do it, the goals and internal architecture of the two frameworks differ significantly.
The only aspect they truly share is that both are built on top of the Kivy framework.

.. admonition:: A quick clarification
    :class: developer

    At the moment, KivyDK is built and maintained by one developer.

    The documentation uses *"we"* and *"us"* simply to keep things future‑friendly and to leave the door open
    for anyone who may want to join the project later on.

.. attention::

    KivyDK is currently under active development and should be considered **unstable**.
    While the major version remains ``0.x``, the public API is expected to change
    frequently as features evolve and the framework matures.

    If you plan to use KivyDK in long‑term or production projects, please be aware that
    breaking changes may occur without deprecation periods. Use caution and track updates
    closely when upgrading between versions.

~~~~

Contents
--------

.. include:: contents.rst.inc
