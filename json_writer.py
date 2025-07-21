import json
from datetime import datetime
import os

class JSONWriter:
    def __init__(self, output_dir="outputs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.data = {
            "exercise_name": "",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "video_filename": "",
            "captured_positions": []
        }

    def set_metadata(self, exercise_name, video_filename):
        self.data["exercise_name"] = exercise_name
        self.data["video_filename"] = video_filename

    def add_position(self, position_type, frame_number, timestamp_ms, posture_desc, joint_angles, raw_landmarks):
        self.data["captured_positions"].append({
            "position_type": position_type,
            "timestamp_ms": timestamp_ms,
            "frame_number": frame_number,
            "posture_description": posture_desc,
            "joint_angles": joint_angles,
            "raw_landmarks": raw_landmarks
        })

    def save(self, filename="analysis.json"):
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(self.data, f, indent=4)
        print(f"✅ Saved to {filepath}")
