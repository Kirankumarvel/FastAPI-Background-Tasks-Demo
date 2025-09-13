from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import asyncio
import time
from contextlib import asynccontextmanager

from . import models, schemas, tasks
from .database import engine, get_async_db, Base

# Application lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    print("🚀 Starting up FastAPI Background Tasks Demo...")
    
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Database tables created")
    yield
    
    # Shutdown code
    print("🛑 Shutting down...")
    await engine.dispose()

app = FastAPI(
    title="FastAPI Background Tasks Demo",
    description="Demonstration of offloading heavy work to background tasks",
    version="1.0.0",
    lifespan=lifespan
)

# In-memory storage for demo purposes
fake_db = {}

@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: schemas.UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_async_db)
):
    # Check if user already exists
    if user.email in fake_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Save user to in-memory DB for demo
    fake_db[user.email] = user
    
    # Add background task to send welcome email
    background_tasks.add_task(tasks.send_welcome_email, user.email, user.username)
    
    # Return immediate response
    return {
        "id": len(fake_db),
        "email": user.email,
        "username": user.username,
        "is_active": True,
        "message": "User created successfully! Welcome email is being sent in the background."
    }

@app.post("/users/with-notifications/", response_model=schemas.User)
async def create_user_with_notifications(
    user: schemas.UserCreate,
    background_tasks: BackgroundTasks
):
    if user.email in fake_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    fake_db[user.email] = user
    
    # Add multiple background tasks
    background_tasks.add_task(tasks.send_welcome_email, user.email, user.username)
    background_tasks.add_task(tasks.send_discord_notification, user.username)
    
    return {
        "id": len(fake_db),
        "email": user.email,
        "username": user.username,
        "is_active": True,
        "message": "User created! Notifications are being sent in the background."
    }

@app.post("/process-image/", response_model=schemas.ImageProcessingResponse)
async def process_image(
    request: schemas.ImageProcessingRequest,
    background_tasks: BackgroundTasks
):
    job_id = len(fake_db) + 1  # Simple ID generation
    
    # Add image processing task to background
    background_tasks.add_task(tasks.process_image_task, request.image_url, request.operations)
    
    return {
        "job_id": job_id,
        "status": "queued",
        "message": f"Image processing started in background. Operations: {request.operations}"
    }

@app.post("/sync-task/")
async def run_sync_task(request: schemas.TaskRequest):
    """Synchronous task - blocks until complete"""
    start_time = time.time()
    
    # This blocks the event loop!
    result = tasks.heavy_computation_task(request.duration)
    
    processing_time = time.time() - start_time
    return {
        "task": request.task_name,
        "result": result,
        "processing_time": f"{processing_time:.2f}s",
        "message": "Task completed synchronously (blocking)"
    }

@app.post("/async-task/")
async def run_async_task(
    request: schemas.TaskRequest,
    background_tasks: BackgroundTasks
):
    """Asynchronous task - returns immediately, runs in background"""
    start_time = time.time()
    
    # This returns immediately and runs in background
    background_tasks.add_task(tasks.async_heavy_computation_task, request.duration)
    
    processing_time = time.time() - start_time
    return {
        "task": request.task_name,
        "processing_time": f"{processing_time:.2f}s",
        "message": "Task started in background (non-blocking)"
    }

@app.get("/users/", response_model=list[schemas.User])
async def list_users():
    """List all users (for testing)"""
    return [
        {"id": i, "email": email, "username": user.username, "is_active": True}
        for i, (email, user) in enumerate(fake_db.items(), 1)
    ]

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Background tasks demo is running"}