"""***************************************************************************
Title:          Heating and Cooling Graphic
File:           heating_cooling.py
Release Notes:  N/A

Author:         Zhaolin Wei

Description:    This file is used to initiate the graphic for any heating or
                cooling device, and change the output.
***************************************************************************"""

"""*********************Libraries******************************************"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QTimer


"""*********************Global*********************************************"""
furnace_images = {
    "Fault" : "Furnace/furnace_fault.png",
    "Off" : "Furnace/furnace_off.png",
    "On" : ["Furnace/furnace_on_1.png", "Furnace/furnace_on_2.png", 
            "Furnace/furnace_on_3.png", "Furnace/furnace_on_4.png"]
    }

aircon_images = {
    "Fault" : "Aircon/aircon_fault.png",
    "Off" : "Aircon/aircon_off.png",
    "On" : ["Aircon/aircon_on_1.png", "Aircon/aircon_on_2.png", 
            "Aircon/aircon_on_3.png"]
    }
    
    
"""*********************Classes********************************************"""
'========================================='
class Appliance(QLabel):
    """
    Generates the structure for either the heating or cooling unit graphic.
    """
    def __init__(self, appliance = "furnace", status = "Off", 
                 energy = 0.00, scale = 1, 
                 pos_x = 0, pos_y = 0, instance = None):
        """
        Initializes the appliance and pushes the graphic.
        
        appliance: The installed heating/cooling device.
        status: Sets the status of the appliance as on/off/fault.
        temperature: The target temperature of the appliance output.
        scale: Sets the scale of the graphic.
        pos_x: Position along x axis on the graphic window (>=0).
        pos_y: Position along y axis on the graphic window (>=0).
        instance: For callout in a class, this would be self (usually a window).
        """
        super().__init__(instance)
        
        # Initialize variables
        self.__appliance = appliance
        self.__status = status
        self.__energy = energy
        self.__scale = scale
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__frame = 0 # Starting frame
        
        # Image verification
        try:  
            if self.__appliance == "furnace":
                self.graphics = furnace_images
            else:
                self.graphics = aircon_images
        except Exception as e: 
            print(e) 
            self.__status = "Fault" 
            self.graphics = {"An error has occurred generating the image."}
            
                # Graphic Animation
        self.__timer = QTimer(self)  # Timer to handle the animation
        self.__timer.timeout.connect(self.update_appliance_on)
                
        # Initiate Graphic
        if self.__status == "On":
            self.start_appliance_on()
        else:
            self.appliance_inactive()
        
    def paintEvent(self, event):
        """
        This method is called to update the graphic.
        
        Note: Method supported by chatgtp to initialize the painter
        """
        try:
            painter = QPainter(self)
            painter.begin(self)
            
            # Draw the furnace image based on the current status
            if self.__status == "On":
                image = self.graphics["On"][self.__frame]
            else:
                image = self.graphics[self.__status]
            
            # Scale the image
            pixmap = QPixmap(image).scaled(int(300 * self.__scale), 
                                           int(350 * self.__scale), 
                                           Qt.KeepAspectRatio)
            
            # Set the widget's size to match the image size (this is critical)
            self.setFixedSize(pixmap.size())
            
            # Draw the furnace image at the position specified by pos_x and pos_y
            painter.drawPixmap(0, 0, pixmap)
            
            # Draw the status and temperature text
            painter.setFont(QFont("Aptos", int(self.__scale * 18))) 
            painter.setPen(QColor(0, 0, 0))
            
            # Draw status text, positioned relative to the image
            status = self.__status.capitalize()
            painter.drawText(int(self.__scale * 170), int(self.__scale * 50), 
                             status)
            
            # Draw temperature text if the furnace is on
            if self.__status == "On":
                temperature = f"{self.__energy}°C"
                painter.drawText(int(self.__scale * 160), int(self.__scale * 110), 
                                 temperature)
                
            # Additional text on image
            painter.drawText(int(self.__scale * 110), int(self.__scale * 340), 
                             self.__appliance.capitalize())
            painter.drawText(int(self.__scale * 20), int(self.__scale * 110), 
                             "Energy")
            painter.drawText(int(self.__scale * 20), int(self.__scale * 50), 
                             "Status")
            
            # Move to final position, no impact from scale
            self.move(self.__pos_x, self.__pos_y)
            
            # End painter
            painter.end()
            
        except Exception as e:
            print(f"Error has occured in HeatingCooling paintEvent: {e}")
                
    def appliance_inactive(self):
        """
        Initiates image for either fault or off modes of the furnace images.
        """        
        self.update()
        self.__timer.stop()     
       
    def start_appliance_on(self):
        """
        Starts the animation for the "On" state.
        """
        self.__timer.start(500)
        
    def update_appliance_on(self):
        """
        Cycles through the on graphic.
        """
        try:
            # Initialize images
            image = self.graphics["On"][self.__frame]
            pixmap = QPixmap(image).scaled(int(300 * self.__scale), 
                                           int(350 * self.__scale), 
                                           Qt.KeepAspectRatio)
            self.setPixmap(pixmap)
            self.setFixedSize(pixmap.size())
            self.move(self.__pos_x, self.__pos_y)
            
            # Increment frame and cycle it
            self.__frame = (self.__frame + 1) % len(self.graphics["On"])   
            
        except Exception as e:
            print(f"Error in updating the appliance: {e}")            
    
    def update_temperature(self, energy):
        """
        Updates the temperature and graphic.
        
        temperature: The new temperature of the system.
        """
        self.__energy = energy
        self.update()
        

'========================================='
class Furnace(Appliance): 
    """
    Instantiates an instance of the furnace class.
    """
    def __init__(self, status="Off", energy=0.00, scale=1, 
                 pos_x=0, pos_y=0, instance=None): 
        """
        Initializing the class through inheritance from the appliance class.
        
        status: Sets the status of the appliance as on/off/fault.
        temperature: The target temperature of the appliance output.
        scale: Sets the scale of the graphic.
        pos_x: Position along x axis on the graphic window (>=0).
        pos_y: Position along y axis on the graphic window (>=0).
        instance: For callout in a class, this would be self (usually a window).
        """
        super().__init__(appliance="furnace", status=status, 
                         energy=energy, scale=scale, 
                         pos_x=pos_x, pos_y=pos_y, instance=instance)
        
        
'========================================='
class Aircon(Appliance): 
    """
    Instantiates an instance of the air conditioner class.
    """
    def __init__(self, status="Off", energy=0.00, scale=1, 
                 pos_x=0, pos_y=0, instance=None): 
        """
        Initializing the class through inheritance from the appliance class.
        
        status: Sets the status of the appliance as on/off/fault.
        temperature: The target temperature of the appliance output.
        scale: Sets the scale of the graphic.
        pos_x: Position along x axis on the graphic window (>=0).
        pos_y: Position along y axis on the graphic window (>=0).
        instance: For callout in a class, this would be self (usually a window).
        """
        super().__init__(appliance="aircon", status=status, 
                         energy=energy, scale=scale, 
                         pos_x=pos_x, pos_y=pos_y, instance=instance)
    
    
"""*********************Main Routine***************************************"""
if __name__ == "__main__":
    # Demonstration window
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.setWindowTitle("PyQt5 GUI")
    main_window.setGeometry(500, 500, 500, 500)
    
    # Graphic
    furnace_graphic = Furnace("On", scale=1, 
                                pos_x=100, pos_y=100, instance=main_window)
    furnace_graphic.show()
    main_window.show()
    sys.exit(app.exec_())