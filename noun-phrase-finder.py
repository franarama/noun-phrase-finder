####################################################################
#                       FRANCESCA RAMUNNO                          #
#                           T00053082                              #
#                          Homework #3                             #
#                         COMP 4980-04                             #
#                                                                  #                                                           #
# This program takes input for a file name and a number N,         #
#  which will be used to get the top-N frequencies of              #
# each occurence of each sequence type found in the given file.    #
# Furthermore, this program will take all occurences found         #
# and place them in a text file called all_occurences.txt with the #
# sequence type at the top, followed by the occurences of that type.#
# (If you are interested in that information....)                   #
#                                                                  #
# It also prints out the number of times each sequence type occurs.#
# (of course)                                                      #
#                                                                  #
# For basic stats, I printed the token count, the sentence count,  #
#  N and the number of noun phrases found.                         #
#  Nothing else really seemed that relevant.                       #
#                                                                  #
# It is required to have Texttable module installed to run this    #
# program.                                                         #
#                                                                  #
####################################################################

import nltk as nltk
from texttable import Texttable
from nltk import *

# get user input for an existing file
def file_input(message):
    file = input(message)
    if os.path.isfile(file):
        return file
    else:
        return file_input('Enter an existing file path: ')

def get_sequences(pos_tag_sentence, nouns, adjectives):
    i = 0
    found_sequences = []
    master_tag_sequence = []  # this will keep track of the tag sequences found
    #print("SENTENCE=", pos_tag_sentence)
    while i < len(pos_tag_sentence):

        # GET THE TUPLE eg) [('We'),('PRP')]
        pair = pos_tag_sentence[i]
        # GET THE WORD eg) 'We'
        word = pair[0]
        # GET THE WORD TYPE eg) 'PRP'
        tag = pair[1]

        index = 0

        # If the word type is a determiner..
        if tag == "DT":
            # if it is the last element of the sentence
            if i == (len(pos_tag_sentence) - 1):
                break
            else:

                j = i+1

                # get the next tuple and word type
                next_pair = pos_tag_sentence[j]
                next_tag = next_pair[1]
                # append to this each time to get the full sequence of words
                to_add = []
                tag_sequence = []

                #--- 2 CASES: Next word after determiner can be 1) an adjective or 2) a noun ---#

                # CASE 1: the word is an adjective
                if next_tag in adjectives:
                    index = j
                    to_add = [word]
                    tag_sequence = ["DT"]
                    # keep going until there are no more adjectives
                    while next_tag in adjectives:
                        tag_sequence.append("ADJ")
                        if index == len(pos_tag_sentence) - 1:
                            # dont add if the determiner adjective* not followed by a noun, get out
                            break
                        else:
                            to_add.append(pos_tag_sentence[index][0])
                            index = index + 1
                            next_tag = pos_tag_sentence[index][1]
                # CASE 2: the word is a noun
                if next_tag in nouns:
                    # if there was adjectives start where the adjectives stopped
                    if index > 0:
                        start_index = index
                    # otherwise start at the determiner
                    else:
                        start_index = j
                    # if adjectives havent already done it, put the determiner into the to add list.
                    if len(to_add) == 0:
                        to_add = [word]
                        tag_sequence = ["DT"]
                    while next_tag in nouns:
                        tag_sequence.append("NOUN")
                        if start_index == len(pos_tag_sentence) - 1:
                            # if we are at the end of the sentence, add the sequence and get out
                            to_add.append(pos_tag_sentence[start_index][0])
                            break
                        # otherwise, add it and keep going
                        to_add.append(pos_tag_sentence[start_index][0]) # add word to sequence
                        start_index = start_index + 1
                        next_tag = pos_tag_sentence[start_index][1] # get the next word type
                    found_sequences.append(to_add)
                    master_tag_sequence.append(tag_sequence)
        i = i + 1
    return found_sequences,master_tag_sequence

# get the file to read
print("")
file = file_input("Enter a file path: ")
print("")
# get N
n = input("Enter a value between 1 and 10 for N: ")
n = int(n)
if n < 1 or n > 10:
    while n < 1 or n > 10:
        n = int(input("Please re-enter. Value must be between 1 and 10: "))

print("")
print("FOR FILE: ",file)
print("")

# open the file for reading
file = open(file).read()

print("TOKEN COUNT =", len(nltk.word_tokenize(file)))
sent_tokenize = nltk.sent_tokenize(file)

# get rid of the newline characters
sent_tokenize = [each.replace('\n',' ') for each in sent_tokenize]

print("SENTENCE COUNT =", len(sent_tokenize))
print("N =",n)

word_tokenize = [nltk.word_tokenize(sent) for sent in sent_tokenize]


pos_tag = [nltk.pos_tag(word) for word in word_tokenize]

#    -- NOW THE ACTUAL ASSIGNMENT --    #

# FIND FREQUENCIES OF SIMPLE NOUN PHRASES OF THIS FORM: #
# determiner adjective* noun+ #
# so 0 or more adjectives and 1 or more noun #

# in the pos tagger, things we care about:
# JJ - adjective, NN - noun, DT - determiner
# JJR - comparative adjective, JJS - superlative adjective, NNP - proper noun
# NNS - common noun

adjectives = ["JJ","JJR","JJS"]
nouns = ["NNP","NNS","NN","NNPS"]
dict = {}
table = Texttable()
table.add_row(["Sequence type","Sequnce Frequency","Top N Most Frequent Occurences"])

for sentence in pos_tag:
    # get the sequences occurences with the corresponding tag type
    sentences,tags= get_sequences(sentence,nouns,adjectives)
    i = 0
    # create a dictionary with the tags as keys and the occurences as values
    for part in sentences:
        tag_string = " ".join(str(x) for x in tags[i])
        if tag_string in dict:
            dict[tag_string].append(part)
        else:
            dict[tag_string] = []
            dict[tag_string].append(part)
        i = i + 1

# we will write the occurences to a file, along with the sequence type
to_write = open("all_occurences.txt","w")
total_count = 0

# go through the dictionary to write to the file,
# and count the frequences, and get the top N frequencies
for key,value in dict.items():
    total_count = total_count + len(value)
    freq_count = 0
    sent_str = ""
    checked_vals = []
    # create another dictionary with the tags as keys and their frequencies as values
    val_frequencies = {}
    for val in value:
        freq_count = freq_count + 1
        val_str = ""
        for word in val:
            val_str = val_str + " " + word
        if val not in checked_vals:
            checked_vals.append(val)
            val_frequencies[val_str] = 1
            for word in val:
                sent_str = sent_str + " " + word
            sent_str = sent_str + "\n"
        else:
            val_frequencies[val_str] = val_frequencies[val_str] + 1
    # sort the dictionary and get the top n
    top_n = sorted(val_frequencies.items(), key=lambda x: x[1], reverse=True)[:n]
    top_n_str = ""
    for entry in top_n:
        top_n_str = top_n_str + entry[0] + " : " + str(entry[1]) + " time(s)" + "\n"

    table.add_row([key,freq_count,top_n_str])

    to_write.write(key)
    to_write.write("\n")
    to_write.write(sent_str)
    to_write.write("\n")

to_write.close()
print("TOTAL NOUN PHRASES FOUND = ", total_count)
print("")
print("FILE CREATED CALLED all_occurences.txt CONTAINING SEQUENCE TYPES AND ALL UNIQUE OCCURENCES.")
print("")
print("Note that DT=determiner, Adj=adjective, and Noun=noun(of course)")
table.align = "l"
print(table.draw())




