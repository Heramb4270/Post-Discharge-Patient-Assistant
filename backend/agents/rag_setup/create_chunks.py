# from langchain_text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
class ChunkCreator:
    def __init__(self, chunk_size: int = 10000, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        return 

    def create_chunks(self, documents: List[Document]) -> List[Document]:
        all_chunks = []
        for doc in documents:
            chunks = self.text_splitter.split_text(doc.page_content)
            for i, chunk in enumerate(chunks):
                chunk_metadata = dict(doc.metadata)
                chunk_metadata.update({"chunk_index": i})
                all_chunks.append(Document(page_content=chunk, metadata=chunk_metadata))
        return all_chunks
