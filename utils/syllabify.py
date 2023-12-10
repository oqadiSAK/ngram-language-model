import re

rules = [
    {"pattern": r'^[aeiouöüıİ][bcçdfgğhjklmnprsştvyz][aeiouöüıİ]', "length": 1},
    {"pattern": r'^[aeiouöüıİ]{2}[bcçdfgğhjklmnprsştvyz]', "length": 1},      
    {"pattern": r'^[bcçdfgğhjklmnprsştvyz][aeiouöüıİ]{2}', "length": 2},      
    {"pattern": r'^[aeiouöüıİ][bcçdfgğhjklmnprsştvyz]{2}[aeiouöüıİ]', "length": 2}, 
    {"pattern": r'^([bcçdfgğhjklmnprsştvyz][aeiouöüıİ]){2}', "length": 2},         
    {"pattern": r'^[aeiouöüıİ][bcçdfgğhjklmnprsştvyz]{2}($|[bcçdfgğhjklmnprsştvyz])', "length": 3},  
    {"pattern": r'^[bcçdfgğhjklmnprsştvyz][aeiouöüıİ][bcçdfgğhjklmnprsştvyz]($|[bcçdfgğhjklmnprsştvyz][aeiouöüıİ])', "length": 3},  
    {"pattern": r'^[bcçdfgğhjklmnprsştvyz]{2}[aeiouöüıİ][bcçdfgğhjklmnprsştvyz][aeiouöüıİ]', "length": 3}, 
    {"pattern": r'^[bcçdfgğhjklmnprsştvyz][aeiouöüıİ][bcçdfgğhjklmnprsştvyz]{2}($|[bcçdfgğhjklmnprsştvyz])', "length": 4},  
    {"pattern": r'^[bcçdfgğhjklmnprsştvyz]{2}[aeiouöüıİ][bcçdfgğhjklmnprsştvyz]($|[bcçdfgğhjklmnprsştvyz][aeiouöüıİ])', "length": 4},  
    {"pattern": r'^[bcçdfgğhjklmnprsştvyz]{2}[aeiouöüıİ][bcçdfgğhjklmnprsştvyz]{2}($|[bcçdfgğhjklmnprsştvyz])', "length": 5}  
]

def syllabify(word):
    if len(word) < 3: 
        return word

    for rule in rules:
        if re.match(rule["pattern"], word, re.IGNORECASE):
            if len(word) > rule["length"]:
                return f"{word[:rule['length']]} {syllabify(word[rule['length']:])}"
            else:
                return word

    return word