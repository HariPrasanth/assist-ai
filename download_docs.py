import os
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


# Function to create folder if it doesn't exist
def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


# Function to download a single page
def download_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        page_content = response.text  # Get the text content for ReadTheDocsLoader
        return page_content
    else:
        print(f"Failed to download {url}")
        return None


# Main function to download the website
def download_website(url):
    page_content = download_page(url)
    if page_content:
        print("Page content retrieved successfully.")
        return page_content
    else:
        print("No content to process.")
        return None


# Function to save HTML content to a file
def save_content_to_file(content, url, folder):
    parsed_url = urlparse(url)
    filename = os.path.join(folder, f"{parsed_url.netloc}_{parsed_url.path.strip('/').replace('/', '_')}.html")
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Saved content to {filename}")
    return filename


# Function to read HTML content from a file and convert it into a document
def convert_html_to_document(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    # Assuming ReadTheDocsLoader is a placeholder for actual document processing function
    # Here, we are using BeautifulSoup to parse the HTML content and extract text
    soup = BeautifulSoup(html_content, 'html.parser')
    document_text = soup.get_text()
    return document_text


# URL of the website to download
url = 'https://srimandir.com/?lang=en'
download_folder = 'downloaded_pages'

# Create folder if it doesn't exist
create_folder(download_folder)

# Get the page content
page_content = download_website(url)

# Save content to a file and convert to document
if page_content:
    file_path = save_content_to_file(page_content, url, download_folder)
    document = convert_html_to_document(file_path)
    print("Document content:")
    print(document)
