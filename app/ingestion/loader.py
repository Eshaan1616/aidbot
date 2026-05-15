"""
Document loading and file management.
"""
import os
from typing import Dict
from pathlib import Path

from app.config import get_upload_dir_path
from app.ingestion.extractors import ExtractorRegistry

class DocumentLoader:
    """Load and manage uploaded documents"""
    
    def __init__(self, upload_dir: str | None = None):
        self.upload_dir = Path(upload_dir or get_upload_dir_path())
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.registry = ExtractorRegistry()

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        return self.registry.supported_extensions
    
    def load_file(self, file_path: str) -> Dict:
        """Load supported file content into a common ingestion contract."""
        path = Path(file_path)
        content = self.registry.extract(path)
        
        return {
            'filename': os.path.basename(file_path),
            'content': content,
            'size': len(content),
            'path': file_path,
            'file_type': path.suffix.lower().lstrip("."),
        }
    
    def save_upload(self, filename: str, content: bytes) -> str:
        """Save uploaded file"""
        file_path = self.upload_dir / filename
        with open(file_path, 'wb') as f:
            f.write(content)
        return str(file_path)

    def clear_uploads(self):
        """Remove uploaded files from the workspace upload directory."""
        for file_path in self.upload_dir.iterdir():
            if file_path.is_file():
                file_path.unlink()

    def delete_upload(self, filename: str) -> bool:
        file_path = self.upload_dir / Path(filename).name
        if not file_path.exists() or not file_path.is_file():
            return False
        file_path.unlink()
        return True
