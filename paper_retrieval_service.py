import pandas as pd
from datetime import datetime
import pickle
import os
import re
from pathlib import Path
import requests
from scrapers.core import AuthorInfo
from scrapers.core import *
from scrapers.nytimes_scraper.nytimes_main import NyTimesScraper
from scrapers.semantic_scholar_scraper.semantic_scholar_scraper import SemanticScholarScraper
from scrapers.arxiv_scraper.arxiv import ArxivScraper
#from scrapers.icml_scraper.icml import IcmlScraper
from scrapers.kdd_scraper.kdd import KddScraper
from scrapers.nips_scraper.nips import NipsScraper
from scrapers.dblp_scraper.dblp import DblpScraper
from scrapers.acm_scraper.acm import AcmScraper
from scrapers.nih_scraper.nih import NihScraper
from scrapers.nih_scraper.nih import NihData
from scrapers.entrez_scraper import *
#from scrapers.entrez_scraper import pubmed
#from scrapers.entrez_scraper import entrez
#from scrapers.entrez_scraper.pubmed import get_pubmed_info
#from scrapers.entrez_scraper.pubmed import get_pubmed_info
from scrapers.nips_scraper.nips import NipsPaperInfo
from scrapers.nips_scraper.nips import NipsScraper
#from globals import Author




faculty_file = r"C:\Users\prana\Downloads\combined_data.csv"


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
end_date = datetime.datetime(2024, 8, 13)
NihScraper.get_papers(author_list, start_date, end_date, target_folder_path)
ArxivScraper.get_papers(author_list, start_date, end_date, target_folder_path)
AcmScraper.get_papers(author_list, start_date, end_date, target_folder_path)

SemanticScholarScraper.get_papers(author_list, start_date, end_date, target_folder_path)
#icml_data = IcmlScraper.get_papers_by_authors(200)
#IcmlScraper.get_papers_by_author(author_list,icml_data,start_date,end_date)
#IcmlScraper.get_papers(author_list, icml_data, start_date=start_date, end_date=end_date)
#IcmlScraper.get_papers(author_list, start_date, end_date, target_folder_path)
#IcmlScraper.get_papers(author_list, start_date, end_date, target_folder_path)
DblpScraper.get_papers(author_list, start_date, end_date, target_folder_path)
#PubMedScraper.get_papers(faculty_file, start_date, end_date, target_folder_path)


#KddScraper.get_papers_by_authors(start_date, end_date)

#NyTimesScraper.get_papers(author_list, start_date, end_date,target_folder_path)

all_papers = []
for filename in os.listdir(target_folder_path):
    # if not filename.startswith("nih"):
    #     continue
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
    print(item)


output_file = os.path.join(base_dir, "papers.csv")



# Create a DataFrame from the list of AuthorInfo objects
df = pd.DataFrame([vars(item) for item in all_papers])

df.to_csv("updated_pap.csv")

output_file = os.path.join(base_dir, "TEST_papers.csv")
df.to_csv(output_file, index=False, encoding="utf-8")

#import time
#import random

#texts = []
#t2 = []

#for url,name in zip(df['pdf_link'],df['full_name']):
 #   if url is None:
  #      continue
   # else:
    #    print(url,name.split(" ")[0],)
     #   try:
      #      layout_image, ocr_text = url_to_layout(url)
       #     print(ocr_text)
        #    if layout_image is not None:
        #        results = perform_query(ocr_text,name.split(" ")[0])
         #       print(results)
          #      texts.append(results)
           #     time.sleep(random.randint(1,5))
            #    queries2 = {
             #               "query1": name.split(" ")[0],
              #              "query2": name.split(" ")[1],
               #             "query3":name.split(" ")[2],
                #            "full_name_query": name,
                 #           "query4": "Northeastern",
                  #          "query5": ".edu",
                   #         "query6": "neu",
                    #        "query7": "ece"
                     #   }
#                results2 = perform_query2(ocr_text, queries2)
#                print(results2)
#                t2.append(results2)
#        except Exception as e:
#            time.sleep(random.randint(1,5))
#            continue

#print(t2)            
#df['matches'] = pd.Series(t2)
#df['matches2'] = pd.Series(t2)

#pd.DataFrame(t2).to_csv("queries.csv")



# Write DataFrame to CSV file
df.to_csv(output_file, index=False, encoding="utf-8")




# Convert list of dictionaries to DataFrame
#df_t2 = pd.DataFrame(t2)

# Reset the index of the main DataFrame if necessary
#df.reset_index(drop=True, inplace=True)

# Join the two DataFrames based on their indices
#merged_df = pd.concat([df, df_t2], axis=1)

# Save the merged DataFrame to a CSV file
#merged_df.to_csv("merged_data.csv", index=False)


#with open(output_file, 'w', encoding="utf-8") as out_file:
    # Write the header row
 #   out_file.write("FullName,EaiUrl,Url,PdfUrl,PublicationDate,DataSource,Publication,Title,EaiMatch,Affiliation,Type,Citations\n")
    
    # Write data rows
  #  for item in all_papers:
   #     csv_row = f"{item.full_name},{item.eai_url},{item.link},{item.pdf_link},{item.publication_date},{item.data_source},{item.publication},{item.title},{item.eai_match},{item.affiliation},{item.type},{item.venue}"
    #    out_file.write(csv_row + "\n")



#output_file = os.path.join(base_dir, "papers.csv")
#with open(output_file, 'w', encoding="utf-8") as out_file:
#    out_file.write("FullName\tEaiUrl\tUrl\tPdfUrl\tPublicationDate\tDataSource\tPublication\tTitle\tEaiMatch\tAffiliation\tType\tCitations\n")
#    for item in all_papers:
#        out_file.write(item.to_string())
#        out_file.write("\n")

#print(base_dir)


#ArxivScraper.test_get_papers_by_author()
#ArxivScraper.test_get_papers()