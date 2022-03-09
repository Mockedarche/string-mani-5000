from tkinter import *
from tkinter import filedialog
import os
import subprocess, sys
import re
import time
from tkinter.messagebox import showinfo
from tkinter import ttk

#global variable locationoffiles is simply a easy way to keep track of all files requests to be worked on
global locationoffiles
locationoffiles = []

#filesreadin is all the data of each file requests to be worked on
filesreadin = []

# closed the main gui and thus closes the entire program.
def quitapp():
    gui.destroy()

def closefilereads():
    fLR.flush()
    fLR.close()

def getwritelocation():
    global fLR
    fLR = filedialog.asksaveasfile(mode='w', defaultextension=".txt")

def writefileLR(line):
    if "\n" not in line:
        line = line + "\n"
    try:
        fLR.write(line)
    except:
        getwritelocation()
        fLR.write(line)


#multiple comments out show differences in development. Now it simply asks the user where to save the file and what name each time a task is done.
def writefile(data):
    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:
        return

    if locationoffiles:

        for i in data:
            f.write(str(i))

        f.flush()
        f.close()

#updates the output field aka the location where selected file locations are shown.
def updateoutput():
    output.insert(END, "COMPLETED TASK RESETTING")
    # time.sleep(2)
    filesreadin.clear()
    locationoffiles.clear()
    output.delete('1.0', END)

#opens a filedialog to find what files the user wants to work with.
def select():
    gui.filename = filedialog.askopenfilename(initialdir="/Users/mockedarche/Downloads", title="Select A File",
                                              filetypes=(("All files", "*.*"),))
    # locationoftxt = Label(gui, text=gui.filename)
    locationoftxt = gui.filename
    # print(locationoftxt)
    locationoffiles.append(locationoftxt)
    output.insert(END, locationoftxt)
    output.insert(END, "\n")

#the gui window for all trim tasks
def trimwindow():
    guitrim = Toplevel()
    before = 'before'
    after = 'after'
    guitrim.title("Configure clip")
    guitrim.geometry('420x100')
    guitrim.resizable(0, 0)
    textentrytrim = Entry(guitrim, width=20, bg="grey")
    textentrytrim.grid(row=0, column=0, sticky=W)
    Button(guitrim, text="take before", width=7, command=lambda: trim(textentrytrim, before)).grid(row=0, column=1,
                                                                                                    sticky=W)
    Button(guitrim, text="take after", width=7, command=lambda: trim(textentrytrim, after)).grid(row=0, column=2,
                                                                                                  sticky=W)
    guitrim.mainloop()

#trims either before the separator or after (keeps before or after). //updated for new LR write
def trim(text, BorA):
    text = text.get()

    if BorA == "before":
        for i in locationoffiles:
            fp = open(i, "r")
            for j in fp:
                j = j.split(text)[0]
                writefileLR(j)
            fp.close()

    else:
        for i in locationoffiles:
            fp = open(i, "r")
            for j in fp:
                j = j.split(text, 1)[1]
                writefileLR(j)
            fp.close()


    closefilereads()
    #writefile(trimedlist)
    updateoutput()

#Gui for all removal tasks
def removalgui():
    guisremoval = Toplevel()
    guisremoval.title("removal (case sensitive)")
    guisremoval.geometry("420x125")
    guisremoval.resizable(0, 0)

    textentryremoval = Entry(guisremoval, width=9, bg="grey")
    textentryremoval.grid(row=0, column=0, sticky=W)
    textentryremovalnum = Entry(guisremoval, width=9, bg="grey")
    textentryremovalnum.grid(row=0, column=1, sticky=W)

    Button(guisremoval, text="Remove all", width=7, command=lambda: removeall(textentryremoval.get())).grid(row=1,
                                                                                                            column=0,
                                                                                                            sticky=W)
    Button(guisremoval, text="First oc", width=7, command=lambda: removefirstoc(textentryremoval.get())).grid(row=2,
                                                                                                              column=0,
                                                                                                              sticky=W)
    Button(guisremoval, text="Last oc", width=7, command=lambda: removelastoc(textentryremoval.get())).grid(row=3,
                                                                                                            column=0,
                                                                                                            sticky=W)
    Button(guisremoval, text="x first oc", width=7,
           command=lambda: removexfoc(textentryremoval.get(), textentryremovalnum.get())).grid(row=1, column=1,
                                                                                               sticky=W)
    Button(guisremoval, text="x last oc", width=7,
           command=lambda: removexloc(textentryremoval.get(), textentryremovalnum.get())).grid(row=2, column=1,
                                                                                               sticky=W)

    guisremoval.mainloop()

#removes all characters or strings from each line. Note removes ALL instances of the requested character or string.//updated for new LR write
def removeall(toremove):
    removallist = []
    # print("Here")


    for i in locationoffiles:
        fp = open(i, "r")
        for j in fp:
            writefileLR(j.replace(toremove, ""))
        fp.close()

    closefilereads()
    #writefile(removallist)
    updateoutput()

#removes only the first occurence of a character or string (left to right)
def removefirstoc(toremove):

    for i in locationoffiles:
        fp = open(i, "r")
        for j in fp:
            writefileLR(j.replace(toremove, "", 1))
        fp.close()

    closefilereads()
    updateoutput()

#removes only the last occurence of a character or string (right to left)
def removelastoc(toremove):
    removallist = []

    for i in locationoffiles:
        fp = open(i, "r")
        for j in fp:
            line = j[::-1].replace(toremove[::-1], "", 1)[::-1]
            writefileLR(line)
        fp.close()

    closefilereads()
    updateoutput()

#removes x number of instances of characters or strings (left to right)
def removexfoc(toremove, num):
    removallist = []

    for i in locationoffiles:
        fp = open(i, "r")
        for j in fp:
            writefileLR(j.replace(toremove, "", int(num)))
        fp.close()

    closefilereads()
    #writefile(removallist)
    updateoutput()

#removes x number of instances of characters or strings (right to left)
def removexloc(toremove, num):
    removallist = []

    for i in locationoffiles:
        fp = open(i, "r")
        for j in fp:
            line = j[::-1].replace(toremove[::-1], "", int(num))[::-1]
            writefileLR(line)
        fp.close()

    closefilereads()
    #writefile(removallist)
    updateoutput()

#gui for all tasks that work with cases (a A)
def casesgui():
    guicases = Toplevel()
    guicases.title("Case manipulation")
    guicases.geometry("420x100")
    guicases.resizable(0, 0)

    textentrycases = Entry(guicases, width=9, bg="grey")
    textentrycases.grid(row=0, column=0, sticky=W)
    textentrycasesnum = Entry(guicases, width=9, bg="grey")
    textentrycasesnum.grid(row=0, column=1, sticky=W)

    Button(guicases, text="Up all", width=7, command=lambda: Uppercaseall()).grid(row=1, column=0, sticky=W)
    Button(guicases, text="Low all", width=7, command=lambda: Lowercaseall()).grid(row=2, column=0, sticky=W)
    Button(guicases, text="Step up", width=7, command=lambda: Stepup(textentrycasesnum.get())).grid(row=1, column=1,
                                                                                                    sticky=W)
    Button(guicases, text="Step low", width=7, command=lambda: Steplow(textentrycasesnum.get())).grid(row=2, column=1,
                                                                                                      sticky=W)
    Button(guicases, text="Only x up", width=7, command=lambda: Onlyxup(textentrycases.get())).grid(row=1, column=2,
                                                                                                    sticky=W)
    Button(guicases, text="Only x low", width=7, command=lambda: Onlyxlow(textentrycases.get())).grid(row=2, column=2,
                                                                                                      sticky=W)

#uppercases all letters in the entire string
def Uppercaseall():
    caseslist = []

    for i in locationoffiles:
        fp = open(i, "r")
        for j in fp:
            writefileLR(str(j).upper())
        fp.close()

    closefilereads()
    #writefile(caseslist)
    updateoutput()

#lowercases all letters in the entire string
def Lowercaseall():
    caselist = []

    for i in locationoffiles:
        fp = open(i, "r")
        for j in fp:
            writefileLR(str(j).lower())
        fp.close()

    closefilereads()
    #writefile(caselist)
    updateoutput()

#uppercases letters following a step such as 1 (aAaAaA)
def Stepup(num):
    caselist = []

    for i in locationoffiles:
        fp = open(i, "r")
        for j in fp:
            a = list(j)
            a[2::int(num)] = [x.upper() for x in a[2::int(num)]]
            s = ''.join(a)
            writefileLR(s)
        fp.close()

    closefilereads()
    #writefile(caselist)
    updateoutput()

#lowercases letters following a step such as 1(AaAaAa)
def Steplow(num):
    caselist = []

    for i in locationoffiles:
        fp = open(i, "r")
        for j in fp:
            a = list(j)
            a[2::int(num)] = [x.lower() for x in a[2::int(num)]]
            s = ''.join(a)
            writefileLR(s)
        fp.close()

    closefilereads()
    #writefile(caselist)
    updateoutput()

#uppercaes all instances of a certain letter such as 'a' (Ask the tAll mAn)
def Onlyxup(letter):
    caselist = []

    if str(letter).islower():
        uppercaseletter = str(letter).upper()
    else:
        uppercaseletter = letter
        letter = str(letter).lower()

    for i in locationoffiles:
        fp = open(i, "r")
        for j in fp:
            writefileLR(j.replace(letter, uppercaseletter))
        fp.close()

    closefilereads()
    #writefile(caselist)
    updateoutput()

#lowercasses all instances of a certain letter such as 'a' (aSK THE TaLL MaN)
def Onlyxlow(letter):
    caselist = []

    if str(letter).isupper():
        lowercaseletter = str(letter).lower()
    else:
        lowercaseletter = letter
        letter = str(letter).upper()

    for i in locationoffiles:
        fp = open(i, "r")
        for j in fp:
            writefileLR(j.replace(letter, lowercaseletter))
        fp.close()

    closefilereads()
    #writefile(caselist)
    updateoutput()

#the gui for all insert tasks
def insertgui():
    guiinsert = Toplevel()
    guiinsert.title("Insert")
    guiinsert.geometry("420x100")
    guiinsert.resizable(0, 0)

    textentryinsert = Entry(guiinsert, width=10, bg="grey")
    textentryinsert.grid(row=0, column=0, sticky=W)
    textentryinsertnum = Entry(guiinsert, width=10, bg="grey")
    textentryinsertnum.grid(row=0, column=1, sticky=W)

    Button(guiinsert, text="front", width=7, command=lambda: insertfront(textentryinsert.get())).grid(row=1, column=0,
                                                                                                      sticky=W)
    Button(guiinsert, text="end", width=7, command=lambda: insertend(textentryinsert.get())).grid(row=2, column=0,
                                                                                                  sticky=W)
    Button(guiinsert, text="insertatX", width=7,
           command=lambda: insertatX(textentryinsert.get(), textentryinsertnum.get())).grid(row=1, column=1, sticky=W)
    Button(guiinsert, text="insertstep", width=7,
           command=lambda: insertstep(textentryinsert.get(), textentryinsertnum.get())).grid(row=2, column=1, sticky=W)

#inserts the character or string given in the front of each line (left to right)
def insertfront(toinsert):
    insertlist = []

    for i in locationoffiles:
        fp = open(i, "r")
        for j in fp:
            writefileLR(toinsert + j)
        fp.close()


    closefilereads()
    #writefile(insertlist)
    updateoutput()

#inserts the character or string given in the back of each line (right to left)
def insertend(toinsert):
    insertlist = []

    for i in locationoffiles:
        fp = open(i, "r")
        for j in fp:
            j = j.strip('\n')
            writefileLR(j + toinsert + '\n')
        fp.close()

    closefilereads()
    #writefile(insertlist)
    updateoutput()

#inserts a character or string at a certain index of a string. NOTE if the string length is shorter than the string nothing is inserted.
def insertatX(toinsert, location):
    insertlist = []


    for i in locationoffiles:
        fp = open(i, "r")
        for j in fp:
            writefileLR(j[0:int(location)] + toinsert +j[int(location):len(j)])
        fp.close()

    closefilereads()
    #writefile(insertlist)
    updateoutput()

#inserts a character or string on a step such as dog ever 2 (I doglodogvedog tdogo dogwadoglk) from (I love to talk)
def insertstep(toinsert, step):
    insertlist = []

    for i in locationoffiles:
        fp = open(i, "r")
        for j in fp:
            writefileLR(toinsert.join(j[i:i + int(step)] for i in range(0, len(j), int(step))))
        fp.close()

    closefilereads()
    #writefile(insertlist)
    updateoutput()

#the gui for all analyze tasks
def analyzegui():
    guianalyze = Toplevel()
    guianalyze.title("Analyze")
    guianalyze.geometry("420x100")

    textentryanalyze = Entry(guianalyze, width=10, bg="grey")
    textentryanalyze.grid(row=0, column=0, sticky=W)
    textentryanalyzenum = Entry(guianalyze, width=10, bg="grey")
    textentryanalyzenum.grid(row=0, column=1, sticky=W)

    Button(guianalyze, text="Frequency", width=7, command=lambda: frequency()).grid(row=1, column=0, sticky=W)

#lists the frequency of all characters in a file. (such as a = 8 meaning 8 lowercase letter a's are in the entire file)
def frequency():
    curIndex = 0
    charList = [ '!' ,'"' ,'#' ,'$' ,'%' ,'&' ,'\'' ,'(' ,')' ,'*' ,'+' ,',' ,'-' ,'.' ,'/' ,'0' ,'1' ,'2' ,'3' ,'4' ,'5' ,'6' ,'7' ,'8' ,'9' ,':' ,';' ,'<' ,'=' ,'>' ,'?' ,'@' ,'A' ,'B' ,'C' ,'D' ,'E' ,'F' ,'G' ,'H' ,'I' ,'J' ,'K' ,'L' ,'M' ,'N' ,'O' ,'P' ,'Q' ,'R' ,'S' ,'T' ,'U' ,'V' ,'W' ,'X' ,'Y' ,'Z' ,'[' ,'\\' ,']' ,'^' ,'_' ,'`' ,'a' ,'b' ,'c' ,'d' ,'e' ,'f' ,'g' ,'h' ,'i' ,'j' ,'k' ,'l' ,'m' ,'n' ,'o' ,'p' ,'q' ,'r' ,'s' ,'t' ,'u' ,'v' ,'w' ,'x' ,'y' ,'z' ,'{' ,'|' ,'}' ,'~', '\n' ]
    charNumList = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]


    for i in locationoffiles:
        fp = open(i, mode='r', encoding='utf8', errors='replace')
        for j in fp:
            for k in j:
                try:
                    curIndex = charList.index(k)
                    charNumList[curIndex] += 1
                except ValueError:
                    charList.append(k)
                    charNumList.append(0)

        fp.close()


    for i in range(len(charList) - 1):
        writefileLR(charList[i] + " = " + str(charNumList[i]))



    closefilereads()
    updateoutput()

#the help button triggers the systems text editor to open the help.txt which contains the manual
def help(): #needs windows (operating system) support
    filename = "help.txt"
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, filename])


#the main gui window
gui = Tk(className="String modulator 5000")

gui.configure(background="#3b3937")

gui.geometry('720x220')

# Photo to give some personality
photo1 = PhotoImage(file="justsmallface_25.png")
Label(gui, image=photo1, bg="black").grid(row=0, column=0, sticky=W)

#made forced size to enable a simpler design
gui.resizable(0, 0) #Make a scaler option (such as simply doubling the gui.geometry('720x240')

# button to select files
Button(gui, text="Select", width=7, command=select).grid(row=1, column=0, sticky=W)

output = Text(gui, width=84, height=6, wrap=WORD, background="grey")
output.grid(row=0, column=1, columnspan=2, sticky=W)

# button for trimming
Button(gui, text="Trim", width=7, command=trimwindow).grid(row=2, column=0, sticky=W)

# button for removal
Button(gui, text="Removal", width=7, command=removalgui).grid(row=3, column=0, sticky=W)

# button for changing cases
Button(gui, text="Cases", width=7, command=casesgui).grid(row=1, column=1, sticky=W)

# button for inserting

Button(gui, text="Insert", width=7, command=insertgui).grid(row=2, column=1, sticky=W)

# button to quit the appilcation and all other windows
Button(gui, text="Quit", width=7, command=quitapp).grid(row=4, column=0, sticky=W)

# button for the analyzation of files
Button(gui, text="Analyze", width=7, command=analyzegui).grid(row=3, column=1, sticky=W)

# button for help
Button(gui, text="Help", width=7, command=help).grid(row=4, column=1, sticky=W)

#Button(gui, text="test", width=7, command=tester).grid(row=1, column=2, sticky=W)

gui.mainloop()
