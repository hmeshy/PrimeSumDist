# author: H. Mesh
# version: v3
import time
import numpy as np
import sympy as sp
import primesieve as ps
depthFreq = [] #placeholder for editing the composite and all number calculations


# Step 1 - Ask user for inputs needed + display version number
# Inputs Needed - Base (2-10 at least) Primality (P for prime, C for composite, A for all numbers) Depth (number of primes/composites to search for), reading from file?
print("Welcome to PrimeSumDist v3.dev!")
primality = int(input("What type of numbers are you searching? (0 = primes, 1 = composites, 2 = all) "))
depth = int(input("How many primes/composites do you want to search to? "))
maxBase = int(input("What base do you want to search up to? "))
if primality == 0:
    base = 3
else:
    base = 2


# Step 2 - Converting inputs given to easier things to do (really just depth -> estimate of location of nth prime)
    #unneeded because of sp.prime function
# Step 3 - Generating the list of primes, composites, all numbers to save to array / file
start_time = time.time()
if primality == 0: #primes
    print("Generating primes...")
    scamArray = np.asarray(ps.n_primes(depth), dtype = np.uint64)
    primesArray = scamArray.reshape(depth, 1)
    primeArray = np.zeros(shape=(depth, 1), dtype = np.uint64)
    print("Finished generating primes! Time taken: %s seconds." % (time.time() - start_time))
elif primality == 1: #composites
    print("Generating composites...")
    primesArray = np.asarray(ps.primes(sp.composite(depth)), dtype = np.uint64)
    primesArray = np.subtract(primesArray,2)
    allArray = np.arange(2, sp.composite(depth)+1, 1)
    flatArray = np.delete(allArray, primesArray) #this line gets rid of the primes within an array of numbers from 2 to the composite needed
    #the lines below just rearrange the composites to the necessary format
    compositesArray = flatArray.reshape(flatArray.size, 1)
    compositeArray = np.zeros(shape=(compositesArray.size, 1), dtype = np.uint64)
    print("Finished generating composites! Time taken: %s seconds." % (time.time() - start_time))
elif primality == 2:
    print("Adding numbers to array...")
    wholeArray = np.arange(1, depth + 1, 1)
    emptyArray = np.zeros(depth)
    fullArray = np.stack((wholeArray, emptyArray), -1)
    fullArray = fullArray.reshape(depth, 2)
    print("Finished generating numbers! Time taken: %s seconds." % (time.time() - start_time))

# Step 4 / 5 - find partial sums and modulo it by the base i.e. [[2],[3],[5],[7]] base 3 -> 2 % 3, (2%3 +3) %3, (x + 5) %3, etc.; output [[2,2], [3,2], [5,1], [7,2]]
while base <= maxBase:
    print("Calculating base %s." % base)
    check_time = time.time()
    base_time = time.time()
    if primality == 0:
        print("Generating sums...")
        partialSum = 0
        cellNumber = 0
        for cell in primesArray:
            partialSum = (partialSum + cell) % base
            primeValue = cell
            primeArray[cellNumber] = [partialSum]
            cellNumber += 1
        print("Finished partial sums! Time taken: %s seconds." % (time.time() - check_time))
    elif primality == 1:
        print("Generating sums...")
        partialSum = 0
        cellNumber = 0
        for cell in compositesArray:
            partialSum = (partialSum + cell) % base
            compValue = cell
            compositeArray[cellNumber] = [partialSum]
            cellNumber += 1
        print("Finished partial sums! Time taken: %s seconds." % (time.time() - check_time))
    elif primality == 2:
        fullArray[:, -1] = 0
        print("Generating sums...")
        partialSum = 0
        rowNumber = 0
        for row in fullArray:
            for cell in row:
                if cell != 0:
                    partialSum = (partialSum + cell) % base
                    value = cell
                else:
                    fullArray[rowNumber] = [value, partialSum]
            rowNumber += 1
        print("Finished partial sums! Time taken: %s seconds." % (time.time() - check_time))

    # Step 6 - Calculate last digit dist and save as well as partial baseFreq at each step
    check_time = time.time()
    print("Generating frequency calculations...")
    baseFreq = np.zeros(base, dtype = np.uint64)
    leadChangeArray = np.zeros((100000, 3), dtype = np.uint64)
    x = 1
    leadNum = 0
    changeNum = 0
    if primality == 0:
        for cell in primeArray:
            baseFreq[cell] = baseFreq[cell] + 1
            newleadIndex = np.argmax(baseFreq)
            if newleadIndex != leadNum:
                leadChangeArray[changeNum] = [newleadIndex, x, scamArray[x-1]]
                changeNum += 1
                leadNum = newleadIndex
            x += 1
        print("Finished frequency calculations! Time taken: %s seconds." % (time.time() - check_time))
        openFile = open("C:/Users/hmesh/Downloads/research data/leadFreqP%s_%s.txt" % (base,depth),"w")
        np.savetxt(openFile, leadChangeArray)
        openFile.close()
    elif primality == 1:
        for cell in compositeArray:
            baseFreq[cell] = baseFreq[cell] + 1
            newleadIndex = np.argmax(baseFreq)
            if newleadIndex != leadNum:
                leadChangeArray[changeNum] = [newleadIndex, x, flatArray[x-1]]
                changeNum += 1
                leadNum = newleadIndex
            x += 1
        print("Finished frequency calculations! Time taken: %s seconds." % (time.time() - check_time))
        openFile = open("C:/Users/hmesh/Downloads/research data/leadFreqC%s_%s.txt" % (base,depth),"w")
        np.savetxt(openFile, leadChangeArray)
        openFile.close()
    elif primality == 2:
        for row in fullArray:
            partial = int(row[1])
            baseFreq[partial] = baseFreq[partial] + 1 
            depthFreq[x] = baseFreq
            x += 1       
        print("Finished frequency calculations! Time taken: %s seconds." % (time.time() - check_time))
    openFile = open("C:/Users/hmesh/Downloads/research data/baseFreq%s_%s.txt" % (base, depth),"w")
    saveArray = [baseFreq]
    for each in saveArray:
        np.savetxt(openFile, each)
    openFile.close()

    base += 1
 
# Step 8 - Output (finished)
print("This program ran successfully in %s seconds." % (time.time() - start_time))
