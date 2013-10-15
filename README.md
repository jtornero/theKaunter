TheKaunter
==========

(c) Jorge Tornero Núñez, http://imasdemase.com

What is it?
===========

TheKaunter is a multi-category, configurable differential counter.

Differential counters are used in fields like haematology, for counting blood cells; in marine science, for instance, they are used for counting different kinds of plankton organisms (eggs, larvae...), among many other uses.

Classic (mechanical) differential counters have up to 10 individual counters and one totalizer. TheKaunter features the possibility of having several categories or groups of counters with one totalizer by category and, unlike mechanical counters, TheKaunter makes possible to reset individual counters and decrease the count.

![Alt text](./screenshot.png "Screenshot of TheKaunter")

License
=======
TheKaunter ir released under GPL V3.0 license.

Features
=============
- No theorical limit of counters/categories. However, up to a total of 36 individual counters is recommended, due to limitations in keyboard and desktop/GUI size.
- Counters can be increased, decreased as well as individually reset. 
- One totalizer for category/group of counters.
- Category/counter names as well as key bindings are shown in the GUI for ease of use.
- Results are exportable to CSV as well as to the clipboard.
- Silent... no more crank, lever, sounds in your lab...
- English as well as Spanish translations for the GUI are provided.

Future enhancements
===================
- If you still like sound feedback from the counter... you'll get it.
- Descriptive image for each counter.
- Prettier CSV/clipboard export.
- Export to SQLite database .
- Connection to custom OpenHardware keyboard based on Arduino.

Dependencies
============
As of version 1.0.0, TheKaunter depends on:
- PyQt4
- ConfigParser
