import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# load IoT anomaly scores
iot_errors = np.load(os.path.join(BASE_DIR, "data", "iot_errors.npy"))

print("IoT scores length:", len(iot_errors))

# normalize scores
iot_errors = (iot_errors - np.min(iot_errors)) / (np.max(iot_errors) - np.min(iot_errors))

# generate labels using threshold (since dataset is synthetic)
threshold = np.percentile(iot_errors, 90)

labels = (iot_errors > threshold).astype(int)

print("Threshold:", threshold)
print("Unique labels:", np.unique(labels))

# compute ROC
fpr, tpr, thresholds = roc_curve(labels, iot_errors)

roc_auc = auc(fpr, tpr)

print("IoT ROC-AUC:", roc_auc)

# plot ROC
plt.figure(figsize=(6,6))

plt.plot(fpr, tpr,
         color="green",
         lw=2,
         label="ROC curve (AUC = %0.3f)" % roc_auc)

plt.plot([0,1],[0,1], color="gray", linestyle="--")

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - IoT Anomaly Detection")

plt.legend(loc="lower right")

# save figure
fig_dir = os.path.join(BASE_DIR, "figures")
os.makedirs(fig_dir, exist_ok=True)

plt.savefig(os.path.join(fig_dir, "roc_iot.png"))

plt.show()