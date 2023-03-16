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

filename = input("File name: ")
k = int(input("k: "))
file = open(filename, 'r')
outputfilename = input("Output file name:")
bitstreams = {i:[] for i in range(1,k+1)}
content = file.readlines()
for i in tqdm(range(len(content[0]))):
    bitstreams[(i%k)+1].append(content[0][i])

result = []
for i in tqdm(range(1,k+1)):
    result += amls_round(bitstreams[i])
outputfile = open(outputfilename, 'w')
outputfile.write(''.join(result))

