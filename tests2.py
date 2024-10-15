import pandas as pd
import requests
import cv2
from pdf2image import convert_from_bytes
import pytesseract
import re
import time
import random


import pandas as pd
from datetime import datetime
import pickle
import os
import re
from pathlib import Path
import requests
import cv2
import pdf2image
from pdf2image import convert_from_bytes
import pytesseract
import re
import pandas as pd
import numpy as np

# Create a DataFrame from the list of AuthorInfo objects
df = pd.read_csv("C:/Users/prana/Downloads/papers.csv")
# Function to download PDF from URL
def download_pdf_from_url(pdf_url):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to download PDF from {pdf_url}")
        return None

# Function to extract document layout
def extract_layout(image):
    # Convert the image to grayscale
    pdf_content = download_pdf_from_url(url)

    images = convert_from_bytes(pdf_content)

    # Process only the first page (first image)
    first_page_image = np.array(images[0])

    # Resize the image to make it bigger
    resized_image = cv2.resize(first_page_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Perform edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original image
    layout = image.copy()
    cv2.drawContours(layout, contours, -1, (0, 255, 0), 2)

    return layout

# Function to perform OCR on document
def perform_ocr(image):
    # Perform OCR using Tesseract
    ocr_text = pytesseract.image_to_string(image)
    return ocr_text

# ArXiv PDF URL
def url_to_layout(url):
    
    # Download PDF from ArXiv URL
    pdf_content = download_pdf_from_url(url)

    # Convert PDF to images
    images = convert_from_bytes(pdf_content)

    # Process only the first page (first image)
    first_page_image = np.array(images[0])

    # Resize the image to make it bigger
    resized_image = cv2.resize(first_page_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Extract layout from the resized image
    layout_image = extract_layout(resized_image)

    # Perform OCR on the resized image
    ocr_text = perform_ocr(layout_image)
    
    #print(ocr_text)
    return  ocr_text

# Display the layout image


# Print OCR text for the first page
#print("OCR Text - First Page:")
#print(ocr_text)




#def perform_query(text, query):
    # Compile the regular expression pattern for the query
 #   pattern = re.compile(query, re.IGNORECASE)

    # Search for the pattern in the text
  #  matches = pattern.finditer(text)

    # Store the results
   # results = []

    # Iterate over the matches
   # for match in matches:
        # Get the start index of the match
    #    match_start = match.start()

     #   # Get the next two strings after the match index
      #  next_strings = text[match_start:].split(maxsplit=4)[1:4]

        # Append the match and next two strings to the results
       # results.append((match.group(), *next_strings))

    # Return the results
    #return results



def perform_query(text, query):
    # Compile the regular expression pattern for the query
    pattern = re.compile(query, re.IGNORECASE, re.MULTILINE)

    # Search for the pattern in the text
    matches = pattern.finditer(text)

    # Store the results
    results = []

    # Iterate over the matches
    for match in matches:
        # Get the start index and end index of the line containing the match
        match_start = match.start()
        match_end = match.end()

        # Find the start and end index of the line containing the match
        line_start = text.rfind('\n', 0, match_start) + 1
        line_end = text.find('\n', match_end)

        # Extract the entire line containing the match
        line_containing_match = text[line_start:line_end]

        # Append the entire line to the results
        results.append(line_containing_match)

    # Return the results
    return results


import re

def perform_query2(text, queries):
    # Initialize results dictionary to store results for each query
    #results = {}
    results2 = {}

    # Iterate over each query
    for query_name, query_pattern in queries.items():
        # Compile the regular expression pattern for the query
        pattern = re.compile(query_pattern, re.MULTILINE, re.IGNORECASE)

        # Search for the pattern in the text
        matches = pattern.finditer(text)

        # Store the matches for the current query
        query_results = []

        for match in matches:
            # Get the start index of the line containing the match
            line_start = text.rfind('\n', 0, match.start()) + 1 if '\n' in text[:match.start()] else 0

            # Get the end index of the line containing the match
            line_end = text.find('\n', match.end())
            line_end = len(text) if line_end == -1 else line_end

            # Extract the entire line containing the match
            line_containing_match = text[line_start:line_end]

            # Append the line containing the match to the results
            query_results.append(line_containing_match)

        # Store the results for the current query in the dictionary
        results2[query_name] = query_results
        #print(results2)
    
        # Iterate over the matches
        #for match in matches:
            # Get the start index of the match
         #   match_start = match.start()

            # Get the next two strings after the match index
          #  next_strings = text[match_start:].split()[1:]
           # previous_strings = text[max(0, match_start - 2):match_start]


            # Append the match and next two strings to the results
            #query_results.append((match.group(), *next_strings))
            #query_results.append((match.group(),*previous_strings))

        # Store the results for the current query in the dictionary
        results2[query_name] = query_results

    # Return the results dictionary
    return results2
    




import time
import random
# Define the output file path
#output_file = os.path.join(base_dir, "papers.csv")
#df.to_csv(output_file, index=False, encoding="utf-8")


# Create a DataFrame from the list of AuthorInfo objects
df = pd.read_csv("C:/Users/prana/Downloads/papers.csv")
#df = df[pd.notna(df['pdf_link'])][0:5]


# Function to download PDF from URL
def download_pdf_from_url(pdf_url):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to download PDF from {pdf_url}")
        return None

# Function to extract document layout
def extract_layout(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Perform edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original image
    layout = image.copy()
    cv2.drawContours(layout, contours, -1, (0, 255, 0), 2)

    return layout

# Function to perform OCR on document
def perform_ocr(image):
    # Perform OCR using Tesseract
    ocr_text = pytesseract.image_to_string(image)
    return ocr_text

# ArXiv PDF URL
def url_to_layout(url):
    # Download PDF from ArXiv URL
    pdf_content = download_pdf_from_url(url)

    # Convert PDF to images
    images = convert_from_bytes(pdf_content)

    # Process only the first page (first image)
    first_page_image = images[0]

    # Extract layout from the resized image
    layout_image = extract_layout(first_page_image)

    # Perform OCR on the resized image
    ocr_text = perform_ocr(first_page_image)
    
    #print(ocr_text)
    return  ocr_text

# Define a function to check if "Northeastern" is present in the OCR text
def check_northeastern_presence(ocr_text):
    return "Northeastern" in ocr_text

# Apply the function to create the new column "mtc"
df['mtc'] = False
for index, row in df.head(10).iterrows():
    url = row['pdf_link']
    if pd.notna(url):
        print(url)
        try:
            ocr_text = url_to_layout(url)
            print(ocr_text)
    
            results = perform_query(ocr_text, row['full_name'].split(" ")[0])
            print(results)
            r1 = perform_query(ocr_text, row['full_name'])
            print(r1)
            r2 = perform_query(ocr_text, "Northeastern")
            print(r2)
                
            if not r2:  # Check if r2 is an empty list
                    mtc = False
            else:
                    mtc = True
                #texts.append([results, r1, r2])
            df.at[index, 'mtc'] = mtc
                # Check if the URL exists in the dataframe before updating
            print("Iteration complete.")
            time.sleep(random.randint(1, 5))
             
        except Exception as e:
            time.sleep(random.randint(1, 5))
            continue

# Save the updated DataFrame to a CSV file
df.to_csv("updated_papers.csv", index=False)
