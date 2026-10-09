"""
Enhanced PDF processor with pdfplumber integration and coordinate-based extraction
Combines multiple PDF processing engines for maximum accuracy
"""

import logging
import os
import time
import tempfile
from typing import Dict, Any, List, Optional, Tuple, Union
from pathlib import Path
import json

# PDF processing libraries
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False
    logging.warning("pdfplumber not available")

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    logging.warning("PyMuPDF not available")

try:
    from markitdown import MarkItDown
    MARKITDOWN_AVAILABLE = True
except ImportError:
    MARKITDOWN_AVAILABLE = False
    logging.warning("markitdown not available")

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False
    logging.warning("PyPDF2 not available")

# Image processing for OCR
import cv2
import numpy as np
from PIL import Image

# OCR integration
from processors.ocr_processor import get_ocr_processor

from processors.base_processor import BaseProcessor
from utils.exceptions import ProcessingFailedError, CorruptedFileError

logger = logging.getLogger(__name__)


class PDFTextRegion:
    """Represents a text region with coordinates"""
    
    def __init__(self, text: str, bbox: Dict[str, float], confidence: float = 1.0):
        self.text = text
        self.bbox = bbox  # {'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1}
        self.confidence = confidence
        self.page_number = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "bbox": self.bbox,
            "confidence": self.confidence,
            "page": self.page_number
        }


class PDFTable:
    """Represents a table extracted from PDF"""
    
    def __init__(self, data: List[List[str]], bbox: Dict[str, float], page_number: int = 0):
        self.data = data
        self.bbox = bbox
        self.page_number = page_number
        self.headers = data[0] if data else []
        self.rows = data[1:] if len(data) > 1 else []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "headers": self.headers,
            "rows": self.rows,
            "bbox": self.bbox,
            "page": self.page_number,
            "row_count": len(self.rows),
            "column_count": len(self.headers)
        }


class EnhancedPDFProcessor(BaseProcessor):
    """Enhanced PDF processor with multiple engines and coordinate extraction"""

    def __init__(self):
        super().__init__()
        self.supported_extensions = ["pdf"]
        self.supported_mime_types = ["application/pdf"]
        
        # Check available engines
        self.engines = {
            'pdfplumber': PDFPLUMBER_AVAILABLE,
            'pymupdf': PYMUPDF_AVAILABLE,
            'markitdown': MARKITDOWN_AVAILABLE,
            'pypdf2': PYPDF2_AVAILABLE
        }
        
        logger.info(f"Available PDF engines: {list(name for name, available in self.engines.items() if available)}")
        
        # OCR processor for scanned PDFs
        self.ocr_processor = get_ocr_processor()
        
        # Configuration
        self.min_text_confidence = 0.5
        self.ocr_threshold = 0.3  # Switch to OCR if text extraction confidence < this

    async def process(self, file_path: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Enhanced PDF processing with multiple engines and OCR fallback
        
        Args:
            file_path: Path to PDF file
            options: Processing options including:
                - use_ocr: bool (default: auto-detect)
                - extract_tables: bool (default: True)
                - extract_images: bool (default: False)
                - preferred_engine: str (default: 'pdfplumber')
                - language: str (default: 'vie')

        Returns:
            Dictionary with extracted content, coordinates, and metadata
        """
        try:
            start_time = time.time()
            options = options or {}

            logger.info(f"Processing PDF with enhanced engine: {file_path}")

            # Validate file
            if not self.validate_file(file_path):
                raise CorruptedFileError(f"Invalid PDF file: {file_path}")

            # Determine processing strategy
            processing_strategy = await self._determine_processing_strategy(file_path, options)
            
            # Extract content using selected strategy
            result = await self._extract_with_strategy(file_path, processing_strategy, options)
            
            # Add metadata
            metadata = self._extract_metadata(file_path)
            metadata.update({
                "processing_time": time.time() - start_time,
                "processing_strategy": processing_strategy,
                "engines_used": list(self.engines.keys()),
                "ocr_enabled": processing_strategy.get("use_ocr", False),
                "options_used": options
            })

            logger.info(f"Enhanced PDF processing completed for {file_path}")

            return {
                **result,
                "metadata": metadata
            }

        except Exception as e:
            logger.error(f"Enhanced PDF processing failed for {file_path}: {e}", exc_info=True)
            raise ProcessingFailedError(f"Failed to process PDF: {str(e)}", "pdf_enhanced_processing")

    async def _determine_processing_strategy(self, file_path: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Determine the best processing strategy for this PDF"""
        strategy = {
            "use_ocr": options.get("use_ocr", "auto"),
            "primary_engine": options.get("preferred_engine", "pdfplumber"),
            "fallback_engines": []
        }

        # Test if PDF has extractable text
        has_text = await self._test_text_extractability(file_path)
        
        if strategy["use_ocr"] == "auto":
            strategy["use_ocr"] = not has_text
        
        # Determine engine order based on availability and PDF characteristics
        if PDFPLUMBER_AVAILABLE and strategy["primary_engine"] == "pdfplumber":
            strategy["fallback_engines"] = ["pymupdf", "markitdown", "pypdf2"]
        elif PYMUPDF_AVAILABLE and strategy["primary_engine"] == "pymupdf":
            strategy["fallback_engines"] = ["pdfplumber", "markitdown", "pypdf2"]
        else:
            # Use any available engine
            available = [name for name, available in self.engines.items() if available]
            if available:
                strategy["primary_engine"] = available[0]
                strategy["fallback_engines"] = available[1:]

        return strategy

    async def _test_text_extractability(self, file_path: str) -> bool:
        """Test if PDF has extractable text"""
        try:
            # Try with pdfplumber first (most reliable)
            if PDFPLUMBER_AVAILABLE:
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages[:3]:  # Check first 3 pages
                        if page.extract_text() and len(page.extract_text().strip()) > 50:
                            return True
            
            # Try with PyMuPDF
            if PYMUPDF_AVAILABLE:
                doc = fitz.open(file_path)
                for page in doc[:3]:
                    if page.get_text() and len(page.get_text().strip()) > 50:
                        doc.close()
                        return True
                doc.close()
            
            return False
            
        except Exception as e:
            logger.warning(f"Text extractability test failed: {e}")
            return False

    async def _extract_with_strategy(self, file_path: str, strategy: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """Extract content using the determined strategy"""
        language = options.get("language", "vie")
        extract_tables = options.get("extract_tables", True)
        
        result = {
            "text_content": "",
            "text_regions": [],
            "tables": [],
            "images": [],
            "structured_data": []
        }

        # Try primary engine first
        primary_result = await self._extract_with_engine(
            file_path, strategy["primary_engine"], extract_tables, language
        )
        
        if primary_result["success"]:
            result.update(primary_result["data"])
            
            # Check if we need OCR fallback
            if strategy["use_ocr"] or self._should_use_ocr_fallback(primary_result["data"]):
                logger.info("Applying OCR fallback for better text extraction")
                ocr_result = await self._extract_with_ocr(file_path, language)
                result = self._merge_extraction_results(result, ocr_result)
        else:
            # Try fallback engines
            for engine_name in strategy["fallback_engines"]:
                logger.info(f"Trying fallback engine: {engine_name}")
                fallback_result = await self._extract_with_engine(
                    file_path, engine_name, extract_tables, language
                )
                
                if fallback_result["success"]:
                    result.update(fallback_result["data"])
                    break
            
            # If all engines fail, use OCR as last resort
            if not result["text_content"] and strategy["use_ocr"] != False:
                logger.info("All text extraction engines failed, using OCR")
                ocr_result = await self._extract_with_ocr(file_path, language)
                result.update(ocr_result)

        # Post-process extracted content
        result = self._post_process_content(result)

        return result

    async def _extract_with_engine(self, file_path: str, engine_name: str, extract_tables: bool, language: str) -> Dict[str, Any]:
        """Extract content using specific engine"""
        try:
            if engine_name == "pdfplumber":
                return await self._extract_with_pdfplumber(file_path, extract_tables)
            elif engine_name == "pymupdf":
                return await self._extract_with_pymupdf(file_path, extract_tables)
            elif engine_name == "markitdown":
                return await self._extract_with_markitdown(file_path)
            elif engine_name == "pypdf2":
                return await self._extract_with_pypdf2(file_path)
            else:
                return {"success": False, "error": f"Unknown engine: {engine_name}"}
                
        except Exception as e:
            logger.error(f"Engine {engine_name} failed: {e}")
            return {"success": False, "error": str(e)}

    async def _extract_with_pdfplumber(self, file_path: str, extract_tables: bool) -> Dict[str, Any]:
        """Extract content using pdfplumber"""
        if not PDFPLUMBER_AVAILABLE:
            return {"success": False, "error": "pdfplumber not available"}
        
        try:
            result = {
                "success": True,
                "data": {
                    "text_content": "",
                    "text_regions": [],
                    "tables": []
                }
            }
            
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # Extract text with coordinates
                    words = page.extract_words()
                    for word in words:
                        region = PDFTextRegion(
                            text=word["text"],
                            bbox={
                                "x0": word["x0"],
                                "y0": word["top"],
                                "x1": word["x1"],
                                "y1": word["bottom"]
                            },
                            confidence=1.0  # pdfplumber doesn't provide confidence
                        )
                        region.page_number = page_num
                        result["data"]["text_regions"].append(region.to_dict())
                    
                    # Extract tables
                    if extract_tables:
                        tables = page.extract_tables()
                        for table in tables:
                            if table and len(table) > 1:  # At least header + one row
                                # Calculate table bbox
                                x_coords = [cell[0] if cell else 0 for row in table for cell in row if cell]
                                y_coords = [cell[1] if cell else 0 for row in table for cell in row if cell]
                                
                                if x_coords and y_coords:
                                    table_obj = PDFTable(
                                        data=[[str(cell) if cell else "" for cell in row] for row in table],
                                        bbox={
                                            "x0": min(x_coords),
                                            "y0": min(y_coords),
                                            "x1": max(x_coords) + 200,  # Estimate width
                                            "y1": max(y_coords) + 30    # Estimate height
                                        },
                                        page_number=page_num
                                    )
                                    result["data"]["tables"].append(table_obj.to_dict())
                    
                    # Extract plain text
                    page_text = page.extract_text()
                    if page_text:
                        result["data"]["text_content"] += f"\n\n--- Page {page_num + 1} ---\n{page_text}"
            
            return result
            
        except Exception as e:
            logger.error(f"pdfplumber extraction failed: {e}")
            return {"success": False, "error": str(e)}

    async def _extract_with_pymupdf(self, file_path: str, extract_tables: bool) -> Dict[str, Any]:
        """Extract content using PyMuPDF"""
        if not PYMUPDF_AVAILABLE:
            return {"success": False, "error": "PyMuPDF not available"}
        
        try:
            result = {
                "success": True,
                "data": {
                    "text_content": "",
                    "text_regions": [],
                    "tables": []
                }
            }
            
            doc = fitz.open(file_path)
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Extract text with coordinates
                text_dict = page.get_text("dict")
                for block in text_dict["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                region = PDFTextRegion(
                                    text=span["text"],
                                    bbox={
                                        "x0": span["bbox"][0],
                                        "y0": span["bbox"][1],
                                        "x1": span["bbox"][2],
                                        "y1": span["bbox"][3]
                                    },
                                    confidence=1.0
                                )
                                region.page_number = page_num
                                result["data"]["text_regions"].append(region.to_dict())
                
                # Extract tables (limited in PyMuPDF)
                if extract_tables:
                    tables = page.find_tables()
                    for table in tables:
                        table_data = table.extract()
                        if table_data and len(table_data) > 1:
                            table_obj = PDFTable(
                                data=table_data,
                                bbox={
                                    "x0": table.bbox[0],
                                    "y0": table.bbox[1],
                                    "x1": table.bbox[2],
                                    "y1": table.bbox[3]
                                },
                                page_number=page_num
                            )
                            result["data"]["tables"].append(table_obj.to_dict())
                
                # Extract plain text
                page_text = page.get_text()
                if page_text:
                    result["data"]["text_content"] += f"\n\n--- Page {page_num + 1} ---\n{page_text}"
            
            doc.close()
            return result
            
        except Exception as e:
            logger.error(f"PyMuPDF extraction failed: {e}")
            return {"success": False, "error": str(e)}

    async def _extract_with_markitdown(self, file_path: str) -> Dict[str, Any]:
        """Extract content using MarkItDown"""
        if not MARKITDOWN_AVAILABLE:
            return {"success": False, "error": "MarkItDown not available"}
        
        try:
            md = MarkItDown()
            result_data = md.convert(file_path)
            
            text_content = ""
            if hasattr(result_data, 'text_content'):
                text_content = result_data.text_content
            elif hasattr(result_data, 'text'):
                text_content = result_data.text
            else:
                text_content = str(result_data)
            
            return {
                "success": True,
                "data": {
                    "text_content": text_content,
                    "text_regions": [],
                    "tables": []
                }
            }
            
        except Exception as e:
            logger.error(f"MarkItDown extraction failed: {e}")
            return {"success": False, "error": str(e)}

    async def _extract_with_pypdf2(self, file_path: str) -> Dict[str, Any]:
        """Extract content using PyPDF2"""
        if not PYPDF2_AVAILABLE:
            return {"success": False, "error": "PyPDF2 not available"}
        
        try:
            result = {
                "success": True,
                "data": {
                    "text_content": "",
                    "text_regions": [],
                    "tables": []
                }
            }
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        result["data"]["text_content"] += f"\n\n--- Page {page_num + 1} ---\n{page_text}"
            
            return result
            
        except Exception as e:
            logger.error(f"PyPDF2 extraction failed: {e}")
            return {"success": False, "error": str(e)}

    async def _extract_with_ocr(self, file_path: str, language: str) -> Dict[str, Any]:
        """Extract content using OCR for scanned PDFs"""
        try:
            result = {
                "text_content": "",
                "text_regions": [],
                "tables": []
            }
            
            # Convert PDF pages to images
            images = await self._pdf_to_images(file_path)
            
            for page_num, image_path in enumerate(images):
                # Extract text using OCR
                ocr_result = await self.ocr_processor.extract_with_coordinates(image_path, language)
                
                if ocr_result.get("text"):
                    result["text_content"] += f"\n\n--- Page {page_num + 1} (OCR) ---\n{ocr_result['text']}"
                
                # Add text regions with coordinates
                if "structured_text" in ocr_result:
                    for line in ocr_result["structured_text"]["lines"]:
                        for word in line:
                            region = PDFTextRegion(
                                text=word["text"],
                                bbox={
                                    "x0": word["bbox"]["x"],
                                    "y0": word["bbox"]["y"],
                                    "x1": word["bbox"]["x"] + word["bbox"]["width"],
                                    "y1": word["bbox"]["y"] + word["bbox"]["height"]
                                },
                                confidence=word["confidence"]
                            )
                            region.page_number = page_num
                            result["text_regions"].append(region.to_dict())
                
                # Clean up temporary image
                try:
                    os.remove(image_path)
                except:
                    pass
            
            return result
            
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            return {"text_content": "", "text_regions": [], "tables": []}

    async def _pdf_to_images(self, file_path: str, dpi: int = 200) -> List[str]:
        """Convert PDF pages to images for OCR"""
        images = []
        
        try:
            if PYMUPDF_AVAILABLE:
                doc = fitz.open(file_path)
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
                    
                    # Save to temporary file
                    temp_path = tempfile.mktemp(suffix=".png")
                    pix.save(temp_path)
                    images.append(temp_path)
                
                doc.close()
            else:
                # Fallback: use pdf2image if available
                try:
                    from pdf2image import convert_from_path
                    pil_images = convert_from_path(file_path, dpi=dpi)
                    
                    for i, pil_image in enumerate(pil_images):
                        temp_path = tempfile.mktemp(suffix=".png")
                        pil_image.save(temp_path, "PNG")
                        images.append(temp_path)
                        
                except ImportError:
                    logger.warning("pdf2image not available, cannot convert PDF to images")
            
        except Exception as e:
            logger.error(f"PDF to image conversion failed: {e}")
        
        return images

    def _should_use_ocr_fallback(self, data: Dict[str, Any]) -> bool:
        """Determine if OCR fallback should be used based on extraction quality"""
        text_content = data.get("text_content", "")
        
        # Check for low text extraction quality indicators
        indicators = [
            len(text_content.strip()) < 100,  # Very little text extracted
            "�" in text_content,  # Unicode errors
            text_content.count(" ") / len(text_content) > 0.9 if text_content else False,  # Too many spaces
        ]
        
        return any(indicators)

    def _merge_extraction_results(self, primary_result: Dict[str, Any], ocr_result: Dict[str, Any]) -> Dict[str, Any]:
        """Merge results from text extraction and OCR"""
        merged = primary_result.copy()
        
        # Prefer OCR text if it's significantly better
        ocr_text = ocr_result.get("text_content", "").strip()
        primary_text = primary_result.get("text_content", "").strip()
        
        if len(ocr_text) > len(primary_text) * 1.5:
            merged["text_content"] = ocr_text
            merged["text_regions"] = ocr_result.get("text_regions", [])
        else:
            # Combine both results
            merged["text_content"] += "\n\n[OCR Enhancement]\n" + ocr_text
            merged["text_regions"].extend(ocr_result.get("text_regions", []))
        
        return merged

    def _post_process_content(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Post-process extracted content"""
        try:
            # Clean up text content
            text_content = result.get("text_content", "")
            text_content = self._clean_extracted_text(text_content)
            result["text_content"] = text_content
            
            # Process tables
            tables = result.get("tables", [])
            processed_tables = []
            for table in tables:
                if isinstance(table, dict):
                    processed_table = self._process_table_data(table)
                    processed_tables.append(processed_table)
            result["tables"] = processed_tables
            
            # Create structured data
            result["structured_data"] = self._create_structured_data(result)
            
        except Exception as e:
            logger.error(f"Post-processing failed: {e}")
        
        return result

    def _clean_extracted_text(self, text: str) -> str:
        """Clean up extracted text"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        import re
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common OCR errors
        text = text.replace(' l ', ' I ')  # Common confusion
        text = text.replace(' O ', ' 0 ')  # Common confusion
        
        # Remove page break markers
        text = re.sub(r'--- Page \d+ ---', '', text)
        
        return text.strip()

    def _process_table_data(self, table: Dict[str, Any]) -> Dict[str, Any]:
        """Process and clean table data"""
        try:
            if "data" in table:
                data = table["data"]
            elif "headers" in table and "rows" in table:
                data = [table["headers"]] + table["rows"]
            else:
                return table
            
            # Clean table data
            cleaned_data = []
            for row in data:
                cleaned_row = []
                for cell in row:
                    if cell is None:
                        cleaned_row.append("")
                    else:
                        cleaned_cell = str(cell).strip()
                        # Clean up common extraction errors
                        cleaned_cell = cleaned_cell.replace('\n', ' ')
                        cleaned_row.append(cleaned_cell)
                cleaned_data.append(cleaned_row)
            
            # Update table with cleaned data
            table["data"] = cleaned_data
            if cleaned_data:
                table["headers"] = cleaned_data[0]
                table["rows"] = cleaned_data[1:]
            
            return table
            
        except Exception as e:
            logger.error(f"Table processing failed: {e}")
            return table

    def _create_structured_data(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create structured data from extraction results"""
        structured_data = []
        
        # Add tables
        for table in result.get("tables", []):
            structured_data.append({
                "type": "table",
                "source": "pdf_extraction",
                **table
            })
        
        # Add text regions as structured content
        text_regions = result.get("text_regions", [])
        if text_regions:
            # Group regions by page
            pages = {}
            for region in text_regions:
                page_num = region.get("page", 0)
                if page_num not in pages:
                    pages[page_num] = []
                pages[page_num].append(region)
            
            for page_num, regions in pages.items():
                # Sort regions by reading order
                regions.sort(key=lambda r: (r["bbox"]["y0"], r["bbox"]["x0"]))
                
                structured_data.append({
                    "type": "text_page",
                    "page": page_num,
                    "regions": regions,
                    "text": " ".join([r["text"] for r in regions])
                })
        
        return structured_data

    def _extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract PDF metadata"""
        try:
            metadata = {"file_type": "pdf"}
            
            # Try PyMuPDF for metadata
            if PYMUPDF_AVAILABLE:
                doc = fitz.open(file_path)
                metadata.update({
                    "page_count": doc.page_count,
                    "metadata": doc.metadata,
                    "pdf_version": doc.pdf_version,
                    "is_pdf": True
                })
                doc.close()
            
            # Try pdfplumber for additional metadata
            elif PDFPLUMBER_AVAILABLE:
                with pdfplumber.open(file_path) as pdf:
                    metadata.update({
                        "page_count": len(pdf.pages),
                        "metadata": pdf.metadata or {}
                    })
            
            return metadata
            
        except Exception as e:
            logger.error(f"Metadata extraction failed: {e}")
            return {"file_type": "pdf", "error": str(e)}
