"""***************************************************************************
Title:          Fan Graphic
File:           fan.py
Release Notes:  N/A

Author:         Zhaolin Wei

Description:    This file is used to initiate the graphic for Fan
***************************************************************************"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QTimer

"""*********************Global*********************************************"""
fan_images = {
    "fault": "Fan/fan_fault.png",
    "off": "Fan/fan_off.png",
    "on_high_speed": ["Fan/fan_high_1.png", "Fan/fan_high_2.png"],
    "on_medium_speed": ["Fan/fan_medium_1.png", "Fan/fan_medium_2.png"],
    "on_low_speed": ["Fan/fan_low_1.png", "Fan/fan_low_2.png", 
                     "Fan/fan_low_3.png", "Fan/fan_low_4.png"]
}

"""*********************Classes********************************************"""
class Fan(QLabel):
    """
    Generates the structure for the fan graphic

    Note: Structure decided with the help of Chatgpt
    """
    def __init__(self, status="off", speed="low", scale=1, 
                 pos_x=0, pos_y=0, instance=None):
        """
        Initializes the fan and pushes the graphic
        """
        super().__init__(instance)
        
        # Initialize variables
        self.__status = status
        self.__speed = speed
        self.__scale = scale
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__frame = 0  # Starting frame

        # Graphics for the fan
        self.graphics = fan_images
        
        # Timer for animation
        self.__timer = QTimer(self)
        self.__timer.timeout.connect(self.update_fan_on)
        
        # Initiate Graphic
        self.update_fan_state()


    def paintEvent(self, event):
        """
        This method is called to update the graphic
        """
        painter = QPainter(self)
        painter.begin(self)
        
        # Choose the correct image
        if self.__status == "on":
            images = self.graphics[f"on_{self.__speed}_speed"]
            image = images[self.__frame]
        elif self.__status == "fault":
            image = self.graphics["fault"]
        else:
            image = self.graphics["off"]

        # Scale the image
        pixmap = QPixmap(image).scaled(int(300 * self.__scale), 
                                       int(350 * self.__scale), 
                                       Qt.KeepAspectRatio)
        
        # Set widget size to match image size
        self.setFixedSize(pixmap.size())
        
        # Draw the image
        painter.drawPixmap(0, 0, pixmap)
        
        # Draw status and speed text
        painter.setFont(QFont("Aptos", int(self.__scale * 18))) 
        painter.setPen(QColor(0, 0, 0))
        
        # Status text
        status_text = self.__status.capitalize()
        
        # Speed text
        if self.__status == "on":
            painter.drawText(int(self.__scale * 190), int(self.__scale * 45), 
                             self.__speed)
            painter.drawText(int(self.__scale * 90), int(self.__scale * 45), 
                            "Speed:")
            painter.drawText(int(self.__scale * 170), int(self.__scale * 210), 
                             "On")
        elif self.__status == "fault":
            painter.setPen(QColor(255, 0, 0))  # Red text for fault
            painter.drawText(int(self.__scale * 170), int(self.__scale * 210), 
                             "is Faulty")
        else:
            painter.drawText(int(self.__scale * 170), int(self.__scale * 210), 
                             "Off")


        # Additional text on the image
        painter.drawText(int(self.__scale * 110), int(self.__scale * 210), 
                         "Fan")
        
        # Move to final position
        self.move(self.__pos_x, self.__pos_y)
        
        painter.end()


    def update_fan_state(self):
        """
        Updates the fan state based on the status.
        """
        if self.__status == "on":
            self.start_fan_on()
        else:
            self.fan_inactive()


    def fan_inactive(self):
        """
        Displays the fan in 'off' or 'fault' mode.
        """
        self.update()
        self.__timer.stop()


    def start_fan_on(self):
        """
        Starts the fan animation for 'on' state.
        """
        self.__timer.start(500)


    def update_fan_on(self):
        """
        Cycles through the 'on' graphics based on speed.
        """
        images = self.graphics[f"on_{self.__speed}_speed"]
        self.__frame = (self.__frame + 1) % len(images)
        self.update()


    def update_status(self, status):
        """
        Updates the fan status to 'on', 'off', or 'fault'.
        """
        if status not in ["on", "off", "fault"]:
            raise ValueError("Invalid status. Must be 'on', 'off', or 'fault'.")
        self.__status = status
        self.__frame = 0
        self.update_fan_state()


    def update_speed(self, speed):
        """
        Updates the fan speed when the fan is 'on'.
        """
        if self.__status == "on":
            if speed.lower() not in ["low", "medium", "high"]:
                raise ValueError("Invalid speed. Must be 'low', 'medium', or 'high'.")
            self.__speed = speed.lower()
            self.__frame = 0
            self.start_fan_on()


"""*********************Main Routine***************************************"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.setWindowTitle("Fan Animation GUI")
    main_window.setGeometry(500, 500, 500, 500)

    # Create and show a fan object
    fan_graphic = Fan(status="on", speed="low", scale=1, 
                  pos_x=90, pos_y=120, instance=main_window)

    
    fan_graphic.show()

    main_window.show()
    sys.exit(app.exec_())
