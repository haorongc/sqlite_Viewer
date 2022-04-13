import re
import sys

import pyperclip
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontMetrics, QTextCursor
from PyQt5.QtWidgets import (QApplication, QPlainTextEdit)

from chrSupport.basicFun import dprt, dateStamp
from chrQtClass.qtFun import addShortcut
import cgitb
cgitb.enable(format='text')

class TextEdit(QPlainTextEdit):  # QPlainTextEdit, QTextEdit
    def __init__(self):
        super().__init__()

        # visual settings
        self.tabWidth = 4
        self.fontsize = 10
        cursorWidth = int(self.fontsize * 0.4)
        font = QFont()
        font.setStyleHint(QFont.Monospace)
        font.setFamily('Consolas')  # 'Courier'
        font.setPointSize(self.fontsize)
        font.setFixedPitch(True)
        self.setFont(font)
        self.setCursorWidth(cursorWidth)
        QApplication.setCursorFlashTime(0)

        # customize tab size
        metrics = QFontMetrics(font)
        self.setTabStopWidth(self.tabWidth * metrics.width(' '))
        # self.setFont(QFont('Arial', 10))

        self.setupShortcuts()
        #
        # self.adHoc()
        self.setMinimumWidth(500)

    def saveCursor(self):
        cursor = self.textCursor()
        self.savedCursorPos = cursor.position()

    def reloadCursor(self):
        cursor = self.textCursor()
        cursor.setPosition(self.savedCursorPos)
        self.setTextCursor(cursor)

    def leftCursorPos(self):
        return self.textCursor().selectionStart()

    def rightCursorPos(self):
        return self.textCursor().selectionEnd()

    def expandSelection(self):
        cursor = self.wordsSelector()
        self.setTextCursor(cursor)
        return cursor

    def paste_space2tab(self):
        # convert spaces to tab
        leftPos = self.leftCursorPos()
        text2paste = pyperclip.paste()
        text_tab2space = re.sub(r' {'+str(self.tabWidth)+'}', '\t', text2paste)
        self.insertPlainText(text_tab2space)

    # def redoAvailable(self):
    #     dprt('redo')

    # def redo(self, available):
    #     dprt('redo changed to delete line')
    #     self.deleteSelectedLines()
    #
    #     # super().redo()

    def cut(self):
        cursor = self.copy()
        cursor.removeSelectedText()

    # def createMimeDataFromSelection(self):
    #     pass
    def copyLine(self):
        cursor = self.linesSelector(includeTrailingSeparator=True)
        # self.setTextCursor(cursor)
        selectedText = cursor.selectedText()
        pyperclip.copy(selectedText)
        return cursor

    def copy(self):
        dprt('my copy function')
        cursor = self.textCursor()
        selectedText = cursor.selectedText()
        if selectedText:
            pyperclip.copy(selectedText)
            return cursor
        else:
            return self.copyLine()


    def adHoc(self):
        cursor = self.textCursor()
        cursor.insertText('11111\n\t222222\n\t\t33333\n\t44444')
        pass

    def lineLevelDown(self, cursor):
        cursor.movePosition(QTextCursor.StartOfLine)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
        firstChar = cursor.selectedText()
        if firstChar == '\t':
            cursor.removeSelectedText()

    def linesLevelUp(self):
        self.linesLevelUpDown(wantUp=True)

    def linesLevelDown(self):
        self.linesLevelUpDown(wantUp=False)

    def lineLevelUp(self, cursor):
        cursor.movePosition(QTextCursor.StartOfLine)
        cursor.insertText('\t')

    def linesLevelUpDown(self, wantUp):
        if wantUp:
            lineMoveFun = self.lineLevelUp
        else:
            lineMoveFun = self.lineLevelDown

        cursor = self.textCursor()

        cursor.beginEditBlock()
        leftLinePos = self.start7selectedLines()
        rightPos = cursor.selectionEnd()
        # iterate selected lines from bottom to top.
        # so that early changes won't affect environment for later operations
        cursor.setPosition(rightPos)
        while cursor.position() >= leftLinePos:  # cursor.position() >= 0 and
            # operate on line and move up
            lineMoveFun(cursor)

            prevPos = cursor.position()
            cursor.movePosition(QTextCursor.Up)
            if cursor.position() == prevPos:
                # no move, because cannot move up
                break

        cursor.endEditBlock()

    def linesLevelDown(self):

        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.StartOfLine)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()

    def probeFun(self, seq='default'):
        print(f'debug probe triggered by {seq}')

    def insertDateText(self):
        date = dateStamp()
        dateStr = '{' + date + '}'
        cursor = self.textCursor()
        cursor.insertText(dateStr)

    def duplicateLine(self):
        cursor = self.linesSelector(includeTrailingSeparator=True)
        lineText = cursor.selectedText()
        # self.newLineBelow()
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.StartOfLine)
        cursor.insertText(lineText)

    def deleteSelectedLines(self):
        cursor = self.linesSelector()
        cursor.removeSelectedText()



    def start7selectedWords(self):
        cursor = self.textCursor()
        pos = cursor.selectionStart()
        # go to begining of first selected lines
        cursor.setPosition(pos)
        cursor.movePosition(QTextCursor.StartOfWord)
        return cursor.position()

    def end7selectedWords(self):
        cursor = self.textCursor()
        pos = cursor.selectionEnd()
        # go to begining of first selected lines
        cursor.setPosition(pos)
        cursor.movePosition(QTextCursor.EndOfWord)
        return cursor.position()

    def start7selectedLines(self):
        cursor = self.textCursor()
        pos = cursor.selectionStart()
        # go to begining of first selected lines
        cursor.setPosition(pos)
        cursor.movePosition(QTextCursor.StartOfLine)
        return cursor.position()

    def end7selectedLines(self):
        cursor = self.textCursor()
        pos = cursor.selectionEnd()
        # go to begining of first selected lines
        cursor.setPosition(pos)
        cursor.movePosition(QTextCursor.EndOfLine)
        return cursor.position()

    def linesSelector(self, includeTrailingSeparator=True):
        cursor = self.textCursor()
        leftPos_fullLine = self.start7selectedLines()
        rightPos_fullLine = self.end7selectedLines()

        if includeTrailingSeparator:
            cursor.setPosition(rightPos_fullLine)
            if cursor.atEnd():
                dprt('end of editor')
                cursor.insertText('\n')
                rightPos_fullLine = cursor.position()
            else:
                rightPos_fullLine += 1

        cursor.setPosition(leftPos_fullLine)
        cursor.setPosition(rightPos_fullLine, QTextCursor.KeepAnchor)
        return cursor

    def wordsSelector(self):
        cursor = self.textCursor()
        leftPos_fullLine = self.start7selectedWords()
        rightPos_fullLine = self.end7selectedWords()

        cursor.setPosition(leftPos_fullLine)
        cursor.setPosition(rightPos_fullLine, QTextCursor.KeepAnchor)
        return cursor

    def moveLinesUp(self):
        self.moveLinesUpDown(wantUp=True)

    def moveLinesDown(self):
        self.moveLinesUpDown(wantUp=False)

    def moveLinesUpDown(self, wantUp=True):
        if wantUp:
            moveDirection = QTextCursor.Up
        else:
            moveDirection = QTextCursor.Down

        # cursor.movePosition(QTextCursor.StartOfLine)
        # cursor.movePosition(QTextCursor.EndOfLine, mode=QTextCursor.KeepAnchor)
        cursor = self.linesSelector()
        cursor.beginEditBlock()

        linesText = cursor.selectedText()

        # if not linesText.endswith('\n'):
        #     linesText += '\n'
        cursor.removeSelectedText()
        cursor.movePosition(moveDirection, mode=QTextCursor.MoveAnchor)

        pos_beforeInsertion = cursor.position()
        cursor.insertText(linesText)
        cursor.movePosition(QTextCursor.Left, mode=QTextCursor.MoveAnchor)
        cursor.setPosition(pos_beforeInsertion, QTextCursor.KeepAnchor)

        self.setTextCursor(cursor)
        cursor.endEditBlock()

    def getCurrentLineLevel(self):
        # no valid, need to find current level
        cursor = self.textCursor()
        cursor.select(QTextCursor.LineUnderCursor)
        lineText = cursor.selectedText()
        n = 0
        for char in lineText:
            if char == '\t':
                n += 1
            else:
                break
        self.currentLinelevel = n
        return n

    def keyPressEvent(self, event):
        # shortCuts involving enter
        if event.key() == Qt.Key_Return:
            if event.modifiers() & Qt.ShiftModifier:
                self.newLineBelow()
                return
            else:
                n = self.getCurrentLineLevel()
                self.insertPlainText('\n' + '\t' * n)
                return

        # shortCuts involving ctrl
        if event.modifiers() & Qt.ControlModifier:
            keyOrd = event.key()
            if keyOrd in {ord('y'), ord('Y')}:
                self.deleteSelectedLines()
                return
            elif keyOrd in {ord('x'), ord('X')}:
                self.cut()
                return
            elif keyOrd in {ord('c'), ord('C')}:
                self.copy()
                return
            elif keyOrd in {ord('v'), ord('V')}:
                self.paste_space2tab()
                return
        # paired symbols
        charPairDict = {"[": "]", "'": "'", '"': '"', "{": "}", "(": ")"}
        newChar = event.text()
        # auto complettion pair
        if newChar in charPairDict.keys():
            complementChar = charPairDict[newChar]
            # add pair depending on selection
            cursor = self.textCursor()
            if cursor.hasSelection() == False:
                cursor.beginEditBlock()
                self.insertPlainText(newChar + complementChar)
                cursor.movePosition(QTextCursor.Left)
                self.setTextCursor(cursor)
                cursor.endEditBlock()
            else:
                # wrap pairing chars around selected text
                cursor.beginEditBlock()
                leftPos = cursor.selectionStart()
                rightPos = cursor.selectionEnd()
                cursor.setPosition(rightPos)
                cursor.insertText(complementChar)

                cursor.setPosition(leftPos)
                cursor.insertText(newChar)
                # keep selection
                cursor.setPosition(rightPos + 1, QTextCursor.KeepAnchor)
                self.setTextCursor(cursor)
                cursor.endEditBlock()

        else:
            # other keys, let function normally
            super().keyPressEvent(event)

    # def redo(self):
    #     dprt('redo')
    #
    # def undo(self):
    #     dprt('undo')

    def setupShortcuts(self):
        # self.copyAvailable.connect(self.copy)
        # self.redoAvailable.connect(self.redo)
        # insert datetime stamp
        addShortcut(self, 'Ctrl+d', self.duplicateLine)
        addShortcut(self, 'Ctrl+b', self.newLineBelow)  # choose another combination
        addShortcut(self, 'Ctrl+u', self.deleteSelectedLines)  # choose another combination
        addShortcut(self, 'Ctrl+p', self.probeFun)  # choose another combination

        addShortcut(self, 'Alt+Shift+d', self.insertDateText)  # choose another combination
        addShortcut(self, 'Alt+e', self.expandSelection)  # choose another combination
        addShortcut(self, 'Ctrl+]', self.linesLevelUp)  # choose another combination
        addShortcut(self, 'Ctrl+[', self.linesLevelDown)  # choose another combination
        addShortcut(self, 'Shift+tab', self.linesLevelDown)  # choose another combination

        addShortcut(self, 'Ctrl+Shift+up', self.moveLinesUp)  # choose another combination
        addShortcut(self, 'Ctrl+Shift+Down', self.moveLinesDown)  # choose another combination


    def newLineBelow(self):
        currentLineLevel = self.getCurrentLineLevel()
        self.moveCursor(QTextCursor.EndOfLine)
        self.insertPlainText('\n' + '\t' * currentLineLevel)
        pass
        # self.goto

    def setupCustomShortcuts(self):
        pass

    def setEditLocked(self, want2lock):
        if want2lock:
            self.setTextInteractionFlags(Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse )
            #Qt.TextSelectableByKeyboard |Qt.TextBrowserInteraction
            # self.setTextInteractionFlags()
            # AccessibleTextRole NoTextInteraction  Qt.TextSelectableByKeyboard, TextBrowserInteraction, TextEditable
        else:
            self.setTextInteractionFlags(Qt.TextEditorInteraction)


def main():
    app = QApplication(sys.argv)

    editor = TextEdit()
    editor.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
