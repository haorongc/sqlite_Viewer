import re

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit


class FilterLineEdit(QLineEdit):
    expressionChanged = pyqtSignal(object)

    def __init__(self, field):
        super().__init__()
        self.field = field
        self.expression = None

        self.textChanged.connect(self.updateExpression)

    def updateExpression(self):
        comparerRegex = re.compile(r'^([>=<]+)')

        searchValue = self.text().strip()
        comparer = comparerRegex.search(searchValue)
        # value comparison, add quote if want to compare string
        if comparer:
            expression = f'{self.field} {searchValue}'
        # select empty
        elif searchValue == '!!!':
            expression = f'{self.field} is NULL'
        elif searchValue == '!!':
            expression = f'({self.field} is NULL or {self.field}=\'\') '
        # like % % or None
        else:
            if searchValue.startswith('!'):
                modifyer = 'NOT'
                searchValue = searchValue.replace('!', '', 1).strip()
            else:
                modifyer = ''
            if searchValue == '':
                expression = None
            else:
                expression = f"{self.field} {modifyer} like '%{searchValue}%'"

        if expression != self.expression:
            # emit a valid expression or None
            self.currentExpression = expression
            self.expressionChanged.emit((self.expression, expression))
            self.expression = expression

    def clear(self):
        super().clear()
        self.expression = None
