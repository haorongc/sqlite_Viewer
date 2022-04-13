from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QTableView, QItemDelegate, QStyledItemDelegate)
from PyQt5.QtGui import QPalette, QColor
from PyQt5 import QtWidgets

class ReadOnlyDelegate(QStyledItemDelegate):
    # def __init__(self):
    #     super().__init__()
    #     # palette = QPalette()
    #     # palette.setColor(QPalette.Inactive, QPalette.Highlight,
    #     #                  palette.color(QPalette.Active, QPalette.Highlight))
    #     self.setStyleSheet('font: italic')
    def initStyleOption(self, option, index):
        # adapted from https://www.5axxw.com/questions/content/uxeobe
        super().initStyleOption(option, index)

        # color = QColor("#FFFFFF")
        # color = QColor("#34ebc6")
        color = QColor("#000080")

        # if index.column() == 1:
        #     color = QColor("#34ebc6")
        # elif index.column() == 2:
        #     color = QColor("#FFFFFF")
        # elif index.column() == 3:
        #     color = QColor("#9546c7")

        # if option.state & QtWidgets.QStyle.State_Enabled:
        #     cg = QPalette.Normal
        # else:
        #     cg = QPalette.Disabled

        # if option.state & QtWidgets.QStyle.State_Selected:
        # if True:
        #     option.palette.setColor(cg, QPalette.HighlightedText, color)

        option.palette.setBrush(QPalette.Text, color)  # QPalette.TextQ Palette.Background
        option.palette.setColor(QPalette.Background, color)  # QPalette.TextQ Palette.Background

    # def drawDisplay(self, painter, option, rect, text):
    #     color = painter._color
    #     opt = QtWidgets.QStyleOptionViewItem(option)
    #     cg = (
    #         QPalette.Normal
    #         if opt.state & QtWidgets.QStyle.State_Enabled
    #         else QPalette.Disabled
    #     )
    #     if opt.state & QtWidgets.QStyle.State_Selected:
    #         opt.palette.setColor(cg, QPalette.HighlightedText, color)
    #     opt.palette.setColor(cg, QPalette.Text, color)
    #     super().drawDisplay(painter, opt, rect, text)

    def createEditor(self, *args):
        return None




