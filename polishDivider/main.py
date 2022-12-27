from constants import *
from config import *
import sylUtils

debug_file = []

print("Hello there, would you like to enter a polish text or a file containing polish text?")

# input validation
while True:
    print("1. Select 1 for standard input")
    print("2. Select 2 for file path ")
    choice = input()
    try:
        choice = int(choice)
        break
    except:
        print("You entered something wrong")

if choice == 1:
    print("Please write here your text: ")

    text_from_std_input = input()
elif choice == 2:
    while True:
        address_from_std_input = input()
        try:
            with open(address_from_std_input) as f:
                text_from_std_input = ' '.join([x.rstrip("\n") for x in f.readlines()])
            break
        except:
            print("No such file or directory: {}".format(address_from_std_input))
else:
    with open("test_input.txt") as f:
        text_from_std_input = ' '.join([x.rstrip("\n") for x in f.readlines()])



# Eliminate all unwanted chars
# Might change this aproach and keep but ignore the signs later
for el in RMFROMTEXT:
    text_from_std_input = sylUtils.removeInterpunct(el, text_from_std_input)

# Splittin the text on space
entry_text_copy = text_from_std_input.split()
text_from_std_input = text_from_std_input.lower().split()



# List copy
list_of_words_in_CV_notation = []
words_with_dbl_let = [] 
dict_words_with_dbl_let = {}
for k, word in enumerate(text_from_std_input):
    if word in RMFROMTEXT:
        list_of_words_in_CV_notation.append(word)
        continue

    CVword, i = "", 0
    debug_letters = []

    while i < len(word):
        if i < len(word)-1 and (word[i] + word[i+1]) in list_of_double_letters:
            indexesOfDoubleLetters = [word.index(letter) for letter in list_of_double_letters if letter in word]
            indexesOfDoubleLetters.sort()
            dict_words_with_dbl_let[str(k)] = (word, indexesOfDoubleLetters)

            return_letter = sylUtils.getCorespondingLetter(word[i] + word[i+1], letter_division)
            CVword = CVword + return_letter
            

            if DEBUG == True:
                tmp = "input letter: " + word[i] + word[i+1] + " -> corespondingLetter: " + return_letter
                debug_letters.append(tmp)

            i += 2
            continue
        elif i < len(word)-1 and word[i] == "i" and word[i+1] in letter_division["V"]:
            CVword = CVword + "C" # if special "ie" case than pass a consonant instead of vocal

            if DEBUG == True:
                tmp = "input letter: " + word[i] + " -> corespondingLetter: C"
                debug_letters.append(tmp)
        else:
            return_letter = sylUtils.getCorespondingLetter(word[i], letter_division)
            CVword = CVword + return_letter

            if DEBUG == True:
                tmp = "input letter: " + word[i] + " -> corespondingLetter: " + return_letter
                debug_letters.append(tmp)
        i += 1
    debug_file.append(debug_letters)
    list_of_words_in_CV_notation.append(CVword)
    


import re

debug_words = []
# Checking for patterns and applying changes
for i in range(len(list_of_words_in_CV_notation)):
    if list_of_words_in_CV_notation[i] in RMFROMTEXT: # avoid interpunctions
        continue
    # Have to repeat twice because of overlaping occurances
    # First pass VCVCVCV will find two VCV occurances not 3
    # Second pass V-CVCV-CV will find the last VCV 
    debug_cv_words = []
    if DEBUG == True:
            debug_cv_words.append(list_of_words_in_CV_notation[i])
    for _ in range(2):
        print(list_of_words_in_CV_notation[i])
        for searchPattern in rulesA.keys(): # Check for patterns in a word
            if len(re.findall(searchPattern, list_of_words_in_CV_notation[i])) > 0: # if a match exists
                # Substitute the pattern found with the respective string from the *rules object 
                list_of_words_in_CV_notation[i] = re.sub(searchPattern, rulesA[searchPattern], list_of_words_in_CV_notation[i])
    if DEBUG == True:
            debug_cv_words.append(list_of_words_in_CV_notation[i])

    list_of_words_in_CV_notation[i] = re.sub("[GLOFSN]", "C", list_of_words_in_CV_notation[i]) # Transform consonants [GLOFSN] to C
    if DEBUG == True:
            debug_cv_words.append(list_of_words_in_CV_notation[i])
    for _ in range(2):
        print(list_of_words_in_CV_notation[i])
        for searchPattern in rulesB.keys(): # Check for patterns in a word
            if len(re.findall(searchPattern, list_of_words_in_CV_notation[i])) > 0: # if a match exists
                # Substitute the pattern found with the respective string from the *rules object 
                list_of_words_in_CV_notation[i] = re.sub(searchPattern, rulesB[searchPattern], list_of_words_in_CV_notation[i])
        if DEBUG == True:
            debug_cv_words.append(list_of_words_in_CV_notation[i])
    if DEBUG == True:
        debug_words.append(debug_cv_words)          

for i in range(len(entry_text_copy)):
    if entry_text_copy[i] in RMFROMTEXT:
        continue
    if str(i) in list(dict_words_with_dbl_let.keys()):
        entry_text_copy[i] = sylUtils.split_dbl_letter_word(entry_text_copy[i], list_of_words_in_CV_notation[i], dict_words_with_dbl_let[str(i)][1])
    else:
        entry_text_copy[i] = sylUtils.splitWord(entry_text_copy[i], list_of_words_in_CV_notation[i])
    entry_text_copy[i] = ' '.join(entry_text_copy[i].split("-")) 

outputText = ' '.join(entry_text_copy)

print(outputText)
with open('./output/syllableSplitOutput.txt', 'w') as f:
    f.write(outputText)

# debug file
if choice == 3:
    with open('./output/test_output.txt', 'w') as f:
        for item in entry_text_copy:
            # write each item on a new line
            f.write("%s\n" % item)

print("\nOutput writen to file -> './syllableSplitOutput.txt' in your current directory\n")

if DEBUG == True:
    with open('./output/debug.txt', 'w') as f:  
        for letters, cv in zip(debug_file, debug_words):
            for el in letters:
                f.write("%s\n" % el)
            f.write("\n")
            for el in cv:
                f.write("%s\n" % el)
            f.write("--------------\n")
