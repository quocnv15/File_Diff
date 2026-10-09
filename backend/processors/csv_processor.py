"""
CSV processor for converting CSV files to Markdown
"""

import logging
import os
import time
import csv
from typing import Dict, Any, List, Optional
from pathlib import Path
import chardet

import pandas as pd

from processors.base_processor import BaseProcessor
from utils.exceptions import ProcessingFailedError, CorruptedFileError

logger = logging.getLogger(__name__)


class CSVProcessor(BaseProcessor):
    """CSV file processor using pandas"""

    def __init__(self):
        super().__init__()
        self.supported_extensions = ["csv"]
        self.supported_mime_types = ["text/csv", "application/csv"]

    async def process(self, file_path: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process CSV file and convert to Markdown

        Args:
            file_path: Path to the CSV file
            options: Processing options including:
                - extract_tables: bool (default: True)
                - extract_text: bool (default: True)
                - preserve_formatting: bool (default: True)
                - delimiter: str (auto-detect if not provided)
                - encoding: str (auto-detect if not provided)
                - header_row: int (0 if first row is header)

        Returns:
            Dictionary with markdown content and structured data
        """
        try:
            start_time = time.time()
            options = options or {}

            logger.info(f"Processing CSV file: {file_path}")

            # Validate file
            if not self.validate_file(file_path):
                raise CorruptedFileError(f"Invalid CSV file: {file_path}")

            # Detect encoding and delimiter
            encoding = await self._detect_encoding(file_path)
            delimiter = await self._detect_delimiter(file_path, encoding)

            # Extract data from CSV
            csv_data = await self._extract_csv_data(file_path, encoding, delimiter, options)

            # Convert to Markdown
            markdown_content = self._convert_to_markdown(csv_data, options)

            # Create structured data
            structured_data = self._create_structured_data(csv_data)

            # Extract metadata
            metadata = self._extract_metadata(file_path)
            metadata.update({
                "processing_time": time.time() - start_time,
                "encoding_detected": encoding,
                "delimiter_detected": delimiter,
                "total_rows": csv_data.get("rows", 0),
                "total_columns": csv_data.get("columns", 0),
                "options_used": options
            })

            logger.info(f"CSV processing completed for {file_path}")

            return {
                "markdown_content": markdown_content,
                "structured_data": structured_data,
                "metadata": metadata
            }

        except Exception as e:
            logger.error(f"CSV processing failed for {file_path}: {e}", exc_info=True)
            raise ProcessingFailedError(f"Failed to process CSV: {str(e)}", "csv_conversion")

    def validate_file(self, file_path: str) -> bool:
        """Validate CSV file"""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return False

            # Check file extension
            if not file_path.lower().endswith('.csv'):
                return False

            # Check if file is readable
            with open(file_path, 'rb') as f:
                header = f.read(1024)  # Read first 1KB
                if not header:
                    return False

            return True

        except Exception as e:
            logger.error(f"CSV validation failed for {file_path}: {e}")
            return False

    async def _detect_encoding(self, file_path: str) -> str:
        """Detect file encoding"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # Read first 10KB
                result = chardet.detect(raw_data)
                encoding = result.get('encoding', 'utf-8')
                confidence = result.get('confidence', 0)

                logger.info(f"Detected encoding: {encoding} (confidence: {confidence})")

                # If confidence is low, try common encodings
                if confidence < 0.7:
                    for test_encoding in ['utf-8', 'latin1', 'cp1252']:
                        try:
                            with open(file_path, 'r', encoding=test_encoding) as f:
                                f.read(1024)  # Test read
                            logger.info(f"Using fallback encoding: {test_encoding}")
                            return test_encoding
                        except UnicodeDecodeError:
                            continue

                return encoding

        except Exception as e:
            logger.error(f"Failed to detect encoding: {e}")
            return 'utf-8'  # Default fallback

    async def _detect_delimiter(self, file_path: str, encoding: str) -> str:
        """Detect CSV delimiter"""
        try:
            # Try pandas auto-detection first
            try:
                sample_df = pd.read_csv(file_path, nrows=5, encoding=encoding)
                if len(sample_df.columns) > 1:
                    logger.info(f"Auto-detected delimiter using pandas")
                    return ','  # Pandas typically handles this automatically
            except:
                pass

            # Manual delimiter detection
            with open(file_path, 'r', encoding=encoding) as f:
                first_line = f.readline()

            # Common delimiters to test
            delimiters = [',', ';', '\t', '|']
            delimiter_counts = {}

            for delimiter in delimiters:
                count = first_line.count(delimiter)
                if count > 0:
                    delimiter_counts[delimiter] = count

            if delimiter_counts:
                best_delimiter = max(delimiter_counts, key=delimiter_counts.get)
                logger.info(f"Detected delimiter: '{best_delimiter}'")
                return best_delimiter

            # Default to comma if no delimiter found
            logger.info("No clear delimiter found, defaulting to comma")
            return ','

        except Exception as e:
            logger.error(f"Failed to detect delimiter: {e}")
            return ','  # Default fallback

    async def _extract_csv_data(self, file_path: str, encoding: str, delimiter: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Extract data from CSV file"""
        try:
            # Read CSV options
            header_row = options.get("header_row", 0)
            include_empty = options.get("include_empty_rows", False)

            # Read CSV with pandas
            df = pd.read_csv(
                file_path,
                encoding=encoding,
                delimiter=delimiter,
                header=header_row if header_row is not None else 'infer',
                skipinitialspace=True,
                dtype=str,  # Keep all data as strings initially
                na_filter=False,  # Don't convert empty strings to NaN
                keep_default_na=False
            )

            # Clean DataFrame
            df = self._clean_dataframe(df, include_empty)

            # Convert to list of lists
            data = []
            if hasattr(df, 'columns'):
                data.append(df.columns.tolist())  # Headers
                for _, row in df.iterrows():
                    data.append([self._format_cell_value(cell) for cell in row])

            return {
                "file_name": Path(file_path).stem,
                "data": data,
                "rows": len(df),
                "columns": len(df.columns) if hasattr(df, 'columns') else 0,
                "dataframe": df,
                "encoding": encoding,
                "delimiter": delimiter
            }

        except Exception as e:
            logger.error(f"Failed to extract CSV data: {e}")
            raise

    def _clean_dataframe(self, df: pd.DataFrame, include_empty: bool = False) -> pd.DataFrame:
        """Clean and prepare DataFrame"""
        try:
            # Remove completely empty rows and columns if not including empty
            if not include_empty:
                # Remove rows that are completely empty
                df = df[~df.apply(lambda row: row.astype(str).str.strip().eq('').all(), axis=1)]

                # Remove columns that are completely empty
                df = df.loc[:, ~df.apply(lambda col: col.astype(str).str.strip().eq('').all())]

            # Reset index
            df = df.reset_index(drop=True)

            return df

        except Exception as e:
            logger.error(f"Failed to clean DataFrame: {e}")
            return df

    def _format_cell_value(self, value: Any) -> str:
        """Format cell value for display"""
        try:
            if pd.isna(value) or value == '' or value == 'nan':
                return ''
            elif isinstance(value, str):
                return value.strip()
            else:
                return str(value).strip()

        except Exception:
            return str(value) if value is not None else ''

    def _convert_to_markdown(self, csv_data: Dict[str, Any], options: Dict[str, Any]) -> str:
        """Convert CSV data to Markdown"""
        try:
            markdown_parts = []

            # Add title
            file_name = csv_data.get("file_name", "CSV Document")
            markdown_parts.append(f"# {file_name}")
            markdown_parts.append("")

            # Add file info
            encoding = csv_data.get("encoding", "unknown")
            delimiter = csv_data.get("delimiter", ",")
            markdown_parts.append(f"**Encoding:** {encoding}, **Delimiter:** '{delimiter}'")
            markdown_parts.append("")

            # Create table if data exists
            if csv_data.get("data") and len(csv_data["data"]) > 0:
                data = csv_data["data"]
                headers = data[0]
                rows = data[1:]

                # Create table
                table_markdown = self._create_markdown_table(headers, rows)
                markdown_parts.append(table_markdown)
                markdown_parts.append("")

                # Add statistics
                row_count = len(rows)
                col_count = len(headers)
                markdown_parts.append(f"*Rows: {row_count}, Columns: {col_count}*")
                markdown_parts.append("")

            if not markdown_parts[-1]:  # Remove trailing empty line
                markdown_parts.pop()

            return "\n".join(markdown_parts)

        except Exception as e:
            logger.error(f"Failed to convert to Markdown: {e}")
            return f"# {csv_data.get('file_name', 'CSV Document')}\n\nError converting to Markdown: {str(e)}"

    def _create_structured_data(self, csv_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create structured data from CSV data"""
        structured_data = []

        try:
            if csv_data.get("data") and len(csv_data["data"]) > 1:  # Has headers and at least one row
                data = csv_data["data"]
                table_data = {
                    "type": "table",
                    "headers": data[0],
                    "rows": data[1:],
                    "row_count": len(data) - 1,
                    "column_count": len(data[0]),
                    "encoding": csv_data.get("encoding"),
                    "delimiter": csv_data.get("delimiter")
                }
                structured_data.append(table_data)

        except Exception as e:
            logger.error(f"Failed to create structured data: {e}")

        return structured_data

    def _extract_csv_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract CSV-specific metadata"""
        try:
            metadata = {}
            stat = os.stat(file_path)

            metadata.update({
                "file_format": "csv",
                "file_size": stat.st_size,
                "line_ending": self._detect_line_ending(file_path)
            })

            return metadata

        except Exception as e:
            logger.error(f"Failed to extract CSV metadata: {e}")
            return {}

    def _detect_line_ending(self, file_path: str) -> str:
        """Detect line ending format"""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)

                if b'\r\n' in chunk:
                    return 'CRLF (Windows)'
                elif b'\r' in chunk:
                    return 'CR (Classic Mac)'
                elif b'\n' in chunk:
                    return 'LF (Unix/Linux)'
                else:
                    return 'Unknown'

        except Exception as e:
            logger.error(f"Failed to detect line ending: {e}")
            return 'Unknown'