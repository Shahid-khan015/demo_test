from flask import Blueprint, jsonify, current_app
import pandas as pd
import cv2
import base64
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
import random
import numpy as np
import imageio
from pathlib import Path

api = Blueprint('api', __name__)

@api.route('/', methods=['GET', 'POST'])
def addition_api():
    # Use Path for cross-platform compatibility
    base_dir = Path(current_app.root_path)
    output_path = base_dir / 'static' / 'output' / 'mereg.mp4'
    
    num1 = random.randint(0, 10)
    num2 = random.randint(0, 10)
    add = num1 + num2

    # Fix CSV paths
    df = pd.read_csv(base_dir / 'static' / 'number.csv')
    op = pd.read_csv(base_dir / 'static' / 'operator.csv')

    filtered_df1 = df[df['Number'] == num1]
    filtered_op = op[op['Operator'] == '+']
    filtered_df2 = df[df['Number'] == num2]
    filtered_sum = df[df['Number'] == add]

    filtered_df = [filtered_df1, filtered_op, filtered_df2, filtered_sum]

    folder_path = []
    for fd in filtered_df:
        if not fd.empty:
            folder_path.extend(fd['Links'].tolist())

    if not folder_path:
        return jsonify({"error": "No links found for the specified numbers."})

    video_extensions = ('.mp4', '.avi', '.mov', '.mkv')

    def video_return(video_path):
        try:
            if not os.path.exists(video_path):
                return jsonify({"error": "Video file not found"})
                
            reader = imageio.get_reader(str(video_path))
            frames_list = []

            for frame in reader:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                _, buffer = cv2.imencode('.png', frame)
                encoded_image = base64.b64encode(buffer).decode('utf-8')
                frames_list.append(encoded_image)

            return jsonify({"data": frames_list})
        except Exception as e:
            return jsonify({"error": f"Could not process video: {str(e)}"})

    def merge_videos(video_paths, output_path):
        try:
            clips = [VideoFileClip(str(path)) for path in video_paths if os.path.exists(path)]
            if clips:
                merged_clip = concatenate_videoclips(clips)
                merged_clip.write_videofile(str(output_path), codec='libx264')
                for clip in clips:
                    clip.close()
        except Exception as e:
            print(f"Error merging videos: {str(e)}")

    video_files = []
    for folder in folder_path:
        folder_path = Path(folder)
        if folder_path.is_dir():
            video_files.extend([
                str(folder_path / f) 
                for f in folder_path.glob('*') 
                if f.suffix.lower() in video_extensions
            ])

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not output_path.exists():
        merge_videos(video_files, output_path)

    return video_return(output_path)