                                                #===============================================================================#
                                                #                   Pontificia Universidad Javeriana, Cali                      #
                                                #                           Facultad de Ingeniería                              #
                                                #                    Ingeniería de Sistemas y Computación                       #
                                                #                       Arquitectura del Computador II                          #
                                                #                               Antonio Yu Chen                                 #
                                                #===============================================================================#

import re
from tkinter import *

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
frequency = 0
period = 0

def registerToConstant(line, cycles):
    """Function that has a line of code as an argument and matches it to the register = constant instruction in Von Neumann and returns the cycles it takes."""
    # Regular expression for register = constant.
    if(re.match("^([A-z]+)\s*=\s*([0-9]+)$", line)):
        outputText.config(state = NORMAL)
        instruction = re.match("^([A-z]+)\s*=\s*([0-9]+)$", line)
        register = instruction.group(1)
        constant = instruction.group(2)
        if(register not in registerList):
            registerList.append(register)
        outputText.insert(END, "MOV R{}, {}\n".format(registerList.index(register), constant))
        cycles = cycles + 5
        outputText.config(state = DISABLED)
    return cycles
        
def registerToRegister(line, cycles):
    """Function that has a line of code as an argument and matches it to the register = register instruction in Von Neumann and returns the cycles it takes."""
    # Regular expression for register = register.
    if(re.match("^([A-z]+)\s*=\s*([A-z]+)$", line)):
        outputText.config(state = NORMAL)
        instruction = re.match("^([A-z]+)\s*=\s*([A-z]+)$", line)
        register1 = instruction.group(1)
        register2 = instruction.group(2)
        if(register1 not in registerList):
            registerList.append(register1)
        if(register2 not in registerList):
            registerList.append(register2)
        outputText.insert(END, "MOV R{}, R{}\n".format(registerList.index(register1), registerList.index(register2)))
        cycles = cycles + 6
        outputText.config(state = DISABLED)
    return cycles

def addRegisterToConstant(line, cycles):
    """Function that has a line of code as an argument and matches it to the register = register + constant instruction in Von Neumann and returns the cycles it takes."""
    if(re.match("^([A-z]+)\s*=\s*([A-z]+)\s*[+]\s*([0-9]+)$", line)):
        outputText.config(state = NORMAL)
        instruction = re.match("^([A-z]+)\s*=\s*([A-z]+)\s*[+]\s*([0-9]+)$", line)
        register1 = instruction.group(1)
        register2 = instruction.group(2)
        constant = instruction.group(3)
        if(register1 not in registerList):
            registerList.append(register1)
        if(register2 not in registerList):
            registerList.append(register2)
        if(register1 == register2):
            outputText.insert(END, "ADD R{}, {}\n".format(registerList.index(register1), constant))
            cycles = cycles + 8
        elif(register1 != register2):
            outputText.insert(END, "ADD R{}, {}\n".format(registerList.index(register2), constant))
            outputText.insert(END, "MOV R{}, R{}\n".format(registerList.index(register1), registerList.index(register2)))
            cycles = cycles + 14
        outputText.config(state = DISABLED)
    elif(re.match("^([A-z]+)\s*=\s*([0-9]+)\s*[+]\s*([A-z]+)$", line)):
        outputText.config(state = NORMAL)
        instruction = re.match("^([A-z]+)\s*=\s*([0-9]+)\s*[+]\s*([A-z]+)$", line)
        register1 = instruction.group(1)
        register2 = instruction.group(3)
        constant = instruction.group(2)
        if(register1 not in registerList):
            registerList.append(register1)
        if(register2 not in registerList):
            registerList.append(register2)
        if(register1 == register2):
            outputText.insert(END, "ADD R{}, {}\n".format(registerList.index(register1), constant))
            cycles = cycles + 8
        elif(register1 != register2):
            outputText.insert(END, "ADD R{}, {}\n".format(registerList.index(register2), constant))
            outputText.insert(END, "MOV R{}, R{}\n".format(registerList.index(register1), registerList.index(register2)))
            cycles = cycles + 14
        outputText.config(state = DISABLED)
    return cycles

def addRegisterToRegister(line, cycles):
    """Function that has a line of code as an argument and matches it to the register = register + register instruction in Von Neumann and returns the cycles it takes."""
    if(re.match("^([A-z]+)\s*=\s*([A-z]+)\s*[+]\s*([A-z]+)$", line)):
        outputText.config(state = NORMAL)
        instruction = re.match("^([A-z]+)\s*=\s*([A-z]+)\s*[+]\s*([A-z]+)$", line)
        register1 = instruction.group(1)
        register2 = instruction.group(2)
        register3 = instruction.group(3)
        if(register1 not in registerList):
            registerList.append(register1)
        if(register2 not in registerList):
            registerList.append(register2)
        if(register3 not in registerList):
            registerList.append(register3)
        if(register1 == register2 and register1 != register3):
            outputText.insert(END, "ADD R{}, R{}\n".format(registerList.index(register1), registerList.index(register3)))
            cycles = cycles + 0
        elif(register1 == register3 and register1 != register2):
            outputText.insert(END, "ADD R{}, R{}\n".format(registerList.index(register1), registerList.index(register2)))
            cycles = cycles + 0
        elif(register1 == register2 and register1 == register3):
            outputText.insert(END, "ADD R{}, R{}\n".format(registerList.index(register1), registerList.index(register1)))
            cycles = cycles + 0
        else:
            outputText.insert(END, "ADD R{}, R{}\n".format(registerList.index(register2), registerList.index(register3)))
            outputText.insert(END, "MOV R{}, R{}\n".format(registerList.index(register1), registerList.index(register2)))
            cycles = cycles + 0
        outputText.config(state = DISABLED)
    return cycles

def addConstantToConstant(line, cycles):
    """Function that has a line of code as an argument and matches it to the register = constant + constant instruction in Von Neumann and returns the cycles it takes."""
    if(re.match("^([A-z]+)\s*=\s*([0-9]+)\s*[+]\s*([0-9]+)$", line)):
        outputText.config(state = NORMAL)
        instruction = re.match("^([A-z]+)\s*=\s*([0-9]+)\s*[+]\s*([0-9]+)$", line)
        register = instruction.group(1)
        constant1 = instruction.group(2)
        constant2 = instruction.group(3)
        if(register not in registerList):
            registerList.append(register)
        outputText.insert(END, "MOV R{}, {}\n".format(registerList.index(register), constant1))
        outputText.insert(END, "ADD R{}, {}\n".format(registerList.index(register), constant2))
        cycles = cycles + 0
        outputText.config(state = DISABLED)
    return cycles

def mulRegisterToConstant(line, cycles):
    """Function that has a line of code as an argument and matches it to the register = register * constant instruction in Von Neumann and returns the cycles it takes."""
    if(re.match("^([A-z]+)\s*=\s*([A-z]+)\s*[*]\s*([0-9]+)$", line)):
        outputText.config(state = NORMAL)
        instruction = re.match("^([A-z]+)\s*=\s*([A-z]+)\s*[*]\s*([0-9]+)$", line)
        register1 = instruction.group(1)
        register2 = instruction.group(2)
        constant = instruction.group(3)
        if(register1 not in registerList):
            registerList.append(register1)
        if(register2 not in registerList):
            registerList.append(register2)
        if(register1 == register2):
            outputText.insert(END, "MUL R{}, {}\n".format(registerList.index(register1), constant))
            cycles = cycles + 0
        elif(register1 != register2):
            outputText.insert(END, "MUL R{}, {}\n".format(registerList.index(register2), constant))
            outputText.insert(END, "MOV R{}, R{}\n".format(registerList.index(register1), registerList.index(register2)))
            cycles = cycles + 0
        outputText.config(state = DISABLED)
    elif(re.match("^([A-z]+)\s*=\s*([0-9]+)\s*[*]\s*([A-z]+)$", line)):
        outputText.config(state = NORMAL)
        instruction = re.match("^([A-z]+)\s*=\s*([0-9]+)\s*[*]\s*([A-z]+)$", line)
        register1 = instruction.group(1)
        register2 = instruction.group(3)
        constant = instruction.group(2)
        if(register1 not in registerList):
            registerList.append(register1)
        if(register2 not in registerList):
            registerList.append(register2)
        if(register1 == register2):
            outputText.insert(END, "MUL R{}, {}\n".format(registerList.index(register1), constant))
            cycles = cycles + 0
        elif(register1 != register2):
            outputText.insert(END, "MUL R{}, {}\n".format(registerList.index(register2), constant))
            outputText.insert(END, "MOV R{}, R{}\n".format(registerList.index(register1), registerList.index(register2)))
            cycles = cycles + 0
        outputText.config(state = DISABLED)
    return cycles

def mulRegisterToRegister(line, cycles):
    """Function that has a line of code as an argument and matches it to the register = register * register instruction in Von Neumann and returns the cycles it takes."""
    if(re.match("^([A-z]+)\s*=\s*([A-z]+)\s*[*]\s*([A-z]+)$", line)):
        outputText.config(state = NORMAL)
        instruction = re.match("^([A-z]+)\s*=\s*([A-z]+)\s*[*]\s*([A-z]+)$", line)
        register1 = instruction.group(1)
        register2 = instruction.group(2)
        register3 = instruction.group(3)
        if(register1 not in registerList):
            registerList.append(register1)
        if(register2 not in registerList):
            registerList.append(register2)
        if(register3 not in registerList):
            registerList.append(register3)
        if(register1 == register2 and register1 != register3):
            outputText.insert(END, "MUL R{}, R{}\n".format(registerList.index(register1), registerList.index(register3)))
            cycles = cycles + 0
        elif(register1 == register3 and register1 != register2):
            outputText.insert(END, "MUL R{}, R{}\n".format(registerList.index(register1), registerList.index(register2)))
            cycles = cycles + 0
        elif(register1 == register2 and register1 == register3):
            outputText.insert(END, "MUL R{}, R{}\n".format(registerList.index(register1), registerList.index(register1)))
            cycles = cycles + 0
        else:
            outputText.insert(END, "MUL R{}, R{}\n".format(registerList.index(register2), registerList.index(register3)))
            outputText.insert(END, "MOV R{}, R{}\n".format(registerList.index(register1), registerList.index(register2)))
            cycles = cycles + 0
        outputText.config(state = DISABLED)
    return cycles

def mulConstantToConstant(line, cycles):
    """Function that has a line of code as an argument and matches it to the register = constant * constant instruction in Von Neumann and returns the cycles it takes."""
    if(re.match("^([A-z]+)\s*=\s*([0-9]+)\s*[*]\s*([0-9]+)$", line)):
        outputText.config(state = NORMAL)
        instruction = re.match("^([A-z]+)\s*=\s*([0-9]+)\s*[*]\s*([0-9]+)$", line)
        register = instruction.group(1)
        constant1 = instruction.group(2)
        constant2 = instruction.group(3)
        if(register not in registerList):
            registerList.append(register)
        outputText.insert(END, "MOV R{}, {}\n".format(registerList.index(register), constant1))
        outputText.insert(END, "MUL R{}, {}\n".format(registerList.index(register), constant2))
        cycles = cycles + 0
        outputText.config(state = DISABLED)
    return cycles

def subRegisterToConstant(line, cycles):
    """Function that has a line of code as an argument and matches it to the register = register - constant or constant - register instruction in Von Neumann and returns the cycles it takes."""
    if(re.match("^([A-z]+)\s*=\s*([A-z]+)\s*[-]\s*([0-9]+)$", line)):
        outputText.config(state = NORMAL)
        instruction = re.match("^([A-z]+)\s*=\s*([A-z]+)\s*[-]\s*([0-9]+)$", line)
        register1 = instruction.group(1)
        register2 = instruction.group(2)
        constant = instruction.group(3)
        if(register1 not in registerList):
            registerList.append(register1)
        if(register2 not in registerList):
            registerList.append(register2)
        if(register1 == register2):
            outputText.insert(END, "SUB R{}, {}\n".format(registerList.index(register1), constant))
            cycles = cycles + 0
        elif(register1 != register2):
            outputText.insert(END, "SUB R{}, {}\n".format(registerList.index(register2), constant))
            outputText.insert(END, "MOV R{}, R{}\n".format(registerList.index(register1), registerList.index(register2)))
            cycles = cycles + 0
        outputText.config(state = DISABLED)
    elif(re.match("^([A-z]+)\s*=\s*([0-9]+)\s*[-]\s*([A-z]+)$", line)):
        outputText.config(state = NORMAL)
        instruction = re.match("^([A-z]+)\s*=\s*([0-9]+)\s*[-]\s*([A-z]+)$", line)
        register1 = instruction.group(1)
        register2 = instruction.group(3)
        constant = instruction.group(2)
        if(register1 not in registerList):
            registerList.append(register1)
        if(register2 not in registerList):
            registerList.append(register2)
        outputText.insert(END, "MOV R{}, {}\n".format(len(registerList), constant))
        outputText.insert(END, "SUB R{}, R{}\n".format(len(registerList), registerList.index(register2)))
        outputText.insert(END, "MOV R{}, R{}\n".format(registerList.index(register1), len(registerList)))
        cycles = cycles + 0
        outputText.config(state = DISABLED)
    return cycles

def subConstantToConstant(line, cycles):
    """Function that has a line of code as an argument and matches it to the register = constant - constant instruction in Von Neumann and returns the cycles it takes."""
    if(re.match("^([A-z]+)\s*=\s*([0-9]+)\s*[-]\s*([0-9]+)$", line)):
        outputText.config(state = NORMAL)
        instruction = re.match("^([A-z]+)\s*=\s*([0-9]+)\s*[-]\s*([0-9]+)$", line)
        register = instruction.group(1)
        constant1 = instruction.group(2)
        constant2 = instruction.group(3)
        if(register not in registerList):
            registerList.append(register)
        outputText.insert(END, "MOV R{}, {}\n".format(registerList.index(register), constant1))
        outputText.insert(END, "SUB R{}, {}\n".format(registerList.index(register), constant2))
        cycles = cycles + 0
        outputText.config(state = DISABLED)
    return cycles

def subRegisterToRegister(line, cycles):
    """Function that has a line of code as an argument and matches it to the register = register - register instruction in Von Neumann and returns the cycles it takes."""
    if(re.match("^([A-z]+)\s*=\s*([A-z]+)\s*[-]\s*([A-z]+)$", line)):
        outputText.config(state = NORMAL)
        instruction = re.match("^([A-z]+)\s*=\s*([A-z]+)\s*[-]\s*([A-z]+)$", line)
        register1 = instruction.group(1)
        register2 = instruction.group(2)
        register3 = instruction.group(3)
        if(register1 not in registerList):
            registerList.append(register1)
        if(register2 not in registerList):
            registerList.append(register2)
        if(register3 not in registerList):
            registerList.append(register3)
        if(register1 == register2 and register1 != register3):
            outputText.insert(END, "SUB R{}, R{}\n".format(registerList.index(register1), registerList.index(register3)))
            cycles = cycles + 0
        elif(register1 == register2 and register1 == register3):
            outputText.insert(END, "SUB R{}, R{}\n".format(registerList.index(register1), registerList.index(register1)))
            cycles = cycles + 0
        else:
            outputText.insert(END, "SUB R{}, R{}\n".format(registerList.index(register2), registerList.index(register3)))
            outputText.insert(END, "MOV R{}, R{}\n".format(registerList.index(register1), registerList.index(register2)))
            cycles = cycles + 0
        outputText.config(state = DISABLED)
    return cycles

def divConstantToConstant(line, cycles):
    """Function that has a line of code as an argument and matches it to the register = constant / constant instruction in Von Neumann and returns the cycles it takes."""
    if(re.match("^([A-z]+)\s*=\s*([0-9]+)\s*[/]\s*([0-9]+)$", line)):
        outputText.config(state = NORMAL)
        instruction = re.match("^([A-z]+)\s*=\s*([0-9]+)\s*[/]\s*([0-9]+)$", line)
        register = instruction.group(1)
        constant1 = instruction.group(2)
        constant2 = instruction.group(3)
        if(register not in registerList):
            registerList.append(register)
        outputText.insert(END, "MOV R{}, {}\n".format(registerList.index(register), constant1))
        outputText.insert(END, "DIV R{}, {}\n".format(registerList.index(register), constant2))
        cycles = cycles + 0
        outputText.config(state = DISABLED)
    return cycles

def divRegisterToConstant(line, cycles):
    """Function that has a line of code as an argument and matches it to the register = register / constant or constant / register instruction in Von Neumann and returns the cycles it takes."""
    if(re.match("^([A-z]+)\s*=\s*([A-z]+)\s*[/]\s*([0-9]+)$", line)):
        outputText.config(state = NORMAL)
        instruction = re.match("^([A-z]+)\s*=\s*([A-z]+)\s*[/]\s*([0-9]+)$", line)
        register1 = instruction.group(1)
        register2 = instruction.group(2)
        constant = instruction.group(3)
        if(register1 not in registerList):
            registerList.append(register1)
        if(register2 not in registerList):
            registerList.append(register2)
        if(register1 == register2):
            outputText.insert(END, "DIV R{}, {}\n".format(registerList.index(register1), constant))
            cycles = cycles + 0
        elif(register1 != register2):
            outputText.insert(END, "DIV R{}, {}\n".format(registerList.index(register2), constant))
            outputText.insert(END, "MOV R{}, R{}\n".format(registerList.index(register1), registerList.index(register2)))
            cycles = cycles + 0
        outputText.config(state = DISABLED)
    elif(re.match("^([A-z]+)\s*=\s*([0-9]+)\s*[/]\s*([A-z]+)$", line)):
        outputText.config(state = NORMAL)
        instruction = re.match("^([A-z]+)\s*=\s*([0-9]+)\s*[/]\s*([A-z]+)$", line)
        register1 = instruction.group(1)
        register2 = instruction.group(3)
        constant = instruction.group(2)
        if(register1 not in registerList):
            registerList.append(register1)
        if(register2 not in registerList):
            registerList.append(register2)
        outputText.insert(END, "MOV R{}, {}\n".format(len(registerList), constant))
        outputText.insert(END, "DIV R{}, R{}\n".format(len(registerList), registerList.index(register2)))
        outputText.insert(END, "MOV R{}, R{}\n".format(registerList.index(register1), len(registerList)))
        cycles = cycles + 0
        outputText.config(state = DISABLED)
    return cycles
            
def compiler(cycles):
    algorithm = (inputText.get("1.0", "end-1c")).split("\n") # Splits the algorithm that was written into the input text box and stores it in an array.
    for line in algorithm:
        cycles = registerToConstant(line, cycles)
        cycles = registerToRegister(line, cycles)
        cycles = addRegisterToConstant(line, cycles)
        cycles = addRegisterToRegister(line, cycles)
        cycles = addConstantToConstant(line, cycles)
        cycles = mulRegisterToConstant(line, cycles)
        cycles = mulRegisterToRegister(line, cycles)
        cycles = mulConstantToConstant(line, cycles)
        cycles = subRegisterToConstant(line, cycles)
        cycles = subConstantToConstant(line, cycles)
        cycles = subRegisterToRegister(line, cycles)
        cycles = divConstantToConstant(line, cycles)
        cycles = divRegisterToConstant(line, cycles)
    return cycles
        
def translate():
    cycles = 0
    if(inputText.get("1.0", END) != "\n"):
        cycles = compiler(cycles)
    print(cycles)
    
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
    cycles = 0
    period = 0
    frequency = 0
    
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
