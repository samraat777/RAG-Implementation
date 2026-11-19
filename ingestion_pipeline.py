import os
from langchain_community.document_loaders import TextLoader,DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

def load_documents(docs_path="docs"):

    print(f"Loading documents from {docs_path}...")
    if not os.path.exists(docs_path):
            raise FileNotFoundError(f"The specified path {docs_path} does not exist. Please provide a valid path to the documents.")

        

    #loading the documents from the specified path using DirectoryLoader and TextLoader
    loader = DirectoryLoader(
        path=docs_path,
        glob="*.txt", 
        loader_cls=TextLoader
    )
        
    documents = loader.load()

    #checking if there is content in the document 
    if len(documents) == 0:
        raise File(f"No documents found in {docs_path}. Please ensure that the directory contains .txt files.")


    for i,doc in enumerate(documents):
        print(f"Document {i+1}: {doc.metadata['source']} - {len(doc.page_content)} characters")
        print(f"Content Preview: {doc.page_content[:100]}...")  # Print first 100 characters of the document content
        print(f"Metadata: {doc.metadata}")


    return documents

def split_documents(documents, chunk_size=800, chunk_overlap=0):
        """split the documents into smaller chunks for processing"""
        print(f"Splitting documents into chunks of size {chunk_size} with overlap {chunk_overlap}...")
        text_splitter = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        chunks = text_splitter.split_documents(documents)
        if chunks:
            for i, chunk in enumerate(chunks[:5]):  # Print only the first 5 chunks for brevity
                print(f"\n--- Chunk {i+1} ---")
                print(f"Source: {chunk.metadata['source']}")
                print(f"Length: {len(chunk.page_content)} characters") 
                print(chunk.page_content)  
                print("-"*50)

            if len(chunks) > 5:
                print(f"\n... and {len(chunks) - 5} more chunks")  # Print the number of additional chunks
        return chunks




def main():
    print("Starting ingestion pipeline...")
    documents = load_documents(docs_path="docs")
    chunks = split_documents(documents, chunk_size=800, chunk_overlap=0)




if __name__ == "__main__":
    main()