package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"unicode"
)

/*
Expected formatting

./string_mani file/path_to_input_file [options indicator 1] [options input]

all options follow along with descriptions of their options and expected syntax

-out output file
    has one argument
    expects a valid file name and extension
-t trim command
    has four arguments
    first is the seperator character
    second is either -a or -b indicating if it should take everything BEFORE or AFTER the seperator
    third is either -e or -i indicating if the seperator should be INCLUDED in the new string or EXCLUDED
    fourth is either -i or -d indicating if strings which DONT have the seperator should be included in the output or discarded

    Example input
    test:bird

    Example command
    ./string_mani EXAMPLE_FILE -t : -a -e -i

    Result output
    bird

-r removal command
	has three arguments
	first argument is just the character or string to remove
	second argument is either -a -l -f indicating if all occurrences should be removed, the last occurrence, or the first occurrence.
	third argument is either -i or -d indicating if strings without the substring should be included or discarded

-c cases command
	has one argument
	the only argument is either -u or -l indicating if the string should be made uppercase or lowercase

*/

// Declare our dictionary holding the commands
var commandBook map[string]string

// Declare our function type (function as variable for code reuse and standardization)
type command func(string) string

/*
isFile - exits if the file read failed or encountered some error (ultimately a CLI shouldn't try and run if an error occurs instead it should CLEANLY exit)
return true if path is pointing to a file AND FALSE if path is pointing to a folder
*/
func isFile(path string) bool {
	info, err := os.Stat(path)

	// if its not null then its an error indicating that the path doesnt' exist
	if err != nil {
		fmt.Println("Error occured reading file most likely indicating file doesn't exist (path invalid)")
		os.Exit(1)
	}

	if info.IsDir() {
		commandBook["InputName"] = path
		return false
	} else {
		commandBook["InputName"] = path
		return true
	}

}

func isDigitOnly(s string) bool {
	for _, c := range s {
		if !unicode.IsDigit(c) {
			return false
		}
	}
	return true
}

/*
validateArguments - takes in the arguments finds the desired command and validates that all the correct arguments for that given command are given being MINDFUL that of potential lack of arguments. Once its validated that the arguments exist it adds it to the commandBook and returns true indicating success. If any step fails it returns false indicating incorrect arguments were passed
*/
func validateArguments(arguments []string) bool {
	if len(arguments) >= 2 {
		switch arguments[1] {
		case "-t":
			if len(arguments) >= 6 {
				if arguments[3] == "-a" || arguments[3] == "-b" {
					if arguments[4] == "-e" || arguments[4] == "-i" {
						if arguments[5] == "-i" || arguments[5] == "-d" {
							commandBook["command"] = "trim"
							commandBook["arguments"] = fmt.Sprintf("%s %s %s %s", arguments[2], arguments[3], arguments[4], arguments[5])
							return true
						}
					}
				}
			}
			return false
		case "-r":
			if len(arguments) >= 5 {
				if arguments[3] == "-a" || arguments[3] == "-l" || arguments[3] == "-f" {
					if arguments[4] == "-i" || arguments[4] == "-d" {
						commandBook["command"] = "removal"
						commandBook["arguments"] = fmt.Sprintf("%s %s $s", arguments[2], arguments[3], arguments[4])
						return true
					}
				}
			}

		case "-c":
			if len(arguments) >= 3 {
				if arguments[2] == "-u" || arguments[2] == "-l" {
					commandBook["command"] = "cases"
					commandBook["arguments"] = fmt.Sprintf("%s", arguments[2])
					return true
				}
			}

		case "-s":
			if len(arguments) >= 3 {
				if arguments[2] == "-u" || arguments[2] == "-l" {
					if isDigitOnly(arguments[3]) {
						commandBook["command"] = "step"
						commandBook["arguments"] = fmt.Sprintf("%s %s", arguments[2], arguments[3])
						return true
					}
				}
			}
		case "-i":
			if len(arguments) >= 4 {
				if arguments[2] == "-f" || arguments[2] == "-e" || isDigitOnly(arguments[2]) {
					commandBook["command"] = "insert"
					commandBook["arguments"] = fmt.Sprintf("%s %s", arguments[2], arguments[3])
					return true
				}
			}

		default:
			fmt.Println("Arguments are invalid exiting")
			os.Exit(1)

		}
	}
	return false

}

/*
trim - simply takes a string and performs the desired trim operation on the string using the commandBook and returns the trimed string. Doesn't handle incorrect arguments (Note if any arguments are incorrect it indicates an issue elsewhere such as validateArguments)
Note should have 4 arguments
first is the seperator
second -a or -b indicating if we take before or after seperator
third -e or -i indicating if we take the seperator
fourth -i or -d indicating if we include or discard lines which don't contain the seperator
*/
func trim(line string) string {
	// trim the string according to the commands
	arguments := strings.Split(commandBook["arguments"], " ")
	var newLine string

	if len(arguments) != 4 {
		fmt.Println("Incorrect amount of arguments passed to function trim EXITING")
		os.Exit(1)
	}

	parts := strings.Split(line, arguments[0])
	//DEBUG STATEMENT
	//fmt.Println(len(parts))
	if len(parts) > 1 {
		if arguments[1] == "-a" {
			newLine = parts[1]
			if arguments[2] == "-i" {
				newLine = arguments[0] + newLine
			}
		} else {
			newLine = parts[0]
			if arguments[2] == "-i" {
				newLine += arguments[0]
			}
		}
	} else {
		if arguments[3] == "-i" {
			return line
		} else {
			return ""
		}
	}
	return newLine
}

/*
removal - Takes a string and removes the substring or character as denoted by the user
has three arguments
first argument is just the character or string to remove
second argument is either -a -l -f indicating if all occurrences should be removed, the last occurrence, or the first occurrence.
third argument is either -i or -d indicating if strings without the substring should be included or discarded
*/
func removal(line string) string {

	arguments := strings.Split(commandBook["arguments"], " ")
	var newLine string

	if arguments[1] == "-a" {
		newLine = strings.ReplaceAll(line, arguments[0], "")
	} else if arguments[1] == "-f" {
		newLine = strings.Replace(line, arguments[0], "", 1)
	} else {
		newLine = line
		index := strings.LastIndex(line, arguments[0])
		if index != -1 {
			newLine = line[:index] + strings.Replace(newLine[index:], arguments[0], "", 1)
		}

	}

	if arguments[2] == "-i" {
		return newLine
	} else {
		if newLine != line {
			return newLine
		} else {
			return ""
		}
	}

}

func cases(line string) string {
	var newLine string

	if commandBook["arguments"] == "-u" {
		newLine = strings.ToUpper(line)
	} else {
		newLine = strings.ToLower(line)
	}

	return newLine

}

func step(line string) string {
	newLine := make([]rune, len(line))
	arguments := strings.Split(commandBook["arguments"], " ")
	step, err := strconv.Atoi(arguments[1])
	if err != nil {
		fmt.Println("Issue converting the step number into a integer INTERNAL error: ", err)
		os.Exit(1)
	}

	step += 1
	count := 0

	for i, c := range line {
		count++
		if count == step {
			count = 0
			if arguments[0] == "-u" {
				newLine[i] = unicode.ToUpper(c)
			} else {
				newLine[i] = unicode.ToLower(c)
			}
		} else {
			newLine[i] = c
		}

	}
	line = string(newLine)

	return line
}

func insert(line string) string {
	var newLine string

	arguments := strings.Split(commandBook["arguments"], " ")

	if arguments[0] == "-f" {
		newLine = arguments[1] + line
	} else if arguments[0] == "-e" {
		newLine = line + arguments[1]
	} else {
		index, err := strconv.Atoi(arguments[0])
		if err != nil {
			fmt.Println("An error occured in converting the index for insert to a number: ", err)
		}
		if len(line) >= index {
			newLine = line[:index] + arguments[1] + line[index:]
		}
	}

	return newLine

}

func updateProgressBar(progress, total int64) {
	barLength := 50
	filledLength := int(float64(barLength) * float64(progress) / float64(total))
	bar := ""
	for i := 0; i < filledLength; i++ {
		bar += "="
	}
	for i := filledLength; i < barLength; i++ {
		bar += "-"
	}
	percentage := float64(progress) / float64(total) * 100
	fmt.Printf("\r\033[K[%s] %.1f%%", bar, percentage)
	if progress == total {
		fmt.Println()
	}
}

/*
readProcessWriteStrings - main loop simply checks out inputFile, outputFile, and then goes through eachline performing the desired command
*/
func readProcessWriteStrings(args []string) {

	var f command = trim

	// setup the input file
	inputFile, err := os.Open(args[0])
	if err != nil {
		fmt.Println("Error opening file: ", err)
		os.Exit(1)
	}
	defer inputFile.Close()

	// get the files size so we can determine progress on the file
	inputFileDescriptor, fileError := os.Stat(args[0])
	if fileError != nil {
		fmt.Println("Error seeing file stats: ", fileError)
		os.Exit(1)
	}
	var inputFileSize = inputFileDescriptor.Size()

	// assign the command function to variable
	switch commandBook["command"] {
	case "trim":
		f = trim
	case "removal":
		f = removal
	case "cases":
		f = cases
	case "step":
		f = step
	case "insert":
		f = insert
	default:
		fmt.Println("An error occured in the switch statement for command selection exiting")
		return
	}

	// set up our output file using either user specified or the default of out.txt
	var outputFile *os.File
	if commandBook["outputFileName"] == "temp" {
		if commandBook["appendOrErase"] == "append" {
			outputFile, err = os.OpenFile("out.txt", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		} else {
			outputFile, err = os.OpenFile("out.txt", os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0644)
		}
		if err != nil {
			fmt.Println("error setting up output file error: ", err)
			return
		}
	} else {
		if commandBook["appendOrErase"] == "append" {
			outputFile, err = os.OpenFile(commandBook["outputFileName"], os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		} else {
			outputFile, err = os.OpenFile(commandBook["outputFileName"], os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0644)
		}
		if err != nil {
			fmt.Println("error setting up output file error: ", err)
			return
		}
	}
	defer outputFile.Close()

	// setup our buffered reader for the inputFile so we can begin to process the file
	scanner := bufio.NewScanner(inputFile)
	var currentProgressStep int64

	// create a temp variable to hold the read in string and a byte counter for our progress bar
	var currentLine string
	var byteCounter int64
	for scanner.Scan() {
		// read in the next line
		currentLine = scanner.Text()
		// determine how many bytes were processing and add that to our counter for progress
		byteCounter += int64(len(scanner.Bytes()))
		currentLine = f(currentLine)
		if len(currentLine) != 0 {
			// DEBUG STATEMENT
			//fmt.Println(currentLine)
			outputFile.WriteString(currentLine + "\n")
		}

		if (int64((float64(byteCounter) / float64(inputFileSize)) * 100)) >= currentProgressStep {
			currentProgressStep++
			updateProgressBar(byteCounter, inputFileSize)
		}

	}
	if err := scanner.Err(); err != nil {
		fmt.Println("Some error occured while reading the file: ", err)
	}

}

func main() {
	// validate we have enough arguments
	if len(os.Args) < 2 {
		fmt.Println("not enough arguments given")
		os.Exit(1)
	}

	// init our command book
	commandBook = map[string]string{
		"command":        "temp",
		"fileOrFolder":   "temp",
		"arguments":      "temp",
		"inputName":      "temp",
		"outputFileName": "temp",
		"noCheck":        "false",
		"debug":          "false",
		"appendOrErase":  "erase",
	}
	// remove script name from arguments
	args := os.Args[1:]

	for i, arg := range args {
		switch arg {
		case "-debug":
			commandBook["debug"] = "true"

		case "-out":
			commandBook["outputFileName"] = args[i+1]

		case "-append":
			commandBook["appendOrErase"] = "append"
		}
	}

	if commandBook["debug"] == "true" {
		// DEBUG print our arguments
		for i, arg := range args {
			fmt.Printf("Argument #%d is %s\n", i, arg)
		}
	}

	// Set if we're working with a file or folder
	if isFile(args[0]) {
		commandBook["fileOrFolder"] = "File"
	} else {
		commandBook["fileOrFolder"] = "Folder"
	}
	// DEBUG STATEMENT
	//fmt.Println(commandBook["fileOrFolder"])

	if !validateArguments(args) {
		fmt.Println("An error occured in validating your arguments. Please type -help for guidence on arguments")
		os.Exit(1)
	}
	readProcessWriteStrings(args)

}
