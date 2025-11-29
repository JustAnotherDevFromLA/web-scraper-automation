# CONTRIBUTING.md

## Development Setup

### 1. Clone the Repository

```bash
git clone <repo-url>
cd web-scraper-automation
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -e ".[dev]"
```

### 4. Install Pre-commit Hooks

```bash
pre-commit install
pre-commit run --all-files
```

### 5. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 6. Initialize Database

```bash
python -m src.main init-db-cmd
# Or: python -c "from src.database import init_db; init_db()"
```

## Development Workflow

### Running Tests

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit -v

# With coverage
pytest --cov=src --cov-report=html

# Watch mode (requires pytest-watch)
pytest-watch -- -v

# Specific test
pytest tests/unit/test_scrapers.py::test_beautifulsoup_scraper_initialization -v
```

### Code Quality

```bash
# Format code
black src tests

# Sort imports
isort src tests

# Lint
pylint src

# Type check
mypy src --ignore-missing-imports

# Run all checks
bash scripts/lint.sh
```

### Debugging

#### With VS Code

1. Set breakpoint (click gutter)
2. Press `Cmd+Shift+D`
3. Select configuration (Python: Pytest, etc.)
4. Step through with F10/F11

#### With IPython

```bash
ipython
> from src.scrapers import BeautifulSoupScraper
> scraper = BeautifulSoupScraper("https://example.com")
> scraper.fetch()
```

#### With pdb

```python
import pdb; pdb.set_trace()
```

### Local Testing with Docker

```bash
# Start services
docker-compose up -d

# Run tests against Docker database
export DATABASE_URL=postgresql://scraper:scraper_pass@localhost:5432/scraper_db
pytest tests/integration -v

# Stop services
docker-compose down
```

## Code Style Guide

### Python

- Follow PEP 8
- Use type hints for all function signatures
- Document all public functions with docstrings
- Use Black for formatting (line length: 100)
- Import order: stdlib, third-party, local

### Imports Example

```python
# Standard library
import asyncio
from typing import Any, Dict, List, Optional

# Third-party
import requests
from sqlalchemy import Column, String

# Local
from src.config import logger
from src.utils import retry_on_exception
```

### Docstring Format

```python
def scrape(url: str, timeout: Optional[int] = None) -> Dict[str, Any]:
    """
    Scrape website data from URL

    Args:
        url: Target URL to scrape
        timeout: Request timeout in seconds (default: 30)

    Returns:
        Dictionary with scraped data including title, content, etc.

    Raises:
        requests.RequestException: If request fails
        ValueError: If URL is invalid

    Example:
        >>> from src.scrapers import BeautifulSoupScraper
        >>> scraper = BeautifulSoupScraper("https://example.com")
        >>> result = scraper.fetch()
        >>> print(result['title'])
    """
```

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add async scraper support
fix: handle timeout exceptions in retries
docs: update API documentation
test: add integration tests for workflows
chore: update dependencies
```

## Pull Request Process

1. **Create Feature Branch**

   ```bash
   git checkout -b feature/xyz
   ```

2. **Write Tests First** (TDD)

   ```bash
   # Write failing test
   # Implement feature to pass test
   # Refactor as needed
   ```

3. **Run Full Test Suite**

   ```bash
   pytest tests/ --cov=src --cov-report=term
   ```

4. **Lint & Format**

   ```bash
   black src tests && isort src tests && pylint src
   ```

5. **Commit Changes**

   ```bash
   git commit -m "feat: descriptive message"
   ```

6. **Push & Open PR**

   ```bash
   git push origin feature/xyz
   ```

7. **PR Requirements**
   - [ ] Tests pass (GitHub Actions)
   - [ ] Coverage maintained (>80%)
   - [ ] Code formatted with Black
   - [ ] No linting errors
   - [ ] Documentation updated
   - [ ] PR description includes ticket/issue reference

## Performance Guidelines

- **Caching**: Use Redis for caching scrape results
- **Batching**: Insert 500-1000 records per batch to DB
- **Concurrency**: Use async scrapers for I/O-bound operations
- **Rate Limiting**: Respect target site's rate limits
- **Profiling**: Use `pytest --profile` for slow tests

## Troubleshooting

### Import Errors

```bash
# Reinstall package
pip install -e ".[dev]"
```

### Database Issues

```bash
# Reset database
python -c "from src.database import drop_db, init_db; drop_db(); init_db()"
```

### Port Already in Use

```bash
# Find process using port 5432
lsof -i :5432
# Kill process
kill -9 <PID>
```

## Questions?

- Check existing issues/discussions
- Review documentation in `README.md`
- Ask in pull request comments
- Open a new issue with detailed description

---

**Thank you for contributing!** 🚀
