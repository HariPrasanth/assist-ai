from dotenv import load_dotenv

from read_html import read_html_files, extract_text_from_html, split_text
from read_txt import read_text_files_from_folder, process_text_data, split_text_into_chunks

load_dotenv()

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from consts import INDEX_NAME

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


def ingest_docs():
    directory = 'sm-temple-docs'  # Specify your directory path here
    html_contents = read_html_files(directory)
    print(f"loaded {len(html_contents)} documents")

    separators = ['\n\n', '\n', '.', ',']
    chunk_size = 600  # You can adjust the chunk size as needed

    count = 0
    for html_content in html_contents:
        text = extract_text_from_html(html_content)
        split_texts = split_text(text, separators, chunk_size)

        count += 1
        print(f"Going to add {len(split_texts)} to Pinecone : {count} {split_texts}")
        # PineconeVectorStore.from_texts(split_texts, embeddings, index_name=INDEX_NAME)
        print("****Loading to vectorstore done ***")


def ingest_text_file():
    separators = ['\n\n\n', '\n\n']
    chunk_size = 600  # You can adjust the chunk size as needed
    directory = 'sm-faq'  # Specify your directory path here
    text_data = read_text_files_from_folder(directory)
    processed_text_data = process_text_data(text_data, separators, chunk_size)
    print(f"loaded {len(processed_text_data)} documents")

    count = 0
    for text in processed_text_data["faq.txt"]:
        count += 1
        print(f"Going to add {len(text)} to Pinecone : {count} {text}")
        # PineconeVectorStore.from_texts(text, embeddings, index_name=INDEX_NAME)
        print("****Loading to vectorstore done ***")


if __name__ == "__main__":
    ingest_docs()
    # ingest_text_file()
