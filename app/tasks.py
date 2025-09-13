import asyncio
import random
import time
import httpx
from typing import List, Dict, Any
from .email_service import email_service

async def send_welcome_email(email: str, username: str):
    """Background task to send welcome email"""
    try:
        success = await email_service.send_welcome_email(email, username)
        if not success:
            print(f"Warning: Email to {email} failed, might need retry logic")
    except Exception as e:
        print(f"Error sending welcome email to {email}: {e}")

async def send_discord_notification(username: str):
    """Background task to send Discord notification"""
    webhook_url = "https://discord.com/api/webhooks/your/webhook"
    message = {"content": f"🎉 New user signed up: {username}!"}
    
    try:
        async with httpx.AsyncClient() as client:
            # In a real app, you'd use an actual webhook URL
            # For demo purposes, we'll simulate the API call
            await asyncio.sleep(1)  # Simulate network delay
            print(f"✅ Discord notification sent for user: {username}")
    except Exception as e:
        print(f"Error sending Discord notification: {e}")

async def process_image_task(image_url: str, operations: List[str]) -> Dict[str, Any]:
    """Background task to process images"""
    print(f"🖼️ Processing image from {image_url}...")
    
    try:
        # Simulate different processing times based on operations
        processing_time = 0.5
        if "resize" in operations:
            processing_time += 1.0
            print("  ↳ Resizing image...")
            await asyncio.sleep(1.0)
        
        if "compress" in operations:
            processing_time += 0.8
            print("  ↳ Compressing image...")
            await asyncio.sleep(0.8)
        
        if "watermark" in operations:
            processing_time += 1.2
            print("  ↳ Adding watermark...")
            await asyncio.sleep(1.2)
        
        if "filter" in operations:
            processing_time += 0.7
            print("  ↳ Applying filter...")
            await asyncio.sleep(0.7)
        
        # Simulate occasional failure
        if random.random() < 0.05:  # 5% chance of failure
            raise Exception("Image processing failed due to corrupt file")
        
        print(f"✅ Image processing completed in {processing_time:.1f}s. Operations: {operations}")
        return {"status": "success", "processing_time": processing_time}
    
    except Exception as e:
        print(f"❌ Image processing failed: {e}")
        return {"status": "failed", "error": str(e)}

def heavy_computation_task(duration: float = 3.0):
    """CPU-intensive task (blocking) - should use BackgroundTasks.add_task"""
    print(f"🧮 Starting heavy computation for {duration} seconds...")
    time.sleep(duration)  # This is blocking!
    result = sum(i * i for i in range(1000000))
    print(f"✅ Heavy computation completed. Result: {result}")
    return result

async def async_heavy_computation_task(duration: float = 3.0):
    """Async version of heavy computation (non-blocking)"""
    print(f"🧮 Starting async heavy computation for {duration} seconds...")
    await asyncio.sleep(duration)  # This is non-blocking
    # For real CPU-bound work, you'd use asyncio.to_thread()
    result = await asyncio.to_thread(lambda: sum(i * i for i in range(1000000)))
    print(f"✅ Async heavy computation completed. Result: {result}")
    return result