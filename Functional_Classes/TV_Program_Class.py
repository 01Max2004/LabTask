import sqlite3

class TVProgramDB():
   def __init__(self):
      self.base = sqlite3.connect("DataBases/TV_Program.db")
      self.cur = self.base.cursor()

   def CreateChanel(self, channelName: str):
      self.cur.execute(f"""CREATE TABLE IF NOT EXISTS '{channelName}' (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           weekDay TEXT,
                           programTime TEXT,
                           programName TEXT,
                           programType TEXT,
                           programDiscription LONGTEXT
                       );""")
      self.base.commit()

   def AddProgram(self, channelName: str, weekDay: str, programTime: str, programName: str, programType: str, programDiscription: str):
      try:  
         self.cur.execute(f"""INSERT INTO '{channelName}' (id, weekDay, programTime, programName, programType, programDiscription) VALUES (NULL, ?, ?, ?, ?, ?);""", (weekDay, programTime, programName, programType, programDiscription,))
         self.base.commit()
         return "ADDING COMPLETE"
      except:
         return "ADDING ERROR"
      
   def ViewChanels(self):
      return self.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND NOT name = 'sqlite_sequence';").fetchall()

   def ViewPrograms(self, channelName: str, weekDay: str, genre: str = "ANY GENRE"):
      return self.cur.execute(f"""SELECT * FROM '{channelName}' WHERE weekDay = '{weekDay}'"""
                               + ("", f" AND programType = '{genre}'")[genre != "ANY GENRE"] + ";").fetchall()
      
   def ViewDiscription(self, channelName: str, programId: int):
      return self.cur.execute(f"""SELECT programName, programDiscription FROM '{channelName}' WHERE id = '{programId}';""").fetchone()