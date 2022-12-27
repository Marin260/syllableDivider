from config import *
# Remove interpunction characters [., !, ?,...]
def removeInterpunct(elToRemoveFromStr: str, text: str):
    text = text.replace(elToRemoveFromStr, " " + elToRemoveFromStr + " ")
    return text



# Input letter -> output letter in CV notation
def getCorespondingLetter(inputLetter: str, dictOfValues: dict):
    corespondingLetter = "X" # Default values... need to change this later
    for group in dictOfValues.values():
        if inputLetter in group:
            # Get key (letter needed) by the values (values is the tupple)
            # Get value from list of dict keys
            # where index is touple in list of values
            corespondingLetter = list(dictOfValues.keys())[list(dictOfValues.values()).index(group)]
            break
    return corespondingLetter


def split_dbl_letter_word(inputWord: str, ruleToFollowWord:str, indexes_of_dbl_letters: list):
    outputWord = ""

    # Get lengths of the syllables
    syllablesLengths = [len(x) for x in ruleToFollowWord.split("-")]
    
    counter = 0 #current position in word
    for i in range(len(syllablesLengths)):
        if len(indexes_of_dbl_letters) > 0:
            if counter <= indexes_of_dbl_letters[0] < counter + syllablesLengths[i]:
                syllablesLengths[i] += 1
                indexes_of_dbl_letters.pop(0)
        
            counter += syllablesLengths[i]

    indexcounter = 0
    #print(indexesOfDoubleLetters)

    for syllableLen in syllablesLengths:
        outputWord += inputWord[indexcounter:indexcounter+syllableLen] + "-"
        indexcounter += syllableLen
    #print("this: ", outputWord[:-1])
    return outputWord[:-1]
    



# Split the input words on positions set by the ruleToFollowWord variable
def splitWord(inputWord: str, ruleToFollowWord:str):
    lisOfDblLtr = ["dz", "dż", "cz", "dź", "sz", "rz", "ch"]

    outputWord = ""

    # Get lengths of the syllables
    syllablesLengths = [len(x) for x in ruleToFollowWord.split("-")]
    
    indexcounter = 0
    #print(indexesOfDoubleLetters)

    for syllableLen in syllablesLengths:
        outputWord += inputWord[indexcounter:indexcounter+syllableLen] + "-"
        indexcounter += syllableLen
    return outputWord[:-1]