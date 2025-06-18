# Autonomous HVAC System
An autonomous automation system for home HVAC system, featuring an interactive
GUI for monitoring and controlling HVAC components dynamically.

---

## Table of Contents
1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Development Environment](#development-environment)
5. [Project Structure](#project-structure)
6. [How to Run](#how-to-run)
7. [Usage](#usage)
8. [GUI Tabs](#gui-tabs)
9. [Features](#features)
10. [Future Scope](#future-scope)

---

## Overview
This project is an **autonomous HVAC system** for homes that:
- Monitors and controls HVAC components such as fans, dampers, furnaces, and
 air conditioners.
- Takes user inputs like setpoint temperature, date, and time to dynamically 
adjust the HVAC system.
- Extracts and simulates outdoor temperature data based on historical data
 from the Government of Canada.
- Displays real-time system status using an interactive **Graphical User
 Interface (GUI)**.

---

## Requirements
To set up and run the project, the following dependencies are required:

### Software Requirements
- **Python Version**: 3.12.6 *(Any version of Python 3+ is sufficient)*

### Python Dependencies
Install the required libraries using `pip`:

```bash
pip install pyqt5
pip install pandas
pip install numpy
```

---

## Installation
Follow these steps to set up the project:
1. Clone the repository:
   ```bash
   git clone <repository-link>
   cd Autonomous_HVAC_System
   ```
2. Install dependencies (as shown above).

---

## Development Environment
The project has been developed and tested using:
- **Visual Studio Code** (VS Code)
- **Spyder**

---

## Project Structure
The project is organized into the following structure:

```
Autonomous_HVAC_System/
│
├── main.py           					# Main script to connect all features
├── gui.py            					# GUI implementation
│	├── Aircon.py     					# Graphics for air conditioner
│	│	├── Aircon/					# Animation images for air conditioner
│	│
│	├── Damper.py     					# Graphics for damper
│	│	├── Damper/					# Animation images for damper
│	│
│	├── Fan.py        					# Graphics for fan
│	│	├── Fan/						# Animation images for fan
│	│
│	├── Furnace.py    					# Graphics for furnace
│	│	├── Furnace/					# Animation images for furnace
│	│
│	├── Layout.py     					# Graphics for layout
│	│	├── Layout/					# Layout images for layout
│	│
│	├── Symbols.py    					# Graphics for symbols & dynamic text
│		├── Symbols/					# Static images for text & symbols
│
├── model.py          					# Models for system components
│	├── Temperature_Humidity_Data.csv	# Outdoor dataset
│
├── controller.py     					# Controller managing project logic
├── fan.py            					# Fan graphics and control
├── heating_cooling.py					# Heating and cooling graphics control
├── symbols.py        					# Symbols graphics and outputs
└── test.py           					# Unit tests for controller and model
```

> **Note**: Place GUI graphics in the same folder as the GUI file to ensure
	proper execution.

---

## How to Run .py file
1. Navigate to the project directory:
   ```bash
   cd Autonomous_HVAC_System
   ```
2. Run the project using the following command:
   ```bash
   python main.py
   ```

## How to Run .exe file
1. Navigate to the project directory:
   ```bash
   cd Autonomous_HVAC_System
   ```
2. Run the project using the following command:
   ```bash
   Autonomous_HVAC_System.exe
   ```
---

## Usage
1. Open the GUI and input the **setpoint temperature**, **date**, and 
	**time**.
2. The system will automatically activate the furnace or air conditioner
	based on the simulated outdoor temperature.
3. Monitor and control components such as:
   - **Fan**: Monitor its status.
   - **Damper**: Manage airflow direction.
   - **Furnace**: Display status and energy heat levels.
   - **Air Conditioner**: Display status and cooling power.
4. Use the interactive tabs in the GUI to explore specific rooms and 
	components.

---

## GUI Tabs
The GUI contains 5 main tabs:

1. **Overview Window**
   - Displays an overview of all rooms and their status.

2. **Mechanical Room**
   - Displays the mechanical room components, including:
     - Fan speed
     - Furnace energy heat
     - Air conditioner cooling power

3. **Ground Floor**
   - Layout includes:
     - Living Room
     - Bedroom 1
     - Bedroom 2
     - Bathroom 1
     - Kitchen
   - Allows input of setpoint temperature, date, and time.

4. **Basement**
   - Layout includes:
     - Bedroom 3
     - Mechanical Room
     - Bathroom 2
     - Rec Room

5. **Settings**
   - Layout includes:
     - Manual date adjustment*

*Within scope of outdoor dataset file

---

## Features
- **Dynamic Control**: The system automatically activates HVAC components 
	based on user-defined setpoints and simulated outdoor temperature.
- **Interactive GUI**: Real-time monitoring and control of HVAC components.
- **Historical Data Integration**: Uses Government of Canada's historical 
	weather data to simulate outdoor temperature.
- **Component Visualization**: Displays graphical status of fans, furnaces,
	air conditioners, and dampers.
- **Scalability**: The project structure allows easy extension to other 
	automation systems.
- **Thermal Modelling**: Implements basic HVAC features to control the 
	temperature of home systems.
---

## Future Scope
This project can be extended to:
1. Currently, this project is developed to take setpoint temperature values 
	for the whole house. This can be extended to control the temperature 
	of each room separately.
2. Use precise equations of heat energy transfer & humidity integration to 
	give more realistic current temperature calculations.
3. Full **Home Automation System** with smart lighting, security, and energy
	management.
4. Integration with **IoT sensors** for real-time outdoor temperature and 
	humidity data.
5. Development of hardware for home monitor system.

---

## Compilation Instructions
To compile and run the project:
1. Ensure all dependencies are installed.
2. Use Python 3 to execute the `main.py` file.

---

## Project Description
This project demonstrates an autonomous HVAC system that monitors and controls
the heating, ventilation, and air conditioning of a home. It uses a **GUI** 
for user interaction, real-time visualization, and control of components such 
as:
- Fans
- Dampers
- Furnaces
- Air Conditioners

By leveraging historical temperature data, the system ensures dynamic and 
efficient control to maintain desired indoor conditions.

---

### Credits

- **Language**: Python
- **Tools**: PyQt5, Pandas, Numpy
- **AI Usage**: Stated in the source files where the ChatGPT & Microsoft 
	Copilot was used to assist project. ChatGPT assistance used in Drafting
	structure of README.

---

### License
This project is licensed under the MIT License.

---