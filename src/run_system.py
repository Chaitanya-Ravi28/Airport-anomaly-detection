import json
import numpy as np
import os
import hashlib
from datetime import datetime, UTC

# -----------------------------
# Base directory
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -----------------------------
# Load anomaly score arrays
# -----------------------------

video_scores = np.load(os.path.join(BASE_DIR, "data", "video_errors.npy"))
iot_scores   = np.load(os.path.join(BASE_DIR, "data", "iot_errors.npy"))
xray_scores  = np.load(os.path.join(BASE_DIR, "data", "xray_confidences.npy"))

print("Video length:", len(video_scores))
print("IoT length:", len(iot_scores))
print("Xray length:", len(xray_scores))

# -----------------------------
# Normalize scores
# -----------------------------

video_scores = (video_scores - video_scores.min())/(video_scores.max()-video_scores.min())
iot_scores   = (iot_scores - iot_scores.min())/(iot_scores.max()-iot_scores.min())
xray_scores  = (xray_scores - xray_scores.min())/(xray_scores.max()-xray_scores.min())

# -----------------------------
# Align lengths
# -----------------------------

min_len = min(len(video_scores), len(iot_scores), len(xray_scores))

video_scores = video_scores[:min_len]
iot_scores   = iot_scores[:min_len]
xray_scores  = xray_scores[:min_len]

print("Events to process:", min_len)

# -----------------------------
# Fusion weights
# -----------------------------

w_video = 0.333
w_iot   = 0.415
w_xray  = 0.252

# -----------------------------
# Compute fusion scores
# -----------------------------

fusion_scores = (
    w_video * video_scores +
    w_iot * iot_scores +
    w_xray * xray_scores
)

# -----------------------------
# Thresholds
# -----------------------------

fusion_std = np.std(fusion_scores)

warning_threshold  = fusion_std
critical_threshold = 2 * fusion_std

xray_threshold = np.mean(xray_scores) + np.std(xray_scores)

print("\nThresholds")
print("Warning threshold:", warning_threshold)
print("Critical threshold:", critical_threshold)
print("Xray threshold:", xray_threshold)

# -----------------------------
# Blockchain ledger
# -----------------------------

ledger = []
previous_hash = "0"

# -----------------------------
# Hash function
# -----------------------------

def compute_hash(data):
    block_string = json.dumps(data, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

# -----------------------------
# Process events
# -----------------------------

for i in range(min_len):

    video_score = float(video_scores[i])
    iot_score   = float(iot_scores[i])
    xray_score  = float(xray_scores[i])

    risk_score = (
        w_video * video_score +
        w_iot * iot_score +
        w_xray * xray_score
    )

    # fusion decision

    if risk_score > critical_threshold:
        fusion_status = "CRITICAL"
    elif risk_score > warning_threshold:
        fusion_status = "WARNING"
    else:
        fusion_status = "NORMAL"

    # prohibited item detection

    prohibited = xray_score > xray_threshold

    if prohibited and fusion_status != "NORMAL":
        status = fusion_status + " + PROHIBITED ITEM"
    elif prohibited:
        status = "PROHIBITED ITEM DETECTED"
    else:
        status = fusion_status

    print(f"\nEvent {i+1}")
    print("Video score:", video_score)
    print("IoT score:", iot_score)
    print("Xray score:", xray_score)
    print("Risk score:", risk_score)
    print("Status:", status)

    block_data = {
        "timestamp": datetime.now(UTC).isoformat(),
        "event_id": i + 1,
        "video_score": video_score,
        "iot_score": iot_score,
        "xray_score": xray_score,
        "risk_score": risk_score,
        "status": status,
        "previous_hash": previous_hash
    }

    block_hash = compute_hash(block_data)

    block = {
        "data": block_data,
        "hash": block_hash
    }

    ledger.append(block)

    previous_hash = block_hash

# -----------------------------
# Save blockchain ledger
# -----------------------------

ledger_path = os.path.join(BASE_DIR, "security_ledger.json")

with open(ledger_path, "w", encoding="utf-8") as f:
    json.dump(ledger, f, indent=4)

print("\nAll events processed and logged.")
print("Ledger file:", ledger_path)
print("Total events logged:", len(ledger))