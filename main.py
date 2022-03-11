'''
String mani 5000
This program is quite simple. It's just a gui using tkinter to easily maniplulate a file(s) lines in a desired way and output them to a new file.
Currently works with any python version that support tkinter and supports Linux, Macos, and Windows
NOTE currently only .txt fortmat has been tested (RTF is known to not work)
'''

from tkinter import *
from tkinter import filedialog
import subprocess, sys
import time


# global variable locationoffiles is simply a easy way to keep track of all files requests to be worked on
global locationoffiles
locationoffiles = []

# closed the main gui and thus closes the entire program.
def quitapp():
    gui.destroy()

# determine how often to update (more times for larger work loads)
def getUpdateInterval(numLines):
    # previous attempt at making a good scaler for update frequency
    # math.pow(2, math.log(numLines, 10)*2)) * 4)

    if(numLines > 10000000):
        return int(numLines/ 250)
    else:
        return int(numLines / 10)

# updates the progress with what file we're on, what line we're on, and what percentage we are complete
def updateProgress(fileNum, curLine, numberOfLines):
    progressOP.delete('1.0', END)
    if(numberOfLines > 0):
        progressOP.insert(END,  "File (" + str(fileNum) + "/" + str(len(locationoffiles)) + ")\n" + "Line (" + str(curLine) + "/" + str(numberOfLines) + ")\n " + format((curLine/numberOfLines) * 100, '.2f') + "%")

# uppdates the progress output to show that we're counting the number of lines in the file
def progressReadLines():
    progressOP.delete('1.0', END)
    progressOP.insert(END, "Reading num \nof lines")

# quickly gets the number of lines in a file
def getLineCount(filename):
    f = open(filename,  mode='r', encoding='utf8', errors='replace')
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.read

    buf = read_f(buf_size)
    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)

    return lines

# closes all file readins
def closefilereads():
    fLR.flush()
    fLR.close()

# gets the desired output location
def getwritelocation():
    global fLR
    fLR = filedialog.asksaveasfile(mode='w', defaultextension=".txt")

# writes the given line to the output file if it doesn't exist it gets it
def writefileLR(line):
    if "\n" not in line:
        line = line + "\n"
    try:
        fLR.write(line)
    except:
        getwritelocation()
        fLR.write(line)


# multiple comments out show differences in development. Now it simply asks the user where to save the file and what name each time a task is done.
def writefile(data):
    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:
        return

    if locationoffiles:
        for i in data:
            f.write(str(i))

        f.flush()
        f.close()

# updates the output field aka the location where selected file locations are shown.
def updateoutput():
    output.insert(END, "COMPLETED TASK RESETTING")
    locationoffiles.clear()
    output.delete('1.0', END)
    progressOP.delete('1.0', END)
    progressOP.insert(END, "completed")

# opens a filedialog to find what files the user wants to work with.
def select():
    gui.filename = filedialog.askopenfilename(initialdir="/Users/mockedarche/Downloads", title="Select A File",
                                              filetypes=(("All files", "*.*"),))

    locationoftxt = gui.filename
    locationoffiles.append(locationoftxt)
    output.insert(END, locationoftxt)
    output.insert(END, "\n")

# the gui window for all trim tasks
def trimwindow():
    guitrim = Toplevel()
    before = 'before'
    after = 'after'
    guitrim.title("Configure trim")
    guitrim.geometry('420x100')
    guitrim.resizable(0, 0)

    Label(guitrim, text="string").grid(column=0, row=0, sticky=W)
    #Label(guitrim, text="step").grid(column=1, row=0, sticky=W)


    textentrytrim = Entry(guitrim, width=20, bg="grey")
    textentrytrim.grid(row=1, column=0, sticky=W)
    Button(guitrim, text="take before", width=7, command=lambda: trim(textentrytrim, before)).grid(row=1, column=1,
                                                                                                    sticky=W)
    Button(guitrim, text="take after", width=7, command=lambda: trim(textentrytrim, after)).grid(row=1, column=2,
                                                                                                  sticky=W)
    guitrim.mainloop()

# trims either before or after the separator excluding separator
def trim(text, BorA):
    getwritelocation()
    fileCount = 0
    text = text.get()

    if BorA == "before":
        for i in locationoffiles:
            progressReadLines()
            gui.update()
            numOfLines = getLineCount(i)
            updateInterval = getUpdateInterval(numOfLines)
            curLineNum = 0
            fileCount += 1
            fp = open(i, mode='r', encoding='utf8', errors='replace')
            if (numOfLines > 0 and updateInterval > 0):
                for j in fp:
                    try:
                        j = j.split(text)[0]
                        writefileLR(j)
                        curLineNum += 1
                        if curLineNum % updateInterval == 0:
                            updateProgress(fileCount, curLineNum, numOfLines)
                            gui.update()
                    except IndexError:
                        writefileLR(j)
                        curLineNum += 1
                        if curLineNum % updateInterval == 0:
                            updateProgress(fileCount, curLineNum, numOfLines)
                            gui.update()
                fp.close()

    else:
        for i in locationoffiles:
            progressReadLines()
            gui.update()
            numOfLines = getLineCount(i)
            updateInterval = getUpdateInterval(numOfLines)
            curLineNum = 0
            fileCount += 1
            fp = open(i, mode='r', encoding='utf8', errors='replace')
            if (numOfLines > 0 and updateInterval > 0):
                for j in fp:
                    try:
                        j = j.split(text, 1)[1]
                        writefileLR(j)
                        curLineNum += 1
                        if curLineNum % updateInterval == 0:
                            updateProgress(fileCount, curLineNum, numOfLines)
                            gui.update()
                    except IndexError:
                        writefileLR(j)
                        curLineNum += 1
                        if curLineNum % updateInterval == 0:
                            updateProgress(fileCount, curLineNum, numOfLines)
                            gui.update()
                fp.close()


    closefilereads()
    updateoutput()

# Gui for all removal tasks
def removalgui():
    guisremoval = Toplevel()
    guisremoval.title("removal (case sensitive)")
    guisremoval.geometry("420x140")
    guisremoval.resizable(0, 0)

    Label(guisremoval, text="string").grid(column=0, row=0, sticky=W)
    Label(guisremoval, text="step").grid(column=1, row=0, sticky=W)

    textentryremoval = Entry(guisremoval, width=9, bg="grey")
    textentryremoval.grid(row=1, column=0, sticky=W)
    textentryremovalnum = Entry(guisremoval, width=9, bg="grey")
    textentryremovalnum.grid(row=1, column=1, sticky=W)

    Button(guisremoval, text="Remove all", width=7, command=lambda: removeall(textentryremoval.get())).grid(row=2,
                                                                                                            column=0,
                                                                                                            sticky=W)
    Button(guisremoval, text="First oc", width=7, command=lambda: removefirstoc(textentryremoval.get())).grid(row=3,
                                                                                                              column=0,
                                                                                                              sticky=W)
    Button(guisremoval, text="Last oc", width=7, command=lambda: removelastoc(textentryremoval.get())).grid(row=4,
                                                                                                            column=0,
                                                                                                            sticky=W)
    Button(guisremoval, text="x first oc", width=7,
           command=lambda: removexfoc(textentryremoval.get(), textentryremovalnum.get())).grid(row=2, column=1,
                                                                                               sticky=W)
    Button(guisremoval, text="x last oc", width=7,
           command=lambda: removexloc(textentryremoval.get(), textentryremovalnum.get())).grid(row=3, column=1,
                                                                                               sticky=W)

    guisremoval.mainloop()

# removes all characters or strings from each line. Note removes ALL instances of the requested character or string.//updated for new LR write
def removeall(toremove):
    getwritelocation()
    fileCount = 0


    for i in locationoffiles:
        progressReadLines()
        gui.update()
        numOfLines = getLineCount(i)
        updateInterval = getUpdateInterval(numOfLines)
        curLineNum = 0
        fileCount += 1
        fp = open(i, mode='r', encoding='utf8', errors='replace')
        if (numOfLines > 0 and updateInterval > 0):
            for j in fp:
                writefileLR(j.replace(toremove, ""))
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closefilereads()
    updateoutput()

# removes only the first occurence of a character or string (left to right)
def removefirstoc(toremove):
    getwritelocation()
    fileCount = 0

    for i in locationoffiles:
        progressReadLines()
        gui.update()
        numOfLines = getLineCount(i)
        updateInterval = getUpdateInterval(numOfLines)
        curLineNum = 0
        fileCount += 1
        fp = open(i, mode='r', encoding='utf8', errors='replace')
        if (numOfLines > 0 and updateInterval > 0):
            for j in fp:
                writefileLR(j.replace(toremove, "", 1))
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closefilereads()
    updateoutput()

# removes only the last occurence of a character or string (right to left)
def removelastoc(toremove):
    getwritelocation()
    fileCount = 0

    for i in locationoffiles:
        progressReadLines()
        gui.update()
        numOfLines = getLineCount(i)
        updateInterval = getUpdateInterval(numOfLines)
        curLineNum = 0
        fileCount += 1
        fp = open(i, mode='r', encoding='utf8', errors='replace')
        if (numOfLines > 0 and updateInterval > 0):
            for j in fp:
                line = j[::-1].replace(toremove[::-1], "", 1)[::-1]
                writefileLR(line)
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closefilereads()
    updateoutput()

# removes x number of instances of characters or strings (left to right)
def removexfoc(toremove, num):
    getwritelocation()
    fileCount = 0

    for i in locationoffiles:
        progressReadLines()
        gui.update()
        numOfLines = getLineCount(i)
        updateInterval = getUpdateInterval(numOfLines)
        curLineNum = 0
        fileCount += 1
        fp = open(i, mode='r', encoding='utf8', errors='replace')
        if (numOfLines > 0 and updateInterval > 0):
            for j in fp:
                writefileLR(j.replace(toremove, "", int(num)))
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closefilereads()
    updateoutput()

# removes x number of instances of characters or strings (right to left)
def removexloc(toremove, num):
    getwritelocation()
    fileCount = 0

    for i in locationoffiles:
        progressReadLines()
        gui.update()
        numOfLines = getLineCount(i)
        updateInterval = getUpdateInterval(numOfLines)
        curLineNum = 0
        fileCount += 1
        fp = open(i, mode='r', encoding='utf8', errors='replace')
        if (numOfLines > 0 and updateInterval > 0):
            for j in fp:
                line = j[::-1].replace(toremove[::-1], "", int(num))[::-1]
                writefileLR(line)
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closefilereads()
    updateoutput()

# gui for all tasks that work with cases (a A)
def casesgui():
    guicases = Toplevel()
    guicases.title("Case manipulation")
    guicases.geometry("420x120")
    guicases.resizable(0, 0)

    Label(guicases, text="string").grid(column=0, row=0, sticky=W)
    Label(guicases, text="step").grid(column=1, row=0, sticky=W)

    textentrycases = Entry(guicases, width=9, bg="grey")
    textentrycases.grid(row=1, column=0, sticky=W)
    textentrycasesnum = Entry(guicases, width=9, bg="grey")
    textentrycasesnum.grid(row=1, column=1, sticky=W)

    Button(guicases, text="Up all", width=7, command=lambda: Uppercaseall()).grid(row=2, column=0, sticky=W)
    Button(guicases, text="Low all", width=7, command=lambda: Lowercaseall()).grid(row=3, column=0, sticky=W)
    Button(guicases, text="Step up", width=7, command=lambda: Stepup(textentrycasesnum.get())).grid(row=2, column=1,
                                                                                                    sticky=W)
    Button(guicases, text="Step low", width=7, command=lambda: Steplow(textentrycasesnum.get())).grid(row=3, column=1,
                                                                                                      sticky=W)
    Button(guicases, text="Only x up", width=7, command=lambda: Onlyxup(textentrycases.get())).grid(row=2, column=2,
                                                                                                    sticky=W)
    Button(guicases, text="Only x low", width=7, command=lambda: Onlyxlow(textentrycases.get())).grid(row=3, column=2,
                                                                                                      sticky=W)

# uppercases all letters in the entire string
def Uppercaseall():
    getwritelocation()
    fileCount = 0

    for i in locationoffiles:
        progressReadLines()
        gui.update()
        numOfLines = getLineCount(i)
        updateInterval = getUpdateInterval(numOfLines)
        curLineNum = 0
        fileCount += 1
        fp = open(i, mode='r', encoding='utf8', errors='replace')
        if (numOfLines > 0 and updateInterval > 0):
            for j in fp:
                writefileLR(str(j).upper())
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closefilereads()
    updateoutput()

# lowercases all letters in the entire string
def Lowercaseall():
    getwritelocation()
    fileCount = 0

    for i in locationoffiles:
        progressReadLines()
        gui.update()
        numOfLines = getLineCount(i)
        updateInterval = getUpdateInterval(numOfLines)
        curLineNum = 0
        fileCount += 1
        fp = open(i, mode='r', encoding='utf8', errors='replace')
        if (numOfLines > 0 and updateInterval > 0):
            for j in fp:
                writefileLR(str(j).lower())
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closefilereads()
    updateoutput()

# uppercases letters following a step such as 1 (aAaAaA)
def Stepup(num):
    getwritelocation()
    fileCount = 0

    for i in locationoffiles:
        progressReadLines()
        gui.update()
        numOfLines = getLineCount(i)
        updateInterval = getUpdateInterval(numOfLines)
        curLineNum = 0
        fileCount += 1
        fp = open(i, mode='r', encoding='utf8', errors='replace')
        if (numOfLines > 0 and updateInterval > 0):
            for j in fp:
                a = list(j)
                a[2::int(num)] = [x.upper() for x in a[2::int(num)]]
                s = ''.join(a)
                writefileLR(s)
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closefilereads()
    updateoutput()

# lowercases letters following a step such as 1(AaAaAa)
def Steplow(num):
    getwritelocation()
    fileCount = 0

    for i in locationoffiles:
        progressReadLines()
        gui.update()
        numOfLines = getLineCount(i)
        updateInterval = getUpdateInterval(numOfLines)
        curLineNum = 0
        fileCount += 1
        fp = open(i, mode='r', encoding='utf8', errors='replace')
        if (numOfLines > 0 and updateInterval > 0):
            for j in fp:
                a = list(j)
                a[2::int(num)] = [x.lower() for x in a[2::int(num)]]
                s = ''.join(a)
                writefileLR(s)
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closefilereads()
    updateoutput()

# uppercaes all instances of a certain letter such as 'a' (Ask the tAll mAn)
def Onlyxup(letter):
    getwritelocation()
    fileCount = 0

    if str(letter).islower():
        uppercaseletter = str(letter).upper()
    else:
        uppercaseletter = letter
        letter = str(letter).lower()

    for i in locationoffiles:
        progressReadLines()
        gui.update()
        numOfLines = getLineCount(i)
        updateInterval = getUpdateInterval(numOfLines)
        curLineNum = 0
        fileCount += 1
        fp = open(i, mode='r', encoding='utf8', errors='replace')
        if (numOfLines > 0 and updateInterval > 0):
            for j in fp:
                writefileLR(j.replace(letter, uppercaseletter))
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closefilereads()
    updateoutput()

# lowercasses all instances of a certain letter such as 'a' (aSK THE TaLL MaN)
def Onlyxlow(letter):
    getwritelocation()
    fileCount = 0

    if str(letter).isupper():
        lowercaseletter = str(letter).lower()
    else:
        lowercaseletter = letter
        letter = str(letter).upper()

    for i in locationoffiles:
        progressReadLines()
        gui.update()
        numOfLines = getLineCount(i)
        updateInterval = getUpdateInterval(numOfLines)
        curLineNum = 0
        fileCount += 1
        fp = open(i, mode='r', encoding='utf8', errors='replace')
        if (numOfLines > 0 and updateInterval > 0):
            for j in fp:
                writefileLR(j.replace(letter, lowercaseletter))
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closefilereads()
    updateoutput()

# the gui for all insert tasks
def insertgui():
    guiinsert = Toplevel()
    guiinsert.title("Insert")
    guiinsert.geometry("420x120")
    guiinsert.resizable(0, 0)

    Label(guiinsert, text="to insert").grid(column=0, row=0, sticky=W)
    Label(guiinsert, text="step/loc").grid(column=1, row=0, sticky=W)

    textentryinsert = Entry(guiinsert, width=10, bg="grey")
    textentryinsert.grid(row=1, column=0, sticky=W)
    textentryinsertnum = Entry(guiinsert, width=10, bg="grey")
    textentryinsertnum.grid(row=1, column=1, sticky=W)

    Button(guiinsert, text="front", width=7, command=lambda: insertfront(textentryinsert.get())).grid(row=2, column=0,
                                                                                                      sticky=W)
    Button(guiinsert, text="end", width=7, command=lambda: insertend(textentryinsert.get())).grid(row=3, column=0,
                                                                                                  sticky=W)
    Button(guiinsert, text="insertatX", width=7,
           command=lambda: insertatX(textentryinsert.get(), textentryinsertnum.get())).grid(row=2, column=1, sticky=W)
    Button(guiinsert, text="insertstep", width=7,
           command=lambda: insertstep(textentryinsert.get(), textentryinsertnum.get())).grid(row=3, column=1, sticky=W)

# inserts the character or string given in the front of each line (left to right)
def insertfront(toinsert):
    getwritelocation()
    fileCount = 0

    for i in locationoffiles:
        progressReadLines()
        gui.update()
        numOfLines = getLineCount(i)
        updateInterval = getUpdateInterval(numOfLines)
        curLineNum = 0
        fileCount += 1
        fp = open(i, mode='r', encoding='utf8', errors='replace')
        if (numOfLines > 0 and updateInterval > 0):
            for j in fp:
                writefileLR(toinsert + j)
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closefilereads()
    updateoutput()

# inserts the character or string given in the back of each line (right to left)
def insertend(toinsert):
    getwritelocation()
    fileCount = 0

    for i in locationoffiles:
        progressReadLines()
        gui.update()
        numOfLines = getLineCount(i)
        updateInterval = getUpdateInterval(numOfLines)
        curLineNum = 0
        fileCount += 1
        fp = open(i, mode='r', encoding='utf8', errors='replace')
        if (numOfLines > 0 and updateInterval > 0):
            for j in fp:
                j = j.strip('\n')
                writefileLR(j + toinsert + '\n')
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closefilereads()
    updateoutput()

# inserts a character or string at a certain index of a string. NOTE if the string length is shorter than the string nothing is inserted.
def insertatX(toinsert, location):
    getwritelocation()
    fileCount = 0


    for i in locationoffiles:
        progressReadLines()
        gui.update()
        numOfLines = getLineCount(i)
        updateInterval = getUpdateInterval(numOfLines)
        curLineNum = 0
        fileCount += 1
        fp = open(i, mode='r', encoding='utf8', errors='replace')
        if (numOfLines > 0 and updateInterval > 0):
            for j in fp:
                writefileLR(j[0:int(location)] + toinsert +j[int(location):len(j)])
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closefilereads()
    updateoutput()

# inserts a character or string on a step such as dog ever 2 (I doglodogvedog tdogo dogwadoglk) from (I love to talk)
def insertstep(toinsert, step):
    getwritelocation()
    fileCount = 0

    for i in locationoffiles:
        progressReadLines()
        gui.update()
        numOfLines = getLineCount(i)
        updateInterval = getUpdateInterval(numOfLines)
        curLineNum = 0
        fileCount += 1
        fp = open(i, mode='r', encoding='utf8', errors='replace')
        if (numOfLines > 0 and updateInterval > 0):
            for j in fp:
                writefileLR(toinsert.join(j[i:i + int(step)] for i in range(0, len(j), int(step))))
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closefilereads()
    updateoutput()

# the gui for all analyze tasks
def analyzegui():
    guianalyze = Toplevel()
    guianalyze.title("Analyze")
    guianalyze.geometry("420x100")

    Label(guianalyze, text="placehold").grid(column=0, row=0, sticky=W)
    Label(guianalyze, text="placehold").grid(column=1, row=0, sticky=W)

    textentryanalyze = Entry(guianalyze, width=10, bg="grey")
    textentryanalyze.grid(row=1, column=0, sticky=W)
    textentryanalyzenum = Entry(guianalyze, width=10, bg="grey")
    textentryanalyzenum.grid(row=1, column=1, sticky=W)

    Button(guianalyze, text="Frequency", width=7, command=lambda: frequency()).grid(row=2, column=0, sticky=W)

# lists the frequency of all characters in a file. (such as a = 8 meaning 8 lowercase letter a's are in the entire file)
def frequency():
    getwritelocation()
    charList = [ '!' ,'"' ,'#' ,'$' ,'%' ,'&' ,'\'' ,'(' ,')' ,'*' ,'+' ,',' ,'-' ,'.' ,'/' ,'0' ,'1' ,'2' ,'3' ,'4' ,'5' ,'6' ,'7' ,'8' ,'9' ,':' ,';' ,'<' ,'=' ,'>' ,'?' ,'@' ,'A' ,'B' ,'C' ,'D' ,'E' ,'F' ,'G' ,'H' ,'I' ,'J' ,'K' ,'L' ,'M' ,'N' ,'O' ,'P' ,'Q' ,'R' ,'S' ,'T' ,'U' ,'V' ,'W' ,'X' ,'Y' ,'Z' ,'[' ,'\\' ,']' ,'^' ,'_' ,'`' ,'a' ,'b' ,'c' ,'d' ,'e' ,'f' ,'g' ,'h' ,'i' ,'j' ,'k' ,'l' ,'m' ,'n' ,'o' ,'p' ,'q' ,'r' ,'s' ,'t' ,'u' ,'v' ,'w' ,'x' ,'y' ,'z' ,'{' ,'|' ,'}' ,'~', '\n' ]
    charNumList = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    fileCount = 0


    for i in locationoffiles:
        progressReadLines()
        gui.update()
        numOfLines = getLineCount(i)
        updateInterval = getUpdateInterval(numOfLines)
        curLineNum = 0
        fileCount += 1
        fp = open(i, mode='r', encoding='utf8', errors='replace')
        if(numOfLines > 0 and updateInterval > 0):
            for j in fp:
                for k in j:
                    try:
                        curIndex = charList.index(k)
                        charNumList[curIndex] += 1
                    except ValueError:
                        charList.append(k)
                        charNumList.append(0)
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()

            fp.close()

    for i in range(len(charList) - 1):
        writefileLR(charList[i] + " = " + str(charNumList[i]))

    closefilereads()
    updateoutput()

# the help button triggers the systems text editor to open the help.txt which contains the manual
def help(): #needs windows (operating system) support
    filename = "help.txt"
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, filename])


# the main gui window
gui = Tk(className="String modulator 5000")

gui.configure(background="#3b3937")

gui.geometry('720x250')

# photo to give some personality
photo1 = PhotoImage(file="justsmallface_25.png")
Label(gui, image=photo1, bg="black").grid(row=0, column=0, sticky=W)

# made forced size to enable a simpler design
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

# progress output
progressOP = Text(gui, width=30)
progressOP.grid(row=5, column=1, sticky=W)
progressOP.insert(END, "progress")


gui.mainloop()
