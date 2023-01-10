# author: Harrison Mesh
# version: 0.1
import numpy as np
import sympy as sp


#note: I consider ties to have the same leading digit as the digit leading into the tie.

#ask user for input file names and base
print("Welcome to TieChecker!")
primality = int(input("What type of numbers are you checking? (0 = primes, 1 = composites, 2 = all) "))
base = int(input("What base are you checking over? "))
fileName = input("What is the path to the file? ")
#open file and get it to array
savedArray = np.loadtxt(fileName)
#filter out empty rows
filteredArray = savedArray[~np.all(savedArray == 0, axis=1)]
#figure out which lead changes might actually be ties and then calculate moduli to see how long the tie lasts and how it changes.
leadDigit = 0
index = 0
tiesIndex = 0
tiesArray = np.zeros((100000,1))
#figure out the indexes of the lead changes that are actually ties (if first number of row x > first number of row (x+1), it is actually a tie)
for each in filteredArray:
    newleadDigit = each[0]
    if leadDigit > newleadDigit:
        tiesArray[tiesIndex] = index
        tiesIndex += 1
    leadDigit = newleadDigit
    index +=1
filteredTies = tiesArray[~np.all(tiesArray == 0, axis =1)]
#figure out the length of the tie and which indexes were effected (old and new)
distChanges = np.zeros((len(filteredTies)*2, 2))
distIndex = 0
deletedRows = []
index = 0
if primality == 0:
    for each in filteredTies:
        leadToAnalyze = filteredArray[int(each)] #getting the data point where the tie occured
        primeToAnalyze = int(leadToAnalyze[2]) #getting the prime number where the tie occured
        indexOfTie = int(leadToAnalyze[1]) #getting the index of the tie
        newTied = int(leadToAnalyze[0]) #getting the last digit where the tie occured
        priorLeadToCompare = filteredArray[int(each)-1]
        oldTied = int(priorLeadToCompare[0]) #getting the last digit before the tie occured
        #note: newtied is already the modulus where it occured
        tieLength = 1 #length of tie
        tieFinished = False #representing if the tie has been calculated or not
        currentMod = newTied #present value of the mod
        while tieFinished == False:
            primeToAnalyze = sp.nextprime(primeToAnalyze)
            currentMod = (currentMod + primeToAnalyze) % base
            if currentMod == newTied:
                #tie ends with newmod taking the lead
                filteredArray[int(each)] = [newTied, indexOfTie + tieLength,primeToAnalyze] #the array has to be edited so that the lead is pushed farther back
                distChanges[distIndex] = [oldTied, tieLength] #new terms that have old as lead
                distChanges[distIndex+1] = [newTied, -1 * tieLength] #new terms that don't have new as lead
                tieFinished = True
            elif currentMod == oldTied:
                deletedRows = np.append(deletedRows, (int(filteredTies[index]), int(filteredTies[index]) + 1)) #mark where to delete row as it was a tie that went back to old winner, and the old winner was notated and mark where to delete the row after as it will be redundant
                distChanges[distIndex] = [oldTied, tieLength] #new terms that have old as lead
                distChanges[distIndex+1] = [newTied, -1 * tieLength] #new terms that don't have new as lead
                tieFinished = True
            else:
                tieLength += 1
        distIndex += 2
        index += 1
if primality == 1:
    for each in filteredTies:
        leadToAnalyze = filteredArray[int(each)] #getting the data point where the tie occured
        compositeToAnalyze = int(leadToAnalyze[2]) #getting the prime number where the tie occured
        indexOfTie = int(leadToAnalyze[1]) #getting the index of the tie
        newTied = int(leadToAnalyze[0]) #getting the last digit where the tie occured
        priorLeadToCompare = filteredArray[int(each)-1]
        oldTied = int(priorLeadToCompare[0]) #getting the last digit before the tie occured
        #note: newtied is already the modulus where it occured
        tieLength = 1 #length of tie
        tieFinished = False #representing if the tie has been calculated or not
        currentMod = newTied #present value of the mod
        while tieFinished == False: 
            if compositeToAnalyze + 1 == sp.nextprime(compositeToAnalyze):
                compositeToAnalyze += 2
            else:
                compositeToAnalyze += 1
            currentMod = (currentMod + compositeToAnalyze) % base
            if currentMod == newTied:
                #tie ends with newmod taking the lead
                filteredArray[int(each)] = [newTied, indexOfTie + tieLength,compositeToAnalyze] #the array has to be edited so that the lead is pushed farther back
                distChanges[distIndex] = [oldTied, tieLength] #new terms that have old as lead
                distChanges[distIndex+1] = [newTied, -1 * tieLength] #new terms that don't have new as lead
                tieFinished = True
            elif currentMod == oldTied:
                deletedRows = np.append(deletedRows, (int(filteredTies[index]), int(filteredTies[index]) + 1)) #mark where to delete row as it was a tie that went back to old winner, and the old winner was notated and mark where to delete the row after as it will be redundant
                distChanges[distIndex] = [oldTied, tieLength] #new terms that have old as lead
                distChanges[distIndex+1] = [newTied, -1 * tieLength] #new terms that don't have new as lead
                tieFinished = True
            else:
                tieLength += 1
        distIndex += 2
        index += 1
deletedRows = deletedRows.astype('int32')
print(len(filteredArray))
x=0
for each in deletedRows:
    if each >= len(filteredArray):
        deletedRows[x] = deletedRows[x-1]
    x += 1
filteredArray = np.delete(filteredArray, deletedRows, axis=0) #delete marked rows
#edit the distribution array (how many to add/delete) after calcuating the ties
editDistance = np.zeros(base)
for each in distChanges:
    remainder = int(each[0])
    amount = int(each[1])
    editDistance[remainder] = editDistance[remainder] + amount
#save new files
print(len(filteredArray))
openFile = open("C:/Users/hmesh/Downloads/research data/leadFreqFixed%s.txt" % base,"w")
saveArray = [filteredArray]
for each in saveArray:
    np.savetxt(openFile, each)
openFile.close()