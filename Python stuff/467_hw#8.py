import subprocess
import shlex

# Set the path to your desktop
desktop_path = "C:\\Users\\jmscr\\OneDrive\\Desktop"

# Call the ls command with the -l argument on the desktop folder
command = f'ls -l "{desktop_path}"'
process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# Parse the output of the ls command to find the largest file
largest_file = None
largest_file_size = 0
for line in iter(process.stdout.readline, b''):
    parts = line.split()
    if len(parts) < 5:
        continue
    size = int(parts[4])
    if size > largest_file_size:
        largest_file = parts[-1]
        largest_file_size = size

# Print the name and size of the largest file
print(f"The largest file on your desktop is '{largest_file}' with a size of {largest_file_size} bytes.")
