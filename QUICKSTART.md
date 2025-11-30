# QUICKSTART.md

## Project Overview

**Web Scraper Automation** is a production-ready Python framework for:

- 🕷️ Multi-method web scraping (BeautifulSoup, Selenium, Async)
- ⚙️ Workflow orchestration and job scheduling
- 📊 Data processing and storage (PostgreSQL, MongoDB, Redis)
- 🛡️ Enterprise-grade error handling and retry logic
- ✅ Comprehensive testing with pytest
- 🚀 CI/CD ready with GitHub Actions

## 5-Minute Quick Start

### 1. Setup Environment

```bash
cd /Users/alexkocharyan/web-scraper-automation
bash setup.sh
```

Or manually:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
python -c "from src.database import init_db; init_db()"
```

### 2. Verify Installation

```bash
# Run tests
pytest tests/unit -v

# Check imports
python -c "from src.scrapers import BeautifulSoupScraper; print('✓ Imports OK')"
```

### 3. Run Your First Scrape

```bash
# Using CLI
python -m src.main scrape --url "https://example.com"

# Using Python code
python << 'EOF'
from src.scrapers import BeautifulSoupScraper

scraper = BeautifulSoupScraper("https://example.com")
result = scraper.fetch()
print(f"Title: {result['title']}")
EOF
```

### 4. Create Your First Workflow

```python
# file: scrape_workflow.py
import asyncio
from src.workflows import Workflow, Task
from src.scrapers import BeautifulSoupScraper

async def fetch_example():
    scraper = BeautifulSoupScraper("https://example.com")
    result = scraper.fetch()
    return result

async def process_data(data):
    print(f"Processing: {data}")
    return data

async def main():
    workflow = Workflow("my_first_workflow")
    workflow.add_task(Task(name="fetch", func=fetch_example))
    workflow.add_task(Task(name="process", func=process_data))

    run = await workflow.execute()
    print(run.to_dict())

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python scrape_workflow.py
```

## Common Commands

### Testing

```bash
pytest                           # Run all tests
pytest -v                       # Verbose output
pytest tests/unit -k "scraper"  # Filter by name
pytest --cov=src                # With coverage
pytest -m "not slow"            # Skip slow tests
```

### Code Quality

```bash
black src tests        # Format code
isort src tests        # Sort imports
pylint src             # Lint
mypy src               # Type check
```

### Database

```bash
# Initialize
python -c "from src.database import init_db; init_db()"

# Reset
python -c "from src.database import drop_db, init_db; drop_db(); init_db()"

# Query
python << 'EOF'
from src.database import get_session
from src.database import ScrapedData

with get_session() as session:
    rows = session.query(ScrapedData).all()
    print(f"Found {len(rows)} records")
EOF
```

### Docker

```bash
docker-compose up -d           # Start services (PostgreSQL, MongoDB, Redis)
docker-compose down            # Stop services
docker-compose logs -f app     # View logs
```

## Project Structure

```
web-scraper-automation/
├── src/
│   ├── scrapers/          # Multiple scraper implementations
│   ├── workflows/         # Job orchestration
│   ├── config/            # Configuration management
│   ├── database/          # Models & ORM
│   ├── utils/             # Utilities & decorators
│   └── main.py           # CLI entry point
├── tests/
│   ├── unit/             # Unit tests (~80% coverage)
│   ├── integration/      # Integration tests
│   └── fixtures.py       # Shared test fixtures
├── .github/workflows/    # CI/CD pipeline
├── pyproject.toml        # Dependencies & config
├── docker-compose.yml    # Multi-service setup
├── .pre-commit-config.yaml  # Git hooks
└── README.md            # Full documentation
```

## Key Features Explained

### Scrapers

Multiple scraper types for different use cases:

```python
# Static HTML - Fast & Lightweight
from src.scrapers import BeautifulSoupScraper
scraper = BeautifulSoupScraper(url)

# JavaScript-heavy sites - Slower but handles JS
from src.scrapers import SeleniumScraper
scraper = SeleniumScraper(url)

# High concurrency - Async I/O
from src.scrapers import AsyncScraper
scraper = AsyncScraper(url)
```

### Workflows

Chain tasks with automatic error handling:

```python
workflow = Workflow("daily_scrape")

# Add tasks that run sequentially
workflow.add_task(Task(name="scrape", func=scrape_handler))
workflow.add_task(Task(name="transform", func=transform_data))
workflow.add_task(Task(name="store", func=store_in_db))

run = await workflow.execute()
print(f"Status: {run.status}")
print(f"Duration: {run.duration}s")
```

### Configuration

Environment-based config with validation:

```python
from src.config import config

# Access settings
print(config.scraper.timeout)           # 30
print(config.database.url)              # sqlite:///./scraper.db
print(config.monitoring.log_level)      # INFO

# All configs auto-loaded from .env
```

### Error Handling

Built-in retry logic with exponential backoff:

```python
from src.utils import retry_on_exception

@retry_on_exception(max_retries=3, backoff=1.5)
def fetch_data():
    # Automatically retries 3x with backoff
    return scraper.fetch()
```

## Performance Tips

1. **Use BeautifulSoup for static sites** (fast, no JS overhead)
2. **Use AsyncScraper for multiple URLs** (concurrent requests)
3. **Cache results** with Redis to avoid re-scraping
4. **Batch database inserts** (500-1000 per batch)
5. **Monitor with logs** and Sentry for errors

## Debugging

### See logs in real-time

```bash
tail -f logs/app.log | jq  # Pretty JSON logs
```

### Enable debug mode in .env

```bash
DEBUG=true
MONITORING_LOG_LEVEL=DEBUG
```

### VS Code Debugging

1. Click breakpoint (left gutter)
2. Press `Cmd+Shift+D`
3. Select configuration
4. Step through with F10/F11

## Next Steps

1. **Update .env** with your database and API keys
2. **Write first test** in `tests/unit/test_*.py`
3. **Create scraper** for your target site
4. **Build workflow** to chain tasks
5. **Deploy** with Docker or GitHub Actions

## Help & Troubleshooting

**Tests failing?**

```bash
pytest -vvs --tb=long tests/unit/test_name.py
```

**Import errors?**

```bash
pip install -e ".[dev]"
```

**Database connection error?**
Check `DATABASE_URL` in `.env` and ensure database is running.

**Need more info?**

- Read full docs in `README.md`
- Check `CONTRIBUTING.md` for development guide
- Review code examples in `tests/`

---

**Happy scraping!** 🚀

Questions? Open an issue or check the documentation.
