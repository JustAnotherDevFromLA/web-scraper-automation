#!/bin/bash
# Quick project setup script

set -e

echo "🚀 Setting up Web Scraper Automation project..."

# Check Python version
python_version=$(python --version | awk '{print $2}')
echo "✓ Python $python_version"

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "Installing dependencies..."
pip install -e ".[dev]"

# Install pre-commit hooks
echo "Setting up pre-commit hooks..."
pre-commit install
pre-commit run --all-files 2>/dev/null || true

# Copy environment template
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration"
fi

# Initialize database
echo "Initializing database..."
python -c "from src.database import init_db; init_db()"

echo ""
echo "✅ Project setup complete!"
echo ""
echo "Next steps:"
echo "  1. Update .env with your configuration"
echo "  2. Run tests: pytest"
echo "  3. Run linting: black src tests && isort src tests"
echo "  4. Start developing!"
echo ""
echo "For Docker setup:"
echo "  docker-compose up -d"
echo ""
