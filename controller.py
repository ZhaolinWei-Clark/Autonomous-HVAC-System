"""***************************************************************************
Title:          Controller
File:           controller.py
Release Notes:  N/A
Author:         Zhaolin Wei
Description:    Controls method for the automated HVAC controls
***************************************************************************"""

"""*********************Libraries ******************************************"""
from model import Model, ThermostatModel, FanModel
from model import FurnaceModel, AirConditionerModel
import gui
from PyQt5.QtCore import QTime, QDate
import threading
import time


"""*********************Classes********************************************"""
class ThermostatController:
    def __init__(self):
        """
        Initialize the thermostat, fan, furnace, and air conditioner models.
        """
        try:
            
            # Initialize general properties taken input from gui
            self.date = "2024-01-01"
            self.time = "12:00"
            self.setpoint = 22

            # Initializing room variables to updated in controller
            self.aircon_status = "Off" # 0: Off and 1: On
            self.aircon_energy = 0
            self.furnace_status = 0 # 0: Off and 1: On
            self.furnace_energy = 0
            self.fan_status = "Off"
            self.fan_speed = "Low"
            self.damper = 100
            self.mode = "Normal mode"
            self.current_temp = 22
            self.airflow = 300
            self.damp_sup_pos = 100
            self.damp_ret_pos = 80
            self.damp_out_pos = 20

            # Outdoor temperature taken from simulation
            self.temp_out = 27

            # Ground Floor
            self.bdrm_1_temp = 22
            self.bdrm_1_damper = 100
            self.bdrm_2_temp = 22
            self.bdrm_2_damper = 100
            self.bath_1_temp = 22
            self.bath_1_damper = 100
            self.living_temp = 22
            self.living_damper = 100
            self.kitchen_temp = 22
            self.kitchen_damper = 100
            
            # Basement
            self.bdrm_3_temp = 22
            self.bdrm_3_damper = 100
            self.bath_2_temp = 22
            self.bath_2_damper = 100
            self.mech_rm_temp = 22
            self.mech_rm_damper = 100
            self.rec_rm_temp = 22
            self.rec_rm_damper = 100
            
        except Exception as e:
            print(f"Error initializing components: {e}")
            raise

    def system_overview(self):
        """
        Returns the mechanical room GUI properties.
        """
        try:
            return [self.bdrm_1_temp, self.bdrm_2_temp, self.bdrm_3_temp, 
                self.bath_1_temp, self.bath_2_temp, 
                self.living_temp, self.kitchen_temp, 
                self.mech_rm_temp, self.rec_rm_temp, 
                self.temp_out, self.date, self.time, self.mode, 
                self.furnace_status, self.furnace_energy, 
                self.aircon_status, self.aircon_energy, 
                self.fan_status, 
                self.damp_sup_pos, self.damp_ret_pos, self.damp_out_pos]
        except AttributeError as e:
            print(f"Missing attributes in system_overview: {e}")
            raise

    def mechanical_room(self):
        """
        Returns the mechanical room GUI properties.
        """
        try:
            return [self.furnace_status, self.furnace_energy, 
                self.aircon_status, self.aircon_energy, 
                self.fan_status, self.fan_speed, self.airflow, 
                self.damp_sup_pos, self.damp_ret_pos, self.damp_out_pos, 
                self.temp_out]
        except AttributeError as e:
            print(f"Missing attributes in mechanical_room: {e}")
            raise

    def ground_floor(self):
        """
        Returns the ground floor GUI properties.
        """
        try:
            return [self.bdrm_1_temp, self.bdrm_1_damper, 
                self.bdrm_2_temp, self.bdrm_2_damper, 
                self.bath_1_temp, self.bath_1_damper, 
                self.living_temp, self.living_damper, 
                self.kitchen_temp, self.kitchen_damper, 
                self.setpoint, self.temp_out]
        except AttributeError as e:
            print(f"Missing attributes in ground_floor: {e}")
            raise
    
    def basement(self):
        """
        Returns the basement GUI properties.
        """
        try:
            return [self.bdrm_3_temp, self.bdrm_3_damper, 
                self.bath_2_temp, self.bath_2_damper, 
                self.mech_rm_temp, self.mech_rm_damper,
                self.rec_rm_temp, self.rec_rm_damper, 
                self.setpoint, self.temp_out]
        except AttributeError as e:
            print(f"Missing attributes in basement: {e}")
            raise
            
    def settings(self):
        """
        Returns the ground floor GUI properties.
        """
        try:
            return [self.date, self.time, self.mode]
        except AttributeError as e:
            print(f"Missing attributes in ground_floor: {e}")
            raise

    def set_current_temperature_aircon(self):
        """
        Continuously  updates the value of all the features while cooling.
        """
        try:
            while not self.aircon.stop_polling:
                self.current_temp = self.aircon.read_current_temp()
                print(f"current_temp: {self.current_temp}")
                self.aircon_energy = self.aircon.read_q_aircon()

                # Update temperatures for all rooms
                self.bdrm_1_temp = self.current_temp
                self.bdrm_2_temp = self.current_temp
                self.bath_1_temp = self.current_temp
                self.living_temp = self.current_temp
                self.kitchen_temp = self.current_temp
                self.bdrm_3_temp = self.current_temp
                self.bath_2_temp = self.current_temp
                self.mech_rm_temp = self.current_temp
                self.rec_rm_temp = self.current_temp
                time.sleep(0.1)
            self.aircon_status = 0 
            self.fan_speed = "low"
        except Exception as e:
            print(f"Error in set_current_temperature_aircon: {e}")
        
    def set_current_temperature_furnace(self):
        """
        Continuously  updates the value of all the features while heating.
        """
        try:
            while not self.furnace.stop_polling:
                self.current_temp = self.furnace.read_current_temp()
                print(f"current_temp: {self.current_temp}")
                self.aircon_energy = self.aircon.read_q_aircon()

                # Update temperatures for all rooms
                self.bdrm_1_temp = self.current_temp
                self.bdrm_2_temp = self.current_temp
                self.bath_1_temp = self.current_temp
                self.living_temp = self.current_temp
                self.kitchen_temp = self.current_temp
                self.bdrm_3_temp = self.current_temp
                self.bath_2_temp = self.current_temp
                self.mech_rm_temp = self.current_temp
                self.rec_rm_temp = self.current_temp
                time.sleep(0.1)
            self.furnace_status = "Off"
            self.fan_speed = "low"
        except Exception as e:
            print(f"Error in set_current_temperature_furnace: {e}")

    def control_temperature(self):
        """
        Control the indoor temperature by heating or cooling as needed.
        """
        try:
            self.furnace.stop_polling = False
            self.aircon.stop_polling = False
            
            if self.setpoint > self.current_temp:
                print("Furnace started heating.")
                # Heating mode: Activate the furnace
                self.furnace_status = 1
                t1 = threading.Thread(target=self.furnace.heating, 
                                      args=(self.current_temp,self.setpoint,))
                t2 = threading.Thread(
                    target=self.set_current_temperature_furnace)
                t1.start()
                t2.start()
            elif self.setpoint < self.current_temp:
                print("Air Conditioner started cooling.")
                # Cooling mode: Activate the AC
                self.aircon_status=1
                t1 = threading.Thread(target=self.aircon.cooling, args=(
                    self.current_temp, self.setpoint,))
                t2 = threading.Thread(
                    target=self.set_current_temperature_aircon)
                t1.start()
                t2.start()
            else:
                # Optimal temperature, no action needed
                print("Temperature is already optimal. No action needed.")
        except Exception as e:
            print(f"Error in temperature control: {e}")
            
    def start_hvac_simulation_thread(self):
        """
        在一个单独的线程中启动HVAC的初始操作，以避免阻塞GUI。
        """
        simulation_thread = threading.Thread(target=self.start_operation_heating_cooling, args=(22.0, "2024-01-01", "0:00"))
        simulation_thread.daemon = True  # 设置为守护线程，主程序退出时它也会退出
        simulation_thread.start()


    def start_operation_heating_cooling(self, set_point, 
                                        date_input, time_input):
        """
        Start the thermostat controller using the inputs provided by the GUI. 
        This Function will be called from gui after getting the input from GUI
        in the dictionary format.
        
        set_point: Temperature setpoint to initiate heating/cooling (float)
        date_input: Date input as yyyy-mm-dd (string)
        time_input: Time input h:dd (string)
        """
        try:
            self.setpoint = set_point
            self.date = date_input
            self.time = time_input
            
            # Initializing Models
            self.model = Model()
            self.model.load_data_from_csv()
            self.thermostat = ThermostatModel(self.model.temperature_data)
            self.fan = FanModel(self.model)
            self.furnace = FurnaceModel(self.model)
            self.aircon = AirConditionerModel(self.model)
            
            # Set the date and time on the thermostat
            self.thermostat.set_date_time(self.date, self.time)

            # Get outdoor temperature
            self.temp_out = float(self.thermostat.get_outdoor_temperature())
            if self.temp_out is None:
                raise ValueError("Unable to retrieve outdoor temperature.")

            # Set the thermostat to the desired target temperature
            set_temp = self.thermostat.set_temperature_value(self.setpoint)

            # Determine the mode (e.g., heating or cooling)
            self.mode = self.thermostat.set_mode()
            try:
                self.fan_status="On"
                # Set the fan speed based on the mode
                self.fan_speed = self.fan.set_fan_speed_value(self.mode)
            
            except:
                self.fan_status="Off"

            # in the begining the current temp == outdoor temp
            self.current_temp = self.temp_out
            self.control_temperature()
        except ValueError as ve:
            print(f"Value error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def update_time(self):
        """
        Update the time every second.
        """
        self.time = QTime.currentTime().toString('HH:mm:ss')
        self.date = QDate.currentDate().toString('yyyy-MM-dd')

    def update_temperature(self):
        """
        Update the current temperature and system status.
        """
        print(f"Updating temperature...")
        self.current_temp = self.thermostat.read_current_temp()
        self.fan_status = self.fan.read_status()
        self.fan_speed = self.fan.read_speed()
        print(f"Current Temperature: {self.current_temp}")
        print(f"Fan Status: {self.fan_status}")
        print(f"Fan Speed: {self.fan_speed}")

        
