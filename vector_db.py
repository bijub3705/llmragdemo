import chromadb
import os
from pathlib import Path 
from chromadb.utils import embedding_functions
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import CharacterTextSplitter

chroma_client = chromadb.Client()
default_ef = embedding_functions.DefaultEmbeddingFunction()
collection = chroma_client.create_collection(name="my_collection", embedding_function=default_ef)

def load_data() -> None:
    doc_folder_path = "documents"
    root_path = Path(doc_folder_path)
    documents = []
    for file in os.listdir(root_path):
        doc_path = doc_folder_path+"/"+file
        if file.endswith(".pdf"):
            loader=PyPDFLoader(doc_path)
        elif file.endswith(".txt"):
            loader=TextLoader(doc_path)
        elif file.endswith(".docx") or file.endswith(".doc"):
            loader=Docx2txtLoader(doc_path)
        documents.extend(loader.load())
    if len(documents) > 0:
        #print(len(documents))
        load_chunk_persist_data(documents)     


def load_chunk_persist_data(documents) -> None:          
    document_splitter = CharacterTextSplitter(chunk_size=25, chunk_overlap=10)
    document_chunks = document_splitter.split_documents(documents)
    #print(len(document_chunks))
    for count, chunk in enumerate(document_chunks):
        #print(chunk)
        collection.add(
            documents=chunk.page_content,
            metadatas=[{"source": chunk.metadata['source']}],
            ids=[chunk.metadata['source']+ str(count)]
         )
    
def get_chunk_data(queries):
    results = collection.query(
        query_texts=queries,
        n_results=1
    )
    return results['documents']

if __name__ == "__main__":
  load_data()
  print(get_chunk_data(["What does a Coverage Example show? "]))