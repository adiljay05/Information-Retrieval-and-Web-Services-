Task 1:
=============================================================================================
Video Link: https://griffith.zoom.us/rec/share/eh60FCIgz0WdoqzeufkB2nUOvfWP8Pm3xrkVhcjIHN6hyMM5Lk6AuJN5uTV6QLQ.c8Q3T1VVyFT-1JXM?startTime=1620948471000
---------------------------------------------------------------------------------------------
Requirements:   python 3.6+ installed ( Coded and tested in 3.9.4 )


How to run files:
    1. Open command prompt in Task1 folder.
    2. Make sure you have correctly installed python by typing the command "python --version"
    3. Then run the following commands to see the working of each sub-part.
    4. Make sure you don't have extra whitespace in the command while copying.
       We are working with command line arugments, a single space matters.

Commands to type:
Preprocessing:      python "1 - Preprocessing.py" data1.txt output_stemming.txt stop_words.txt
Inverted Index:     python "2 - inverted index.py" output_stemming.txt output_indexing.txt
TF_IDF:             python "3 - TF-IDF.py" output_indexing.txt output_TFIDF.txt
Cosine Similarity:  python "4 - Cosine Similarity.py" output_TFIDF.txt D1 D2
IR system:          python "5 - IR System.py" data1.txt "new student"

-----------------------------------------------------------------------------------------------
Important things:
    1.  The output of 1st part is the input of 2nd part.
    2.  The output of 2nd part is the input of 3rd part.
    3.  The output of 3rd part is the input of 4th part.
    4.  The input of 1st and 5th part is same. ( raw data )