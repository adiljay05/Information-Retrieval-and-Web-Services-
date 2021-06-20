from porterStemmer import PorterStemmer
import sys


# function to remove punctuation
def remove_punctuation_and_numbers(line):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~1234567890'''  # these symbols and characters will be removed
    no_punct = ""
    for char in line:
        if char not in punctuations:  # if character is not in the list
            no_punct = no_punct + char  # add it to the new string
    return no_punct  # returning string without punctuations


# function to search and element in the list
def search_element_in_list(stop_words, element):
    for w in stop_words:
        if w.strip() == element.strip():  # remove the extra whitespaces and then compare
            return True
    return False

# remove stop word from a list
def remove_stop_words(regular_words, stop_words):
    after_stop_words = ""   # get an empty strin
    for w in regular_words: # for evey word
        if not search_element_in_list(stop_words, w):   # if word is not already present in the string
            after_stop_words += w + " " # add it to the string
    return after_stop_words.strip() # return the new string


if len(sys.argv) < 4:   # if there are less then 3 arguments (Excluding the program itself)
    print("Please specify 'input.txt output.txt stopwords.txt' as arguments")
    exit(0)
if len(sys.argv) > 4:   # if there are greater then 3 arguments (Excluding the program itself)
    print("You can specify only 3 arguments")
    exit(0)
print(str(sys.argv))

# Step 1: Gathering Document
data = open(sys.argv[1], "r")   # open input file
stop_words_file = open(sys.argv[3], "r")    # open stop words file

stop_words_list = stop_words_file.read()    # read stop words
stop_words = stop_words_list.split(",") # split and convert them into array

data_list = data.readlines()    # read the data from data file

splitted_data = []

for line in data_list:
    splitted_data.append(line.split("\t"))  # split document from words

print("\nGathered Data\n==========================================")
print(splitted_data)

# Step 2: Tokenization (removing punctuations, numbers and lower casing the alphabets
for line in splitted_data:
    line[1] = line[1].strip()  # removing \n from the lines
    line[1] = remove_punctuation_and_numbers(line[1])  # removing the punctuation and numbers
    line[1] = line[1].lower()  # converting to lower case

print("\nTokenized data\n==========================================")
print(splitted_data)

# Step 3: Removing stop words
for line in splitted_data:
    line[1] = remove_stop_words(line[1].split(" "), stop_words)

print("\nRemoved Stopwords Data\n==========================================")
print(splitted_data)

# Step 4: Stemming
p = PorterStemmer() # perter stemmer library is used

for line in splitted_data:  # for evey line in the words list against all the documents
    words = line[1].split(" ")  # split words by space
    new_line = ""
    for w in words: # for every word in the list of words
        new_line += p.stem(w.strip(), 0, len(w) - 1) + " " # call the stem function
    line[1] = new_line.strip() # remove the last space and store them back
print("\nStemmed Data\n==========================================")
print(splitted_data)
# print(stop_words)
file1 = open(sys.argv[2], "w")  # open the output file
i = 0
for line in splitted_data:  # for every line
    file1.write(line[0] + "\t") # write the document number
    file1.write(line[1])    # then write the words against that document
    if i != len(splitted_data) - 1: # place \n only if the document is not the last document
        file1.write("\n")
    i = i + 1

file1.close()   # close the file
