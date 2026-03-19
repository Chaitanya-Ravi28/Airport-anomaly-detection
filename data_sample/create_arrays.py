import os
import json
import numpy as np

# Get project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

video_json = os.path.join(BASE_DIR, "outputs", "video_anomalies.json")
iot_json = os.path.join(BASE_DIR, "outputs", "iot_anomalies.json")
xray_json = os.path.join(BASE_DIR, "outputs", "prohibited_items.json")

# Load video anomaly scores
with open(video_json) as f:
    video = json.load(f)

video_errors = np.array([v["recon_error"] for v in video])

# Load IoT anomaly scores
with open(iot_json) as f:
    iot = json.load(f)

iot_errors = np.array([i["recon_error"] for i in iot])

# Load X-ray anomaly scores
with open(xray_json) as f:
    xray = json.load(f)

xray_scores = np.array([x["anomaly_score"] for x in xray])

# Compute threshold for video
mean = np.mean(video_errors)
std = np.std(video_errors)
threshold = np.percentile(video_errors, 95)

labels_video = (video_errors > threshold).astype(int)

# Simple IoT labels
# IoT anomaly threshold
iot_threshold = np.percentile(iot_errors, 90)

labels_iot = (iot_errors > iot_threshold).astype(int)

print("IoT threshold:", iot_threshold)
print("Normal samples:", np.sum(labels_iot==0))
print("Anomaly samples:", np.sum(labels_iot==1))
# Save arrays
np.save(os.path.join(BASE_DIR,"data","video_errors.npy"), video_errors)
np.save(os.path.join(BASE_DIR,"data","iot_errors.npy"), iot_errors)
np.save(os.path.join(BASE_DIR,"data","xray_confidences.npy"), xray_scores)
np.save(os.path.join(BASE_DIR,"data","labels_video.npy"), labels_video)
np.save(os.path.join(BASE_DIR,"data","labels_iot.npy"), labels_iot)

print("Arrays created successfully")
print("threshold:", threshold)
