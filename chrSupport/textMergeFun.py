import numpy as np
from chrSupport.basicFun import nanList


def textChosenByLength(texts, preferShortest=True):
    nanTexts = nanList(texts)
    lengths = [len(nanText) for nanText in nanTexts]
    lengths = np.asarray(lengths)
    if preferShortest:
        index = np.argmin(lengths)
    else:
        index = np.argmax(lengths)

    return nanTexts[index]


def mergedTextArrays(tagStrings, inputSeparator=',', outputSeparator=', '):
    allTags = []
    for tagString in tagStrings:
        try:
            tags = tagString.split(inputSeparator)
            for tag in tags:
                tag = tag.strip()
                if tag and tag not in allTags:
                    allTags.append(tag)  # gather unique tags while also keeping order
        except:
            # cannot strip, something is not right, skip this note string
            continue

    allTagString = ', '.join(allTags)
    if allTagString:
        return allTagString
    else:
        return ''


def mergedNote(noteStrings):
    mergedNoteString = ''
    for noteString in noteStrings:
        try:
            noteString = noteString.strip()
        except:
            # cannot strip, something is not right, skip this note string
            continue
        if noteString and noteString not in mergedNoteString:
            if mergedNoteString:
                mergedNoteString = f'{mergedNoteString}; {noteString}'
            else:
                mergedNoteString = noteString
    return mergedNoteString
