import sys
import math

if len(sys.argv) < 3:   # if there are less then 2 arguments (Excluding the program itself)
    print("Please specify 'input.txt output.txt' as arguments")
    exit(0)
if len(sys.argv) > 3:   # if there are greater then 2 arguments (Excluding the program itself)
    print("You can specify only 3 arguments")
    exit(0)

data = open(sys.argv[1], "r")

data_list = data.readlines()  # to read from files
doc_list = []  # to store the documents in order to calculate it.
words_list = []
documents = []
for line in data_list:
    splitted_line = line.strip().split("\t")
    documents.append(",".join(splitted_line[1:len(splitted_line)])) # occurrences ( documents )
    words_list.append(splitted_line[0]) # words used
    for i in range(1, len(splitted_line)):
        if splitted_line[i] not in doc_list:    # add every document into list ( non - repeating )
            doc_list.append(splitted_line[i])   # this list is used to calculate the number of documents used

print(doc_list)
N = int(len(doc_list))  # number of documents
print(N)
occurancies = []

for i in range(0, len(words_list)): # creating len(word_list) * N matrix
    occurancies.append([0]* (N))    # initiallizing every element with 0

for i in range(0, len(words_list)): # filling the occurrances list with documents values
    docs = documents[i].split(',')
    for j in range(0, len(docs)):
        index = int(docs[j][1]) - 1
        occurancies[i][index] = 1
    print(occurancies[i])
Ni = []

for i in range(0, len(words_list)): # calculating Ni for each word in the document
    sum = 0
    for j in range(0, len(occurancies[i])):
        sum = sum + occurancies[i][j]
    Ni.append(sum)

term_frequency = occurancies    # creating matrix for term frequency( to get same size ), values will be changed later

maxFreq = []
# print()
def sumColumn(m, column):   # calculating the max frequency
    total = -1
    for row in range(len(m)):
        total = max(total, m[row][column])
    return total

for j in range(0,N):
    maxFreq.append(sumColumn(occurancies, j)) # creating an array with max frequency
print()
for i in range(0, len(words_list)):
    for j in range(0, len(occurancies[i])):
        term_frequency[i][j] = occurancies[i][j] / maxFreq[j]   # find TF by dividing each occurrence with max freq of document.
    print(term_frequency[i])
IDF = []
for ni in Ni:
    IDF.append(math.log10(N / ni))  # calculating IDF from N and Ni

print(IDF)
TF_IDF = term_frequency
for i in range(0, len(words_list)):
    for j in range(0, len(occurancies[i])):
        TF_IDF[i][j] = round(term_frequency[i][j] * IDF[i], 3)  # calculating TF.IDF
    print(TF_IDF[i])
output_file = open(sys.argv[2], "w")
output_file.write("\t\t")
for i in range(0, N):
    output_file.write("D" + str(i + 1)) # writing document number into the file ( heading )
    if i != N - 1:
        output_file.write("\t")
output_file.write("\n")
for i in range(0, len(words_list)):
    output_file.write(words_list[i] + "\t") # writing the word in the file
    for j in range(0, len(occurancies[i])):
        output_file.write(str(TF_IDF[i][j]))    # writing the TF.IDF for that word for each document in the file
        if j != len(occurancies[i]) - 1:    # if not last element of line, put \t
            output_file.write("\t")
    if i != len(words_list) - 1:    # if not last line put \n
        output_file.write("\n")

output_file.close()
