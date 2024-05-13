import math

import cv2

draw_pos = [50, 200]

def default_draw(text, img, pos=None):
    global draw_pos
    if pos:
        draw_pos = pos
    img = draw_text(text, draw_pos, img)
    draw_pos[1] += 50

    return img


def euclidean_distance(point1, point2):
    """
    Calculates the Euclidean distance between two points in n-dimensional space.
    
    Parameters:
    point1 (tuple): Coordinates of the first point.
    point2 (tuple): Coordinates of the second point.
    
    Returns:
    float: The Euclidean distance between the two points.
    """
    if len(point1) != len(point2):
        raise ValueError("Points must have the same number of dimensions")
    
    squared_distances = [(x - y) ** 2 for x, y in zip(point1, point2)]
    distance = math.sqrt(sum(squared_distances))
    return distance


def draw_text(text, pos, img):

    if isinstance(pos, list):
        pos = tuple(pos)

    img = cv2.putText(img, text,
            pos,
            cv2.FONT_HERSHEY_PLAIN, 2,
            (255, 0, 0), 2)
    
    return img

def calculate_angle(a, b, c):
    """
    Calculate the angle between two arcs defined by three points (A, B, and C).
    
    Parameters:
    a (tuple): Coordinates of point A (x, y).
    b (tuple): Coordinates of point B (x, y).
    c (tuple): Coordinates of point C (x, y).
    
    Returns:
    float: The angle between the two arcs in degrees.
    """
    # Calculate vectors AB and BC
    AB = (b[0] - a[0], b[1] - a[1])
    BC = (c[0] - b[0], c[1] - b[1])
    
    # Calculate dot product of AB and BC
    dot_product = AB[0] * BC[0] + AB[1] * BC[1]
    
    # Calculate magnitude of AB and BC
    magnitude_AB = math.sqrt(AB[0] ** 2 + AB[1] ** 2)
    magnitude_BC = math.sqrt(BC[0] ** 2 + BC[1] ** 2)
    
    # Calculate cosine of the angle between AB and BC
    cosine_angle = dot_product / (magnitude_AB * magnitude_BC)
    
    # Calculate the angle in radians
    angle_rad = math.acos(cosine_angle)
    
    # Convert radians to degrees
    angle_deg = math.degrees(angle_rad)
    
    return angle_deg