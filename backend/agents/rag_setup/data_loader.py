from langchain_core.documents import Document
from pathlib import Path
from typing import List
from langchain_community.document_loaders import PyMuPDFLoader,TextLoader,CSVLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.document_loaders import JSONLoader

# Supports loading PDF, TXT, CSV, DOCX, XLSX, and JSON files
class DataLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.loader = self._get_loader()

    def _get_loader(self):
        ext = Path(self.file_path).suffix.lower()
        if ext == ".pdf":
            return PyMuPDFLoader(self.file_path)
        elif ext == ".txt":
            return TextLoader(self.file_path)
        elif ext == ".csv":
            return CSVLoader(self.file_path)
        elif ext == ".docx":
            return Docx2txtLoader(self.file_path)
        elif ext in [".xls", ".xlsx"]:
            return UnstructuredExcelLoader(self.file_path)
        elif ext == ".json":
            return JSONLoader(self.file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def load_data(self) -> List[Document]:
        return self.loader.load()
