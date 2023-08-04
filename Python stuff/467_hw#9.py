#James Carton
#April 30th, 2023
import subprocess

input_file = "C:/Users/jmscr/Downloads/twitch_nft_demo.mp4"
output_file = "C:/Users/jmscr/Downloads/twitch_nft_demo.avi"

info_command = ['ffmpeg', '-i', input_file]
info_result = subprocess.run(info_command, capture_output=True, text=True)
print(info_result.stdout)

convert_command = ['ffmpeg', '-i', input_file, output_file]
subprocess.run(convert_command)
