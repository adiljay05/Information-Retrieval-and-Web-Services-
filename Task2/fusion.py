import io

historic_results_csv = input("What is the name of historic results csv file?  ")
historic_results_csv_dictionary = {}
query_rating_dictionary = {}
doc_rating_dictionary = {}
max_query_dictionary = {}
segment_length = 0
segments = 0
try:
    print("\nFile " + historic_results_csv + " contains following data\n")
    csv = io.open(historic_results_csv, "r", encoding='utf-8-sig')
    for row in csv:
        # skipping 3rd word as it is comma and last word is next line char
        historic_results_csv_dictionary[row[0:2]] = row[3:-1]  # 0:2 values are the keys of this hashmap
        print(row)
except:
    print("File " + historic_results_csv + " not found")
input("Press Enter to continue...")
# ask user to set segments for dividing historic results data
segments = input("How many segments to use? enter 0-99  ")
try:
    segments = int(segments)
except:
    print("Enter integer only")
# iterate over hr csv file
for key in historic_results_csv_dictionary:
    historic_results_csv_dictionary_array = historic_results_csv_dictionary[key].split(",")
    # find length of each segment by dividing total number of results in a query by segments user wants
    segment_length = int(len(historic_results_csv_dictionary_array) / segments)
    print("Segment length = " + str(segment_length))
    c = 0  # count total results
    r = 0  # store number of R in a segment
    k = 0  # store k value of each segment
    for result in historic_results_csv_dictionary_array:
        if result == 'R':
            r = r + 1  # if Relevant then increment r value
        c = c + 1  # increment c value at each iteration
        if c == segment_length:
            # calculate rating by dividing total number R by total number of results in a segment
            doc_rating = r / c
            k = k + 1
            # store rating in a dict
            # store in format AK2 = rating where A is engine name, K is segment and 2 is second segment
            rating_dict_key = str(k) + "K" + key[0]  # IF key is B2 then key[0] = B
            if rating_dict_key not in query_rating_dictionary:  # if rating not already present, add it
                query_rating_dictionary[rating_dict_key] = doc_rating
            else:  # if the rating is already present, add to previous rating
                query_rating_dictionary[rating_dict_key] += doc_rating
            max_query_dictionary[key[0]] = int(key[1])  # it will store engine name and max query
            # if c is equal to segment length then reset c and r
            c = 0
            r = 0

for key in query_rating_dictionary:
    # as last element of key is engine name which is key of max_query_dictionary
    query_rating_dictionary[key] /= max_query_dictionary[key[-1]]
# now we divide rating by segment number e.g. in 5KA = 1.5, 5 is segment number hence 1.5/5 = 0.3
for key in query_rating_dictionary:
    try:
        segment_number = int(list(filter(str.isdigit, str(key)))[0])  # extract 1st digit
        segment_number = segment_number * 10 + int(list(filter(str.isdigit, key))[1])  # extract second digit
    except Exception as e:
        segment_number = int(list(filter(str.isdigit, str(key)))[0])  # extract 1st digit if no second digit
    # print("Segment number: " + str(segment_number))
    rating = query_rating_dictionary[key]
    query_rating_dictionary[key] = rating / segment_number

# print()

live_results_csv = input("What is the name of live results csv file?  ")
# open csv file with utf-8 encoding which removes BOM character
live_results_csv_dictionary = {}
try:
    print("\nFile " + live_results_csv + " contains following data\n")
    csv = io.open(live_results_csv, "r", encoding='utf-8-sig')
    for row in csv:
        # index '1' contains comma so skip it
        live_results_csv_dictionary[row[0]] = row[2:-1] # engine name is key, 3rd to last word are documents
    # print(row)
except Exception as e:
    print("File " + live_results_csv + " not found")
print("Rating Dictionary: ")
print(query_rating_dictionary)
print("Live result file: ")
print(live_results_csv_dictionary)

print()  # blank space
# ask user to provide engine results to be fused
fusion_input = input("What results to be fused out of A, B, C or D enter engine name comma seperated  ")
fusion_array = fusion_input.split(",")
# assign rating for each document in live result csv file by using query_rating_dictionary
for engine in live_results_csv_dictionary:
    if engine in fusion_array:
        live_results_csv_dictionary_array = live_results_csv_dictionary[engine].split(",")
        k = 1  # counter for segment number
        c = 1  # counter to count number of doc
        for doc in live_results_csv_dictionary_array:
            # create key using engine number counter
            rating_dict_key = str(k) + "K" + engine
            if doc not in doc_rating_dictionary:  # if no value for same doc found, add its value
                doc_rating_dictionary[doc] = round(query_rating_dictionary[rating_dict_key], 2)
            else:   # otherwise add to previous value
                doc_rating_dictionary[doc] = round(
                    doc_rating_dictionary[doc] + query_rating_dictionary[rating_dict_key],2)
            if c == segment_length:
                c = 1  # assign initial value to counter
                k = k + 1  # increment k if segment length reached
                if k > segments:
                    k = segments
            c = c + 1  # increment c
print("Doc and rating after fusion")
# sort dict in reverse order
ordered_list = sorted(doc_rating_dictionary.items(), key=lambda x: x[1], reverse=True)
print(ordered_list)
# write output to a file
output = open("output-" + fusion_input + "-" + str(segments) + ".txt", "w")
output.write("Rank")
output.write("\t")
output.write("Doc")
output.write("\t")
output.write("Rating")
output.write("\n")
r = 0
for doc in ordered_list:
    output.write(str(r + 1))
    output.write("\t")
    output.write(str(doc[0]))
    output.write("\t")
    output.write(str(doc[1]))
    output.write("\n")
    r = r + 1
output.close()
