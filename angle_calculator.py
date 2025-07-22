import numpy as np

class AngleCalculator:
    @staticmethod
    def calculate_angle(a, b, c):
        """
        Calculates the angle at point 'b' given three 2D points:
        a (start), b (mid / joint), c (end)

        Parameters:
        a, b, c: Tuples or lists of (x, y) coordinates

        Returns:
        Angle in degrees
        """
        a = np.array(a)  # First point (e.g., hip)
        b = np.array(b)  # Midpoint (e.g., knee)
        c = np.array(c)  # Last point (e.g., ankle)

        # Calculate the angle using arctangent of the vectors
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        # Ensure angle is always between 0 and 180
        if angle > 180.0:
            angle = 360 - angle

        return angle

