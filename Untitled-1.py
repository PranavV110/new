import pandas as pd
from datetime import datetime
import pickle
import os
from pathlib import Path
from scrapers.nih_scraper.nih import NihScraper
from scrapers.nih_scraper.nih import NihData

faculty_file = r"C:/Users/prana/Downloads/eai_faculty.csv"

data = pd.read_csv(faculty_file, delimiter=",", encoding="utf-8")
author_list = []
for index, row in data.iterrows():
    author_list.append((row["Name"], row["Url"]))

script_path = Path(__file__).resolve()
base_dir = script_path.parent.parent
target_folder_path = os.path.join(base_dir, "pkl_files")
if not os.path.exists(target_folder_path):
    os.makedirs(target_folder_path)

start_date = datetime(1900, 1, 1)
end_date = datetime(2023, 12, 31)

try:
    NihScraper.get_papers(author_list, start_date, end_date, target_folder_path)
except Exception as e:
    print("Error occurred while scraping papers:", e)

all_papers = []
for filename in os.listdir(target_folder_path):
    if filename.endswith('.pkl'):
        filepath = os.path.join(target_folder_path, filename)
        try:
            with open(filepath, 'rb') as file:
                papers = pickle.load(file)
                all_papers.extend(papers)
        except Exception as e:
            print("Error occurred while loading papers from file:", e)

papers_by_authors = {}
for item in all_papers:
    if item.full_name not in papers_by_authors:
        papers_by_authors[item.full_name] = []
    papers_by_authors[item.full_name].append(item)

output_file = os.path.join(base_dir, "papers.csv")
try:
    with open(output_file, 'w', encoding="utf-8") as out_file:
        out_file.write("FullName\tEaiUrl\tUrl\tPdfUrl\tPublicationDate\tDataSource\tPublication\tTitle\tEaiMatch\tAffiliation\tType\tCitations\n")
        for item in all_papers:
            out_file.write(item.to_string())
            out_file.write("\n")
except Exception as e:
    print("Error occurred while writing papers to file:", e)

print("Script execution completed.")
