import os
from syntex.ingestion.scraper import DocScraper
from syntex.ingestion.chunker import DocChunker
from syntex.ingestion.vector_store import VectorStore
from syntex.core.logger import logger

def test_pipeline():
    # initialize the pipeline components
    scraper = DocScraper()
    chunker = DocChunker(chunk_size=800, chunk_overlap=100)
    vector_store = VectorStore(collection_name="syntex_test")

    # use fastapi's documentation as a realistic test case
    test_url = "https://fastapi.tiangolo.com/features/"
    
    logger.info("--- starting ingestion pipeline test ---")
    
    # step 1: scrape the html
    raw_text = scraper.scrape_url(test_url)
    if not raw_text:
        logger.error("scraping failed. check network or url.")
        return

    # step 2: split text into semantic chunks
    chunks = chunker.chunk_text(raw_text)
    if not chunks:
        logger.error("chunking failed. no text to process.")
        return
        
    # step 3: embed and store in chromadb
    vector_store.add_chunks(chunks, source_url=test_url)
    
    # step 4: execute a semantic search
    test_query = "how fast is the framework?"
    logger.info(f"querying vector store for: '{test_query}'")
    
    results = vector_store.search(test_query, n_results=2)
    
    # display the retrieved chunks
    print("\n--- search results ---")
    for i, res in enumerate(results, 1):
        print(f"\n[result {i}] source: {res['metadata']['source']}")
        print(res["content"])
        print("-" * 40)

if __name__ == "__main__":
    test_pipeline()
