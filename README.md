# noun-phrase-finder

This program utilities nltk to find the frequencies of noun phrases of the form:

determiner adjective* noun+

so one determiner, 0 or more adjectives, and 1 or more nouns for an existing file inputted by the user. The program takes into account the different adjective and noun tags in nltk's POS-tagger.

Furthermore, this program outputs a table with the type of sequence found, sequence frequency, and the top n-most frequent occurences of this sequence (based on a user input between 1 and 10).

Output also includes basic stats about the file, such as token count, sentence count, and the total number of noun phrases found.

The program also creates a file with the sequence type, followed by all occurence of that sequence found (which is called "all_occurences.txt").
