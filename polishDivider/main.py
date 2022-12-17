# Rules
rulesA = {
    "VO[GLOFSNC]V": "V-OCV", 
    "VF[GLOFSNC]V": "V-FCV",
    "VS[GLOFN]V": "V-SCV", # except where C=S
    "V[GLOFSNC]GV": "V-CGV", 

    "VOO[GLOFSN]V": "V-OOCV",
    "VFFGV": "V-FFGV"
}
rulesB = {
    "VV" : "V-V",
    "VCV" : "V-CV",
    "VCCV" : "VC-CV",
    "VCCCV" : "VC-CCV",
    "VCCCCV" : "VC-CCCV",
    "VCCCCCV" : "VCC-CCCV",
    "VCCCCCCV" : "VCC-CCCCV"
}

# Remove punctuation
RMFROMTEXT = [".", ",", "?", "'", "!", ":", ";", "„", "“", "(", ")", "[", "]", "{", "}", "`", "£", "$", "%", "^", "&", "*", "+", "-"]

# Create new list using CV formalism:
# Constants
letter_division = {
    "V" : ("a", "ą", "e", "ę", "i", "o", "ó", "u", "y"), # Vowels
    "G" : ("j", "ł"), # Glides
    "L" : ("l", "r"), # Liquids
    "O" : ("p", "t", "k", "b", "d", "g", "q", "x"), # Occlusives
    "F" : ("dz", "dż", "f", "cz", "c", "ć", "dź", "z", "ź", "ż", "w", "h", "v", "ch", "rz"), # Fricatives
    "S" : ("ś", "s", "sz"), # Fricatives
    "N" : ("n", "ń", "m"), # Nasals
}
list_of_double_letters = ["dz", "dż", "cz", "dź", "sz", "rz", "ch"]
#--- end of rules and vars

import sylUtils

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
    if word not in RMFROMTEXT:
        CVword, i = "", 0
        while i < len(word):
            if i < len(word)-1 and (word[i] + word[i+1]) in list_of_double_letters:
                indexesOfDoubleLetters = [word.index(letter) for letter in list_of_double_letters if letter in word]
                indexesOfDoubleLetters.sort()
                dict_words_with_dbl_let[str(k)] = (word, indexesOfDoubleLetters)

                CVword = CVword + sylUtils.getCorespondingLetter(word[i] + word[i+1], letter_division)
                i += 2
                continue
            elif i < len(word)-1 and word[i] == "i" and word[i+1] in letter_division["V"]:
                CVword = CVword + "C" # if special "ie" case than pass a consonant instead of vocal
            else:
                CVword = CVword + sylUtils.getCorespondingLetter(word[i], letter_division)
            i += 1
        list_of_words_in_CV_notation.append(CVword)
    else:
        list_of_words_in_CV_notation.append(word)


import re

# Checking for patterns and applying changes
for i in range(len(list_of_words_in_CV_notation)):
    if list_of_words_in_CV_notation[i] not in RMFROMTEXT: # avoid interpunctions
        # Have to repeat twice because of overlaping occurances
        # First pass VCVCVCV will find two VCV occurances not 3
        # Second pass V-CVCV-CV will find the last VCV 
        for _ in range(2):
            print(list_of_words_in_CV_notation[i])
            for searchPattern in rulesA.keys(): # Check for patterns in a word
                if len(re.findall(searchPattern, list_of_words_in_CV_notation[i])) > 0: # if a match exists
                    # Substitute the pattern found with the respective string from the *rules object 
                    list_of_words_in_CV_notation[i] = re.sub(searchPattern, rulesA[searchPattern], list_of_words_in_CV_notation[i])
        list_of_words_in_CV_notation[i] = re.sub("[GLOFSN]", "C", list_of_words_in_CV_notation[i]) # Transform consonants [GLOFSN] to C

        for _ in range(2):
            print(list_of_words_in_CV_notation[i])
            for searchPattern in rulesB.keys(): # Check for patterns in a word
                if len(re.findall(searchPattern, list_of_words_in_CV_notation[i])) > 0: # if a match exists
                    # Substitute the pattern found with the respective string from the *rules object 
                    list_of_words_in_CV_notation[i] = re.sub(searchPattern, rulesB[searchPattern], list_of_words_in_CV_notation[i])
                    

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

if choice == 3:
    with open('./output/test_output.txt', 'w') as f:
        for item in entry_text_copy:
            # write each item on a new line
            f.write("%s\n" % item)

print("\nOutput writen to file -> './syllableSplitOutput.txt' in your current directory\n")

