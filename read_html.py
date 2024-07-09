import os
from bs4 import BeautifulSoup
import re


# Function to read HTML files from a directory
def read_html_files(directory):
    html_contents = []
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                html_contents.append(file.read())
    return html_contents


# Function to extract text from HTML content using BeautifulSoup
def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()


# Function to split text into chunks of a specified size with multiple separators
def split_text(text, separators, chunk_size):
    # Combine the separators into a single regex pattern
    pattern = '|'.join(map(re.escape, separators))

    chunks = []
    current_chunk = []
    current_length = 0

    for line in re.split(pattern, text):
        if current_length + len(line) > chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = [line]
            current_length = len(line)
        else:
            current_chunk.append(line)
            current_length += len(line)

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


def main():
    directory = 'sm-docs'  # Specify your directory path here
    html_contents = read_html_files(directory)

    separators = ['\n\n', '\n', '.', ',']
    chunk_size = 600  # You can adjust the chunk size as needed

    for html_content in html_contents:
        text = extract_text_from_html(html_content)
        split_texts = split_text(text, separators, chunk_size)

        # Print or process split texts
        for i, chunk in enumerate(split_texts):
            print(f'Chunk {i + 1}:')
            print(chunk)
            print('-' * 40)


if __name__ == "__main__":
    main()
