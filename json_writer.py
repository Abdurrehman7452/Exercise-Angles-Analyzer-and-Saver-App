import json
import os

class JSONWriter:
    def __init__(self, output_dir="outputs", filename="analysis.json"):
        self.output_dir = output_dir
        self.filename = filename
        self.filepath = os.path.join(self.output_dir, filename)
        os.makedirs(self.output_dir, exist_ok=True)
        self.data = self.load_data()

    def load_data(self):
        """Loads existing JSON data from the file."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    # Handle empty file case
                    content = f.read()
                    if not content:
                        return {}
                    return json.loads(content)
            except (json.JSONDecodeError, IOError):
                # If file is corrupt or other IO error, start fresh
                return {}
        return {}

    def add_pose(self, exercise_name, position_type, joint_angles, raw_landmarks):
        """
        Adds or updates a pose for a given exercise.
        If the exercise or position exists, it will be overwritten.
        """
        if exercise_name not in self.data:
            self.data[exercise_name] = {}

        self.data[exercise_name][position_type] = {
            "joint_angles": joint_angles,
            "raw_landmarks": raw_landmarks
        }
        self.save()

    def save(self):
        """Saves the current data dictionary to the JSON file."""
        with open(self.filepath, 'w') as f:
            json.dump(self.data, f, indent=4)
        print(f"✅ Saved to {self.filepath}")
