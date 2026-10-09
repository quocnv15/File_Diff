"""
Layout analyzer for coordinate-based field extraction from PDFs
Provides intelligent document structure analysis and field region detection
"""

import logging
import json
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass
from pathlib import Path
import re

import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class BoundingBox:
    """Represents a bounding box with coordinates"""
    x0: float
    y0: float
    x1: float
    y1: float
    
    def width(self) -> float:
        return self.x1 - self.x0
    
    def height(self) -> float:
        return self.y1 - self.y0
    
    def area(self) -> float:
        return self.width() * self.height()
    
    def center(self) -> Tuple[float, float]:
        return ((self.x0 + self.x1) / 2, (self.y0 + self.y1) / 2)
    
    def contains(self, x: float, y: float) -> bool:
        return self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1
    
    def intersects(self, other: 'BoundingBox') -> bool:
        return not (self.x1 < other.x0 or self.x0 > other.x1 or 
                   self.y1 < other.y0 or self.y0 > other.y1)
    
    def union(self, other: 'BoundingBox') -> 'BoundingBox':
        return BoundingBox(
            min(self.x0, other.x0),
            min(self.y0, other.y0),
            max(self.x1, other.x1),
            max(self.y1, other.y1)
        )
    
    def to_dict(self) -> Dict[str, float]:
        return {"x0": self.x0, "y0": self.y0, "x1": self.x1, "y1": self.y1}


@dataclass
class TextRegion:
    """Represents a text region with coordinates and content"""
    text: str
    bbox: BoundingBox
    confidence: float = 1.0
    page_number: int = 0
    font_size: Optional[float] = None
    is_bold: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "bbox": self.bbox.to_dict(),
            "confidence": self.confidence,
            "page": self.page_number,
            "font_size": self.font_size,
            "is_bold": self.is_bold
        }


@dataclass
class TableRegion:
    """Represents a table region with structure"""
    bbox: BoundingBox
    headers: List[str]
    rows: List[List[str]]
    page_number: int = 0
    confidence: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "bbox": self.bbox.to_dict(),
            "headers": self.headers,
            "rows": self.rows,
            "page": self.page_number,
            "confidence": self.confidence,
            "row_count": len(self.rows),
            "column_count": len(self.headers)
        }


@dataclass
class DocumentTemplate:
    """Represents a document template with field definitions"""
    name: str
    document_type: str
    version: str
    confidence_threshold: float
    regions: List[Dict[str, Any]]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DocumentTemplate':
        return cls(
            name=data["name"],
            document_type=data["document_type"],
            version=data["version"],
            confidence_threshold=data["confidence_threshold"],
            regions=data["regions"]
        )


class LayoutAnalyzer:
    """Analyzes document layout and extracts structured information"""
    
    def __init__(self):
        self.templates_dir = Path(__file__).parent.parent / "templates" / "pdf_templates"
        self.templates = {}
        self.load_templates()
        
        # Configuration
        self.line_height_threshold = 5  # Pixels
        self.column_gap_threshold = 50   # Pixels
        self.min_region_confidence = 0.7
        
    def load_templates(self):
        """Load document templates from templates directory"""
        try:
            if self.templates_dir.exists():
                for template_file in self.templates_dir.glob("*.json"):
                    with open(template_file, 'r', encoding='utf-8') as f:
                        template_data = json.load(f)
                        template = DocumentTemplate.from_dict(template_data)
                        self.templates[template.document_type] = template
                        logger.info(f"Loaded template: {template.name}")
        except Exception as e:
            logger.error(f"Failed to load templates: {e}")
    
    async def analyze_document_layout(self, extraction_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze document layout and structure
        
        Args:
            extraction_result: Result from enhanced PDF processor
            
        Returns:
            Dictionary with layout analysis results
        """
        try:
            # Extract text regions and tables
            text_regions = self._extract_text_regions(extraction_result)
            tables = self._extract_tables(extraction_result)
            
            # Analyze document structure
            layout_info = {
                "pages": self._analyze_pages(text_regions, tables),
                "regions": self._identify_regions(text_regions, tables),
                "columns": self._detect_columns(text_regions),
                "reading_order": self._determine_reading_order(text_regions),
                "template_match": self._match_template(text_regions, tables),
                "field_regions": self._identify_field_regions(text_regions)
            }
            
            return layout_info
            
        except Exception as e:
            logger.error(f"Layout analysis failed: {e}")
            return {"error": str(e)}
    
    def _extract_text_regions(self, extraction_result: Dict[str, Any]) -> List[TextRegion]:
        """Extract text regions from extraction result"""
        regions = []
        
        for region_data in extraction_result.get("text_regions", []):
            bbox = BoundingBox(
                x0=region_data["bbox"]["x0"],
                y0=region_data["bbox"]["y0"],
                x1=region_data["bbox"]["x1"],
                y1=region_data["bbox"]["y1"]
            )
            
            region = TextRegion(
                text=region_data["text"],
                bbox=bbox,
                confidence=region_data.get("confidence", 1.0),
                page_number=region_data.get("page", 0),
                font_size=region_data.get("font_size"),
                is_bold=region_data.get("is_bold", False)
            )
            regions.append(region)
        
        return regions
    
    def _extract_tables(self, extraction_result: Dict[str, Any]) -> List[TableRegion]:
        """Extract table regions from extraction result"""
        tables = []
        
        for table_data in extraction_result.get("tables", []):
            bbox = BoundingBox(
                x0=table_data["bbox"]["x0"],
                y0=table_data["bbox"]["y0"],
                x1=table_data["bbox"]["x1"],
                y1=table_data["bbox"]["y1"]
            )
            
            table = TableRegion(
                bbox=bbox,
                headers=table_data.get("headers", []),
                rows=table_data.get("rows", []),
                page_number=table_data.get("page", 0),
                confidence=table_data.get("confidence", 1.0)
            )
            tables.append(table)
        
        return tables
    
    def _analyze_pages(self, text_regions: List[TextRegion], tables: List[TableRegion]) -> List[Dict[str, Any]]:
        """Analyze each page separately"""
        pages = {}
        
        # Group regions by page
        for region in text_regions:
            page_num = region.page_number
            if page_num not in pages:
                pages[page_num] = {"text_regions": [], "tables": []}
            pages[page_num]["text_regions"].append(region)
        
        for table in tables:
            page_num = table.page_number
            if page_num not in pages:
                pages[page_num] = {"text_regions": [], "tables": []}
            pages[page_num]["tables"].append(table)
        
        # Analyze each page
        page_analyses = []
        for page_num, content in sorted(pages.items()):
            analysis = self._analyze_single_page(content["text_regions"], content["tables"], page_num)
            page_analyses.append(analysis)
        
        return page_analyses
    
    def _analyze_single_page(self, text_regions: List[TextRegion], tables: List[TableRegion], page_num: int) -> Dict[str, Any]:
        """Analyze a single page"""
        try:
            # Determine page boundaries
            if not text_regions and not tables:
                return {"page": page_num, "empty": True}
            
            all_bbox = [region.bbox for region in text_regions] + [table.bbox for table in tables]
            page_bbox = self._calculate_page_bbox(all_bbox)
            
            # Analyze layout
            layout_info = {
                "page": page_num,
                "bbox": page_bbox.to_dict(),
                "text_regions_count": len(text_regions),
                "tables_count": len(tables),
                "text_density": len(text_regions) / page_bbox.area() if page_bbox.area() > 0 else 0,
                "has_tables": len(tables) > 0,
                "regions": self._classify_regions(text_regions),
                "columns": self._detect_page_columns(text_regions, page_bbox),
                "header_regions": self._identify_headers(text_regions),
                "footer_regions": self._identify_footers(text_regions, page_bbox)
            }
            
            return layout_info
            
        except Exception as e:
            logger.error(f"Page analysis failed for page {page_num}: {e}")
            return {"page": page_num, "error": str(e)}
    
    def _calculate_page_bbox(self, bboxes: List[BoundingBox]) -> BoundingBox:
        """Calculate bounding box for the entire page"""
        if not bboxes:
            return BoundingBox(0, 0, 0, 0)
        
        min_x0 = min(bbox.x0 for bbox in bboxes)
        min_y0 = min(bbox.y0 for bbox in bboxes)
        max_x1 = max(bbox.x1 for bbox in bboxes)
        max_y1 = max(bbox.y1 for bbox in bboxes)
        
        return BoundingBox(min_x0, min_y0, max_x1, max_y1)
    
    def _classify_regions(self, text_regions: List[TextRegion]) -> List[Dict[str, Any]]:
        """Classify text regions by type"""
        classified = []
        
        for region in text_regions:
            region_type = self._classify_region_type(region)
            classified.append({
                "text": region.text,
                "bbox": region.bbox.to_dict(),
                "type": region_type,
                "confidence": region.confidence
            })
        
        return classified
    
    def _classify_region_type(self, region: TextRegion) -> str:
        """Classify a text region by its content type"""
        text = region.text.strip()
        
        # Check for common Vietnamese field patterns
        field_patterns = {
            "invoice_number": r"^(số|hóa đơn|invoice).*[:：]\s*(.+)",
            "date": r"(ngày|date|năm).*[:：]\s*(.+)",
            "company_name": r"(công ty|company|tên).*[:：]\s*(.+)",
            "address": r"(địa chỉ|address).*[:：]\s*(.+)",
            "phone": r"(điện thoại|phone|sdt).*[:：]\s*(.+)",
            "tax_code": r"(mã số thuế|tax).*[:：]\s*(.+)",
            "total": r"(tổng|total|thành tiền).*[:：]\s*(.+)",
            "quantity": r"(số lượng|quantity|sl).*[:：]\s*(.+)",
            "unit_price": r"(đơn giá|unit price|price).*[:：]\s*(.+)",
            "amount": r"(thành tiền|amount).*[:：]\s*(.+)"
        }
        
        for field_type, pattern in field_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                return field_type
        
        # Check if it's a number
        if re.match(r"^[0-9.,]+$", text):
            return "number"
        
        # Check if it's a price/currency
        if re.search(r"[\d,.]+\s*(vnđ|usd|$|đ)", text, re.IGNORECASE):
            return "currency"
        
        # Check if it's a date
        if re.search(r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}", text):
            return "date"
        
        # Check if it's likely a header (short, capitalized, at top)
        if len(text) < 50 and region.bbox.y0 < 200 and (text.isupper() or text.title()):
            return "header"
        
        # Default classification
        if len(text) > 100:
            return "paragraph"
        elif len(text) > 20:
            return "sentence"
        else:
            return "label"
    
    def _detect_columns(self, text_regions: List[TextRegion]) -> List[Dict[str, Any]]:
        """Detect column layout in document"""
        if not text_regions:
            return []
        
        # Get x-coordinates of all text regions
        x_positions = [region.bbox.x0 for region in text_regions]
        
        # Find gaps that might indicate column breaks
        x_positions.sort()
        gaps = []
        for i in range(1, len(x_positions)):
            gap = x_positions[i] - x_positions[i-1]
            if gap > self.column_gap_threshold:
                gaps.append({"gap": gap, "position": x_positions[i]})
        
        # Define column boundaries
        columns = []
        if gaps:
            # Multiple columns detected
            start_x = min(region.bbox.x0 for region in text_regions)
            
            for i, gap in enumerate(gaps):
                end_x = gap["position"]
                column_regions = [r for r in text_regions if r.bbox.x0 >= start_x and r.bbox.x0 < end_x]
                
                if column_regions:
                    columns.append({
                        "column": i + 1,
                        "x_range": [start_x, end_x],
                        "regions": len(column_regions),
                        "width": end_x - start_x
                    })
                
                start_x = end_x
            
            # Add last column
            last_regions = [r for r in text_regions if r.bbox.x0 >= gaps[-1]["position"]]
            if last_regions:
                end_x = max(region.bbox.x1 for region in last_regions)
                columns.append({
                    "column": len(columns) + 1,
                    "x_range": [gaps[-1]["position"], end_x],
                    "regions": len(last_regions),
                    "width": end_x - gaps[-1]["position"]
                })
        else:
            # Single column
            min_x = min(region.bbox.x0 for region in text_regions)
            max_x = max(region.bbox.x1 for region in text_regions)
            columns.append({
                "column": 1,
                "x_range": [min_x, max_x],
                "regions": len(text_regions),
                "width": max_x - min_x
            })
        
        return columns
    
    def _detect_page_columns(self, text_regions: List[TextRegion], page_bbox: BoundingBox) -> List[Dict[str, Any]]:
        """Detect columns for a specific page"""
        return self._detect_columns(text_regions)
    
    def _identify_headers(self, text_regions: List[TextRegion]) -> List[Dict[str, Any]]:
        """Identify header regions"""
        headers = []
        
        # Sort by y-coordinate (top to bottom)
        sorted_regions = sorted(text_regions, key=lambda r: r.bbox.y0)
        
        # Look for regions at the top of the document
        for region in sorted_regions[:5]:  # Check first 5 regions
            if region.bbox.y0 < 200:  # Within 200 pixels from top
                if (len(region.text) < 100 and 
                    (region.text.isupper() or region.is_bold or 
                     any(keyword in region.text.lower() for keyword in ['hóa đơn', 'invoice', 'công ty', 'company']))):
                    headers.append({
                        "text": region.text,
                        "bbox": region.bbox.to_dict(),
                        "confidence": region.confidence,
                        "type": "header"
                    })
        
        return headers
    
    def _identify_footers(self, text_regions: List[TextRegion], page_bbox: BoundingBox) -> List[Dict[str, Any]]:
        """Identify footer regions"""
        footers = []
        page_bottom = page_bbox.y1
        
        # Look for regions at the bottom of the page
        for region in text_regions:
            if region.bbox.y1 > page_bottom - 150:  # Within 150 pixels from bottom
                if (len(region.text) < 200 and 
                    any(keyword in region.text.lower() for keyword in 
                        ['chữ ký', 'signature', 'người lập', 'giám đốc', 'director', 'kế toán', 'accountant'])):
                    footers.append({
                        "text": region.text,
                        "bbox": region.bbox.to_dict(),
                        "confidence": region.confidence,
                        "type": "footer"
                    })
        
        return footers
    
    def _identify_regions(self, text_regions: List[TextRegion], tables: List[TableRegion]) -> List[Dict[str, Any]]:
        """Identify different types of regions in the document"""
        regions = []
        
        # Add table regions
        for table in tables:
            regions.append({
                "type": "table",
                "bbox": table.bbox.to_dict(),
                "content": {
                    "headers": table.headers,
                    "rows": table.rows,
                    "row_count": len(table.rows),
                    "column_count": len(table.headers)
                },
                "confidence": table.confidence,
                "page": table.page_number
            })
        
        # Add text regions grouped by proximity
        text_groups = self._group_text_by_proximity(text_regions)
        
        for group in text_groups:
            if len(group) > 1:  # Only group multiple regions
                group_bbox = self._calculate_group_bbox(group)
                group_text = " ".join([region.text for region in group])
                
                regions.append({
                    "type": "text_group",
                    "bbox": group_bbox.to_dict(),
                    "content": {
                        "text": group_text,
                        "region_count": len(group),
                        "regions": [region.to_dict() for region in group]
                    },
                    "confidence": sum(region.confidence for region in group) / len(group),
                    "page": group[0].page_number
                })
            else:
                # Single regions
                region = group[0]
                regions.append({
                    "type": "text_region",
                    "bbox": region.bbox.to_dict(),
                    "content": {
                        "text": region.text
                    },
                    "confidence": region.confidence,
                    "page": region.page_number
                })
        
        return regions
    
    def _group_text_by_proximity(self, text_regions: List[TextRegion], max_distance: float = 50) -> List[List[TextRegion]]:
        """Group text regions by spatial proximity"""
        if not text_regions:
            return []
        
        # Sort by y-coordinate, then x-coordinate
        sorted_regions = sorted(text_regions, key=lambda r: (r.page_number, r.bbox.y0, r.bbox.x0))
        
        groups = []
        current_group = [sorted_regions[0]]
        
        for region in sorted_regions[1:]:
            # Check if region belongs to current group
            last_region = current_group[-1]
            
            # Same page and close enough
            if (region.page_number == last_region.page_number and
                abs(region.bbox.y0 - last_region.bbox.y0) < max_distance):
                current_group.append(region)
            else:
                # Start new group
                groups.append(current_group)
                current_group = [region]
        
        # Add last group
        groups.append(current_group)
        
        return groups
    
    def _calculate_group_bbox(self, regions: List[TextRegion]) -> BoundingBox:
        """Calculate bounding box for a group of regions"""
        if not regions:
            return BoundingBox(0, 0, 0, 0)
        
        min_x0 = min(region.bbox.x0 for region in regions)
        min_y0 = min(region.bbox.y0 for region in regions)
        max_x1 = max(region.bbox.x1 for region in regions)
        max_y1 = max(region.bbox.y1 for region in regions)
        
        return BoundingBox(min_x0, min_y0, max_x1, max_y1)
    
    def _determine_reading_order(self, text_regions: List[TextRegion]) -> List[Dict[str, Any]]:
        """Determine the reading order of text regions"""
        # Group by page first
        pages = {}
        for region in text_regions:
            page_num = region.page_number
            if page_num not in pages:
                pages[page_num] = []
            pages[page_num].append(region)
        
        ordered_regions = []
        
        for page_num in sorted(pages.keys()):
            page_regions = pages[page_num]
            
            # Sort by reading order: top to bottom, left to right
            page_regions.sort(key=lambda r: (r.bbox.y0, r.bbox.x0))
            
            for i, region in enumerate(page_regions):
                ordered_regions.append({
                    "order": len(ordered_regions) + 1,
                    "page": page_num,
                    "text": region.text,
                    "bbox": region.bbox.to_dict(),
                    "confidence": region.confidence
                })
        
        return ordered_regions
    
    def _match_template(self, text_regions: List[TextRegion], tables: List[TableRegion]) -> Dict[str, Any]:
        """Match document against known templates"""
        template_matches = []
        
        for template_name, template in self.templates.items():
            match_score = self._calculate_template_match(text_regions, tables, template)
            
            if match_score >= template.confidence_threshold:
                template_matches.append({
                    "template_name": template.name,
                    "document_type": template.document_type,
                    "version": template.version,
                    "match_score": match_score,
                    "confidence_threshold": template.confidence_threshold
                })
        
        # Sort by match score
        template_matches.sort(key=lambda m: m["match_score"], reverse=True)
        
        return {
            "matches": template_matches,
            "best_match": template_matches[0] if template_matches else None,
            "total_matches": len(template_matches)
        }
    
    def _calculate_template_match(self, text_regions: List[TextRegion], tables: List[TableRegion], template: DocumentTemplate) -> float:
        """Calculate how well a document matches a template"""
        try:
            score = 0.0
            total_checks = 0
            
            # Check expected regions
            for region_def in template.regions:
                total_checks += 1
                
                # Look for matching text regions
                matched_regions = self._find_matching_regions(text_regions, region_def)
                
                if matched_regions:
                    # Score based on confidence and position accuracy
                    best_match = max(matched_regions, key=lambda r: r.confidence)
                    position_score = self._calculate_position_accuracy(best_match, region_def)
                    region_score = (best_match.confidence + position_score) / 2
                    score += region_score
            
            # Check table expectations
            expected_tables = len([r for r in template.regions if r.get("type") == "table"])
            actual_tables = len(tables)
            
            if expected_tables > 0:
                total_checks += 1
                table_score = min(actual_tables / expected_tables, 1.0)
                score += table_score
            
            return score / total_checks if total_checks > 0 else 0.0
            
        except Exception as e:
            logger.error(f"Template matching failed: {e}")
            return 0.0
    
    def _find_matching_regions(self, text_regions: List[TextRegion], region_def: Dict[str, Any]) -> List[TextRegion]:
        """Find text regions that match a template region definition"""
        matches = []
        
        # Extract expected text patterns
        expected_patterns = region_def.get("text_patterns", [])
        expected_type = region_def.get("field_type")
        expected_bbox = region_def.get("bbox", {})
        
        for region in text_regions:
            # Check text pattern matches
            pattern_match = True
            if expected_patterns:
                pattern_match = any(
                    re.search(pattern, region.text, re.IGNORECASE)
                    for pattern in expected_patterns
                )
            
            # Check field type match
            type_match = True
            if expected_type:
                region_type = self._classify_region_type(region)
                type_match = region_type == expected_type
            
            # Check position match (if bbox is specified)
            position_match = True
            if expected_bbox:
                position_match = self._check_position_match(region.bbox, expected_bbox)
            
            if pattern_match and type_match and position_match:
                matches.append(region)
        
        return matches
    
    def _calculate_position_accuracy(self, region: TextRegion, region_def: Dict[str, Any]) -> float:
        """Calculate how well a region matches expected position"""
        expected_bbox = region_def.get("bbox", {})
        
        if not expected_bbox:
            return 1.0
        
        # Calculate overlap with expected position
        exp_bbox = BoundingBox(
            expected_bbox.get("x0", 0),
            expected_bbox.get("y0", 0),
            expected_bbox.get("x1", 100),
            expected_bbox.get("y1", 100)
        )
        
        # Calculate intersection over union
        intersection_bbox = self._calculate_intersection(region.bbox, exp_bbox)
        union_bbox = region.bbox.union(exp_bbox)
        
        if union_bbox.area() == 0:
            return 0.0
        
        iou = intersection_bbox.area() / union_bbox.area()
        return iou
    
    def _calculate_intersection(self, bbox1: BoundingBox, bbox2: BoundingBox) -> BoundingBox:
        """Calculate intersection of two bounding boxes"""
        if not bbox1.intersects(bbox2):
            return BoundingBox(0, 0, 0, 0)
        
        return BoundingBox(
            max(bbox1.x0, bbox2.x0),
            max(bbox1.y0, bbox2.y0),
            min(bbox1.x1, bbox2.x1),
            min(bbox1.y1, bbox2.y1)
        )
    
    def _check_position_match(self, bbox: BoundingBox, expected_bbox: Dict[str, Any]) -> bool:
        """Check if a bounding box matches expected position"""
        tolerance = 50  # Pixels tolerance
        
        exp_x0 = expected_bbox.get("x0")
        exp_y0 = expected_bbox.get("y0")
        exp_x1 = expected_bbox.get("x1")
        exp_y1 = expected_bbox.get("y1")
        
        # Check if bbox is within tolerance of expected position
        if exp_x0 is not None and abs(bbox.x0 - exp_x0) > tolerance:
            return False
        if exp_y0 is not None and abs(bbox.y0 - exp_y0) > tolerance:
            return False
        if exp_x1 is not None and abs(bbox.x1 - exp_x1) > tolerance:
            return False
        if exp_y1 is not None and abs(bbox.y1 - exp_y1) > tolerance:
            return False
        
        return True
    
    def _identify_field_regions(self, text_regions: List[TextRegion]) -> List[Dict[str, Any]]:
        """Identify specific field regions for data extraction"""
        field_regions = []
        
        # Common Vietnamese field patterns
        field_patterns = {
            "invoice_number": [
                r"số\s*hóa\s*don[:：]\s*(.+)",
                r"invoice\s*no?\.?[:：]\s*(.+)",
                r"mã\s*số[:：]\s*(.+)"
            ],
            "date": [
                r"ngày\s*\d{1,2}\s*tháng\s*\d{1,2}\s*năm\s*\d{4}",
                r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
                r"date[:：]\s*(.+)"
            ],
            "company_name": [
                r"công\s*ty.*?[:：]\s*(.+)",
                r"company\s*name[:：]\s*(.+)",
                r"tên\s*công\s*ty[:：]\s*(.+)"
            ],
            "tax_code": [
                r"mã\s*số\s*thuế[:：]\s*([0-9-]+)",
                r"tax\s*code[:：]\s*([0-9-]+)"
            ],
            "total_amount": [
                r"tổng\s*cộng[:：]\s*([0-9.,]+\s*vnđ?)",
                r"tổng\s*tiền[:：]\s*([0-9.,]+\s*vnđ?)",
                r"total[:：]\s*([0-9.,]+\s*(usd|$|vnđ))",
                r"thành\s*tiền[:：]\s*([0-9.,]+\s*vnđ?)"
            ]
        }
        
        for field_name, patterns in field_patterns.items():
            for pattern in patterns:
                for region in text_regions:
                    match = re.search(pattern, region.text, re.IGNORECASE)
                    if match:
                        field_regions.append({
                            "field_name": field_name,
                            "value": match.group(1) if match.groups() else region.text,
                            "full_text": region.text,
                            "bbox": region.bbox.to_dict(),
                            "confidence": region.confidence,
                            "page": region.page_number,
                            "pattern_matched": pattern
                        })
        
        return field_regions
    
    def get_region_at_coordinates(self, x: float, y: float, text_regions: List[TextRegion]) -> Optional[TextRegion]:
        """Get text region at specific coordinates"""
        for region in text_regions:
            if region.bbox.contains(x, y):
                return region
        return None
    
    def get_regions_in_area(self, bbox: BoundingBox, text_regions: List[TextRegion]) -> List[TextRegion]:
        """Get all text regions within a specific area"""
        return [region for region in text_regions if region.bbox.intersects(bbox)]
