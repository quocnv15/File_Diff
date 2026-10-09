"""
Multi-engine OCR processor for extracting text from images and scanned PDFs
Supports Tesseract, EasyOCR, and PaddleOCR with confidence scoring
"""

import logging
import os
import time
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import tempfile
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Image processing
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

# OCR engines
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    logging.warning("Tesseract not available")

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False
    logging.warning("EasyOCR not available")

try:
    from paddleocr import PaddleOCR
    PADDLEOCR_AVAILABLE = True
except ImportError:
    PADDLEOCR_AVAILABLE = False
    logging.warning("PaddleOCR not available")

logger = logging.getLogger(__name__)


class OCREngine:
    """Base class for OCR engines"""
    
    def __init__(self, name: str):
        self.name = name
        self.is_available = False
        self.confidence_threshold = 0.7
    
    async def extract_text(self, image_path: str, language: str = 'vie') -> Dict[str, Any]:
        """Extract text from image"""
        raise NotImplementedError
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """Preprocess image for better OCR accuracy"""
        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                logger.error(f"Cannot load image: {image_path}")
                return None
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Noise reduction
            denoised = cv2.fastNlMeansDenoising(gray)
            
            # Thresholding
            _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Morphological operations
            kernel = np.ones((2,2), np.uint8)
            processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            return processed
            
        except Exception as e:
            logger.error(f"Image preprocessing failed: {e}")
            return cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)


class TesseractEngine(OCREngine):
    """Tesseract OCR engine implementation"""
    
    def __init__(self):
        super().__init__("tesseract")
        self.is_available = TESSERACT_AVAILABLE
        if self.is_available:
            # Configure Tesseract for Vietnamese
            self.config = r'--oem 3 --psm 6 -l vie+eng'
            # Check if Vietnamese language pack is installed
            try:
                pytesseract.get_languages(config='')
            except Exception as e:
                logger.warning(f"Tesseract language check failed: {e}")
    
    async def extract_text(self, image_path: str, language: str = 'vie') -> Dict[str, Any]:
        """Extract text using Tesseract"""
        if not self.is_available:
            return {"text": "", "confidence": 0.0, "engine": self.name}
        
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image_path)
            if processed_image is None:
                return {"text": "", "confidence": 0.0, "engine": self.name}
            
            # Extract text with confidence data
            data = pytesseract.image_to_data(
                processed_image,
                config=self.config,
                output_type=pytesseract.Output.DICT,
                lang='vie+eng'
            )
            
            # Calculate average confidence
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            # Extract text blocks
            text_blocks = []
            for i in range(len(data['text'])):
                if int(data['conf'][i]) > 30:  # Filter low confidence
                    text_blocks.append(data['text'][i])
            
            extracted_text = ' '.join(text_blocks).strip()
            
            # Extract word-level data for coordinate mapping
            words = []
            for i in range(len(data['text'])):
                if int(data['conf'][i]) > 30 and data['text'][i].strip():
                    words.append({
                        'text': data['text'][i],
                        'confidence': int(data['conf'][i]) / 100.0,
                        'bbox': {
                            'x': data['left'][i],
                            'y': data['top'][i],
                            'width': data['width'][i],
                            'height': data['height'][i]
                        }
                    })
            
            return {
                "text": extracted_text,
                "confidence": avg_confidence / 100.0,
                "engine": self.name,
                "words": words,
                "processing_time": time.time()
            }
            
        except Exception as e:
            logger.error(f"Tesseract extraction failed: {e}")
            return {"text": "", "confidence": 0.0, "engine": self.name, "error": str(e)}


class EasyOCREngine(OCREngine):
    """EasyOCR engine implementation"""
    
    def __init__(self):
        super().__init__("easyocr")
        self.is_available = EASYOCR_AVAILABLE
        self.reader = None
        
    async def extract_text(self, image_path: str, language: str = 'vie') -> Dict[str, Any]:
        """Extract text using EasyOCR"""
        if not self.is_available:
            return {"text": "", "confidence": 0.0, "engine": self.name}
        
        try:
            # Initialize reader if not already done
            if self.reader is None:
                self.reader = easyocr.Reader(['vi', 'en'], gpu=False)
            
            # Extract text
            results = self.reader.readtext(image_path)
            
            # Process results
            words = []
            text_parts = []
            confidences = []
            
            for (bbox, text, confidence) in results:
                if confidence > 0.3:  # Filter low confidence
                    text_parts.append(text)
                    confidences.append(confidence)
                    
                    # Convert bbox to standard format
                    x1, y1 = min(point[0] for point in bbox), min(point[1] for point in bbox)
                    x2, y2 = max(point[0] for point in bbox), max(point[1] for point in bbox)
                    
                    words.append({
                        'text': text,
                        'confidence': confidence,
                        'bbox': {
                            'x': int(x1),
                            'y': int(y1),
                            'width': int(x2 - x1),
                            'height': int(y2 - y1)
                        }
                    })
            
            extracted_text = ' '.join(text_parts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                "text": extracted_text,
                "confidence": avg_confidence,
                "engine": self.name,
                "words": words,
                "processing_time": time.time()
            }
            
        except Exception as e:
            logger.error(f"EasyOCR extraction failed: {e}")
            return {"text": "", "confidence": 0.0, "engine": self.name, "error": str(e)}


class PaddleOCREngine(OCREngine):
    """PaddleOCR engine implementation"""
    
    def __init__(self):
        super().__init__("paddleocr")
        self.is_available = PADDLEOCR_AVAILABLE
        self.ocr = None
        
    async def extract_text(self, image_path: str, language: str = 'vie') -> Dict[str, Any]:
        """Extract text using PaddleOCR"""
        if not self.is_available:
            return {"text": "", "confidence": 0.0, "engine": self.name}
        
        try:
            # Initialize OCR if not already done
            if self.ocr is None:
                self.ocr = PaddleOCR(use_angle_cls=True, lang='vi')
            
            # Extract text
            result = self.ocr.ocr(image_path, cls=True)
            
            # Process results
            words = []
            text_parts = []
            confidences = []
            
            if result and result[0]:
                for line in result[0]:
                    if line:
                        box = line[0]
                        text = line[1][0]
                        confidence = line[1][1]
                        
                        if confidence > 0.3:  # Filter low confidence
                            text_parts.append(text)
                            confidences.append(confidence)
                            
                            # Convert box to standard format
                            x1 = min(point[0] for point in box)
                            y1 = min(point[1] for point in box)
                            x2 = max(point[0] for point in box)
                            y2 = max(point[1] for point in box)
                            
                            words.append({
                                'text': text,
                                'confidence': confidence,
                                'bbox': {
                                    'x': int(x1),
                                    'y': int(y1),
                                    'width': int(x2 - x1),
                                    'height': int(y2 - y1)
                                }
                            })
            
            extracted_text = ' '.join(text_parts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                "text": extracted_text,
                "confidence": avg_confidence,
                "engine": self.name,
                "words": words,
                "processing_time": time.time()
            }
            
        except Exception as e:
            logger.error(f"PaddleOCR extraction failed: {e}")
            return {"text": "", "confidence": 0.0, "engine": self.name, "error": str(e)}


class MultiOCRProcessor:
    """Multi-engine OCR processor with consensus voting"""
    
    def __init__(self):
        self.engines = {
            'tesseract': TesseractEngine(),
            'easyocr': EasyOCREngine(),
            'paddleocr': PaddleOCREngine()
        }
        
        # Filter available engines
        self.available_engines = {
            name: engine for name, engine in self.engines.items() 
            if engine.is_available
        }
        
        logger.info(f"Available OCR engines: {list(self.available_engines.keys())}")
        
        # Thread pool for parallel processing
        self.executor = ThreadPoolExecutor(max_workers=3)
    
    async def extract_text_with_confidence(self, image_path: str, language: str = 'vie') -> Dict[str, Any]:
        """Extract text using multiple OCR engines with confidence scoring"""
        start_time = time.time()
        
        if not self.available_engines:
            logger.error("No OCR engines available")
            return {
                "text": "",
                "confidence": 0.0,
                "engines_used": [],
                "consensus": False,
                "error": "No OCR engines available"
            }
        
        # Run extraction in parallel
        tasks = []
        for name, engine in self.available_engines.items():
            task = asyncio.create_task(engine.extract_text(image_path, language))
            tasks.append((name, task))
        
        # Wait for all engines to complete
        results = {}
        for name, task in tasks:
            try:
                result = await task
                results[name] = result
            except Exception as e:
                logger.error(f"OCR engine {name} failed: {e}")
                results[name] = {"text": "", "confidence": 0.0, "engine": name, "error": str(e)}
        
        # Find best result
        best_result = self._select_best_result(results)
        
        # Apply consensus voting if multiple engines
        consensus_result = None
        if len(results) > 1:
            consensus_result = self._consensus_voting(results)
        
        final_result = consensus_result if consensus_result else best_result
        final_result.update({
            "engines_used": list(results.keys()),
            "all_results": results,
            "processing_time": time.time() - start_time,
            "consensus": consensus_result is not None
        })
        
        return final_result
    
    def _select_best_result(self, results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Select the best result based on confidence and text quality"""
        if not results:
            return {"text": "", "confidence": 0.0}
        
        # Sort by confidence
        sorted_results = sorted(
            [(name, result) for name, result in results.items() if result.get("confidence", 0) > 0],
            key=lambda x: x[1].get("confidence", 0),
            reverse=True
        )
        
        if sorted_results:
            return sorted_results[0][1]
        
        # Fallback to first result with any text
        for name, result in results.items():
            if result.get("text", "").strip():
                return result
        
        return {"text": "", "confidence": 0.0}
    
    def _consensus_voting(self, results: Dict[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Apply consensus voting between multiple OCR results"""
        if len(results) < 2:
            return None
        
        # Extract texts with weights based on confidence
        weighted_texts = []
        for name, result in results.items():
            text = result.get("text", "").strip()
            confidence = result.get("confidence", 0)
            if text and confidence > 0.3:
                weighted_texts.append((text, confidence))
        
        if not weighted_texts:
            return None
        
        # Sort by confidence
        weighted_texts.sort(key=lambda x: x[1], reverse=True)
        
        # Use highest confidence result as base
        base_text, base_confidence = weighted_texts[0]
        
        # Check if other engines agree
        agreement_count = 0
        total_confidence = base_confidence
        
        for text, confidence in weighted_texts[1:]:
            # Simple similarity check (can be enhanced)
            similarity = self._calculate_similarity(base_text, text)
            if similarity > 0.7:  # 70% similarity threshold
                agreement_count += 1
                total_confidence += confidence
        
        # If there's agreement, create consensus result
        if agreement_count >= len(weighted_texts) // 2:
            avg_confidence = total_confidence / (agreement_count + 1)
            
            # Merge words from all engines
            merged_words = []
            for name, result in results.items():
                words = result.get("words", [])
                merged_words.extend(words)
            
            return {
                "text": base_text,
                "confidence": min(avg_confidence * 1.1, 1.0),  # Boost confidence for consensus
                "engine": "consensus",
                "words": merged_words,
                "agreement_count": agreement_count + 1,
                "total_engines": len(results)
            }
        
        return None
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        try:
            # Simple word-based similarity
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            
            if not words1 or not words2:
                return 0.0
            
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            
            return len(intersection) / len(union)
            
        except Exception:
            return 0.0
    
    async def extract_with_coordinates(self, image_path: str, language: str = 'vie') -> Dict[str, Any]:
        """Extract text with coordinate information for layout analysis"""
        result = await self.extract_text_with_confidence(image_path, language)
        
        # Process words into structured format with coordinates
        if "words" in result:
            # Sort words by reading order (top to bottom, left to right)
            words = result["words"]
            words.sort(key=lambda w: (w["bbox"]["y"], w["bbox"]["x"]))
            
            # Group words into lines
            lines = []
            current_line = []
            current_y = None
            
            for word in words:
                word_y = word["bbox"]["y"]
                
                if current_y is None:
                    current_y = word_y
                    current_line = [word]
                elif abs(word_y - current_y) < 20:  # Same line (within 20 pixels)
                    current_line.append(word)
                else:
                    # New line
                    if current_line:
                        lines.append(current_line)
                    current_line = [word]
                    current_y = word_y
            
            # Add last line
            if current_line:
                lines.append(current_line)
            
            result["structured_text"] = {
                "lines": lines,
                "word_count": len(words),
                "line_count": len(lines)
            }
        
        return result
    
    def get_engine_status(self) -> Dict[str, Any]:
        """Get status of all OCR engines"""
        return {
            name: {
                "available": engine.is_available,
                "confidence_threshold": engine.confidence_threshold
            }
            for name, engine in self.engines.items()
        }


# Global OCR processor instance
_ocr_processor = None

def get_ocr_processor() -> MultiOCRProcessor:
    """Get global OCR processor instance"""
    global _ocr_processor
    if _ocr_processor is None:
        _ocr_processor = MultiOCRProcessor()
    return _ocr_processor
