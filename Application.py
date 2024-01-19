from PyQt6.QtWidgets import QApplication
import sys

from Interface_Classes.Main_Window import Interface


if __name__ == "__main__":
   application = QApplication(sys.argv)
   app_window = Interface()
   app_window.show()
   sys.exit(application.exec())