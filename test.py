"""***************************************************************************
Title:          Unit Tests
File:           test.py
Release Notes:  N/A
Author:         Zhaolin Wei
Description:    This file contains the testing of the model and controller.
***************************************************************************"""

"""*********************Libraries******************************************"""
import unittest
from unittest.mock import MagicMock, patch
from controller import ThermostatController
from model import Model, ThermostatModel, FanModel, FurnaceModel, AirConditionerModel

"""*********************Classes****************************************"""
class TestThermostatController(unittest.TestCase):
    
    def setUp(self):
        """
        Set up the test environment by creating an instance of ThermostatController.
        Mock dependent model classes to isolate the testing.

        Chatgpt Assistance for learning the format of the unit test
        """
        # Patch and mock the imported models
        patcher_thermostat = patch('controller.ThermostatModel')
        patcher_fan = patch('controller.FanModel')
        patcher_furnace = patch('controller.FurnaceModel')
        patcher_aircon = patch('controller.AirConditionerModel')

        self.mock_thermostat = patcher_thermostat.start()
        self.mock_fan = patcher_fan.start()
        self.mock_furnace = patcher_furnace.start()
        self.mock_aircon = patcher_aircon.start()

        self.addCleanup(patcher_thermostat.stop)
        self.addCleanup(patcher_fan.stop)
        self.addCleanup(patcher_furnace.stop)
        self.addCleanup(patcher_aircon.stop)

        # Set return value for get_outdoor_temperature
        self.mock_thermostat.return_value.get_outdoor_temperature.return_value = 22

        # Instantiate the controller with mocked models
        self.controller = ThermostatController()

    def test_initialization(self):
        """
        Test that the controller initializes with the correct default values.
        """
        self.assertEqual(self.controller.date, "2024-01-01")
        self.assertEqual(self.controller.time, "0:00")
        self.assertEqual(self.controller.setpoint, 22)


    def test_system_overview(self):
        """
        Test that the system overview returns the expected properties.
        """
        # Mock necessary attributes
        self.controller.bdrm_1_temp = 21
        self.controller.bdrm_2_temp = 22
        self.controller.bdrm_3_temp = 23
        self.controller.bath_1_temp = 24
        self.controller.bath_2_temp = 25
        self.controller.living_temp = 20
        self.controller.kitchen_temp = 19
        self.controller.mech_rm_temp = 18
        self.controller.rec_rm_temp = 17
        self.controller.temp_out = 15
        self.controller.mode = "Heating"
        self.controller.furnace_status = 1
        self.controller.furnace_energy = 100
        self.controller.aircon_status = 0
        self.controller.aircon_energy = 0
        self.controller.fan_status = 1
        self.controller.damp_sup_pos = 50
        self.controller.damp_ret_pos = 50
        self.controller.damp_out_pos = 50

        expected_overview = [
            21, 22, 23, 24, 25, 20, 19, 18, 17, 15, "2024-01-01", "0:00", "Heating",
            1, 100, 0, 0, 1, 50, 50, 50
        ]
        result = self.controller.system_overview()
        self.assertEqual(result, expected_overview)

    def test_control_temperature_heating(self):
        """
        Test the heating control logic when setpoint is higher than current temperature.
        """
        self.controller.setpoint = 25
        self.controller.current_temp = 20

        # Mock methods to avoid real threading calls
        self.controller.furnace.heating = MagicMock()
        self.controller.set_current_temperature_furnace = MagicMock()

        self.controller.control_temperature()

        self.controller.furnace.heating.assert_called_once_with(20, 25)
        self.controller.set_current_temperature_furnace.assert_called_once()
        self.assertEqual(self.controller.furnace_status, 1)

    def test_control_temperature_cooling(self):
        """
        Test the cooling control logic when setpoint is lower than current temperature.
        """
        self.controller.setpoint = 20
        self.controller.current_temp = 25

        # Mock methods to avoid real threading calls
        self.controller.aircon.Cooling = MagicMock()
        self.controller.set_current_temperature_aircon = MagicMock()

        self.controller.control_temperature()

        self.controller.aircon.Cooling.assert_called_once_with(25, 20)
        self.controller.set_current_temperature_aircon.assert_called_once()
        self.assertEqual(self.controller.aircon_status, 1)

    def test_start_operation_heating_cooling(self):
        """
        Test the start_operation_heating_cooling method to ensure inputs are correctly processed.
        """
        # Mock thermostat methods
        self.controller.thermostat.set_date_time = MagicMock()
        self.controller.thermostat.get_outdoor_temperature = MagicMock(return_value=30)
        self.controller.thermostat.set_temperature_value = MagicMock()
        self.controller.thermostat.set_mode = MagicMock(return_value="Heating")
        self.controller.fan.set_fan_speed_value = MagicMock(return_value="high")

        self.controller.start_operation_heating_cooling(24, "2024-03-13", "12:30")

        self.controller.thermostat.set_date_time.assert_called_once_with("2024-03-13", "12:30")
        self.controller.thermostat.get_outdoor_temperature.assert_called_once()
        self.controller.thermostat.set_temperature_value.assert_called_once_with(24)
        self.controller.thermostat.set_mode.assert_called_once()
        self.controller.fan.set_fan_speed_value.assert_called_once_with("Heating")

        self.assertEqual(self.controller.setpoint, 24)
        self.assertEqual(self.controller.date, "2024-03-13")
        self.assertEqual(self.controller.time, "12:30")
        self.assertEqual(self.controller.mode, "Heating")
        self.assertEqual(self.controller.fan_speed, "high")

class TestHVACSystem(unittest.TestCase):
    def setUp(self):
        self.model = Model()
        self.thermostat = ThermostatModel()
        self.fan = FanModel()
        self.furnace = FurnaceModel()
        self.aircon = AirConditionerModel()

    def test_initialization(self):
        # Test default values
        self.assertEqual(self.model.current_values["Set_temp"], 22)
        self.assertEqual(self.model.current_values["fan_speed"], "low")
        self.assertEqual(self.model.current_values["mode"], "Normal mode")

    @patch('pandas.read_csv')
    def test_load_data_from_csv(self, mock_read_csv):
        # Mock CSV data
        mock_read_csv.return_value = MagicMock(to_numpy=lambda: [["2024-01-01 00:00", 15]])
        self.model.load_data_from_csv("mock.csv")
        self.assertEqual(self.model.temperature_data[0][1], 15)

    def test_set_date_time(self):
        # Test valid date and time
        date, time = self.thermostat.set_date_time("2024-01-01", "15:00")
        self.assertEqual(date, "2024-01-01")
        self.assertEqual(time, 15)

        # Test invalid date and time
        date, time = self.thermostat.set_date_time("invalid-date", "invalid-time")
        self.assertIsNone(date)
        self.assertIsNone(time)

    def test_set_temperature_value(self):
        # Test setting a valid temperature
        self.assertEqual(self.thermostat.set_temperature_value(25), 25)
        self.assertEqual(self.thermostat.current_values["Set_temp"], 25)

        # Test behavior when date and time are not set
        self.thermostat.user_selected_date = None
        self.assertEqual(
            self.thermostat.set_temperature_value(25), 
            "Date and time not set. Please set them first."
        )

    @patch.object(ThermostatModel, 'get_outdoor_temperature')
    def test_get_outdoor_temperature(self, mock_get_temp):
        # Mock outdoor temperature
        mock_get_temp.return_value = 20
        outdoor_temp = self.thermostat.get_outdoor_temperature()
        self.assertEqual(outdoor_temp, 20)

    def test_set_mode(self):
        # Test mode determination
        self.thermostat.current_values["outdoor_temp"] = 20
        self.thermostat.current_values["Set_temp"] = 25
        self.assertEqual(self.thermostat.set_mode(), "Heating mode")

        self.thermostat.current_values["Set_temp"] = 15
        self.assertEqual(self.thermostat.set_mode(), "Cooling mode")

        self.thermostat.current_values["Set_temp"] = 20
        self.assertEqual(self.thermostat.set_mode(), "Normal mode")

    def test_fan_speed(self):
        # Test fan speed adjustment
        self.assertEqual(self.fan.set_fan_speed_value("Heating mode"), "high")
        self.assertEqual(self.fan.set_fan_speed_value("Normal mode"), "low")
        self.assertEqual(self.fan.set_fan_speed_value("Cooling mode"), "high")

    def test_furnace_heating(self):
        # Test furnace heating logic
        self.furnace.heating(15, 25)  # From 15°C to 25°C
        self.assertTrue(self.furnace.stop_polling)
        self.assertGreaterEqual(self.furnace.current_values["current_temp"], 25)

    def test_air_conditioner_cooling(self):
        # Test air conditioner cooling logic
        self.aircon.cooling(30, 22)  # From 30°C to 22°C
        self.assertTrue(self.aircon.stop_polling)
        self.assertLessEqual(self.aircon.current_values["current_temp"], 22)

"""*********************Main Routine***************************************"""
if __name__ == "__main__":
    unittest.main()