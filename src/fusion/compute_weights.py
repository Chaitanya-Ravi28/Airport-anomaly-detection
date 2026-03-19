import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

video = np.load(os.path.join(BASE_DIR,"data","video_errors.npy"))
iot = np.load(os.path.join(BASE_DIR,"data","iot_errors.npy"))
xray = np.load(os.path.join(BASE_DIR,"data","xray_confidences.npy"))

# normalize each modality
video_norm = (video - video.min()) / (video.max() - video.min())
iot_norm = (iot - iot.min()) / (iot.max() - iot.min())
xray_norm = (xray - xray.min()) / (xray.max() - xray.min())

# aggregate
video_score = np.mean(video_norm)
iot_score = np.mean(iot_norm)
xray_score = np.mean(xray_norm)

scores = np.array([video_score, iot_score, xray_score])

weights = scores / np.sum(scores)

print("Fusion Weights")
print("Video:", weights[0])
print("IoT:", weights[1])
print("Xray:", weights[2])