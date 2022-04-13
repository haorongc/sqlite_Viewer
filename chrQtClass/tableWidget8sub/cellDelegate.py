from PyQt5.QtWidgets import (QItemDelegate)
from chrSupport.basicFun import dprt

class CellDelegate(QItemDelegate):
    def __init__(self):
        super().__init__()
    #     addShortCut(self, 'Alt+Shift+d', self.paste)
    #
    def paste(self):
        dprt('pasting to cell')
    # def createEditor(self, *args):
    #     return None




