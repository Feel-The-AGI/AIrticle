"""Application Configuration"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'SECRET_KEY_BACKUP')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = os.getenv('FLASK_ENV') == 'development'

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
