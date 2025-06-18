"""***************************************************************************
Title:          Damper Graphic
File:           damper.py
Release Notes:  N/A

Author:         Zhaolin Wei

Description:    This file is used to initiate the graphic for the damper as
                well as receive inputs/outputs when called.
***************************************************************************"""

"""*********************Libraries******************************************"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt
import math


"""*********************Global*********************************************"""
damper_images = {
    -1 : "Damper/damper_fault.png", # fault case
    0 : "Damper/damper_0.png",
    15: "Damper/damper_15.png",
    30: "Damper/damper_30.png",
    50: "Damper/damper_50.png",
    70: "Damper/damper_70.png",
    85: "Damper/damper_85.png",
    99: "Damper/damper_100.png"
    }


"""*********************Classes********************************************"""
'========================================='
class Damper(QWidget):
    """
    Generates the object for a damper graphic
    """
    def __init__(self, status = 0, scale = 1/1, angle = 0,
                 pos_x = 0, pos_y = 0, instance = None):
        """
        Initializes the damper and pushes the graphic.
        
        status: The angular position of the damper blades (0-100, -1 fault).
        scale: The scale of the damper graphic.
        angle: The angle of the damper graphic.
        pos_x: Position along x axis on the graphic window (>=0).
        pos_y: Position along y axis on the graphic window (>=0).
        instance: For callout in a class, this would be self (usually a window).
        """
        super().__init__(instance)
        
        try:
            # Initialize variables
            self.__scale = scale
            self.__pos_x = pos_x
            self.__pos_y = pos_y
            self.__angle = angle
            
            if not 0 <= status <= 100 and status != -1: 
                raise ValueError("Status must be between 0 ",
                                 "and 100 or -1 for fault.")
            else:        
                self.__status = status
                                
            # Initiate Graphic
            if self.__status in range(0,5): 
                self.graphic = damper_images[0] # 0% graphic
            elif self.__status in range(6,19):
                self.graphic = damper_images[15] # 15% graphic
            elif self.__status in range(20,39):
                self.graphic = damper_images[30] # 30% graphic
            elif self.__status in range(40,60):
                self.graphic = damper_images[50] # 50% graphic
            elif self.__status in range(61,79):
                self.graphic = damper_images[70] # 70% graphic
            elif self.__status in range(80,94):
                self.graphic = damper_images[85] # 85% graphic
            elif self.__status in range(95,101):
                self.graphic= damper_images[99] # 100% graphic
            else: 
                self.graphic = damper_images[-1]  # fault graphic
                
        except ValueError:
            self.__status = -1
            self.graphic = damper_images[-1] # fault graphic
            self.update()
            
        except KeyError as e: 
            print(f"Error loading damper image: {e}") 
            self.__status = -1
            self.graphic = damper_images[-1] # fault graphic
            self.update()
    
    def paintEvent(self, event):
        """
        This method is called to update the graphic.
            
        Note: Rotation supported by chatGTP.
        """
        try:
            painter = QPainter(self)
            painter.begin(self)
            
            # Set the angle 
            painter.translate(self.width() / 2, self.height() / 2)
            painter.rotate(self.__angle) 
            painter.translate(-self.width() / 2, -self.height() / 2)
            
            # Scale the image
            pixmap = QPixmap(self.graphic).scaled(int(208 * self.__scale), 
                                                    int(76 * self.__scale), 
                                                    Qt.KeepAspectRatio)
            
            # Set the widget's size to match the image size
            rotated_width = int(pixmap.width() * 
                                math.cos(math.radians(self.__angle)) + 
                                pixmap.height() * 
                                math.sin(math.radians(self.__angle)))
            rotated_height = int(pixmap.width() * 
                                 math.sin(math.radians(self.__angle)) + 
                                 pixmap.height() * 
                                 math.cos(math.radians(self.__angle)))
            self.setFixedSize(rotated_width, rotated_height)
            
            # Draw damper image at the position specified by pos_x and pos_y
            painter.translate(self.width() / 2, self.height() / 2)
            painter.drawPixmap(int(-pixmap.width() / 2), 
                               int(-pixmap.height() / 2), pixmap)
                
            # Move to final position, no impact from scale
            self.move(self.__pos_x, self.__pos_y)
            
            # End update
            painter.end()
            
        except Exception as e:
            print(f"Error in Damper paintEvent: {e}")
            
    def update_status(self, status):
        """
        Updates the position and graphic.
        
        status: The angular position of the damper blades (0-100, -1 fault).
        """
        self.__status = status
        self.update()
    
    
"""*********************Main Routine***************************************"""
if __name__ == "__main__":
    try:
        # Setup window
        app = QApplication(sys.argv)
        main_window = QMainWindow()
        main_window.setWindowTitle("PyQt5 GUI")
        main_window.setGeometry(500, 500, 400, 400)
        
        # Test graphic
        graphic = Damper(status = 85, scale = 1/1, pos_x=100, pos_y=100,
                         angle = 10, instance=main_window)
        graphic.show()
        main_window.show()
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"An error occurred: {e}")
