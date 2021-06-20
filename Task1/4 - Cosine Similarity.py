import math
import sys

def cosine_similarity(D1, D2):
    # compute cosine similarity of D1 to D2: (D1 dot D2)/{||D1||*||D2||)
    xx = 0
    xy = 0
    yy = 0
    for i in range(0,len(D1)):
        x = D1[i]
        y = D2[i]
        xx += x * x     # multiply x value with itself and add result into xx
        yy += y * y     # multiply y value with itself and add result into xx
        xy += x * y     # multiply x and value with itself and add result into xy
    return xy / math.sqrt(xx * yy)

data = open(sys.argv[1], "r")   # open the file

doc_1 = int(sys.argv[2][1])     # get the document 1 to find similarity
doc_2 = int(sys.argv[3][1])     # get the document 2 to find similarity

data_list = data.readlines()    # read input from the file

splitted_line = []

document1_list = []
document2_list = []
occurancies = []

for i in range(1, len(data_list)):  # for every line of the list
    document1_list.append(float(data_list[i].strip().split("\t")[doc_1])) # append the TF.IDF value of each word against 1st document
    document2_list.append(float(data_list[i].strip().split("\t")[doc_2])) # append the TF.IDF value of each word against 2nd document

print(document1_list)
print(document2_list)

print(round(cosine_similarity(document1_list,document2_list),3))    # get and print cosine similarity from the above function