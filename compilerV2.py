                                                #===============================================================================#
                                                #                   Pontificia Universidad Javeriana, Cali                      #
                                                #                           Facultad de Ingeniería                              #
                                                #                    Ingeniería de Sistemas y Computación                       #
                                                #                       Arquitectura del Computador II                          #
                                                #                               Antonio Yu Chen                                 #
                                                #===============================================================================#

import re
from tkinter import *

# R0 will be the base address. It will point to the start of the data memory. It starts at the position 0.
# The memory address which points to the arrays will be 100. Each array has a size of 100.
# counterList: first position corresponds to else counter, second to while counter, third to endWhile counter,
#              fourth to doWhile counter, fifth to doEnd counter.
# Split the algorithm that was written into the input text box and stores it in an array to start compiling the program.

# Initialization of window with widgets #
root = Tk()
root.title("Compilador a Von Neumann")
root.geometry("800x700")
inputText = Text(width = 35)
inputText.place(x = 35, y = 80)
outputText = Text(width = 35)
outputText.place(x = 485, y = 80)
inputLabel = Label(text = "Algoritmo en alto nivel", font = ("Inconsolata", 12))
inputLabel.place(x = 90, y = 50)
outputLabel = Label(text = "Algoritmo en Von Neumann", font = ("Inconsolata", 12))
outputLabel.place(x = 530, y = 50)
periodText = Text(height = 1, width = 10)
periodText.place(x = 35, y = 525)
periodLabel = Label(text = "Periodo de reloj", font = ("Inconsolata", 12))
periodLabel.place(x = 32, y = 500)
frequencyText = Text(height = 1, width = 10)
frequencyText.place(x = 35, y = 580)
frequencyLabel = Label(text = "Frecuencia de reloj", font = ("Inconsolata", 12))
frequencyLabel.place(x = 32, y = 555)
execText = Text(height = 1, width = 25)
execText.place(x = 483, y = 525)
execLabel = Label(text = "Tiempo de ejecucion", font = ("Inconsolata", 12))
execLabel.place(x = 480, y = 500)
outputText.config(state = DISABLED)
periodText.config(state = DISABLED)
frequencyText.config(state = DISABLED)
execText.config(state = DISABLED)
# Initialization of variables #
registerList = []
counterList = [0, 0, 0, 0, 0]
balancedList = []
frequency = 0
period = 0

def operations(line, cycles):
	"""Function that receives a line of code and applies the appropiate instruction in Von Neumann."""
	if(re.match("^\s*([A-z]+[0-9]*)\s*=\s*([A-z]+[0-9]*|[0-9]+)(\s*([-|+|*|/])\s*([A-z]+[0-9]*|[0-9]+))*;\s*$", line)):
		outputText.config(state = NORMAL)
		instruction = re.match("^\s*([A-z]+[0-9]*)\s*=\s*([A-z]+[0-9]*|[0-9]+)(\s*([-|+|*|/])\s*([A-z]+[0-9]*|[0-9]+))*;$", line)
		if(instruction.group(3) != None):
			temporal = re.sub("\s*", "", line)
			operator = re.split("[A-z]+[0-9]*|[0-9]+", temporal)
			operand = re.split("[-|=|+|*|/]", temporal)
			operator.pop(len(operator) - 1)
			operator.pop(0)
			operator.pop(0)
			counter = 3
			index = 0
			while(operator != []):
				if("*" in operator or "/" in operator):
					if(operator[index] == "*" or operator[index] == "/"):
						if(operand[index + 1] in registerList):
							outputText.insert(END, "    MOV R1, [R0 + {}]\n".format(registerList.index(operand[index + 1])))
							cycles = cycles + 0
						else:
							outputText.insert(END, "    MOV R1, {}\n".format(operand[index + 1]))
							cycles = cycles + 0
						if(operand[index + 2] in registerList):
							outputText.insert(END, "    MOV R2, [R0 + {}]\n".format(registerList.index(operand[index + 2])))
							cycles = cycles + 0
						else:
							outputText.insert(END, "    MOV R2, {}\n".format(operand[index + 2]))
							cycles = cycles + 0
						if(operator[index] == "*"):
							outputText.insert(END, "    MUL R1, R2\n")
						else:
							outputText.insert(END, "    DIV R1, R2\n")
						outputText.insert(END, "    MOV R{}, R1\n".format(counter))
						cycles = cycles + 0
						operator.pop(index)
						operand.pop(index + 1)
						operand.pop(index + 1)
						operand.insert(index + 1, "R{}".format(counter))
						index = 0
						counter = counter + 1
						continue
					index = index + 1
				else:
					if(operator[index] == "+" or operator[index] == "-"):
						if(operand[index + 1] in registerList):
							outputText.insert(END, "    MOV R1, [R0 + {}]\n".format(registerList.index(operand[index + 1])))
							cycles = cycles + 0
						else:
							outputText.insert(END, "    MOV R1, {}\n".format(operand[index + 1]))
							cycles = cycles + 0
						if(operand[index + 2] in registerList):
							outputText.insert(END, "    MOV R2, [R0 + {}]\n".format(registerList.index(operand[index + 2])))
							cycles = cycles + 0
						else:
							outputText.insert(END, "    MOV R2, {}\n".format(operand[index + 2]))
							cycles = cycles + 0
						if(operator[index] == "+"):
							outputText.insert(END, "    ADD R1, R2\n")
						else:
							outputText.insert(END, "    SUB R1, R2\n")
						outputText.insert(END, "    MOV R{}, R1\n".format(counter))
						cycles = cycles + 0
						operator.pop(index)
						operand.pop(index + 1)
						operand.pop(index + 1)
						operand.insert(index + 1, "R{}".format(counter))
						index = 0
						counter = counter + 1
						continue
					index = index + 1
			outputText.insert(END, "    MOV [R0 + {}], R{}\n\n".format(registerList.index(operand[0]), counter - 1))
			cycles = cycles + 0
		else:
			register1 = instruction.group(1)
			register2 = instruction.group(2)
			if(register2 in registerList):
				outputText.insert(END, "    MOV R1, [R0 + {}]\n".format(registerList.index(register2)))
				cycles = cycles + 0
			else:
				outputText.insert(END, "    MOV R1, {}\n".format(register2))
				cycles = cycles + 0
			outputText.insert(END, "    MOV [R0 + {}], R1\n\n".format(registerList.index(register1)))
			cycles = cycles + 0
		outputText.config(state = DISABLED)
	return cycles

def forInstruction(algorithm, cycles):
	alphanumeric = "\s*([A-z]+[0-9]*|[0-9]+)\s*"
	operations = "\s*([A-z]+[0-9]*)\s*=\s*([A-z]+[0-9]*|[0-9]+)(\s*([-|+|*|/])\s*([A-z]+[0-9]*|[0-9]+))*\s*"
	forExpression = "^\s*for[(]\s*([A-z]+[0-9]*)\s*="
	expression = forExpression + alphanumeric + ";" + alphanumeric + "(<|>|!=|==)" + alphanumeric + ";" + operations + "[)]\s*{\s*$"
	if(re.match(expression, algorithm[0])):


def matching(char1, char2):
	if(char1 == "(" and char2 == ")"):
		return 1
	elif(char1 == "[" and char2 == "]"):
		return 1
	elif(char1 == "{" and char2 == "}"):
		return 1
	else:
		return 0

def balanced(line):
	for char in line:
		if(char == "{" or char == "(" or char == "["):
			balancedList.append(char)
		elif(char == "}" or char == ")" or char == "]"):
			if(len(balancedList) == 0):
				bracketFlag = 0
				outputText.insert(END, "SyntaxError: missing parentheses.\n")
				return bracketFlag
			elif(matching(balancedList.pop(0), char) == 0):
				bracketFlag = 0
	if(len(balancedList) == 0):
		bracketFlag = 1
	else:
		bracketFlag = 0
	return bracketFlag

def validAlgorithm(algorithm):
	tmpAlgorithm = algorithm
	init = "^\s*(int)\s*([A-z]+[0-9]*);\s*$"
	ifWhile = "^\s*(if|while)[(]\s*([A-z]+[0-9]*|[0-9]+)\s*(<|>|!=|==)\s*([A-z]+[0-9]*|[0-9]+)\s*[)]\s*{\s*$"
	operations = "^\s*([A-z]+[0-9]*)\s*=\s*([A-z]+[0-9]*|[0-9]+)(\s*([-|+|*|/])\s*([A-z]+[0-9]*|[0-9]+))*;\s*$"
	doExp = "^\s*do\s*{\s*$"
	doWhileExp = "^\s*}\s*while[(]\s*(	|[0-9]+)\s*(<|>|!=|==)\s*([A-z]+[0-9]*|[0-9]+)\s*[)];\s*$"
	closingBracket = "^\s*}$"
	spaces = "^\s*$"
	alphanumeric = "\s*([A-z]+[0-9]*|[0-9]+)\s*"
	forOp = "\s*([A-z]+[0-9]*)\s*=\s*([A-z]+[0-9]*|[0-9]+)(\s*([-|+|*|/])\s*([A-z]+[0-9]*|[0-9]+))*\s*"
	forExpression = "^\s*for[(]\s*([A-z]+[0-9]*)\s*="
	expression = forExpression + alphanumeric + ";" + alphanumeric + "(<|>|!=|==)" + alphanumeric + ";" + forOp + "[)]\s*{\s*$"
	flag = 0
	bracketFlag = 1
	lineNumber = 1
	doFlag = 1
	doWhileFlag = 1
	syntaxFlag = 0
	outputText.config(state = NORMAL)
	while(tmpAlgorithm != []):
		if(re.match(init, tmpAlgorithm[0])):
			flag = 1
			instruction = re.match(init, tmpAlgorithm[0])
			register = instruction.group(2)
			if(register not in registerList):
				registerList.append(register)
		elif(re.match(operations, tmpAlgorithm[0])):
			flag = 1
			instruction = re.match(operations, tmpAlgorithm[0])
			if(instruction.group(3) != None):
				temporal = re.sub("\s*", "", tmpAlgorithm[0])
				operand = re.split("[-|=|+|*|/]", temporal)
				for register in operand:
					if(register.isdigit() == 0 and register not in registerList):
						flag = 0
						outputText.insert(END, "SyntaxError at line {}: {} has not been declared.\n\n".format(lineNumber, register))
			else:
				register1 = instruction.group(1)
				register2 = instruction.group(2)
				if(register1 not in registerList):
					flag = 0
					outputText.insert(END, "SyntaxError at line {}: {} has not been declared.\n\n".format(lineNumber, register1))
				if(register2.isdigit() == 0 and register2 not in registerList):
					flag = 0
					outputText.insert(END, "SyntaxError at line {}: {} has not been declared.\n\n".format(lineNumber, register2))
		elif(re.match(ifWhile, tmpAlgorithm[0])):
			flag = 1
			instruction = re.match(ifWhile, tmpAlgorithm[0])
			register1 = instruction.group(2)
			register2 = instruction.group(4)
			if(register1.isdigit() == 0 and register1 not in registerList):
				flag = 0
				outputText.insert(END, "SyntaxError at line {}: {} has not been declared.\n\n".format(lineNumber, register1))
			if(register2.isdigit() == 0 and register2 not in registerList):
				flag = 0
				outputText.insert(END, "SyntaxError at line {}: {} has not been declared.\n\n".format(lineNumber, register2))
			bracketFlag = balanced(tmpAlgorithm[0])
		elif(re.match(closingBracket, tmpAlgorithm[0])):
			flag = 1
			bracketFlag = balanced(tmpAlgorithm[0])
		elif(re.match(doWhileExp, tmpAlgorithm[0])):
			flag = 1
			instruction = re.match(doWhileExp, tmpAlgorithm[0])
			register1 = instruction.group(1)
			register2 = instruction.group(3)
			if(register1.isdigit() == 0 and register1 not in registerList):
				flag = 0
				outputText.insert(END, "SyntaxError at line {}: {} has not been declared.\n\n".format(lineNumber, register1))
			if(register2.isdigit() == 0 and register2 not in registerList):
				flag = 0
				outputText.insert(END, "SyntaxError at line {}: {} has not been declared.\n\n".format(lineNumber, register2))
			bracketFlag = balanced(tmpAlgorithm[0])
			if(doWhileFlag == 0):
				doWhileFlag = 1
			else:
				doFlag = 0
		elif(re.match(doExp, tmpAlgorithm[0])):
			flag = 1
			bracketFlag = balanced(tmpAlgorithm[0])
			doWhileFlag = 0
		elif(re.match(spaces, tmpAlgorithm[0])):
			flag = 1
		else:
			syntaxFlag = 1
			outputText.insert(END, "SyntaxError at line {}: invalid syntax.\n".format(lineNumber))
		lineNumber = lineNumber + 1
		tmpAlgorithm.pop(0)
	if(bracketFlag == 0):
		flag = 0
		outputText.insert(END, "SyntaxError: missing parentheses.\n")
	if(doFlag == 0 or doWhileFlag == 0):
		flag = 0
		outputText.insert(END, "SyntaxError: missing do or while expression.")
	if(syntaxFlag == 1):
		flag = 0
	return flag

def doWhile(algorithm, cycles):
	if(re.match("^\s*do\s*{\s*$", algorithm[0])):
		outputText.config(state = NORMAL)
		currentDo = counterList[3]
		currentDoEnd = counterList[4]
		outputText.insert(END, "DO{}:\n".format(currentDo))
		counterList[3] = counterList[3] + 1
		counterList[4] = counterList[4] + 1
		algorithm.pop(0)
		while(re.match("^\s*}\s*while[(]\s*([A-z]+[0-9]*|[0-9]+)\s*(<|>|!=|==)\s*([A-z]+[0-9]*|[0-9]+)\s*[)];\s*", algorithm[0]) == None):
			cycles = branchWhile(algorithm, cycles)
			cycles = operations(algorithm[0], cycles)
			cycles = doWhile(algorithm, cycles)
			algorithm.pop(0)
		instruction = re.match("^\s*}\s*while[(]\s*([A-z]+[0-9]*|[0-9]+)\s*(<|>|!=|==)\s*([A-z]+[0-9]*|[0-9]+)\s*[)];\s*$", algorithm[0])
		register1 = instruction.group(1)
		operator = instruction.group(2)
		register2 = instruction.group(3) 
		outputText.config(state = NORMAL)
		if(register1 in registerList):
			outputText.insert(END, "    MOV R1, [R0 + {}]\n".format(registerList.index(register1)))
			cycles = cycles + 0
		else:
			outputText.insert(END, "    MOV R1, {}\n".format(register1))
			cycles = cycles + 0
		if(register2 in registerList):
			outputText.insert(END, "    MOV R2, [R0 + {}]\n".format(registerList.index(register2)))
			cycles = cycles + 0
		else:
			outputText.insert(END, "    MOV R2, {}\n".format(register2))
			cycles = cycles + 0
		if(operator == "<"):
			outputText.insert(END, "    BRM R1, R2, DOEND{}\n".format(currentDoEnd))
			outputText.insert(END, "    BRI R1, R2, DOEND{}\n".format(currentDoEnd))
			cycles = cycles + 0
		elif(operator == ">"):
			outputText.insert(END, "    BRME R1, R2, DOEND{}\n".format(currentDoEnd))
			outputText.insert(END, "    BRI R1, R2, DOEND{}\n".format(currentDoEnd))
			cycles = cycles + 0
		elif(operator == "=="):
			outputText.insert(END, "    BRM R1, R2, DOEND{}\n".format(currentDoEnd))
			outputText.insert(END, "    BRME R1, R2, DOEND{}\n".format(currentDoEnd))
			cycles = cycles + 0
		elif(operator == "!="):
			outputText.insert(END, "    BRI R1, R2, DOEND{}\n".format(currentDoEnd))
			cycles = cycles + 0
		outputText.insert(END, "    JUMP DO{}\n\n".format(currentDo))
		cycles = cycles + 0
		outputText.insert(END, "DOEND{}:\n".format(currentDoEnd))
		outputText.config(state = DISABLED)
	return cycles

def branchWhile(algorithm, cycles):
	"""Function that receives an algorithm as parameter and the current cycles and applies if or while instructions."""
	if(re.match("^\s*(if|while)[(]\s*([A-z]+[0-9]*|[0-9]+)\s*(<|>|!=|==)\s*([A-z]+[0-9]*|[0-9]+)\s*[)]\s*{\s*$", algorithm[0])):
		outputText.config(state = NORMAL)
		instruction = re.match("^\s*(if|while)[(]\s*([A-z]+[0-9]*|[0-9]+)\s*(<|>|!=|==)\s*([A-z]+[0-9]*|[0-9]+)\s*[)]\s*{\s*$", algorithm[0])
		condition = instruction.group(1)
		register1 = instruction.group(2)
		operator = instruction.group(3)
		register2 = instruction.group(4)
		currentElse = counterList[0]
		currentWhile = counterList[1]
		currentEndWhile = counterList[2]
		markup = ""
		markupIndex = -1
		if(condition == "if"):
			markup = "ELSE"
			markupIndex = currentElse
			counterList[0] = counterList[0] + 1
			algorithm.pop(0)
		if(condition == "while"):
			markup = "ENDWHILE"
			markupIndex = currentEndWhile
			counterList[1] = counterList[1] + 1
			counterList[2] = counterList[2] + 1
			outputText.insert(END, "WHILE{}:\n".format(currentWhile))
			algorithm.pop(0)
		if(register1 in registerList):
			outputText.insert(END, "    MOV R1, [R0 + {}]\n".format(registerList.index(register1)))
			cycles = cycles + 0
		else:
			outputText.insert(END, "    MOV R1, {}\n".format(register1))
			cycles = cycles + 0
		if(register2 in registerList):
			outputText.insert(END, "    MOV R2, [R0 + {}]\n".format(registerList.index(register2)))
			cycles = cycles + 0
		else:
			outputText.insert(END, "    MOV R2, {}\n".format(register2))
			cycles = cycles + 0
		if(operator == "<"):
			outputText.insert(END, "    BRM R1, R2, {}{}\n".format(markup, markupIndex))
			outputText.insert(END, "    BRI R1, R2, {}{}\n".format(markup, markupIndex))
			cycles = cycles + 0
		elif(operator == ">"):
			outputText.insert(END, "    BRME R1, R2, {}{}\n".format(markup, markupIndex))
			outputText.insert(END, "    BRI R1, R2, {}{}\n".format(markup, markupIndex))
			cycles = cycles + 0
		elif(operator == "=="):
			outputText.insert(END, "    BRM R1, R2, {}{}\n".format(markup, markupIndex))
			outputText.insert(END, "    BRME R1, R2, {}{}\n".format(markup, markupIndex))
			cycles = cycles + 0
		elif(operator == "!="):
			outputText.insert(END, "    BRI R1, R2, {}{}\n".format(markup, markupIndex))
			cycles = cycles + 0
		while(re.match("^\s*}$", algorithm[0]) == None):
			cycles = branchWhile(algorithm, cycles)
			cycles = operations(algorithm[0], cycles)
			cycles = doWhile(algorithm, cycles)
			algorithm.pop(0)
		outputText.config(state = NORMAL)
		if(condition == "while"):
			outputText.delete("end-1c", END)
			outputText.insert(END, "    JUMP WHILE{}\n\n".format(currentWhile))
			cycles = cycles + 0
		outputText.insert(END, "{}{}:\n".format(markup, markupIndex))
		cycles = cycles + 0
		outputText.config(state = DISABLED)
	for i in counterList:
		counterList[i] = 0
	return cycles
	
def compiler(cycles):
	algorithm = (inputText.get("1.0", END)).split("\n")
	balancedList[:] = []
	if(validAlgorithm(algorithm)):
		outputText.config(state = NORMAL)
		outputText.insert(END, "    MOV R0, 0\n\n")
		outputText.config(state = DISABLED)
		while(algorithm != [] and cycles != 0):
			cycles = branchWhile(algorithm, cycles)
			cycles = operations(algorithm[0], cycles)
			cycles = doWhile(algorithm, cycles)
			algorithm.pop(0)
	return cycles

def translate():
	cycles = 1
	outputText.config(state = NORMAL)
	outputText.delete("1.0", END)
	outputText.config(state = DISABLED)
	registerList[:] = []
	if(inputText.get("1.0", END) != "\n"):
		cycles = compiler(cycles)
	outputFile = open("output.txt", "w")
	outputFile.write(outputText.get("1.0", "end-1c"))
	outputFile.close()
	#print(cycles)

def clear():
	"""Procedure that clears all the text boxes."""
	inputText.delete("1.0", END)
	outputText.config(state = NORMAL)
	outputText.delete("1.0", END)
	outputText.config(state = DISABLED)
	periodText.config(state = NORMAL)
	periodText.delete("1.0", END)
	periodText.config(state = DISABLED)
	frequencyText.config(state = NORMAL)
	frequencyText.delete("1.0", END)
	frequencyText.config(state = DISABLED)
	execText.config(state = NORMAL)
	execText.delete("1.0", END)
	execText.config(state = DISABLED)
	registerList = []
	for i in counterList:
		counterList[i] = 0

def period():
	"""Procedure that enables the periodText text box and clears the frequencyText text box."""
	frequencyText.config(state = NORMAL)
	frequencyText.delete("1.0", END)
	frequencyText.config(state = DISABLED)
	periodText.config(state = NORMAL)

def frequency():
	"""Procedure that enables the frequencyText text box and clears the frequencyText text box."""
	periodText.config(state = NORMAL)
	periodText.delete("1.0", END)
	periodText.config(state = DISABLED)
	frequencyText.config(state = NORMAL)

translateButton = Button(text = "Traducir", font = ("Inconsolata", 12), command = translate)
translateButton.place(x = 365, y = 250)
clearButton = Button(text = "Limpiar", font = ("Inconsolata", 12), command = clear)
clearButton.place(x = 365, y = 300)
periodButton = Button(text = "Periodo de reloj", font = ("Inconsolata", 9), command = period)
periodButton.place(x = 165, y = 500)
frequencyButton = Button(text = "Frecuencia de reloj", font = ("Inconsolata", 9), command = frequency)
frequencyButton.place(x = 180, y = 555)