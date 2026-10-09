"""
PDF processor for converting PDF files to Markdown
"""

import logging
import os
import re
import time
from typing import Dict, Any, List, Optional
from pathlib import Path

from processors.base_processor import BaseProcessor
from utils.exceptions import ProcessingFailedError, CorruptedFileError

logger = logging.getLogger(__name__)


class PDFProcessor(BaseProcessor):
    """PDF file processor using markitdown"""

    def __init__(self):
        super().__init__()
        self.supported_extensions = ["pdf"]
        self.supported_mime_types = ["application/pdf"]

    async def process(self, file_path: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process PDF file and convert to Markdown

        Args:
            file_path: Path to the PDF file
            options: Processing options including:
                - extract_tables: bool (default: True)
                - extract_text: bool (default: True)
                - preserve_formatting: bool (default: True)
                - ocr_enabled: bool (default: False)
                - target_language: str (default: "vi")

        Returns:
            Dictionary with markdown content and structured data
        """
        try:
            start_time = time.time()
            options = options or {}

            logger.info(f"Processing PDF file: {file_path}")

            # Validate file
            if not self.validate_file(file_path):
                raise CorruptedFileError(f"Invalid PDF file: {file_path}")

            # Convert PDF to Markdown using markitdown
            markdown_content = await self._convert_pdf_to_markdown(file_path, options)

            # Extract structured data from markdown
            structured_data = self._parse_markdown_to_structured_data(markdown_content)

            # Extract metadata
            metadata = self._extract_metadata(file_path)
            metadata.update({
                "processing_time": time.time() - start_time,
                "tables_extracted": len([item for item in structured_data if item.get("type") == "table"]),
                "text_extracted": bool(markdown_content.strip()),
                "options_used": options
            })

            logger.info(f"PDF processing completed for {file_path}")

            return {
                "markdown_content": markdown_content,
                "structured_data": structured_data,
                "metadata": metadata
            }

        except Exception as e:
            logger.error(f"PDF processing failed for {file_path}: {e}", exc_info=True)
            raise ProcessingFailedError(f"Failed to process PDF: {str(e)}", "pdf_conversion")

    def validate_file(self, file_path: str) -> bool:
        """Validate PDF file"""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return False

            # Check file extension
            if not file_path.lower().endswith('.pdf'):
                return False

            # Basic PDF header validation
            with open(file_path, 'rb') as f:
                header = f.read(5)
                if not header.startswith(b'%PDF-'):
                    return False

            return True

        except Exception as e:
            logger.error(f"PDF validation failed for {file_path}: {e}")
            return False

    async def _convert_pdf_to_markdown(self, file_path: str, options: Dict[str, Any]) -> str:
        """Convert PDF to Markdown using markitdown"""
        try:
            # Import markitdown
            from markitdown import MarkItDown

            # Initialize MarkItDown converter
            md = MarkItDown()

            logger.info(f"Converting PDF to markdown: {file_path}")

            # Convert PDF to Markdown
            result = md.convert(file_path)
            
            # Extract text content from result
            if hasattr(result, 'text_content'):
                markdown_content = result.text_content
            elif hasattr(result, 'text'):
                markdown_content = result.text
            else:
                markdown_content = str(result)

            logger.info(f"PDF conversion successful, content length: {len(markdown_content)}")
            return markdown_content

        except ImportError:
            logger.warning("markitdown not available, using fallback method")
            return await self._fallback_pdf_conversion(file_path, options)

        except Exception as e:
            logger.error(f"Markitdown conversion failed: {e}", exc_info=True)
            # Fallback to basic conversion
            return await self._fallback_pdf_conversion(file_path, options)

    async def _fallback_pdf_conversion(self, file_path: str, options: Dict[str, Any]) -> str:
        """Fallback PDF conversion method"""
        try:
            # Try to use PyPDF2 for basic text extraction
            import PyPDF2

            markdown_content = []
            markdown_content.append(f"# PDF Document: {Path(file_path).stem}")
            markdown_content.append("")

            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)

                markdown_content.append(f"**Total Pages:** {num_pages}")
                markdown_content.append("")

                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    if text.strip():
                        markdown_content.append(f"## Page {page_num + 1}")
                        markdown_content.append("")
                        markdown_content.append(text)
                        markdown_content.append("")

            return "\n".join(markdown_content)

        except ImportError:
            logger.warning("PyPDF2 not available, creating placeholder")
            return self._create_placeholder_markdown(file_path, options)

        except Exception as e:
            logger.error(f"Fallback PDF conversion failed: {e}")
            return self._create_placeholder_markdown(file_path, options)

    def _create_placeholder_markdown(self, file_path: str, options: Dict[str, Any]) -> str:
        """Create placeholder Markdown when PDF conversion fails"""
        filename = Path(file_path).stem
        file_hash = hash(file_path + str(os.path.getsize(file_path))) % 10000
        
        markdown_content = f"""# PDF Document: {filename}

**Note:** PDF processing encountered issues. Showing file information.

## File Information
- **Filename:** {filename}
- **File Path:** {file_path}
- **File Size:** {os.path.getsize(file_path)} bytes
- **File Hash ID:** {file_hash}
- **Processing Options:** {options}

## Extracted Text (Limited)
Unable to extract text content from PDF. The file may be:
- Scanned image PDF (requires OCR)
- Password protected
- Corrupted or damaged
- Using unsupported encoding

## Next Steps
1. Check if the PDF is password protected
2. Try opening the PDF manually to verify content
3. Install OCR dependencies for scanned PDFs: `pip install pytesseract`
4. Ensure the PDF contains selectable text, not just images

## Debug Info
- Processing time: {time.time()}
- Error: PDF text extraction failed
- Recommendation: Use a different PDF or convert to text format

---
*Generated by File Comparison System*
"""
        return markdown_content

    def _parse_markdown_to_structured_data(self, markdown_content: str) -> List[Dict[str, Any]]:
        """Parse Markdown content to extract structured data"""
        structured_data = []

        try:
            lines = markdown_content.split('\n')
            
            # First, try to parse markdown tables
            current_table = None
            table_headers = []
            table_rows = []

            for line in lines:
                line = line.strip()

                # Detect table headers
                if line.startswith('|') and '|' in line[1:]:
                    if current_table is None:
                        # Start new table
                        current_table = {
                            "type": "table",
                            "headers": [],
                            "rows": []
                        }
                        table_headers = [cell.strip() for cell in line.split('|')[1:-1]]
                        current_table["headers"] = table_headers
                    elif all(c.strip() in ('', '-', ':') for c in line.split('|')[1:-1]):
                        # Table separator, continue
                        continue
                    else:
                        # Table row
                        row_data = [cell.strip() for cell in line.split('|')[1:-1]]
                        if len(row_data) == len(table_headers):
                            current_table["rows"].append(row_data)

                # End table
                elif current_table is not None and not line.startswith('|'):
                    if current_table["rows"]:  # Only add if table has data
                        structured_data.append(current_table)
                    current_table = None
                    table_headers = []
                    table_rows = []

            # Add last table if exists
            if current_table is not None and current_table["rows"]:
                structured_data.append(current_table)

            # If no markdown tables found, try to parse invoice-like structure
            if not structured_data:
                logger.info("No markdown tables found, attempting to parse invoice structure")
                table_data = self._parse_invoice_structure(lines)
                if table_data:
                    structured_data.append(table_data)
                else:
                    contract_table = self._parse_contract_structure(lines)
                    if contract_table:
                        structured_data.append(contract_table)

            # Extract text sections
            text_sections = []
            current_section = None

            for line in lines:
                line = line.strip()

                # Detect headers
                if line.startswith('#'):
                    if current_section:
                        text_sections.append(current_section)
                    current_section = {
                        "type": "text",
                        "level": len(line) - len(line.lstrip('#')),
                        "title": line.lstrip('# ').strip(),
                        "content": []
                    }
                elif current_section and line:
                    current_section["content"].append(line)

            if current_section:
                text_sections.append(current_section)

            # Add text sections to structured data
            structured_data.extend(text_sections)

        except Exception as e:
            logger.error(f"Failed to parse markdown to structured data: {e}")

        return structured_data

    def _parse_invoice_structure(self, lines: List[str]) -> Optional[Dict[str, Any]]:
        """Parse invoice-like structure from PDF content"""
        try:
            # Look for patterns that indicate invoice data
            header_patterns = [
                ["STT", "Tên hàng hóa", "Đơn vị", "Số lượng", "Đơn giá", "Thành tiền"],
                ["STT", "Tên hàng hóa", "Số lượng", "Đơn giá", "Thành tiền"],
                ["STT", "Tên hàng hóa, dịch vụ", "Đơn vị", "Số lượng", "Đơn giá", "Thành tiền"],
                # Handle garbled Vietnamese text from PDF extraction
                ["STT", "Tên hàng hóa", "dnch vn", "Sn lnnng", "nnn giá", "Thành tinn"],
                ["STT", "Tên hàng hóa, dnch vn", "nnn vn", "Sn lnnng", "nnn giá", "Thành tinn"],
                ["STT", "Ten hang hoa", "Don vi", "So luong", "Don gia", "Thanh tien"],
                ["STT", "Ten hang hoa", "So luong", "Don gia", "Thanh tien"],
                # Simple patterns that might match
                ["STT", "Tên hàng", "Số lượng", "Đơn giá", "Thành tiền"],
                ["STT", "Hàng hóa", "Số lượng", "Đơn giá", "Thành tiền"]
            ]
            
            # Find the header row
            header_line_idx = -1
            matched_headers = None
            
            for i, line in enumerate(lines):
                line_clean = line.strip().upper()
                for headers in header_patterns:
                    # More flexible matching - at least 3 key headers should match
                    match_count = 0
                    for header in headers:
                        header_upper = header.upper()
                        if header_upper in line_clean or header in line:
                            match_count += 1
                    
                    # Consider it a match if at least half of the headers are found
                    if match_count >= len(headers) // 2 + 1:
                        header_line_idx = i
                        matched_headers = headers
                        logger.info(f"Found headers at line {i}: {line} (matched {match_count}/{len(headers)})")
                        break
                if header_line_idx != -1:
                    break
            
            if header_line_idx == -1:
                logger.warning("No invoice headers found in content")
                return None
            
            # Extract data after headers
            table_rows = []
            expected_columns = len(matched_headers)
            
            # Skip empty lines and separator lines
            data_start = header_line_idx + 1
            while data_start < len(lines) and (not lines[data_start].strip() or 
                                              all(c in '-_=+' for c in lines[data_start].strip())):
                data_start += 1
            
            # Extract data using column-based parsing
            table_rows = self._parse_columnar_data(lines, data_start)
            logger.info(f"Parsed {len(table_rows)} rows from columnar data")
            
            if table_rows:
                logger.info(f"Successfully parsed {len(table_rows)} invoice rows")
                return {
                    "type": "table",
                    "headers": matched_headers,
                    "rows": table_rows,
                    "row_count": len(table_rows),
                    "column_count": expected_columns
                }
            
            logger.warning("No data rows found in invoice structure")
            return None
            
        except Exception as e:
            logger.error(f"Failed to parse invoice structure: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _parse_contract_structure(self, lines: List[str]) -> Optional[Dict[str, Any]]:
        """Parse contract-style tables laid out in column blocks"""
        try:
            header_idx = next((i for i, line in enumerate(lines) if line.strip().lower() == "no."), None)
            if header_idx is None:
                return None

            amount_idx = next((i for i, line in enumerate(lines) if line.strip().lower() == "amount"), None)
            skip_tokens = {
                "no.",
                "description",
                "quantity",
                "unit",
                "unit price (usd)",
                "unit price",
                "amount",
                "(usd)",
                "total amount fob hai phong, vietnam",
                "as per incoterms 2010",
                "tổng số tiền fob hải phòng, việt nam",
                "theo incoterms 2010"
            }

            main_segment = []
            end_idx = amount_idx if amount_idx is not None else len(lines)
            for idx in range(header_idx + 1, end_idx):
                text = lines[idx].strip()
                if not text:
                    continue
                lower = text.lower()
                if lower in skip_tokens or lower.startswith("total amount"):
                    continue
                main_segment.append(text)

            if not main_segment:
                return None

            seq_numbers = []
            i = 0
            while i < len(main_segment) and main_segment[i].isdigit():
                seq_numbers.append(main_segment[i])
                i += 1

            item_count = len(seq_numbers)
            if item_count == 0:
                return None

            desc_lines = []
            while i < len(main_segment) and not self._is_number(main_segment[i]):
                desc_lines.append(main_segment[i])
                i += 1

            if not desc_lines:
                return None

            def compose_descriptions(lines_list: List[str], count: int) -> List[str]:
                if not lines_list:
                    return []
                if len(lines_list) == count:
                    return [line.strip() for line in lines_list]
                if len(lines_list) % count == 0:
                    chunk = len(lines_list) // count
                    return [" ".join(lines_list[j * chunk:(j + 1) * chunk]).strip() for j in range(count)]

                result: List[str] = []
                current: List[str] = []
                for entry in lines_list:
                    lower_entry = entry.lower()
                    starts_new = lower_entry.startswith((
                        "coated",
                        "uncoated",
                        "canxi",
                        "calcium",
                        "talc",
                        "kaolin",
                        "phí",
                        "phi"
                    ))
                    if current and starts_new and len(result) < count:
                        result.append(" ".join(current).strip())
                        current = [entry]
                    else:
                        current.append(entry)

                if current and len(result) < count:
                    result.append(" ".join(current).strip())

                if len(result) < count:
                    result.extend([""] * (count - len(result)))

                return result[:count]

            descriptions = compose_descriptions(desc_lines, item_count)
            if len(descriptions) < item_count:
                return None

            quantities: List[str] = []
            while i < len(main_segment) and len(quantities) < item_count and self._is_number(main_segment[i]):
                quantities.append(main_segment[i])
                i += 1

            if len(quantities) < item_count:
                return None

            unit_candidates = {
                "kg",
                "ton",
                "tons",
                "tấn",
                "tan",
                "unit",
                "units",
                "pcs",
                "piece",
                "pieces",
                "lượt",
                "luot",
                "box",
                "bag",
                "bộ",
                "bo"
            }

            units: List[str] = []
            while i < len(main_segment) and len(units) < item_count:
                entry = main_segment[i]
                if entry.lower() in unit_candidates:
                    units.append(entry)
                    i += 1
                else:
                    break

            if len(units) < item_count:
                units.extend([""] * (item_count - len(units)))

            unit_prices: List[str] = []
            while i < len(main_segment) and len(unit_prices) < item_count:
                entry = main_segment[i]
                if self._is_number(entry):
                    unit_prices.append(entry)
                i += 1

            if len(unit_prices) < item_count:
                return None

            amount_values: List[str] = [""] * item_count
            if amount_idx is not None:
                collected: List[str] = []
                for idx in range(amount_idx + 1, len(lines)):
                    text = lines[idx].strip()
                    if not text:
                        continue
                    lower = text.lower()
                    if lower.startswith("2. ") or lower.startswith("2."):
                        break
                    if lower in skip_tokens or lower.startswith("(say words") or "bằng chữ" in lower:
                        continue
                    if self._is_number(text):
                        collected.append(text)

                if collected:
                    amount_values = (collected + [""] * item_count)[:item_count]

            headers = [
                "No.",
                "Description",
                "Quantity",
                "Unit",
                "Unit price (USD)",
                "Amount (USD)"
            ]

            rows = []
            for idx in range(item_count):
                rows.append([
                    seq_numbers[idx] if idx < len(seq_numbers) else str(idx + 1),
                    descriptions[idx] if idx < len(descriptions) else "",
                    quantities[idx] if idx < len(quantities) else "",
                    units[idx] if idx < len(units) else "",
                    unit_prices[idx] if idx < len(unit_prices) else "",
                    amount_values[idx] if idx < len(amount_values) else ""
                ])

            return {
                "type": "table",
                "headers": headers,
                "rows": rows,
                "row_count": len(rows),
                "column_count": len(headers)
            }

        except Exception as e:
            logger.error(f"Failed to parse contract structure: {e}")
            return None
    
    def _looks_like_data_row(self, line: str) -> bool:
        """Check if a line looks like invoice data row"""
        # Remove extra whitespace and check pattern
        cleaned = line.strip()
        
        # Skip empty lines
        if not cleaned:
            return False
        
        # Skip header and summary lines
        if any(keyword in cleaned.upper() for keyword in ["STT", "TỔNG TÍNH", "TỔNG CỘNG", "VAT", "THÀNH TIỀN", "HÓA ĐƠN"]):
            return False
        
        # Look for product names, quantities, or units
        if (len(cleaned) > 3 and 
            (any(word in cleaned.lower() for word in ['kg', 'cái', 'lô', 'mesh', 'powder', 'clay', 'carbonate']) or
             self._is_number(cleaned) or
             any(char.isdigit() for char in cleaned))):
            return True
            
        return False
    
    def _parse_invoice_row(self, line: str, expected_columns: int) -> List[str]:
        """Parse a single invoice row into columns"""
        try:
            parts = line.split()
            row_data = []
            current_desc = []
            
            for part in parts:
                if self._is_number(part):
                    # If we find a number, finish current description and add the number
                    if current_desc:
                        row_data.append(' '.join(current_desc))
                        current_desc = []
                    row_data.append(part)
                else:
                    if part.lower() in ['kg', 'cái', 'lô', 'túi', 'hộp', 'bộ', 'chiếc', 'lon', 'vỉ', 'thùng', 'ton', 'tons', 'tấn', 'tan']:
                        if current_desc:
                            row_data.append(' '.join(current_desc))
                            current_desc = []
                        row_data.append(part)
                    else:
                        current_desc.append(part)
            
            # Add remaining description
            if current_desc:
                row_data.append(' '.join(current_desc))
            
            # Handle cases where we didn't find any numbers (all description)
            if len(row_data) == 1:
                # Try to split by common patterns
                text = row_data[0]
                # Look for price patterns at the end
                import re
                price_match = re.search(r'(\d+(?:,\d+)*)$', text)
                if price_match:
                    price = price_match.group(1)
                    desc = text[:price_match.start()].strip()
                    return [desc, price]
            
            return row_data
            
        except Exception as e:
            logger.error(f"Error parsing invoice row '{line}': {e}")
            return [line]  # Return as single column if parsing fails
    
    def _parse_columnar_data(self, lines: List[str], start_idx: int) -> List[List[str]]:
        """Parse column-based invoice data where items and values are on separate lines"""
        try:
            # Extract all non-empty lines after headers
            data_lines = []
            for i in range(start_idx, len(lines)):
                line = lines[i].strip()
                
                # Stop at summary lines
                if any(keyword in line.upper() for keyword in ["TỔNG TÍNH", "TỔNG CỘNG", "VAT", "THÀNH TIỀN", "TỔNG", "Tnm tính"]):
                    break
                
                # Include non-empty lines
                if line:
                    data_lines.append(line)
            
            logger.info(f"Found {len(data_lines)} data lines: {data_lines}")
            
            # Use the specialized columnar reconstruction method
            return self._reconstruct_columnar_table(data_lines)
            
        except Exception as e:
            logger.error(f"Error parsing columnar data: {e}")
            return []
    
    def _reconstruct_columnar_table(self, data_lines: List[str]) -> List[List[str]]:
        """Reconstruct table from columnar PDF layout"""
        try:
            # The PDF layout appears to be:
            # STT numbers (1, 2, 3, 4...)
            # Product names 
            # Units (kg, kg, kg, lượt)
            # Quantities (500, 200, 100, 1)
            # Unit prices (75000, 120000, 95000, 500000)
            # Amounts (37500000, 24000000, 9500000, 500000)
            
            # Find where the actual data starts
            # Look for the first short number that's likely a sequence number
            seq_start = -1
            for i, line in enumerate(data_lines):
                if line.isdigit() and len(line) <= 2 and i < 10:  # Sequence numbers are usually 1-2 digits and early
                    seq_start = i
                    break
            
            if seq_start == -1:
                logger.warning("Could not find sequence number start")
                return []
            
            # Extract the data sections
            seq_numbers = []
            product_names = []
            units = []
            quantities = []
            unit_prices = []
            amounts = []
            
            i = seq_start
            # Extract sequence numbers (consecutive short numbers)
            while i < len(data_lines) and data_lines[i].isdigit() and len(data_lines[i]) <= 2:
                seq_numbers.append(data_lines[i])
                i += 1
            
            # Extract product names (until we hit units or numbers)
            while i < len(data_lines) and not self._is_number(data_lines[i]) and data_lines[i].lower() not in ['kg', 'cái', 'lô', 'túi', 'hộp', 'bộ', 'chiếc', 'lon', 'vỉ', 'thùng', 'ton', 'tons', 'tấn', 'tan']:
                product_names.append(data_lines[i])
                i += 1
            
            # Extract units
            while i < len(data_lines) and data_lines[i].lower() in ['kg', 'cái', 'lô', 'túi', 'hộp', 'bộ', 'chiếc', 'lon', 'vỉ', 'thùng', 'lnnt', 'ton', 'tons', 'tấn', 'tan']:
                units.append(data_lines[i])
                i += 1
            
            # Extract quantities
            while i < len(data_lines) and self._is_number(data_lines[i]) and len(quantities) < len(seq_numbers):
                quantities.append(data_lines[i])
                i += 1
            
            # Extract unit prices
            while i < len(data_lines) and self._is_number(data_lines[i]) and len(unit_prices) < len(seq_numbers):
                unit_prices.append(data_lines[i])
                i += 1
            
            # Extract amounts
            while i < len(data_lines) and self._is_number(data_lines[i]) and len(amounts) < len(seq_numbers):
                amounts.append(data_lines[i])
                i += 1
            
            logger.info(f"Parsed sections - Seq: {seq_numbers}, Products: {product_names}, Units: {units}, Qty: {quantities}, Prices: {unit_prices}, Amounts: {amounts}")
            
            # Build table rows
            table_rows = []
            num_items = len(seq_numbers)
            
            for idx in range(num_items):
                row = [""] * 6  # STT, Tên hàng hóa, Đơn vị, Số lượng, Đơn giá, Thành tiền
                
                row[0] = seq_numbers[idx] if idx < len(seq_numbers) else ""
                
                # For product names, we may need to group them if there are multiple products per sequence
                if idx < len(product_names):
                    # Handle cases where products might be split across multiple lines
                    if num_items == 1 and len(product_names) > 1:
                        # Single item with multiple description lines
                        row[1] = " ".join(product_names)
                    elif num_items == len(product_names):
                        # One product per item
                        row[1] = product_names[idx]
                    elif num_items < len(product_names):
                        # More products than items, group them
                        products_per_item = len(product_names) // num_items
                        start_idx = idx * products_per_item
                        end_idx = start_idx + products_per_item
                        if idx == num_items - 1:  # Last item gets remaining products
                            end_idx = len(product_names)
                        row[1] = " ".join(product_names[start_idx:end_idx])
                    else:
                        # Fewer products than items, assign what we can
                        if idx < len(product_names):
                            row[1] = product_names[idx]
                
                row[2] = units[idx] if idx < len(units) else ""
                row[3] = quantities[idx] if idx < len(quantities) else ""
                row[4] = unit_prices[idx] if idx < len(unit_prices) else ""
                row[5] = amounts[idx] if idx < len(amounts) else ""
                
                table_rows.append(row)
                logger.debug(f"Built row {idx+1}: {row}")
            
            return table_rows
            
        except Exception as e:
            logger.error(f"Error reconstructing columnar table: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _parse_single_item(self, item_data: List[str]) -> List[str]:
        """Parse a single item's data from its component lines"""
        try:
            # Expected format: [seq, product, unit, qty, unit_price, amount]
            normalized = [""] * 6
            
            if not item_data:
                return normalized
            
            # First element is usually the sequence number
            if item_data[0].isdigit():
                normalized[0] = item_data[0]
            
            # Find product descriptions (contain keywords, not numbers)
            product_parts = []
            for line in item_data[1:]:
                if self._looks_like_product_description(line):
                    product_parts.append(line)
                elif line.lower() in ['kg', 'cái', 'lô', 'túi', 'hộp', 'bộ', 'chiếc', 'lon', 'vỉ', 'thùng', 'ton', 'tons', 'tấn', 'tan']:
                    normalized[2] = line  # Unit
                elif self._is_number(line):
                    # This will be handled below
                    continue
                else:
                    # Might be part of product name
                    product_parts.append(line)
            
            # Build product name
            if product_parts:
                normalized[1] = " ".join(product_parts)
            
            # Extract numbers in order (should be quantity, unit price, amount)
            numbers = []
            for line in item_data[1:]:
                if self._is_number(line):
                    numbers.append(line)
            
            # Assign numbers to columns
            if len(numbers) >= 1:
                normalized[3] = numbers[0]  # Quantity
            if len(numbers) >= 2:
                normalized[4] = numbers[1]  # Unit price
            if len(numbers) >= 3:
                normalized[5] = numbers[2]  # Amount
            
            logger.debug(f"Item data {item_data} -> normalized {normalized}")
            return normalized
            
        except Exception as e:
            logger.error(f"Error parsing single item {item_data}: {e}")
            return [""] * 6
    
    def _parse_by_pattern_detection(self, data_lines: List[str]) -> List[List[str]]:
        """Alternative parsing method when sequence numbers aren't clear"""
        try:
            table_rows = []
            
            # Look for the pattern: product description, unit, then numbers
            current_row = []
            
            for line in data_lines:
                if self._looks_like_product_description(line):
                    current_row.append(line)
                elif line.lower() in ['kg', 'cái', 'lô', 'túi', 'hộp', 'bộ', 'chiếc', 'lon', 'vỉ', 'thùng', 'ton', 'tons', 'tấn', 'tan']:
                    current_row.append(line)
                elif self._is_number(line):
                    current_row.append(line)
                else:
                    # Unknown line, might end current row
                    if len(current_row) >= 4:  # At least product + 3 numbers
                        parsed = self._parse_single_item(current_row)
                        if parsed:
                            table_rows.append(parsed)
                    current_row = []
            
            # Add final row
            if len(current_row) >= 4:
                parsed = self._parse_single_item(current_row)
                if parsed:
                    table_rows.append(parsed)
            
            return table_rows
            
        except Exception as e:
            logger.error(f"Error in pattern detection parsing: {e}")
            return []
    
    def _looks_like_product_description(self, line: str) -> bool:
        """Check if line looks like a product description"""
        if not line or len(line) < 3:
            return False
        
        # Skip if it's clearly a number
        if self._is_number(line):
            return False
        
        # Look for product keywords
        product_keywords = [
            'canxi', 'carbonate', 'coated', 'talc', 'powder', 'mesh', 
            'kaolin', 'clay', 'premium', 'phí', 'vận chuyển', 'chi phí', 'đóng gói'
        ]
        
        line_lower = line.lower()
        return any(keyword in line_lower for keyword in product_keywords)
    
    def _normalize_row_data(self, row_data: List[str]) -> List[str]:
        """Normalize row data to have consistent columns"""
        try:
            # Expected columns: STT, Tên hàng hóa, Đơn vị, Số lượng, Đơn giá, Thành tiền
            normalized = [""] * 6  # 6 columns
            
            if not row_data:
                return normalized
            
            # Find sequence number (should be first element if it's a number)
            seq_idx = 0
            if row_data and row_data[0].isdigit():
                normalized[0] = row_data[0]
                seq_idx = 1
            
            # Find unit (kg, cái, etc.)
            unit_idx = -1
            for j, item in enumerate(row_data[seq_idx:], seq_idx):
                if item.lower() in ['kg', 'cái', 'lô', 'túi', 'hộp', 'bộ', 'chiếc', 'lon', 'vỉ', 'thùng', 'ton', 'tons', 'tấn', 'tan']:
                    normalized[2] = item  # Đơn vị
                    unit_idx = j
                    break
            
            # Find numbers (quantity, unit price, amount)
            numbers = []
            for j, item in enumerate(row_data[seq_idx:], seq_idx):
                if self._is_number(item):
                    numbers.append(item)
            
            # Assign numbers to columns
            if len(numbers) >= 1:
                normalized[3] = numbers[0]  # Số lượng
            if len(numbers) >= 2:
                normalized[4] = numbers[1]  # Đơn giá
            if len(numbers) >= 3:
                normalized[5] = numbers[2]  # Thành tiền
            
            # Build product description from remaining text
            desc_parts = []
            for j, item in enumerate(row_data[seq_idx:], seq_idx):
                if j != unit_idx and not self._is_number(item) and item.lower() not in ['kg', 'cái', 'lô', 'túi', 'hộp', 'bộ', 'chiếc', 'lon', 'vỉ', 'thùng', 'ton', 'tons', 'tấn', 'tan']:
                    desc_parts.append(item)
            
            if desc_parts:
                normalized[1] = " ".join(desc_parts)  # Tên hàng hóa
            
            logger.debug(f"Normalized {row_data} -> {normalized}")
            return normalized
            
        except Exception as e:
            logger.error(f"Error normalizing row data {row_data}: {e}")
            return row_data[:6] if len(row_data) >= 6 else row_data + [""] * (6 - len(row_data))

    def _is_number(self, text: str) -> bool:
        """Check if text represents a number"""
        try:
            # Remove commas and try to convert to float
            cleaned = text.replace(',', '').strip()
            float(cleaned)
            return True
        except ValueError:
            return False

    def _extract_pdf_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract PDF-specific metadata"""
        try:
            import PyPDF2

            metadata = {}
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)

                # Basic PDF info
                metadata["num_pages"] = len(pdf_reader.pages)

                # PDF info if available
                if hasattr(pdf_reader, 'metadata') and pdf_reader.metadata:
                    pdf_info = pdf_reader.metadata
                    metadata.update({
                        "title": pdf_info.get('/Title', ''),
                        "author": pdf_info.get('/Author', ''),
                        "subject": pdf_info.get('/Subject', ''),
                        "creator": pdf_info.get('/Creator', ''),
                        "producer": pdf_info.get('/Producer', ''),
                        "creation_date": pdf_info.get('/CreationDate', ''),
                        "modification_date": pdf_info.get('/ModDate', '')
                    })

            return metadata

        except ImportError:
            logger.warning("PyPDF2 not available, basic metadata only")
            return {}
        except Exception as e:
            logger.error(f"Failed to extract PDF metadata: {e}")
            return {}