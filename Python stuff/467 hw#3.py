#James Carton
#March 5th, 2023
import os
import time

folder_path = "C:/Users/jmscr/OneDrive/Documents/coding/Python/week3"

files = set(os.listdir(folder_path))

while True:
    time.sleep(1)
    updated_files = set(os.listdir(folder_path))
    new_files = updated_files - files

    for file in new_files:
        file_path = os.path.join(folder_path, file)
        file_type = os.path.splitext(file)[1]
        file_time = time.ctime(os.path.getmtime(file_path))
        print(f"New file added: {file} ({file_type}) at {file_time}")

    files = updated_files
