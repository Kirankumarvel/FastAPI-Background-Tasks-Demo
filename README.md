# FastAPI Background Tasks Demo

A practical demonstration of FastAPI's Background Tasks functionality for offloading heavy work and keeping API responses fast.

---


## 📁 Project Structure

```
fastapi-background-tasks-demo/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── tasks.py
│   └── email_service.py
├── requirements.txt
├── test_performance.py
└── README.md
```

---

## 🚀 Features

- 🚀 Fast response times by offloading heavy work to background tasks
- 📧 Simulated email sending in the background
- 🔔 Async notifications to external services
- 📊 Performance comparison between sync and async approaches
- 🗄️ Database operations with SQLAlchemy (async)
- ⚡ Event handlers for startup/shutdown operations

---

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.7+
- pip (Python package manager)

---

### 1. Create and Set Up the Project

```bash
mkdir fastapi-background-tasks-demo
cd fastapi-background-tasks-demo

python -m venv venv
# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Potential Errors & Solutions:**
- **Error:** `Failed building wheel for cryptography`
  - **Solution:**  
    - Ubuntu/Debian: `sudo apt-get install build-essential libssl-dev libffi-dev python3-dev`
    - Windows: Install Visual Studio Build Tools
    - macOS: `xcode-select --install`

---

### 3. Create Project Structure

```bash
mkdir app
touch app/__init__.py app/main.py app/database.py app/models.py app/schemas.py app/tasks.py app/email_service.py
touch requirements.txt
touch test_performance.py
```

---

### 4. Add the Code Files

Copy the provided code for each file into your project structure.

---

## ▶️ Running the Application

### Start the Server

```bash
uvicorn app.main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

### Access the API Documentation

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Testing the Background Tasks

### 1. User Creation with Background Tasks

- **POST `/users/`**  
  Request body:
  ```json
  {
    "email": "user@example.com",
    "username": "testuser"
  }
  ```
  - Immediate response with user data
  - Background task: Welcome email sent after response

- **POST `/users/with-notifications/`**  
  Request body:
  ```json
  {
    "email": "user2@example.com",
    "username": "testuser2"
  }
  ```
  - Immediate response
  - Background tasks: Welcome email + Discord notification

### 2. Image Processing

- **POST `/process-image/`**  
  Request body:
  ```json
  {
    "image_url": "https://example.com/sample.jpg",
    "operations": ["resize", "compress", "watermark"]
  }
  ```
  - Immediate response with job ID
  - Background task: Image processing occurs after response

### 3. Performance Comparison

- **POST `/sync-task/`**  
  Blocks until complete (~3+ seconds per request)

- **POST `/async-task/`**  
  Immediate response, work runs in background

### 4. Monitoring Background Tasks

Check your terminal/server logs for output like:
```
Simulating sending welcome email to user@example.com...
Welcome email sent to testuser at user@example.com!
Processing image from https://example.com/sample.jpg...
Image processing completed. Operations: ['resize', 'compress', 'watermark']
```

---

## 🏎️ Performance Testing

Run the included performance script:

```bash
python test_performance.py
```

**Expected Output:**
```
Testing 10 sequential requests to /sync-task/
Total time: 30.52 seconds
Average time per request: 3.05 seconds

Testing 10 concurrent requests to /async-task/
Total time: 3.21 seconds
Average time per request: 0.32 seconds

Performance improvement: 9.5x faster!
```

---

## 🔗 API Endpoints

| Method | Endpoint                   | Description                     | Background Tasks           |
|--------|----------------------------|---------------------------------|----------------------------|
| POST   | `/users/`                  | Create user                     | Welcome email              |
| POST   | `/users/with-notifications/`| Create user with notifications | Email + Discord            |
| POST   | `/process-image/`          | Process image                   | Image operations           |
| POST   | `/sync-task/`              | Sync task (blocking)            | None                       |
| POST   | `/async-task/`             | Async task (background)         | Background processing      |
| GET    | `/users/`                  | List all users                  | None                       |
| GET    | `/health`                  | Health check                    | None                       |

---

## 🗂️ Key Files Overview

- **app/main.py** – FastAPI app and endpoint definitions
- **app/tasks.py** – Background task functions
- **app/email_service.py** – Simulated email sending
- **app/database.py** – Database configuration
- **app/models.py** – SQLAlchemy models
- **app/schemas.py** – Pydantic schemas

---

## 🏆 Best Practices Demonstrated

- **Fast Responses**: Return to client immediately, work continues in background
- **Error Handling**: Robust handling in background tasks
- **Async I/O**: Use async for notification/email tasks
- **Resource Management**: Proper database and async session handling
- **Prioritization**: Multiple background tasks per endpoint

---

## 🛡️ Production Considerations

1. **Use a Task Queue**: For production, use Celery, RQ, or Dramatiq for background tasks
2. **Monitoring**: Add logging/monitoring for background tasks
3. **Retry Logic**: Implement retry for failed background jobs
4. **Resource Limits**: Prevent resource exhaustion by limiting concurrent tasks
5. **Database**: Use connection pooling and manage DB connections per task

---

## 🐞 Common Issues & Solutions

- **Background tasks not running**:  
  Ensure `BackgroundTasks` is properly injected and used.
- **DB errors in background tasks**:  
  Use separate DB sessions for background work; handle session lifecycle.
- **Performance issues**:  
  Limit concurrency, offload blocking work, use async where possible.
- **Task failures**:  
  Implement error handling and retry in your task functions.

---

## 🔧 Extending the Demo

- Integrate with a real email service (SendGrid, Mailgun)
- Add real image processing (e.g. Pillow)
- Implement task status tracking
- Secure endpoints with JWT authentication
- Add rate limiting to prevent abuse

---

## 📜 License

MIT License – Free to use for learning and development.

---

**This demo shows how FastAPI's BackgroundTasks keep your APIs fast and responsive by offloading heavy work to the background!**
