import cv2
import numpy as np

def frame_to_led_bytes(frame):
    #resising to 8x8
    small_frame = cv2.resize(frame, (8, 8), interpolation=cv2.INTER_AREA)
    #grayscaling
    gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
    #clamping to B&W
    _, bw = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    #converting frame to LED
    bytes_list = []
    for row in bw:
        byte = 0
        for i, pixel in enumerate(row):
            #white pixels ON
            if pixel == 255:
                byte |= (1 << (7 - i))
        bytes_list.append(f'B{byte:08b}')

    return bytes_list

def process_video(video_path, output_txt_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    saved_count = 0
    all_frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        #skipping every 2nd frame (low RP2040 memory)
        #remove if statement and its block indentation for all frames
        if frame_count % 2 == 0:
            led_bytes = frame_to_led_bytes(frame)
            all_frames.append(led_bytes)
            saved_count += 1

        frame_count += 1

    cap.release()

    #saving the frames as an array of 8-byte-arrays (array of 8x8 pixels)
    with open(output_txt_path, 'w') as f:
        f.write(f'byte all_frames[{saved_count}][8] = {{\n')
        for frame in all_frames:
            f.write('  {\n')
            for b in frame:
                f.write(f'    {b},\n')
            f.write('  },\n')
        f.write('};\n')

    print(f'Done! Wrote {saved_count} frames to {output_txt_path}')


process_video("YOUR_VIDEO_NAME_HERE.mp4", "frames_8x8_15_FPS.txt")