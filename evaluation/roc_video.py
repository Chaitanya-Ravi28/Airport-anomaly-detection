import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from sklearn.metrics import roc_curve, auc

# project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# load anomaly scores
errors = np.load(os.path.join(BASE_DIR, "data", "video_errors.npy"))

# normalize scores (recommended for anomaly detection)
errors = (errors - np.min(errors)) / (np.max(errors) - np.min(errors))

print("Errors length:", len(errors))

# load Avenue labels
label_dir = os.path.join(BASE_DIR, "datasets", "video_dataset", "testing_label_mask")

labels = []

for file in sorted(os.listdir(label_dir)):

    if file.endswith(".mat"):

        mat = loadmat(os.path.join(label_dir, file))

        volLabel = mat["volLabel"]

        for i in range(volLabel.shape[1]):

            frame_mask = volLabel[0, i]

            # convert mask → frame-level label
            label = 1 if np.max(frame_mask) > 0 else 0

            labels.append(label)

labels = np.array(labels)

print("Total labels loaded:", len(labels))
print("Unique labels:", np.unique(labels))
print("Total anomaly frames:", np.sum(labels))

# align labels with error length
indices = np.linspace(0, len(labels) - 1, len(errors)).astype(int)
labels = labels[indices]

print("Labels length after alignment:", len(labels))
print("Unique labels after alignment:", np.unique(labels))

# compute ROC
fpr, tpr, thresholds = roc_curve(labels, errors)

roc_auc = auc(fpr, tpr)

print("Video ROC-AUC:", roc_auc)

# plot ROC curve
plt.figure(figsize=(6,6))

plt.plot(fpr, tpr,
         color="blue",
         lw=2,
         label="ROC curve (AUC = %0.3f)" % roc_auc)

plt.plot([0,1], [0,1], color="gray", linestyle="--")

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - Video Anomaly Detection")

plt.legend(loc="lower right")

# save figure
fig_dir = os.path.join(BASE_DIR, "figures")
os.makedirs(fig_dir, exist_ok=True)

plt.savefig(os.path.join(fig_dir, "roc_video.png"))

plt.show()