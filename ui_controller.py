from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QFileDialog, QSlider
)
import cv2
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from video_handler import VideoHandler
from pose_estimator import PoseEstimator
from utils.draw import FrameDrawer
from angle_calculator import AngleCalculator
from utils.constants import JOINT_TRIPLETS
from PyQt5.QtWidgets import QComboBox
from json_writer import JSONWriter
from PyQt5.QtWidgets import QInputDialog


class UIController(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exercise Video Analyzer")
        self.setGeometry(100, 100, 800, 600)

        # Create widgets
        self.analyze_button = QPushButton("Analyze Frame")
        self.video_label = QLabel("Video will appear here")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.load_button = QPushButton("Load Video")
        self.prev_button = QPushButton("Previous Frame")
        self.next_button = QPushButton("Next Frame")
        self.slider = QSlider(Qt.Horizontal)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.slider)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.analyze_button)  # <- Moved here

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Video logic
        self.video_handler = VideoHandler()
        self.current_frame_index = 0

        # Pose estimator
        self.pose_estimator = PoseEstimator()

        # Signals
        self.load_button.clicked.connect(self.load_video)
        self.prev_button.clicked.connect(self.prev_frame)
        self.next_button.clicked.connect(self.next_frame)
        self.slider.valueChanged.connect(self.slider_moved)
        self.analyze_button.clicked.connect(self.analyze_current_frame)
        
        self.joint_selector = QComboBox()
        self.joint_selector.addItems(JOINT_TRIPLETS.keys())
        layout.addWidget(self.joint_selector)
        
        self.json_writer = JSONWriter()
        self.capture_button = QPushButton("Capture Pose")
        button_layout.addWidget(self.capture_button)
        self.capture_button.clicked.connect(self.capture_pose)

        self.video_filename = ""



    def load_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Video File")
        if file_path:
            self.video_handler.load(file_path)
            self.slider.setMaximum(self.video_handler.frame_count - 1)
            self.current_frame_index = 0
            self.show_frame(self.current_frame_index)
            self.video_filename = file_path.split("/")[-1]
            self.json_writer.set_metadata("Generic Exercise", self.video_filename)


    def show_frame(self, index):
        frame = self.video_handler.get_frame(index)
        if frame is not None:
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            image = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_BGR888)
            pixmap = QPixmap.fromImage(image)
            self.video_label.setPixmap(pixmap.scaled(
                self.video_label.width(),
                self.video_label.height(),
                Qt.AspectRatioMode.KeepAspectRatio
            ))
            self.slider.blockSignals(True)
            self.slider.setValue(index)
            self.slider.blockSignals(False)
            
    def analyze_current_frame(self):
        frame = self.video_handler.get_frame(self.current_frame_index)
        result = self.pose_estimator.detect(frame)

        if result is not None:
            landmarks = result["landmarks"]
            selected_joint = self.joint_selector.currentText()
            joint_names = JOINT_TRIPLETS[selected_joint]

            try:
                a = [landmarks[joint_names[0]]["x"], landmarks[joint_names[0]]["y"], landmarks[joint_names[0]]["z"]]
                b = [landmarks[joint_names[1]]["x"], landmarks[joint_names[1]]["y"], landmarks[joint_names[1]]["z"]]
                c = [landmarks[joint_names[2]]["x"], landmarks[joint_names[2]]["y"], landmarks[joint_names[2]]["z"]]

                angle = AngleCalculator.calculate_angle(a, b, c)
                pose_frame = FrameDrawer.draw_landmarks(frame, result["raw_result"])
                text = f"{selected_joint} Angle: {angle:.1f}°"

                # Draw angle on frame
                cv2.putText(pose_frame, text, (20, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                h, w, ch = pose_frame.shape
                bytes_per_line = ch * w
                image = QImage(pose_frame.data, w, h, bytes_per_line, QImage.Format.Format_BGR888)
                pixmap = QPixmap.fromImage(image)
                self.video_label.setPixmap(pixmap.scaled(
                    self.video_label.width(),
                    self.video_label.height(),
                    Qt.AspectRatioMode.KeepAspectRatio
                ))

            except KeyError:
                print("Missing joint data. Pose not detected correctly.")
                
    def capture_pose(self):
        frame = self.video_handler.get_frame(self.current_frame_index)
        result = self.pose_estimator.detect(frame)

        if result is None:
            print("Pose not detected.")
            return

        landmarks = result["landmarks"]
        joint_angles = {}

        for joint_name, triplet in JOINT_TRIPLETS.items():
            try:
                a = [landmarks[triplet[0]]["x"], landmarks[triplet[0]]["y"], landmarks[triplet[0]]["z"]]
                b = [landmarks[triplet[1]]["x"], landmarks[triplet[1]]["y"], landmarks[triplet[1]]["z"]]
                c = [landmarks[triplet[2]]["x"], landmarks[triplet[2]]["y"], landmarks[triplet[2]]["z"]]
                angle = AngleCalculator.calculate_angle(a, b, c)
                joint_angles[f"{joint_name.lower().replace(' ', '_')}_angle"] = round(angle, 2)
            except KeyError:
                continue

        # Get frame metadata
        timestamp_ms = self.video_handler.get_timestamp(self.current_frame_index)

        # Ask user for position type and description
        position_type, ok1 = QInputDialog.getText(self, "Label Pose", "e.g. start, middle, end:")
        posture_desc, ok2 = QInputDialog.getText(self, "Describe Pose", "Posture description:")

        if ok1 and ok2:
            self.json_writer.add_position(
                position_type=position_type,
                frame_number=self.current_frame_index,
                timestamp_ms=int(timestamp_ms),
                posture_desc=posture_desc,
                joint_angles=joint_angles,
                raw_landmarks=result["landmarks"]
            )
            self.json_writer.save()
            print("Pose captured and saved to JSON.")



    def prev_frame(self):
        if self.current_frame_index > 0:
            self.current_frame_index -= 1
            self.show_frame(self.current_frame_index)

    def next_frame(self):
        if self.current_frame_index < self.video_handler.frame_count - 1:
            self.current_frame_index += 1
            self.show_frame(self.current_frame_index)

    def slider_moved(self, value):
        self.current_frame_index = value
        self.show_frame(value)
