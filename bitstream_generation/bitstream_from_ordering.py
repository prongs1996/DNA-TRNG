#@MSSh
import numpy as np
# import matplotlib.pyplot as plt
import pickle as pkl
from tqdm import tqdm
import sys
import getopt

argv = sys.argv[1:]
inputfile = ''
outputfile = ''
k = 0
opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile=","sides="])
for opt, arg in opts:
    if opt == '-h':
        print ('bitstream_from_ordering.py -i <inputfile> -o <outputfile> -s <number of faces in dice>')
        sys.exit()
    elif opt in ("-i", "--ifile"):
        inputfile = arg
    elif opt in ("-o", "--ofile"):
        outputfile = arg
    elif opt in ("-s", "--sides"):
        k = int(arg)


with open(inputfile, 'r') as f:
    lines = f.readlines()

numbers = [int(line.split(',')[1].strip()) for line in lines[1:]]

print("Number of reads found: ", len(numbers))
print(numbers[:5], numbers[-5:])

f = open(outputfile, 'w')

bitSequences = []

numbers_taken = []

n = 2**k

for num in tqdm(numbers):
    if num<n: # 2^13
        numbers_taken.append(num)
        string = '{0:0'+str(k)+'b}'
        bit_seq = string.format(num)
        # f.write(bit_seq + '\n')
        f.write(bit_seq)
        bitSequences.append(bit_seq)

f.close()


# print("Number of reads with address filtered below 2^s: ", len(numbers_taken)) # 
# cnt0 = np.zeros(13)
# cnt1 = np.zeros(13)

# cumSums = []

# for bit_seq in tqdm(bitSequences):
#     cumSum = 0
#     for i in range(13):
#         if bit_seq[i]=='0':
#             cnt0[i] += 1
#             cumSum -=1
#         else:
#             cnt1[i] += 1
#             cumSum += 1
    
#     cumSums.append(cumSum)

# plt.figure(figsize=(20,10))

# # plt.hist(numbers_taken, bins=1000)
# # plt.hist(cumSums, bins=30)


# plt.ylim(0.45,0.55)
# plt.plot(cnt0/len(numbers_taken), label='0s')
# plt.plot(cnt1/len(numbers_taken), label='1s')
# plt.legend()


# plt.savefig('plot.png')