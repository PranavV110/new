import pandas as pd
from datetime import datetime, timedelta
import pickle
import os
from pathlib import Path
import requests
from scrapers.core import AuthorInfo
from scrapers.core import *
from scrapers.nytimes_scraper.nytimes_main import NyTimesScraper
from scrapers.semantic_scholar_scraper.semantic_scholar_scraper import SemanticScholarScraper
from scrapers.arxiv_scraper.arxiv import ArxivScraper
from scrapers.kdd_scraper.kdd import KddScraper
from scrapers.nips_scraper.nips import NipsScraper
from scrapers.dblp_scraper.dblp import DblpScraper
from scrapers.acm_scraper.acm import AcmScraper
from scrapers.nih_scraper.nih import NihScraper
from scrapers.nih_scraper.nih import NihData
from scrapers.entrez_scraper import *
from scrapers.nips_scraper.nips import NipsPaperInfo, NipsScraper




def get_last_execution_date(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            return pd.to_datetime(file.read().strip())
    return None

def update_last_execution_date(file_name, date):
    with open(file_name, 'w') as file:
        file.write(date.isoformat())

def main():
    faculty_file = r"C:\Users\prana\Downloads\combined_data.csv"
    data = pd.read_csv(faculty_file, delimiter=",", encoding="utf-8")
    d2 = data[0:1]
    author_list = [(row["Name"], row["Url"]) for _, row in d2.iterrows()]

    script_path = Path(__file__).resolve()
    base_dir = script_path.parent
    target_folder_path = os.path.join(base_dir, "pkl_files")
    os.makedirs(target_folder_path, exist_ok=True)

    last_execution_file = os.path.join(base_dir, 'last_execution_date.txt')
    last_execution_date = get_last_execution_date(last_execution_file)

    if last_execution_date is None:
        start_date = datetime.datetime(2020, 1, 1)
    else:
        start_date = last_execution_date + timedelta(days=1)

    end_date = datetime.datetime.now()

    scrapers = [ArxivScraper]
    for scraper in scrapers:
        scraper.get_papers(author_list, start_date, end_date, target_folder_path)

    all_papers = []
    for filename in os.listdir(target_folder_path):
        if filename.endswith('.pkl'):
            filepath = os.path.join(target_folder_path, filename)
            with open(filepath, 'rb') as file:
                papers = pickle.load(file)
                all_papers.extend(papers)

    papers_by_authors = {}
    for item in all_papers:
        if item.full_name not in papers_by_authors:
            papers_by_authors[item.full_name] = []
        papers_by_authors[item.full_name].append(item)

    df = pd.DataFrame([vars(item) for item in all_papers])

    output_file = os.path.join(base_dir, "papers.csv")
    if os.path.exists(output_file):
        existing_data = pd.read_csv(output_file)
        updated_data = pd.concat([existing_data, df]).drop_duplicates()
    else:
        updated_data = df

    updated_data.to_csv(output_file, index=False, encoding="utf-8")

    update_last_execution_date(last_execution_file, end_date)
    print(f"Data collected from {start_date.date()} to {end_date.date()}")

if __name__ == "__main__":
    main()