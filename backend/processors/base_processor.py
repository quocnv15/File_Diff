"""
Abstract base processor for file conversion
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging

from utils.logger import get_process_logger

logger = logging.getLogger(__name__)


class BaseProcessor(ABC):
    """Abstract base class for file processors"""

    def __init__(self):
        self.supported_extensions: List[str] = []
        self.supported_mime_types: List[str] = []
        self.process_logger = get_process_logger(f"{__name__}.{self.__class__.__name__}")

    @abstractmethod
    async def process(self, file_path: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process file and return structured data

        Args:
            file_path: Path to the file to process
            options: Processing options

        Returns:
            Dictionary containing:
            - markdown_content: Converted markdown content
            - structured_data: Parsed structured data
            - metadata: Processing metadata
        """
        pass

    @abstractmethod
    def validate_file(self, file_path: str) -> bool:
        """
        Validate if file can be processed by this processor

        Args:
            file_path: Path to the file to validate

        Returns:
            True if file can be processed, False otherwise
        """
        pass

    def get_processor_info(self) -> Dict[str, Any]:
        """Get processor information"""
        return {
            "name": self.__class__.__name__,
            "supported_extensions": self.supported_extensions,
            "supported_mime_types": self.supported_mime_types
        }

    def _create_markdown_table(self, headers: List[str], rows: List[List[str]]) -> str:
        """Create markdown table from headers and rows"""
        if not headers or not rows:
            return ""

        # Calculate column widths
        col_widths = [len(str(header)) for header in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(str(cell)))

        # Create table
        markdown = []

        # Header row
        header_row = "| " + " | ".join(
            str(header).ljust(col_widths[i]) for i, header in enumerate(headers)
        ) + " |"
        markdown.append(header_row)

        # Separator row
        separator_row = "| " + " | ".join(
            "-" * col_widths[i] for i in range(len(headers))
        ) + " |"
        markdown.append(separator_row)

        # Data rows
        for row in rows:
            data_row = "| " + " | ".join(
                str(cell).ljust(col_widths[i]) if i < len(row) else "".ljust(col_widths[i])
                for i in range(len(headers))
            ) + " |"
            markdown.append(data_row)

        return "\n".join(markdown)

    def _extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract basic metadata from file"""
        import os
        from datetime import datetime

        process_id = self.process_logger.start_process(
            "metadata_extraction",
            file_path=file_path,
            processor=self.__class__.__name__
        )
        
        try:
            self.process_logger.log_step("reading_file_stats")
            
            stat = os.stat(file_path)
            metadata = {
                "file_size": stat.st_size,
                "created_time": datetime.fromtimestamp(stat.st_ctime),
                "modified_time": datetime.fromtimestamp(stat.st_mtime),
                "processor": self.__class__.__name__
            }
            
            self.process_logger.log_step(
                "metadata_extracted",
                file_size=stat.st_size,
                created_time=metadata["created_time"].isoformat(),
                modified_time=metadata["modified_time"].isoformat()
            )
            
            self.process_logger.end_process(process_id, metadata_keys=list(metadata.keys()))
            return metadata
            
        except Exception as e:
            self.process_logger.log_error(e, file_path=file_path)
            logger.error(f"Failed to extract metadata from {file_path}: {e}")
            return {"processor": self.__class__.__name__}