print("Hello there, would you like to enter a polish text or a file containing polish text?")

while True:
    print("1. Select 1 for standard input")
    print("2. Select 2 for file path ")
    choice = input()
    try:
        choice = int(choice)
        break
    except:
        print("You entered something wrong")


import sylUtils

if choice == 1:
    print("Please write here your text: ")

    textFromStdInput = input()
else:
    while True:
        addressFromStdInput = input()
        try:
            with open(addressFromStdInput) as f:
                textFromStdInput = ' '.join([x.rstrip("\n") for x in f.readlines()])
            break
        except:
            print("No such file or directory: {}".format(addressFromStdInput))

# Remove punctuation
RMFROMTEXT = [".", ",", "?", "'", "!", ":", ";", "„", "“", "(", ")", "[", "]", "{", "}", "`", "£", "$", "%", "^", "&", "*", "+", "-"]

# Eliminate all unwanted chars
# Might change this aproach and keep but ignore the signs later
for el in RMFROMTEXT:
    textFromStdInput = sylUtils.removeInterpunct(el, textFromStdInput)

# Splittin the text on space
entryTextCopy = textFromStdInput.split()
textFromStdInput = textFromStdInput.lower().split()

# Create new list using CV formalism:
# Constants
letterDiv = {
    "V" : ("a", "ą", "e", "ę", "i", "o", "ó", "u", "y"), # Vowels
    "G" : ("j", "ł"), # Glides
    "L" : ("l", "r"), # Liquids
    "O" : ("p", "t", "k", "b", "d", "g", "q", "x"), # Occlusives
    "F" : ("dz", "dż", "f", "cz", "c", "ć", "dź", "z", "ź", "ż", "w", "h", "v"), # Fricatives
    "S" : ("ś", "s", "sz"), # Fricatives
    "N" : ("n", "ń", "m") # Nasals
}
lisOfDblLtr = ["dz", "dż", "cz", "dź", "sz"]

# List copy
textCVcopy = []
for word in textFromStdInput:
    if word not in RMFROMTEXT:
        CVword, i = "", 0
        while i < len(word):
            if i < len(word)-1 and (word[i] + word[i+1]) in lisOfDblLtr:    
                CVword = CVword + sylUtils.getCorespondingLetter(word[i] + word[i+1], letterDiv)
                i += 2
                continue
            CVword = CVword + sylUtils.getCorespondingLetter(word[i], letterDiv)
            i += 1
        textCVcopy.append(CVword)
    else:
        textCVcopy.append(word)

# Rules
rulesA = {
    "VO[GLOFSN]V": "V-OCV", 
    "VF[GLOFSN]V": "V-FCV",
    "VS[GLOFN]V": "V-SCV", # except where C=S
    "V[GLOFSN]GV": "V-CGV", 

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

import re

# Checking for patterns and applying changes
for i in range(len(textCVcopy)):
    if textCVcopy[i] not in RMFROMTEXT: # avoid interpunctions
        for searchPattern in rulesA.keys(): # Check for patterns in a word
            if len(re.findall(searchPattern, textCVcopy[i])) > 0: # if a match exists
                # Substitute the pattern found with the respective string from the *rules object 
                textCVcopy[i] = re.sub(searchPattern, rulesA[searchPattern], textCVcopy[i])

        textCVcopy[i] = re.sub("[GLOFSN]", "C", textCVcopy[i]) # Transform consonants [GLOFSN] to C

        for searchPattern in rulesB.keys(): # Check for patterns in a word
            if len(re.findall(searchPattern, textCVcopy[i])) > 0: # if a match exists
                # Substitute the pattern found with the respective string from the *rules object 
                textCVcopy[i] = re.sub(searchPattern, rulesB[searchPattern], textCVcopy[i])


#outputTextSyllables = textFromStdInput.join()
for i in range(len(entryTextCopy)):
    if entryTextCopy[i] in RMFROMTEXT:
        continue
    entryTextCopy[i] = sylUtils.splitWord(entryTextCopy[i], textCVcopy[i])
    entryTextCopy[i] = ' '.join(entryTextCopy[i].split("-")) 

outputText = ' '.join(entryTextCopy)

print(outputText)
with open('./syllableSplitOutput.txt', 'w') as f:
    f.write(outputText)

print("\nOutput writen to file -> './syllableSplitOutput.txt' in your current directory\n")