import numpy as np
from typing import Dict, List, Tuple


def calculate_angle(p1: Dict, p2: Dict, p3: Dict) -> float:
    """
    Calculate angle between three points.
    p2 is the vertex of the angle.
    """
    # Convert to numpy arrays
    a = np.array([p1['x'], p1['y']])
    b = np.array([p2['x'], p2['y']])
    c = np.array([p3['x'], p3['y']])

    # Calculate vectors
    ba = a - b
    bc = c - b

    # Calculate angle
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))

    return np.degrees(angle)


def get_landmark(pose: Dict, landmark_idx: int) -> Dict:
    """Get a specific landmark from pose data."""
    return pose['landmarks'][landmark_idx]


def calculate_vertical_alignment(point1: Dict, point2: Dict) -> float:
    """Calculate how vertically aligned two points are (0 = perfect alignment)."""
    return abs(point1['x'] - point2['x'])


def calculate_depth_ratio(hip: Dict, knee: Dict) -> float:
    """Calculate the depth ratio (hip position relative to knee)."""
    # Lower y value means higher position (image coordinates)
    if hip['y'] < knee['y']:
        return (knee['y'] - hip['y']) / knee['y']
    else:
        return -(hip['y'] - knee['y']) / knee['y']


def detect_rep_phases(poses: List[Dict], angle_key: str = 'knee') -> List[Dict]:
    """
    Detect repetition phases (eccentric, bottom, concentric) in the movement.
    Returns list of phase data.
    """
    phases = []

    # This is a simplified version - can be enhanced
    for i, pose in enumerate(poses):
        phases.append({
            'frame': pose['frame'],
            'timestamp': pose['timestamp'],
            'pose': pose
        })

    return phases


# MediaPipe Pose landmark indices
class PoseLandmark:
    NOSE = 0
    LEFT_EYE_INNER = 1
    LEFT_EYE = 2
    LEFT_EYE_OUTER = 3
    RIGHT_EYE_INNER = 4
    RIGHT_EYE = 5
    RIGHT_EYE_OUTER = 6
    LEFT_EAR = 7
    RIGHT_EAR = 8
    MOUTH_LEFT = 9
    MOUTH_RIGHT = 10
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_ELBOW = 13
    RIGHT_ELBOW = 14
    LEFT_WRIST = 15
    RIGHT_WRIST = 16
    LEFT_PINKY = 17
    RIGHT_PINKY = 18
    LEFT_INDEX = 19
    RIGHT_INDEX = 20
    LEFT_THUMB = 21
    RIGHT_THUMB = 22
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_KNEE = 25
    RIGHT_KNEE = 26
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28
    LEFT_HEEL = 29
    RIGHT_HEEL = 30
    LEFT_FOOT_INDEX = 31
    RIGHT_FOOT_INDEX = 32
