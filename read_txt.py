import os
import re


def read_text_files_from_folder(folder_path):
    text_data = {}

    # Iterate through all files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text_data[filename] = file.read()

    return text_data


def split_text_into_chunks(text, separators):
    # Create a regex pattern from the list of separators
    regex_pattern = '|'.join(map(re.escape, separators))
    chunks = re.split(regex_pattern, text)
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def split_large_chunks(chunks, max_chunk_size):
    smaller_chunks = []
    for chunk in chunks:
        while len(chunk) > max_chunk_size:
            split_index = chunk[:max_chunk_size].rfind(' ')
            if split_index == -1:  # No space found, split at max_chunk_size
                split_index = max_chunk_size
            smaller_chunks.append(chunk[:split_index].strip())
            chunk = chunk[split_index:].strip()
        smaller_chunks.append(chunk)
    return smaller_chunks


def process_text_data(text_data, separators, max_chunk_size):
    processed_data = {}

    # Process each text file's content
    for filename, content in text_data.items():
        chunks = split_text_into_chunks(content, separators)
        smaller_chunks = split_large_chunks(chunks, max_chunk_size)
        processed_data[filename] = smaller_chunks

    return processed_data


# Specify the folder containing text files
folder_path = 'sm-faq'

# Define the separators and max chunk size
separators = ['\n\n\n', '\n\n']
max_chunk_size = 600

# Read and process text files
text_data = read_text_files_from_folder(folder_path)
processed_data = process_text_data(text_data, separators, max_chunk_size)

# Print processed data (or handle it as needed)
# for filename, chunks in processed_data.items():
#     print(f"Data from {filename}:")
#     for i, chunk in enumerate(chunks, 1):
#         print(f"Chunk {i}:\n{chunk}\n")
#     print("\n" + "=" * 50 + "\n")

# Further processing can be done as per your requirements
