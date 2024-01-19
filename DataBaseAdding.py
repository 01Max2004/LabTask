from PyQt6 import QtWidgets, QtCore
import sys
import json

from Functional_Classes.TV_Program_Class import TVProgramDB

channelNameValue = ""

def AddChannel_button_clicked(channelName: str):
   tvProgram = TVProgramDB()

   global channelNameValue

   if channelName != "":
      channelNameValue = channelName

      tvProgram.CreateChanel(channelNameValue)
      return(print("Channel connected"))
   else:
      return(print("ERROR:\n\tChannel's name is empty"))

def AddProgram_button_clicked(data: list):
   tvProgram = TVProgramDB()

   global channelNameValue

   if channelNameValue == "":
      return(print("ERROR:\n\tChannel's name is empty"))

   for element in data:
      if(element == ""):
         return(print("ERROR:\n\tSeveral inputs are empty"))
   
   return(print("Status: ", tvProgram.AddProgram(channelNameValue, *data)))

if __name__ == "__main__":
   application = QtWidgets.QApplication(sys.argv)
   window = QtWidgets.QMainWindow()
   window.setWindowTitle("DataBassesCreating")

   content_layout = QtWidgets.QVBoxLayout()

   main_widget = QtWidgets.QWidget()
   main_widget.setLayout(content_layout)

   channel_layout = QtWidgets.QHBoxLayout()

   channel_name_lineEdit = QtWidgets.QLineEdit()
   channel_name_lineEdit.setPlaceholderText("Channel name")
   
   channel_creating_button = QtWidgets.QPushButton()
   channel_creating_button.setText("Add/Connect channel")
   channel_creating_button.clicked.connect(lambda: AddChannel_button_clicked(channel_name_lineEdit.text()))

   channel_layout.addWidget(channel_name_lineEdit)
   channel_layout.addWidget(channel_creating_button)

   content_layout.addLayout(channel_layout)

   weekDay_comboBox = QtWidgets.QComboBox()
   weekDay_comboBox.addItems(json.load(open("Lists/Days.json", encoding="utf-8")))

   programName_lineEdit = QtWidgets.QLineEdit()
   programName_lineEdit.setPlaceholderText("Program's name")

   programTime_timeEdit = QtWidgets.QTimeEdit()

   programGenre_comboBox = QtWidgets.QComboBox()
   programGenre_comboBox.addItems(json.load(open("Lists/Genre.json", encoding="utf-8")))

   programDiscription_textEdit = QtWidgets.QTextEdit()
   programDiscription_textEdit.setPlaceholderText("Program's discription")

   programAdding_button = QtWidgets.QPushButton()
   programAdding_button.setText("Add program")
   programAdding_button.clicked.connect(lambda: AddProgram_button_clicked([weekDay_comboBox.currentText(), programTime_timeEdit.text(), programName_lineEdit.text(), programGenre_comboBox.currentText(), programDiscription_textEdit.toPlainText()]))

   content_layout.addWidget(weekDay_comboBox)
   content_layout.addWidget(programName_lineEdit)
   content_layout.addWidget(programTime_timeEdit)
   content_layout.addWidget(programGenre_comboBox)
   content_layout.addWidget(programDiscription_textEdit)
   content_layout.addWidget(programAdding_button)

   window.setCentralWidget(main_widget)

   window.show()
   sys.exit(application.exec())

