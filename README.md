TheKaunter
==========

(c) 2013, 2104 Jorge Tornero Núñez, http://imasdemase.com

What is it?
===========

TheKaunter is a **multi-category, configurable differential counter**.

Differential counters are used in fields like haematology, for counting blood cells; in marine science, for instance, they are used for counting different kinds of plankton organisms (eggs, larvae...), among many other uses.

Classic (mechanical) differential counters have up to 10 individual counters and one totalizer. TheKaunter features the possibility of having several categories or groups of counters with one totalizer by category and, unlike mechanical counters, TheKaunter makes possible to reset individual counters and decrease the count.

![Alt text](./screenshot.png "Screenshot of TheKaunter")

License
=======
TheKaunter ir **released under GPL V3.0 license.** For further information please see http://www.gnu.org/licenses/gpl-3.0.html

Donations
=========
No donations/fees are required for the use of this software, but if you want to reward me in some way, you can send me a postcard from where you live. It will be nice to show to my kid!! In that case, you can mail me to get my postal address.
If you have a happy pocket, I'm sure you can help people around you, or donate some to your preferred charity/NGO. 

Citation
========
If you use TheKaunter in a scientific research work, you can cite it as:


Features
=============
- **No theoretical limit of counters/categories**. However, up to a total of 36 individual counters is recommended, due to limitations in keyboard and desktop/GUI size.
- **Counters can be increased, decreased as well as individually reset.**
- One **totalizer for category/group** of counters.
- **User configurable section header** color as well as counter background
- User configurable **counter descriptive images.**
- **Category/counter names as well as key bindings are shown in the GUI** for ease of use.
- **Results are exportable** to CSV as well as to the clipboard.
- **Silent...** no more crank, lever, sounds in your lab...
- English as well as Spanish **translations for the GUI are provided.**

Usage
=====
Once TheKaunter is properly configured (**see theKaunter.conf for details about configuration and usage**), you can start counting like you were using a conventional, mechanical counter. Just pressing the key bounded to each class, you increase the count. But TheKaunter makes possible other fancy operations, like:

**Count decrease:** Press Alt+Bound key
**Individual counter reset:** Ctrl+Bound Key
**Total reset:** Ctrl+Shift+R

TheKaunter, as stated before, makes use of a configuration file (see below) to properly arrange and set counters and key bindings. See the section about it below and the file theKaunter.conf to know about how to create your own configuration files. You can import them into TheKaunter through the menu *Options -> Load Configuration File*

Future enhancements
===================
- Prettier CSV/clipboard export.
- Excel export with fancy headers and all.
- Better configuration file validation.
- Export to SQLite database.
- Connection to custom OpenHardware keyboard based on Arduino.

Dependencies
============
TheKaunter has been programmed under Python 2.7 and, as of version 2.0.0, TheKaunter depends on the following Python modules:

- PyQt4
- Collections
- ConfigObj

Installation from source
========================
You can install TheKaunter just by copying the source files in a folder of your choice.
Four source files are provided:

- ***TheKaunter.py:*** The source code file for TheKaunter.
- ***theKaunter.conf:*** Sample configuration file for TheKaunter. **When starting, TheKaunter will look for it in the same folder that TheKaunter.py; if not found,TheKaunter will ask for a valid configuration file.** You can modify theKaunter.conf as you wish to meet your needs, or create a new one following the instrucions provided in theKaunter.conf.
- ***theKaunter.qm:*** Translation file for TheKaunter. **It must be in the same folder that TheKaunter.py** if you want to have TheKaunter translated. By now, just Spanish translation is provided.
- ***theKaunter.ts:*** Source translation file for TheKaunter. It is not necessary for running TheKaunter, but you can edit it with the appropiate software (Qt Linguist) for having TheKaunter translated for your language, and release a new theKaunter.qm file. Please think about sharing your translations with the community.

Once all the dependencies are met,  just execute theKaunter.py.

How to configure TheKaunter
=====================
Each *[Section]* comprises one or more *[[counters]]* in which 
a key binding must be defined by the parameter *KeyBinding=key*.
Valid KeyBinding values are those in the range A-Z and 0-9.
TheKaunter is case-insensitive. Bear in mind that, despite it is
possible to define a big number of sections/counters, there are
some practical limits = key bindings (36 possible) and also screen
size (it's probably impractical to define more than 25-30 counters.
Practical limits (screen/widget size) apply also to the length of
section/counter names. However, it is possible to use multi-word
names, as shown in the example configuration file. Linebreaks have no effect.

Section Colors
---------------------
**Section colors can be defined** with the keyword *sectionColor* after [Section]
declaration. The color affects to the header of the section as well as
to the background of the line edit widgets.
For color definition, using HTML/X11 named colors is mandatory. For a complete reference,
please check http://en.wikipedia.org/wiki/Web_colors
Example: *sectionColor:lightGreen*

Counter images
-----------------------
**You can provide an image for each of the counters** with the parameter
*counterImage=path_to_counter_image*. Supported formats include jpg, png and bmp.
The software scales the images to 80 px wide, so is better to provide images
with sizes close to 80 px wide for better performance.
Example: *counterImage=./myCounterImage.png*

Comments
----------------
**You can insert comments** in the configuration file to describe each section,
counter, etc. Inline comments are allowed. 

Configuration example
---------------------------

This is a little configuration example.

    [Section1]
    sectionColor=myHTMLColor
    [[Counter1-1]]
    KeyBinding=q
    counterImage=./MyCounterImage1.png
    [[Counter1-2]]
    KeyBinding=z
    counterImage=./MyCounterImage2.png
    [Section2]
    sectionColor=myHTMLColor2
    [[Counter2-1]]
    KeyBinding=r
    counterImage=./MyCounterImage3.png

