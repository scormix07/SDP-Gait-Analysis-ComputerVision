import os

from walk_predictor import predict_walk


distance = 17
thresh = 0.45

def work_on_dir(dir):
    for f in os.listdir(dir):
        if 'side' in f:
            pth = os.path.join(dir, f)

            for pred, _ in predict_walk(pth, distance, thresh, 20):
                if isinstance(pred, str):
                    break
            print('pred: ', pred)
            print(pth)
            if pred in f:
                print('Correct!')
            else:
                print('-------- Incorrect!!')
            
            _ = input()

dir = '../2cameras/abnormal'
dir2 = '../2cameras/normal'

work_on_dir(dir)
work_on_dir(dir2)


