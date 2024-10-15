import pandas as pd
from datetime import datetime
import pickle
import os
from pathlib import Path
#from scrapers.icml_scraper.icml import IcmlPaperInfo
#from scrapers.icml_scraper.icml import IcmlScraper
from scrapers.core import AuthorInfo
from scrapers.core import *
from scrapers.nytimes_scraper.nytimes_main import NyTimesScraper
#from scrapers.nips_scraper.nips import NipsPaperInfo, NipsScraper

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

start_date = datetime.datetime(1950, 12, 29)
end_date = datetime.datetime(2024, 6, 13)

NyTimesScraper.get_papers(author_list, start_date, end_date,target_folder_path)


all_papers = []
for filename in os.listdir(target_folder_path):
    # if not filename.startswith("nih"):
    #     continue
    #if filename.endswith('.pkl'):
        filepath = os.path.join(target_folder_path, filename)
        with open(filepath, 'rb') as file:
            papers = pickle.load(file)
            all_papers.extend(papers)
    


papers_by_authors = {}
for item in all_papers:
    if item.full_name not in papers_by_authors:
        papers_by_authors[item.full_name] = []
    papers_by_authors[item.full_name].append(item)
    print(item)


output_file = os.path.join(base_dir, "nytpapers.csv")



# Create a DataFrame from the list of AuthorInfo objects
df = pd.DataFrame([vars(item) for item in all_papers])

df.to_csv("updated_pap.csv")

