import asyncio
import random
from typing import Optional

class EmailService:
    @staticmethod
    async def send_welcome_email(email: str, username: str) -> bool:
        """Simulate sending a welcome email asynchronously"""
        print(f"📧 Preparing to send welcome email to {email}...")
        
        # Simulate network delay
        await asyncio.sleep(2)
        
        # Simulate occasional failure
        if random.random() < 0.1:  # 10% chance of failure
            print(f"❌ Failed to send email to {email}")
            return False
        
        print(f"✅ Welcome email sent to {username} at {email}!")
        return True

    @staticmethod
    async def send_password_reset(email: str, token: str) -> bool:
        """Simulate sending a password reset email"""
        print(f"📧 Preparing to send password reset email to {email}...")
        await asyncio.sleep(1.5)
        
        if random.random() < 0.1:
            print(f"❌ Failed to send password reset email to {email}")
            return False
        
        print(f"✅ Password reset email sent to {email} with token {token}")
        return True

email_service = EmailService()