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
    # Check if we're running from within the source task directory
    current_dir_name = os.path.basename(os.getcwd())
    if current_dir_name == src_task_name:
        # We're inside the source directory, go up one level to find the parent
        parent_dir = os.path.dirname(os.getcwd())
        src_folder = os.path.join(parent_dir, src_task_name)
        dst_folder = os.path.join(parent_dir, dst_task_name)
    else:
        # We're in the parent directory containing the source folder
        src_folder = os.path.join(os.getcwd(), src_task_name)
        dst_folder = os.path.join(os.getcwd(), dst_task_name)

    # Check if source folder exists
    if not os.path.exists(src_folder):
        print(f"Error: Source folder '{src_folder}' does not exist!")
        return

    # Remove destination folder if it exists
    if os.path.exists(dst_folder):
        shutil.rmtree(dst_folder)

    print(f"Copying from: {src_folder}")
    print(f"Copying to: {dst_folder}")
    
    shutil.copytree(src_folder, dst_folder)
    # Remove __pycache__ directories from destination folder
    for root, dirs, files in os.walk(dst_folder):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            shutil.rmtree(pycache_path)

    # First, rename directories from bottom to top
    dirs_to_rename = []
    for root, dirs, files in os.walk(dst_folder):
        for dirname in dirs:
            if src_task_name in dirname:
                old_dir_path = os.path.join(root, dirname)
                new_dir_name = dirname.replace(src_task_name, dst_task_name)
                new_dir_path = os.path.join(root, new_dir_name)
                dirs_to_rename.append((old_dir_path, new_dir_path))
    
    # Sort by depth (deepest first) to avoid conflicts
    dirs_to_rename.sort(key=lambda x: x[0].count(os.sep), reverse=True)
    
    # Rename directories
    for old_path, new_path in dirs_to_rename:
        if os.path.exists(old_path):
            print(f"Renaming directory: {old_path} -> {new_path}")
            os.rename(old_path, new_path)

    # Process files recursively in all subdirectories
    for root, dirs, files in os.walk(dst_folder):
        # Skip __pycache__ directories
        for filename in files:
            print(filename)
            if filename != os.path.basename(__file__):
                full_file_name = os.path.join(root, filename)
                if os.path.isfile(full_file_name):
                    # Update file content
                    with open(full_file_name, 'r', encoding='utf-8', errors='ignore') as file:
                        file_content = file.read()
                    
                    new_file_content = file_content.replace(src_task_name, dst_task_name)
                    new_file_content = new_file_content.replace(src_task_name.upper(), dst_task_name.upper())
                    
                    with open(full_file_name, 'w', encoding='utf-8') as file:
                        file.write(new_file_content)

                    # Rename file if filename contains src_task_name
                    if src_task_name in filename:
                        new_filename = filename.replace(src_task_name, dst_task_name)
                        new_full_path = os.path.join(root, new_filename)
                        print(f"Renaming file: {full_file_name} -> {new_full_path}")
                        os.rename(full_file_name, new_full_path)

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

        line_edit = QLineEdit("Task2", win)
        line_edit.setGeometry(label_1.x(), label_1.y() + 20, 200, 30)
        line_edit.setCursorPosition(0)

        label_2 = QLabel("Copy from", win)
        label_2.setGeometry(label_1.x(), label_1.y() + 70, 300, 15)

        line_edit_1 = QLineEdit("Task1", win)
        line_edit_1.setGeometry(label_1.x(), label_2.y() + 20, 200, 30)
        line_edit_1.setCursorPosition(0)

        button_1 = QPushButton("Submit", win)
        button_1.setGeometry(line_edit_1.x() + line_edit_1.width() + 5, line_edit_1.y(), 50, 30)
        button_1.clicked.connect(lambda: createTaskCode(line_edit_1.text(), line_edit.text()))

        win.show()
        sys.exit(app.exec())

    else:
        if len(sys.argv) >= 3:
            createTaskCode(sys.argv[1], sys.argv[2])
        else:
            print("Usage: python create_client_code.py <source_task_name> <destination_task_name>")
            print("Example: python create_client_code.py Task_1 Task_2")

# Driver Code
if __name__ == '__main__':
    # Calling main() function
    main()
