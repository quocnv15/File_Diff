# SOP: Adding New Document Types

## 🎯 Overview

Standard Operating Procedure cho việc thêm new document types vào hệ thống trích xuất dữ liệu. Process này đảm bảo consistency và maintainability khi mở rộng system capabilities.

## 📋 Prerequisites

1. **System Access**: Access đến backend codebase và templates directory
2. **Document Samples**: Có ít nhất 5-10 sample documents của type mới
3. **Field Mapping**: Understanding của các fields cần extract
4. **Testing**: Access đến testing framework và sample data

## 🔄 Process Steps

### Step 1: Document Analysis (2-4 hours)

#### 1.1 Collect Sample Documents
```bash
# Create directory for new document type
mkdir -p backend/templates/document_types/new_type/samples
```

#### 1.2 Analyze Document Structure
- **Layout Analysis**: Xác định text regions, table structures
- **Field Identification**: List tất cả fields cần extract
- **Variation Assessment**: Xác định các variations trong layout
- **Quality Assessment**: Đánh giá chất lượng scanned documents

#### 1.3 Create Field Specification
Document trong: `backend/templates/document_types/new_type/field_spec.json`

```json
{
  "document_type": "new_type",
  "vietnamese_name": "Tên Loại Chứng Từ",
  "description": "Mô tả loại chứng từ",
  "required_fields": [
    {
      "name": "field_name",
      "vietnamese_name": "Tên Trường",
      "field_type": "text|number|date|currency",
      "required": true,
      "validation_rules": ["rule1", "rule2"],
      "coordinates": {"x": 100, "y": 200, "width": 300, "height": 50}
    }
  ],
  "optional_fields": [...],
  "table_fields": [
    {
      "name": "table_name",
      "headers": ["Column1", "Column2", "Column3"],
      "coordinate_regions": [
        {"x": 50, "y": 300, "width": 500, "height": 200}
      ]
    }
  ]
}
```

### Step 2: Template Creation (3-6 hours)

#### 2.1 Create PDF Template
File: `backend/templates/pdf_templates/new_type_template.json`

```json
{
  "template_name": "new_type_template",
  "document_type": "new_type",
  "version": "1.0",
  "confidence_threshold": 0.85,
  "regions": [
    {
      "name": "header_region",
      "coordinates": {"x": 0, "y": 0, "width": 600, "height": 150},
      "fields": [
        {
          "name": "document_number",
          "coordinates": {"x": 100, "y": 50, "width": 200, "height": 30},
          "extraction_method": "ocr|text|table",
          "validation_patterns": ["^[A-Z0-9]{3,}$"]
        }
      ]
    }
  ],
  "extraction_engines": ["tesseract", "easyocr", "pdfplumber"],
  "post_processing_rules": [
    {"field": "amount", "operation": "clean_currency"}
  ]
}
```

#### 2.2 Create Excel Template (nếu applicable)
File: `backend/templates/excel_templates/new_type_template.json`

```json
{
  "template_name": "new_type_excel_template",
  "document_type": "new_type",
  "sheet_patterns": [
    {
      "sheet_name_pattern": ".*Tờ khai.*",
      "header_row_detection": {
        "patterns": ["Tên hàng", "Số lượng", "Đơn giá"],
        "min_matches": 2
      }
    }
  ],
  "column_mappings": {
    "product_name": ["Tên hàng", "Tên sản phẩm", "Hàng hóa"],
    "quantity": ["Số lượng", "SL", "Quantity"],
    "unit_price": ["Đơn giá", "Giá", "Price"]
  },
  "data_validation": {
    "quantity": {"min": 0, "type": "number"},
    "unit_price": {"min": 0, "type": "currency"}
  }
}
```

#### 2.3 Create Word Output Template
File: `backend/templates/word_templates/new_type_output.docx`

Sử dụng Jinja2 template syntax:
```django
{% if document_number %}
Số chứng từ: {{ document_number }}
{% endif %}

{% if table_data %}
Bảng chi tiết:
{% for row in table_data %}
- {{ row.product_name }}: {{ row.quantity }} {{ row.unit }}
{% endfor %}
{% endif %}
```

### Step 3: Processing Logic Implementation (4-8 hours)

#### 3.1 Create Field Extractor
File: `backend/processors/extractors/new_type_extractor.py`

```python
from processors.base_extractor import BaseExtractor
from models.extraction_models import ExtractionResult

class NewTypeExtractor(BaseExtractor):
    def __init__(self):
        super().__init__()
        self.document_type = "new_type"
        self.load_template("new_type_template.json")
    
    async def extract(self, file_path: str, options: dict = None) -> ExtractionResult:
        """Extract data from new_type documents"""
        # 1. Pre-processing
        processed_image = await self.preprocess_image(file_path)
        
        # 2. Multi-engine extraction
        extraction_results = await self.extract_with_multiple_engines(processed_image)
        
        # 3. Apply template matching
        matched_data = await self.apply_template_matching(extraction_results)
        
        # 4. Validation and confidence scoring
        validated_result = await self.validate_extracted_data(matched_data)
        
        return validated_result
    
    async def validate_extracted_data(self, data: dict) -> ExtractionResult:
        """Apply business rules and validation"""
        # Implement validation logic
        pass
```

#### 3.2 Update Main Extractor Factory
File: `backend/processors/extractor_factory.py`

```python
from processors.extractors.new_type_extractor import NewTypeExtractor

class ExtractorFactory:
    EXTRACTORS = {
        "invoice": InvoiceExtractor,
        "contract": ContractExtractor,
        "new_type": NewTypeExtractor,  # Add new extractor
    }
    
    @classmethod
    def get_extractor(cls, document_type: str):
        extractor_class = cls.EXTRACTORS.get(document_type)
        if not extractor_class:
            raise ValueError(f"Unsupported document type: {document_type}")
        return extractor_class()
```

### Step 4: API Integration (2-3 hours)

#### 4.1 Add New Document Type to API
File: `backend/api/routes/extraction.py`

```python
from processors.extractor_factory import ExtractorFactory

@router.post("/extract/{document_type}")
async def extract_document(
    document_type: str,
    file: UploadFile = File(...),
    options: ExtractionOptions = None
):
    """Extract data from specific document type"""
    
    # Validate document type
    try:
        extractor = ExtractorFactory.get_extractor(document_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Process file
    result = await extractor.extract(file.file, options.dict())
    
    return result
```

#### 4.2 Update Document Type List
File: `backend/api/routes/document_types.py`

```python
@router.get("/types")
async def get_document_types():
    """Get list of supported document types"""
    return {
        "document_types": [
            {"type": "invoice", "name": "Hóa đơn"},
            {"type": "contract", "name": "Hợp đồng"},
            {"type": "new_type", "name": "Tên Loại Chứng Từ"},  # Add new type
        ]
    }
```

### Step 5: Testing (4-6 hours)

#### 5.1 Create Unit Tests
File: `backend/tests/test_new_type_extraction.py`

```python
import pytest
from processors.extractors.new_type_extractor import NewTypeExtractor

@pytest.mark.asyncio
async def test_new_type_extraction():
    """Test new_type document extraction"""
    extractor = NewTypeExtractor()
    
    # Test with sample file
    result = await extractor.extract("samples/new_type/sample1.pdf")
    
    # Assertions
    assert result.document_type == "new_type"
    assert result.confidence_score > 0.8
    assert "document_number" in result.extracted_data
    assert len(result.table_data) > 0

@pytest.mark.asyncio
async def test_new_type_validation():
    """Test data validation for new_type"""
    # Test validation logic
    pass

@pytest.mark.asyncio
async def test_new_type_word_generation():
    """Test Word document generation"""
    # Test Word template processing
    pass
```

#### 5.2 Create Integration Tests
File: `backend/tests/test_integration_new_type.py`

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_extract_new_type_endpoint():
    """Test extraction API endpoint"""
    with open("samples/new_type/sample1.pdf", "rb") as f:
        response = client.post(
            "/api/extraction/extract/new_type",
            files={"file": ("test.pdf", f, "application/pdf")}
        )
    
    assert response.status_code == 200
    result = response.json()
    assert result["document_type"] == "new_type"
    assert result["confidence_score"] > 0.8
```

#### 5.3 Accuracy Validation
Test với minimum 10 sample documents:

```python
# Test matrix
test_documents = [
    "samples/new_type/high_quality.pdf",
    "samples/new_type/scanned_copy.pdf", 
    "samples/new_type/handwritten_notes.pdf",
    # ... more samples
]

for doc in test_documents:
    result = await extractor.extract(doc)
    assert result.confidence_score > 0.85
    assert validate_field_accuracy(result.extracted_data, doc)
```

### Step 6: Documentation (1-2 hours)

#### 6.1 Update API Documentation
- Add new document type to OpenAPI specs
- Document field specifications
- Include sample requests/responses

#### 6.2 Update User Guide
- Add instructions for new document type
- Include template requirements
- Document supported variations

#### 6.3 Update System Documentation
File: `.agent/System/supported_document_types.md`

```markdown
## New Document Type Support

### Type: new_type
- **Vietnamese Name**: Tên Loại Chứng Từ
- **Supported Formats**: PDF, Excel
- **Required Fields**: field1, field2
- **Optional Fields**: field3, field4
- **Table Extraction**: Yes
- **Accuracy Target**: >90%
- **Processing Time**: <15 seconds
```

## ✅ Quality Gates

### Before Release
- [ ] **Unit Tests**: 100% passing
- [ ] **Integration Tests**: All scenarios covered
- [ ] **Accuracy Validation**: >90% on 10+ samples
- [ ] **Performance**: Processing time <15 seconds
- [ ] **Error Handling**: Graceful failure with meaningful messages
- [ ] **Documentation**: Complete and up-to-date

### Production Readiness
- [ ] **User Acceptance**: Beta testing with real users
- [ ] **Performance Testing**: Load testing with concurrent users
- [ ] **Security Review**: File validation and access control
- [ ] **Monitoring**: Accuracy tracking and alerting

## 🚨 Common Pitfalls & Solutions

### Pitfall 1: Inconsistent Document Layouts
**Problem**: Documents có nhiều layout variations
**Solution**: 
- Create multiple templates cho từng variation
- Implement template detection algorithm
- Use fuzzy matching cho template selection

### Pitfall 2: Low OCR Accuracy
**Problem**: Vietnamese OCR accuracy thấp
**Solution**:
- Use multi-engine approach
- Implement custom Vietnamese language models
- Add post-processing corrections

### Pitfall 3: Complex Table Structures
**Problem**: Tables with merged cells hoặc complex layouts
**Solution**:
- Use advanced table detection algorithms
- Implement manual region selection
- Provide template overrides for complex cases

## 📊 Success Metrics

### Technical Metrics
- **Extraction Accuracy**: >90%
- **Processing Time**: <15 seconds
- **Error Rate**: <5%
- **Template Matching**: >95%

### Business Metrics
- **User Satisfaction**: >4.5/5
- **Processing Volume**: Target documents/day
- **Error Reduction**: >80% vs manual
- **Time Savings**: >70% vs manual processing

---

**SOP Version**: 1.0  
**Last Updated**: 2025-10-16  
**Review Frequency**: Quarterly  
**Approval Required**: System Architect, QA Lead
