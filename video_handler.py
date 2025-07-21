import cv2

class VideoHandler:
    def __init__(self):
        self.cap = None
        self.frame_count = 0

    def load(self, path):
        self.cap = cv2.VideoCapture(path)
        if not self.cap.isOpened():
            raise Exception("Failed to load video")
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def get_frame(self, frame_index):
        if not self.cap:
            return None
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        success, frame = self.cap.read()
        return frame if success else None

    def get_timestamp(self, frame_index):
        if not self.cap:
            return 0
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        return self.cap.get(cv2.CAP_PROP_POS_MSEC)

