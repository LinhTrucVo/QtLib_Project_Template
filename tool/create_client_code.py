# command to build onefile executable
# pyinstaller --onefile Copy_This_File_To_Client_Code_To_Create_Client_Code.py

import sys
import os
import shutil
import glob

if len(sys.argv) == 1:
    from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
    from PySide6 import QtCore, QtGui
    from PySide6.QtGui import *
    from PySide6.QtCore import *

# Function to rename multiple files
def createTaskCode(src_task_name, dst_task_name):
    if os.path.exists(dst_task_name):
        shutil.rmtree(os.getcwd() + "/" + dst_task_name)

    src_folder = os.getcwd() + "/" + src_task_name
    dst_folder = os.getcwd() + "/" + dst_task_name

    shutil.copytree(src_folder, dst_folder)
    # Remove __pycache__ directories from destination folder
    for root, dirs, files in os.walk(dst_folder):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            shutil.rmtree(pycache_path)

    # Process files recursively in all subdirectories
    for root, dirs, files in os.walk(dst_folder):
        # Skip __pycache__ directories
        for filename in files:
            print(filename)
            if filename != os.path.basename(__file__):
                full_file_name = os.path.join(root, filename)
                if os.path.isfile(full_file_name):
                    file = open(full_file_name)
                    file_content = file.read()
                    new_file_content = file_content.replace(src_task_name, dst_task_name)
                    new_file_content = new_file_content.replace(src_task_name.upper(), dst_task_name.upper())
                    file.close()

                    file = open(full_file_name, "w+")
                    file.write(new_file_content)
                    file.close()

                    temp_str = full_file_name.replace(src_task_name, dst_task_name)
                    os.rename(full_file_name, temp_str)

    if len(sys.argv) == 1:
        QApplication.instance().quit()

def main():
    if len(sys.argv) == 1:
        app = QApplication(sys.argv)
        win = QMainWindow()
        win.setGeometry(500, 350, 265, 150)
        win.setWindowTitle("Create Client Code")

        label_1 = QLabel("Name", win)
        label_1.setGeometry(5, 5, 100, 15)

        line_edit = QLineEdit("Task_1", win)
        line_edit.setGeometry(label_1.x(), label_1.y() + 20, 200, 30)
        line_edit.setCursorPosition(0)

        label_2 = QLabel("Copy from", win)
        label_2.setGeometry(label_1.x(), label_1.y() + 70, 300, 15)

        line_edit_1 = QLineEdit("Bico_QUIThread_Sample", win)
        line_edit_1.setGeometry(label_1.x(), label_2.y() + 20, 200, 30)
        line_edit_1.setCursorPosition(0)

        button_1 = QPushButton("Submit", win)
        button_1.setGeometry(line_edit_1.x() + line_edit_1.width() + 5, line_edit_1.y(), 50, 30)
        button_1.clicked.connect(lambda: createTaskCode(line_edit_1.text(), line_edit.text()))

        win.show()
        sys.exit(app.exec())

    else:
        createTaskCode(sys.argv[1])

# Driver Code
if __name__ == '__main__':
    # Calling main() function
    main()
