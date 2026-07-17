import chromadb
from langchain_openai import OpenAIEmbeddings
from syntex.core.config import settings
from syntex.core.logger import logger

class VectorStore:
    def __init__(self, collection_name: str = "syntex_docs"):
        # initialize chromadb client with local storage path
        self.client = chromadb.PersistentClient(path=settings.chroma_db_dir)
        
        # setup openai embeddings
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.openai_api_key,
            model="text-embedding-3-small"
        )
        
        # retrieve existing collection or create a new one
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_chunks(self, chunks: list[str], source_url: str):
        # validate input before processing
        if not chunks:
            logger.warning("no chunks provided to add to vector store")
            return

        # generate unique identifiers for each chunk based on the source
        ids = [f"{source_url}_chunk_{i}" for i in range(len(chunks))]
        
        # attach source metadata to allow for targeted filtering later
        metadatas = [{"source": source_url} for _ in chunks]

        try:
            logger.info(f"generating embeddings for {len(chunks)} chunks")
            # generate vector embeddings
            embeddings = self.embeddings.embed_documents(chunks)
            
            # insert data into chromadb
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadatas
            )
            logger.info("successfully stored chunks in vector database")
            
        except Exception as e:
            logger.error(f"failed to store chunks: {e}")

    def search(self, query: str, n_results: int = 4) -> list[dict]:
        # query the database for chunks semantically similar to the user prompt
        try:
            logger.debug(f"searching vector store for: {query}")
            # embed the search query
            query_embedding = self.embeddings.embed_query(query)
            
            # execute the semantic search
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            # extract and format the retrieved data
            documents = results.get("documents", [[]])[0]
            metadatas = results.get("metadatas", [[]])[0]
            
            # return a clean list of dictionaries for the agent to read
            return [
                {"content": doc, "metadata": meta}
                for doc, meta in zip(documents, metadatas)
            ]
            
        except Exception as e:
            logger.error(f"vector search encountered an error: {e}")
            return []
