import mediapipe as mp
import cv2
import numpy as np

class PoseEstimator:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=False,
            min_detection_confidence=0.5
        )

    def detect(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)

        if not results.pose_landmarks:
            return None

        landmarks = results.pose_world_landmarks.landmark
        landmark_dict = {}
        for idx, lm in enumerate(landmarks):
            landmark_dict[self.mp_pose.PoseLandmark(idx).name] = {
                "x": lm.x, "y": lm.y, "z": lm.z, "visibility": lm.visibility
            }

        return {
            "landmarks": landmark_dict,
            "raw_result": results.pose_landmarks  # for drawing
        }
