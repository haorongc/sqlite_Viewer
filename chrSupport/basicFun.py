#! python3.8
# -*- coding: utf-8 -*-
import datetime
import os
import re
import shutil
from xml.etree import cElementTree as ET

import numpy as np
from PyPDF2 import PdfFileReader
from PyQt5.QtWidgets import (QShortcut)
from send2trash import send2trash
from tinytag import TinyTag
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt

def addLetterSuffix(originalStr,i):
    letterAscii = ord('A') + i
    letter = chr(letterAscii)
    return originalStr + letter

def dprt(value, discription=None):
    if discription != None:
        print(f'>>{discription}')
    print(value)


def ascendConcate(strings):
    sortedNames = sorted(strings)
    return '_'.join(sortedNames)


def nanList(items):
    result = []
    for item in items:
        if item is not None:
            result.append(item)
    return result


def nanMax(nums):
    nums = nanList(nums)
    nums = np.asarray(nums)
    return np.nanmax(nums)


def positiveNanMin(nums):
    nums = nanList(nums)
    nums = np.asarray(nums)
    nums = nums[nums > 0]
    return np.nanmin(nums)


def megabytes6path(path):
    if os.path.isfile(path):
        return os.stat(path).st_size / (1024 ** 2)
    elif os.path.isdir(path):
        bytes = 0
        for loc, dirNames, fnames in os.walk(path, topdown=False):
            for fname in fnames:
                _path = os.path.join(loc, fname)
                bytes += os.stat(_path).st_size
        return bytes / (1024 ** 2)
    else:
        return None


def dateTimeStamp(now=None, start=2, len=13):
    """convert passed time/current time to YYMMDD.hhmm, return as string"""
    if now == None:
        now = datetime.datetime.now()  # create time stamp
    return f'{now.year:02d}{now.month:02d}{now.day:02d}.{now.hour:02d}{now.minute:02d}{now.second:02d}'[
           start:start + len]
    # now.strftime('%y')[-2:]+now.strftime('%m')[-2:]+now.strftime('%d')[-2:]


def dateStamp(now=None):
    return dateTimeStamp(now, start=2, len=6)

def dictExclude(oriDict, fields2exclude):
    newDict = dict()
    for key, value in oriDict.items():
        if key not in fields2exclude:
            newDict[key] = value
    return newDict

def dictIntersect(oriDict, fields2keep):
    newDict = dict()
    for key, value in oriDict.items():
        if key in fields2keep:
            newDict[key] = value
    return newDict


def pdf2note(pdfPath, notePath, writeMode='a'):
    with open(notePath, writeMode, errors='replace') as noteHandle:
        with open(pdfPath, "rb") as pdfHandle:
            reader = PdfFileReader(pdfHandle)
            nPages = reader.getNumPages()
            for i in range(nPages):  #
                pagePrinted = False
                currentPage = reader.getPage(i)
                for annot in currentPage.get('/Annots', []):
                    annotationObject = annot.getObject()
                    if annotationObject.get('/Subj', None) == 'Typewriter':
                        xmlString = annotationObject.get('/RC', None)

                        text = text6xml(xmlString)
                        text = ridSpaces(text)
                        if text:
                            if pagePrinted == False:
                                noteHandle.write(f'-<{i + 1}>-')
                                noteHandle.write('\n')
                                pagePrinted = True
                            noteHandle.write(text)
                            noteHandle.write('\n')


def getPdfLength(pdfPath):
    try:
        pdfReader = PdfFileReader(pdfPath, strict=False)
        numPages = pdfReader.getNumPages()
        return numPages
    except:
        print(f'bad pdf: {pdfPath}')
        return -1


def getAudioFolderlength(folderPath):
    seconds = 0
    for leafname in os.listdir(folderPath):
        nname, ext = os.path.splitext(leafname)
        if ext in audioExts:
            leafpath = os.path.join(folderPath, leafname)
            tag = TinyTag.get(leafpath)
            try:
                seconds += tag.duration
            except:
                print('failed to get duration')
    hours = seconds / 3600
    print(folderPath)
    print(f'\t{hours} hours')
    return hours


def text6xml(xmlString):
    texts = list()

    def visit(root):
        if root.text and root.text.strip():
            texts.append(root.text.strip())
            # print(root.text.strip())
        try:
            for p in list(root):
                visit(p)
        except:
            pass

    root = ET.fromstring(xmlString)
    visit(root)
    return ' '.join(texts)


def ridSpaces(line):
    spaceRegex = re.compile(r' [B-HJ-Zb-z] [A-Za-z]+?')
    matches = spaceRegex.findall(line)
    for match in matches:
        newMatch = ' ' + match.replace(' ', '')
        line = line.replace(match, newMatch, 1)
    return line
