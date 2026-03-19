# Multi-Layer Airport Security Monitoring System

## Overview
This project implements a multi-modal airport security framework integrating:

- X-ray prohibited item detection using YOLO
- Video anomaly detection using Conv3D Autoencoder
- IoT anomaly detection using LSTM Autoencoder
- Multimodal fusion for risk estimation
- Blockchain-based secure logging for tamper-proof event storage

The system combines multiple data sources to improve anomaly detection reliability in airport environments.

---

## Project Structure

---

## Important Note on Paths

Due to restructuring of directories, file paths may need to be updated before running the code.

Ensure that:
- All file paths inside scripts match your local folder structure
- Update paths for:
  - model weights
  - input files (images, videos, IoT data)
  - sample data files

Example:data_sample/video_errors.npy


If errors occur, verify paths in:
src/run_system.py
src/compute_weights.py


---

## Installation

Install required dependencies:

```bash
pip install -r requirements.txt

## Run complete system
python src/run_system.py