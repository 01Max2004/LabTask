from PyQt6 import QtWidgets, QtGui, QtCore
import json
import re

from Interface_Classes.Program_Item import ProgramItem
from Functional_Classes.TV_Program_Class import TVProgramDB

class Interface(QtWidgets.QMainWindow):
   currentChannel = None

   def __init__(self):
      super().__init__()

      self.tvProgram = TVProgramDB()

      self.setupUi(self)
      self.ConnectDataBase()

   def setupUi(self, Interface):
      Interface.resize(1000, 600)
      Interface.setWindowTitle("TV Program")

      self.setWindowIcon(QtGui.QIcon("Images\icon_tv_40.png"))
      self.setFixedWidth(1000)
      self.setFixedHeight(600)

      main_widget = QtWidgets.QWidget(Interface)
      self.setCentralWidget(main_widget)

      centarl_frame = QtWidgets.QFrame(main_widget)
      centarl_frame.setGeometry(0, 0, 1000, 600)
      centarl_frame.setStyleSheet("""
                                          background-color: rgba(40, 40, 40, 1);
                                       """)
      
      channelsArea_frame = QtWidgets.QFrame(centarl_frame)
      channelsArea_frame.setGeometry(0, 100, 200, 500)
      channelsArea_frame.setStyleSheet("""
                                             background-color: rgba(28, 28, 28, 1);
                                           """)
      
      programArea_frame = QtWidgets.QFrame(centarl_frame)
      programArea_frame.setGeometry(200, 100, 500, 500)
      programArea_frame.setStyleSheet("""
                                       background-color: rgba(32, 32, 32, 1);
                                      """)
         
      discriptionArea_frame = QtWidgets.QFrame(centarl_frame)
      discriptionArea_frame.setGeometry(700, 0, 300, 600)
      discriptionArea_frame.setStyleSheet("""
                                                background-color: rgba(20,20,20, 1);
                                               """)
      
      self.search_lineEdit = QtWidgets.QLineEdit(centarl_frame)
      self.search_lineEdit.setGeometry(30, 37, 500, 28)
      self.search_lineEdit.setStyleSheet("""
                                          QLineEdit {
                                             background-color: rgba(230, 230, 230, 1);
                                             color: black;
                                             border-radius: 5px;
                                             padding-left: 5px; 
                                             padding-bottom: 2px;
                                             font-size: 14px;                  
                                          }
                                         """)
      self.search_lineEdit.setPlaceholderText("Enter name of program")
      self.search_lineEdit.textChanged.connect(self.SearchLineEdit_chenged)
      
      self.genre_comboBox = QtWidgets.QComboBox(centarl_frame)
      self.genre_comboBox.setGeometry(550, 36, 120, 29)
      self.genre_comboBox.setStyleSheet("""
                                       QComboBox {
                                          background-color: rgba(20, 20, 20, 0.8);
                                          color: rgba(250, 250, 250, 0.8);
                                          border-radius: 5px;   
                                          font-size: 14px;
                                          padding-left: 23px;                          
                                       }
                                       QComboBox:hover {
                                          background-color: rgba(20, 20, 20, 1)
                                       }
                                       QComboBox QAbstractItemView {
                                          outline: 0px solid;
                                       }
                                       QComboBox QAbstractItemView::item {
                                          background-color: rgb(20, 20, 20);
                                          color: rgba(250, 250, 250, 0.5);
                                          padding-left: 11px; 
                                       }                                        
                                       QComboBox QAbstractItemView::item:hover {
                                          background-color: rgb(40, 40, 40)
                                       }
                                       QComboBox::down-arrow {
                                          background: transparent;
                                       }
                                       QComboBox::drop-down {
                                          width: 0px;
                                          border-radius: 5px;
                                       }
                                       """)
      self.genre_comboBox.addItem("ANY GENRE")
      self.genre_comboBox.addItems(json.load(open("Lists/Genre.json", encoding="utf-8")))
      self.genre_comboBox.currentIndexChanged.connect(lambda: self.ChannelChoosen(self.currentChannel))
                                             
      self.channels_layout = QtWidgets.QVBoxLayout(channelsArea_frame)
      self.channels_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

      self.program_layout = QtWidgets.QVBoxLayout(programArea_frame)
      self.program_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
      self.program_layout.setSpacing(10)

      program_widget = QtWidgets.QWidget()
      program_widget.setLayout(self.program_layout)

      program_scrollArea = QtWidgets.QScrollArea(programArea_frame)
      program_scrollArea.setGeometry(QtCore.QRect(10, 10, 490, 490))
      program_scrollArea.setStyleSheet("""border: none;""")
      program_scrollArea.verticalScrollBar().hide()
      program_scrollArea.setVerticalScrollBarPolicy(
         QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn
      )
      program_scrollArea.setHorizontalScrollBarPolicy(
         QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
      )
      program_scrollArea.horizontalScrollBar().setDisabled(True)
      program_scrollArea.setWidgetResizable(True)
      program_scrollArea.setWidget(program_widget)

      self.discriptionContainer_frame = QtWidgets.QFrame(discriptionArea_frame)  
      self.discriptionContainer_frame.setVisible(False)

      self.programDiscriptionPreview_label = QtWidgets.QLabel(self.discriptionContainer_frame)
      self.programDiscriptionPreview_label.setGeometry(20, 20, 260, 146)
      self.programDiscriptionPreview_label.setStyleSheet("""
                                                            border-radius: 5px;
                                                            background-color: rgba(100, 100, 100, 1);
                                                         """)
      self.programDiscriptionPreview_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
      
      self.programDiscriptionName_label = QtWidgets.QLabel(self.discriptionContainer_frame)
      self.programDiscriptionName_label.setGeometry(20, 180, 260, 40)
      self.programDiscriptionName_label.setStyleSheet("""
                                                            color: rgba(255, 255, 0, 0.95);
                                                         """)
      self.programDiscriptionName_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
      self.programDiscriptionName_label.setWordWrap(True)

      self.programDiscription_label = QtWidgets.QLabel(self.discriptionContainer_frame)
      self.programDiscription_label.setGeometry(QtCore.QRect(20, 230, 260, 320))
      self.programDiscription_label.setStyleSheet("""
                                                   color: rgba(255, 255, 255, 0.95);
                                                  """)
      self.programDiscription_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
      self.programDiscription_label.setWordWrap(True)

   def ConnectDataBase(self):
      for channelName in self.tvProgram.ViewChanels():
         channelItem_button = QtWidgets.QPushButton()
         channelItem_button.setText(*channelName)
         channelItem_button.setFixedHeight(40)
         channelItem_button.setStyleSheet("""
                                          QPushButton {
                                             background-color: rgba(20, 20, 20, 0.8);
                                             color: rgba(250, 250, 250, 0.8);
                                             margin: 5px;
                                             border-radius: 5px;
                                          }
                                          QPushButton:hover {
                                             background-color: rgba(20, 20, 20, 1);
                                          }
                                          QPushButton:focus {
                                             background-color: rgba(255, 255, 0, 0.8);
                                             color: black;
                                          }
                                         """)
         channelItem_button.clicked.connect(lambda checked, channelName=channelName: self.ChannelChoosen(*channelName))

         self.channels_layout.addWidget(channelItem_button)

   def ChannelChoosen(self, channelName: str):
      self.currentChannel = channelName
      self.discriptionContainer_frame.setVisible(False)

      for i in reversed(range(self.program_layout.count())): 
         self.program_layout.itemAt(i).widget().setParent(None)
   
      for weekDay in json.load(open("Lists/Days.json", encoding="utf-8")):
         voidDayCheck = True

         weekDay_label = QtWidgets.QLabel()
         weekDay_label.setText(f"<strong>{weekDay}<strong>")
         weekDay_label.setMinimumHeight(26)
         weekDay_label.setStyleSheet("""
                                       background-color: transparent;
                                       font-size: 24px;
                                       color: rgba(255, 255, 0, 0.95);
                                     """)
         
         self.program_layout.addWidget(weekDay_label)

         for program in self.tvProgram.ViewPrograms(channelName, weekDay, self.genre_comboBox.currentText()):
            if (re.search(".*" + self.search_lineEdit.text() + ".*", program[3])):
               voidDayCheck = False

               programItem = ProgramItem([program[0], program[2], program[3], program[4]])
               programItem.setMinimumHeight(75)
               programItem.setMinimumWidth(480)
               programItem.itemClicked_signal.connect(self.ProgramChoosen)

               self.program_layout.addWidget(programItem) 

         if voidDayCheck:
            voidDay_label = QtWidgets.QLabel()
            voidDay_label.setText(f"<strong>No any information about program<strong>")
            voidDay_label.setMinimumHeight(26)
            voidDay_label.setStyleSheet("""
                                          background-color: transparent;
                                          font-size: 16px;
                                          color: rgba(255, 0, 0, 0.95);
                                       """)
            
            self.program_layout.addWidget(voidDay_label)

   def SearchLineEdit_chenged(self):
      if self.currentChannel is not None:
         self.ChannelChoosen(self.currentChannel)

   @QtCore.pyqtSlot(int)
   def ProgramChoosen(self, programId):
      self.discriptionContainer_frame.setVisible(True)

      programDiscription = self.tvProgram.ViewDiscription(self.currentChannel, programId)

      self.programDiscriptionPreview_label.setPixmap(QtGui.QPixmap("Images/icon-movie-100.png"))
      
      self.programDiscriptionName_label.setText(f"<strong>{programDiscription[0]}<strong>")
      self.programDiscription_label.setText(f"<strong>{programDiscription[1]}<strong>")
