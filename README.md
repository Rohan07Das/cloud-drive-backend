# Cloud Drive Backend

A robust file management and storage orchestration engine built with **Flask**. This project provides a reliable backend for cloud-based storage services, featuring secure file handling, automated directory indexing, and a dedicated safety layer for deleted assets.

## 🚀 Features

* **File Upload & Download:** Securely handle file transfers between the client and the server.
* **Recycle Bin Logic:** Implementation of a safety layer that moves deleted files to a temporary retention folder instead of permanent deletion.
* **Dynamic Indexing:** Automatically tracks and lists files within the storage directories.
* **Administrative Interface:** An integrated web-based dashboard for monitoring storage and testing API endpoints.

## 🏗️ Tech Stack

* **Backend Framework:** [Flask](https://flask.palletsprojects.com/) (Python)
* **Language:** Python 3.10+
* **Storage Logic:** Local file-system based storage with directory mapping.
* **Frontend:** HTML5/CSS3 (Integrated for testing and management).

## 📁 Project Structure
```markdown

├── uploads/             # Primary directory for active cloud storage
├── recycle_bin/         # Secondary directory for temporary file retention
├── app.py               # Main application logic and API route orchestration
├── index.html           # Backend interaction interface
├── requirements.txt     # Project dependencies
└── README.md            # Technical documentation

```
## 🛠️ Installation & Setup
### 1. Clone the repository
```bash
git clone [https://github.com/Rohan07Das/cloud-drive-backend.git]
cd cloud-drive-backend

```
### 2. Set up a virtual environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

```
### 3. Install dependencies
```bash
pip install -r requirements.txt

```
### 4. Run the application
```bash
python app.py

```
The server will start at http://127.0.0.1:5000.
## 🔌 API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | / | Serves the management interface (index.html). |
| POST | /upload | Uploads a file to the uploads/ directory. |
| GET | /files | Lists all currently stored files. |
| DELETE | /delete/<filename> | Moves a file from uploads/ to recycle_bin/. |
## 🛡️ Security & Best Practices
 * **Filename Sanitization:** The application uses secure filename handling to prevent directory traversal attacks.
 * **Separation of Concerns:** Distinct directories for active storage and deleted files ensure data integrity.


*Developed by Rohan Lal Das as an individual technical project.*

