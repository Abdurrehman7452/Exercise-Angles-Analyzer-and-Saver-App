import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

class FrameDrawer:
    @staticmethod
    def draw_landmarks(frame, results):
        if results is None:
            return frame
        annotated = frame.copy()
        mp_drawing.draw_landmarks(
            image=annotated,
            landmark_list=results,
            connections=mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
        )
        return annotated
