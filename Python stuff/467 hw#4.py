#James Carton
#March 12th, 2023
with open("lesson4_folderexample.txt", "r") as f:
    lines = f.readlines()

for line in lines:
    original_line = line.rstrip()
    line = ''.join(original_line.split())
    if original_line == line:
        print(f"'{original_line}' was fine.")
    else:
        print(f"'{line}' needed to be fixed.")
