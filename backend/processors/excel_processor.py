"""
Excel processor for converting Excel files to Markdown
"""

import logging
import os
import time
from typing import Dict, Any, List, Optional, Union
from pathlib import Path

import pandas as pd
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows

from processors.base_processor import BaseProcessor
from utils.exceptions import ProcessingFailedError, CorruptedFileError

logger = logging.getLogger(__name__)


class ExcelProcessor(BaseProcessor):
    """Excel file processor using pandas and openpyxl"""

    def __init__(self):
        super().__init__()
        self.supported_extensions = ["xlsx", "xls"]
        self.supported_mime_types = [
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-excel"
        ]

    async def process(self, file_path: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process Excel file and convert to Markdown

        Args:
            file_path: Path to the Excel file
            options: Processing options including:
                - extract_tables: bool (default: True)
                - extract_text: bool (default: True)
                - preserve_formatting: bool (default: True)
                - sheet_name: str or int (default: first sheet)
                - include_empty_rows: bool (default: False)

        Returns:
            Dictionary with markdown content and structured data
        """
        try:
            start_time = time.time()
            options = options or {}

            logger.info(f"Processing Excel file: {file_path}")

            # Validate file
            if not self.validate_file(file_path):
                raise CorruptedFileError(f"Invalid Excel file: {file_path}")

            # Extract data from Excel
            excel_data = await self._extract_excel_data(file_path, options)

            # Convert to Markdown
            markdown_content = self._convert_to_markdown(excel_data, options)

            # Create structured data
            structured_data = self._create_structured_data(excel_data)

            # Extract metadata
            metadata = self._extract_metadata(file_path)
            metadata.update({
                "processing_time": time.time() - start_time,
                "sheets_processed": len(excel_data.get("sheets", {})),
                "total_tables": len(structured_data),
                "options_used": options
            })

            logger.info(f"Excel processing completed for {file_path}")

            return {
                "markdown_content": markdown_content,
                "structured_data": structured_data,
                "metadata": metadata
            }

        except Exception as e:
            logger.error(f"Excel processing failed for {file_path}: {e}", exc_info=True)
            raise ProcessingFailedError(f"Failed to process Excel: {str(e)}", "excel_conversion")

    def validate_file(self, file_path: str) -> bool:
        """Validate Excel file"""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                logger.error(f"File does not exist: {file_path}")
                return False

            # Check file extension
            file_ext = Path(file_path).suffix.lower().lstrip('.')
            if file_ext not in self.supported_extensions:
                logger.error(f"Unsupported file extension: {file_ext}")
                return False

            # Try to open with openpyxl to validate
            if file_ext == 'xlsx':
                try:
                    wb = openpyxl.load_workbook(file_path, read_only=True)
                    wb.close()
                    return True
                except Exception:
                    # Fallback to pandas validation
                    try:
                        pd.read_excel(file_path, nrows=1)
                        return True
                    except Exception:
                        return False

            # Try to open with pandas for .xls files
            elif file_ext == 'xls':
                try:
                    pd.read_excel(file_path, nrows=1)
                    return True
                except Exception:
                    return False

            return False

        except Exception as e:
            logger.error(f"Excel validation failed for {file_path}: {e}")
            return False

    async def _extract_excel_data(self, file_path: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Extract data from Excel file"""
        try:
            excel_data = {
                "file_name": Path(file_path).stem,
                "sheets": {},
                "workbook_info": {}
            }

            # Get workbook information
            excel_data["workbook_info"] = await self._get_workbook_info(file_path)

            # Determine which sheets to process
            sheet_name = options.get("sheet_name")
            if sheet_name:
                # Process specific sheet
                sheet_data = await self._process_sheet(file_path, sheet_name, options)
                excel_data["sheets"][sheet_name] = sheet_data
            else:
                # Process all sheets
                all_sheets = self._get_sheet_names(file_path)
                for sheet in all_sheets:
                    sheet_data = await self._process_sheet(file_path, sheet, options)
                    excel_data["sheets"][sheet] = sheet_data

            return excel_data

        except Exception as e:
            logger.error(f"Failed to extract Excel data: {e}")
            raise

    async def _get_workbook_info(self, file_path: str) -> Dict[str, Any]:
        """Get workbook information"""
        try:
            if file_path.endswith('.xlsx'):
                # Use openpyxl for .xlsx files
                wb = openpyxl.load_workbook(file_path, read_only=True)
                info = {
                    "file_format": "xlsx",
                    "sheet_names": wb.sheetnames,
                    "active_sheet": wb.active.title if wb.active else None,
                    "calculation": wb.calculation.calcMode if hasattr(wb, 'calculation') else None
                }
                wb.close()
            else:
                # Use pandas for .xls files
                xl_file = pd.ExcelFile(file_path)
                info = {
                    "file_format": "xls",
                    "sheet_names": xl_file.sheet_names,
                    "active_sheet": xl_file.sheet_names[0] if xl_file.sheet_names else None
                }

            return info

        except Exception as e:
            logger.error(f"Failed to get workbook info: {e}")
            return {"file_format": "unknown", "sheet_names": []}

    def _get_sheet_names(self, file_path: str) -> List[str]:
        """Get all sheet names from Excel file"""
        try:
            if file_path.endswith('.xlsx'):
                wb = openpyxl.load_workbook(file_path, read_only=True)
                sheet_names = wb.sheetnames
                wb.close()
            else:
                xl_file = pd.ExcelFile(file_path)
                sheet_names = xl_file.sheet_names

            return sheet_names

        except Exception as e:
            logger.error(f"Failed to get sheet names: {e}")
            return ["Sheet1"]  # Default fallback

    async def _process_sheet(self, file_path: str, sheet_name: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single sheet"""
        try:
            # Read sheet with pandas
            include_empty = options.get("include_empty_rows", False)

            if sheet_name.isdigit():
                # Sheet index
                df = pd.read_excel(file_path, sheet_index=int(sheet_name))
            else:
                # Sheet name
                df = pd.read_excel(file_path, sheet_name=sheet_name)

            # Clean DataFrame
            df = self._clean_dataframe(df, include_empty)

            # Convert to list of lists
            data = [df.columns.tolist()]  # Headers
            for _, row in df.iterrows():
                data.append([self._format_cell_value(cell) for cell in row])

            return {
                "name": sheet_name,
                "data": data,
                "rows": len(df),
                "columns": len(df.columns),
                "dataframe": df
            }

        except Exception as e:
            logger.error(f"Failed to process sheet {sheet_name}: {e}")
            # Return empty sheet data
            return {
                "name": sheet_name,
                "data": [],
                "rows": 0,
                "columns": 0,
                "dataframe": pd.DataFrame()
            }

    def _clean_dataframe(self, df: pd.DataFrame, include_empty: bool = False) -> pd.DataFrame:
        """Clean and prepare DataFrame"""
        try:
            # Remove completely empty rows and columns if not including empty
            if not include_empty:
                df = df.dropna(how='all').dropna(axis=1, how='all')

            # Find the actual header row (first non-empty row)
            if len(df) > 0:
                header_row_idx = 0
                for idx, row in df.iterrows():
                    # Check if this row has any non-empty values
                    if any(pd.notna(val) and str(val).strip() != '' for val in row):
                        header_row_idx = idx
                        break
                
                # If we found empty rows at the top, remove them
                if header_row_idx > 0:
                    df = df.iloc[header_row_idx:].reset_index(drop=True)

            # Reset index
            df = df.reset_index(drop=True)

            # Fill NaN values with empty string for consistency
            df = df.fillna('')

            # Generate proper column names if they are all 'Unnamed' or generic
            if all('Unnamed:' in str(col) or col == '' for col in df.columns):
                # Try to find a better header row within the first few rows
                header_found = False
                for check_row_idx in range(min(5, len(df))):  # Check first 5 rows max
                    row = df.iloc[check_row_idx]
                    # Check if this row looks like a header (has varied content)
                    non_empty_values = [str(val).strip() for val in row if str(val).strip() != '']
                    if len(non_empty_values) >= 3:  # At least 3 non-empty values for header
                        # Use this row as header and remove it from data
                        df.columns = [str(val).strip() if str(val).strip() != '' else f'Column_{i+1}' 
                                    for i, val in enumerate(row)]
                        df = df.iloc[check_row_idx+1:].reset_index(drop=True)
                        header_found = True
                        break
                
                if not header_found:
                    df.columns = [f'Column_{i+1}' for i in range(len(df.columns))]

            return df

        except Exception as e:
            logger.error(f"Failed to clean DataFrame: {e}")
            return df

    def _format_cell_value(self, value: Any) -> str:
        """Format cell value for display"""
        try:
            if pd.isna(value) or value == '':
                return ''
            elif isinstance(value, (int, float)):
                # Format numbers
                if isinstance(value, float) and not value.is_integer():
                    return f"{value:.2f}"
                else:
                    return str(int(value) if isinstance(value, float) else value)
            else:
                return str(value).strip()

        except Exception:
            return str(value) if value is not None else ''

    def _convert_to_markdown(self, excel_data: Dict[str, Any], options: Dict[str, Any]) -> str:
        """Convert Excel data to Markdown"""
        try:
            markdown_parts = []

            # Add title
            file_name = excel_data.get("file_name", "Excel Document")
            markdown_parts.append(f"# {file_name}")
            markdown_parts.append("")

            # Add workbook info
            workbook_info = excel_data.get("workbook_info", {})
            if workbook_info.get("sheet_names"):
                markdown_parts.append(f"**Sheets:** {', '.join(workbook_info['sheet_names'])}")
                markdown_parts.append("")

            # Process each sheet
            sheets = excel_data.get("sheets", {})
            for sheet_name, sheet_data in sheets.items():
                if sheet_data.get("data") and len(sheet_data["data"]) > 0:
                    # Add sheet title
                    markdown_parts.append(f"## {sheet_name}")
                    markdown_parts.append("")

                    # Create table
                    table_markdown = self._create_markdown_table(
                        sheet_data["data"][0],  # headers
                        sheet_data["data"][1:]   # rows
                    )
                    markdown_parts.append(table_markdown)
                    markdown_parts.append("")

                    # Add sheet statistics
                    rows = sheet_data.get("rows", 0)
                    columns = sheet_data.get("columns", 0)
                    markdown_parts.append(f"*Rows: {rows}, Columns: {columns}*")
                    markdown_parts.append("")

            if not markdown_parts[-1]:  # Remove trailing empty line
                markdown_parts.pop()

            return "\n".join(markdown_parts)

        except Exception as e:
            logger.error(f"Failed to convert to Markdown: {e}")
            return f"# {excel_data.get('file_name', 'Excel Document')}\n\nError converting to Markdown: {str(e)}"

    def _create_structured_data(self, excel_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create structured data from Excel data"""
        structured_data = []

        try:
            sheets = excel_data.get("sheets", {})
            for sheet_name, sheet_data in sheets.items():
                if sheet_data.get("data") and len(sheet_data["data"]) > 1:  # Has headers and at least one row
                    table_data = {
                        "type": "table",
                        "sheet_name": sheet_name,
                        "headers": sheet_data["data"][0],
                        "rows": sheet_data["data"][1:],
                        "row_count": len(sheet_data["data"]) - 1,
                        "column_count": len(sheet_data["data"][0])
                    }
                    structured_data.append(table_data)

        except Exception as e:
            logger.error(f"Failed to create structured data: {e}")

        return structured_data

    def _extract_excel_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract Excel-specific metadata"""
        try:
            metadata = {}
            file_ext = Path(file_path).suffix.lower()

            if file_ext == 'xlsx':
                # Use openpyxl for .xlsx files
                wb = openpyxl.load_workbook(file_path, read_only=True)
                metadata.update({
                    "file_format": "xlsx",
                    "sheet_count": len(wb.sheetnames),
                    "sheet_names": wb.sheetnames,
                    "active_sheet": wb.active.title if wb.active else None
                })

                # Try to get document properties
                if hasattr(wb, 'properties'):
                    props = wb.properties
                    metadata.update({
                        "title": getattr(props, 'title', ''),
                        "subject": getattr(props, 'subject', ''),
                        "creator": getattr(props, 'creator', ''),
                        "keywords": getattr(props, 'keywords', ''),
                        "description": getattr(props, 'description', ''),
                        "category": getattr(props, 'category', ''),
                        "comments": getattr(props, 'comments', '')
                    })

                wb.close()

            else:
                # Use pandas for .xls files
                xl_file = pd.ExcelFile(file_path)
                metadata.update({
                    "file_format": "xls",
                    "sheet_count": len(xl_file.sheet_names),
                    "sheet_names": xl_file.sheet_names,
                    "active_sheet": xl_file.sheet_names[0] if xl_file.sheet_names else None
                })

            return metadata

        except Exception as e:
            logger.error(f"Failed to extract Excel metadata: {e}")
            return {}