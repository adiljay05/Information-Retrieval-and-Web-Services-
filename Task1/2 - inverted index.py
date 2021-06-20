import sys


if len(sys.argv) < 3:   # if there are less then 2 arguments (Excluding the program itself)
    print("Please specify 'input.txt output.txt' as arguments")
    exit(0)
if len(sys.argv) > 3:   # if there are greater then 2 arguments (Excluding the program itself)
    print("You can specify only 3 arguments")
    exit(0)
print(str(sys.argv))

data = open(sys.argv[1], "r")   # open the input file

data_list = data.readlines()    # read data from it

splitted_data = []

for line in data_list:
    line = line.strip()
    splitted_data.append(line.split("\t"))  # split on the basis of tabs

document = []
words = []
for line in splitted_data:  # for every row in the data
    for w in line[1].split(" "):    # for every word in a row/line
        document.append(line[0])    # append document in a separate list
        words.append(w) # append the word in a separate list


final_words = []
final_documents = []
for i in range(0, len(words)):
    str = document[i]
    for j in range(i + 1, len(words)):
        if words[i] == words[j]:    # find repeatative word
            str += "\t" + document[j]   # and combine its documents occurrence list
    final_words.append(words[i])    # -> see the comment and working below for detail
    final_documents.append(str)
output_file = open(sys.argv[2], "w")

final_words1 = []
final_documents1 = []
for i in range(0, len(final_words)):    # removing the extra words ( which were repeated in other documents )
    if final_words[i] not in final_words1:
        final_words1.append(final_words[i])
        final_documents1.append(final_documents[i])

final_documents = final_documents1
final_words = final_words1
for i in range(0, len(final_words)):
    print(final_words[i] + "  \t\t" + final_documents[i])
    output_file.write(final_words[i]+"\t"+final_documents[i])   # write the word and occurrence list tab separated in file
    if i != len(final_words) - 1:
        output_file.write("\n")
output_file.close()
