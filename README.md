# PrimeSumDist
This was the program used for my research paper in order to calculate the last digit distribution of prime and composite numbers. 

In order to use this program, you should first use the psd.py file. You will need to change the paths of the files that it saves to.

Then, in order to turn the interval data into usable data, you would need to first run the tiechecker.py progam ONCE. Note that this program removes ties left by psd, but does not check for ties, so running it multiple times will result in incorrect data. Also note that some of the varaibles, such as depth, may need to be changed for tiechecker to work properly.

Lastly, you can use IntervalAnalyzer to take the edited data and convert it into the frequency table. You can also find the length of the tiechecker output file to find the number of lead changes.
