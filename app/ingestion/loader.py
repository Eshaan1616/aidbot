"""
Document loading and file management.
"""
import os
from typing import Dict
from pathlib import Path

class DocumentLoader:
    """Load and manage uploaded documents"""
    
    def __init__(self, upload_dir: str = "./uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)
    
    def load_text_file(self, file_path: str) -> Dict:
        """Load text file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                'filename': os.path.basename(file_path),
                'content': content,
                'size': len(content),
                'path': file_path
            }
        except Exception as e:
            raise Exception(f"Error loading {file_path}: {str(e)}")
    
    def save_upload(self, filename: str, content: bytes) -> str:
        """Save uploaded file"""
        file_path = self.upload_dir / filename
        with open(file_path, 'wb') as f:
            f.write(content)
        return str(file_path)