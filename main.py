"""***************************************************************************
Title:          Home Automation HVAC Controls System
File:           main.py
Release Notes:  N/A

Author:         Zhaolin Wei

Description:    The main application to call and run the GUI, Model, and the
                controller.
***************************************************************************"""

"""*********************Libraries******************************************"""
import sys
from PyQt5.QtWidgets import QApplication
import controller
import gui

"""*********************Main Routine***************************************"""
if __name__ == "__main__":
    try:
        # 1. 创建 QApplication 实例，这是任何PyQt应用的第一步
        app = QApplication(sys.argv)
        
        # 2. 创建控制器实例
        # 控制器现在会初始化所有必要的模型和数据
        hvac_controller = controller.ThermostatController()
        
        # 3. 创建主窗口（GUI），并将控制器实例传递给它
        main_window = gui.MainWindow(hvac_controller)
        
        # 4. 显示主窗口
        main_window.show()
        
        # 5. 启动控制器的后台操作（例如，开始温度模拟）
        hvac_controller.start_hvac_simulation_thread()
        
        # 6. 启动Qt事件循环，并确保在关闭窗口时程序能正确退出
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"Critical error: {e}")