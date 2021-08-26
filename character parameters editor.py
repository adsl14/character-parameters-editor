import os
import stat
import functools

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
path_small_images = os.path.join("lib", "images", "small")
path_large_images = os.path.join("lib", "images", "large")
path_fourSlot_images = os.path.join("lib", "images", "fourSlot")
path_small_four_slot_images = os.path.join(path_fourSlot_images, "small")

# base position transformations
base_pos_trans = 66723

# number of bytes between each character
sizeTrans = 33

# panelPortraistlist
mini_portraits_image = []

# portraits object for the Select Character window
chara_selected_character_window = 100
mini_portraits_image_select_chara_window = []

# List of character with their data from the file
character_list = []
chara_selected = 0  # Index of the char selected in the program
trans_slot_panel_selected = 0  # Slot thas is being edited
# Array of the characters that has been edited
character_list_edited = []

# Store what character has original transform version
characters_with_trans = [0, 5, 8, 17, 22, 24, 27, 29, 31, 34, 40, 48, 58, 63, 67, 79, 82, 85, 88]
# Store what transformations has the character originally
characters_with_trans_index = [[1, 2, 3], [6, 7], [9, 10], [18, 19, 20], [23], [25, 26], [28], [30], [32, 33],
                               [35], [41], [49, 50, 51, 52], [59, 60, 61], [64, 65], [68, 69], [80], [83], [86], [89]]


def del_rw(name_method, path, error):
    os.chmod(path, stat.S_IWRITE)
    os.remove(path)

    return name_method, error


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):

        global mini_portraits_image, mini_portraits_image_select_chara_window

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
        mini_portraits_image = self.panel.findChildren(QLabel)

        for i in range(0, 62):
            index_chara = mini_portraits_image[i].objectName().split("_")[1]
            mini_portraits_image[i].setPixmap(QPixmap(os.path.join(path_small_images, "sc_chara_0" +
                                                                   index_chara + ".bmp")))
            mini_portraits_image[i].setStyleSheet("QLabel {border : 3px solid grey;}")
            mini_portraits_image[i].mousePressEvent = functools.partial(self.action_change_character,
                                                                        index=int(index_chara),
                                                                        modify_slot_transform=True)
            mini_portraits_image[i].setDisabled(True)

        for i in range(62, len(mini_portraits_image)):
            mini_portraits_image[i].setStyleSheet("QLabel {border : 3px solid grey;}")
            mini_portraits_image[i].setVisible(False)

        # Set the the main image
        self.portrait.setVisible(False)

        # Set the transform panel invisible
        self.transPanel.setPixmap(QPixmap(os.path.join(path_fourSlot_images, "pl_transform.png")))
        self.transPanel.setVisible(False)

        # Load the Select Chara window
        self.selectCharaWindow = QtWidgets.QMainWindow()
        self.selectCharaUI = Ui_Dialog()
        self.selectCharaUI.setupUi(self.selectCharaWindow)
        mini_portraits_image_select_chara_window = self.selectCharaUI.frame.findChildren(QLabel)
        for i in range(0, 100):
            mini_portraits_image_select_chara_window[i].setPixmap(QPixmap(os.path.join(path_small_images,
                                                                                       "sc_chara_0" +
                                                                                       str(i).zfill(2) + ".bmp")))
            mini_portraits_image_select_chara_window[i].mousePressEvent = functools.partial(
                self.action_edit_transformation, char_selected_new=i)

    def action_edit_transformation(self, event, char_selected_new):

        global chara_selected, trans_slot_panel_selected

        # If the selected character in the window is the same as in the panel transformations,
        # we assume there won't be any transformation in that slot
        # so it will be 100
        if character_list[chara_selected].transformations[trans_slot_panel_selected] == char_selected_new:
            char_selected_new = 100

        # Change the transformation in our array of characters
        character_list[chara_selected].transformations[trans_slot_panel_selected] = char_selected_new

        # Change the visual transformation
        if trans_slot_panel_selected == 0:
            self.transSlotPanel0.setPixmap(QPixmap(os.path.join(path_small_four_slot_images, "sc_chara_s_0" +
                                                                str(char_selected_new).zfill(2) + ".png")))
            self.transSlotPanel0.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                     index=char_selected_new, trans_slot_panel_index=0)
        elif trans_slot_panel_selected == 1:
            self.transSlotPanel1.setPixmap(QPixmap(os.path.join(path_small_four_slot_images, "sc_chara_s_0" +
                                                                str(char_selected_new).zfill(2) + ".png")))
            self.transSlotPanel1.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                     index=char_selected_new, trans_slot_panel_index=1)
        elif trans_slot_panel_selected == 2:
            self.transSlotPanel2.setPixmap(QPixmap(os.path.join(path_small_four_slot_images, "sc_chara_s_0" +
                                                                str(char_selected_new).zfill(2) + ".png")))
            self.transSlotPanel2.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                     index=char_selected_new, trans_slot_panel_index=2)
        elif trans_slot_panel_selected == 3:
            self.transSlotPanel3.setPixmap(QPixmap(os.path.join(path_small_four_slot_images, "sc_chara_s_0" +
                                                                str(char_selected_new).zfill(2) + ".png")))
            self.transSlotPanel3.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                     index=char_selected_new, trans_slot_panel_index=3)

        # If the character was edited before, we won't append the index to our array of characters edited once
        if character_list[chara_selected] not in character_list_edited:
            character_list_edited.append(character_list[chara_selected])

        self.selectCharaWindow.close()

    def action_change_character(self, event, index=None, modify_slot_transform=False):

        global chara_selected

        # Change only if the char selected is other
        if chara_selected != index:

            # Load the portrait
            self.portrait.setPixmap(QPixmap(os.path.join(path_large_images, "chara_up_chips_l_0" +
                                                         str(index).zfill(2) + ".png")))

            # Load the transformations for the panel transformations
            transformations = character_list[index].transformations
            # Change panel transformations and their interactions
            if transformations[0] != 100:
                self.transSlotPanel0.setPixmap(QPixmap(os.path.join(path_small_four_slot_images, "sc_chara_s_0" +
                                                                    str(transformations[0]).zfill(2) + ".png")))
                self.transSlotPanel0.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                         index=transformations[0],
                                                                         trans_slot_panel_index=0)
                self.transSlotPanel0.setVisible(True)
            else:
                self.transSlotPanel0.setPixmap(QPixmap())
                self.transSlotPanel0.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                         index=100, trans_slot_panel_index=0)
            if transformations[1] != 100:
                self.transSlotPanel1.setPixmap(QPixmap(os.path.join(path_small_four_slot_images, "sc_chara_s_0" +
                                                                    str(transformations[1]).zfill(2) + ".png")))
                self.transSlotPanel1.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                         index=transformations[1],
                                                                         trans_slot_panel_index=1)
                self.transSlotPanel1.setVisible(True)
            else:
                self.transSlotPanel1.setPixmap(QPixmap())
                self.transSlotPanel1.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                         index=100, trans_slot_panel_index=1)
            if transformations[2] != 100:
                self.transSlotPanel2.setPixmap(QPixmap(os.path.join(path_small_four_slot_images, "sc_chara_s_0" +
                                                                    str(transformations[2]).zfill(2) + ".png")))
                self.transSlotPanel2.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                         index=transformations[2],
                                                                         trans_slot_panel_index=2)
                self.transSlotPanel2.setVisible(True)
            else:
                self.transSlotPanel2.setPixmap(QPixmap())
                self.transSlotPanel2.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                         index=100, trans_slot_panel_index=2)
            if transformations[3] != 100:
                self.transSlotPanel3.setPixmap(QPixmap(os.path.join(path_small_four_slot_images, "sc_chara_s_0" +
                                                                    str(transformations[3]).zfill(2) + ".png")))
                self.transSlotPanel3.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                         index=transformations[3],
                                                                         trans_slot_panel_index=3)
                self.transSlotPanel3.setVisible(True)
            else:
                self.transSlotPanel3.setPixmap(QPixmap())
                self.transSlotPanel3.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                         index=100, trans_slot_panel_index=3)

            # Modify the slots of the transformations in the main panel
            if modify_slot_transform:

                # Disable all the transformations of the slots if it has been activated in the main panel
                if self.label_trans_0.isVisible():
                    self.label_trans_0.setVisible(False)
                    self.label_trans_1.setVisible(False)
                    self.label_trans_2.setVisible(False)
                    self.label_trans_3.setVisible(False)

                # Get the original transformations for the character
                if index in characters_with_trans:
                    transformations = characters_with_trans_index[characters_with_trans.index(index)]
                    num_transformations = len(transformations)
                    if num_transformations > 0:
                        self.label_trans_0.setPixmap(QPixmap(os.path.join(path_small_images, "sc_chara_0" +
                                                                          str(transformations[0]).zfill(2) + ".bmp")))
                        self.label_trans_0.mousePressEvent = functools.partial(self.action_change_character,
                                                                               index=transformations[0],
                                                                               modify_slot_transform=False)
                        self.label_trans_0.setVisible(True)
                        if num_transformations > 1:
                            self.label_trans_1.setPixmap(QPixmap(os.path.join(path_small_images, "sc_chara_0" +
                                                                              str(transformations[1]).zfill(2) +
                                                                              ".bmp")))
                            self.label_trans_1.mousePressEvent = functools.partial(self.action_change_character,
                                                                                   index=transformations[1],
                                                                                   modify_slot_transform=False)
                            self.label_trans_1.setVisible(True)
                            if num_transformations > 2:
                                self.label_trans_2.setPixmap(QPixmap(os.path.join(path_small_images, "sc_chara_0" +
                                                                                  str(transformations[2]).zfill(2) +
                                                                                  ".bmp")))
                                self.label_trans_2.mousePressEvent = functools.partial(self.action_change_character,
                                                                                       index=transformations[2],
                                                                                       modify_slot_transform=False)
                                self.label_trans_2.setVisible(True)
                                if num_transformations > 3:
                                    self.label_trans_3.setPixmap(QPixmap(os.path.join(path_small_images,
                                                                                      "sc_chara_0" +
                                                                                      str(transformations[3]).zfill(2) +
                                                                                      ".bmp")))
                                    self.label_trans_3.mousePressEvent = functools.partial(self.action_change_character,
                                                                                           index=transformations[3],
                                                                                           modify_slot_transform=False)
                                    self.label_trans_3.setVisible(True)                                                                

            # Store the actual index selected of the char
            chara_selected = index

    def action_open_logic(self):

        global temp_folder, mini_portraits_image, character_list, pak_file_path_original, pak_file_path
        global chara_selected, character_list_edited, character_list

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
                msg.setText("Selected file is not the correct one.")
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

        # reset the values
        character_list_edited.clear()
        character_list.clear()
        chara_selected = 0  # Index of the char selected in the program

        # Read the file
        with open(pak_file_path, mode="rb") as pak_file:

            # Read the data from the file
            for i in range(0, 100):
                character = Character()
                character.positionTrans = base_pos_trans + (i * sizeTrans)
                pak_file.seek(character.positionTrans)

                # Transformation 1
                character.transformations.append(int.from_bytes(pak_file.read(1), byteorder='little'))
                # Transformation 2
                character.transformations.append(int.from_bytes(pak_file.read(1), byteorder='little'))
                # Transformation 3
                character.transformations.append(int.from_bytes(pak_file.read(1), byteorder='little'))
                # Transformation 4
                character.transformations.append(int.from_bytes(pak_file.read(1), byteorder='little'))

                character_list.append(character)

        # Enable the characters portraits
        for i in range(0, 62):
            mini_portraits_image[i].setEnabled(True)

        # Show the large portrait
        self.portrait.setPixmap(QPixmap(os.path.join(path_large_images, "chara_up_chips_l_000.png")))
        self.portrait.setVisible(True)

        # Show the transformations in the main panel
        transformations = character_list[0].transformations
        self.label_trans_0.setPixmap(QPixmap(os.path.join(path_small_images, "sc_chara_0" +
                                                          str(transformations[0]).zfill(2) + ".bmp")))
        self.label_trans_0.mousePressEvent = functools.partial(self.action_change_character,
                                                               index=transformations[0], modify_slot_transform=False)
        self.label_trans_1.setPixmap(QPixmap(os.path.join(path_small_images, "sc_chara_0" +
                                                          str(transformations[1]).zfill(2) + ".bmp")))
        self.label_trans_1.mousePressEvent = functools.partial(self.action_change_character,
                                                               index=transformations[1], modify_slot_transform=False)
        self.label_trans_2.setPixmap(QPixmap(os.path.join(path_small_images, "sc_chara_0" +
                                                          str(transformations[2]).zfill(2) + ".bmp")))
        self.label_trans_2.mousePressEvent = functools.partial(self.action_change_character,
                                                               index=transformations[2], modify_slot_transform=False)
        self.label_trans_0.setVisible(True)
        self.label_trans_1.setVisible(True)
        self.label_trans_2.setVisible(True)

        # Show the transform panel
        self.transText.setPixmap(QPixmap(os.path.join(path_fourSlot_images, "tx_transform_US.png")))
        self.transSlotPanel0.setPixmap(QPixmap(os.path.join(path_small_four_slot_images, "sc_chara_s_0" +
                                                            str(transformations[0]).zfill(2) + ".png")))
        self.transSlotPanel0.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                 index=transformations[0], trans_slot_panel_index=0)
        self.transSlotPanel1.setPixmap(QPixmap(os.path.join(path_small_four_slot_images, "sc_chara_s_0" +
                                                            str(transformations[1]).zfill(2) + ".png")))
        self.transSlotPanel1.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                 index=transformations[1], trans_slot_panel_index=1)
        self.transSlotPanel2.setPixmap(QPixmap(os.path.join(path_small_four_slot_images, "sc_chara_s_0" +
                                                            str(transformations[2]).zfill(2) + ".png")))
        self.transSlotPanel2.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                 index=transformations[2], trans_slot_panel_index=2)
        self.transSlotPanel3.setPixmap(QPixmap(os.path.join(path_small_four_slot_images, "sc_chara_s_0" +
                                                            str(transformations[3]).zfill(2) + ".png")))
        self.transSlotPanel3.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                 index=transformations[3], trans_slot_panel_index=3)
        self.transPanel.setVisible(True)

    def open_select_chara_window(self, event, index, trans_slot_panel_index):

        global chara_selected_character_window, trans_slot_panel_selected

        # Store in a global var what slot in the transformation panel has been selected
        trans_slot_panel_selected = trans_slot_panel_index

        # Avoid adding the red border to the character transform selected
        if chara_selected_character_window != index:
            # If the index is 100 (means there's no character transformation),
            # we will remove the red border for the previous character transform panel
            if index == 100:
                mini_portraits_image_select_chara_window[chara_selected_character_window].setStyleSheet("QLabel {}")
            else:
                mini_portraits_image_select_chara_window[index].setStyleSheet("QLabel {border : 3px solid red;}")
                if chara_selected_character_window != 100:
                    mini_portraits_image_select_chara_window[chara_selected_character_window].setStyleSheet("QLabel {}")
                
            chara_selected_character_window = index
        self.selectCharaWindow.show()

    def action_save_logic(self):

        global character_list_edited, pak_file_path, pak_file_path_original

        # If the user has edited one character, we will save
        if character_list_edited:

            # Create the output name
            basename = os.path.basename(pak_file_path_original).replace(".pak",
                                                                        datetime.now().strftime("_%d-%m-%Y_%H-%M-%S"))

            # Ask to the user where to save the file
            path_output_file = QFileDialog.getSaveFileName(self, "Save file",
                                                           os.path.abspath(os.path.join(os.getcwd(), basename)),
                                                           "PAK files (*.pak)")[0]

            if path_output_file:

                pak_export_path = pak_file_path.replace(".pak", "_m.pak")
                copyfile(pak_file_path, pak_export_path)

                # We open the file decrypted
                with open(pak_export_path, mode="rb+") as file:

                    # Change the transformations in the file
                    for character in character_list_edited:
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
                    os.system('explorer.exe ' + os.path.dirname(path_output_file).replace("/", "\\"))

        else:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText("The file hasn't been modified.")
            msg.exec()

    def closeEvent(self, event):
        if os.path.exists(temp_folder):
            rmtree(temp_folder, onerror=del_rw)

        if not self.selectCharaWindow.isHidden():
            self.selectCharaWindow.setVisible(False)

        event.accept()

    @staticmethod
    def action_author_logic():
        msg = QMessageBox()
        msg.setTextFormat(1)
        msg.setWindowTitle("Author")
        msg.setText(
            "character parameters editor 1.0 by "
            "<a href=https://www.youtube.com/channel/UCkZajFypIgQL6mI6OZLEGXw>adsl13</a>")
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
