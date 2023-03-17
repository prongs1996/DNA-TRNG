import sys
import getopt
from tqdm import *


def amls_round(stream):
    if len(stream) < 2:
        return []
    res = []
    s1 = []
    sa = []
    p0 = None
    for p1 in stream:
        if p0 == None:
            p0 = p1
        else:
            if p0 == p1:
                sa.append('0')
                s1.append(str(p0))
            else:
                sa.append('1')
                res.append(str(p0))
            p0 = None
    return res + amls_round(sa) + amls_round(s1)
argv = sys.argv[1:]
inputfile = ''
outputfile = ''
k = 0
opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile=","sides="])
for opt, arg in opts:
    if opt == '-h':
        print ('peres.py -i <inputfile> -o <outputfile> -s <number of faces in dice>')
        sys.exit()
    elif opt in ("-i", "--ifile"):
        inputfile = arg
    elif opt in ("-o", "--ofile"):
        outputfile = arg
    elif opt in ("-s", "--sides"):
        k = int(arg)

# filename = input("File name: ")
# k = int(input("k: "))
filename = inputfile
file = open(filename, 'r')
# outputfilename = input("Output file name:")
outputfilename = outputfile

bitstreams = {i:[] for i in range(1,k+1)}
content = file.readlines()
for i in tqdm(range(len(content[0]))):
    bitstreams[(i%k)+1].append(content[0][i])

result = []
for i in tqdm(range(1,k+1)):
    result += amls_round(bitstreams[i])
outputfile = open(outputfilename, 'w')
outputfile.write(''.join(result))

