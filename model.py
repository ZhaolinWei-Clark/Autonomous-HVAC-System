"""***************************************************************************
Title:          Model
File:           Model.py
Release Notes:  N/A
Author:         Zhaolin Wei
Description:    This file contains the class and functions for the model of 
                the Autonomous_HVAC_System
***************************************************************************"""

"""*********************Libraries******************************************"""
import pandas as pd
import time


"""*********************Classes********************************************"""
class Model:
    """
    This is the base class for managing the HVAC system model. It contains 
    core functionalities for connecting to the database and managing system 
    states such as temperature and mode.
    """
    def __init__(self):
        """
        Initialize the model with default values for the HVAC system.
        This includes the current date, time, temperature settings, HVAC 
        status, and data loading.
        """
        self._temperature_data = None  # Use a private attribute
        self.current_values = {
            "date": (1, 1),  # Default date: (month, day)
            "time": 0,  # Default time: hour
            "Set_temp": 22,  # Default temperature set to 22°C
            "current_temp": 22,  # Current temperature (to be updated)
            "outdoor_temp": 22,  # Outdoor temperature (to be fetched)
            "fan_speed": "low",  # Fan speed setting (to be updated)
            "furnace_status": "off",  # Furnace status (initially off)
            "furnace_temperature": 40,  # Furnace temperature (to be updated)
            "air_conditioner_energy": 0,  # AC temperature (to be updated)
            "air_conditioner_status": "off",  # AC status (initially off)
            "mode": "Normal mode",  # Current mode (Cooling/Heating/Normal)
        }

    def load_data_from_csv(self):
        """
        Load data from a CSV file into a NumPy array for easy access.
        """
        try:
            # Load the CSV data into a pandas DataFrame
            df = pd.read_csv("Temperature_Humidity_Data.csv")
            # Convert the DataFrame to a NumPy array
            self._temperature_data = df.to_numpy()
            print("CSV data loaded successfully.")
        except Exception as e:
            print(f"Error loading CSV data: {e}")

    @property
    def temperature_data(self):
        """
        Getter for temperature data.
        """
        return self._temperature_data

    @temperature_data.setter
    def temperature_data(self, value):
        """
        Setter for temperature data.
        """
        self._temperature_data = value


class ThermostatModel(Model):
    """
    This derived class of Model class and is used specifically for managing
    the thermostat functionality. It includes methods for setting date and 
    time, adjusting temperature, and fetching outdoor temperature.
    """
    def __init__(self, temperature_data):
        """
        Initialize the thermostat model, inheriting from the `Model` class.
        Additional attributes for user-selected date and hour are added here.
        """
        super().__init__()  # Initialize the base class
        self.user_selected_date = "2024-01-01"  # Store user-select date
        self.user_selected_hour = "12:00"  # Store user-select hour
        self.temperature_data = temperature_data

    def set_date_time(self, date_input, time_input):
        """
        Set the date and hour for thermostat operations.
        
        date_input: Date input as yyyy-mm-dd (string)
        time_input: Time input h:dd (string)
        """
        try:
            # Remove spaces
            date_input = date_input.strip()
            time_input = time_input.strip()
            
            # Extract year, month, and day from the date_input string
            year, month, day = map(int, date_input.split('-'))
            
            # Extract hour from the time_input string
            hour = int(time_input.split(":")[0])
            
            # Update current_values
            self.current_values["date"] = f"{year}-{str(month\
                                        ).zfill(2)}-{str(day).zfill(2)}"
            self.current_values["time"] = hour
            
            # Update user-selected date and hour
            self.user_selected_date = f"{year}-{str(month\
                                        ).zfill(2)}-{str(day).zfill(2)}"
            self.user_selected_hour = hour
    
            print(f"Date: {self.current_values['date'][1]}/{\
                self.current_values['date'][2]}/{\
                self.current_values['date'][0]}, ", 
                f"Time: {self.current_values['time']}:00") 
            return self.current_values["date"], self.current_values["time"]
    
        except Exception as e:
            print(f"Error setting date and time: {e}")
            return None, None

    def set_temperature_value(self, set_temperature):
        """
        Update the set temperature value in the system.
        
        set_temperature: New temperature setpoint (float)
        """
        self.current_values["Set_temp"] = set_temperature
        if not self.user_selected_date or self.user_selected_hour is None:
            return "Date and time not set. Please set them first."
        return set_temperature

    def get_outdoor_temperature(self):
        """
        Retrieve the outdoor temperature from the loaded CSV data for the 
        selected date and time.
        """
        if not self.user_selected_date or self.user_selected_hour is None:
            return "Date and time not set. Please set them first."
    
        date = self.user_selected_date  # "2024-01-01"
        hour = self.user_selected_hour  # 0, 1, ..., 23
        formatted_date_time = f"{self.user_selected_date} {int(hour):d}:00"  
        
        try:
            # Ensure the formatted date & time string matches data
            for row in self.temperature_data:
                if row[0] == formatted_date_time:
                    outdoor_temperature = row[1]  # second col in the row=temp
                    print(f"Outdoor temp for {formatted_date_time}\
                          is {outdoor_temperature}°C")
                    self.current_values["outdoor_temp"] = outdoor_temperature
                    return outdoor_temperature  
    
            return "No temperature data found for the specified date & time."
    
        except Exception as e:
            print(f"Error: {e}")
            return f"Error retrieving outdoor temperature: {e}"

    def set_mode(self):
        """
        Determine the operational mode (heating, cooling, or normal)
            based on the target and outdoor temperatures.
        """
        outdoor_temperature = self.current_values["outdoor_temp"]
        set_temperature = self.current_values["Set_temp"]
        if set_temperature < outdoor_temperature:
            self.current_values["mode"] = "Cooling mode"
        elif set_temperature > outdoor_temperature:
            self.current_values["mode"] = "Heating mode"
        else:
            self.current_values["mode"] = "Normal mode"
        return self.current_values["mode"]


class FanModel(Model):
    """
    This subclass of `Model` is responsible for managing the fan's operation,
    including speed adjustments.
    """
    def __init__(self, temperature_data):
        """
        Initialize the fan model, inheriting from the `Model` class.
        """
        super().__init__()
        self.temperature_data = temperature_data

    def set_fan_speed_value(self, mode):
        """
        This method sets the fan speed based on the operational mode.
        
        mode: Either of heating/cooling/normal mode of the system (string)
        """
        fan_speed = "None"  # Initialize fan speed

        if mode == "Heating mode":
            fan_speed = "high"
        elif mode == "Normal mode":
            fan_speed = "low"
        elif mode == "Cooling mode":
            fan_speed = "high"
        else:
            raise ValueError("The mode should be Heating mode, Normal\
                             mode or Cooling mode.")
        return fan_speed


class FurnaceModel(Model):
    """
    This subclass of `Model` is responsible for managing furnace operations,
    including calculating heat output.
    """
    def __init__(self, temperature_data):
        super().__init__()
        self.stop_polling = False
        self.q_furnace = 500  # unit BTU
        self.temperature_data = temperature_data

    def calculate_q_furnace(self, temp_difference):
        """
        Determine the Q_furnace value based on the temperature difference
        using the pandas DataFrame.
        
        temp_difference: Temperature difference betwn out and inside (float)
        """
        if temp_difference > 10:
            return 500  # Maximum heat output
        elif 5 < temp_difference <= 10:
            return 300  # Medium heat output
        elif 0 < temp_difference <= 5:
            return 100  # Low heat output
        else:
            return 0  # Minimal heat for fine adjustments

    def heating(self, outdoor_temp, set_temp):
        """
        Simulate the heating process to maintain the desired temperature 
        using temperature data.
        
        outdoor_temp: Current outdoor temperature (float)
        set_temp: Temperature setpoint (Float)
        """
        current_temperature = outdoor_temp
        iter = 0  # Initialize iteration counter
        U = 10.0  # Heat loss coefficient (arbitrary units)
        C = 500.0  # Thermal capacity (arbitrary units)
        dt = 2.0  # Time step in seconds

        while set_temp > current_temperature:
            temp_difference = set_temp - current_temperature
            self.q_furnace = self.calculate_q_furnace(temp_difference)
            dT = (self.q_furnace - U * (set_temp - current_temperature)) / C
            current_temperature += dT
            iter += 1
            self.current_values["current_temp"] = current_temperature
            time.sleep(dt)
        self.stop_polling = True
        print("Desired temperature reached!")

    def read_current_temp(self):
        """
        Retrieve the current room temperature during the heating process.
        """
        return self.current_values["current_temp"]

    def read_q_furnace(self):
        """
        Retrieve the current furnace output (Q_furnace) in BTU.
        """
        return self.q_furnace


class AirConditionerModel(Model):
    """
    This subclass of `Model` manages air conditioner operations,
    including simulating the cooling process and adjusting the temperature.
    """
    def __init__(self, temperature_data):
        super().__init__()
        self.stop_polling = False
        self.q_aircon = 500  # BTU
        self.temperature_data = temperature_data

    def calculate_q_aircon(self, temp_difference):
        """
        Determine the Q_aircon value based on the temperature difference 
        using the pandas DataFrame.
        
        temp_difference: Difference between outdoor and indoor temp (float)
        """
        if temp_difference > 10:
            return 500
        elif 5 < temp_difference <= 10:
            return 300
        elif 0 < temp_difference <= 5:
            return 100
        else:
            return 0

    def cooling(self, outdoor_temp, set_temp):
        """
        Simulate the Cooling process to maintain the desired temperature 
        using temperature data.
        
        outdoor_temp: Current outdoor temperature (float)
        set_temp: Temperature setpoint (Float)
        """
        current_temperature = outdoor_temp
        iter = 0  # Initialize iteration counter
        U = 10.0  # Heat loss coefficient (arbitrary units)
        C = 500.0  # Thermal capacity (arbitrary units)
        dt = 2.0  # Time step in seconds

        while set_temp < current_temperature:
            temp_difference = current_temperature - set_temp
            self.q_aircon = self.calculate_q_aircon(temp_difference)
            dT = ((self.q_aircon) - (U * (temp_difference))) / C
            current_temperature -= dT
            iter += 1
            self.current_values["current_temp"] = current_temperature
            time.sleep(dt)
        self.stop_polling = True
        print("Desired temperature reached!")

    def read_current_temp(self):
        """
        Retrieve the current room temperature during the cooling process.
        """
        return self.current_values["current_temp"]

    def read_q_aircon(self):
        """
        Retrieve the current aircon output (Q_aircon) in BTU.
        """
        return self.q_aircon