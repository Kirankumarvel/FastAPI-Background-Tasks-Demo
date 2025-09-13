from sqlalchemy import Column, Integer, String, Boolean, JSON
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, index=True)
    is_active = Column(Boolean, default=True)

class ImageProcessingJob(Base):
    __tablename__ = "image_jobs"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    operations = Column(JSON)  # List of operations to perform
    status = Column(String, default="pending")  # pending, processing, completed, failed