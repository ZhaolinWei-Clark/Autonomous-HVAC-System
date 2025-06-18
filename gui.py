"""***************************************************************************
Title:          GUI
File:           gui.py
Release Notes:  N/A
Author:         Zhaolin Wei
Description:    This file is to operate the entirety of the GUI, calling on
                additional GUI related files as necessary as well as 
                communications with the controller.
***************************************************************************"""

"""*********************Libraries******************************************"""
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget 
from PyQt5.QtWidgets import QAction, QTabWidget, QVBoxLayout, QGridLayout 
from PyQt5.QtWidgets import QLabel, QDoubleSpinBox, QTimeEdit, QDateEdit
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot, QDate, QTime, QTimer
import symbols
import damper
import heating_cooling
import fan
import controller


"""*********************Classes********************************************"""
'========================================='
class MainWindow(QMainWindow):
    """
    Main application window with tabs.
    """
    def __init__(self, controller):
        """
        Initialize the main window with tabs.
        """
        # Initialize the window
        super().__init__()
        self.setWindowTitle("Home Automation System")
        self.resize(1000, 600)
        
        # Tab Widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        # Initialize or set up initial data in the controller
        self.controller = controller
        
        # Tabs
        self.overview_tab = OverviewWindow(self)
        self.tab_widget.addTab(self.overview_tab, "Overview")
        
        self.mechanical_tab = MechanicalWindow(self)
        self.tab_widget.addTab(self.mechanical_tab, "Mechanical Room")
        
        self.ground_tab = GroundWindow(self)
        self.tab_widget.addTab(self.ground_tab, "Ground Floor")
        
        self.basement_tab = BasementWindow(self)
        self.tab_widget.addTab(self.basement_tab, "Basement")
        
        self.settings_tab = SettingsWindow(self)
        self.tab_widget.addTab(self.settings_tab, "Settings")

        # Connect the signal to update_tab method
        self.tab_widget.currentChanged.connect(self.update_tab)
        
        # Initiate operations
        #self.controller.start_operation_heating_cooling(
        #    22.0, "2024-01-01", "0:00")
        # 添加一个定时器来定期刷新GUI
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_all_tabs)
        self.timer.start(1000) # 每1000毫秒（1秒）刷新一次
        
    def update_all_tabs(self):
        self.update_tab
        
    def update_tab(self):
        """
        Updates the tab properties based on the selected tab.
        """
        current_index = self.tab_widget.currentIndex()
        
        if current_index == 0:  # Overview tab
            self.overview_tab.update_tab(self.controller)
        elif current_index == 1:  # Mechanical tab
            self.mechanical_tab.update_tab(self.controller)
        elif current_index == 2:  # Ground tab
            self.ground_tab.update_tab(self.controller)
        elif current_index == 3:  # Basement tab
            self.basement_tab.update_tab(self.controller)
        elif current_index == 4:  # Settings tab
            self.settings_tab.update_tab(self.controller)
            
        self.repaint

'========================================='
class OverviewWindow(QWidget):
    """
    Overview window displaying home overview graphics.
    """
    def __init__(self, parent, bdrm_1_temp=20, bdrm_2_temp=20, bdrm_3_temp=20, 
                 bath_1_temp=20, bath_2_temp=20, living_temp=20, 
                 kitchen_temp=20, mech_rm_temp=20, rec_rm_temp=20,
                 temp_out=20, date="2024-10-13", time="3:00 pm",
                 mode = "Normal",
                 furnace_status="Fault", furnace_energy = 0,
                 aircon_status="Fault", aircon_energy = 0,
                 fan_status="Fault", airflow=0,
                 damp_sup_pos=0, damp_ret_pos=0, damp_out_pos=0):
        """
        Initiate the overview GUI and illustrate the home overview graphics.
        
        parent: Reference to the MainWindow class.
        bdrm_1_temp: Sensor temperature of bedroom 1 (float)
        bdrm_2_temp: Sensor temperature of bedroom 2 (float)
        bdrm_3_temp: Sensor temperature of bedroom 3 (float)
        bath_1_temp: Sensor temperature of bathroom 1 (float)
        bath_2_temp: Sensor temperature of bathroom 2 (float)
        living_temp:  Sensor temperature of the living room (float)
        kitchen_temp: Sensor temperature of the kitchen (float)
        mech_rm_temp: Sensor temperature of the mechanical room (float)
        rec_rm_temp: Sensor temperature of the recreational room (float)
        temp_out: Sensor temperature of the outdoor air (float)
        date: Date of the system (yyyy-mm-dd)
        time: Time of the system (hh:mm)
        mode: Either of Heating/Cooling/Normal/Fault (string)
        furnace_status: Status of the furnace of either On/Off/Fault (string)
        furnace_energy: Output energy of the furnace (float)
        aircon_status: Status of the aircon of either On/Off/Fault (string)
        aircon_energy: Output energy of the air conditioner (string)
        fan_status: Status of the fan of either High/Low/Off/Fault (string)
        airflow: Output airflow of the fan (float)
        damp_sup_pos: Supply damper position (0-100 or -1 for fault, int).
        damp_ret_pos: Return damper position (0-100 or -1 for fault, int).
        damp_out_pos: Fresh air damper position (0-100 or -1 for fault, int).
        """
        # Create a QGridLayout and set it for the central widget
        super(QWidget, self).__init__(parent)
        grid_layout = QGridLayout()
        central_widget = QWidget(self)
        central_widget.setLayout(grid_layout)
        
        # Initialize Variables
        self.bdrm_1_temp = bdrm_1_temp
        self.bdrm_2_temp = bdrm_2_temp
        self.bdrm_3_temp = bdrm_3_temp
        self.bath_1_temp = bath_1_temp
        self.bath_2_temp = bath_2_temp
        self.living_temp = living_temp
        self.kitchen_temp = kitchen_temp
        self.mech_rm_temp = mech_rm_temp
        self.rec_rm_temp = rec_rm_temp
        self.temp_out = temp_out
        self.date = date
        self.time = time
        self.mode = mode
        self.aircon_energy = aircon_energy
        self.aircon_status = aircon_status
        self.furnace_energy = furnace_energy
        self.furnace_status = furnace_status
        self.fan_status = fan_status
        self.airflow = airflow
        self.damp_sup_pos = damp_sup_pos
        self.damp_ret_pos = damp_ret_pos
        self.damp_out_pos = damp_out_pos
        
        # Alarms
        if self.damp_sup_pos==0 and self.damp_ret_pos==0 and damp_out_pos==0:
            self.alert = "Fault"
        else:
            self.alert = "Normal"
                
        # Sheet Format      
        symbols.add_image(file="Layout/House_Ground.png", 
                          scale=1/2.25, instance=self, 
                          size_x=700, size_y=426, pos_x=150, pos_y=90)
        symbols.add_image(file="Layout/House_Basement.png", 
                          scale=1/2.25, instance=self, 
                          size_x=700, size_y=426, pos_x=150, pos_y=310)
        symbols.add_text("HOME OVERVIEW", font="title", instance=self,
                         size_x=500, size_y=60, pos_x=60, pos_y=0)
                
        # Uncontrolled Properties
        symbols.add_text("Time:", font="text", instance=self,
                         size_x=200, size_y=30, pos_x=800, pos_y=40)
        symbols.Symbols("time value", scale=0.8, instance=self,
                        value=self.time, pos_x=850, pos_y=45)
        symbols.add_text("Date:", font="text", instance=self,
                         size_x=200, size_y=30, pos_x=800, pos_y=10)
        symbols.Symbols("time value", scale=0.8, instance=self,
                        value=self.date, pos_x=850, pos_y=15)
        symbols.add_text("O/A Temp.:", font="text", instance=self,
                         size_x=200, size_y=30, pos_x=150, pos_y=50)
        symbols.Symbols("temp value", scale=0.8, instance=self,
                        value=self.temp_out, pos_x=230, pos_y=55)
                
        # Ground Floor
        symbols.add_text("GROUND FLOOR", font="text", instance=self,
                         size_x=200, size_y=30, pos_x=260, pos_y=275)
        symbols.Symbols("temp value", scale=0.8, instance=self,
                        value=self.bdrm_1_temp, pos_x=290, pos_y=220)
        symbols.Symbols("temp value", scale=0.8, instance=self,
                        value=self.bdrm_2_temp, pos_x=170, pos_y=95) 
        symbols.Symbols("temp value", scale=0.8, instance=self,
                        value=self.bath_1_temp, pos_x=290, pos_y=95)
        symbols.Symbols("temp value", scale=0.8, instance=self,
                        value=self.living_temp, pos_x=170, pos_y=220)
        symbols.Symbols("temp value", scale=0.8, instance=self,
                        value=self.kitchen_temp, pos_x=385, pos_y=140)
                
        # Basement
        symbols.add_text("BASEMENT", font="text", instance=self,
                         size_x=200, size_y=30, pos_x=260, pos_y=500)
        symbols.Symbols("temp value", scale=0.8, instance=self,
                        value=self.bdrm_3_temp, pos_x=160, pos_y=320)
        symbols.Symbols("temp value", scale=0.8, instance=self,
                        value=self.bath_2_temp, pos_x=260, pos_y=320)
        symbols.Symbols("temp value", scale=0.8, instance=self,
                        value=self.mech_rm_temp, pos_x=350, pos_y=320)
        symbols.Symbols("temp value", scale=0.8, instance=self,
                        value=self.rec_rm_temp, pos_x=270, pos_y=420)      
        
        # Operations
        symbols.add_text("OPERATIONS", font="subtitle", instance=self,
                         size_x=250, size_y=45, pos_x=550, pos_y=140)
        
        # Furnace
        symbols.add_text("FURNACE", font="text", instance=self,
                         size_x=200, size_y=30, pos_x=550, pos_y=180)
        symbols.Symbols("state value", scale=0.8, instance=self,
                        value=self.furnace_status, pos_x=675, pos_y=180) 
        symbols.Symbols("energy value", scale=0.8, instance=self,
                        value=self.furnace_energy, pos_x=750, pos_y=180)  
        
        # Air Conditioner
        symbols.add_text("AIR CONDITIONER", font="text", instance=self,
                         size_x=200, size_y=30, pos_x=550, pos_y=220)
        symbols.Symbols("state value", scale=0.8, instance=self,
                        value=self.aircon_status, pos_x=675, pos_y=220) 
        symbols.Symbols("energy value", scale=0.8, instance=self,
                        value=self.aircon_energy, pos_x=750, pos_y=220) 
        
        # Fan
        symbols.add_text("FAN", font="text", instance=self,
                         size_x=200, size_y=30, pos_x=550, pos_y=260)
        symbols.Symbols("state value", scale=0.8, instance=self,
                        value=self.fan_status, pos_x=675, pos_y=260) 
        symbols.Symbols("airflow value", scale=0.8, instance=self,
                        value=self.airflow, pos_x=750, pos_y=260) 
                
        # Alarms
        symbols.add_text("ALARMS", font="subtitle", instance=self,
                         size_x=200, size_y=45, pos_x=550, pos_y=340)
        symbols.add_text("SYSTEM STATUS", font="text", instance=self,
                         size_x=200, size_y=30, pos_x=550, pos_y=380)
        symbols.Symbols("state value", scale=0.8, instance=self,
                        value=self.alert, pos_x=675, pos_y=380) 
        
    def update_tab(self, controller):
        """
        Updates the tab properties.
        
        controller: Instance of controller running software (class)
        """
        # Get system overview as a list
        system_data = controller.system_overview()
        
        tab_data = [self.bdrm_1_temp, self.bdrm_2_temp, self.bdrm_3_temp,
                    self.bath_1_temp, self.bath_2_temp,
                    self.living_temp, self.kitchen_temp,
                    self.mech_rm_temp, self.rec_rm_temp,
                    self.temp_out, self.date, self.time, self.mode,
                    self.furnace_status, self.furnace_energy,
                    self.aircon_status, self.aircon_energy,
                    self.fan_status, self.damp_sup_pos, 
                    self.damp_ret_pos, self.damp_out_pos]
        
        # Unpack the list into the corresponding attributes
        for i in range(len(system_data)):
            tab_data[i] = system_data[i]
        

'========================================='
class MechanicalWindow(QWidget):
    """
    Generates the GUI window for the mechanical room.
    """
    def __init__(self, parent, aircon_status="Fault", aircon_energy=0,
                 furnace_status="Fault",  furnace_energy=200,
                 fan_status="Off", fan_speed="Off", airflow=0,
                 damp_sup_pos=-1, damp_ret_pos=-1, damp_out_pos=-1, 
                 temp_sup=20, temp_ret=20, temp_out=20, 
                 date="2024-10-13", time= "3:00 pm"):
        """
        Initiates the GUI window with all objects in place.
        
        parent: Reference to the MainWindow class.
        furnace_status: Status of the furnace of either On/Off/Fault (string)
        furnace_energy: Output energy of the furnace (float)
        aircon_status: Status of the aircon of either on/off/fault (string)
        aircon_energy: Output energy of the air conditioner (float)
        fan_status: Status of the fan of either high/low/off/fault (string)
        airflow: System airflow speed (float)
        damp_sup_pos: Supply damper position (0-100 or -1 for fault, int)
        damp_ret_pos: Return damper position (0-100 or -1 for fault, int)
        damp_out_pos: Fresh air damper position (0-100 or -1 for fault, int)
        temp_sup: Supply air temperature (float)
        temp_ret: Return air temperature (float)
        temp_out: Outdoor air temperature (float)
        date: Date of the system (yyyy-mm-dd)
        time: Time of the system (hh:mm)
        """
        # Create a QGridLayout and set it for the central widget
        super(QWidget, self).__init__(parent)
        grid_layout = QGridLayout()
        central_widget = QWidget(self)
        central_widget.setLayout(grid_layout)
                
        # Initialize variables
        self.aircon_energy = aircon_energy
        self.aircon_status = aircon_status
        self.furnace_energy = furnace_energy
        self.furnace_status = furnace_status
        self.fan_status = fan_status
        self.fan_speed = fan_speed
        self.damp_sup_pos = damp_sup_pos
        self.damp_ret_pos = damp_ret_pos
        self.damp_out_pos = damp_out_pos
        self.temp_sup = temp_sup
        self.temp_ret = temp_ret
        self.temp_out = temp_out
        self.airflow = airflow
        self.date = date
        self.time = time
                
        # Sheet Format
        symbols.add_image(file="Layout/Mech_Schematic.png", scale=1, 
                          instance=self, size_x=900, size_y=500, 
                          pos_x=50, pos_y=50)
        symbols.add_text(label="MECHANICAL ROOM", font="title", instance=self, 
                         size_x=500, size_y=60, pos_x=60, pos_y=0)
                        
        # Uncontrolled Properties
        symbols.add_text("Time:", font="text", instance=self,
                         size_x=200, size_y=30, pos_x=800, pos_y=40)
        symbols.Symbols("time value", scale=0.8, instance=self,
                        value=self.time, pos_x=850, pos_y=45)
        symbols.add_text("Date:", font="text", instance=self,
                         size_x=200, size_y=30, pos_x=800, pos_y=10)
        symbols.Symbols("time value", scale=0.8, instance=self,
                        value=self.date, pos_x=850, pos_y=15)
                
        # Supply Air
        symbols.add_text(label="Supply Air", font="text", instance=self, 
                         size_x=180, size_y=30, pos_x=665, pos_y=40)
        damper.Damper(status=self.damp_sup_pos, scale=.35, 
                      pos_x=800, pos_y=120, angle=90, instance=self)
        symbols.Symbols("damper value", value=self.damp_sup_pos, scale=0.7, 
                        pos_x=780, pos_y=75, instance=self)
        symbols.Symbols("airflow", scale=.5, pos_x=575, pos_y=70, 
                        instance=self)
        symbols.Symbols("airflow value", value=self.airflow, scale=0.7, 
                        pos_x=490, pos_y=75, instance=self)
        symbols.Symbols("temperature", scale=.5, pos_x=620, pos_y=70, 
                        instance=self)
        symbols.Symbols("temp value", value=self.temp_sup, scale=0.7, 
                        pos_x=665, pos_y=75, instance=self)
        
        # Return Air
        symbols.add_text(label="Return Air", font="text", instance=self, 
                         size_x=180, size_y=30, pos_x=50, pos_y=340)
        damper.Damper(status=self.damp_ret_pos, scale=.35, 
                      pos_x=220, pos_y=217, angle=90, instance=self)
        symbols.Symbols("damper value", value=self.damp_ret_pos, scale=0.7, 
                        pos_x=120, pos_y=380, instance=self)
        symbols.Symbols("temperature", scale=.5, pos_x=158, pos_y=300, 
                        instance=self)
        symbols.Symbols("temp value", value=self.temp_ret, scale=0.7, 
                        pos_x=120, pos_y=340, instance=self)
                
        # Outdoor Air
        symbols.add_text(label="Outdoor Air", font="text", instance=self, 
                         size_x=180, size_y=50, pos_x=120, pos_y=90)
        damper.Damper(status=self.damp_out_pos, scale=.35, 
                      pos_x=253, pos_y=170, angle=0, instance=self)
        symbols.Symbols("damper value", value=self.damp_out_pos, scale=0.7, 
                        pos_x=120, pos_y=170, instance=self)
        symbols.Symbols("temperature", scale=.5, pos_x=205, pos_y=128, 
                        instance=self)
        symbols.Symbols("temp value", value=self.temp_sup, scale=0.7, 
                        pos_x=120, pos_y=130, instance=self)
                
        # Heating/Cooling
        heating_cooling.Aircon(status=self.aircon_status, 
                               energy=self.aircon_energy, scale=.5, 
                               pos_x=700, pos_y=285, instance=self)
        heating_cooling.Furnace(status=self.furnace_status, 
                                energy=self.furnace_energy, scale=.5, 
                                pos_x=450, pos_y=285, instance=self)
        
        # Fan
        fan.Fan(status=self.fan_status, speed=self.fan_speed, scale=0.60, 
                pos_x=290, pos_y=430, instance=self)
        
    def update_tab(self, controller):
        """
        Updates the tab properties.
        
        controller: Instance of controller running software (class)
        """
        # Get system overview as a tuple
        system_data = controller.mechanical_room()
        
        tab_data = [self.furnace_status, self.furnace_energy,
                    self.aircon_status, self.aircon_energy,
                    self.fan_status, self.fan_speed, self.airflow,
                    self.damp_sup_pos, self.damp_ret_pos, self.damp_out_pos,
                    self.temp_sup, self.temp_ret, self.temp_out]
                
        # Unpack the list into the corresponding attributes
        for i in range(len(system_data)):
            tab_data[i] = system_data[i]
        
        
'========================================='
class GroundWindow(QWidget):
    """
    Generates the GUI window for the ground floor with temperature controls.
    """
    def __init__(self, parent, bdrm_1_temp=20, bdrm_1_damper=-1,
                 bdrm_2_temp=20, bdrm_2_damper=-1,
                 bath_1_temp=20, bath_1_damper=-1,
                 living_temp=20, living_damper=-1,
                 kitchen_temp=20, kitchen_damper=-1, temp_setpoint=20,
                 date="2024-10-13", time= "3:00 pm", temp_out = 10):
        """
        Initiates the GUI window with all objects in place.
        
        parent: Reference to the MainWindow class
        bdrm_1_temp: Sensor temperature of bedroom 1 (float)
        bdrm_1_damper: Damper position of bedroom 1 (int)
        bdrm_2_temp: Sensor temperature of bedroom 2 (float)
        bdrm_2_damper: Damper position of bedroom 2 (int)
        bath_1_temp: Sensor temperature of bathroom 1 (float)
        bath_1_damper: Damper position of bathroom 1 (int)
        living_temp:  Sensor temperature of the living room (float)
        living_damper: Damper position of the living room (int)
        kitchen_temp: Sensor temperature of the kitchen (float)
        kitchen_damper: Damper position of the kitchen (int)
        temp_setpoint: Temperature setpoint of the house (float)
        date: Date of the system (yyyy-mm-dd)
        time: Time of the system (hh:mm)
        temp_out: Outdoor air temperature (float)
        controller: Instance of controller running software (class)
        
        Note: Updates and setpoint gui made with Microsoft Copilot
        """
        # Create a QGridLayout and set it for the central widget
        super(QWidget, self).__init__(parent)
        grid_layout = QGridLayout()
        central_widget = QWidget(self)
        central_widget.setLayout(grid_layout)
        
        # Initialize Variables
        self.bdrm_1_temp = bdrm_1_temp
        self.bdrm_2_temp = bdrm_2_temp
        self.bath_1_temp = bath_1_temp
        self.living_temp = living_temp
        self.kitchen_temp = kitchen_temp
        self.date = date
        self.time = time
        self.bdrm_1_damper = bdrm_1_damper
        self.bdrm_2_damper = bdrm_2_damper
        self.bath_1_damper = bath_1_damper
        self.living_damper = living_damper
        self.kitchen_damper = kitchen_damper
        self.temp_setpoint = temp_setpoint
        self.temp_out = temp_out
        
        # Sheet Format      
        symbols.add_image(file="Layout/House_Ground.png", 
                          scale=.85, instance=self, 
                          size_x=900, size_y=500, pos_x=70, pos_y=70)
        symbols.add_image(file="Layout/Ground_HVAC.png", 
                          scale=.85, instance=self, 
                          size_x=900, size_y=500, pos_x=70, pos_y=70)
        symbols.add_text("GROUND FLOOR", font="title", instance=self,
                         size_x=500, size_y=60, pos_x=60, pos_y=0)
                
        # Uncontrolled Properties
        symbols.add_text("Time:", font="text", instance=self,
                         size_x=200, size_y=30, pos_x=800, pos_y=40)
        symbols.Symbols("time value", scale=0.8, instance=self,
                        value=self.time, pos_x=850, pos_y=45)
        symbols.add_text("Date:", font="text", instance=self,
                         size_x=200, size_y=30, pos_x=800, pos_y=10)
        symbols.Symbols("time value", scale=0.8, instance=self,
                        value=self.date, pos_x=850, pos_y=15)

        # Home Setpoint
        symbols.add_text(label="Setpoint", font="text", instance=self, 
                         size_x=200, size_y=30, pos_x=785, pos_y=95)
        self.setpoint_spinbox = symbols.Symbols.spinbox_sp(self, 18, 25, 
                                                         self.temp_setpoint, 
                                                         "°C", 0.5, 
                                                         80, 40, 850, 90)
 
        # Bedroom 1
        # Room Title
        symbols.add_text(label="Bedroom 1", font="subtitle", instance=self, 
                         size_x=240, size_y=45, pos_x=350, pos_y=340)
        # Temp Output
        symbols.add_text(label="Temp.", font="text", instance=self, 
                         size_x=180, size_y=30, pos_x=380, pos_y=440)
        symbols.Symbols("temp value", scale=0.7, instance=self,
                        value=self.bdrm_1_temp, pos_x=435, pos_y=440)
        # Damper
        damper.Damper(status=self.bdrm_1_damper, scale=.2, 
                      pos_x=295, pos_y=425, angle=90, instance=self)
        symbols.Symbols("damper value", value=self.bdrm_1_damper, scale=0.5, 
                        pos_x=295, pos_y=405, instance=self)
                
        # Bedroom 2
        # Room title
        symbols.add_text(label="Bedroom 2", font="subtitle", instance=self, 
                         size_x=240, size_y=45, pos_x=100, pos_y=70)
        # Temperature Output
        symbols.add_text(label="Temp.", font="text", instance=self, 
                         size_x=180, size_y=30, pos_x=145, pos_y=165)
        symbols.Symbols("temp value", scale=0.7, instance=self,
                        value=self.bdrm_2_temp, pos_x=200, pos_y=165) 
        # Damper
        damper.Damper(status=self.bdrm_2_damper, scale=.2, 
                      pos_x=348, pos_y=125, angle=90, instance=self)
        symbols.Symbols("damper value", value=self.bdrm_2_damper, scale=0.5, 
                        pos_x=328, pos_y=105, instance=self)
                
        # Bathroom 1
        # Room title
        symbols.add_text(label="Bathroom 1", font="subtitle", instance=self, 
                         size_x=250, size_y=45, pos_x=385, pos_y=70)
        # Temperature Output
        symbols.add_text(label="Temp.", font="text", instance=self, 
                         size_x=180, size_y=30, pos_x=435, pos_y=165)
        symbols.Symbols("temp value", scale=0.7, instance=self,
                        value=self.bath_1_temp, pos_x=490, pos_y=165)
        # Damper
        damper.Damper(status=self.bath_1_damper, scale=.2, 
                      pos_x=372, pos_y=125, angle=90, instance=self)
        symbols.Symbols("damper value", value=self.bath_1_damper, scale=0.5, 
                        pos_x=372, pos_y=105, instance=self)
             
        # Living Room
        # Room title
        symbols.add_text(label="Living Room", font="subtitle", instance=self, 
                         size_x=250, size_y=45, pos_x=120, pos_y=210)
        # Temperature
        symbols.add_text(label="Temp.", font="text", instance=self, 
                         size_x=180, size_y=30, pos_x=145, pos_y=295)
        symbols.Symbols("temp value", scale=0.7, instance=self,
                        value=self.living_temp, pos_x=200, pos_y=295)
        # Dampers
        damper.Damper(status=self.living_damper, scale=.2, 
                      pos_x=270, pos_y=425, angle=90, instance=self)
        symbols.Symbols("damper value", value=self.living_damper, scale=0.5, 
                        pos_x=245, pos_y=405, instance=self)
        damper.Damper(status=self.living_damper, scale=.2, 
                      pos_x=350, pos_y=210, angle=0, instance=self)
        symbols.Symbols("damper value", value=self.living_damper, scale=0.5, 
                        pos_x=305, pos_y=210, instance=self)
                 
        # Kitchen
        # Room title
        symbols.add_text(label="Kitchen", font="subtitle", instance=self, 
                         size_x=250, size_y=45, pos_x=595, pos_y=70)
        # Temperature Output
        symbols.add_text(label="Temp.", font="text", instance=self, 
                         size_x=180, size_y=30, pos_x=605, pos_y=175)
        symbols.Symbols("temp value", scale=0.7, instance=self,
                        value=self.kitchen_temp, pos_x=670, pos_y=175)
        # Dampers
        damper.Damper(status=self.kitchen_damper, scale=.2, 
                      pos_x=740, pos_y=212, angle=90, instance=self)
        symbols.Symbols("damper value", value=self.kitchen_damper, scale=0.5, 
                        pos_x=720, pos_y=258, instance=self)  
        damper.Damper(status=self.kitchen_damper, scale=.2, 
                      pos_x=680, pos_y=470, angle=0, instance=self)
        symbols.Symbols("damper value", value=self.kitchen_damper, scale=0.5, 
                        pos_x=640, pos_y=470, instance=self)  
        
    def update_tab(self, controller):
        """
        Updates the tab properties.
        
        controller: Instance of controller running software (class)
        """      
        # Connect changed values to the controller using one method
        self.setpoint_spinbox.valueChanged.connect(
            lambda value: controller.control_temperature(value, self.temp_out)
        )
        # Get system overview as a list
        system_data = controller.ground_floor()
        
        tab_data = [self.bdrm_1_temp, self.bdrm_1_damper,
                    self.bdrm_2_temp, self.bdrm_2_damper,
                    self.bath_1_temp, self.bath_1_damper,
                    self.living_temp, self.living_damper,
                    self.kitchen_temp, self.kitchen_damper,
                    self.temp_setpoint, self.temp_out]
                
        # Unpack the list into the corresponding attributes
        for i in range(len(system_data)):
            tab_data[i] = system_data[i]
            
            
'========================================='
class BasementWindow(QWidget):
    """
    Generates the GUI window for the basement with temperature controls.
    """
    def __init__(self, parent, bdrm_3_temp=20, bdrm_3_damper=-1,
                 bath_2_temp=20, bath_2_damper=-1,
                 mech_rm_temp=20,  mech_rm_damper=-1,
                 rec_rm_temp=20, rec_rm_damper=-1, temp_setpoint=20,
                 date="2024-10-13", time= "3:00 pm", temp_out = 10):
        """
        Initiates the GUI window with all objects in place.
        
        parent: Reference to the MainWindow class.
        bdrm_3_temp: Sensor temperature of bedroom 3 (float)
        bdrm_3_damper: Damper position of bedroom 3 (int)
        bath_2_temp: Sensor temperature of bathroom 2 (float)
        bath_2_damper: Damper position of bathroom 2 (int)
        mech_rm_temp: Sensor temperature of mechanical room (float)
        mech_rm_damper: Damper position of mechanical room (int)
        rec_rm_temp:  Sensor temperature of the rec room (float)
        rec_rm_damper: Damper position of the rec room (int)
        temp_setpoint: Setpoint temperature of the house (float)
        date: Date of the system (yyyy-mm-dd)
        time: Time of the system (hh:mm)
        controller: Instance of controller running software (class)
        """
        # Create a QGridLayout and set it for the central widget
        super(QWidget, self).__init__(parent)
        grid_layout = QGridLayout()
        central_widget = QWidget(self)
        central_widget.setLayout(grid_layout)

        # Initialize Variables
        self.bdrm_3_temp = bdrm_3_temp
        self.bath_2_temp = bath_2_temp
        self.mech_rm_temp = mech_rm_temp
        self.rec_rm_temp = rec_rm_temp
        self.date = date
        self.time = time
        self.bdrm_3_damper = bdrm_3_damper
        self.bath_2_damper = bath_2_damper
        self.mech_rm_damper = mech_rm_damper
        self.rec_rm_damper = rec_rm_damper
        self.temp_setpoint = temp_setpoint
        self.temp_out = temp_out
    
        # Sheet Format      
        symbols.add_image(file="Layout/House_Basement.png", 
                          scale=.85, instance=self, 
                          size_x=900, size_y=500, pos_x=70, pos_y=70)
        symbols.add_image(file="Layout/Basement_HVAC.png", 
                          scale=.85, instance=self, 
                          size_x=900, size_y=500, pos_x=70, pos_y=70)
        symbols.add_text("Basement", font="title", instance=self,
                         size_x=500, size_y=60, pos_x=60, pos_y=0)

        # Uncontrolled Properties
        symbols.add_text("Time:", font="text", instance=self,
                         size_x=200, size_y=30, pos_x=800, pos_y=40)
        symbols.Symbols("time value", scale=0.8, instance=self,
                        value=self.time, pos_x=850, pos_y=45)
        symbols.add_text("Date:", font="text", instance=self,
                         size_x=200, size_y=30, pos_x=800, pos_y=10)
        symbols.Symbols("time value", scale=0.8, instance=self,
                        value=self.date, pos_x=850, pos_y=15)
    
        #Home Setpoint
        symbols.add_text(label="Setpoint", font="text", instance=self, 
                         size_x=200, size_y=30, pos_x=785, pos_y=95)
        self.setpoint_spinbox = symbols.Symbols.spinbox_sp(self, 18, 25, 
                                                         self.temp_setpoint, 
                                                         "°C", 0.5, 
                                                         80, 40, 850, 90)
        
        # Bedroom 3
        # Room title
        symbols.add_text(label="Bedroom 3", font="subtitle", instance=self, 
                         size_x=240, size_y=45, pos_x=100, pos_y=70)
        # Temperature Output
        symbols.add_text(label="Temp.", font="text", instance=self, 
                         size_x=180, size_y=30, pos_x=145, pos_y=150)
        symbols.Symbols("temp value", scale=0.7, instance=self,
                        value=self.bdrm_3_temp, pos_x=200, pos_y=150) 
        # Damper
        damper.Damper(status=self.bdrm_3_damper, scale=.2, 
                      pos_x=315, pos_y=165, angle=90, instance=self)
        symbols.Symbols("damper value", value=self.bdrm_3_damper, scale=0.5, 
                        pos_x=300, pos_y=145, instance=self)  

        # Bath 2
        # Room title
        symbols.add_text(label="Bathroom 2", font="subtitle", instance=self, 
                         size_x=240, size_y=45, pos_x=265, pos_y=30)
        # Temperature output
        symbols.add_text(label="Temp.", font="text", instance=self, 
                         size_x=180, size_y=30, pos_x=410, pos_y=45) 
        symbols.Symbols("temp value", scale=0.7, instance=self,
                        value=self.bath_2_temp, pos_x=465, pos_y=45)
        # Damper
        damper.Damper(status=self.bath_2_damper, scale=.2, 
                      pos_x=399, pos_y=202, angle=0, instance=self)
        symbols.Symbols("damper value", value=self.bath_2_damper, scale=0.5, 
                        pos_x=440, pos_y=202, instance=self)  
        
        # Mechanical Room
        # Title of the room
        symbols.add_text(label="Mechanical", font="subtitle", instance=self,
                         size_x=250, size_y=45, pos_x=510, pos_y=70)
        # Temperature output
        symbols.add_text(label="Temp.", font="text", instance=self, 
                         size_x=160, size_y=30, pos_x=510, pos_y=145)            
        symbols.Symbols("temp value", scale=0.7, instance=self,
                        value=self.mech_rm_temp, pos_x=565, pos_y=145)
        # Damper
        damper.Damper(status=self.mech_rm_damper, scale=.2, 
                      pos_x=720, pos_y=140, angle=90, instance=self)
        symbols.Symbols("damper value", value=self.mech_rm_damper, scale=0.5, 
                        pos_x=720, pos_y=120, instance=self)  

        # Recreational Room
        # Room Title
        symbols.add_text(label="Rec. Room", font="subtitle", instance=self, 
                         size_x=240, size_y=45, pos_x=350, pos_y=430)
        # Temperature output
        symbols.add_text(label="Temp.", font="text", instance=self, 
                         size_x=180, size_y=30, pos_x=330, pos_y=355)
        symbols.Symbols("temp value", scale=.7, instance=self,
                        value=self.rec_rm_temp, pos_x=380, pos_y=355)
        # Dampers
        damper.Damper(status=self.rec_rm_damper, scale=.2, 
                      pos_x=162, pos_y=400, angle=90, instance=self)
        symbols.Symbols("damper value", value=self.rec_rm_damper, scale=0.5, 
                        pos_x=162, pos_y=380, instance=self)  
        damper.Damper(status=self.rec_rm_damper, scale=.2, 
                      pos_x=465, pos_y=386, angle=0, instance=self)
        symbols.Symbols("damper value", value=self.rec_rm_damper, scale=0.5, 
                        pos_x=515, pos_y=386, instance=self)  
        
    def update_tab(self, controller):
        """
        Updates the tab properties.
                
        controller: Instance of controller running software (class)
        """        
        # Connect changed values to the controller using one method
        self.setpoint_spinbox.valueChanged.connect(
            lambda value: controller.control_temperature(value,self.temp_out))
        
        # Get system overview as a tuple
        system_data = controller.basement()
        
        tab_data = [self.bdrm_3_temp, self.bdrm_3_damper,
                    self.bath_2_temp, self.bath_2_damper,
                    self.mech_rm_temp, self.mech_rm_damper,
                    self.rec_rm_temp, self.rec_rm_damper,
                    self.temp_setpoint, self.temp_out]
                
        # Unpack the list into the corresponding attributes
        for i in range(len(system_data)):
            tab_data[i] = system_data[i]
        

'========================================='
class SettingsWindow(QWidget):
    """
    Generates the GUI window for the writable settings.
    """
    def __init__(self, parent, date="2024-10-13", 
                 time= "3:00 pm", mode = "Off"):
        """
        Initiates the GUI window with all objects in place.
        
        parent: Reference to the MainWindow class (self)
        date: Date of the system (yyyy-mm-dd)
        time: Time of the system (hh:mm)
        mode: Setting of the system (string)
        
        Note: Made in part with Microsoft Copilot for date edit and buttons
        """
        # Create a QGridLayout and set it for the central widget
        super(QWidget, self).__init__(parent)
        grid_layout = QGridLayout()
        central_widget = QWidget(self)
        central_widget.setLayout(grid_layout)
        
        # Initialize variables
        self.date = date
        self.time = time
        self.mode = mode
        
        # Sheet format
        symbols.add_text(label="SETTINGS", font="title", instance=self, 
                         size_x=500, size_y=60, pos_x=60, pos_y=0)
                
        # Date edit 
        self.date_edit = QDateEdit(self) 
        self.date_edit.setDate(QDate.fromString(self.date, "yyyy-MM-dd")) 
        self.date_edit.dateChanged.connect(self.update_date) 
        symbols.add_text(label="Edit date:", font="subtitle", instance=self, 
                         size_x=250, size_y=45, pos_x=100, pos_y=100)
        self.date_edit.setGeometry(250, 110, 120, 25)
                
        # Time edit 
        self.time_edit = QTimeEdit(self) 
        self.time_edit.setTime(QTime.fromString(self.time, "h:mm ap")) 
        self.time_edit.timeChanged.connect(self.update_time) 
        symbols.add_text(label="Edit time:", font="subtitle", instance=self, 
                         size_x=250, size_y=45, pos_x=100, pos_y=150)
        self.time_edit.setGeometry(250, 160, 120, 25) 
        
    def update_date(self, qdate): 
        """
        Updates the date, returns a value to the controller.
        
        qdate: The newly adjusted date (yyyy-mm-dd)
        """
        self.date = qdate.toString("yyyy-MM-dd") 
        controller.update_date(self.date) 
            
    def update_time(self, qtime): 
        """
        Updates the time, returns a value to the controller.
        
        qtime: The newly adjusted time (hh:mm)
        """
        self.time = qtime.toString("h:mm ap") 
        controller.update_time(self.time)
    
    def update_tab(self, controller):
        """
        Updates the tab properties.
        
        controller: Instance of controller running software (class)
        """
        # Get system overview as a tuple
        system_data = controller.settings()
        print(system_data)
        tab_data = [self.date, self.time, self.mode]
                
        # Unpack the list into the corresponding attributes
        for i in range(len(system_data)):
            tab_data[i] = system_data[i]