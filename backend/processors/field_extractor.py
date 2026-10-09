"""
Field extractor for intelligent data extraction from documents
Combines OCR, layout analysis, and template matching for accurate field extraction
"""

import logging
import re
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass
from datetime import datetime
import json

from processors.enhanced_pdf_processor import EnhancedPDFProcessor
from processors.layout_analyzer import LayoutAnalyzer, DocumentTemplate
from processors.ocr_processor import get_ocr_processor

logger = logging.getLogger(__name__)


@dataclass
class ExtractedField:
    """Represents an extracted field with confidence and metadata"""
    name: str
    value: str
    confidence: float
    source: str  # ocr, text_extraction, template_match
    bbox: Optional[Dict[str, float]] = None
    page_number: int = 0
    validation_errors: List[str] = None
    
    def __post_init__(self):
        if self.validation_errors is None:
            self.validation_errors = []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "confidence": self.confidence,
            "source": self.source,
            "bbox": self.bbox,
            "page": self.page_number,
            "validation_errors": self.validation_errors
        }


@dataclass
class ExtractedTable:
    """Represents an extracted table with validation"""
    headers: List[str]
    rows: List[List[str]]
    confidence: float
    bbox: Optional[Dict[str, float]] = None
    page_number: int = 0
    table_type: str = "unknown"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "headers": self.headers,
            "rows": self.rows,
            "confidence": self.confidence,
            "bbox": self.bbox,
            "page": self.page_number,
            "table_type": self.table_type,
            "row_count": len(self.rows),
            "column_count": len(self.headers)
        }


@dataclass
class ExtractionResult:
    """Complete extraction result with all fields and metadata"""
    document_type: str
    template_match: Optional[Dict[str, Any]]
    fields: List[ExtractedField]
    tables: List[ExtractedTable]
    confidence_score: float
    processing_time: float
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_type": self.document_type,
            "template_match": self.template_match,
            "fields": [field.to_dict() for field in self.fields],
            "tables": [table.to_dict() for table in self.tables],
            "confidence_score": self.confidence_score,
            "processing_time": self.processing_time,
            "errors": self.errors,
            "field_count": len(self.fields),
            "table_count": len(self.tables)
        }


class FieldExtractor:
    """Intelligent field extraction system"""
    
    def __init__(self):
        self.pdf_processor = EnhancedPDFProcessor()
        self.layout_analyzer = LayoutAnalyzer()
        self.ocr_processor = get_ocr_processor()
        
        # Configuration
        self.min_field_confidence = 0.5
        self.min_table_confidence = 0.6
        
        # Field processors
        self.field_processors = {
            "currency": self._process_currency_field,
            "date": self._process_date_field,
            "number": self._process_number_field,
            "phone": self._process_phone_field,
            "email": self._process_email_field,
            "tax_code": self._process_tax_code_field,
            "vehicle_plate": self._process_vehicle_plate_field
        }
    
    async def extract_fields(self, file_path: str, document_type: str = None, options: Dict[str, Any] = None) -> ExtractionResult:
        """
        Extract fields from document using multi-engine approach
        
        Args:
            file_path: Path to the document
            document_type: Optional document type hint
            options: Processing options
            
        Returns:
            ExtractionResult with all extracted data
        """
        import time
        start_time = time.time()
        
        try:
            options = options or {}
            language = options.get("language", "vie")
            
            logger.info(f"Starting field extraction for: {file_path}")
            
            # Step 1: Process document with enhanced PDF processor
            pdf_result = await self.pdf_processor.process(file_path, options)
            
            # Step 2: Analyze layout
            layout_result = await self.layout_analyzer.analyze_document_layout(pdf_result)
            
            # Step 3: Determine document type and template
            template_match = self._determine_document_type(layout_result, document_type)
            
            # Step 4: Extract fields using template matching
            template_fields = self._extract_fields_with_template(pdf_result, layout_result, template_match)
            
            # Step 5: Extract fields using pattern matching
            pattern_fields = self._extract_fields_with_patterns(pdf_result, layout_result)
            
            # Step 6: Extract and validate tables
            tables = self._extract_and_validate_tables(pdf_result, layout_result, template_match)
            
            # Step 7: Merge and deduplicate fields
            merged_fields = self._merge_fields(template_fields, pattern_fields)
            
            # Step 8: Apply post-processing and validation
            processed_fields = self._post_process_fields(merged_fields, template_match)
            
            # Step 9: Calculate overall confidence
            confidence_score = self._calculate_overall_confidence(processed_fields, tables, template_match)
            
            # Step 10: Create result
            processing_time = time.time() - start_time
            
            result = ExtractionResult(
                document_type=template_match.get("document_type", "unknown") if template_match else "unknown",
                template_match=template_match,
                fields=processed_fields,
                tables=tables,
                confidence_score=confidence_score,
                processing_time=processing_time
            )
            
            logger.info(f"Field extraction completed in {processing_time:.2f}s with confidence {confidence_score:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Field extraction failed: {e}", exc_info=True)
            processing_time = time.time() - start_time
            return ExtractionResult(
                document_type="unknown",
                template_match=None,
                fields=[],
                tables=[],
                confidence_score=0.0,
                processing_time=processing_time,
                errors=[str(e)]
            )
    
    def _determine_document_type(self, layout_result: Dict[str, Any], document_type_hint: str = None) -> Optional[Dict[str, Any]]:
        """Determine document type using template matching and heuristics"""
        # Use hint if provided
        if document_type_hint:
            return {
                "document_type": document_type_hint,
                "source": "hint",
                "confidence": 0.8
            }
        
        # Use template matching from layout analyzer
        template_match = layout_result.get("template_match", {})
        if template_match.get("best_match"):
            best_match = template_match["best_match"]
            return {
                "document_type": best_match["document_type"],
                "template_name": best_match["template_name"],
                "confidence": best_match["match_score"],
                "source": "template_match"
            }
        
        # Use heuristics based on content
        heuristics = self._apply_document_type_heuristics(layout_result)
        if heuristics:
            return heuristics
        
        return None
    
    def _apply_document_type_heuristics(self, layout_result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Apply heuristics to determine document type"""
        text_content = ""
        
        # Collect all text from regions
        for page in layout_result.get("pages", []):
            for region in page.get("regions", []):
                if region.get("type") == "text_group":
                    text_content += region["content"]["text"].lower() + " "
                elif region.get("type") == "text_region":
                    text_content += region["content"]["text"].lower() + " "
        
        # Check for invoice indicators
        invoice_keywords = ["hóa đơn", "invoice", "thành tiền", "tổng cộng", "thuế gtgt"]
        if sum(1 for keyword in invoice_keywords if keyword in text_content) >= 2:
            return {
                "document_type": "invoice",
                "confidence": 0.7,
                "source": "heuristics"
            }
        
        # Check for contract indicators
        contract_keywords = ["hợp đồng", "contract", "bên a", "bên b", "thỏa thuận"]
        if sum(1 for keyword in contract_keywords if keyword in text_content) >= 2:
            return {
                "document_type": "contract",
                "confidence": 0.7,
                "source": "heuristics"
            }
        
        # Check for shipping document indicators
        shipping_keywords = ["vận đơn", "bill of lading", "người gửi", "người nhận", "giao hàng"]
        if sum(1 for keyword in shipping_keywords if keyword in text_content) >= 2:
            return {
                "document_type": "shipping",
                "confidence": 0.7,
                "source": "heuristics"
            }
        
        return None
    
    def _extract_fields_with_template(self, pdf_result: Dict[str, Any], layout_result: Dict[str, Any], template_match: Optional[Dict[str, Any]]) -> List[ExtractedField]:
        """Extract fields using template matching"""
        if not template_match:
            return []
        
        fields = []
        template_name = template_match.get("template_name")
        
        if not template_name:
            return fields
        
        # Get template details
        template = self.layout_analyzer.templates.get(template_match.get("document_type"))
        if not template:
            return fields
        
        # Extract fields based on template regions
        for region_def in template.regions:
            if region_def.get("type") == "field":
                field = self._extract_single_field(pdf_result, layout_result, region_def, template_match.get("confidence", 1.0))
                if field:
                    fields.append(field)
            elif region_def.get("type") == "field_group":
                group_fields = self._extract_field_group(pdf_result, layout_result, region_def, template_match.get("confidence", 1.0))
                fields.extend(group_fields)
        
        return fields
    
    def _extract_single_field(self, pdf_result: Dict[str, Any], layout_result: Dict[str, Any], region_def: Dict[str, Any], template_confidence: float) -> Optional[ExtractedField]:
        """Extract a single field based on template definition"""
        field_name = region_def["name"]
        expected_bbox = region_def.get("bbox", {})
        patterns = region_def.get("text_patterns", [])
        
        # Get text regions from layout result
        text_regions = []
        for page in layout_result.get("pages", []):
            for region in page.get("regions", []):
                if region.get("type") == "text_region":
                    text_regions.append(region)
        
        # Find matching regions
        best_match = None
        best_score = 0
        
        for region in text_regions:
            text = region["content"]["text"]
            region_bbox = region["bbox"]
            
            # Check pattern matches
            pattern_score = 0
            matched_value = text
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    pattern_score = 1.0
                    if match.groups():
                        matched_value = match.group(1)
                    break
            
            # Check position match
            position_score = self._calculate_position_score(region_bbox, expected_bbox)
            
            # Calculate overall score
            overall_score = (pattern_score * 0.7 + position_score * 0.3) * template_confidence
            
            if overall_score > best_score and overall_score >= self.min_field_confidence:
                best_score = overall_score
                best_match = ExtractedField(
                    name=field_name,
                    value=matched_value.strip(),
                    confidence=overall_score,
                    source="template_match",
                    bbox=region_bbox,
                    page_number=region.get("page", 0)
                )
        
        return best_match
    
    def _extract_field_group(self, pdf_result: Dict[str, Any], layout_result: Dict[str, Any], region_def: Dict[str, Any], template_confidence: float) -> List[ExtractedField]:
        """Extract fields from a field group"""
        fields = []
        sub_fields = region_def.get("sub_fields", [])
        group_bbox = region_def.get("bbox", {})
        
        # Get text regions within group area
        group_regions = self._get_regions_in_area(layout_result, group_bbox)
        
        for sub_field_def in sub_fields:
            sub_field = self._extract_single_field_from_regions(
                group_regions, sub_field_def, template_confidence
            )
            if sub_field:
                fields.append(sub_field)
        
        return fields
    
    def _get_regions_in_area(self, layout_result: Dict[str, Any], bbox: Dict[str, float]) -> List[Dict[str, Any]]:
        """Get text regions within a specific area"""
        regions_in_area = []
        
        for page in layout_result.get("pages", []):
            for region in page.get("regions", []):
                if region.get("type") == "text_region":
                    region_bbox = region["bbox"]
                    if self._bbox_intersects(region_bbox, bbox):
                        regions_in_area.append(region)
        
        return regions_in_area
    
    def _bbox_intersects(self, bbox1: Dict[str, float], bbox2: Dict[str, float]) -> bool:
        """Check if two bounding boxes intersect"""
        return not (bbox1["x1"] < bbox2["x0"] or bbox1["x0"] > bbox2["x1"] or
                   bbox1["y1"] < bbox2["y0"] or bbox1["y0"] > bbox2["y1"])
    
    def _calculate_position_score(self, region_bbox: Dict[str, float], expected_bbox: Dict[str, float]) -> float:
        """Calculate position matching score"""
        if not expected_bbox:
            return 1.0
        
        # Simple overlap calculation
        overlap = self._calculate_bbox_overlap(region_bbox, expected_bbox)
        return overlap
    
    def _calculate_bbox_overlap(self, bbox1: Dict[str, float], bbox2: Dict[str, float]) -> float:
        """Calculate overlap ratio between two bounding boxes"""
        # Calculate intersection
        x0 = max(bbox1["x0"], bbox2["x0"])
        y0 = max(bbox1["y0"], bbox2["y0"])
        x1 = min(bbox1["x1"], bbox2["x1"])
        y1 = min(bbox1["y1"], bbox2["y1"])
        
        if x1 <= x0 or y1 <= y0:
            return 0.0
        
        intersection_area = (x1 - x0) * (y1 - y0)
        
        # Calculate union
        area1 = (bbox1["x1"] - bbox1["x0"]) * (bbox1["y1"] - bbox1["y0"])
        area2 = (bbox2["x1"] - bbox2["x0"]) * (bbox2["y1"] - bbox2["y0"])
        union_area = area1 + area2 - intersection_area
        
        return intersection_area / union_area if union_area > 0 else 0.0
    
    def _extract_single_field_from_regions(self, regions: List[Dict[str, Any]], field_def: Dict[str, Any], template_confidence: float) -> Optional[ExtractedField]:
        """Extract a single field from a list of regions"""
        field_name = field_def["name"]
        patterns = field_def.get("patterns", [])
        
        best_match = None
        best_score = 0
        
        for region in regions:
            text = region["content"]["text"]
            
            # Check patterns
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    score = template_confidence
                    value = match.group(1) if match.groups() else text
                    
                    if score > best_score:
                        best_score = score
                        best_match = ExtractedField(
                            name=field_name,
                            value=value.strip(),
                            confidence=score,
                            source="template_match",
                            bbox=region["bbox"],
                            page_number=region.get("page", 0)
                        )
                    break
        
        return best_match
    
    def _extract_fields_with_patterns(self, pdf_result: Dict[str, Any], layout_result: Dict[str, Any]) -> List[ExtractedField]:
        """Extract fields using pattern matching without templates"""
        # Get field regions from layout analysis
        field_regions = layout_result.get("field_regions", [])
        
        fields = []
        for field_region in field_regions:
            field = ExtractedField(
                name=field_region["field_name"],
                value=field_region["value"],
                confidence=field_region["confidence"],
                source="pattern_match",
                bbox=field_region["bbox"],
                page_number=field_region["page"]
            )
            fields.append(field)
        
        return fields
    
    def _extract_and_validate_tables(self, pdf_result: Dict[str, Any], layout_result: Dict[str, Any], template_match: Optional[Dict[str, Any]]) -> List[ExtractedTable]:
        """Extract and validate tables from document"""
        tables = []
        
        # Get tables from PDF processing result
        pdf_tables = pdf_result.get("tables", [])
        
        for table_data in pdf_tables:
            # Determine table type based on headers
            table_type = self._determine_table_type(table_data.get("headers", []))
            
            # Validate table structure
            validation_score = self._validate_table_structure(table_data, template_match)
            
            if validation_score >= self.min_table_confidence:
                table = ExtractedTable(
                    headers=table_data.get("headers", []),
                    rows=table_data.get("rows", []),
                    confidence=validation_score,
                    bbox=table_data.get("bbox"),
                    page_number=table_data.get("page", 0),
                    table_type=table_type
                )
                tables.append(table)
        
        return tables
    
    def _determine_table_type(self, headers: List[str]) -> str:
        """Determine table type based on headers"""
        if not headers:
            return "unknown"
        
        headers_text = " ".join(headers).lower()
        
        if any(keyword in headers_text for keyword in ["stt", "tên hàng", "số lượng", "đơn giá", "thành tiền"]):
            return "invoice_items"
        elif any(keyword in headers_text for keyword in ["no.", "description", "quantity", "amount"]):
            return "contract_items"
        elif any(keyword in headers_text for keyword in ["stt", "mô tả", "trọng lượng", "ghi chú"]):
            return "shipping_items"
        
        return "general"
    
    def _validate_table_structure(self, table_data: Dict[str, Any], template_match: Optional[Dict[str, Any]]) -> float:
        """Validate table structure and return confidence score"""
        score = 0.5  # Base score
        
        headers = table_data.get("headers", [])
        rows = table_data.get("rows", [])
        
        # Check if we have headers and rows
        if headers and rows:
            score += 0.2
        
        # Check header consistency
        if headers and all(len(row) == len(headers) for row in rows):
            score += 0.2
        
        # Check for empty rows
        if rows:
            non_empty_rows = sum(1 for row in rows if any(cell.strip() for cell in row))
            if non_empty_rows / len(rows) > 0.8:
                score += 0.1
        
        return min(score, 1.0)
    
    def _merge_fields(self, template_fields: List[ExtractedField], pattern_fields: List[ExtractedField]) -> List[ExtractedField]:
        """Merge and deduplicate fields from different extraction methods"""
        all_fields = template_fields + pattern_fields
        
        # Group by field name
        field_groups = {}
        for field in all_fields:
            if field.name not in field_groups:
                field_groups[field.name] = []
            field_groups[field.name].append(field)
        
        # Select best field for each name
        merged_fields = []
        for field_name, fields in field_groups.items():
            if len(fields) == 1:
                merged_fields.append(fields[0])
            else:
                # Select field with highest confidence
                best_field = max(fields, key=lambda f: f.confidence)
                
                # Merge values if they're different
                unique_values = list(set(f.value for f in fields if f.value.strip()))
                if len(unique_values) > 1:
                    best_field.value = f"MERGED: {'; '.join(unique_values)}"
                    best_field.confidence *= 0.8  # Reduce confidence for merged fields
                
                merged_fields.append(best_field)
        
        return merged_fields
    
    def _post_process_fields(self, fields: List[ExtractedField], template_match: Optional[Dict[str, Any]]) -> List[ExtractedField]:
        """Apply post-processing rules and validation"""
        processed_fields = []
        
        for field in fields:
            # Determine field type for processing
            field_type = self._determine_field_type(field.name, template_match)
            
            # Apply field-specific processing
            if field_type in self.field_processors:
                field = self.field_processors[field_type](field)
            
            # Apply validation
            field = self._validate_field(field, template_match)
            
            processed_fields.append(field)
        
        return processed_fields
    
    def _determine_field_type(self, field_name: str, template_match: Optional[Dict[str, Any]]) -> str:
        """Determine field type for processing"""
        field_type_mapping = {
            "total_amount": "currency",
            "unit_price": "currency",
            "amount": "currency",
            "subtotal": "currency",
            "vat_amount": "currency",
            "invoice_date": "date",
            "contract_date": "date",
            "shipping_date": "date",
            "phone": "phone",
            "seller_phone": "phone",
            "consignee_phone": "phone",
            "email": "email",
            "tax_code": "tax_code",
            "vehicle_number": "vehicle_plate",
            "quantity": "number",
            "total_weight": "number",
            "total_quantity": "number"
        }
        
        return field_type_mapping.get(field_name, "text")
    
    def _process_currency_field(self, field: ExtractedField) -> ExtractedField:
        """Process currency field"""
        # Extract numeric value
        pattern = r'([0-9.,]+)'
        match = re.search(pattern, field.value)
        
        if match:
            numeric_value = match.group(1).replace(',', '')
            try:
                # Convert to float and back to string for consistency
                value = float(numeric_value)
                field.value = f"{value:,.2f}"
            except ValueError:
                pass
        
        return field
    
    def _process_date_field(self, field: ExtractedField) -> ExtractedField:
        """Process date field and normalize format"""
        date_patterns = [
            r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})',
            r'(\d{1,2})\s*(tháng|month)\s*(\d{1,2})\s*(năm|year)\s*(\d{4})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, field.value, re.IGNORECASE)
            if match:
                try:
                    if len(match.groups()) == 3:
                        day, month, year = match.groups()
                    elif len(match.groups()) == 4:
                        day, month, _, year = match.groups()
                    else:
                        day, month, _, _, year = match.groups()
                    
                    # Normalize year
                    if len(year) == 2:
                        year = f"20{year}"
                    
                    # Create normalized date
                    field.value = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    break
                    
                except (ValueError, IndexError):
                    continue
        
        return field
    
    def _process_number_field(self, field: ExtractedField) -> ExtractedField:
        """Process numeric field"""
        # Extract numeric value
        pattern = r'([0-9.,]+)'
        match = re.search(pattern, field.value)
        
        if match:
            numeric_value = match.group(1).replace(',', '')
            try:
                value = float(numeric_value)
                field.value = str(value)
            except ValueError:
                pass
        
        return field
    
    def _process_phone_field(self, field: ExtractedField) -> ExtractedField:
        """Process phone field"""
        # Extract phone number pattern
        pattern = r'([0-9\s\-\+\(\)]{7,})'
        match = re.search(pattern, field.value)
        
        if match:
            # Clean phone number
            phone = re.sub(r'[^\d+]', '', match.group(1))
            field.value = phone
        
        return field
    
    def _process_email_field(self, field: ExtractedField) -> ExtractedField:
        """Process email field"""
        # Extract email pattern
        pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        match = re.search(pattern, field.value)
        
        if match:
            field.value = match.group(1).lower()
        
        return field
    
    def _process_tax_code_field(self, field: ExtractedField) -> ExtractedField:
        """Process tax code field"""
        # Extract tax code pattern (10 digits or 13 digits with dashes)
        pattern = r'([0-9-]{10,13})'
        match = re.search(pattern, field.value)
        
        if match:
            tax_code = match.group(1).replace('-', '')
            if len(tax_code) == 10:
                field.value = f"{tax_code[:2]}-{tax_code[2:4]}-{tax_code[4:]}"
            else:
                field.value = tax_code
        
        return field
    
    def _process_vehicle_plate_field(self, field: ExtractedField) -> ExtractedField:
        """Process vehicle plate field"""
        # Standardize Vietnamese plate format
        pattern = r'([0-9]{2}[A-Z]-[0-9]{3,4}\.[0-9]{2})'
        match = re.search(pattern, field.value.upper())
        
        if match:
            field.value = match.group(1)
        
        return field
    
    def _validate_field(self, field: ExtractedField, template_match: Optional[Dict[str, Any]]) -> ExtractedField:
        """Validate field value and add validation errors"""
        # Basic validation rules
        if not field.value or not field.value.strip():
            field.validation_errors.append("Empty value")
            field.confidence *= 0.5
        
        # Check confidence threshold
        if field.confidence < self.min_field_confidence:
            field.validation_errors.append(f"Low confidence: {field.confidence:.2f}")
        
        return field
    
    def _calculate_overall_confidence(self, fields: List[ExtractedField], tables: List[ExtractedTable], template_match: Optional[Dict[str, Any]]) -> float:
        """Calculate overall extraction confidence score"""
        if not fields and not tables:
            return 0.0
        
        # Field confidence
        field_confidence = sum(f.confidence for f in fields) / len(fields) if fields else 0
        
        # Table confidence
        table_confidence = sum(t.confidence for t in tables) / len(tables) if tables else 0
        
        # Template match confidence
        template_confidence = template_match.get("confidence", 0.5) if template_match else 0.5
        
        # Weighted average
        weights = {
            "fields": 0.4,
            "tables": 0.3,
            "template": 0.3
        }
        
        overall_score = (
            field_confidence * weights["fields"] +
            table_confidence * weights["tables"] +
            template_confidence * weights["template"]
        )
        
        return min(overall_score, 1.0)


# Global field extractor instance
_field_extractor = None

def get_field_extractor() -> FieldExtractor:
    """Get global field extractor instance"""
    global _field_extractor
    if _field_extractor is None:
        _field_extractor = FieldExtractor()
    return _field_extractor
