import os, stat, functools

from shutil import rmtree, copyfile
from datetime import datetime
from lib.design.character_parameters_editor_design import *
from lib.design.select_chara import Ui_Dialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QFileDialog, QMessageBox
from lib.classes.Character import Character

# Temp folder name
temp_folder = "temp_" + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S")
# Path files
pak_file_path_original = ""
pak_file_path = ""

# resources path
dbrb_compressor_path = os.path.join("lib", "resources", "dbrb_compressor.exe")

# path images
path_little_images = os.path.join("lib","images","little")
path_little2_images = os.path.join("lib","images","little2")
path_large_images = os.path.join("lib","images","large")
path_fourSlot_images = os.path.join("lib","images","fourSlot")

# base position transformations
basePosTrans = 66723

# number of bytes between each character
sizeTrans = 33

# panelPortraistlist
miniPortraitsImage = []

# portraits object for the Select Character window
charaSelectedCharacterWindow = 100
miniPortraitsImageSelectCharaWindow = []

# List of character with their data from the file
characterList = []
charaSelected = 0 # Index of the char selected in the program
transSlotPanelSelected = 0 # Slot thas is being edited
# Array of the characters that was being edited
characterListEdited = []

 # Store what character has original transform version
charactersWithTrans = [0, 5, 8, 17, 22, 24, 27, 29, 31, 34, 40, 48, 58, 63, 67, 79, 82, 85, 88]
# Store what transformations has the character originally
charactersWithTransIndex = [[1,2,3], [6, 7], [9, 10], [18, 19, 20], [23], [25, 26], [28], [30], [32,33], 
[35], [41], [49, 50, 51, 52], [59, 60, 61], [64, 65], [68, 69], [80], [83], [86], [89]]

def del_rw(name_method, path, error):
    os.chmod(path, stat.S_IWRITE)
    os.remove(path)

    return name_method, error

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):

        global miniPortraitsImage, miniPortraitsImageSelectCharaWindow

        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # File tab
        self.actionOpen.triggered.connect(self.action_open_logic)
        self.actionSave.triggered.connect(self.action_save_logic)
        self.actionClose.triggered.connect(self.close)

        # About tab
        self.actionAuthor.triggered.connect(self.action_author_logic)
        self.actionCredits.triggered.connect(self.action_credits_logic)

        # Load all the mini portraits (main panel)
        miniPortraitsImage = self.panel.findChildren(QLabel)
        index = 0
        for i in range(0,62):
            indexChara = miniPortraitsImage[i].objectName().split("_")[1]
            miniPortraitsImage[i].setPixmap(QPixmap(os.path.join(path_little_images, "sc_chara_0" + indexChara + ".bmp")))
            miniPortraitsImage[i].setStyleSheet("QLabel {border : 3px solid grey;}")
            miniPortraitsImage[i].mousePressEvent = functools.partial(self.action_change_character, index=int(indexChara), modifySlotTransform=True)
            miniPortraitsImage[i].setDisabled(True)

        for i in range(62, len(miniPortraitsImage)):
        	miniPortraitsImage[i].setStyleSheet("QLabel {border : 3px solid grey;}")
        	miniPortraitsImage[i].setVisible(False)

        # Set the the main image
        self.portrait.setVisible(False)

        # Set the transform panel invisible
        self.transPanel.setPixmap(QPixmap(os.path.join(path_fourSlot_images, "pl_transform.png")))
        self.transPanel.setVisible(False)

        # Load the Select Chara window
        self.selectCharaWindow = QtWidgets.QMainWindow()
        self.selectCharaUI = Ui_Dialog()
        self.selectCharaUI.setupUi(self.selectCharaWindow)
        miniPortraitsImageSelectCharaWindow = self.selectCharaUI.frame.findChildren(QLabel)
        for i in range(0,100):
            miniPortraitsImageSelectCharaWindow[i].setPixmap(QPixmap(os.path.join(path_little_images, "sc_chara_0" + str(i).zfill(2) + ".bmp")))
            miniPortraitsImageSelectCharaWindow[i].mousePressEvent = functools.partial(self.action_edit_transformation, charSelectedNew = i)

    def action_edit_transformation(self, event, charSelectedNew):

        global charaSelected, transSlotPanelSelected

        # If the selected character in the window is the same as in the panel transformations, we assume there won't be any transformation in that slot
        # so it will be 100
        if characterList[charaSelected].transformations[transSlotPanelSelected] ==  charSelectedNew:
            charSelectedNew = 100

        # Change the transformation in our array of characters
        characterList[charaSelected].transformations[transSlotPanelSelected] = charSelectedNew

        # Change the visual transformation
        if transSlotPanelSelected == 0:
            self.transSlotPanel0.setPixmap(QPixmap(os.path.join(path_little2_images, "sc_chara_s_0" + str(charSelectedNew).zfill(2) + ".png")))
            self.transSlotPanel0.mousePressEvent = functools.partial(self.open_select_chara_window, index=charSelectedNew, transSlotPanelIndex=0)
        elif transSlotPanelSelected == 1:
            self.transSlotPanel1.setPixmap(QPixmap(os.path.join(path_little2_images, "sc_chara_s_0" + str(charSelectedNew).zfill(2) + ".png")))
            self.transSlotPanel1.mousePressEvent = functools.partial(self.open_select_chara_window, index=charSelectedNew, transSlotPanelIndex=1)
        elif transSlotPanelSelected == 2:
            self.transSlotPanel2.setPixmap(QPixmap(os.path.join(path_little2_images, "sc_chara_s_0" + str(charSelectedNew).zfill(2) + ".png")))
            self.transSlotPanel2.mousePressEvent = functools.partial(self.open_select_chara_window, index=charSelectedNew, transSlotPanelIndex=2)
        elif transSlotPanelSelected == 3:
            self.transSlotPanel3.setPixmap(QPixmap(os.path.join(path_little2_images, "sc_chara_s_0" + str(charSelectedNew).zfill(2) + ".png")))
            self.transSlotPanel3.mousePressEvent = functools.partial(self.open_select_chara_window, index=charSelectedNew, transSlotPanelIndex=3)

        # If the character was edited before, we won't append the index to our array of characters edited once
        if characterList[charaSelected] not in characterListEdited:
            characterListEdited.append(characterList[charaSelected])

        self.selectCharaWindow.close()


    def action_change_character(self, event, index=None, modifySlotTransform=False):

        global charaSelected

        # Change only if the char selected is other
        if charaSelected != index:

            # Load the portrait
            self.portrait.setPixmap(QPixmap(os.path.join(path_large_images, "chara_up_chips_l_0" + str(index).zfill(2) + ".png")))

            # Load the transformations for the panel transformations
            transformations = characterList[index].transformations
            # Change panel transformations and their interactions
            if transformations[0] != 100:
                self.transSlotPanel0.setPixmap(QPixmap(os.path.join(path_little2_images, "sc_chara_s_0" + str(transformations[0]).zfill(2) + ".png")))
                self.transSlotPanel0.mousePressEvent = functools.partial(self.open_select_chara_window, index=transformations[0], transSlotPanelIndex=0)
                self.transSlotPanel0.setVisible(True)
            else:
                self.transSlotPanel0.setPixmap(QPixmap())
                self.transSlotPanel0.mousePressEvent = functools.partial(self.open_select_chara_window, index=100, transSlotPanelIndex=0)
            if transformations[1] != 100:
                self.transSlotPanel1.setPixmap(QPixmap(os.path.join(path_little2_images, "sc_chara_s_0" + str(transformations[1]).zfill(2) + ".png")))
                self.transSlotPanel1.mousePressEvent = functools.partial(self.open_select_chara_window, index=transformations[1], transSlotPanelIndex=1)
                self.transSlotPanel1.setVisible(True)
            else:
                self.transSlotPanel1.setPixmap(QPixmap())
                self.transSlotPanel1.mousePressEvent = functools.partial(self.open_select_chara_window, index=100, transSlotPanelIndex=1)
            if transformations[2] != 100:
                self.transSlotPanel2.setPixmap(QPixmap(os.path.join(path_little2_images, "sc_chara_s_0" + str(transformations[2]).zfill(2) + ".png")))
                self.transSlotPanel2.mousePressEvent = functools.partial(self.open_select_chara_window, index=transformations[2], transSlotPanelIndex=2)
                self.transSlotPanel2.setVisible(True)
            else:
                self.transSlotPanel2.setPixmap(QPixmap())
                self.transSlotPanel2.mousePressEvent = functools.partial(self.open_select_chara_window, index=100, transSlotPanelIndex=2)
            if transformations[3] != 100:
                self.transSlotPanel3.setPixmap(QPixmap(os.path.join(path_little2_images, "sc_chara_s_0" + str(transformations[3]).zfill(2) + ".png")))
                self.transSlotPanel3.mousePressEvent = functools.partial(self.open_select_chara_window, index=transformations[3], transSlotPanelIndex=3)
                self.transSlotPanel3.setVisible(True)
            else:
                self.transSlotPanel3.setPixmap(QPixmap())
                self.transSlotPanel3.mousePressEvent = functools.partial(self.open_select_chara_window, index=100, transSlotPanelIndex=3)                                           

            # Modify the slots of the transformations in the main panel
            if modifySlotTransform:

                # Disable all the transformations of the slots if it has been activated in the main panel
                if self.label_trans_0.isVisible():
                    self.label_trans_0.setVisible(False)
                    self.label_trans_1.setVisible(False)
                    self.label_trans_2.setVisible(False)
                    self.label_trans_3.setVisible(False)

                # Get the original transformations for the character
                if index in charactersWithTrans:
                    transformations = charactersWithTransIndex[charactersWithTrans.index(index)]
                    numTransformations = len(transformations)
                    if numTransformations > 0:
                        self.label_trans_0.setPixmap(QPixmap(os.path.join(path_little_images, "sc_chara_0" + str(transformations[0]).zfill(2) + ".bmp")))
                        self.label_trans_0.mousePressEvent = functools.partial(self.action_change_character, index=transformations[0], modifySlotTransform=False)
                        self.label_trans_0.setVisible(True)
                        if numTransformations > 1:
                            self.label_trans_1.setPixmap(QPixmap(os.path.join(path_little_images, "sc_chara_0" + str(transformations[1]).zfill(2) + ".bmp")))
                            self.label_trans_1.mousePressEvent = functools.partial(self.action_change_character, index=transformations[1], modifySlotTransform=False)
                            self.label_trans_1.setVisible(True)
                            if numTransformations > 2:
                                self.label_trans_2.setPixmap(QPixmap(os.path.join(path_little_images, "sc_chara_0" + str(transformations[2]).zfill(2) + ".bmp")))
                                self.label_trans_2.mousePressEvent = functools.partial(self.action_change_character, index=transformations[2], modifySlotTransform=False)
                                self.label_trans_2.setVisible(True)
                                if numTransformations > 3:
                                    self.label_trans_3.setPixmap(QPixmap(os.path.join(path_little_images, "sc_chara_0" + str(transformations[3]).zfill(2) + ".bmp")))
                                    self.label_trans_3.mousePressEvent = functools.partial(self.action_change_character, index=transformations[3], modifySlotTransform=False)
                                    self.label_trans_3.setVisible(True)                                                                


            # Store the actual index selected of the char
            charaSelected = index


    def action_open_logic(self):

        global temp_folder, miniPortraitsImage, characterList, pak_file_path_original, pak_file_path

		# Open pak file
        pak_file_path_original = \
            QFileDialog.getOpenFileName(self, "Open file", os.path.abspath(os.getcwd()), "PAK files (*.pak)")[0]

        # Check if the user has selected a pak format file
        if not os.path.exists(pak_file_path_original):
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("A pak file is needed.")
            msg.exec()
            return

        # Check if the pak file is the correct one
        with open(pak_file_path_original, mode="rb") as pak_file:
            pak_file.seek(78)
            data = pak_file.read(26)
            if data.decode('utf-8') != "operate_resident_param.pak":
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("The file you selected is not the correct one.")
                msg.exec()
                return

        basename = os.path.basename(pak_file_path_original)

        # Create a folder where we store the necessary files or delete it. If already exists,
        # we remove every files in it
        if os.path.exists(temp_folder):
            rmtree(temp_folder, onerror=del_rw)
        os.mkdir(temp_folder)

        # Execute the script in a command line for the pak file
        pak_file_path = os.path.join(os.path.abspath(os.getcwd()), temp_folder, basename.replace(".pak", "_d.pak"))
        args = os.path.join(dbrb_compressor_path) + " \"" + pak_file_path_original + "\" \"" + pak_file_path + "\""
        os.system('cmd /c ' + args)

        # Read the file
        with open(pak_file_path, mode="rb") as pak_file:

            for i in range(0,100):
                character = Character()
                character.positionTrans = basePosTrans + (i * sizeTrans)
                pak_file.seek(character.positionTrans)

                # Transformation 1
                character.transformations.append(int.from_bytes(pak_file.read(1), byteorder='little'))
                 # Transformation 2
                character.transformations.append(int.from_bytes(pak_file.read(1), byteorder='little'))
                 # Transformation 3
                character.transformations.append(int.from_bytes(pak_file.read(1), byteorder='little'))
                 # Transformation 4
                character.transformations.append(int.from_bytes(pak_file.read(1), byteorder='little'))

                characterList.append(character)

        # Enable the characters portraits
        for i in range(0,62):
            miniPortraitsImage[i].setEnabled(True)

        # Show the large portrait
        self.portrait.setPixmap(QPixmap(os.path.join(path_large_images, "chara_up_chips_l_000.png")))
        self.portrait.setVisible(True)

        # Show the transformations in the main panel
        transformations = characterList[0].transformations
        self.label_trans_0.setPixmap(QPixmap(os.path.join(path_little_images, "sc_chara_0" + str(transformations[0]).zfill(2) + ".bmp")))
        self.label_trans_0.mousePressEvent = functools.partial(self.action_change_character, index=transformations[0], modifySlotTransform=False)
        self.label_trans_1.setPixmap(QPixmap(os.path.join(path_little_images, "sc_chara_0" + str(transformations[1]).zfill(2) + ".bmp")))
        self.label_trans_1.mousePressEvent = functools.partial(self.action_change_character, index=transformations[1], modifySlotTransform=False)
        self.label_trans_2.setPixmap(QPixmap(os.path.join(path_little_images, "sc_chara_0" + str(transformations[2]).zfill(2) + ".bmp")))
        self.label_trans_2.mousePressEvent = functools.partial(self.action_change_character, index=transformations[2], modifySlotTransform=False)
        self.label_trans_0.setVisible(True)
        self.label_trans_1.setVisible(True)
        self.label_trans_2.setVisible(True)

        # Show the transform panel
        self.transText.setPixmap(QPixmap(os.path.join(path_fourSlot_images, "tx_transform_US.png")))
        self.transSlotPanel0.setPixmap(QPixmap(os.path.join(path_little2_images, "sc_chara_s_0" + str(transformations[0]).zfill(2) + ".png")))
        self.transSlotPanel0.mousePressEvent = functools.partial(self.open_select_chara_window, index=transformations[0], transSlotPanelIndex=0)
        self.transSlotPanel1.setPixmap(QPixmap(os.path.join(path_little2_images, "sc_chara_s_0" + str(transformations[1]).zfill(2) + ".png")))
        self.transSlotPanel1.mousePressEvent = functools.partial(self.open_select_chara_window, index=transformations[1], transSlotPanelIndex=1)
        self.transSlotPanel2.setPixmap(QPixmap(os.path.join(path_little2_images, "sc_chara_s_0" + str(transformations[2]).zfill(2) + ".png")))
        self.transSlotPanel2.mousePressEvent = functools.partial(self.open_select_chara_window, index=transformations[2], transSlotPanelIndex=2)
        self.transSlotPanel3.setPixmap(QPixmap(os.path.join(path_little2_images, "sc_chara_s_0" + str(transformations[3]).zfill(2) + ".png")))
        self.transSlotPanel3.mousePressEvent = functools.partial(self.open_select_chara_window, index=transformations[3], transSlotPanelIndex=3)
        self.transPanel.setVisible(True)

        # Clean the array of edited characters
        characterListEdited.clear()


    def open_select_chara_window(self, event, index, transSlotPanelIndex):

        global charaSelectedCharacterWindow, transSlotPanelSelected

        # Store in a global var what slot in the transformation panel has been selected
        transSlotPanelSelected = transSlotPanelIndex

        # Avoid adding the red border to the character transform selected
        if charaSelectedCharacterWindow != index:
            # If the index is 100 (means there's no character transformation), we will remove the red border for the previous character transform panel
            if index == 100:
                miniPortraitsImageSelectCharaWindow[charaSelectedCharacterWindow].setStyleSheet("QLabel {}")
            else:
                miniPortraitsImageSelectCharaWindow[index].setStyleSheet("QLabel {border : 3px solid red;}")
                if charaSelectedCharacterWindow != 100:
                    miniPortraitsImageSelectCharaWindow[charaSelectedCharacterWindow].setStyleSheet("QLabel {}")
                
            charaSelectedCharacterWindow = index
        self.selectCharaWindow.show()


    def action_save_logic(self):

        global characterListEdited, pak_file_path, pak_file_path_original

        # If the user has edited one character, we will save
        if characterListEdited:

            # Create the output name
            basename = os.path.basename(pak_file_path_original).replace(".pak", datetime.now().strftime("_%d-%m-%Y_%H-%M-%S"))

            # Ask to the user where to save the file
            path_output_file = QFileDialog.getSaveFileName(self, "Save file", os.path.abspath(os.path.join(os.getcwd(),basename)), "PAK files (*.pak)")[0]

            if path_output_file:

                pak_export_path = pak_file_path.replace(".pak", "_m.pak")
                copyfile(pak_file_path, pak_export_path)

                # We open the file decrypted
                with open(pak_export_path, mode="rb+") as file:

                    # Change the transformations in the file
                    for character in characterListEdited:
                        file.seek(character.positionTrans)
                        for transformation in character.transformations:
                            file.write(transformation.to_bytes(1, byteorder="big"))

                # Generate the final file for the game
                args = os.path.join(dbrb_compressor_path) + " \"" + pak_export_path + "\" \"" \
                    + path_output_file + "\""
                os.system('cmd /c ' + args)

                # Remove the uncompressed modified file
                os.remove(pak_export_path)

                msg = QMessageBox()
                msg.setWindowTitle("Message")
                message = "The file were saved and compressed in: <b>" + path_output_file \
                          + "</b><br><br> Do you wish to open the folder?"
                message_open_saved_files = msg.question(self, '', message, msg.Yes | msg.No)

                # If the users click on 'Yes', it will open the path where the files were saved
                if message_open_saved_files == msg.Yes:
                    # Show the path folder to the user
                    os.system('explorer.exe ' + os.path.dirname(path_output_file).replace("/","\\"))

        else:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText("The file hasn't been modified.")
            msg.exec()


    def closeEvent(self, event):
        if os.path.exists(temp_folder):
            rmtree(temp_folder, onerror=del_rw)
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