"""
Logging configuration for Stupid Duck game.
Captures errors, warnings, and debug information.
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
import traceback


class GameLogger:
    """Centralized logging system for the game."""

    def __init__(self, log_dir: str = "logs"):
        """
        Initialize the game logger.

        Args:
            log_dir: Directory to store log files
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        # Clean up old log files (keep last 10 of each type)
        self._cleanup_old_logs()

        # Create log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"game_{timestamp}.log"
        self.error_log_file = self.log_dir / f"errors_{timestamp}.log"

        # Configure main logger
        self.logger = logging.getLogger("StupidDuck")
        self.logger.setLevel(logging.DEBUG)

        # Remove existing handlers
        self.logger.handlers.clear()

        # File handler - all messages
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Error file handler - errors and critical only
        error_handler = logging.FileHandler(self.error_log_file, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d\n%(message)s\n'
        )
        error_handler.setFormatter(error_formatter)
        self.logger.addHandler(error_handler)

        # Console handler - warnings and above
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.WARNING)
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        self.logger.info("=" * 80)
        self.logger.info("Game logger initialized")
        self.logger.info(f"Log file: {self.log_file}")
        self.logger.info(f"Error log file: {self.error_log_file}")
        self.logger.info("=" * 80)

    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)

    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)

    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)

    def error(self, message: str, exc_info=None):
        """Log error message with optional exception info."""
        if exc_info:
            self.logger.error(message, exc_info=True)
        else:
            self.logger.error(message)

    def critical(self, message: str, exc_info=None):
        """Log critical error with optional exception info."""
        if exc_info:
            self.logger.critical(message, exc_info=True)
        else:
            self.logger.critical(message)

    def exception(self, message: str):
        """Log exception with full traceback."""
        self.logger.exception(message)

    def log_exception(self, exc: Exception, context: str = ""):
        """
        Log an exception with context and full traceback.

        Args:
            exc: The exception to log
            context: Additional context about where/when the error occurred
        """
        error_msg = f"{context}\n" if context else ""
        error_msg += f"Exception: {type(exc).__name__}: {str(exc)}\n"
        error_msg += f"Traceback:\n{''.join(traceback.format_tb(exc.__traceback__))}"

        self.logger.error(error_msg)

    def shutdown(self):
        """Close all handlers and shutdown logging."""
        self.logger.info("=" * 80)
        self.logger.info("Game logger shutting down")
        self.logger.info("=" * 80)

        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

    def _cleanup_old_logs(self, keep: int = 10):
        """Remove old log files, keeping the most recent ones."""
        try:
            for prefix in ("game_", "errors_"):
                log_files = sorted(
                    self.log_dir.glob(f"{prefix}*.log"),
                    key=lambda f: f.stat().st_mtime,
                    reverse=True
                )
                for old_file in log_files[keep:]:
                    try:
                        old_file.unlink()
                    except OSError:
                        pass
        except Exception:
            pass  # Don't fail startup over log cleanup

    def get_latest_errors(self, count: int = 10) -> list:
        """
        Read the latest errors from the error log.

        Args:
            count: Number of recent errors to retrieve

        Returns:
            List of error messages
        """
        try:
            if not self.error_log_file.exists():
                return []

            with open(self.error_log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Group lines into error blocks (separated by blank lines)
            errors = []
            current_error = []

            for line in lines:
                if line.strip():
                    current_error.append(line)
                elif current_error:
                    errors.append(''.join(current_error))
                    current_error = []

            if current_error:
                errors.append(''.join(current_error))

            return errors[-count:]
        except Exception as e:
            self.logger.error(f"Failed to read error log: {e}")
            return []


# Global logger instance
_game_logger = None


def get_logger() -> GameLogger:
    """Get or create the global game logger instance."""
    global _game_logger
    if _game_logger is None:
        _game_logger = GameLogger()
    return _game_logger


def shutdown_logger():
    """Shutdown the global logger."""
    global _game_logger
    if _game_logger is not None:
        _game_logger.shutdown()
        _game_logger = None
