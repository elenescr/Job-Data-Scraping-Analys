import click
from src.scrapers.static_scraper import  scrape_remoteok_jobs, scrape_wwr_jobs
from src.scrapers.selenium_scraper import scrape_indeed_dynamic
from src.data.models import save_jobs_to_db
from src.data.database import init_db
from src.data.processors import clean_and_validate_jobs
from src.scrapers.remotive_scraper import scrape_remotive_jobs
from src.scrapers.jobspresso_scraper import scrape_jobspresso_jobs
from src.scrapers.jobspresso_selenium_scraper import scrape_jobspresso_jobs
from src.scrapers.europeremotely_scraper import scrape_europe_remotely_jobs
from src.scrapers.static_scraper import scrape_wwr_jobs
from src.scrapers.remotive_selenium_scraper import scrape_remotive_jobs

import csv
import json

@click.command()

@click.option(
    '--source', '-s', multiple=True,
    type=click.Choice(['indeed', 'remoteok', 'wwr', 'indeed-selenium', 'jobspresso', 'europeremotely',  'remotive-selenium'], case_sensitive=False),
    help='Choose one or more sources to scrape. Repeat --source for multiple.'
)

@click.option('--limit', '-l', default=5, help='Number of jobs per source to fetch')
@click.option('--csv', 'csv_path', default=None, help='Export results to CSV')
@click.option('--json', 'json_path', default=None, help='Export results to JSON')
def run_cli(source, limit, csv_path, json_path):

    init_db()
    all_jobs = []

    if not source:
        click.echo(" No source specified. Use --source to specify at least one.")
        return

    from concurrent.futures import ThreadPoolExecutor

    def run_scraper_for_source(src, limit):
        if src == 'indeed':
            return scrape_indeed_jobs(limit=limit)
        elif src == 'indeed-selenium':
            return scrape_indeed_dynamic(limit=limit)
        elif src == 'remoteok':
            return scrape_remoteok_jobs(limit=limit)
        elif src == 'wwr':
            return scrape_wwr_jobs(limit=limit)
        elif src == 'remotive':
            return scrape_remotive_jobs(limit=limit)
        elif src == 'jobspresso':
            return scrape_jobspresso_jobs(limit=limit)
        elif src == 'europeremotely':
            return scrape_europe_remotely_jobs(limit=limit)
        elif src == 'remotive-selenium':
            return scrape_remotive_jobs(limit=limit)
        elif src == 'remotive-selenium':
            return scrape_remotive_jobs(limit=limit)

        else:
            return []

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(run_scraper_for_source, src, limit): src for src in source}
        for future in futures:
            jobs = future.result()
            all_jobs.extend(jobs)

    if all_jobs:
        save_jobs_to_db(all_jobs)
        click.echo(f"{len(all_jobs)} jobs saved to database.")

        if csv_path:
            export_to_csv(all_jobs, csv_path)
            click.echo(f" Data exported to CSV: {csv_path}")

        if json_path:
            export_to_json(all_jobs, json_path)
            click.echo(f"Data exported to JSON: {json_path}")
    else:
        click.echo("No jobs collected.")

def export_to_csv(jobs, path):
    keys = jobs[0].keys()
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(jobs)

def export_to_json(jobs, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(jobs, f, indent=2)
