import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
from scipy.signal import find_peaks


from utils import euclidean_distance, default_draw, calculate_angle
from points_ind import *

input_path = "../2cameras/normal/patient2-side-normal0.mp4"

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose()


def predict_walk(input_path, distance, threshold,
                 pelvic_thresh, use_pelvic=False,
                 top_angles=5, out=False):
    cap = cv2.VideoCapture(input_path)
    
    if out:
        # Define the output video codec and create a VideoWriter object
        output_file = input_path.split('/')[-1]
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        output_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        output_fps = int(cap.get(cv2.CAP_PROP_FPS))
        out = cv2.VideoWriter(output_file, fourcc, output_fps, (output_width, output_height))

    series = []

    while True:
        try:
            ret, img = cap.read()

            if not ret:
                break
            
            # cv2.imshow('Frame', img)
            # cv2.waitKey(1)
            results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            h, w, c = img.shape
            opImg = np.zeros([h, w, c])
            opImg.fill(128)
            mp_draw.draw_landmarks(opImg, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_draw.DrawingSpec((255, 0, 0), 1, 1),
                                mp_draw.DrawingSpec((255, 0, 255), 1, 1))

            points = []
            if results.pose_landmarks:
                # points = results.pose_landmarks.landmark
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    points.append([cx, cy])
                    cv2.circle(img, (cx, cy), 2, (255, 0, 0), cv2.FILLED)

                series.append(points)
            if out:
                out.write(img)
            # cv2.imshow("Extracted Pose", opImg)
            # cv2.imshow("Pose Estimation", img)
            yield img, opImg

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print(e)
            break

    cap.release()
    if out:
        out.release()
    # cv2.destroyAllWindows()

    df = pd.DataFrame(series, columns=point_names)

    # breakpoint()

    df['left_leg'] = df.apply( lambda x: euclidean_distance(x['left_hip'], x['left_knee']) 
                                        + euclidean_distance(x['left_knee'], x['left_heel']),
                                axis=1 )

    df['right_leg'] = df.apply( lambda x: euclidean_distance(x['right_hip'], x['right_knee']) 
                                        + euclidean_distance(x['right_knee'], x['right_heel']),
                                axis=1 )


    leg_length = int((max(df['left_leg']) + max(df['right_leg'])) / 2)
    print('leg length ', leg_length)

    # Calculate Stride Length
    df['stride_len'] = df.apply(lambda x: euclidean_distance(x['left_foot_index'], x['right_foot_index']),
                                                        axis=1)
    # find peaks           
    peak_idx = find_peaks(df.stride_len,
                          distance=distance)[0]
    stride_len = df.stride_len[peak_idx].mean() - df.stride_len.min()
    print('stride length: ', stride_len)

    # Calculate Stride Ratio
    stride_ratio = stride_len / leg_length
    print('stride_ratio: ', stride_ratio)

    # pelvic angle caluclation
    df['left_pelvic_angle'] = df.apply(lambda x: calculate_angle(x['left_shoulder'],
                                                                 x['left_hip'],
                                                                 x['left_heel']),
                                        axis=1)
    
    df['right_pelvic_angle'] = df.apply(lambda x: calculate_angle(x['right_shoulder'],
                                                                 x['right_hip'],
                                                                 x['right_heel']),
                                        axis=1)
    
    rt_angle_peak_idx = find_peaks(df['right_pelvic_angle'],
                          distance=distance)[0]
    right_pelvic_top = df['right_pelvic_angle'][rt_angle_peak_idx].nlargest(top_angles)

    lf_angle_peak_idx = find_peaks(df['left_pelvic_angle'],
                          distance=distance)[0]
    left_pelvic_top = df['left_pelvic_angle'][lf_angle_peak_idx].nlargest(top_angles)

    print('left pelvic mean: ', left_pelvic_top.mean())
    print('right pelvic mean: ', right_pelvic_top.mean())
    mean_pelvic_angle = (left_pelvic_top.mean() + right_pelvic_top.mean()) / 2
    print('pelvic angle mean: ', mean_pelvic_angle)

    # final pred
    pred = 'The Gait is Normal!' if stride_ratio > threshold else 'The Gait is Abnormal!'
    
    
    # use pelvic only if it's abnormal based on stride length
    if pred == 'abnormal' and use_pelvic:
        pred = 'abnormal' if mean_pelvic_angle > pelvic_thresh else 'normal'

    yield pred, None


# predict_walk(input_path, 15, 0.4)