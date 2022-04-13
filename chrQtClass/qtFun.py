from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (QShortcut)


def addShortcut(widget, comboKeyStr, function):
    shortcut = QShortcut(QKeySequence(comboKeyStr), widget)
    shortcut.activated.connect(function)
    shortcut.setContext(Qt.WidgetWithChildrenShortcut)
    return shortcut


def toggleVisibility(widget):
    if widget.isHidden():
        widget.show()
    else:
        widget.hide()


def setVisibility(widget, wantShown):
    if wantShown:
        widget.show()
    else:
        widget.hide()
