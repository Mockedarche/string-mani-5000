# string-mani-5000
A simple tkinter gui for manipulating large sets of single line strings (in various file formats)

next version will include a progress indicator of some kind. 

Hello I am mockedarche the creator of this simple program. The goal of this program is to replace a different piece of software that I used to use. This other program had far more features but the ones I commonly used are added to this. 

NOTE: This is still very very early in the days of this program but I don't know how much more will be added. If this gets decent traction ill probably keep working on it as its been a great learning experience. I know Java and a smidge of c but after taking a year leave from college decided to teach myself python. I don't have any formal training in python and currently learned almost everything I know within a week of real learning. Meaning this program will be rough and have plenty of bugs. Bugs will be worked on and fixed just as new features (or potential rewrites of old ones). FEEL FREE TO REACH OUT IF YOU HAVE ANY TROUBLE OR NEED/WANT A NEW OR DIFFERENT FEATURES!

Why the cat/catcoon picture? Needed some kind of moniker. It adds a charm and don't plan to remove it unless it causes more hassle than its worth. 

HELP!!!!!
Now into the meat and potatoes

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