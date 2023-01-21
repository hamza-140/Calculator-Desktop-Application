from functools import partial

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys

ERROR_MSG = "ERROR"
BUTTON_SIZE = 80

class Calculator(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowTitle("Calculator")
        outerlayout = QVBoxLayout()
        widget = QWidget()
        heading_name = QLabel("Standard")
        heading_name.setStyleSheet("font-size:40px;font-weight:bold;color:white")
        outerlayout.addWidget(heading_name)
        self.displayarea = QLineEdit()
        self.displayarea.setStyleSheet("color:white;font-size:80px;font-weight:bold;border-style:none")
        self.displayarea.setReadOnly(True)
        self.displayarea.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.displayarea.setFixedSize(1400, 140)
        outerlayout.addWidget(self.displayarea)
        toprow_layout = QHBoxLayout()
        self.buttonMap = {}
        mc_label = QLabel("MC")
        mc_label.setStyleSheet("color:white;padding-right:40px")
        toprow_layout.addWidget(mc_label)
        mr_label = QLabel("MR")
        mr_label.setStyleSheet("color:white;padding-right:40px")
        toprow_layout.addWidget(mr_label)
        mplus_label = QLabel("M+")
        mplus_label.setStyleSheet("color:white;padding-right:40px")
        toprow_layout.addWidget(mplus_label)
        mminus_label = QLabel("M-")
        mminus_label.setStyleSheet("color:white;padding-right:40px")
        toprow_layout.addWidget(mminus_label)
        ms_label = QLabel("MS")
        ms_label.setStyleSheet("color:white")
        toprow_layout.addWidget(ms_label)
        toprow_layout.addStretch()
        outerlayout.addLayout(toprow_layout)
        keyboard_layout = QGridLayout()
        keyBoard = [
            ["%", "CE", "C", "⌫"],
            ["1/x", "x²", "√x", "÷"],
            ["7", "8", "9", "✕"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["+/-", "0", ".", "="],
        ]
        for row, keys in enumerate(keyBoard):
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(key)
                self.buttonMap[key].setFixedHeight(BUTTON_SIZE)
                self.buttonMap[key].setStyleSheet("color:white;background-color:#263859;font-size:25px")
                keyboard_layout.addWidget(self.buttonMap[key], row, col)
        self.buttonMap["÷"].setStyleSheet("color:white;background-color:#263859;font-size:40px")
        self.buttonMap["-"].setStyleSheet("color:white;background-color:#263859;font-size:40px")
        self.buttonMap["+"].setStyleSheet("color:white;background-color:#263859;font-size:40px")
        self.buttonMap["="].setStyleSheet("color:white;background-color:#FF6768;font-size:40px")
        outerlayout.addLayout(keyboard_layout)
        widget.setLayout(outerlayout)
        self.setCentralWidget(widget)

    def setDisplayText(self, text):
        self.displayarea.setText(text)
        self.displayarea.setFocus()

    def displayText(self):
        return self.displayarea.text()

    def clearDisplay(self):
        self.setDisplayText("")

    def backspace(self):
        text = self.displayarea.text()
        result = text[:len(text)-1]
        self.setDisplayText(result)


def evaluateExpression(expression):
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG
    return result


class calculation:
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignalsAndSlots()

    def _calculateResult(self):
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, subExpression):
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()
        expression = self._view.displayText() + subExpression
        self._view.setDisplayText(expression)

    def _connectSignalsAndSlots(self):
        for keySymbol, button in self._view.buttonMap.items():
            if keySymbol not in {"⌫","CE","=", "C"}:
                button.clicked.connect(
                    partial(self._buildExpression, keySymbol)
                )
        self._view.buttonMap["="].clicked.connect(self._calculateResult)
        self._view.displayarea.returnPressed.connect(self._calculateResult)
        self._view.buttonMap["C"].clicked.connect(self._view.clearDisplay)
        self._view.buttonMap["⌫"].clicked.connect(self._view.backspace)


def main():
    app = QApplication([])
    window = Calculator()
    window.setStyleSheet("background-color:#17223B")
    window.showMaximized()
    window.show()
    calculation(model=evaluateExpression, view=window)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
