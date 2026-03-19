import os
import json
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

video = np.load(os.path.join(BASE_DIR,"data","video_errors.npy"))
iot = np.load(os.path.join(BASE_DIR,"data","iot_errors.npy"))
xray = np.load(os.path.join(BASE_DIR,"data","xray_confidences.npy"))

# normalize scores
video_norm = (video - video.min()) / (video.max() - video.min())
iot_norm = (iot - iot.min()) / (iot.max() - iot.min())
xray_norm = (xray - xray.min()) / (xray.max() - xray.min())

video_score = np.mean(video_norm)
iot_score = np.mean(iot_norm)
xray_score = np.mean(xray_norm)

# learned weights
w_video = 0.3334
w_iot = 0.4149
w_xray = 0.2517

risk_score = (
    w_video * video_score +
    w_iot * iot_score +
    w_xray * xray_score
)

print("Video score:", video_score)
print("IoT score:", iot_score)
print("Xray score:", xray_score)
print("Final Risk Score:", risk_score)

fusion_event = {
    "video_score": float(video_score),
    "iot_score": float(iot_score),
    "xray_score": float(xray_score),
    "risk_score": float(risk_score)
}

with open(os.path.join(BASE_DIR,"outputs","fusion_event.json"),"w") as f:
    json.dump(fusion_event,f,indent=4)