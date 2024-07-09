from dotenv import load_dotenv

from read_html import read_html_files, extract_text_from_html, split_text

load_dotenv()

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from consts import INDEX_NAME

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


def ingest_docs():
    directory = 'sm-docs'  # Specify your directory path here
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
        PineconeVectorStore.from_texts(split_texts, embeddings, index_name=INDEX_NAME)
        print("****Loading to vectorstore done ***")


if __name__ == "__main__":
    ingest_docs()
