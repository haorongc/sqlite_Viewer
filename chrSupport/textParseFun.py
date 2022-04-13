import re
compoundIdRegex = re.compile(r'[a-zA-Z]+\d+(-\d+)?')
typeIdRegex = re.compile(r'([a-zA-Z]+)(\d+)(-\d+)?')
wordNumberRegex = re.compile(r'([a-zA-Z]+)(\d*)?')

def extractCompoundStr(inputStr):
    compoundStrs = []
    while 1:
        match = compoundIdRegex.search(inputStr)
        if not match:
            break
        compoundStr = match.group()
        compoundStrs.append(compoundStr)
        inputStr = inputStr.replace(compoundStr, '', 1)
    return compoundStrs

def sampleDicts6idStr(compoundId):
    match = typeIdRegex.search(compoundId)
    type, id1, id2 = match.groups()
    id1 = int(id1)
    if id2!=None:
        id2 = int(id2[1:])  # skip '-' and turn into int
    else:
        id2 = id1

    compoundIds = []
    for id in range(id1, id2+1):
        compoundIds.append({'type': type, 'id': id})

    return compoundIds

def sampleNames6idDicts(idDicts):
    sampleNames = []
    for idDict in idDicts:
        type = idDict['type']
        id = idDict['id']
        sampleName = f'{type}{id}'
        sampleNames.append(sampleName)
    return ', '.join(sampleNames)

def word_num6text(text):
    match = wordNumberRegex.search(text)
    word, number = match.groups()
    if number:
        number = int(number)
    else:
        number = None
    return word, number


def parsedIdDicts6text(text):
    compoundStrs = extractCompoundStr(text)
    sampleDicts = []
    for compoundStr in compoundStrs:
        sampleDicts += sampleDicts6idStr(compoundStr)
    return sampleDicts

def standardizedIdStr(text):
    idDicts = parsedIdDicts6text(text)
    standardStr = sampleNames6idDicts(idDicts)
    return standardStr

if __name__ == '__main__':
    text = 'p100'
    print(word_num6text(text))

    text = 'gft'
    print(word_num6text(text))
    # text = 'BioRad Chemidoc MP 2022-01-21 21hr 04min_g17-18, g17-18, f243'
    # idDicts = parsedIdDicts6text(text)
    # print(idDicts)
    # compoundStrs = set(compoundStrs)
    # print(compoundStrs)

