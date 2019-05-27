"""
File Path: application/config.py
Description: Application Constants
Copyright (c) 2019. This Application has been developed by OR73.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Set Flask configuration vars"""

    # General Config
    FLASK_APP: str = os.environ.get('FLASK_APP')
    FLASK_DEBUG: bool = os.environ.get('FLASK_DEBUG')
    SECRET_KEY: str = os.environ.get('SECRET_KEY')

    # Database
    SQLALCHEMY_DATABASE_URI: str = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
