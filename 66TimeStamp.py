import sys
from tkinter import *
import tkinter as tk
import os
import datetime
import shutil
# for database
import sqlite3

# create table
with sqlite3.connect("database.db") as connection:
  c = connection.cursor()
  # c.execute("DROP TABLE IF EXISTS TStbl")
  c.execute("CREATE TABLE IF NOT EXISTS TStbl ( \
  id INTEGER PRIMARY KEY AUTOINCREMENT, \
  timestamp TEXT DEFAULT CURRENT_TIMESTAMP \
  )")
  connection.commit()
connection.close()

# GUI layout

mGui = Tk()
w = 450
h = 500
ws = mGui.winfo_screenwidth()
hs = mGui.winfo_screenheight()
x=(ws/2) - (w/2)
y = (hs/2) - (h/2)
mGui.geometry("%dx%d+%d+%d" % (w,h,x,y))
w, h = mGui.winfo_screenwidth(), mGui.winfo_screenheight()
mGui.title("File Transfer Tool")
theEntry = StringVar()
mGui.configure(background="#ffffcc")

## START

src=""
dst=""


def BrowseSrc():
  srcraw = tk.filedialog.askdirectory()
  global src
  src = srcraw.replace('\\','//')+"//"

  # insert src to an entry
  mEntry = Entry(mGui)
  mEntry.configure(width=60)
  mEntry.pack(side=TOP)
  mEntry.delete(0,END)
  mEntry.insert(0,"Source folder:   " + srcraw)
  return src

def BrowseDest():
  dstraw = tk.filedialog.askdirectory()
  global dst
  dst = dstraw.replace('\\','//')+"//"
  dstEntry = Entry(mGui)
  dstEntry.configure(width=60)
  dstEntry.pack(side=TOP)
  dstEntry.delete(0,END)
  dstEntry.insert(0,"Destination folder:   " + dstraw)
  Transfer(src,dst)
  return dst


def TimeStampOfSorting(now):
  with sqlite3.connect("database.db") as connection:
    c = connection.cursor()
    c.execute("INSERT INTO TStbl(timestamp) VALUES (?)", (str(datetime.datetime.now()),))

    ## set theTS type
    theTS = StringVar()
    
    theTS = c.execute("SELECT timestamp FROM TStbl WHERE id=(SELECT MAX(id) FROM TStbl) ").fetchone()

    theTSval = ''.join(map(str,theTS))
    showTS = Entry(mGui)
    showTS.configure( width = 80 )
    showTS.pack(side=TOP)
    showTS.delete(0,END)
    showTS.insert(0,"Files have been sorted. Time of sorting:   " + theTSval)
    connection.commit()
    

def Transfer(src,dst):

  if (src!="" and dst!=""):
    
    myfiles = os.listdir(src)
    now = datetime.datetime.now()

    listOld=Listbox(mGui)
    listOld.pack(fill=BOTH, expand=1)
    listOld.insert(END, "Files not modified or created in the last 24 hours:\n")

    listCopies=Listbox(mGui)
    listCopies.pack(fill=BOTH, expand=1)
    listCopies.insert(END, "Files copied to " + dst + " :\n")
    
    # CALL TIMESTAMP
    TimeStampOfSorting(now)

    for file in myfiles:

      osFunction = os.path.getmtime(src+file)
      ageInSeconds = datetime.datetime.fromtimestamp(osFunction)
      difference = now - ageInSeconds
      differenceSec = difference.total_seconds()

      if differenceSec > (24*60*60):
        listOld.insert(END, file)

      else:
        shutil.copy( src + file , dst )
        listCopies.insert(END, file)


def TimeStampOfLastRuntime():
  with sqlite3.connect("database.db") as connection:
    c = connection.cursor()

    ## set theTS type
    theTS = StringVar()
    theTS = c.execute("SELECT timestamp FROM TStbl WHERE id=(SELECT MAX(id) FROM TStbl) ").fetchone()
    theTSval = ''.join(map(str,theTS))
    showTS = Entry(mGui)
    showTS.configure(width=60)
    showTS.pack(side=TOP)
    showTS.delete(0,END)
    showTS.insert(0,"Last runtime:   " + theTSval)


#creates a label under title 
mTitleLabel = Label(mGui, text= "This tool will copy files modified or created within 24 hours").pack(side=TOP)

# creates a button that calls def BrowseSrc()
mSrcButton = Button(mGui, text="Pick source folder", command = BrowseSrc, fg="#e6ffff",bg="#0000ff").pack(side=TOP) #expand=TRUE
# creates a button that finds dst folder
mDstButton = Button(mGui, text="Pick destination folder", command = BrowseDest, fg="#0000ff",bg="#e6ffff").pack(side=TOP)#expand=TRUE
# CALL FOR LAST RUNTIME TO BE DISPLAYED
TimeStampOfLastRuntime()


