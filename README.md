#  Multi-Layer Airport Security Anomaly Detection System  
### YOLOv8/Yolov11-s X-ray Threat Detection • IoT Sensor Anomaly Detection • 3D-CNN Video Anomalies • Blockchain Logging

This repository contains the full implementation of a **multi-modal security system** designed for automated threat detection in airport environments. The system integrates:

- **X-ray prohibited-item detection** using YOLOv8-s and YOLOv11-s  
- **IoT sensor anomaly detection** using an LSTM Autoencoder  
- **Video surveillance anomaly detection** using a 3D-CNN Autoencoder  
- **Blockchain-based secure logging** of all detected anomalies  

The project is developed as part of a research manuscript submitted to **Scientific Reports (Nature Portfolio)**.



##  **Key Features**

###  1. X-Ray Prohibited Item Detection (YOLOv8-s & YOLOv11-s)
- Trained on **CLCXray dataset** (80/10/10 split)  
- Input size: 640 × 640  
- Advanced augmentations (mosaic, mixup, HSV, flips)  
- High accuracy:
  - **YOLOv8-s:** mAP50 = 0.89719, mAP50–95 = 0.78487  
  - **YOLOv11-s:** mAP50 = 0.89888, mAP50–95 = 0.78917  



### 2. Video Anomaly Detection (3D CNN Autoencoder)
- Based on the **Avenue dataset**  
- Converts video frames (5 FPS, 224×224 grayscale) into 10-frame temporal sequences  
- Learns normal motion, flags abnormal behaviour  
- Reconstruction error threshold automatically computed via  
  `mean + 3 × std`



### 3. IoT Anomaly Detection (LSTM Autoencoder)
- Simulated IoT data (temperature, humidity, vibration)  
- Normalized with Min-Max scaling  
- Detects abnormal sensor behaviour  
- Reconstruction error threshold:  
  `mean + 3 × std`



###  4. Blockchain-Based Secure Logging
All anomalies detected by:
- YOLO X-ray model  
- IoT LSTM autoencoder  
- Video Conv3D autoencoder  

are logged into a **tamper-proof blockchain ledger** using:
- SHA-256 hashing  
- UUID-based event IDs  
- Hash chaining for immutability  

Result: `security_ledger.json`


