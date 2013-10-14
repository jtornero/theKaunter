#!/usr/bin/env python

# TheKaunter. A versatile differential counter.
# 
# Copyright 2013 Jorge Tornero
# 
# This file is part of TheKaunter
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
import ConfigParser as cp
import collections
from PyQt4 import QtGui,QtCore

class cellCounter(QtGui.QWidget):
    """ Main Widget for TheKaunter
    TODO:   Load configuration file instead of have it harcoded
            Check configuration files for errors"""
    
    counterChanged = QtCore.pyqtSignal()
  
    def __init__(self):
        QtGui.QWidget.__init__(self,parent=None)
        
        
        self.configuration = cp.RawConfigParser()
        self.configuration.read('./theKaunter.conf')
                
        self.layout = QtGui.QGridLayout(self)
        self.bottomLayout = QtGui.QHBoxLayout()
        self.setWindowTitle(self.tr("TheKaunter: A versatile differential counter"))
        self.exportFileButton = QtGui.QPushButton(self.tr("Export to &File"))
        self.exportClipboardButton = QtGui.QPushButton(self.tr("Export to &Clipboard"))
                
        self.sections = self.configuration.sections()
        maxColNumber = max([(len(self.configuration.items(i))) for i in self.sections])
        self.widgetDictionary = collections.OrderedDict()
        self.sectionsDictionary = collections.OrderedDict()
        
        for section in enumerate(self.sections):
            sectionIndex, sectionName = section
            self.labelSection=QtGui.QLabel(self.tr("<center><b>%s</b></center>"  %sectionName))
            self.layout.addWidget(self.labelSection,sectionIndex,0,1,1)
            keyBindings = []
            
            for itm in enumerate(self.configuration.items(sectionName)):
                counterLabel = self.configuration.items(sectionName)[itm[0]][0].title()
                keyNumber = ord((itm[1][1]).upper())               
                keyBinding = self.configuration.items(sectionName)[itm[0]][1]
                keyBindings.append(keyNumber)
                newText=countingWidget(counterLabel, keyBinding)
                self.layout.addWidget(newText, sectionIndex, itm[0]+1, 1, 1)
                self.widgetDictionary[keyNumber] = newText
                
            newTotalText = countingWidget(self.tr("Total %s" %sectionName), style='bold')
            self.sectionsDictionary[newTotalText] = keyBindings
            self.layout.addWidget(newTotalText, sectionIndex,maxColNumber+1, 1, 1)
            
        self.layout.addLayout(self.bottomLayout,self.layout.rowCount(), 0, 1, -1)
        self.bottomLayout.insertWidget(0, self.exportFileButton)
        self.bottomLayout.insertWidget(1, self.exportClipboardButton)
        
        self.exportFileButton.clicked.connect(lambda: self.exportData('CSV'))
        self.exportClipboardButton.clicked.connect(lambda: self.exportData('CLIPBOARD'))
        self.counterChanged.connect(self.updateTotals)
        
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
                None, self.tr("Select file for exporting data"), './data.csv',"*.csv")
            
            if filename.isEmpty() == False:
                with open(filename,'w') as export:
                    export.write(exportedText)
                
        elif destination == 'CLIPBOARD':
            app.clipboard().setText(exportedText)
    
    def keyPressEvent(self,event):
           
        if (event.modifiers()==QtCore.Qt.NoModifier) and\
           (event.key() in self.widgetDictionary):
            self.widgetDictionary[event.key()].editor.increase()
            self.counterChanged.emit()
            
        elif (event.modifiers()==QtCore.Qt.ShiftModifier) and\
             (event.key() in self.widgetDictionary):
            self.widgetDictionary[event.key()].editor.decrease()
            self.counterChanged.emit()
            
        elif (event.modifiers()==QtCore.Qt.ControlModifier) and\
            (event.key() in self.widgetDictionary):
            self.widgetDictionary[event.key()].editor.reset()
            self.counterChanged.emit()
            
        elif (event.modifiers().__int__()==(QtCore.Qt.ControlModifier\
            + QtCore.Qt.ShiftModifier)):
            if (event.key() == QtCore.Qt.Key_R):
                self.resetAll()
        else:
            event.ignore()
            
            
class countingWidget(QtGui.QWidget):
    
    """This class provides a widget composed by a countingLineEdit and a QLabel. This eases
    the recovery of information from each counter.
    Parameters:
    ===========
    labelText: Text for the label of the widget
    labelStyle: Style for the label, defaults no font decoration 'bold' 
                for bold typeface"""
    
    def __init__(self, labelText="", keyBinding="", style=None, parent=None,):
        
        QtGui.QWidget.__init__(self, parent)
        self.labelText = labelText
        self.keyBinding = keyBinding
        self.layout=QtGui.QVBoxLayout(self)
        
        if style == None:
            self.label=QtGui.QLabel(self.tr("<center>%s<br>%s</center>"
                                     %(self.labelText,self.keyBinding)))
        elif style == 'bold':
            self.label=QtGui.QLabel(self.tr("<center><b>%s<br>%s</b></center>"
                                     %(self.labelText,self.keyBinding)))
        
        self.editor=countingLineEdit()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.editor)
        
     

class countingLineEdit(QtGui.QLineEdit):
    """This class provides a LineEdit widget which acts like a counter,
    being possible to define a key for increment, decrement and reset its
    count. Amount of increment is configurable.
    
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
            
if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    appTranslator = QtCore.QTranslator() 
    appTranslator.load('./theKaunter.qm') 
    app.installTranslator(appTranslator) 
    counter=cellCounter()
    
    sys.exit(app.exec_())
