**Procedure for Detecting Abnormal Walk**

**Step 1: Input Video File**
- The process begins by providing a video file containing the walking motion. This file path is passed to the function `predict_walk`.

**Step 2: Video Processing**
- The video is read frame by frame using OpenCV. Each frame undergoes pose estimation using the MediaPipe library, which identifies key landmarks on the human body related to posture and movement.

**Step 3: Pose Estimation and Landmark Detection**
- MediaPipe's pose estimation model is employed to detect landmarks like hips, knees, and heels. These landmarks are represented as (x, y) coordinates on the image frame.

**Step 4: Calculation of Leg Length**
- The lengths of both the left and right legs are computed using the Euclidean distance between specific pairs of landmarks (hip to knee and knee to heel).

**Step 5: Stride Length Measurement**
- The stride length, which is the distance between consecutive placements of the same foot, is calculated based on the distance between the indices of consecutive peaks in the stride length signal.

**Step 6: Calculation of Stride Ratio**
- The stride ratio, which represents the ratio of stride length to leg length, is calculated. This metric helps determine if the stride length is abnormal relative to the person's leg length.

**Step 7: Pelvic Angle Calculation**
- The angles formed by the shoulders, hips, and heels are computed to assess pelvic tilt during walking. This angle indicates the inclination of the pelvis, which can be indicative of an abnormal gait.

**Step 8: Peak Detection in Pelvic Angles**
- Peaks in the pelvic angle signal are identified using the `find_peaks` function from SciPy library. The highest angles are selected for both left and right pelvis angles.

**Step 9: Assessment of Pelvic Angle Mean**
- The mean pelvic angle is calculated as the average of the highest angles detected for both left and right pelvic angles. This provides an overall measure of pelvic tilt during walking.

**Step 10: Final Prediction**
- Based on the calculated stride ratio, a prediction is made regarding the normalcy of the walk. If the stride ratio exceeds a predefined threshold, the walk is classified as abnormal. Optionally, if pelvic angles are considered and the walk is predicted as abnormal based on stride length, the mean pelvic angle is used to confirm or refute the abnormality.

**Step 11: Output**
- The result of the prediction (normal or abnormal) is yielded by the function, along with any additional visualizations if specified.

This step-by-step procedure outlines the algorithm's process for detecting abnormal walking patterns using pose estimation and key metrics derived from the detected landmarks.