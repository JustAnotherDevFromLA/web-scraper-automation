"""
Main CLI entry point for the application
"""

import asyncio
import sys
from typing import Optional

import click

from src.config import config, logger
from src.database import init_db
from src.scrapers import BeautifulSoupScraper
from src.workflows import Task, Workflow, WorkflowScheduler


@click.group()
def cli():
    """Web Scraper & Workflow Automation CLI"""
    pass


@cli.command()
def init_db_cmd():
    """Initialize database tables"""
    try:
        init_db()
        click.echo(click.style("✓ Database initialized successfully!", fg="green"))
    except Exception as e:
        click.echo(click.style(f"✗ Failed to initialize database: {str(e)}", fg="red"))
        sys.exit(1)


@cli.command()
@click.option("--url", prompt="Target URL", help="URL to scrape")
@click.option("--parser", default="beautifulsoup", help="Parser type (beautifulsoup, selenium)")
def scrape(url: str, parser: str):
    """Scrape a URL"""
    try:
        click.echo(f"Scraping {url} with {parser} parser...")

        if parser == "beautifulsoup":
            scraper = BeautifulSoupScraper(url)
        else:
            from src.scrapers import SeleniumScraper

            scraper = SeleniumScraper(url)

        result = scraper.fetch()

        click.echo(click.style(f"✓ Successfully scraped {url}", fg="green"))
        click.echo(f"Title: {result.get('title', 'N/A')}")

    except Exception as e:
        click.echo(click.style(f"✗ Failed to scrape: {str(e)}", fg="red"))
        sys.exit(1)


@cli.command()
@click.option("--name", prompt="Workflow name", help="Name of workflow to create")
@click.option("--schedule", default=3600, help="Schedule interval in seconds")
def schedule_workflow(name: str, schedule: int):
    """Schedule a workflow"""
    try:
        click.echo(f"Scheduling workflow: {name}")

        # Create example workflow
        async def example_task():
            logger.info("Running example task")
            return "Task completed"

        workflow = Workflow(name)
        workflow.add_task(Task(name="step1", func=example_task))

        scheduler = WorkflowScheduler()
        scheduler.register(workflow, schedule)

        click.echo(click.style(f"✓ Workflow scheduled every {schedule}s", fg="green"))
        click.echo("Press Ctrl+C to stop...")

        scheduler.run()

    except KeyboardInterrupt:
        click.echo(click.style("\n✓ Scheduler stopped", fg="green"))
    except Exception as e:
        click.echo(click.style(f"✗ Failed to schedule workflow: {str(e)}", fg="red"))
        sys.exit(1)


@cli.command()
def config_show():
    """Show current configuration"""
    click.echo("Current Configuration:")
    click.echo(f"  App: {config.app_name}")
    click.echo(f"  Environment: {config.environment}")
    click.echo(f"  Debug: {config.debug}")
    click.echo(f"  Database: {config.database.url}")
    click.echo(f"  Scraper Timeout: {config.scraper.timeout}s")
    click.echo(f"  Log Level: {config.monitoring.log_level}")


@cli.command()
def version():
    """Show version"""
    from src import __version__

    click.echo(f"Web Scraper Automation v{__version__}")


if __name__ == "__main__":
    cli()
