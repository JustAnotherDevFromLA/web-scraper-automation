# Web Scraper & Workflow Automation Project

Professional Python framework for web scraping, data extraction, and workflow automation with enterprise-grade reliability, testing, and monitoring.

## Features

- 🕷️ **Multi-backend scraping**: Requests, BeautifulSoup, Selenium, Scrapy, Playwright
- ⚙️ **Workflow automation**: Task scheduling, job orchestration, retry logic
- 📊 **Data processing**: Pandas, Polars integration for transformation
- 🗄️ **Multi-database**: PostgreSQL, MongoDB, Redis support
- 🔄 **Async support**: Concurrent scraping with asyncio & aiohttp
- 🛡️ **Error handling**: Retry mechanisms, rate limiting, graceful degradation
- 📝 **Structured logging**: Loguru with JSON export
- ✅ **Testing**: Pytest with fixtures, mocks, and integration tests
- 🚀 **CI/CD ready**: GitHub Actions, pre-commit hooks, code quality gates
- 📈 **Monitoring**: Sentry integration, error tracking, performance metrics

## Quick Start

### 1. Clone & Setup

```bash
git clone <repo-url>
cd web-scraper-automation
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys, database URLs, etc.
```

### 3. Run Tests

```bash
pytest                          # All tests
pytest tests/unit              # Unit tests only
pytest -m "not slow"           # Exclude slow tests
pytest --cov=src --cov-report=html  # With coverage
```

### 4. Start a Scraper

```bash
python src/scrapers/example_scraper.py
```

### 5. Schedule a Workflow

```bash
python src/workflows/job_scheduler.py
```

## Project Structure

```
web-scraper-automation/
├── src/
│   ├── __init__.py
│   ├── scrapers/          # Scraper modules (BeautifulSoup, Selenium, etc.)
│   ├── workflows/         # Workflow & job orchestration
│   ├── config/            # Configuration (env, settings)
│   ├── database/          # Database models & access layer
│   ├── utils/             # Utilities (logging, retry, cache)
│   └── main.py           # CLI entry point
├── tests/
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── fixtures/         # Test data & fixtures
├── .github/
│   └── workflows/        # GitHub Actions CI/CD
├── config/
│   ├── .env.example      # Environment template
│   └── settings.yaml     # Configuration file
├── logs/                 # Application logs (gitignored)
├── data/
│   └── cache/            # Cached data (gitignored)
├── README.md            # This file
├── .gitignore           # Git ignore rules
├── .pre-commit-config.yaml  # Pre-commit hooks
├── pyproject.toml       # Project metadata & dependencies
├── Dockerfile           # Container configuration
└── docker-compose.yml   # Multi-service setup
```

## Core Modules

### Scrapers (`src/scrapers/`)

```python
from src.scrapers import BeautifulSoupScraper, SeleniumScraper

# Simple scraper
scraper = BeautifulSoupScraper(url="https://example.com")
data = scraper.fetch()

# JavaScript-heavy sites
browser_scraper = SeleniumScraper(url="https://example.com")
data = browser_scraper.fetch_with_js()
```

### Workflows (`src/workflows/`)

```python
from src.workflows import Workflow, Task

workflow = Workflow(name="daily_scrape")
workflow.add_task(Task(name="fetch_data", func=scrape_handler))
workflow.add_task(Task(name="transform", func=transform_data))
workflow.add_task(Task(name="store", func=store_in_db))

workflow.execute()
```

### Configuration (`src/config/`)

```python
from src.config import AppConfig

config = AppConfig.from_env()
print(config.database_url)
print(config.scraper_timeout)
```

### Database (`src/database/`)

```python
from src.database import SessionLocal, get_session

with get_session() as session:
    results = session.query(ScrapedData).all()
```

## Configuration

### Environment Variables (`.env`)

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/scraper_db
MONGODB_URL=mongodb://localhost:27017/scraper_db

# Scraping
SCRAPER_TIMEOUT=30
SCRAPER_RETRIES=3
RATE_LIMIT_REQUESTS_PER_SECOND=5

# Workflow
WORKFLOW_SCHEDULE_INTERVAL=3600  # seconds
MAX_CONCURRENT_JOBS=5

# Monitoring
SENTRY_DSN=https://...@sentry.io/...
LOG_LEVEL=INFO

# Proxy & Headers
USE_PROXY=false
PROXY_URL=http://proxy.example.com:8080
USER_AGENT=Mozilla/5.0...
```

## Testing

### Unit Tests

```bash
pytest tests/unit -v
```

### Integration Tests

```bash
pytest tests/integration -v
```

### With Coverage

```bash
pytest --cov=src --cov-report=html --cov-report=term
```

### Watch Mode

```bash
pytest-watch -- -v
```

## CI/CD Pipeline

GitHub Actions automatically:

- ✅ Runs all tests on push/PR
- ✅ Checks code coverage (threshold: 80%)
- ✅ Lints with Black, isort, Pylint
- ✅ Type checks with mypy
- ✅ Builds Docker image
- ✅ Deploys to staging/production

See `.github/workflows/` for details.

## Performance Tips

1. **Use connection pooling** for HTTP requests (already configured)
2. **Cache responses** to avoid redundant requests
3. **Batch database inserts** (500-1000 per batch)
4. **Use async scrapers** for I/O-bound operations
5. **Monitor rate limits** and adjust concurrency
6. **Profile slow tests** with `pytest --profile`

## Debugging

### Enable Debug Logging

```python
import logging
logging.getLogger("src").setLevel(logging.DEBUG)
```

### Use IPython Debugger

```bash
ipython
> from src.scrapers import BeautifulSoupScraper
> scraper = BeautifulSoupScraper("https://example.com")
> scraper.fetch()
```

### VS Code Debugging

1. Create breakpoint (click gutter)
2. Press `Cmd+Shift+D`
3. Select "Python: Pytest (Debug All)"
4. Step through with F10/F11

## Deployment

### Docker

```bash
docker build -t web-scraper:latest .
docker run -e DATABASE_URL=... web-scraper:latest
```

### Docker Compose

```bash
docker-compose up -d
```

## Monitoring & Logging

All logs are structured and sent to:

- Local files: `logs/` directory
- Sentry: Error tracking and alerting
- CloudWatch/ELK: (optional integration)

View logs:

```bash
tail -f logs/app.log | jq  # Pretty JSON logs
```

## Contributing

1. Create feature branch: `git checkout -b feature/xyz`
2. Write tests before code (TDD)
3. Run linters: `black . && isort . && pylint src/`
4. Commit: `git commit -m "feat: xyz"`
5. Push & create PR

## Troubleshooting

### Issue: Tests failing

```bash
pytest -vvs --tb=long tests/unit/test_name.py
```

### Issue: Database connection error

Check `DATABASE_URL` in `.env` and ensure database is running.

### Issue: Scraper times out

Increase `SCRAPER_TIMEOUT` or check target site's response time.

## License

MIT - See LICENSE file

## Support

For issues, questions, or contributions, open a GitHub issue or reach out to the team.

---

**Last Updated**: November 29, 2025  
**Version**: 0.1.0  
**Status**: In Development
