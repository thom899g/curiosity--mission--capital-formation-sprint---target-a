"""
Configuration management for Pipeline Sentinel.
Centralized settings with environment variable support.
"""

import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Central configuration class."""
    
    # Project paths
    PROJECT_ROOT = Path(__file__).parent.parent
    LOGS_DIR = PROJECT_ROOT / 'logs'
    CLIENTS_DIR = PROJECT_ROOT / 'clients'
    LIB_DIR = PROJECT_ROOT / 'lib'
    PRODUCTS_DIR = PROJECT_ROOT / 'products' / 'pipeline_sentinel'
    
    # Financial targets
    HS_FUND_TARGET = 2500.00  # Hardware Sovereignty Fund target
    AUDIT_PRICE = 1200.00     # Fixed price per audit
    
    # Time allocation (in hours)
    MAX_HOURS_PER_AUDIT = 8
    LIBRARY_INVESTMENT_RATIO = 0.2  # 20% of time to library
    
    # Audit parameters
    MIN_PYTHON_VERSION = (3, 8)
    MAX_FILE_SIZE_MB = 10
    
    # Security check thresholds
    SECURITY_SCORE_THRESHOLD = 70  # Minimum security score (0-100)
    CRITICAL_VULNERABILITIES_ALLOWED = 0
    
    # Report generation
    REPORT_TEMPLATE = PRODUCTS_DIR / 'report_template.jinja2'
    CHECKLIST_FILE = PRODUCTS_DIR / 'audit_checklist.json'
    
    # Firebase settings (if available)
    FIREBASE_CONFIG_PATH = PROJECT_ROOT / 'firebase_config.json'
    
    # External services (from environment variables)
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
    
    # Email settings for report delivery
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    EMAIL_USER = os.getenv('EMAIL_USER', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """
        Validate configuration and return status.
        
        Returns:
            Dictionary with validation results
        """
        validation_results = {}
        
        # Check directories
        required_dirs = [cls.LOGS_DIR, cls.CLIENTS_DIR, cls.PRODUCTS_DIR]
        for directory in required_dirs:
            validation_results[f"dir_{directory.name}"] = directory.exists()
            if not directory.exists():
                directory.mkdir(parents=True, exist_ok=True)
                validation_results[f"dir_{directory.name}_created"] = True
        
        # Check required files
        required_files = [cls.REPORT_TEMPLATE, cls.CHECKLIST_FILE]
        for file_path in required_files:
            validation_results[f"file_{file_path.name}"] = file_path.exists()
        
        # Check environment variables
        validation_results['telegram_configured'] = bool(cls.TELEGRAM_BOT_TOKEN and cls.TELEGRAM_CHAT_ID)