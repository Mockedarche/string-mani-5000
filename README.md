# NOTE CURRENTLY ONLY THE GO-CLI IS SUPPORTED 

A gui wrapper for the cli is planned once the cli matures.


String-mani-5000 uses tkinter and tkinter was a great choice at the time but tkinter is slowly becomign deprecated and i've found various pythons tkinter behavior is different resulting in a rather bad user experience. Additionally atleast on macOS tkinter isn't coming included with the default python installation in a lot of sources thus the GUI to run whereever python is well isn't a realistic expectation anymore. Moving to CLI is currently underway with the goal to essentially replicate unified list manager (a great piece of software seemingly not being developed anymore) for once again all platforms that python is supported. A CLI will hurt the user experience but will remove any frameworks from causing another rewrite. Thanks for reading development on the CLI version is udnerway and when it reaches feature parity is denoted below

Feature parity Approx 5/10

# string-mani-5000
A simple tkinter gui for manipulating large sets of single line strings (in various file formats)

The goal of this program is to replace a different piece of software that I used to use. This other program had far more features but the ones I commonly used are added to this. 

Why the cat/catcoon picture? Needed some kind of moniker. It adds a charm and don't plan to remove it unless it causes more hassle than its worth. 

SELECT: Clicking this button should bring up a dialog box that allows you to select a file you want.  You can add as many files as you want. The giant box in the top center to right top shows all files selected. You can add more than what it can show (if some disappear they are still in queue just the box isn't big enough).

Trim: Trim works simply on a separator (a character or string that it then separates on). Just enter the character or string for your separator in the box and select what option you want.
take before: Takes everything EXCLUDING THE SEPARATOR before the separator.
Take after: Takes everything EXCLUDING THE SEPARATOR after the separator.

Removal: The first text box is the character or string you wish to remove. The second is only for options underneath it. In this case how many to remove. NOTE ITS CASE SENSITIVE.
Remove all: Remove all instances of the character or string in the entire file(s). 
First oc: Removes only the first occurrence of the character or string (left to right).
Last oc: Removes only the last occurrence of the character or string (right to left).

x first oc: Removes whatever amount of instances of the character or string (left to right).
x last oc: Removes whatever amount of instances of the character or string (right to left).

Cases: The first text box is the character or string you which to change to uppercase or lowercase. The second text box is only for the steps buttons and expects a digit.
Up all: Uppercases all the letters in the entire file(s).
Low all: Lowercases all the letters in the entire file(s).

Step up: Expects a digit in the second text box. It then uppercases whatever letter it finds following the step such a step of 1 would cause the line "become a cat" to turn to "bEcOmE A CaT".
Step low:Expects a digit in the second text box. It then lowercases whatever letter it finds following the step such a step of 1 would cause the line "BECOME A CAT" to turn to "bEcOmE a cAt".

Only x up: Expects a letter in the first text box. Uppercases all instances of that letter or string.
Only x low: Expects a letter in the first text box. Lowercases all instances of that letter or string.

Insert: First text box is whatever character or string you wish to insert. The second text box is only for for insertatX (the location in each line to insert) and insertstep (the step to follow).
Front: Inserts the first text boxes contents at the front of every line.
End: Inserts the first text boxes contents at the end of every line.

InsertatX: Inserts the first boxes contents at the location given in the seconds boxes given location. Such as if the first box has "hi". The seconds box had 3. The line "boxes rule" would turn to "boxhies rule.
Insertstep: Inserts the first boxes contents every step which is given in the second box. If the first boxes contents were "hi" and the second boxes contents were 3. The line "A long day in the sun" would turn to "A lhionghi dahiy ihin thihe hisun".

Newline: Expects a digit in the second box. Inserts a newline between lines based on a step. newline=blankline.

Analyze: Currently under heavy development! Both boxes don't do anything are placeholders. 
Frequency: Reads every character in a file and then outputs a new file with a count of each character. Supported characters are currently all letters, digits, and common symbols such as (separated by commas) @,!,#,$,%,^,&,*,(,),_,-,=,+,{,[,],},\,|,;,:,',",<,>,.,?,/, and of course the ,

Quit: Quits the entire program.

GIF
![](https://github.com/Mockedarche/string-mani-5000/blob/main/example.gif)
