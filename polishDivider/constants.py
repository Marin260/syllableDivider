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