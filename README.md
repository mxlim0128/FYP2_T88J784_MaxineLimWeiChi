# Smart Energy Monitoring and Appliance Control Using IoT and NILM

## 📖 Overview

This repository contains the source code, deployment configurations, and documentation for a Final Year Project (FYP) titled:

### ⚡ Smart Energy Monitoring and Appliance Control Using IoT

The project presents an IoT-based smart energy management system that combines real-time power monitoring, Non-Intrusive Load Monitoring (NILM), appliance classification, and automated load control.

The system estimates individual appliance energy consumption from aggregate household power measurements and provides real-time visualization through a web-based dashboard.

The proposed solution integrates IoT hardware, machine learning models, and cloud-ready services to improve energy awareness and support intelligent energy management in residential environments.

---

# 🎯 Project Objectives

### 🧠 Objective 1

To assess the effectiveness of the proposed hybrid NILM architecture in appliance power consumption estimation and appliance operating state identification.

### 📡 Objective 2

To design and implement an IoT-based system using ESP32 for real-time energy monitoring and appliance control.

### ⚡ Objective 3

To design and evaluate a priority-based load management mechanism to reduce overload conditions while maintaining the operation of higher-priority appliances.

---

# 🏗️ System Architecture

The system consists of four main layers:

## 📡 1. Data Acquisition Layer

## 🔌 Hardware

| Component                                                                | Purpose                                                                       |
| ------------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| 🔹 ESP32 Microcontroller                                                 | Real-time sensing, MQTT communication, and appliance control                  |
| 🔹 Raspberry Pi 4 Model B (4GB)                                          | Edge server hosting Node-RED, Mosquitto, InfluxDB, Grafana, and NILM services |
| 🔹 SCT-013-000 Current Sensor (×4)                                       | Measures current consumption of connected appliances                          |
| 🔹 ZMPT101B Voltage Sensor                                               | Measures AC mains voltage                                                     |
| 🔹 Midpoint Bias Circuit (10 kΩ Resistors, Capacitor, Protection Diodes) | Shifts AC signals into the ESP32 ADC measurement range                        |
| 🔹 4-Channel Relay Module                                                | Enables automated appliance switching and load management                     |


## 🏠 Test Appliances

The system was evaluated using the following household appliances:

| Appliance  | Purpose                                                             |
| ---------- | ------------------------------------------------------------------- |
| 💡 Lamp    | Low-priority appliance for load shedding tests                      |
| 💻 Laptop  | Medium-priority appliance for load management evaluation            |
| 🍞 Toaster | High-power appliance used for energy monitoring and NILM evaluation |
| ☕ Kettle   | High-priority appliance protected from automatic disconnection      |


---

## ⚙️ 2. Data Processing Layer

### Services

* 📨 Mosquitto MQTT Broker
* 🔄 Node-RED
* 🌐 Flask APIs

Node-RED receives incoming sensor data and forwards it to machine learning services for NILM processing.

---

## 🧠 3. NILM and Classification Layer

### NILM Methods Evaluated

* 📏 Threshold-Based Method
* 🔍 Factorial Hidden Markov Model (FHMM)
* 🤖 Seq2Point Deep Learning Model
* 🏷️ Appliance Classification Model

The Seq2Point model is used as the primary disaggregation model to estimate appliance-level power consumption from aggregate household power data.

The appliance classifier determines the operating status (ON/OFF) of monitored appliances.

---

## 📊 4. Visualization and Storage Layer

### Technologies

* 🗄️ InfluxDB
* 📈 Grafana

Power measurements, NILM predictions, appliance states, and control actions are stored in InfluxDB and visualized through Grafana dashboards.

---

# ✨ Key Features

⚡ Real-time energy monitoring

🏠 Appliance-level energy disaggregation

🧠 Deep learning-based NILM using Seq2Point

🔌 Appliance state classification

📨 MQTT-based communication

📊 Interactive Grafana dashboards

🤖 Automated load management

🐳 Dockerized deployment

🔄 Node-RED workflow automation

---

# 🚨 Automatic Load Control

The system includes a priority-based load management mechanism to prevent excessive power consumption.

## ⚡ Power Threshold

**2200 W**

## 🔢 Priority Order

1️⃣ 💡 Lamp (Lowest Priority)

2️⃣ 💻 Laptop

3️⃣ 🍞 Toaster

4️⃣ ☕ Kettle (Highest Priority)

## 🤖 Control Logic

🔹 When total power exceeds **2200 W**, the lamp is automatically switched OFF.

🔹 If power consumption still exceeds **2200 W**, the laptop is automatically switched OFF.

🔹 The toaster and kettle are never automatically disconnected to ensure user safety and uninterrupted operation of high-priority appliances.

---

# 🛠️ Technologies Used

## 🔌 Hardware

* ESP32
* SCT-013-000 Current Sensor
* ZMPT101B Voltage Sensor
* 4-Channel Relay Module

## 💻 Software

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

# 📚 Dataset

The NILM models were trained and evaluated using the **REFIT Energy Dataset**.

### 📂 Dataset Source

📊 REFIT Electrical Load Measurements Dataset

---

# 🚀 Deployment

The system can be deployed using Docker containers for:

🐳 MQTT Broker

🐳 Node-RED

🐳 Seq2Point API

🐳 Classification API

🐳 InfluxDB

🐳 Grafana

Docker Compose is used to simplify deployment and service orchestration.

---

# 📈 Results

The developed system successfully:

🔹 Monitors household energy consumption in real time.

🔹 Performs appliance-level energy disaggregation using NILM.

🔹 Detects appliance operating states automatically.

🔹 Provides interactive energy dashboards.

🔹 Implements intelligent load control based on power thresholds.

🔹 Demonstrates the feasibility of integrating IoT and machine learning for smart energy management.

---

# 📝 Notes

To keep the repository lightweight:

📂 Raw datasets are not included.

🧠 Trained model files are excluded.

🐳 Docker runtime volumes are excluded.

⚙️ Environment-specific configuration files are excluded.

📖 Refer to the project documentation for setup instructions and deployment details.

---

# 👨‍💻 Author

**Maxine Lim Wei Chi**

🎓 Bachelor of Information Technology (Honours)

🏆 Final Year Project (FYP)

⚡ Smart Energy Monitoring and Appliance Control Using IoT

