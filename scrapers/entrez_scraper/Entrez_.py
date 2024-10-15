import pandas as pd
import requests
from Bio import Entrez
from datetime import datetime
import time

# Define the Article class
class Article:
    def __init__(self, full_name: str, eai_url: str):
        self.full_name = full_name
        self.eai_url = eai_url
        self.link = ""
        self.pdf_link = ""
        self.publication_date = None
        self.data_source = ""
        self.publication = ""
        self.title = ""
        self.eai_match = False
        self.affiliation = ""
        self.type = ""
        self.citations = 0

# Define the PubMedScraper class
class PubMedScraper:
    @staticmethod
    def get_author_articles(full_name: str):
        Entrez.email = "example@example.com"  # Use a generic placeholder email
        search_handle = Entrez.esearch(db="pubmed", term=full_name, retmax=490)
        search_results = Entrez.read(search_handle)
        search_handle.close()

        article_ids = search_results.get("IdList", [])
        articles = []

        for article_id in article_ids:
            fetch_handle = Entrez.efetch(db="pubmed", id=article_id, retmode="xml")
            fetch_results = Entrez.read(fetch_handle)
            fetch_handle.close()

            if 'PubmedArticle' not in fetch_results:
                continue

            for article in fetch_results['PubmedArticle']:
                article_info = Article(full_name, "")
                article_info.data_source = "PubMed"

                # Get the title
                if 'MedlineCitation' in article and 'Article' in article['MedlineCitation'] and 'ArticleTitle' in article['MedlineCitation']['Article']:
                    article_info.title = article['MedlineCitation']['Article']['ArticleTitle']

                # Get the publication date
                pub_date = article['MedlineCitation']['Article']['Journal']['JournalIssue'].get('PubDate', {})
                if 'Year' in pub_date:
                    article_info.publication_date = datetime(int(pub_date['Year']), 1, 1)
                elif 'MedlineDate' in pub_date:
                    year = int(pub_date['MedlineDate'].split(" ")[0])
                    article_info.publication_date = datetime(year, 1, 1)

                # Get the journal name
                if 'Journal' in article['MedlineCitation']['Article'] and 'Title' in article['MedlineCitation']['Article']['Journal']:
                    article_info.publication = article['MedlineCitation']['Article']['Journal']['Title']

                # Get the link to the article
                article_info.link = f"https://pubmed.ncbi.nlm.nih.gov/{article_id}/"

                # Get the affiliation (first author)
                if 'AuthorList' in article['MedlineCitation']['Article'] and article['MedlineCitation']['Article']['AuthorList']:
                    author = article['MedlineCitation']['Article']['AuthorList'][0]
                    if 'AffiliationInfo' in author and author['AffiliationInfo']:
                        article_info.affiliation = author['AffiliationInfo'][0].get('Affiliation', '')

                articles.append(article_info)
                time.sleep(0.5)  # To avoid hitting the NCBI API rate limit

        return articles

    @staticmethod
    def get_papers_by_author_by_interval(full_name: str, eai_url: str, start_date: datetime, end_date: datetime):
        articles = PubMedScraper.get_author_articles(full_name)
        filtered_articles = []

        for article in articles:
            if article.publication_date and start_date <= article.publication_date <= end_date:
                article.eai_url = eai_url
                filtered_articles.append(article)

        return filtered_articles

    @staticmethod
    def get_papers(author_names_and_urls: pd.DataFrame, start_date: datetime, end_date: datetime, target_csv: str):
        papers = []
        for index, row in author_names_and_urls.iterrows():
            full_name = row['Name']
            eai_url = row['Url']

            # Check if the URL is null or empty, and skip if it is
            if pd.isnull(eai_url) or not eai_url.strip():
                print(f"Skipping {full_name} due to missing URL.")
                continue

            try:
                papers_by_author = PubMedScraper.get_papers_by_author_by_interval(full_name, eai_url, start_date, end_date)
                print(f"Processed {full_name}. Number of articles: {len(papers_by_author)}")
                papers.extend(papers_by_author)
                time.sleep(5)
            except Exception as e:
                print(f"Error processing {full_name}:")
                print(e)
                time.sleep(120)

        # Creating a DataFrame and writing to CSV
        papers_df = pd.DataFrame([{
            'Full Name': paper.full_name,
            'Eai_url': paper.eai_url,
            'Title': paper.title,
            'Publication': paper.publication,
            'Publication Date': paper.publication_date.strftime('%Y-%m-%d') if paper.publication_date else '',
            'Link': paper.link,
            'Affiliation': paper.affiliation
        } for paper in papers])

        papers_df.to_csv(target_csv, index=False, encoding='utf-8')