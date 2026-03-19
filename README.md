# Multi-Layer Airport Security Monitoring System using AI and Blockchain

## Overview

This project presents a unified multi-modal airport security framework that integrates:

- X-ray prohibited item detection using YOLO
- Video anomaly detection using a Conv3D Autoencoder
- IoT anomaly detection using an LSTM Autoencoder
- Multimodal fusion for risk assessment
- Blockchain-based secure logging for tamper-proof event storage

The system combines heterogeneous data sources to improve detection reliability in complex airport environments.

---

## System Pipeline

The proposed framework operates through the following stages:

1. X-ray Detection  
   Detects prohibited items using a YOLO-based object detection model.

2. Video Anomaly Detection  
   Identifies abnormal behaviour in surveillance footage using a Conv3D Autoencoder.

3. IoT Anomaly Detection  
   Detects abnormal environmental patterns using an LSTM Autoencoder.

4. Fusion Mechanism  
   Combines anomaly scores from video and IoT subsystems.

5. Decision Module  
   Classifies system state into:
   - NORMAL
   - WARNING
   - CRITICAL  
   Additionally flags prohibited items independently.

6. Blockchain Logging  
   Stores detection events securely using SHA-256 based hashing.

---

## Project Structure

project/
│
├── src/                # Core pipeline (fusion, decision, blockchain, run_system)
├── models/             # YOLO, Video, IoT model implementations
├── evaluation/         # ROC and performance evaluation scripts
├── data_sample/        # Sample input/output data for testing
├── docs/               # Diagrams and system architecture
├── README.md
└── .gitignore

---

## IMPORTANT NOTE ON FILE PATHS

Due to restructuring of directories, file paths may need to be updated before execution.

Ensure that:
- Model paths are correctly specified
- Input files (images, video, IoT data) are accessible
- Sample data paths are correctly referenced

Example:
data_sample/video_errors.npy

If errors occur, update paths in:
src/run_system.py
src/compute_weights.py

---

## Installation

Install required dependencies:
Ultralytics
python 

---

## How to Run

Run the complete system pipeline:

python src/run_system.py

---

## Fusion Mechanism

Anomaly scores from video and IoT subsystems are combined using weighted fusion:

R = w_v * A_v + w_i * A_i

Where:
- A_v = video anomaly score  
- A_i = IoT anomaly score  
- w_v, w_i = modality weights  

The weights are computed based on validation performance (e.g., ROC-AUC).

---

## Decision Logic

The system categorizes events into:

- NORMAL
- WARNING
- CRITICAL

If a prohibited item is detected:
- It is flagged independently
- Combined with fusion status (e.g., WARNING + PROHIBITED ITEM)

---

## Sample Inputs

Example data is provided in:

data_sample/

Includes:
- IoT anomaly scores
- Video anomaly scores
- Labels


---

## Datasets

- CLCXray Dataset – X-ray baggage images
- Avenue Dataset – Video anomaly detection
- IoT Data – Synthetic data generated using Python

Note: Full datasets are not included due to size constraints.

---

## Key Results

- YOLOv11 mAP50-95: 0.789  
- Fusion ROC-AUC: 0.73  
- Blockchain Latency: ~0.000179 sec  

---

## Key Observation

YOLOv11 achieves comparable and slightly improved performance compared to YOLOv8, while being trained with significantly fewer epochs (50 vs 160), indicating improved training efficiency and faster convergence.

---

## Example Output

Risk Score: 0.42  
Status: WARNING + PROHIBITED ITEM  

---

## Notes

- Only essential code and sample data are included
- Model weights and full datasets are excluded
- Ensure file paths are updated before execution

---

## Future Work

- Integration with real-world IoT datasets
- Adaptive fusion strategies
- Detection of additional threat categories

---

## License

This project is intended for academic and research purposes.