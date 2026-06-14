# Smart Energy Monitoring and Appliance Control Using IoT and NILM

## Overview

This repository contains the source code, deployment configurations, and documentation for a Final Year Project (FYP) titled:

**Smart Energy Monitoring and Appliance Control Using IoT**

The project presents an IoT-based smart energy management system that combines real-time power monitoring, Non-Intrusive Load Monitoring (NILM), appliance classification, and automated load control. The system estimates individual appliance energy consumption from aggregate household power measurements and provides real-time visualization through a web-based dashboard.

The proposed solution integrates IoT hardware, machine learning models, and cloud-ready services to improve energy awareness and support intelligent energy management in residential environments.

---

## Project Objectives

* Monitor household electrical consumption in real time.
* Estimate appliance-level power usage from aggregate power measurements using NILM techniques.
* Detect appliance operating states automatically.
* Visualize energy data through interactive dashboards.
* Implement automated load control to prevent excessive power consumption.
* Evaluate and compare different NILM approaches for appliance energy disaggregation.

---

## System Architecture

The system consists of four main layers:

### 1. Data Acquisition Layer

* ESP32 microcontroller
* SCT-013-000 current sensor
* ZMPT101B voltage sensor

The ESP32 continuously measures voltage, current, power, and energy consumption and publishes the data through MQTT.

### 2. Data Processing Layer

* Mosquitto MQTT Broker
* Node-RED
* Flask APIs

Node-RED receives incoming sensor data and forwards it to machine learning services for NILM processing.

### 3. NILM and Classification Layer

The project evaluates several NILM approaches:

* Threshold-Based Method
* Factorial Hidden Markov Model (FHMM)
* Seq2Point Deep Learning Model
* Appliance Classification Model

The Seq2Point model is used as the primary disaggregation model to estimate appliance-level power consumption from aggregate household power data.

The appliance classifier determines the operating status (ON/OFF) of monitored appliances.

### 4. Visualization and Storage Layer

* InfluxDB
* Grafana

Power measurements, NILM predictions, appliance states, and control actions are stored in InfluxDB and visualized through Grafana dashboards.

---

## Key Features

* Real-time energy monitoring
* Appliance-level energy disaggregation
* Deep learning-based NILM using Seq2Point
* Appliance state classification
* MQTT-based communication
* Interactive Grafana dashboards
* Automated load management
* Dockerized deployment
* Node-RED workflow automation

---

## Automatic Load Control

The system includes a priority-based load management mechanism to prevent excessive power consumption.

Power Threshold:

* 2200 W

Priority Order:

1. Lamp (Lowest Priority)
2. Laptop
3. Toaster
4. Kettle (Highest Priority)

Control Logic:

* When total power exceeds 2200 W, the lamp is automatically switched OFF.
* If power consumption still exceeds 2200 W, the laptop is automatically switched OFF.
* The toaster and kettle are never automatically disconnected to ensure user safety and uninterrupted operation of high-priority appliances.

---

## Technologies Used

### Hardware

* ESP32
* SCT-013-000 Current Sensor
* ZMPT101B Voltage Sensor
* 4-Channel Relay Module

### Software

* Python
* TensorFlow
* Keras
* NILMTK
* Flask
* MQTT
* Mosquitto
* Node-RED
* InfluxDB
* Grafana
* Docker

---

## Dataset

The NILM models were trained and evaluated using the REFIT Energy Dataset.

Dataset Source:

* REFIT Electrical Load Measurements Dataset

---

## Deployment

The system can be deployed using Docker containers for:

* MQTT Broker
* Node-RED
* Seq2Point API
* Classification API
* InfluxDB
* Grafana

Docker Compose is used to simplify deployment and service orchestration.

---

## Results

The developed system successfully:

* Monitors household energy consumption in real time.
* Performs appliance-level energy disaggregation using NILM.
* Detects appliance operating states automatically.
* Provides interactive energy dashboards.
* Implements intelligent load control based on power thresholds.
* Demonstrates the feasibility of integrating IoT and machine learning for smart energy management.

---

## Notes

To keep the repository lightweight:

* Raw datasets are not included.
* Trained model files are excluded.
* Docker runtime volumes are excluded.
* Environment-specific configuration files are excluded.

Refer to the project documentation for setup instructions and deployment details.

---

## Author

**Maxine Lim Wei Chi**

Bachelor of Information Technology (Honours)

Final Year Project (FYP)
