"""***************************************************************************
Title:          Symbols Generator
File:           symbols.py
Release Notes:  N/A

Author:         Nik Paulic

Description:    This file is used to initiate the graphic for any heating or
                cooling device, and change the output.
***************************************************************************"""

"""*********************Libraries******************************************"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtWidgets import QDoubleSpinBox
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import Qt

# Enable high DPI scaling 
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

"""*********************Global*********************************************"""
# Consists of the image, True if value and False with no value
symbol_images = {
    "temperature" : ["Symbols/temp_sensor.png", False, None],
    "airflow" : ["Symbols/flow_sensor.png", False, None],
    "damper value" : ["Symbols/numeric.png", True, "%"],
    "temp value" : ["Symbols/numeric.png", True, "°C"],
    "airflow value" : ["Symbols/numeric.png", True, "cfm"],
    "energy value" : ["Symbols/numeric.png", True, "BTU/hr"],
    "time value" : ["Symbols/time.png", True, ""], 
    "state value" : ["Symbols/numeric.png", True, ""]
    } 


"""*********************Functions******************************************"""
'========================================='  
def add_button(label = "Not available", widget = None,
               size_x = 10, size_y = 10, pos_x = 0, pos_y = 0):
    """
    Generates a button on the GUI. Position, size, and label required.
    
    label: Specify the text label on the button.
    widget: Specify the central widget the button is generated.
    size_x: Size along the x axis in the graphic window (>0).
    size_y: Size along the y axis in the graphic window (>0).
    pos_x: Position along x axis on the graphic window (>=0).
    pos_y: Position along y axis on the graphic window (>=0).
    """
    button = QPushButton(label, widget)
    button.setFixedSize(size_x, size_y)
    button.move(pos_x, pos_y) 
    if label == "Quit":
        #button.clicked.connect()
        return button

'========================================='  
def add_text(label = "Not available", font = "title", instance = None,
             size_x = 10, size_y = 10, pos_x = 0, pos_y = 0):
    """
    Generates text in the GUI. Position, size, and label required.
    
    label: Specify the text in the location.
    font: Specify the font type between presets in this document.
    instance: Specify the window in which the text is active (usually self).
    size_x: Size along the x axis in the graphic window (>0).
    size_y: Size along the y axis in the graphic window (>0).
    pos_x: Position along x axis on the graphic window (>=0).
    pos_y: Position along y axis on the graphic window (>=0).
    """
    if font == "title": font = QFont("Aptos", 24)
    elif font == "subtitle": font = QFont("Aptos", 18)
    else: font = QFont("Aptos", 10)
    
    text = QLabel(label, instance)
    text.setFont(font)
    text.setFixedSize(size_x, size_y)
    text.move(pos_x, pos_y) 
    text.adjustSize()
    text.setScaledContents(True)
    

'========================================='  
def add_image(file = None, scale = 1, instance = None, 
              size_x = 10, size_y = 10, pos_x = 0, pos_y = 0):
    """
    Generates an image in the GUI. Position, size, and filename required.
    
    file: Specify the file name and location as text 'folder/name.png'.
    scale: Specify the scale of the graphic relative to the standard size.
    instance: Specify the window in which the text is active (usually self).
    size_x: Size along the x axis in the graphic window (>0).
    size_y: Size along the y axis in the graphic window (>0).
    pos_x: Position along x axis on the graphic window (>=0).
    pos_y: Position along y axis on the graphic window (>=0).
    """
    image = QLabel(instance)
    pixmap = QPixmap(file)
    resized_pixmap = pixmap.scaled(int(size_x*scale), int(size_y*scale), 
                                   Qt.KeepAspectRatio)
    image.setPixmap(resized_pixmap)
    image.setFixedSize(resized_pixmap.size())
    image.move(pos_x, pos_y)
    
    
"""*********************Classes********************************************"""
'========================================='
class Symbols(QLabel):
    """
    Generates the graphic for any predetermined static or dynamic symbol.
    """
    def __init__(self, symbol = "temperature", value = 0.00, instance = None,
                 scale = 1, pos_x = 0, pos_y = 0):
        """
        Initializes the symbol and pushes the graphic.
        
        symbol: Specify what kind of value is used: temperature, airflow, 
                damper value, temp value, energy value, airflow value, 
                and time value.
        value: Specify the value of whatever is being measured.
        instance: Specify the window to generate (usually self).
        scale: Specify the scale of the graphic relative to the standard size.
        pos_x: Position along x axis on the graphic window (>=0).
        pos_y: Position along y axis on the graphic window (>=0).
        """
        super().__init__(instance)
        
        # Initialize variables
        self.__graphic = symbol_images[symbol][0]
        self.__contains_value = symbol_images[symbol][1]
        self.__value = value
        self.__unit = symbol_images[symbol][2]
        self.__scale = scale
        self.__pos_x = pos_x
        self.__pos_y = pos_y
    
    def paintEvent(self, event):
        """
        This method is called to update the graphic via events.
        
        Note: Rotation supported by chatGTP
        """
        # Initialize Painter
        painter = QPainter(self)
        painter.begin(self)
        
        # Scale the image
        pixmap = QPixmap(self.__graphic)
        if self.__graphic == symbol_images["time value"][0]: 
            length = int(pixmap.height() * self.__scale*1.4) 
            width = int(pixmap.width() * (self.__scale*1.4)) 
        else: 
            length = int(pixmap.height() * self.__scale) 
            width = int(pixmap.width() * self.__scale)
        pixmap = pixmap.scaled(length, width, Qt.KeepAspectRatio)
        self.setFixedSize(width, length)
            
        # Draw the furnace image at the position specified by pos_x and pos_y
        painter.translate(width / 2, length / 2)
        painter.drawPixmap(int(-width / 2), int(-length / 2), pixmap)
        
        # Print a value over the image
        if self.__contains_value:
            painter.setFont(QFont("Aptos", int(self.__scale * 12))) 
            painter.setPen(QColor(0, 0, 0))
            text = str(self.__value) + self.__unit
            
            if self.__graphic == symbol_images["time value"][0]:
                text_x = int(self.__scale * -220)
                text_y = int(self.__scale * -35)
            else:
                text_x = int(self.__scale * -80)
                text_y = int(self.__scale * -18)
            painter.drawText(text_x, text_y, text)
            
        # Move to final position, no impact from scale
        self.move(self.__pos_x, self.__pos_y)
        
        painter.end()
             
    def update_value(self, status):
        """
        Updates the value and graphic.
        """
        self.__status = status
        self.update()
        
    @staticmethod
    def spinbox_sp(instance, low_range, high_range, value, suffix, step,
                     size_x, size_y, pos_x, pos_y):
        """
        Generates a spinbox for temperature setpoints.
        
        instance: Specify the window of applicability (usually self).
        low_range: Specify the upper applicable range of the value.
        high_range: Specify the lower applicable range of the value.
        value: Specify the quantity/value.
        suffix: Specify the unit of the value.
        step: Specify the incremental steps for spinbox setpoints.
        size_x: Size along the x axis in the graphic window (>0).
        size_y: Size along the y axis in the graphic window (>0).
        pos_x: Position along x axis on the graphic window (>=0).
        pos_y: Position along y axis on the graphic window (>=0).
        """
        setpoint = QDoubleSpinBox(instance) 
        setpoint.setRange(low_range, high_range)
        setpoint.setValue(value)
        setpoint.setDecimals(1)
        setpoint.setSuffix(suffix)
        setpoint.setSingleStep(step)
        setpoint.setFixedSize(size_x, size_y) 
        setpoint.move(pos_x, pos_y)
        setpoint.setStyleSheet("QDoubleSpinBox { border: 1px solid black; }")
        return setpoint

        
"""*********************Main Routine***************************************"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.setWindowTitle("PyQt5 GUI")
    main_window.setGeometry(200, 200, 300, 300)
    
    symbol = Symbols("time value", value = "2024-10-03", scale=2, 
                              pos_x=100, pos_y=100, instance=main_window)
    symbol.show()
    
    main_window.show()
    sys.exit(app.exec_())
