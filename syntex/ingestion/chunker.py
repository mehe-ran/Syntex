try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter

from syntex.core.logger import logger

class DocChunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        # setup text splitter optimized for preserving code context
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            # prioritize splitting at paragraphs rather than mid-sentence
            separators=["\n\n", "\n", " ", ""]
        )

    def chunk_text(self, text: str) -> list[str]:
        # split the raw scraped text into semantic chunks for the vector db
        if not text:
            logger.warning("empty text provided to chunker")
            return []
            
        chunks = self.splitter.split_text(text)
        logger.info(f"split document into {len(chunks)} chunks")
        
        return chunks
