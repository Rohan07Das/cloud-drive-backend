# Cloud Drive Backend

A robust file management and storage orchestration engine built with **Flask**. This project provides a reliable backend for cloud-based storage services, featuring secure file handling and a dedicated safety-layer for deleted assets.

## 🏗️ Tech Stack

* **Framework:** [Flask](https://flask.palletsprojects.com/) (Python)
* **Language:** Python 3.10+
* **Storage Logic:** File-system based storage with automated directory indexing.
* **Interface:** Integrated HTML/CSS for administrative monitoring and testing.

## 📁 Project Structure

```text
├── uploads/             # Primary directory for active cloud storage
├── recycle_bin/         # Secondary directory for temporary file retention
├── app.py               # Main application logic and API route orchestration
├── index.html           # Backend interaction interface
├── requirements.txt     # Project dependencies
└── README.md            # Technical documentation
