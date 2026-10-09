"""
API routes for document field extraction
"""

import logging
from typing import Dict, Any, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
import tempfile
import os
from pathlib import Path

from processors.field_extractor import get_field_extractor
from processors.ocr_processor import get_ocr_processor
from utils.exceptions import ProcessingFailedError, CorruptedFileError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/extraction", tags=["extraction"])


@router.post("/extract")
async def extract_document_fields(
    file: UploadFile = File(...),
    document_type: Optional[str] = Form(None),
    language: str = Form("vie"),
    use_ocr: str = Form("auto"),
    confidence_threshold: float = Form(0.7)
) -> Dict[str, Any]:
    """
    Extract fields from a document using multi-engine OCR and template matching
    
    Args:
        file: Uploaded document file (PDF, image)
        document_type: Optional document type hint (invoice, contract, shipping, etc.)
        language: Language for OCR processing (vie, eng)
        use_ocr: OCR usage (auto, force, disable)
        confidence_threshold: Minimum confidence threshold for field extraction
    
    Returns:
        JSON response with extracted fields, tables, and metadata
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Check file type
        allowed_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type: {file_ext}. Allowed types: {allowed_extensions}"
            )
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Get field extractor
            extractor = get_field_extractor()
            
            # Prepare extraction options
            options = {
                "language": language,
                "use_ocr": use_ocr,
                "confidence_threshold": confidence_threshold
            }
            
            # Extract fields
            result = await extractor.extract_fields(
                file_path=temp_file_path,
                document_type=document_type,
                options=options
            )
            
            # Convert result to dictionary
            response_data = result.to_dict()
            
            # Add processing summary
            response_data["processing_summary"] = {
                "filename": file.filename,
                "file_size": len(content),
                "file_type": file_ext,
                "status": "success" if result.confidence_score > confidence_threshold else "low_confidence"
            }
            
            return response_data
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass
    
    except CorruptedFileError as e:
        logger.error(f"Corrupted file error: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid or corrupted file: {str(e)}")
    
    except ProcessingFailedError as e:
        logger.error(f"Processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Document processing failed: {str(e)}")
    
    except Exception as e:
        logger.error(f"Unexpected error in document extraction: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/extract-ocr-only")
async def extract_text_with_ocr(
    file: UploadFile = File(...),
    language: str = Form("vie"),
    engine: str = Form("auto")
) -> Dict[str, Any]:
    """
    Extract text from document using OCR only (for testing OCR accuracy)
    
    Args:
        file: Uploaded document file (PDF, image)
        language: Language for OCR processing
        engine: OCR engine to use (auto, tesseract, easyocr, paddleocr)
    
    Returns:
        JSON response with OCR results and confidence scores
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Get OCR processor
            ocr_processor = get_ocr_processor()
            
            # Extract text with coordinates
            result = await ocr_processor.extract_with_coordinates(temp_file_path, language)
            
            # Add file information
            result["file_info"] = {
                "filename": file.filename,
                "file_size": len(content),
                "engine_requested": engine
            }
            
            return result
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass
    
    except Exception as e:
        logger.error(f"OCR extraction failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")


@router.get("/document-types")
async def get_supported_document_types() -> Dict[str, Any]:
    """
    Get list of supported document types and their templates
    
    Returns:
        JSON response with supported document types and template information
    """
    try:
        from processors.layout_analyzer import LayoutAnalyzer
        
        analyzer = LayoutAnalyzer()
        
        # Get available templates
        templates = []
        for doc_type, template in analyzer.templates.items():
            templates.append({
                "document_type": template.document_type,
                "template_name": template.name,
                "version": template.version,
                "confidence_threshold": template.confidence_threshold,
                "description": template.__dict__.get("description", "")
            })
        
        # Add document type descriptions
        document_types = {
            "invoice": {
                "name": "Hóa đơn",
                "description": "Vietnamese invoices with itemized tables",
                "supported_formats": ["PDF"],
                "required_fields": ["invoice_number", "invoice_date", "total_amount"]
            },
            "contract": {
                "name": "Hợp đồng",
                "description": "Sale contracts with parties and item tables",
                "supported_formats": ["PDF"],
                "required_fields": ["contract_number", "contract_date", "parties"]
            },
            "shipping": {
                "name": "Chứng từ vận chuyển",
                "description": "Bill of lading, delivery notes, shipping documents",
                "supported_formats": ["PDF"],
                "required_fields": ["document_number", "shipping_date", "parties"]
            }
        }
        
        return {
            "supported_types": document_types,
            "available_templates": templates,
            "total_templates": len(templates)
        }
    
    except Exception as e:
        logger.error(f"Failed to get document types: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve document types: {str(e)}")


@router.get("/ocr-engines")
async def get_ocr_engine_status() -> Dict[str, Any]:
    """
    Get status of available OCR engines
    
    Returns:
        JSON response with OCR engine availability and status
    """
    try:
        ocr_processor = get_ocr_processor()
        engine_status = ocr_processor.get_engine_status()
        
        return {
            "engines": engine_status,
            "available_engines": [name for name, status in engine_status.items() if status["available"]],
            "total_engines": len(engine_status),
            "recommended_engine": "multi_engine" if len(engine_status) > 1 else list(engine_status.keys())[0]
        }
    
    except Exception as e:
        logger.error(f"Failed to get OCR engine status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve OCR status: {str(e)}")


@router.post("/validate-template")
async def validate_document_template(
    file: UploadFile = File(...),
    document_type: str = Form(...),
    template_name: str = Form(...)
) -> Dict[str, Any]:
    """
    Validate document against a specific template
    
    Args:
        file: Uploaded document file
        document_type: Type of document to validate against
        template_name: Specific template name to validate against
    
    Returns:
        JSON response with template validation results
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Get field extractor
            extractor = get_field_extractor()
            
            # Extract fields with specific document type
            result = await extractor.extract_fields(
                file_path=temp_file_path,
                document_type=document_type
            )
            
            # Validate against template
            validation_result = {
                "template_matched": False,
                "template_name": template_name,
                "document_type": document_type,
                "match_score": 0.0,
                "missing_required_fields": [],
                "extracted_fields_count": len(result.fields),
                "confidence_score": result.confidence_score
            }
            
            # Check if template matched
            if result.template_match:
                if (result.template_match.get("document_type") == document_type and
                    result.template_match.get("template_name") == template_name):
                    validation_result["template_matched"] = True
                    validation_result["match_score"] = result.template_match.get("confidence", 0.0)
            
            # Check missing required fields (basic check)
            required_fields_by_type = {
                "invoice": ["invoice_number", "invoice_date", "total_amount"],
                "contract": ["contract_number", "contract_date"],
                "shipping": ["document_number", "shipping_date"]
            }
            
            required_fields = required_fields_by_type.get(document_type, [])
            extracted_field_names = [field.name for field in result.fields]
            
            missing_fields = [field for field in required_fields if field not in extracted_field_names]
            validation_result["missing_required_fields"] = missing_fields
            
            # Overall validation result
            validation_result["validation_passed"] = (
                validation_result["template_matched"] and
                validation_result["match_score"] > 0.7 and
                len(missing_fields) == 0
            )
            
            return validation_result
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass
    
    except Exception as e:
        logger.error(f"Template validation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Template validation failed: {str(e)}")


@router.get("/health")
async def extraction_health_check() -> Dict[str, Any]:
    """
    Health check for extraction services
    
    Returns:
        JSON response with system health status
    """
    try:
        # Check OCR processor
        ocr_processor = get_ocr_processor()
        ocr_status = ocr_processor.get_engine_status()
        
        # Check field extractor
        field_extractor = get_field_extractor()
        
        # Check templates
        from processors.layout_analyzer import LayoutAnalyzer
        analyzer = LayoutAnalyzer()
        
        available_engines = sum(1 for status in ocr_status.values() if status["available"])
        total_engines = len(ocr_status)
        
        health_status = {
            "status": "healthy" if available_engines > 0 else "unhealthy",
            "ocr_engines": {
                "available": available_engines,
                "total": total_engines,
                "details": ocr_status
            },
            "templates": {
                "available": len(analyzer.templates),
                "types": list(analyzer.templates.keys())
            },
            "components": {
                "field_extractor": "healthy",
                "layout_analyzer": "healthy",
                "pdf_processor": "healthy"
            }
        }
        
        return health_status
    
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "components": {
                "field_extractor": "unhealthy",
                "layout_analyzer": "unknown",
                "pdf_processor": "unknown"
            }
        }
