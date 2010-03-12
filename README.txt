This is a "bootstrap" package that is used to generate new deployments
of the OpenCore software stack, the web-based group collaboration
toolkit that powers `coactivate.org <http://www.coactivate.org/>`_ and
other websites.

Usage
=====

This package provides two commands:

 * ``new-opencore-site`` will create a directory structure useful for
   managing an ongoing OpenCore site deployment.  Run this once, when
   you are first deploying your OpenCore site.

   It will place a file `opencore.conf` in the generated directory.
   You can edit the configuration in this file; it will be used by
   the ``rebuild-opencore`` command to determine what profile to
   build by default; what portset to configure the stack on; and
   other build parameters that are useful to manage on a per-site basis.

 * ``rebuild-opencore`` will initiate a new Fassembler build for your
   OpenCore site, using your desired configuration.


User / Developer Resources
==========================

* `The Opencore Project <http://www.coactivate.org/projects/opencore>`_

* `#opencore <irc://irc.freenode.net/opencore>`
