from porterStemmer import PorterStemmer
import sys
import math


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
    after_stop_words = ""  # get an empty strin
    for w in regular_words:  # for evey word
        if not search_element_in_list(stop_words, w):  # if word is not already present in the string
            after_stop_words += w + " "  # add it to the string
    return after_stop_words.strip()  # return the new string


def remove_repetative_words_in_a_document(document):  # removing repeated words in a list
    list_ = []
    for d in document:
        if d not in list_:
            list_.append(d)
            print(list_)
    return list_


# Step 1: Gathering Document
data = open(sys.argv[1], "r")  # opening input file

stop_words_list = "a, for, many, of, at, as, each, past, the, on, is,was, will, who, and"
stop_words = stop_words_list.split(",")

data_list = data.readlines()  # reading data from input file

splitted_data = []

for line in data_list:
    splitted_data.append(line.lower().split("\t"))  # converting the data to lower case and then splitting

# Step 2: Tokenization (removing punctuations, numbers and lower casing the alphabets
for line in splitted_data:
    line[1] = line[1].strip()  # removing \n from the lines
    line[1] = remove_punctuation_and_numbers(line[1])  # removing the punctuation and numbers
    line[1] = line[1].lower()  # converting to lower case

# Step 3: Removing stop words
for line in splitted_data:
    line[1] = remove_stop_words(line[1].split(" "), stop_words)

# Step 4: Stemming
p = PorterStemmer()

for line in splitted_data:
    words = line[1].split(" ")
    new_line = ""
    for w in words:
        new_line += p.stem(w.strip(), 0, len(w) - 1) + " "
    line[1] = new_line.strip()

# ====================================  Preprocessing Done  =========================================

document = []
words = []
for line in splitted_data:
    for w in line[1].split(" "):
        document.append(line[0])
        words.append(w)
# 5 Indexing
final_words = []
final_documents = []
for i in range(0, len(words)):
    str1 = document[i]
    for j in range(i + 1, len(words)):
        if words[i] == words[j]:  # find repeatative word
            str1 += "\t" + document[j]  # and combine its documents occurrence list
    final_documents.append(words[i] + "\t" + str1)

# ====================================  Indexing Done  =========================================

doc_list = []  # to store the documents in order to calculate number of documents N.
words_list1 = []
words_list = []
documents = []
for line in final_documents:
    splitted_line = line.strip().split("\t")
    words_list1.append(splitted_line[0])  # 1st columns is list of words
    documents.append(",".join(splitted_line[1:len(splitted_line)]))  # rest are the documents

for i in range(0, len(words_list1)):
    if words_list1[i] not in words_list:  # to get non-repeated list of words along with documents
        words_list.append(words_list1[i])
        doc_list.append(documents[i])

distinct_doc_list = []
for i in doc_list:
    s = i.split(",")
    for j in s:
        if j not in distinct_doc_list:  # to find distinct documents used
            # print(distinct_doc_list)
            distinct_doc_list.append(j)

N = int(len(distinct_doc_list))  # number of documents

occurancies = []

for i in range(0, len(words_list)):
    occurancies.append([0] * (N))  # creating occurrence matrix of size N*len(word_size)

for i in range(0, len(words_list)):
    docs = doc_list[i].split(',')
    for j in range(0, len(docs)):
        index = int(docs[j][1]) - 1
        occurancies[i][index] = occurancies[i][index] + 1  # storing the occurrence of each word in documents

Ni = []
maxFreq = []


# print()
def maxFrequency(m, column):  # get max frequency of a column ( Document occurrence)
    total = -1
    for row in range(len(m)):
        total = max(total, m[row][column])
    return total


for j in range(0, N):
    maxFreq.append(maxFrequency(occurancies, j))  # call the above function for each document

for i in range(0, len(occurancies)):
    sum = 0
    for j in range(0, len(occurancies[i])):
        if occurancies[i][j] != 0:
            sum = sum + 1
    Ni.append(sum)  # storing the number of documents in which the term is non-zero zero

term_frequency = occurancies  # creating exact size matrix for term frequency

for i in range(0, len(words_list)):
    for j in range(0, len(occurancies[i])):  # for each docuemnt
        term_frequency[i][j] = round(occurancies[i][j] / maxFreq[j],
                                     3)  # dividing occurrence with max freq to get term frequency

IDF = []
for ni in Ni:
    IDF.append(math.log10(N / ni))  # divide number of document with Number of appearance to get iDF

TF_IDF = term_frequency
for i in range(0, len(words_list)):
    for j in range(0, len(occurancies[i])):
        TF_IDF[i][j] = round(term_frequency[i][j] * IDF[i], 3)  # multiply IDF column with TF column

# ====================================  TF_IDF Done  =========================================

# doing query preprocessing until stemming and removing repetative words

query_words = sys.argv[2]  # get the query from command line
query_words = remove_punctuation_and_numbers(query_words)
query_words_list1 = query_words.split(" ")
query_words_list1 = remove_stop_words(query_words_list1, stop_words).lower()
query_words_list1 = query_words_list1.split(" ")
query_words_list1 = remove_repetative_words_in_a_document(query_words_list1)

query_words_list = []
for word in query_words_list1:
    query_words_list.append(p.stem(word, 0, len(word) - 1))
query_words_list = remove_repetative_words_in_a_document(query_words_list)

# ===============================  Query Preprocessing Done  ===================================

query_term_frequency = []
for i in range(0, len(words_list)):
    query_term_frequency.append(0)  # initiallizing query list of size equal to number of words with zeros

for i in range(0, len(words_list)):
    for j in range(0, len(query_words_list)):
        if words_list[i] == query_words_list[j]:  # if the word is found in query list
            query_term_frequency[i] += 1  # increment the query term frequency

query_TF_IDF = [0] * len(words_list)    # creating and initiallizing the query_TF_IDF list with zeros

for i in range(len(words_list)):
    query_TF_IDF[i] = round(query_term_frequency[i] * IDF[i], 3)    # finding the query TF_IDF


def sumProductTerms(m, n, column):  # will return the sum product of the terms -> used to find length of TF_IDF
    total = 0
    for row in range(len(m)):
        total += m[row][column] * n[row][column]
    return total


lenght_of_TF_IDF = []
sum_product_of_TF_IDF = []
for j in range(0, N):
    sum_product_of_TF_IDF.append(sumProductTerms(TF_IDF, TF_IDF, j))    # sum product returned
    lenght_of_TF_IDF.append(round(math.sqrt(sum_product_of_TF_IDF[j]), 3))  # taking square root of sumProduct to get length


def sumProductForQuery(m):  # it will find the sum product of query TF_IDF -> will be used to get query length
    total = 0
    for row in range(len(m)):
        total += m[row] * m[row]
    return total


sum_product_of_query_TF_IDF = sumProductForQuery(query_TF_IDF)  # sumProduct of Query_TF_IDF
lenght_of_query_TF_IDF = round(math.sqrt(sum_product_of_query_TF_IDF), 3)   # length of Query_TF_IDF

print(lenght_of_query_TF_IDF)


def sumProductForQueryRating(m, n, column): # finding sumProduct for query rating.
    total = 0.0
    for row in range(len(m)):
        total = total + (float(m[row][column]) * float(n[row]))
    return total


sum_product_of_query = []
for i in range(0, N):
    sum_product_of_query.append(sumProductForQueryRating(TF_IDF, query_TF_IDF, i))  # returned sumProduct for query rating

lengths_list = []
for i in range(0, N):
    lengths_list.append(lenght_of_query_TF_IDF * lenght_of_TF_IDF[i])   # length for query_rating

rating = []
flag = True
for i in range(0, N):
    try:
        rating.append(["D" + str(i + 1), round(sum_product_of_query[i] / lengths_list[i], 2)])  # divide sumProduct by length to get Query Rating
    except: # it will execute if the term is not found in the list
        print("Query Document Not found in the document list: " + str(i + 1))
        flag = False
if not flag:
    for i in range(0, N):   # if the term was not found, print 0,0 as rating.
        print("D" + str(i + 1) + "\t" + str(0.0))
    exit(0)
rating.sort(key=lambda x: x[1], reverse=True)   # sort the rating list as it was mentioned in the task

for i in range(0, N):
    print(rating[i][0] + "\t" + str(rating[i][1]))  # printing the query rating
