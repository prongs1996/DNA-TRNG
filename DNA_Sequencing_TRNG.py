import random
from sortedcontainers import *
from math import *
from tqdm import tqdm
from time import *
import argparse

### Jakobsson/Juels Algorithms
# Q1 considers the entire sequence of rolls and generates
# a single unbiased roll from a P-sided die where P is the
# total number of possible permutations of the sequence
def Jakob_Q1(rolls):
    n = len(rolls)
    fr = {}
    rank = SortedSet()
    for i in range(n):
        rank.add(rolls[i])
        if rolls[i] not in fr.keys():
            fr[rolls[i]] = 1
        else:
            fr[rolls[i]] += 1
    S = factorial(n)
    for i in rank:
        S = S // factorial(fr[i])
    L = 0
    F = S
    for i in range(n-1):
        l = 0
        for j in range(rank.index(rolls[i])):
            l += fr[rank[j]]
        v = fr[rolls[i]]
        f = n - i

        L = L + ((l*F) // f)
        F = (F*v) // f
        if fr[rolls[i]] == 1:
            del fr[rolls[i]]
            rank.remove(rolls[i])
        else:
            fr[rolls[i]] -= 1
    R = L+1
    return R, S

# Q2 produces an unbiased bitstream from a
# single roll R of an unbiased S-sided die 
def Jakob_Q2(R,S):
    binS = bin(S)[2:]
    binR = bin(R-1)[2:]
    binR = '0'*(len(binS)-len(binR)) + binR
    for i in range(len(binS)-1):
        if binS[i] == '1' and binR[i] == '0':
            return binR[i+1:]
    return ''

def Jakobsson(rolls):
    if len(rolls) > 10000:
        return ''
    R,S = Jakob_Q1(rolls)
    return Jakob_Q2(R,S)

def BlockwiseJakobsson(all_rolls, b):
    bits_extracted = []
    for i in range(len(all_rolls)//b):
        rolls = all_rolls[i*b:(i+1)*b]
        bits_extracted.append(Jakobsson(rolls))
    bits_extracted.append(Jakobsson(all_rolls[(len(all_rolls)//b)*b:]))
    return ''.join(bits_extracted)

### nCr Extractor Algorithms
# Q1 considers all indexes of a specific roll and generates
# a single unbiased roll from a P-sided die where P is the
# total number of ways to choose the indexes of the roll
def nCr_Q1(indexes, n):
	R = 0
	o = 0
	d = len(indexes)
	for i in indexes:
		R += comb(n-(i-o)-1, d)
		n = n-(i-o)-1
		d = d-1
		o = i+1
		#print(R,n,d,o)
	return R

# Q2 produces an unbiased bitstream from a
# single roll R of an unbiased S-sided die
# (exactly the same as Jakob_Q2)
def nCr_Q2(R,S):
    binS = bin(S)[2:]
    binR = bin(R)[2:]
    binR = '0'*(len(binS)-len(binR)) + binR
    for i in range(len(binS)-1):
        if binS[i] == '1' and binR[i] == '0':
            return binR[i+1:]
    return ''

def nCrExtractor(all_rolls):
    rolls = all_rolls
    sorted_ordering = SortedSet(rolls)
    all_bits = []
    while rolls:
        read = sorted_ordering[0]
        indexes = []
        for i in range(len(rolls)):
            if rolls[i] == read:
                    indexes.append(i)
        roll = nCr_Q1(indexes, len(rolls))
        all_bits.append(nCr_Q2(roll, comb(len(rolls), len(indexes))))
        while read in rolls:
            rolls.remove(read)
        sorted_ordering.discard(read)
    return ''.join(all_bits)

### Shrinking Window Algorithms
def ShrinkingWindow(all_rolls):
    unique = set(all_rolls)
    rolls = []
    for r in all_rolls:
        if r in unique:
            rolls.append(r)
            unique.remove(r)
        elif r in rolls:
            rolls.remove(r)
        
    sl = SortedList(rolls)
    count = len(rolls)
    all_bits = []
    for i in range(count):
        content1 = rolls[i]
        num = sl.index(content1)                                    # returns where content1 lies in the sorted list
        sl.remove(content1)
        window_size = count - i

        no_of_bits = floor(log2(window_size))
        while(num >= 2**no_of_bits):                                 # this loop figures out what is the window within which our random number lies
            num = num - 2**no_of_bits
            window_size = window_size - 2**no_of_bits
            no_of_bits = floor(log2(window_size))

        if window_size == 1:                                         # so that window size == 1
            continue

        bit_seq = ('{0:0'+str(no_of_bits)+'b}').format(num)         # generating the bits from the random number
        all_bits.append(bit_seq)
    return ''.join(all_bits)

### Halfbit
def Halfbit(rolls):
    all_bits = []
    if len(rolls)%2 == 1:
        rolls = rolls[:-1]
    for i in range(len(rolls)//2):
        if rolls[i*2] > rolls[i*2 + 1]:
            all_bits.append('1')
        elif rolls[i*2] < rolls[i*2 + 1]:
            all_bits.append('0')
    return ''.join(all_bits)

###Column-wise Algorithms
# Q2 produces a binary encoding of every
# roll R from a S-sided die
# (exactly the same as Jakob_Q2)
def Q2(R,S):
    binS = bin(S)[2:]
    binR = bin(R)[2:]
    binR = '0'*(len(binS)-len(binR)) + binR
    for i in range(len(binS)-1):
        if binS[i] == '1' and binR[i] == '0':
            return binR[i+1:]
    return ''

def ColumnwiseCoinDebiasing(all_rolls, coin_debiaser):
    all_bits = []
    sides = len(set(all_rolls))
    max_num_bits = floor(log(sides,2))
    all_rolls = list(map(lambda x: Q2(x,sides), all_rolls))
    
    for i in range(max_num_bits):
        rolls = list(filter(lambda x: len(x) >= max_num_bits-i, all_rolls))
        buckets = {}
        for r in rolls:
            if r[:max_num_bits-i-1] not in buckets:
                buckets[r[:max_num_bits-i-1]] = [r[max_num_bits-i-1]]
            else:
                buckets[r[:max_num_bits-i-1]].append(r[max_num_bits-i-1])
        for b in buckets:
            all_bits.append(''.join(coin_debiaser(''.join(buckets[b]))))
    return ''.join(all_bits)

def PeresDebiaser(bit_stream):
    if len(bit_stream) < 2:
        return []
    res = []
    s1 = []
    sa = []
    p0 = None
    for p1 in bit_stream:
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
    return res + PeresDebiaser(sa) + PeresDebiaser(s1)

def VNCDebiaser(bit_stream):
    all_bits = []
    if len(bit_stream)%2 == 1:
        bit_stream = bit_stream[:-1]
    for i in range(len(bit_stream)//2):
        if bit_stream[i*2] != bit_stream[i*2 + 1]:
            all_bits.append(bit_stream[i*2])
    return ''.join(all_bits)
    
def ColumnwisePeres(rolls):
    return ColumnwiseCoinDebiasing(rolls, PeresDebiaser)

def ColumnwiseVNC(rolls):
    return ColumnwiseCoinDebiasing(rolls,VNCDebiaser)

def extract_bits(rolls):
    '''
    ALG:
        0 - Jakobsson/Juels
        1 - Blockwise Jakobsson/Juels
        2 - nCr Extractor
        3 - Shrinking Window
        4 - Halfbit
        5 - Column-wise Peres
        6 - Column-wise VNC
        7 - Compare Extraction Rates for Above 7 Algorithms
    '''
    if ALG == 0:
        return Jakobsson(rolls)
    elif ALG == 1:
        return BlockwiseJakobsson(rolls, b)
    elif ALG == 2:
        return nCrExtractor(rolls)
    elif ALG == 3:
        return ShrinkingWindow(rolls)
    elif ALG == 4:
        return Halfbit(rolls)
    elif ALG == 5:
        return ColumnwisePeres(rolls)
    elif ALG == 6:
        return ColumnwiseVNC(rolls)
    else:
        probabilities = [1/(S-2)]*S
        probabilities[0] = 49.5
        probabilities[-1] = 49.5
        rolls = random.choices(list(range(S)),weights=probabilities,k=N)
        
        print(str(S)+'-sided die with probabilities:', probabilities)
        print('No. Rolls:', N)
        print('\n')
        rolls_copy = list(rolls)
        start = time()
        print('Jakobsson/Juels')
        print('\tBits Extracted:', len(Jakobsson(rolls_copy)))
        print('\tTime Elapsed:', str(time()-start)+'s')

        rolls_copy = list(rolls)
        start = time()
        print('Blockwise Jakobsson/Juels')
        print('\tBits Extracted:', len(BlockwiseJakobsson(rolls_copy, b)))
        print('\tTime Elapsed:', str(time()-start)+'s')

        rolls_copy = list(rolls)
        start = time()
        print('nCr Extractor')
        print('\tBits Extracted:', len(nCrExtractor(rolls_copy)))
        print('\tTime Elapsed:', str(time()-start)+'s')

        rolls_copy = list(rolls)
        start = time()
        print('Shrinking Window')
        print('\tBits Extracted:', len(ShrinkingWindow(rolls_copy)))
        print('\tTime Elapsed:', str(time()-start)+'s')

        rolls_copy = list(rolls)
        start = time()
        print('Halfbit')
        print('\tBits Extracted:', len(Halfbit(rolls_copy)))
        print('\tTime Elapsed:', str(time()-start)+'s')

        rolls_copy = list(rolls)
        start = time()
        print('Column-wise Peres')
        print('\tBits Extracted:', len(ColumnwisePeres(rolls_copy)))
        print('\tTime Elapsed:', str(time()-start)+'s')
        
        rolls_copy = list(rolls)
        start = time()
        print('Column-wise VNC')
        print('\tBits Extracted:', len(ColumnwiseVNC(rolls_copy)))
        print('\tTime Elapsed:', str(time()-start)+'s')
        return ''


if __name__ == '__main__':
    parser = argparse.ArgumentParser('DNA Sequencing TRNG')
    parser.add_argument('--i', type=str, help='Input File (.fastq)')
    parser.add_argument('--o', type=str, default='ExtractedBits.txt', help='Output File')
    parser.add_argument('--b', type=int, default=10000, help='Block Size (for Blockwise Jakobsson, ALG=1)')
    parser.add_argument('--S', type=int, default=16, help='No. sides of die (for comparing algorithms, ALG=7)')
    parser.add_argument('--N', type=int, default=10000, help='No. of rolls of die (for comparing algorithms, ALG=7)')
    parser.add_argument('--ALG', type=int, default=0)
    args = parser.parse_args()
    ALG = args.ALG
    b = args.b
    S = args.S
    N = args.N
    rolls = []
    if ALG != 7:
        input_file = open(args.i,'r')
        strands = input_file.readlines()[1::4]
        input_file.close()
        sorted_strands = SortedSet(strands)
        rolls = [sorted_strands.index(s) for s in strands]

    start = time()
    extracted_bits = extract_bits(rolls)
    end = time()
    
    if ALG != 7:
        output_file = open(args.o,'w')
        output_file.write(extracted_bits)
        output_file.close()
        print('No. Sequences:', len(strands))
        print('No. Bits Extracted:', len(extracted_bits))
        print('Time Elapsed:', str(end-start)+' s')
    
    
    
