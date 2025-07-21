import numpy as np

class AngleCalculator:
    @staticmethod
    def calculate_angle(a, b, c):
        # Convert to numpy arrays
        a, b, c = np.array(a), np.array(b), np.array(c)
        ba = a - b
        bc = c - b
        # Normalize and get angle
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
        return np.degrees(angle)
