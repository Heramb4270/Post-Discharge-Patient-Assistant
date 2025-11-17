"""
Logging utility for the multi-agent medical system
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

class MedicalSystemLogger:
    """Custom logger for medical agent system"""
    
    _instance: Optional[logging.Logger] = None
    
    @classmethod
    def get_logger(cls, name: str = "medical_agent_system", level: int = logging.INFO) -> logging.Logger:
        """
        Get or create logger instance
        
        Args:
            name: Logger name
            level: Logging level
            
        Returns:
            Configured logger instance
        """
        if cls._instance is None:
            cls._instance = cls._setup_logger(name, level)
        return cls._instance
    
    @classmethod
    def _setup_logger(cls, name: str, level: int) -> logging.Logger:
        """Setup logger with file and console handlers"""
        
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.handlers.clear()
        
        # Create logs directory if it doesn't exist
        log_dir = Path(__file__).parent.parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # Console handler (stdout)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        
        # File handler (detailed logs)
        log_file = log_dir / f"medical_system_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        
        # Error file handler
        error_log_file = log_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.log"
        error_handler = logging.FileHandler(error_log_file, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        
        # Add handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.addHandler(error_handler)
        
        return logger


# Convenience function
def setup_logger(name: str = "medical_agent_system", level: int = logging.INFO) -> logging.Logger:
    """
    Setup and return logger instance
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        Configured logger
    """
    return MedicalSystemLogger.get_logger(name, level)


# Default logger instance
logger = setup_logger()


# Agent-specific loggers
def log_receptionist(message: str, level: str = "info"):
    """Log receptionist agent activity"""
    log_func = getattr(logger, level.lower(), logger.info)
    log_func(f"[RECEPTIONIST] {message}")


def log_clinical(message: str, level: str = "info"):
    """Log clinical agent activity"""
    log_func = getattr(logger, level.lower(), logger.info)
    log_func(f"[CLINICAL] {message}")


def log_workflow(message: str, level: str = "info"):
    """Log workflow/graph activity"""
    log_func = getattr(logger, level.lower(), logger.info)
    log_func(f"[WORKFLOW] {message}")


def log_tool(tool_name: str, message: str, level: str = "info"):
    """Log tool execution"""
    log_func = getattr(logger, level.lower(), logger.info)
    log_func(f"[TOOL:{tool_name.upper()}] {message}")