from chrQtClass.qtFun import addShortcut


class FilterDriver():
    backdoorPhrase = None

    def __init__(self, tableWidget):
        self.filterHeader = tableWidget.filterHeader
        self.filterEdits = self.filterHeader.filterEdits
        self.model = tableWidget.model

        self.typedPhraseSet = set()
        self.bgndFilterEnabled = False
        # self.updateBgndPhrase(bgndPhrase)

        for filterEdit in self.filterEdits:
            filterEdit.expressionChanged.connect(self.updateTypedExpression)

        addShortcut(tableWidget, 'Shift+Alt+c', self.clearTypedFilter)
        addShortcut(tableWidget, 'Ctrl+f', self.search0title)
        addShortcut(tableWidget, 'Ctrl+Shift+f', self.filterHeader.hide)

    def search0title(self):
        self.filterHeader.show8selectTitleBox()

    def updateTypedExpression(self, pair):
        previous, current = pair
        self.replaceInWorkingSet(previous, current)
        self.deployFilter()

    def updateBgndPhrase(self, expression=None):
        self.bgndPhrase = expression
        if self.bgndFilterEnabled:
            self.deployFilter()

    def setBackdoorPhrase(self, backDoorPhrase):
        self.backdoorPhrase = backDoorPhrase

    def toggleBgndFilter(self):
        self.bgndFilterEnabled = not self.bgndFilterEnabled
        self.deployFilter()

    def deployFilter(self):
        typedFilterSentence = ' AND '.join(self.typedPhraseSet)

        if self.bgndFilterEnabled:
            finalExpression = self.logicPhraseJoin(typedFilterSentence, 'AND', self.bgndPhrase)
            finalExpression = self.logicPhraseJoin(finalExpression, 'OR', self.backdoorPhrase)

        else:
            if len(self.typedPhraseSet) > 0:
                finalExpression = self.logicPhraseJoin(typedFilterSentence, 'OR', self.backdoorPhrase)
            else:
                finalExpression = ''

        self.model.setFilter(finalExpression)
        self.model.refresh()

    def clearTypedConstraints(self):
        if self.bgndFilterEnabled:
            self.model.setFilter(self.bgndPhrase)
        else:
            self.model.setFilter('')  # show everything

        self.model.refresh()

    def logicPhraseJoin(self, phrase1, operatorSymbol, phrase2):
        if phrase1 and phrase2:
            return f'({phrase1}) {operatorSymbol} ({phrase2})'
        elif phrase1:
            return f'({phrase1})'
        elif phrase2:
            return f'({phrase2})'
        else:
            return ''

    def clearTypedFilter(self):
        self.filterHeader.clearAllBoxes()

    def replaceInWorkingSet(self, prevExpression, expression):
        self.removeExpression(prevExpression)
        self.addExpression(expression)

    def addExpression(self, expression):
        if expression:
            self.typedPhraseSet.add(expression)

    def removeExpression(self, expression):
        if expression:
            try:
                self.typedPhraseSet.remove(expression)
            except:
                pass
                print(f'{expression} not in filter expression set')
