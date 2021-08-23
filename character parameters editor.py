import os

from lib.design.character_parameters_editor_design import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QFileDialog, QMessageBox

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # File tab
        self.actionOpen.triggered.connect(self.action_open_logic)
        #self.actionSave.triggered.connect(self.action_save_logic)
        self.actionClose.triggered.connect(self.close)

        # About tab
        self.actionAuthor.triggered.connect(self.action_author_logic)
        self.actionCredits.triggered.connect(self.action_credits_logic)

        # Load all the mini portraits
        miniPortraits = self.panel.findChildren(QLabel)
        path_little_images = os.path.join("lib","images","little")
        for i in range(0,62):
        	miniPortraits[i].setPixmap(QPixmap(os.path.join(path_little_images, "sc_chara_0" + miniPortraits[i].objectName().split("_")[1] + ".bmp")))
        	miniPortraits[i].setStyleSheet("QLabel {border : 3px solid grey;}")
        	miniPortraits[i].setDisabled(True)

        for i in range(62, len(miniPortraits)):
        	miniPortraits[i].setStyleSheet("QLabel {border : 3px solid grey;}")
        	miniPortraits[i].setVisible(False)

        # Set the the main image invisible
        self.portrait.setVisible(False)

    def action_open_logic(self):

		# Open spr file
        spr_file_path_original = \
            QFileDialog.getOpenFileName(self, "Open file", os.path.abspath(os.getcwd()), "PAK files (*.dak)")[0]


    def closeEvent(self, event):
        event.accept()

    @staticmethod
    def action_author_logic():
        msg = QMessageBox()
        msg.setTextFormat(1)
        msg.setWindowTitle("Author")
        msg.setText(
            "Character Parameter Editor 1.0 by <a href=https://www.youtube.com/channel/UCkZajFypIgQL6mI6OZLEGXw>adsl13</a>")
        msg.exec()

    @staticmethod
    def action_credits_logic():
        msg = QMessageBox()
        msg.setTextFormat(1)
        msg.setWindowTitle("Credits")
        msg.setText('<ul>'
                    '<li>To <b>revelation (revel8n) </b> from <a ''href=https://forum.xentax.com>XeNTaX</a> '
                    'forum who made the compress/uncompress tool <i>dbrb_compressor.exe</i>.</li>'
                    '<li>To the <a ''href=https://discord.gg/tBmcwkGUE6>Raging Blast Modding community</a>.</li>'
                    '</ul>')
        msg.exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()