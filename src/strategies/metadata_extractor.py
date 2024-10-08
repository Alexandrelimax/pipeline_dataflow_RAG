from typing import Dict, Any


class MetadataExtractor:
    @staticmethod
    def extract_metadata(index: int, metadata: Dict[str, str]) -> Dict[str, Any]:
        return {
            'chunk_number': index,
            'file_name': metadata.get('file_name', ''),
            'mime_type': metadata.get('mime_type', ''),
            'gs_uri': metadata.get('gs_uri', '')
        }