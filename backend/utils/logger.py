"""
Structured logging utilities for process tracking
"""

import logging
import logging.handlers
import time
import uuid
from typing import Dict, Any, Optional
from datetime import datetime
from functools import wraps
from contextlib import contextmanager


class ProcessLogger:
    """Enhanced logger for process tracking with structured data"""
    
    def __init__(self, logger_name: str):
        self.logger = logging.getLogger(logger_name)
        self.process_stack = []
    
    def start_process(self, process_name: str, **kwargs) -> str:
        """Start a new process and return process ID"""
        process_id = str(uuid.uuid4())[:8]
        process_data = {
            "process_id": process_id,
            "process_name": process_name,
            "start_time": time.time(),
            "start_timestamp": datetime.now().isoformat(),
            "metadata": kwargs
        }
        
        self.process_stack.append(process_data)
        
        # Filter out reserved logging keys
        reserved_keys = {'filename', 'module', 'funcName', 'lineno', 'created', 'msecs', 'relativeCreated', 'thread', 'threadName', 'processName', 'process', 'message', 'name'}
        safe_kwargs = {k: v for k, v in kwargs.items() if k not in reserved_keys}
        
        self.logger.info(
            f"Process started: {process_name}",
            extra={
                "event": "process_start",
                "process_id": process_id,
                "process_name": process_name,
                "timestamp": process_data["start_timestamp"],
                **safe_kwargs
            }
        )
        
        return process_id
    
    def end_process(self, process_id: Optional[str] = None, **kwargs):
        """End a process (with optional process ID)"""
        if not self.process_stack:
            return
            
        process_data = self.process_stack.pop()
        if process_id and process_data["process_id"] != process_id:
            # Put it back and try to find matching process
            self.process_stack.append(process_data)
            return
        
        duration = time.time() - process_data["start_time"]
        
        # Filter out reserved logging keys
        reserved_keys = {'filename', 'module', 'funcName', 'lineno', 'created', 'msecs', 'relativeCreated', 'thread', 'threadName', 'processName', 'process', 'message', 'name'}
        safe_kwargs = {k: v for k, v in kwargs.items() if k not in reserved_keys}
        
        self.logger.info(
            f"Process completed: {process_data['process_name']} ({duration:.3f}s)",
            extra={
                "event": "process_end",
                "process_id": process_data["process_id"],
                "process_name": process_data["process_name"],
                "duration_seconds": round(duration, 3),
                "timestamp": datetime.now().isoformat(),
                "start_time": process_data["start_timestamp"],
                **safe_kwargs
            }
        )
    
    def log_step(self, step_name: str, **kwargs):
        """Log a step within the current process"""
        current_process = self.process_stack[-1] if self.process_stack else None
        
        # Filter out reserved logging keys
        reserved_keys = {'filename', 'module', 'funcName', 'lineno', 'created', 'msecs', 'relativeCreated', 'thread', 'threadName', 'processName', 'process', 'message', 'name'}
        safe_kwargs = {k: v for k, v in kwargs.items() if k not in reserved_keys}
        
        extra_data = {
            "event": "process_step",
            "step_name": step_name,
            "timestamp": datetime.now().isoformat(),
            **safe_kwargs
        }
        
        if current_process:
            extra_data.update({
                "process_id": current_process["process_id"],
                "process_name": current_process["process_name"],
                "process_elapsed": round(time.time() - current_process["start_time"], 3)
            })
        
        self.logger.info(f"Step: {step_name}", extra=extra_data)
    
    def log_error(self, error: Exception, **kwargs):
        """Log an error with process context"""
        current_process = self.process_stack[-1] if self.process_stack else None
        
        # Filter out reserved logging keys
        reserved_keys = {'filename', 'module', 'funcName', 'lineno', 'created', 'msecs', 'relativeCreated', 'thread', 'threadName', 'processName', 'process', 'message', 'name'}
        safe_kwargs = {k: v for k, v in kwargs.items() if k not in reserved_keys}
        
        extra_data = {
            "event": "process_error",
            "error_type": type(error).__name__,
            "error_message": str(error),
            "timestamp": datetime.now().isoformat(),
            **safe_kwargs
        }
        
        if current_process:
            extra_data.update({
                "process_id": current_process["process_id"],
                "process_name": current_process["process_name"],
                "process_elapsed": round(time.time() - current_process["start_time"], 3)
            })
        
        self.logger.error(f"Process error: {error}", exc_info=True, extra=extra_data)
    
    def log_warning(self, message: str, **kwargs):
        """Log a warning with process context"""
        current_process = self.process_stack[-1] if self.process_stack else None
        
        # Filter out reserved logging keys
        reserved_keys = {'filename', 'module', 'funcName', 'lineno', 'created', 'msecs', 'relativeCreated', 'thread', 'threadName', 'processName', 'process', 'message', 'name'}
        safe_kwargs = {k: v for k, v in kwargs.items() if k not in reserved_keys}
        
        extra_data = {
            "event": "process_warning",
            "warning_message": message,  # Changed from "message" to avoid conflict
            "timestamp": datetime.now().isoformat(),
            **safe_kwargs
        }
        
        if current_process:
            extra_data.update({
                "process_id": current_process["process_id"],
                "process_name": current_process["process_name"],
                "process_elapsed": round(time.time() - current_process["start_time"], 3)
            })
        
        self.logger.warning(message, extra=extra_data)
    
    def get_current_process_id(self) -> Optional[str]:
        """Get the current process ID"""
        return self.process_stack[-1]["process_id"] if self.process_stack else None


def with_process_logging(process_name: str = None):
    """Decorator to add process logging to functions"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            logger = get_process_logger(func.__module__)
            name = process_name or f"{func.__module__}.{func.__name__}"
            
            process_id = logger.start_process(
                name,
                function=func.__name__,
                args_count=len(args),
                kwargs=list(kwargs.keys())
            )
            
            try:
                result = await func(*args, **kwargs)
                logger.end_process(process_id, result_type=type(result).__name__)
                return result
            except Exception as e:
                logger.log_error(e, function=func.__name__)
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            logger = get_process_logger(func.__module__)
            name = process_name or f"{func.__module__}.{func.__name__}"
            
            process_id = logger.start_process(
                name,
                function=func.__name__,
                args_count=len(args),
                kwargs=list(kwargs.keys())
            )
            
            try:
                result = func(*args, **kwargs)
                logger.end_process(process_id, result_type=type(result).__name__)
                return result
            except Exception as e:
                logger.log_error(e, function=func.__name__)
                raise
        
        # Return appropriate wrapper based on whether function is async
        import inspect
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


@contextmanager
def process_context(logger: ProcessLogger, process_name: str, **kwargs):
    """Context manager for process logging"""
    process_id = logger.start_process(process_name, **kwargs)
    try:
        yield process_id
    except Exception as e:
        logger.log_error(e)
        raise
    finally:
        logger.end_process(process_id)


# Global process logger cache
_process_loggers: Dict[str, ProcessLogger] = {}


def get_process_logger(logger_name: str) -> ProcessLogger:
    """Get or create a process logger instance"""
    if logger_name not in _process_loggers:
        _process_loggers[logger_name] = ProcessLogger(logger_name)
    return _process_loggers[logger_name]


def log_file_operation(operation: str, file_id: str, file_name: str = None, **kwargs):
    """Log file operations with consistent format"""
    logger = logging.getLogger("file_operations")
    
    extra_data = {
        "event": "file_operation",
        "operation": operation,
        "file_id": file_id,
        "file_name": file_name,
        "timestamp": datetime.now().isoformat(),
        **kwargs
    }
    
    logger.info(f"File {operation}: {file_name or file_id}", extra=extra_data)


def log_comparison_operation(operation: str, comparison_id: str = None, 
                           file1_id: str = None, file2_id: str = None, **kwargs):
    """Log comparison operations with consistent format"""
    logger = logging.getLogger("comparison_operations")
    
    extra_data = {
        "event": "comparison_operation",
        "operation": operation,
        "comparison_id": comparison_id,
        "file1_id": file1_id,
        "file2_id": file2_id,
        "timestamp": datetime.now().isoformat(),
        **kwargs
    }
    
    logger.info(f"Comparison {operation}: {comparison_id}", extra=extra_data)


class StructuredFormatter(logging.Formatter):
    """Structured JSON formatter for better log parsing"""
    
    def format(self, record: logging.LogRecord) -> str:
        import json
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add extra fields if they exist
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "file_id"):
            log_data["file_id"] = record.file_id
        if hasattr(record, "operation"):
            log_data["operation"] = record.operation
        if hasattr(record, "duration"):
            log_data["duration"] = record.duration
        
        # Add exception info if present
        if record.exc_info:
            import traceback
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": traceback.format_exception(*record.exc_info)
            }
        
        return json.dumps(log_data, default=str)


class ColoredFormatter(logging.Formatter):
    """Colored console formatter for development"""
    
    COLORS = {
        "DEBUG": "\033[36m",      # Cyan
        "INFO": "\033[32m",       # Green
        "WARNING": "\033[33m",    # Yellow
        "ERROR": "\033[31m",      # Red
        "CRITICAL": "\033[35m",   # Magenta
        "RESET": "\033[0m"        # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        reset = self.COLORS["RESET"]
        
        # Basic format with colors
        formatted = (
            f"{color}[{self.formatTime(record)}] "
            f"{record.levelname:8} "
            f"{record.name}: {record.getMessage()}{reset}"
        )
        
        # Add exception info if present
        if record.exc_info:
            formatted += f"\n{self.formatException(record.exc_info)}"
        
        return formatted


def setup_logging():
    """Setup enhanced logging configuration"""
    import logging
    import sys
    from pathlib import Path
    from app.config import get_settings
    
    settings = get_settings()
    
    # Create logs directory
    log_dir = Path(settings.log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler with colors for development
    if settings.debug:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(ColoredFormatter())
        root_logger.addHandler(console_handler)
    else:
        # Production console handler (JSON format)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(StructuredFormatter())
        root_logger.addHandler(console_handler)
    
    # File handler with JSON format
    try:
        import logging.handlers
        file_handler = logging.handlers.RotatingFileHandler(
            settings.log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(StructuredFormatter())
        root_logger.addHandler(file_handler)
    except Exception as e:
        print(f"Failed to setup file logging: {e}")
    
    # Set specific logger levels
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("websockets").setLevel(logging.WARNING)