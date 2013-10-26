#!/usr/bin/env python

# TheKaunter. A versatile differential counter.
# 
# Copyright 2013 Jorge Tornero Nunez http://imasdemase.com
# 
# This file is part of TheKaunter, V2.0.0
# 
# TheKaunter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# TheKaunter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with TheKaunter.  If not, see <http://www.gnu.org/licenses/>.

import sys
import configobj as cp
import collections
from PyQt4 import QtGui,QtCore

class cellCounter(QtGui.QWidget):
    """
    Main Widget for TheKaunter. The parameter configFile defaults to
    theKaunter.conf in the same folder than theKaunter executable.
    """
    
    counterChanged = QtCore.pyqtSignal()
    validSectionParameters = ['sectionColor']
    validCounterParameters = ['KeyBinding','counterImage']
  
    def __init__(self,parent = None, configFile = './theKaunter.conf'):

        QtGui.QWidget.__init__(self,parent)
        
        # Checks for correct configuration file. It mostly checks
        # if the file can be loaded.
        # TODO: A real configuration validator
        
        try:
            
            self.configuration = cp.ConfigObj(configFile,file_error = True,
                                              raise_errors = True)
            
        except cp.ConfigObjError, error:
            
            while True:
                if self.configurationError(self.tr("""Configuration file error:<br><br>%s
                           <br>%s<br>
                           Please check your file and try again."""
                   %(self.tr(error.message), self.tr(error.line)))) == 1:
                    break
            return
        
        except IOError:
            
            while True:
                if self.configurationError(self.tr("Configuration file not found")) == 1:
                    break
            return
        
        # MenuBar definition
        
        self.menu = QtGui.QMenuBar(self)
        self.options = self.menu.addMenu(self.tr("&Options"))
        self.openConfigAction = self.options.addAction(self.tr("&Load configuration file"))
        self.exitAction = self.options.addAction(self.tr("&Exit"))
        self.about = self.menu.addMenu(self.tr("&About"))
        self.aboutAction = self.about.addAction(self.tr("About the Kaunter"))
        
        # Widgets layout definitions and other global stuff
        
        self.counterLayout = QtGui.QGridLayout(self) # General layout
        self.counterLayout.addWidget(self.menu)
        self.bottomLayout = QtGui.QGridLayout() # Bottom layout for buttons and help text
        self.exportFileButton = QtGui.QPushButton(self.tr("Export to &File"))
        self.exportClipboardButton = QtGui.QPushButton(self.tr("Export to &Clipboard"))

        self.helpText=QtGui.QLabel(self.tr("""<center><b>Shif+Key</b> decreases count, <b>Ctrl+Key</b>
                                           resets counter, <b>Ctrl+Shift+R</b> resets TheKaunter</center>"""))
        self.bottomLayout.addWidget(self.exportFileButton, 0, 0, 1, 1)
        self.bottomLayout.addWidget(self.exportClipboardButton, 0, 1, 1, 1)
        self.bottomLayout.addWidget(self.helpText, 1, 0, 1, -1)
        self.setWindowTitle(self.tr("TheKaunter: A versatile differential counter"))
        self.sections = self.configuration.sections
        maxColNumber = max([(len(self.configuration.items())) for i in self.sections])
        self.widgetDictionary = collections.OrderedDict()
        self.sectionsDictionary = collections.OrderedDict()
        
        widgetOffset=1 # For correct widget positioning
        globalKeyBindings = []
        for section in enumerate(self.sections):
            
            sectionIndex, sectionName = section
            sectionParameters = self.configuration[sectionName].keys()
            
            # Handling of wrong counter parameters in config file
        
            for parameter in sectionParameters:
                if parameter not in cellCounter.validSectionParameters:
                    
                    try:
                        self.configuration[sectionName][parameter].dict()
                    
                    except AttributeError:
                        
                        while True:
                
                            if self.configurationError(self.tr(
                                """Wrong counter configuration parameter:<br><br>
                                <b>Section</b> <i>%s</i><br><br>
                                <b>Parameter</b> <i>%s</i>"""
                                %(sectionName,parameter))) == 1:
                                break
                        return

            # Creates the section label and sets its color
            # if defined in configuration
            
            if self.configuration[sectionName].has_key('sectionColor'):
                sectionBackground = "background:%s" %(self.configuration[sectionName].pop('sectionColor'))
            else:
                sectionBackground = "background:None"
            
            self.labelSection=QtGui.QLabel(self.tr("<center><b>%s</b></center>"  %sectionName))
            self.labelSection.setStyleSheet(sectionBackground)
            self.counterLayout.addWidget(self.labelSection,
                                         sectionIndex+widgetOffset, 0, 1, -1)
            keyBindings = [] 

            # Creation of counters
            
            for itm in enumerate(self.configuration[section[1]]):
                
                itmIndex,itmName = itm
                counterLabel = itmName
                counterParameters = self.configuration[sectionName][itmName].keys()
                
                
                # Handling of wrong counter parameters in config file
                
                try:
                    
                    if not all(parameter in self.validCounterParameters for
                               parameter in counterParameters):
                        raise NameError
                           
                except NameError:
                    
                    while True:
                        
                        if self.configurationError(self.tr(
                            """Wrong counter configuration parameter:<br><br>
                            <b>Section</b> <i>%s</i><br><br>
                            <b>Counter</b> <i>%s</i>"""
                            %(sectionName, itmName))) == 1:
                            break
                    return
                                
                # Handling of missing KeyBinding definition
                
                try:
                    
                    keyBinding = self.configuration[sectionName]\
                                [itmName]['KeyBinding'].upper()
                           
                except KeyError:
                    
                    while True:
                        
                        if self.configurationError(self.tr(
                            """Missing key binding for:<br><br>
                            <b>Section</b> <i>%s</i><br><br>
                            <b>Counter</b> <i>%s</i>"""
                            %(sectionName, itmName))) == 1:
                            break
                    return
                    
                keyNumber = ord(keyBinding)
                
                # Sets the counter image if defined in configuration file.
                # If the file path is not valid, the image will be empty, no
                # exception/error is thrown
                
                if self.configuration[sectionName][itmName].has_key('counterImage'):
                    imagePath = self.configuration[sectionName][itmName]['counterImage']
                else:
                    imagePath = None
                
                # Checks for duplicate key bindings
                
                if keyNumber in globalKeyBindings:
                    
                    while True:
                        if self.configurationError(self.tr("""
                            There is a duplicate Key Binding
                            """ ))==1:
                            break
                        
                        
                else:
                    
                # Creates and inserts the new counter    
                    keyBindings.append(keyNumber)
                    globalKeyBindings.append(keyNumber)
                    newText = countingWidget(counterLabel, keyBinding,
                                       image = imagePath, color = sectionBackground)
                    self.counterLayout.addWidget(newText, sectionIndex+1+widgetOffset, itm[0], 1, 1)
                    self.widgetDictionary[keyNumber] = newText      

            # Creates and inserts the totalizer for the section
                        
            newTotalText = countingWidget(self.tr("Total %s" %sectionName),
                                          style='bold',color = sectionBackground)
            self.sectionsDictionary[newTotalText] = keyBindings
            self.counterLayout.addWidget(newTotalText,
                                        sectionIndex+1+widgetOffset, maxColNumber+1, 1, 1)
            widgetOffset += 1
        
        # Inserts the buttons layout and the help text
        
        self.counterLayout.addLayout(self.bottomLayout,
                                     self.counterLayout.rowCount()+widgetOffset+1,
                                     0, 1, -1)
      
        #Signal connections for the widget
        
        self.exportFileButton.clicked.connect(lambda: self.exportData('CSV'))
        self.exportClipboardButton.clicked.connect(lambda: self.exportData('CLIPBOARD'))
        self.counterChanged.connect(self.updateTotals)
        self.exitAction.triggered.connect(self.close)
        self.aboutAction.triggered.connect(lambda: aboutDialog().exec_())
        self.openConfigAction.triggered.connect(self.newConfiguration)
  
        self.show()
    
    def updateTotals(self): 
        
        for totalWidget in self.sectionsDictionary.keys():
            total = 0
            
            for counter in self.sectionsDictionary[totalWidget]:
                total += self.widgetDictionary[counter].editor.count
            totalWidget.editor.count=total
            totalWidget.editor.setText("%i" %total)
            
    def resetAll(self):
        
        confirmation = QtGui.QMessageBox(None)
        confirmation.setWindowTitle(self.tr("Confirmation Dialog"))
        confirmation.setText(self.tr("""<p align='center'><b>The Kaunter is
                                   going to be reset.</b><br><br>
                                   All current information is going to be 
                                   lost.<br><br><b>Are you sure?</b></p>"""))  
        btn1 = confirmation.addButton(self.tr("Proceed"), QtGui.QMessageBox.YesRole)
        btn2 = confirmation.addButton(self.tr("Cancel"), QtGui.QMessageBox.NoRole)
        confirmation.exec_()
        if confirmation.clickedButton() == btn1:
            for totalWidget in self.sectionsDictionary.keys():
                
                for counter in self.sectionsDictionary[totalWidget]:
                    self.widgetDictionary[counter].editor.reset()
                    
                totalWidget.editor.reset()
        else:
            return
        
    def exportData(self, destination):
        """
        Exports counter data to CSV or Clipboard
        Parameters:
        ===========
        destination: 'CSV' or 'CLIPBOARD'
        """
        exportedText = ""
        for section in self.sectionsDictionary:
            headers = []
            counts = []
            sectionTotalHeader = str(section.labelText)
            sectionTotalCount = str(section.editor.count)
            counters = self.sectionsDictionary[section]
            
            for counter in counters:
                counterHeader = str(self.widgetDictionary[counter].labelText)
                counterCount = str(self.widgetDictionary[counter].editor.count)
                headers.append(counterHeader)
                counts.append(counterCount)
            headers.append(sectionTotalHeader)
            counts.append(sectionTotalCount)
            exportedText += ("%s\n%s\n" %(';'.join(headers), ';'.join(counts)))
                   
        if destination == 'CSV':
            filename = QtGui.QFileDialog.getSaveFileName(
                None, self.tr("Select file for exporting data"), './data.csv', "*.csv")
            
            if filename.isEmpty() == False:
                with open(filename, 'w') as export:
                    export.write(exportedText)
                
        elif destination == 'CLIPBOARD':
            app.clipboard().setText(exportedText)
    
    def keyPressEvent(self,event):
        """
        Handles the key presses in TheKaunter main widget.
        The bound key alone increases the counter's count
        Shift + Bound Key decreases it.
        Ctrl + Bound Key resets an individual counter. Global count
        takes it into account.
        Ctrl + Shift + R resets all the counters.
        """
           
        if (event.modifiers() == QtCore.Qt.NoModifier) and\
           (event.key() in self.widgetDictionary):
            self.widgetDictionary[event.key()].editor.increase()
            self.counterChanged.emit()
            
        elif (event.modifiers() == QtCore.Qt.ShiftModifier) and\
             (event.key() in self.widgetDictionary):
            self.widgetDictionary[event.key()].editor.decrease()
            self.counterChanged.emit()
            
        elif (event.modifiers() == QtCore.Qt.ControlModifier) and\
            (event.key() in self.widgetDictionary):
            self.widgetDictionary[event.key()].editor.reset()
            self.counterChanged.emit()
            
        elif (event.modifiers().__int__() == (QtCore.Qt.ControlModifier\
            + QtCore.Qt.ShiftModifier)):
            if (event.key() == QtCore.Qt.Key_R):
                self.resetAll()
        else:
            event.ignore()
    
    
    
    def newConfiguration(self):
        """
        Loads a new configuration file and reloads TheKaunter to reflect
        the changes.
        """
        filename = QtGui.QFileDialog.getOpenFileName(None,
                    self.tr("Select a suitable configuration file for TheKaunter"),
                    './', "*.conf")
        
        if filename != "":
            self.close()
            self.__init__(configFile = str(filename))
            return 1
        
        else:
            return 0
            
    def configurationError(self, message=""):
        
        """
        Manages configuration files errors. If loading fails, gives the
        option of loading another configuraion file or exit the program
        Parameters:
        ===========
        message: Info to be displayed
        """
        
        # This way of creating the message is somehow annoying, but is 
        # the only way to show the translations properly
        # TODO: Fix translations issues
        
        message1 = self.tr("""<center><b>An error has been detected while<br>
                           parsing the configuration file:</b><br><br>""")
        message2 = self.tr("""<br><br>Do you want to try again or do you
                           want to exit TheKaunter?</center>""")
        
        message = self.tr(message1 + message +message2)
                              
        confirmation = QtGui.QMessageBox(None)
        confirmation.setWindowTitle(self.tr("Confirmation Dialog"))
        confirmation.setText(self.tr(message))  
        btn1 = confirmation.addButton(self.tr("Load configuration"), QtGui.QMessageBox.YesRole)
        btn2 = confirmation.addButton(self.tr("Exit"), QtGui.QMessageBox.NoRole)
        confirmation.exec_()
        
        if confirmation.clickedButton() == btn1:
            
            return self.newConfiguration()
        else:
            sys.exit()
        
         

class countingWidget(QtGui.QFrame):
    
    """
    This class provides a widget composed by a countingLineEdit and a QLabel. This eases
    the recovery of information from each counter.
    Parameters:
    ===========
    labelText: Text for the label of the widget
    labelStyle: Style for the label, defaults no font decoration 'bold' 
                for bold typeface
    image: path of the descriptive image for the counter
    color: a background color in the form of a Qt styleSheet definition
           (background:color)
    """
    
    def __init__(self, labelText="", keyBinding="", style = None,
                 parent = None, image = None, color = None):
            
        QtGui.QFrame.__init__(self, parent)
        self.labelText = labelText 
        self.keyBinding = keyBinding 
        self.layout = QtGui.QVBoxLayout(self)
        self.editor = countingLineEdit()
        self.editor.setStyleSheet(color)
        
        # Style settings: Bold or plain text
        
        if style == None:
            self.label=QtGui.QLabel(self.tr("<center>%s<br>%s</center>"
                                     %(self.labelText, self.keyBinding)))
        elif style == 'bold':
            self.label=QtGui.QLabel(self.tr("<center><b>%s<br>%s</b></center>"
                                     %(self.labelText, self.keyBinding)))

        self.label.setAlignment(QtCore.Qt.AlignBottom)
        
        # Counter image management
        
        if image != None:
            
            self.imageLabel = QtGui.QLabel()    
            self.pixmap = QtGui.QPixmap(image)
            self.pixmap = self.pixmap.scaledToWidth(100)
            self.painter = QtGui.QPainter(self.pixmap)
            self.pen = QtGui.QPen()
            self.pen.setWidth(4)
            self.pen.setColor(QtCore.Qt.black)
            self.painter.setPen(self.pen)
            self.painter.drawRect(self.painter.window())
            self.painter.end()
            self.imageLabel.setPixmap(self.pixmap)
            self.layout.addWidget(self.imageLabel)
            self.imageLabel.setAlignment(QtCore.Qt.AlignHCenter)
     
      
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.editor)
    

class countingLineEdit(QtGui.QLineEdit):
    
    """
    This class provides a LineEdit widget which acts like a counter,
    being possible to define a key for increment, decrement and reset its
    count. Amount of increment is configurable.
    The operation of this widget can be through the keyboard or
    programatically, making use of the methods increase, decrease and
    reset.   
    
    Parameters:
    ===========
    increaseKey: Key which increases the widget's count by 1
    decreaseKey: Key which decreases the widget's count by 1
    resetKey:    Key which resets the widget's count to 0
    increment:   Amount of increase for the widget, defaults to 1
    """
    def __init__(self, increaseKey=None, decreaseKey=None, resetKey=None, amount=1):
        
      QtGui.QLineEdit.__init__(self)
      self.setAlignment(QtCore.Qt.AlignHCenter)
      self.count = 0
      self.amount = amount
      self.setText('0')
      if increaseKey != None:
          self.increaseKey = ord(increaseKey)
      else:
          self.increaseKey = None
          
      if decreaseKey != None:
          self.decreaseKey = ord(decreaseKey)
      else:
          self.decreaseKey = None
          
      if resetKey != None:
          self.resetKey = ord(resetKey)
      else:
          self.resetKey = None
      
    def increase(self):
        self.count += self.amount
        self.setText("%i" %self.count)
      
    def decrease(self):
        if self.count >= self.amount:
            self.count -= self.amount
            self.setText("%i" %self.count)

    def reset(self):
        self.count = 0
        self.setText("%i" %self.count)
        
    def keyPressEvent(self, event):
        
        if (event.key() == self.increaseKey):
            self.increase()
        
        if (event.key() == self.decreaseKey):
            self.decrease()
            
        if (event.key() == self.resetKey):
            self.reset()
        
        else:
            event.ignore()

class aboutDialog(QtGui.QDialog):
    
    """
    This is a generic dialog for showing GNU/GPL V3 license
    """
    
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setWindowTitle(self.tr("About TheKaunter"))
        self.layout = QtGui.QVBoxLayout(self)
        self.headerLabel = \
        QtGui.QLabel(self.tr("""<center><h1>TheKaunter</h1><h2>
                                A versatile differential counter</h2>
                                <h4>Version 2.0.0</h4>
                                &copy; 2013 Jorge Tornero<br>
                                <a href="http://imasdemase.com">
                                http://imasdemase.com</a><br></center>"""))
        
        self.headerLabel.setOpenExternalLinks(True)
        
        self.GPL3 = self.tr("""<center><h3>GNU GENERAL PUBLIC LICENSE</h3>
                    <h5>Version 3, 29 June 2007</h5>
                    </center><p align="justify">This program is free software:
                    you can redistribute it and/or modify it under the terms
                    of the GNU General Public License as published by the Free
                    Software Foundation, either version 3 of the License, or
                    (at your option) any later version.<br><br>This program is
                    distributed in the hope that it will be useful, but WITHOUT
                    ANY WARRANTY; without even the implied warranty of
                    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
                    See the GNU General Public License for more details.<br>
                    <br>You should have received a copy of the GNU General
                    Public License along with this program.
                    If not, see:<br><center> <a href="http://www.gnu.org/licenses">
                    http://www.gnu.org/licenses</a><center></p>""")
        
        self.licenseText = QtGui.QTextBrowser()
        self.licenseText.setOpenExternalLinks(True)
        self.licenseText.setReadOnly(True)
        self.licenseText.setHtml(self.tr(self.GPL3))
        self.closeButton = QtGui.QPushButton(self.tr('Accept'))
        self.layout.addWidget(self.headerLabel)
        self.layout.addWidget(self.licenseText)
        self.layout.addWidget(self.closeButton)
        
        self.closeButton.clicked.connect(self.close)
        self.show()
        

if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    appTranslator = QtCore.QTranslator() 
    appTranslator.load('./theKaunter.qm') 
    app.installTranslator(appTranslator) 
    
    counter=cellCounter()
    
    sys.exit(app.exec_())
    