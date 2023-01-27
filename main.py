'''
String mani 5000
This program is quite simple. It's just a gui using tkinter to easily maniplulate a file(s) lines in a desired way and output them to a new file.
Currently works with any python version that support tkinter and supports Linux, Macos, and Windows
NOTE currently only .txt fortmat has been tested (RTF is known to not work)
'''

# TODO do all of the replace functions and continue rewrite of variables and naming to camel case
from tkinter import *
from tkinter import filedialog
import subprocess, sys
import time


# global variable locationoffiles is simply a easy way to keep track of all files requests to be worked on
global locationoffiles
locationoffiles = []

# closed the main gui and thus closes the entire program.
def quitApp():
    gui.destroy()

# determine how often to update (more times for larger work loads)
def getUpdateInterval(numLines):
    # previous attempt at making a good scaler for update frequency
    # math.pow(2, math.log(numLines, 10)*2)) * 4)

    if(numLines > 10000000):
        return int(numLines/ 250)

    elif(numLines > 100):
        return int(numLines / 10)
    else:
        return numLines

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
def closeFileReads():
    fLR.flush()
    fLR.close()

# gets the desired output location
def getWriteLocation():
    global fLR
    fLR = filedialog.asksaveasfile(mode='w', defaultextension=".txt")

# writes the given line to the output file if it doesn't exist it gets it
def writeFileLR(line):
    if "\n" not in line:
        line = line + "\n"
    try:
        fLR.write(line)
    except:
        getWriteLocation()
        fLR.write(line)


# multiple comments out show differences in development. Now it simply asks the user where to save the file and what name each time a task is done.
def writeFile(data):
    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:
        return

    if locationoffiles:
        for i in data:
            f.write(str(i))

        f.flush()
        f.close()

# updates the output field aka the location where selected file locations are shown.
def updateOutput():
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
def trimGui():
    guitrim = Toplevel()
    before = 'before'
    after = 'after'
    guitrim.title("Configure trim")
    guitrim.geometry('420x100')
    guitrim.resizable(0, 0)

    Label(guitrim, text="string").grid(column=0, row=0, sticky=W)
    #Label(guitrim, text="step").grid(column=1, row=0, sticky=W)


    textentrytrim = Entry(guitrim, width=7, bg="grey")
    textentrytrim.grid(row=1, column=0, sticky=W)
    Button(guitrim, text="take before", width=7, command=lambda: trim(textentrytrim, before)).grid(row=2, column=0,
                                                                                                    sticky=W)
    Button(guitrim, text="take after", width=7, command=lambda: trim(textentrytrim, after)).grid(row=2, column=1,
                                                                                                  sticky=W)
    guitrim.mainloop()

# trims either before or after the separator excluding separator
def trim(text, BorA):
    getWriteLocation()
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
                        writeFileLR(j)
                        curLineNum += 1
                        if curLineNum % updateInterval == 0:
                            updateProgress(fileCount, curLineNum, numOfLines)
                            gui.update()
                    except IndexError:
                        writeFileLR(j)
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
                        writeFileLR(j)
                        curLineNum += 1
                        if curLineNum % updateInterval == 0:
                            updateProgress(fileCount, curLineNum, numOfLines)
                            gui.update()
                    except IndexError:
                        writeFileLR(j)
                        curLineNum += 1
                        if curLineNum % updateInterval == 0:
                            updateProgress(fileCount, curLineNum, numOfLines)
                            gui.update()
                fp.close()


    closeFileReads()
    updateOutput()

# Gui for all removal tasks
def removalGui():
    guisremoval = Toplevel()
    guisremoval.title("removal (case sensitive)")
    guisremoval.geometry("420x140")
    guisremoval.resizable(0, 0)

    Label(guisremoval, text="string").grid(column=0, row=0, sticky=W)
    Label(guisremoval, text="step").grid(column=1, row=0, sticky=W)
    Label(guisremoval, text="length").grid(column=2, row=0, sticky=W)

    textentryremoval = Entry(guisremoval, width=9, bg="grey")
    textentryremoval.grid(row=1, column=0, sticky=W)
    textentryremovalnum = Entry(guisremoval, width=9, bg="grey")
    textentryremovalnum.grid(row=1, column=1, sticky=W)
    textentryremovallength = Entry(guisremoval, width=9, bg="grey")
    textentryremovallength.grid(row=1, column=2, sticky=W)

    Button(guisremoval, text="Remove all", width=7, command=lambda: removeAll(textentryremoval.get())).grid(row=2,
                                                                                                            column=0,
                                                                                                            sticky=W)
    Button(guisremoval, text="First oc", width=7, command=lambda: removeFirstOC(textentryremoval.get())).grid(row=3,
                                                                                                              column=0,
                                                                                                              sticky=W)
    Button(guisremoval, text="Last oc", width=7, command=lambda: removeLastOC(textentryremoval.get())).grid(row=4,
                                                                                                            column=0,
                                                                                                            sticky=W)
    Button(guisremoval, text="x first oc", width=7,
           command=lambda: removeXFOC(textentryremoval.get(), textentryremovalnum.get())).grid(row=2, column=1,
                                                                                               sticky=W)
    Button(guisremoval, text="x last oc", width=7,
           command=lambda: removeXLOC(textentryremoval.get(), textentryremovalnum.get())).grid(row=3, column=1,
                                                                                               sticky=W)
                                                                                               
    Button(guisremoval, text="Length < x", width=7,
           command=lambda: removeLengthLessThan(textentryremovallength.get())).grid(row=2, column=2,
                                                                                               sticky=W)
    Button(guisremoval, text="Length > x", width=7,
           command=lambda: removeLengthGreaterThan(textentryremovallength.get())).grid(row=3, column=2,
                                                                                               sticky=W)
    guisremoval.mainloop()

# removes all characters or strings from each line. Note removes ALL instances of the requested character or string.//updated for new LR write
def removeAll(toremove):
    getWriteLocation()
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
                writeFileLR(j.replace(toremove, ""))
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closeFileReads()
    updateOutput()

# removes only the first occurence of a character or string (left to right)
def removeFirstOC(toremove):
    getWriteLocation()
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
                writeFileLR(j.replace(toremove, "", 1))
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closeFileReads()
    updateOutput()

# removes only the last occurence of a character or string (right to left)
def removeLastOC(toremove):
    getWriteLocation()
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
                writeFileLR(line)
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closeFileReads()
    updateOutput()

# removes x number of instances of characters or strings (left to right)
def removeXFOC(toremove, num):
    getWriteLocation()
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
                writeFileLR(j.replace(toremove, "", int(num)))
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closeFileReads()
    updateOutput()

# removes x number of instances of characters or strings (right to left)
def removeXLOC(toremove, num):
    getWriteLocation()
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
                writeFileLR(line)
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closeFileReads()
    updateOutput()
     
def removeLengthLessThan(length):
    getWriteLocation()
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
                if len(j) > int(length):
                    writeFileLR(j)
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closeFileReads()
    updateOutput()

def removeLengthGreaterThan(length):
    getWriteLocation()
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
                if len(j) < int(length) + 1:
                    writeFileLR(j)
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closeFileReads()
    updateOutput()


# gui for all tasks that work with cases (a A)
def casesGui():
    guiCases = Toplevel()
    guiCases.title("Case manipulation")
    guiCases.geometry("420x120")
    guiCases.resizable(0, 0)

    Label(guiCases, text="string").grid(column=0, row=0, sticky=W)
    Label(guiCases, text="step").grid(column=1, row=0, sticky=W)

    textentrycases = Entry(guiCases, width=9, bg="grey")
    textentrycases.grid(row=1, column=0, sticky=W)
    textentrycasesnum = Entry(guiCases, width=9, bg="grey")
    textentrycasesnum.grid(row=1, column=1, sticky=W)

    Button(guiCases, text="Up all", width=7, command=lambda: upperCaseAll()).grid(row=2, column=0, sticky=W)
    Button(guiCases, text="Low all", width=7, command=lambda: lowerCaseAlll()).grid(row=3, column=0, sticky=W)
    Button(guiCases, text="Step up", width=7, command=lambda: stepUp(textentrycasesnum.get())).grid(row=2, column=1,
                                                                                                    sticky=W)
    Button(guiCases, text="Step low", width=7, command=lambda: stepLow(textentrycasesnum.get())).grid(row=3, column=1,
                                                                                                      sticky=W)
    Button(guiCases, text="Only x up", width=7, command=lambda: onlyXUp(textentrycases.get())).grid(row=2, column=2,
                                                                                                    sticky=W)
    Button(guiCases, text="Only x low", width=7, command=lambda: onlyXLow(textentrycases.get())).grid(row=3, column=2,
                                                                                                      sticky=W)

# uppercases all letters in the entire string
def upperCaseAll():
    getWriteLocation()
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
                writeFileLR(str(j).upper())
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closeFileReads()
    updateOutput()

# lowercases all letters in the entire string
def lowerCaseAlll():
    getWriteLocation()
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
                writeFileLR(str(j).lower())
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closeFileReads()
    updateOutput()

# uppercases letters following a step such as 1 (aAaAaA)
def stepUp(num):
    getWriteLocation()
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
                writeFileLR(s)
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closeFileReads()
    updateOutput()

# lowercases letters following a step such as 1(AaAaAa)
def stepLow(num):
    getWriteLocation()
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
                writeFileLR(s)
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closeFileReads()
    updateOutput()

# uppercaes all instances of a certain letter such as 'a' (Ask the tAll mAn)
def onlyXUp(letter):
    getWriteLocation()
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
                writeFileLR(j.replace(letter, uppercaseletter))
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closeFileReads()
    updateOutput()

# lowercasses all instances of a certain letter such as 'a' (aSK THE TaLL MaN)
def onlyXLow(letter):
    getWriteLocation()
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
                writeFileLR(j.replace(letter, lowercaseletter))
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closeFileReads()
    updateOutput()

# the gui for all insert tasks
def insertGui():
    guiInsert = Toplevel()
    guiInsert.title("Insert")
    guiInsert.geometry("420x120")
    guiInsert.resizable(0, 0)

    Label(guiInsert, text="to insert").grid(column=0, row=0, sticky=W)
    Label(guiInsert, text="step/loc").grid(column=1, row=0, sticky=W)

    textentryinsert = Entry(guiInsert, width=10, bg="grey")
    textentryinsert.grid(row=1, column=0, sticky=W)
    textentryinsertnum = Entry(guiInsert, width=10, bg="grey")
    textentryinsertnum.grid(row=1, column=1, sticky=W)

    Button(guiInsert, text="front", width=7, command=lambda: insertFront(textentryinsert.get())).grid(row=2, column=0,
                                                                                                      sticky=W)
    Button(guiInsert, text="end", width=7, command=lambda: insertEnd(textentryinsert.get())).grid(row=3, column=0,
                                                                                                  sticky=W)
    Button(guiInsert, text="insertAtX", width=7,
           command=lambda: insertAtX(textentryinsert.get(), textentryinsertnum.get())).grid(row=2, column=1, sticky=W)
    Button(guiInsert, text="insertStep", width=7,
           command=lambda: insertStep(textentryinsert.get(), textentryinsertnum.get())).grid(row=3, column=1, sticky=W)

# inserts the character or string given in the front of each line (left to right)
def insertFront(toinsert):
    getWriteLocation()
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
                writeFileLR(toinsert + j)
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closeFileReads()
    updateOutput()

# inserts the character or string given in the back of each line (right to left)
def insertEnd(toinsert):
    getWriteLocation()
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
                writeFileLR(j + toinsert + '\n')
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closeFileReads()
    updateOutput()

# inserts a character or string at a certain index of a string. NOTE if the string length is shorter than the string nothing is inserted.
def insertAtX(toinsert, location):
    getWriteLocation()
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
                writeFileLR(j[0:int(location)] + toinsert +j[int(location):len(j)])
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closeFileReads()
    updateOutput()

# inserts a character or string on a step such as dog ever 2 (I doglodogvedog tdogo dogwadoglk) from (I love to talk)
def insertStep(toinsert, step):
    getWriteLocation()
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
                writeFileLR(toinsert.join(j[i:i + int(step)] for i in range(0, len(j), int(step))))
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closeFileReads()
    updateOutput()

# the gui for all analyze tasks
def analyzeGui():
    guiAnalyze = Toplevel()
    guiAnalyze.title("Analyze")
    guiAnalyze.geometry("420x100")

    Label(guiAnalyze, text="placehold").grid(column=0, row=0, sticky=W)
    Label(guiAnalyze, text="placehold").grid(column=1, row=0, sticky=W)

    textentryanalyze = Entry(guiAnalyze, width=10, bg="grey")
    textentryanalyze.grid(row=1, column=0, sticky=W)
    textentryanalyzenum = Entry(guiAnalyze, width=10, bg="grey")
    textentryanalyzenum.grid(row=1, column=1, sticky=W)

    Button(guiAnalyze, text="Frequency", width=7, command=lambda: frequency()).grid(row=2, column=0, sticky=W)

# lists the frequency of all characters in a file. (such as a = 8 meaning 8 lowercase letter a's are in the entire file)
def frequency():
    getWriteLocation()
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
        writeFileLR(charList[i] + " = " + str(charNumList[i]))

    closeFileReads()
    updateOutput()

# the help button triggers the systems text editor to open the help.txt which contains the manual
def help(): #needs windows (operating system) support
    fileName = "help.txt"
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, fileName])

'''
# gui for replace
def replaceGui():
    guiReplace = Toplevel()
    guiReplace.title("Replace")
    guiReplace.geometry("420x120")
    guiReplace.resizable(0, 0)

    Label(guiReplace, text="find").grid(column=0, row=0, sticky=W)
    Label(guiReplace, text="replace").grid(column=1, row=0, sticky=W)

    textEntryFind = Entry(guiReplace, width=10, bg="grey")
    textEntryFind.grid(row=1, column=0, sticky=W)
    textEntryReplace = Entry(guiReplace, width=10, bg="grey")
    textEntryReplace.grid(row=1, column=1, sticky=W)

    Button(guiReplace, text="Replace", width=7, command=lambda: replaceAll(textEntryFind.get(), textEntryReplace.get())).grid(row=2, column=0, sticky=W)
    #Button(guiReplace, text="ReplaceOL", width=7, command=lambda: replaceOL(textEntryFind.get(), textEntryReplace.get())).grid(row=2, column=0, sticky=W)

# Replace all occurances of a string with a given string
def replaceAll(find, replace):
    getWriteLocation()
    fileCount = 0
    print("here")

    for i in locationoffiles:
        print("here1")
        progressReadLines()
        gui.update()
        numOfLines = getLineCount(i)
        updateInterval = getUpdateInterval(numOfLines)
        curLineNum = 0
        fileCount += 1
        fp = open(i, mode='r', encoding='utf8', errors='replace')
        if (numOfLines > 0 and updateInterval > 0):
            print("here2")
            for j in fp:
                print(j)
                writeFileLR(j.replace(find, replace))
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closeFileReads()
    updateOutput()

def replaceAll(find, replace):
    getWriteLocation()
    fileCount = 0
    print("here")

    for i in locationoffiles:
        print("here1")
        progressReadLines()
        gui.update()
        numOfLines = getLineCount(i)
        updateInterval = getUpdateInterval(numOfLines)
        curLineNum = 0
        fileCount += 1
        fp = open(i, mode='r', encoding='utf8', errors='replace')
        if (numOfLines > 0 and updateInterval > 0):
            print("here2")
            for j in fp:
                print(j)
                writeFileLR(j.replace(find, replace))
                curLineNum += 1
                if curLineNum % updateInterval == 0:
                    updateProgress(fileCount, curLineNum, numOfLines)
                    gui.update()
            fp.close()

    closeFileReads()
    updateOutput()
'''
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
output.grid(row=0, column=1, columnspan=16, sticky=W)

# button for trimming
Button(gui, text="Trim", width=7, command=trimGui).grid(row=2, column=0, sticky=W)

# button for removal
Button(gui, text="Removal", width=7, command=removalGui).grid(row=3, column=0, sticky=W)

# button for changing cases
Button(gui, text="Cases", width=7, command=casesGui).grid(row=1, column=1, sticky=W)

# button for inserting

Button(gui, text="Insert", width=7, command=insertGui).grid(row=2, column=1, sticky=W)

# button to quit the appilcation and all other windows
Button(gui, text="Quit", width=7, command=quitApp).grid(row=4, column=0, sticky=W)

# button for the analyzation of files
Button(gui, text="Analyze", width=7, command=analyzeGui).grid(row=3, column=1, sticky=W)

# button for replacing a string with a different string
#Button(gui, text="Replace", width=7, command=replaceGui).grid(row=1, column=2, sticky=W)

# button for help
Button(gui, text="Help", width=7, command=help).grid(row=4, column=1, sticky=W)

# progress output
progressOP = Text(gui, width=30)
progressOP.grid(row=5, column=16, sticky=W)
progressOP.insert(END, "progress")


gui.mainloop()
