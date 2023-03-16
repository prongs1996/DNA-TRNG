#@MSSh
import numpy as np
# import matplotlib.pyplot as plt
import pickle as pkl
from tqdm import tqdm


with open('read_order_alice.txt', 'r') as f:
    lines = f.readlines()

numbers = [int(line.split(',')[1].strip()) for line in lines[1:]]

print("Number of reads found: ", len(numbers))
print(numbers[:5], numbers[-5:])

f = open('generated_bitstream.txt', 'w')

bitSequences = []

numbers_taken = []


for num in tqdm(numbers):
    if num<8192: # 2^13
        numbers_taken.append(num)
        bit_seq = '{0:013b}'.format(num)
        # f.write(bit_seq + '\n')
        f.write(bit_seq)
        bitSequences.append(bit_seq)

f.close()


print("Number of reads with address filtered below 2^13: ", len(numbers_taken)) # 
cnt0 = np.zeros(13)
cnt1 = np.zeros(13)

cumSums = []

for bit_seq in tqdm(bitSequences):
    cumSum = 0
    for i in range(13):
        if bit_seq[i]=='0':
            cnt0[i] += 1
            cumSum -=1
        else:
            cnt1[i] += 1
            cumSum += 1
    
    cumSums.append(cumSum)

# plt.figure(figsize=(20,10))

# # plt.hist(numbers_taken, bins=1000)
# # plt.hist(cumSums, bins=30)


# plt.ylim(0.45,0.55)
# plt.plot(cnt0/len(numbers_taken), label='0s')
# plt.plot(cnt1/len(numbers_taken), label='1s')
# plt.legend()


# plt.savefig('plot.png')