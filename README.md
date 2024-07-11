
# Assist AI

A repository for learning LangChain by building a generative ai application.

This is a web application is using a Pinecone as a vectorsotre and answers questions about LangChain 
(sources from LangChain official documentation). 


## Tech Stack
Client: Streamlit

Server Side: LangChain 🦜🔗

Vectorstore: Pinecone 🌲

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`PINECONE_API_KEY`
`OPENAI_API_KEY`

## Run Locally

Clone the project

```bash
  git clone https://github.com/HariPrasanth/assist-ai.git
```

Go to the project directory

```bash
  cd assist-ai
```

Download LangChain Documentation
```bash
  mkdir docs
  wget -r -A.html -P docs  https://example.com
```

Install dependencies

```bash
  pipenv install
```

Start the flask server

```bash
  streamlit run main.py
```


## Running Tests

To run tests, run the following command

```bash
  pipenv run pytest .
```
