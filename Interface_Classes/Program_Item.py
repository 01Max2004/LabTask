from PyQt6 import QtWidgets, QtCore

class ProgramItem(QtWidgets.QWidget):
   itemClicked_signal = QtCore.pyqtSignal(int)

   def __init__(self, programData: list):
      super().__init__()

      self.itemId = programData[0]

      self.setupUi(self, programData)


   def setupUi(self, ProgramItem, programData: list):  
      item_frame = QtWidgets.QFrame(ProgramItem)
      item_frame.setGeometry(0, 0, 460, 75)
      item_frame.setStyleSheet("""
                                       QFrame {
                                          background-color: transparent;
                                          border-radius: 5px;
                                       }
                                       QFrame:hover {
                                          background-color: rgba(255, 255, 255, 0.1);
                                       }
                                    """)
      item_frame.mouseReleaseEvent = lambda event: self.CurrentItemClicked()

      programItemStartTime_label = QtWidgets.QLabel(item_frame)
      programItemStartTime_label.setGeometry(5, 5, 75, 40)
      
      programItemStartTime_label.setStyleSheet("""
                                                      background-color: transparent;
                                                      color: rgba(250, 250, 250, 1);
                                                      font-size: 28px;
                                                    """)
      programItemStartTime_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
      programItemStartTime_label.setText(f"<strong>{programData[1]}</strong>")
      
      programItemName_label = QtWidgets.QLabel(item_frame)
      programItemName_label.setGeometry(85, 5, 380, 45)
      programItemName_label.setStyleSheet("""
                                                background-color: transparent;
                                                color: rgba(200, 200, 200, 1);
                                                font-size: 16px;
                                               """)
      programItemName_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
      programItemName_label.setText(f"""{programData[2]}""")
      programItemName_label.setWordWrap(True)

      programItemGenre_label = QtWidgets.QLabel(item_frame)
      programItemGenre_label.setGeometry(85, 55, 380, 15)
      programItemGenre_label.setStyleSheet("""
                                                   background-color: transparent;
                                                   color: rgba(255, 255, 255, 0.3);
                                                   font-size: 10px;
                                                """)
      programItemGenre_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
      programItemGenre_label.setText(f"<strong>{programData[3]}<strong>")

   def CurrentItemClicked(self):
      self.itemClicked_signal.emit(self.itemId)