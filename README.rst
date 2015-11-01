=========
 yaghurl
=========

Yet another github URL tool. Pronounced like one is hurling a yag.

My goal for this is to hook up my emacs so that a keystroke will insert
a github comment reference to the current file, line, commit, and
branch. As much functionality as possible should be pushed into the
``yaghurl.py`` python script, for reuse in other editors or from the
shell. Editor integrations should live in ``./contrib``.

Installation
============

.. code:: bash

   $ pip install yaghurl

Examples
========

Commandline Examples
--------------------

Refer to a range of lines in a file. For example, if you were in a clone
of this repository, you could do:

.. code:: bash

   $ yaghurl ./yaghurl/main.py 11 15
   [``./yaghurl/main.py`` L11-L15 at ``87f81660``](https://github.com//nejucomo/yaghurl/blob/87f816605bd4c9fc5669161015c7482cad5009cb/./yaghurl/main.py#L11-L15) ([latest on branch ``master``](https://github.com//nejucomo/yaghurl/blob/master/./yaghurl/main.py#L11-L15))

