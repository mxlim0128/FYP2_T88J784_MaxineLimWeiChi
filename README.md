# Smart Energy NILM System

This repository contains the source code and documentation for a Final Year Project (FYP) on a smart energy monitoring and control system using Non-Intrusive Load Monitoring (NILM).

## Project Overview
The objective of this project is to estimate individual appliance power consumption from aggregate household power data.  
A deep learning Seq2Point NILM model is used to perform appliance-level energy disaggregation, which is integrated with IoT services for real-time monitoring and visualization.

## Key Features
- Appliance-level energy disaggregation using a Seq2Point deep learning model
- Real-time data streaming via MQTT
- Time-series data storage using InfluxDB
- Energy visualization using Grafana
- Flow-based data processing and control using Node-RED
- Docker-based system deployment

## System Components
- **NILM Model**: Seq2Point convolutional neural network for power disaggregation
- **IoT Layer**: MQTT broker for real-time data transmission
- **Data Storage**: InfluxDB for storing time-series power data
- **Visualization**: Grafana dashboards for monitoring energy usage
- **Control Logic**: Node-RED for automation and appliance control

## Repository Structure
src/ - NILM model, inference, and control source code
scripts/ - Training, evaluation, and baseline scripts
configs/ - Configuration files
docs/ - System diagrams and screenshots


## Technologies Used
- Python
- TensorFlow / Keras
- NILMTK
- MQTT
- InfluxDB
- Grafana
- Node-RED
- Docker

## Notes
Datasets, trained models, and Docker runtime data are not included in this repository to keep the project lightweight and clean.

## Author
Maxine Lim Wei Chi
Final Year Project
