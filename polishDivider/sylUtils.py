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



# Split the input words on positions set by the ruleToFollowWord variable
def splitWord(inputWord: str, ruleToFollowWord:str):
    outputWord = ""

    # Get lengths of the syllables
    syllablesLengths = [len(x) for x in ruleToFollowWord.split("-")]
    
    indexcounter = 0
    for syllableLen in syllablesLengths:
        outputWord += inputWord[indexcounter:indexcounter+syllableLen] + "-"
        indexcounter += syllableLen
    return outputWord[:-1]