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
counterList = [0, 0, 0] # First position corresponds to else counter, second to while counter and third to endWhile counter.
frequency = 0
period = 0

# Register = \s*([A-z]+[0-9]*)\s*=\s*
# Alphanumeric or numeric ([A-z]+[0-9]*|[0-9]+)

def operations(line, cycles):
	if(re.match("^\s*([A-z]+[0-9]*)\s*=\s*([A-z]+[0-9]*|[0-9]+)(\s*([-|+|*|/])\s*([A-z]+[0-9]*|[0-9]+))*$", line)):
		outputText.config(state = NORMAL)
		instruction = re.match("^\s*([A-z]+[0-9]*)\s*=\s*([A-z]+[0-9]*|[0-9]+)(\s*([-|+|*|/])\s*([A-z]+[0-9]*|[0-9]+))*$", line)
		if(instruction.group(3) != None):
			temporal = re.sub("\s*", "", line)
			operator = re.split("[A-z]+[0-9]*|[0-9]+", temporal)
			operand = re.split("[-|=|+|*|/]", temporal) # Search re.split function in regexp to improve
			operator.pop(len(operator) - 1)
			operator.pop(0)
			operator.pop(0)
			counter = 3
			index = 0
			while(operator != []):
				if("*" in operator or "/" in operator):
					if(operator[index] == "*" or operator[index] == "/"):
						if(operand[index + 1] in registerList):
							outputText.insert(END, "MOV R1, [R0 + {}]\n".format(registerList.index(operand[index + 1])))
							cycles = cycles + 0
						else:
							outputText.insert(END, "MOV R1, {}\n".format(operand[index + 1]))
							cycles = cycles + 0
						if(operand[index + 2] in registerList):
							outputText.insert(END, "MOV R2, [R0 + {}]\n".format(registerList.index(operand[index + 2])))
							cycles = cycles + 0
						else:
							outputText.insert(END, "MOV R2, {}\n".format(operand[index + 2]))
							cycles = cycles + 0
						if(operator[index] == "*"):
							outputText.insert(END, "MUL R1, R2\n")
						else:
							outputText.insert(END, "DIV R1, R2\n")
						outputText.insert(END, "MOV R{}, R1\n".format(counter))
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
							outputText.insert(END, "MOV R1, [R0 + {}]\n".format(registerList.index(operand[index + 1])))
							cycles = cycles + 0
						else:
							outputText.insert(END, "MOV R1, {}\n".format(operand[index + 1]))
							cycles = cycles + 0
						if(operand[index + 2] in registerList):
							outputText.insert(END, "MOV R2, [R0 + {}]\n".format(registerList.index(operand[index + 2])))
							cycles = cycles + 0
						else:
							outputText.insert(END, "MOV R2, {}\n".format(operand[index + 2]))
							cycles = cycles + 0
						if(operator[index] == "+"):
							outputText.insert(END, "ADD R1, R2\n")
						else:
							outputText.insert(END, "SUB R1, R2\n")
						outputText.insert(END, "MOV R{}, R1\n".format(counter))
						cycles = cycles + 0
						operator.pop(index)
						operand.pop(index + 1)
						operand.pop(index + 1)
						operand.insert(index + 1, "R{}".format(counter))
						index = 0
						counter = counter + 1
						continue
					index = index + 1
			outputText.insert(END, "MOV [R0 + {}], R{}\n".format(registerList.index(operand[0]), counter - 1))
			cycles = cycles + 0
		else:
			register1 = instruction.group(1)
			register2 = instruction.group(2)
			if(register2 in registerList):
				outputText.insert(END, "MOV R1, [R0 + {}]\n".format(registerList.index(register2)))
				cycles = cycles + 0
			else:
				outputText.insert(END, "MOV R1, {}\n".format(register2))
				cycles = cycles + 0
			outputText.insert(END, "MOV [R0 + {}], R1\n".format(registerList.index(register1)))
			cycles = cycles + 0
		outputText.config(state = DISABLED)
	return cycles

def validAlgorithm():
	algorithm = (inputText.get("1.0", "end-1c")).split("\n")
	init = "^\s*(int)\s*([A-z]+[0-9]*)$"
	ifWhile = "^\s*(if|while)[(]\s*([A-z]+[0-9]*|[0-9]+)\s*(<|>|!=|==)\s*([A-z]+[0-9]*|[0-9]+)\s*[)]\s*{$"
	operations = "^\s*([A-z]+[0-9]*)\s*=\s*([A-z]+[0-9]*|[0-9]+)(\s*([-|+|*|/])\s*([A-z]+[0-9]*|[0-9]+))*$"

def branchWhile(algorithm, cycles):
	if(re.match("^(if|while)[(]\s*([A-z]+[0-9]*|[0-9]+)\s*(<|>|!=|==)\s*([A-z]+[0-9]*|[0-9]+)\s*[)]\s*{$", algorithm[0])):
		outputText.config(state = NORMAL)
		instruction = re.match("^(if|while)[(]\s*([A-z]+[0-9]*|[0-9]+)\s*(<|>|!=|==)\s*([A-z]+[0-9]*|[0-9]+)\s*[)]\s*{$", algorithm[0])
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
			outputText.insert(END, "WHILE{}: ".format(currentWhile))
			algorithm.pop(0)
		if(register1 in registerList):
			outputText.insert(END, "MOV R1, [R0 + {}]\n".format(registerList.index(register1)))
			cycles = cycles + 0
		else:
			outputText.insert(END, "MOV R1, {}\n".format(register1))
			cycles = cycles + 0
		if(register2 in registerList):
			outputText.insert(END, "MOV R2, [R0 + {}]\n".format(registerList.index(register2)))
			cycles = cycles + 0
		else:
			outputText.insert(END, "MOV R2, {}\n".format(register2))
			cycles = cycles + 0
		if(operator == "<"):
			outputText.insert(END, "BRM R1, R2, {}{}\n".format(markup, markupIndex))
			outputText.insert(END, "BRI R1, R2, {}{}\n".format(markup, markupIndex))
			cycles = cycles + 0
		elif(operator == ">"):
			outputText.insert(END, "BRME R1, R2, {}{}\n".format(markup, markupIndex))
			outputText.insert(END, "BRI R1, R2, {}{}\n".format(markup, markupIndex))
			cycles = cycles + 0
		elif(operator == "=="):
			outputText.insert(END, "BRM R1, R2, {}{}\n".format(markup, markupIndex))
			outputText.insert(END, "BRME R1, R2, {}{}\n".format(markup, markupIndex))
			cycles = cycles + 0
		elif(operator == "!="):
			outputText.insert(END, "BRI R1, R2, {}{}\n".format(markup, markupIndex))
			cycles = cycles + 0
		while(algorithm[0] != "}"):
			cycles = branchWhile(algorithm, cycles)
			cycles = operations(algorithm[0], cycles)
			algorithm.pop(0)
		outputText.config(state = NORMAL)
		if(condition == "while"):
			outputText.insert(END, "JUMP WHILE{}\n".format(currentWhile))
		outputText.insert(END, "{}{}: ".format(markup, markupIndex))
		outputText.config(state = DISABLED)
	for i in counterList:
		counterList[i] = 0
	return cycles
	
def compiler(cycles):
	algorithm = (inputText.get("1.0", END)).split("\n") # Splits the algorithm that was written into the input text box and stores it in an array.
	for line in algorithm:
		if(re.match("^(int)\s*([A-z]+[0-9]*)$", line)):
			instruction = re.match("^(int)\s*([A-z]+[0-9]*)$", line)
			register = instruction.group(2)
			if(register not in registerList):
				registerList.append(register)
	outputText.config(state = NORMAL)
	outputText.insert(END, "MOV R0, 0\n")
	outputText.config(state = DISABLED)
	while(algorithm != [] and cycles != 0):
		cycles = branchWhile(algorithm, cycles)
		cycles = operations(algorithm[0], cycles)
		algorithm.pop(0)
	return cycles

def translate():
	cycles = 1
	outputText.config(state = NORMAL)
	outputText.delete("1.0", END)
	outputText.config(state = DISABLED)
	registerList = []
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
	counterList = [0, 0, 0]

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
