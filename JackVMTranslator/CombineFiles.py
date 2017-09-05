import glob, os
directory = "C:/Users/sahil.masand/OneDrive/CS/Nand2Tetris/nand2tetris/projects/08/FunctionCalls/FibonacciElement/"
filenames = []
OutFile = "temp.vm"

os.chdir(directory)
for file in glob.glob("*.vm"):
    filenames.append(file)

with open(OutFile, 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read())
outfile.close()
