try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

from lib import newIcon, labelValidator

BB = QDialogButtonBox


class LabelDialog(QDialog):

    def __init__(self, text="Enter object label", parent=None, listItem=None):
        super(LabelDialog, self).__init__(parent)
        self.edit = QLineEdit()
        self.edit.setText(text)
        self.edit.setValidator(labelValidator())
        self.edit.editingFinished.connect(self.postProcess)

        self.desc = QLineEdit()
        #Use the below to support multi-line captions/descriptions
        #Show description textbox invisbily st can be dynamically resized
        #self.desc = QTextEdit()
        #self.desc.setAttribute(103)
        #self.desc.show()
        #self.set_desc_height()
        #self.desc.setValidator(labelValidator())
        #self.desc.textChanged.connect(self.set_desc_height)

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Label:'))
        layout.addWidget(self.edit)
        layout.addWidget(QLabel('Description:'))
        layout.addWidget(self.desc)
        self.buttonBox = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(newIcon('done'))
        bb.button(BB.Cancel).setIcon(newIcon('undo'))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

        if listItem is not None and len(listItem) > 0:
            self.listWidget = QListWidget(self)
            for item in listItem:
                self.listWidget.addItem(item)
            self.listWidget.itemDoubleClicked.connect(self.listItemClick)
            layout.addWidget(self.listWidget)

        self.setLayout(layout)

    def set_desc_height(self):
        lines = self.desc.document().size().height() + 5
        self.desc.setMaximumHeight(lines)

    def get_desc_text(self):
        #Use the below if supporting multi-line captions (QTextEdit)
        #s = self.desc.toPlainText()
        s = self.desc.text()
        return None if s.isEmpty() else s

    def validate(self):
        try:
            if self.edit.text().trimmed():
                self.accept()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            if self.edit.text().strip():
                self.accept()

    def postProcess(self):
        try:
            self.edit.setText(self.edit.text().trimmed())
            self.desc.setText(self.desc.text().trimmed())
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            self.edit.setText(self.edit.text().strip())

    def popUp(self, text='', cap=None, move=True):
        self.edit.setText(text)
        cap = '' if cap is None else cap
        self.desc.setText(cap)
        self.edit.setSelection(0, len(text))
        self.edit.setFocus(Qt.PopupFocusReason)
        if move:
            self.move(QCursor.pos())
        return (self.edit.text(), self.get_desc_text()) if self.exec_() else (None, None)

    def listItemClick(self, tQListWidgetItem):
        try:
            text = tQListWidgetItem.text().trimmed()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            text = tQListWidgetItem.text().strip()
        self.edit.setText(text)
        self.validate()
