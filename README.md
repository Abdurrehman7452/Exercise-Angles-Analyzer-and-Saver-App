# 🏋️ Exercise Video Analysis Tool

A Python-based desktop application for analyzing exercise videos using human pose estimation and joint angle calculation.

Built with **PyQt5**, **OpenCV**, and **MediaPipe**, this tool allows frame-by-frame video navigation, pose analysis, and structured data export in JSON format.

---

## 🚀 Features

- 🎥 Upload and play videos frame-by-frame
- 🧍 Pose detection using **MediaPipe (3D WorldLandmarks)**
- 📐 Joint angle calculation (e.g., knee, elbow, shoulder)
- 📝 Capture key positions (start/mid/end) with posture descriptions
- 💾 Export biomechanical data and raw landmarks to JSON
- ⚡ Designed for responsive performance and future GPU support

---

## 🖥️ Demo

<img width="794" height="628" alt="image" src="https://github.com/user-attachments/assets/d706daf7-2e80-41a6-99ad-19f2088b4b28" />


---

## 🧰 Tech Stack

- Python 3.9+
- PyQt5
- OpenCV
- MediaPipe
- NumPy
- JSON

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/exercise-video-analyzer.git
cd exercise-video-analyzer

# (Optional) Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt
