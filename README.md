# Cloud-Based File Sharing System
## Computer Networks – Practical 10

### 1. Problem Statement
Users often need a simple way to transfer and access files over a network. This project implements a client-server file sharing system where a browser client communicates with a Flask server using HTTP over TCP/IP.

### 2. Objectives
- Upload files from a client browser to the server.
- List files stored on the server.
- Download files using HTTP GET.
- Delete files from the server.
- Demonstrate client-server communication using HTTP/TCP/IP.
- Deploy the web application on a cloud platform if required.

### 3. System Architecture

Client Browser  
↓ HTTP over TCP/IP  
Flask Web Server  
↓ File read/write operations  
Server-side File Storage

### 4. Network Topology
The application follows a **client-server architecture**.

One or more client devices (laptop/phone) connect to the Flask server over the network. The server handles requests and accesses the file storage.

### 5. Software Requirements
- Python 3.10+
- Flask
- Web browser
- VS Code
- Optional: Render/Railway/PythonAnywhere for cloud deployment

### 6. Communication Protocols
- **HTTP** – Application-layer protocol used for web requests.
- **TCP** – Reliable transport used by HTTP.
- **IP** – Network-layer addressing and routing.
- **Wi-Fi/Ethernet** – Local network connectivity when accessed from another device.

### 7. Main HTTP Operations
- `GET /` – Display home page and uploaded files.
- `POST /upload` – Upload a file.
- `GET /download/<filename>` – Download a file.
- `POST /delete/<filename>` – Delete a file.

### 8. Security / Validation
- `secure_filename()` prevents unsafe filenames/path traversal.
- Maximum file upload size is 20 MB.
- Missing files return an HTTP 404 response.
- Empty filenames are rejected.

### 9. Installation

Open the project in VS Code.

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\activate
```

Install requirements:

```powershell
pip install -r requirements.txt
```

Run:

```powershell
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

### 10. LAN Demonstration
Because Flask runs using `host="0.0.0.0"`, another device on the same Wi-Fi can access the server.

Example:

```text
http://192.168.1.10:5000
```

This allows a phone to act as a client while the laptop acts as the server.

### 11. Testing

| Test | Procedure | Expected Result |
|---|---|---|
| Connectivity Test | Open the server URL | Home page loads |
| Upload Test | Upload a sample file | File is stored and shown in list |
| Download Test | Click Download | File downloads correctly |
| Delete Test | Click Delete and confirm | File is removed |
| LAN Test | Open network URL from phone | Same web app opens |
| Size Validation | Upload file larger than 20 MB | Upload rejected |

### 12. Expected Result
The system should allow users to upload, list, download and delete files through a browser using HTTP over TCP/IP.

### 13. Conclusion
The project demonstrates application-layer networking using a Flask client-server web application. It shows how HTTP requests travel over TCP/IP between a browser client and server and how the server processes file operations.

### 14. Future Scope
- User authentication
- Database integration
- Real cloud object storage
- HTTPS
- File sharing links
- Access permissions
- File encryption
- Virus scanning

### 15. Cloud Deployment
For Practical 10, the application can be deployed to a cloud hosting platform such as Render, Railway or PythonAnywhere. When hosted online, the Flask application runs on cloud infrastructure and clients access it through the Internet.

> Note: Some free cloud hosts use temporary/ephemeral local storage. This is fine for a short practical demonstration, but production systems should use object storage such as Amazon S3, Azure Blob Storage or Google Cloud Storage.