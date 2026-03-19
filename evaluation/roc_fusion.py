import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# load scores
video_scores = np.load(os.path.join(BASE_DIR,"data","video_errors.npy"))
iot_scores = np.load(os.path.join(BASE_DIR,"data","iot_errors.npy"))
xray_scores = np.load(os.path.join(BASE_DIR,"data","xray_confidences.npy"))

# normalize
video_scores = (video_scores - video_scores.min())/(video_scores.max()-video_scores.min())
iot_scores = (iot_scores - iot_scores.min())/(iot_scores.max()-iot_scores.min())
xray_scores = (xray_scores - xray_scores.min())/(xray_scores.max()-xray_scores.min())

# align lengths
min_len = min(len(video_scores),len(iot_scores),len(xray_scores))

video_scores = video_scores[:min_len]
iot_scores = iot_scores[:min_len]
xray_scores = xray_scores[:min_len]

# fusion weights (use the ones you computed earlier)
w_video = 0.333
w_iot = 0.415
w_xray = 0.252

# fusion score
fusion_score = w_video*video_scores + w_iot*iot_scores + w_xray*xray_scores

# generate labels using threshold
labels = (xray_scores > 0.5).astype(int)

print("Unique labels:",np.unique(labels))

# ROC
fpr,tpr,_ = roc_curve(labels,fusion_score)

roc_auc = auc(fpr,tpr)

print("Fusion ROC-AUC:",roc_auc)

# plot
plt.figure()

plt.plot(fpr,tpr,label="Fusion ROC (AUC=%0.3f)"%roc_auc)

plt.plot([0,1],[0,1],'k--')

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - Multimodal Fusion")

plt.legend()

# save figure
fig_dir = os.path.join(BASE_DIR,"figures")
os.makedirs(fig_dir,exist_ok=True)

plt.savefig(os.path.join(fig_dir,"roc_fusion.png"))

plt.show()