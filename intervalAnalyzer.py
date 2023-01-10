#intervalAnalyzer.py
#author: H. Mesh
#version: 0.1 
import numpy as np
#ask user for input file name and create variables / arrays needed
print("Welcome to Interval Analyzer!")
base = int(input("What base are you checking over? "))
fileName = input("What is the path to the file? ")
leadArray = np.zeros(base, np.int64)
depth = 1000000000
#open file and get it to array
dataArray = np.loadtxt(fileName)
#run through each base 
priorAmount = 1
priorBase = 0
for each in dataArray:
    newBase = int(each[0])
    amountToAdd = each[1]
    leadArray[priorBase] += (amountToAdd - priorAmount)
    priorAmount = amountToAdd
    priorBase = newBase
leadArray[newBase] += (depth - amountToAdd+1)
#save and print results
print(leadArray)
openFile = open("C:/Users/hmesh/Downloads/research data/leadData%s.txt" % base,"w") 
np.savetxt(openFile, leadArray)
openFile.close() 