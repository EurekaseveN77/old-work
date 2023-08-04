#James Carton
#April 16th, 2023

def convert(frame_num):
    hours = int(frame_num / (24 * 60 * 60))
    minutes = int(frame_num / (24 * 60)) % 60
    seconds = int(frame_num / 24) % 60
    frames = frame_num % 24
    timecode = '{:02d}:{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds, frames)
    return timecode

frame_num = int(input("Enter a frame number: "))
timecode = convert(frame_num)
print("There are", frame_num, "frames in", timecode)

