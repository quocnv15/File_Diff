# PRD: Document Extraction System

## 📋 Product Requirements Document

### 1. Product Overview

**Problem**: Các doanh nghiệp cần trích xuất dữ liệu từ nhiều loại chứng từ (Excel tờ khai, PDF invoices, contracts, etc.) và tự động điền vào Word templates để tiết kiệm thời gian và giảm lỗi.

**Solution**: Hệ thống trích xuất dữ liệu thông minh từ Excel & PDF với accuracy >95%, hỗ trợ Vietnamese language và tự động tạo Word documents.

### 2. Target Users

- **Primary**: Accounting departments, logistics companies, trading firms
- **Secondary**: Legal teams, admin staff, document processors

### 3. Document Types Support

#### Excel Documents:
- Tờ khai hàng hóa
- Bảng định mức
- Bảng phân bổ chi phí
- Sổ chi tiết công nợ

#### PDF Documents:
- Sale Contracts
- Invoices (Hóa đơn)
- Giấy nộm tiền
- Phí cơ sở hạ tầng
- Hoá đơn vận chuyển
- Bảo hiểm hàng hóa
- Hoá đơn local charge
- Thông báo tiền về
- VILAS - Tờ kiểm nghiệm

### 4. Core Features

#### 4.1 Document Processing Engine
- **Multi-format support**: Excel (.xlsx, .xls), PDF
- **OCR integration**: Tesseract + EasyOCR + PaddleOCR
- **Vietnamese language support**: Specialized models
- **Layout analysis**: Coordinate-based field extraction
- **Template matching**: Automatic document type detection

#### 4.2 Data Extraction & Validation
- **Field extraction**: Intelligent field recognition with confidence scoring
- **Cross-validation**: Business rules validation for each document type
- **Anomaly detection**: Flag suspicious data for manual review
- **Data mapping**: Automatic field mapping to template placeholders

#### 4.3 Word Template System
- **Template library**: Pre-built templates for each document type
- **Placeholder system**: Smart field mapping with {{variable}} syntax
- **Conditional formatting**: Dynamic content based on extracted data
- **Version control**: Template versioning and rollback

#### 4.4 User Interface
- **Drag-drop upload**: Multiple file support
- **Document type selection**: Auto-detection with manual override
- **Real-time preview**: Show extracted data before generation
- **Batch processing**: Process multiple documents simultaneously

### 5. Technical Requirements

#### 5.1 Performance Targets
- **Processing speed**: <30 seconds per document
- **Accuracy rate**: >95% for standard documents
- **Concurrent users**: Support 10+ simultaneous users
- **File size limit**: Up to 50MB per file

#### 5.2 Integration Requirements
- **Backend**: FastAPI (existing) enhanced with new processors
- **Frontend**: Vanilla JS web interface (existing) with new components
- **Database**: SQLite for templates, Redis for caching
- **Storage**: File system with organized directory structure

#### 5.3 Quality Requirements
- **Error handling**: Comprehensive error recovery and logging
- **Data validation**: Multi-level validation with business rules
- **Audit trail**: Track all processing steps and changes
- **Security**: File encryption and access control

### 6. Success Metrics

#### 6.1 Accuracy Metrics
- **Field extraction accuracy**: >95%
- **Document type detection**: >98%
- **Template matching**: >90%
- **Vietnamese text recognition**: >95%

#### 6.2 Performance Metrics
- **Processing time**: <30 seconds average
- **System uptime**: >99%
- **User satisfaction**: >4.5/5 rating
- **Error rate**: <2% for standard documents

#### 6.3 Business Metrics
- **Processing time reduction**: >80% compared to manual
- **Error reduction**: >90% compared to manual entry
- **Cost savings**: >50% in document processing costs
- **User adoption**: >80% of target users using system

### 7. Constraints & Assumptions

#### 7.1 Technical Constraints
- Must integrate with existing FastAPI backend
- Must support Vietnamese language natively
- Must work with scanned PDFs and images
- Must maintain existing file comparison functionality

#### 7.2 Business Constraints
- Limited development timeline (4-6 weeks)
- Budget constraints on third-party APIs
- Must be self-hosted (no cloud dependencies)
- Must comply with Vietnamese data regulations

#### 7.3 Assumptions
- Users have basic computer skills
- Documents follow standard Vietnamese formats
- Internet connection is available for OCR processing
- Quality of scanned documents is readable

### 8. Risk Assessment

#### 8.1 Technical Risks
- **OCR accuracy**: Mitigate with multi-engine approach
- **Vietnamese support**: Use specialized language models
- **Template variations**: Build flexible template system
- **Performance bottlenecks**: Implement async processing

#### 8.2 Business Risks
- **User adoption**: Provide training and support
- **Document quality**: Set minimum quality standards
- **Competitive pressure**: Focus on Vietnamese market advantage
- **Regulatory changes**: Build flexible compliance framework

### 9. MVP Scope

#### 9.1 MVP Features (Phase 1)
- Basic PDF text extraction with OCR
- Excel data extraction
- Simple Word template generation
- Web interface for file upload
- Support for 3 most common document types

#### 9.2 Future Features (Phase 2+)
- Advanced layout analysis
- Machine learning for field detection
- Mobile app interface
- Integration with accounting systems
- Advanced reporting and analytics

### 10. Success Criteria

**Launch Success**: 
- MVP delivered within 6 weeks
- >80% accuracy on test documents
- Positive feedback from 5 beta users
- System handles 100+ documents/day

**3-Month Success**:
- >95% accuracy on all document types
- 20+ active users
- Processing 500+ documents/week
- <5% error rate

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-16  
**Next Review**: 2025-10-23  
**Status**: Ready for Development
