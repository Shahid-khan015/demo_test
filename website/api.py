from flask import Blueprint , jsonify
import pandas as pd
import cv2 , base64
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
import random
import numpy as np
import imageio


api = Blueprint('api' , __name__)

@api.route('/', methods=['GET', 'POST'])
def addition_api():
    output_path = r"website\DataSet\Output\mereg.mp4"
    
    num1 = random.randint(0, 10)
    num2 = random.randint(0, 10)

    add = num1 + num2
    df = pd.read_csv(r'website\static\number.csv')
    op = pd.read_csv(r'website\static\operator.csv')

    filtered_df1 = df[df['Number'] == num1]
    filtered_op = op[op['Operator'] == '+']
    filtered_df2 = df[df['Number'] == num2]
    filtered_sum = df[df['Number'] == add]

    filtered_df = [filtered_df1, filtered_op,  filtered_df2, filtered_sum]

    found_links = False
    folder_path = []
    for fd in filtered_df:
        if not fd.empty:
            found_links = True

            for link in fd['Links']:
                folder_path.append(link)

    if not found_links:
        print(f"No links found for the specified numbers.")

    video_extensions = ('.mp4', '.avi', '.mov', '.mkv')

    def video_return(video_path):
        try:
            reader = imageio.get_reader(video_path)
        except Exception as e:
            return jsonify({"error": f"Could not open video: {str(e)}"})

        frames_list = []

        for frame in reader:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # frame = cv2.resize(frame, (128, 128))
           
            _, buffer = cv2.imencode('.png', frame)
            encoded_image = base64.b64encode(buffer).decode('utf-8')
            
            frames_list.append(encoded_image)

        return jsonify({"data": frames_list})

    def merge_videos(video_path, output_path):

        clip = [VideoFileClip(video_path) for video_path in video_path]

        merged_clip = concatenate_videoclips(clip)
        merged_clip.write_videofile(output_path, codec='libx264')

        # for frame in merged_clip.iter_frames(fps=60, dtype='uint8'):
        #     yield frame

    video_files = []
    for folder in folder_path:
        if os.path.isdir(folder):
            files = [f for f in os.listdir(
                folder) if f.endswith(video_extensions)]
            video_files.extend(os.path.join(folder, f) for f in files)

    # merge_videos(video_files, output_path)

    return video_return(output_path)

