"""
Configuration management for web scraper application
Handles environment variables, logging, and app settings
"""

import logging
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import Field, HttpUrl, field_validator
from pydantic_settings import BaseSettings

# Load .env file
load_dotenv()

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
LOGS_DIR = PROJECT_ROOT / "logs"


class ScraperConfig(BaseSettings):
    """Web scraper configuration"""

    timeout: int = Field(default=30, description="Request timeout in seconds")
    retries: int = Field(default=3, description="Number of retries on failure")
    backoff_factor: float = Field(default=0.5, description="Retry backoff multiplier")
    rate_limit_requests_per_sec: float = Field(default=5.0, description="Rate limiting")
    use_proxy: bool = Field(default=False)
    proxy_url: Optional[str] = Field(default=None)
    user_agent: Optional[str] = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    headless_browser: bool = Field(default=True, description="Run browsers in headless mode")

    class Config:
        env_prefix = "SCRAPER_"
        case_sensitive = False


class WorkflowConfig(BaseSettings):
    """Workflow orchestration configuration"""

    schedule_interval: int = Field(default=3600, description="Default schedule interval (seconds)")
    max_concurrent_jobs: int = Field(default=5, description="Max concurrent workflow jobs")
    job_timeout: int = Field(default=3600, description="Job timeout in seconds")
    enable_celery: bool = Field(default=False, description="Use Celery for job queue")
    celery_broker_url: Optional[str] = Field(default=None)

    class Config:
        env_prefix = "WORKFLOW_"
        case_sensitive = False


class DatabaseConfig(BaseSettings):
    """Database configuration"""

    url: str = Field(default="sqlite:///./scraper.db", description="Database URL")
    echo: bool = Field(default=False, description="Echo SQL queries")
    pool_size: int = Field(default=10, description="Connection pool size")
    max_overflow: int = Field(default=20, description="Max overflow connections")
    mongodb_url: Optional[str] = Field(default=None, description="MongoDB connection URL")
    redis_url: Optional[str] = Field(default=None, description="Redis connection URL")

    class Config:
        env_prefix = "DATABASE_"
        case_sensitive = False


class MonitoringConfig(BaseSettings):
    """Monitoring and error tracking"""

    sentry_dsn: Optional[str] = Field(default=None, description="Sentry DSN for error tracking")
    sentry_env: str = Field(default="development")
    log_level: str = Field(default="INFO")
    json_logs: bool = Field(default=True, description="Output logs as JSON")

    class Config:
        env_prefix = "MONITORING_"
        case_sensitive = False


class AppConfig(BaseSettings):
    """Main application configuration"""

    app_name: str = Field(default="Web Scraper Automation")
    debug: bool = Field(default=False)
    environment: str = Field(default="development")

    # Sub-configurations
    scraper: ScraperConfig = Field(default_factory=ScraperConfig)
    workflow: WorkflowConfig = Field(default_factory=WorkflowConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    monitoring: MonitoringConfig = Field(default_factory=MonitoringConfig)

    class Config:
        case_sensitive = False
        env_nested_delimiter = "__"

    @field_validator("environment", mode="before")
    @classmethod
    def validate_environment(cls, v):
        """Validate environment value"""
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return v


def get_config() -> AppConfig:
    """Get application configuration instance"""
    return AppConfig()


# Initialize config
config = get_config()


def setup_logging():
    """Configure application logging"""
    from loguru import logger

    # Remove default handler
    logger.remove()

    # Add file handler
    LOGS_DIR.mkdir(exist_ok=True)
    log_file = LOGS_DIR / "app.log"

    logger.add(
        str(log_file),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=config.monitoring.log_level,
        rotation="500 MB",
        retention="7 days",
        serialize=config.monitoring.json_logs,
    )

    # Add console handler (development)
    if config.debug:
        logger.add(
            lambda msg: print(msg, end=""),
            format="<level>{level: <8}</level> | {message}",
            level=config.monitoring.log_level,
        )

    return logger


# Initialize logger
logger = setup_logging()

if __name__ == "__main__":
    # Print current configuration
    print("Current Configuration:")
    print(f"App: {config.app_name} (env: {config.environment})")
    print(f"Database: {config.database.url}")
    print(f"Scraper Timeout: {config.scraper.timeout}s")
    print(f"Log Level: {config.monitoring.log_level}")
