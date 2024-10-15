# -*- coding: utf-8 -*-
"""pdf_to_text_layout

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RE37d1SqUVV8sErP1Yis4a10h2vreOkU
"""

!pip install pytesseract
!apt-get install poppler-utils

!pip install pdf2image

!apt-get install tesseract-ocr

import numpy as np
import cv2
import requests
from io import BytesIO
import pytesseract
from pdf2image import convert_from_bytes
from google.colab.patches import cv2_imshow

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
arxiv_pdf_url = "https://arxiv.org/pdf/1906.03288v2.pdf"

# Download PDF from ArXiv URL
pdf_content = download_pdf_from_url(arxiv_pdf_url)

# Convert PDF to images
images = convert_from_bytes(pdf_content)

# Process only the first page (first image)
first_page_image = np.array(images[0])

# Resize the image to make it bigger
resized_image = cv2.resize(first_page_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

# Extract layout from the resized image
layout_image = extract_layout(resized_image)

# Perform OCR on the resized image
ocr_text = perform_ocr(resized_image)

# Display the layout image
cv2_imshow(layout_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Print OCR text for the first page
print("OCR Text - First Page:")
print(ocr_text)



