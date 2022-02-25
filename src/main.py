from sys import exit, argv
from subprocess import Popen
from json import load, dump
import traceback

import buildInfo

from PySide6.QtGui import QFont, QAction
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QComboBox, QPushButton, QLabel, QVBoxLayout,
    QApplication, QSizePolicy, QLineEdit, QToolBar, QMessageBox
)

MINIMUM_SIZE = QSizePolicy(
    QSizePolicy.Policy.Maximum,
    QSizePolicy.Policy.Maximum,
    QSizePolicy.ControlType.DefaultType
)

ABOUT_TEXT = \
f"""
f2k
--- 
A simple LaunchPad/Take2Launcher  
replacement for Civ VI
***
`{buildInfo.gitHash}`  
{buildInfo.buildDate}  
Distributed under the MIT (Expat) license
***
© JakeIsMeh  
[GitHub](https://github.com/JakeIsMeh) | [GitLab](https://gitlab.com/JakeIsMeh)
***
Built with Python3 and PySide6
"""

# dicts are ordered since py3.6 :D
renderers = {
    "DX11": "DirectX 11",
    "DX12": "DirectX 12"
}

class f2kWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Options
        self.opts = {
            "launchOpts": "",
            "renderer": 0
        }

        try:
            with open("f2kOpts.json", "r") as f:
                self.opts = load(f)
        except FileNotFoundError:
            pass

        # Elements
        self.toolBar = QToolBar()
        self.toolBar.setMovable(False)

        self.saveAction = QAction("Save", self)
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.setStatusTip("Save your options")
        self.saveAction.triggered.connect(self.saveOpts)

        self.quitAction = QAction("Quit", self)
        self.quitAction.setShortcuts(["Ctrl+Q", "Ctrl+W"])
        self.quitAction.setStatusTip("Quit without launching")
        self.quitAction.triggered.connect(self.quit)

        self.aboutAction = QAction("About", self)
        self.aboutAction.setShortcuts(["Alt+A", "Alt+H"])
        self.aboutAction.setStatusTip("About")
        self.aboutAction.triggered.connect(self.about)

        self.title = QLabel("f2k")
        self.title.setFont(QFont('Sans', 24, 700))

        self.launchOptionsLabel = QLabel("Launch Options")
        self.launchOptionsLabel.setSizePolicy(MINIMUM_SIZE)

        self.launchOptions = QLineEdit()
        self.launchOptions.setText(self.opts["launchOpts"])

        self.rendererLabel = QLabel("Renderer")
        self.rendererLabel.setSizePolicy(MINIMUM_SIZE)

        self.rendererDropdown = QComboBox()
        self.rendererDropdown.InsertPolicy = QComboBox.NoInsert
        for renderer in renderers.keys():
            self.rendererDropdown.addItem(
                renderers[renderer], renderer
            )
        self.rendererDropdown.setCurrentIndex(self.opts["renderer"])

        self.launchButton = QPushButton("Launch Civ VI")
        self.launchButton.setFont(QFont('Sans', 16))
        self.launchButton.clicked.connect(self.launch)
        self.launchButton.setAutoDefault(True)

        # Layout
        self.toolBar.addActions([
            self.saveAction, self.quitAction, self.aboutAction
        ])
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.title, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.launchOptionsLabel)
        self.layout.addWidget(self.launchOptions)
        self.layout.addWidget(self.rendererLabel)
        self.layout.addWidget(self.rendererDropdown)
        self.layout.addWidget(self.launchButton)

    @Slot()
    def quit(self):
        exit()

    @Slot()
    def saveOpts(self):
        with open("f2kOpts.json", "w") as f:
            optsDict = {
                "launchOpts": self.launchOptions.text(),
                "renderer": self.rendererDropdown.currentIndex()
            }
            dump(optsDict, f)

    @Slot()
    def about(self):
        aboutBox = QMessageBox()
        aboutBox.setWindowTitle("About f2k")
        aboutBox.setFont(QFont('Sans', 10, 500))
        aboutBox.setIcon(QMessageBox.Icon.Information)
        aboutBox.setTextFormat(Qt.TextFormat.MarkdownText)
        aboutBox.setText(ABOUT_TEXT)
        aboutQtButton = aboutBox.addButton("About Qt", QMessageBox.ResetRole)
        aboutQtButton.clicked.connect(self.aboutQt)
        okButton = aboutBox.addButton(QMessageBox.Ok)
        aboutBox.exec()

    @Slot()
    def aboutQt(self):
        QMessageBox.aboutQt(self, "About Qt")

    @Slot()
    def launch(self):
        exe, cmd = "", ""

        match list(renderers.keys())[self.rendererDropdown.currentIndex()]:
            case "DX11":
                exe = "Base\Binaries\Win64Steam\CivilizationVI.exe"
            case "DX12":
                exe = "Base\Binaries\Win64Steam\CivilizationVI_DX12.exe"

        # attempt to clean argv, tested with steam only
        cleanedArgv = argv[2:]

        cmd = " ".join([exe] + cleanedArgv + [self.launchOptions.text()])
        try:
            Popen(cmd, start_new_session=True)
            self.saveOpts()
        except FileNotFoundError:
            errorBox = QMessageBox()
            errorBox.setWindowTitle("Failed to launch")
            errorBox.setFont(QFont('Sans', 10, 500))
            errorBox.setIcon(QMessageBox.Icon.Warning)
            errorBox.setTextFormat(Qt.TextFormat.PlainText)
            errorBox.setText("Could not find Civ VI, are you sure f2k is in the right place?")
            errorBox.addButton(QMessageBox.Ok)
            errorBox.exec()
        except Exception as e:
            errorBox = QMessageBox()
            errorBox.setWindowTitle("Failed to launch")
            errorBox.setFont(QFont('Sans', 10, 500))
            errorBox.setIcon(QMessageBox.Icon.Critical)
            errorBox.setTextFormat(Qt.TextFormat.PlainText)
            errorBox.setText("Failed to launch\n\n" + 
                "\n".join(
                    traceback.format_exception(
                        type(e), e, e.__traceback__
                    )
                )
            )
            errorBox.addButton(QMessageBox.Ok)
            errorBox.exec()
        self.quit()


if __name__ == "__main__":
    app = QApplication([])
    app.setFont(QFont('Sans', 10, 500))

    widget = f2kWidget()
    mainWindow = QMainWindow()

    mainWindow.setFixedSize(400,300)
    mainWindow.setWindowTitle("f2k — Civ VI")

    mainWindow.addToolBar(widget.toolBar)
    mainWindow.setCentralWidget(widget)

    mainWindow.show()

    exit(app.exec())