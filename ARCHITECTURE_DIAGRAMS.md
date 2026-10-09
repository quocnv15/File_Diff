# File Comparison System - Architectural Diagrams
**Created:** October 14, 2025  
**Purpose:** Visual system architecture and conversion correctness analysis

## 🎯 1. High-Level System Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[🌐 Web Interface<br/>HTML/CSS/JavaScript]
        UP[📤 File Upload Component]
        DV[🔍 Diff Visualization]
        EX[📊 Export Controls]
    end

    subgraph "API Gateway"
        API[🚪 FastAPI Gateway<br/>Port 8001]
        AUTH[🔐 Authentication]
        VAL[✅ Validation]
    end

    subgraph "Processing Layer"
        FM[📁 File Manager]
        FP[⚙️ File Processors]
        CE[🔬 Comparison Engine]
        GEN[📝 Report Generator]
    end

    subgraph "Storage Layer"
        UPST[📤 Upload Storage<br/>./storage/uploads]
        PRST[💾 Processed Data<br/>./storage/processed]
        EXST[📋 Export Storage<br/>./storage/exports]
    end

    UI --> API
    UP --> API
    DV --> API
    EX --> API
    
    API --> AUTH
    API --> VAL
    AUTH --> FM
    VAL --> FM
    
    FM --> FP
    FP --> CE
    CE --> GEN
    
    FM --> UPST
    FP --> PRST
    GEN --> EXST
```

## 🔧 2. File Processing Pipeline Architecture

```mermaid
flowchart LR
    subgraph "Input Files"
        PDF[📄 PDF File<br/>31JOC.pdf]
        XLS[📊 Excel File<br/>31JOC.xlsx]
        CSV[📋 CSV File<br/>data.csv]
    end

    subgraph "File Detection"
        DETECT[🔍 File Type Detection<br/>MIME + Extension]
    end

    subgraph "Processing Engines"
        PDFP[📖 PDF Processor<br/>pdfplumber]
        XLSP[📊 Excel Processor<br/>pandas/openpyxl]
        CSVP[📋 CSV Processor<br/>pandas]
    end

    subgraph "Conversion Pipeline"
        NORM[🔧 Data Normalization]
        TABLE[📋 Table Extraction]
        MARK[📝 Markdown Conversion]
        VALID[✅ Quality Validation]
    end

    subgraph "Output Results"
        MD[📄 Markdown Content]
        DATA[🗂️ Structured Data]
        META[📊 Metadata]
    end

    PDF --> DETECT
    XLS --> DETECT
    CSV --> DETECT
    
    DETECT --> PDFP
    DETECT --> XLSP
    DETECT --> CSVP
    
    PDFP --> NORM
    XLSP --> NORM
    CSVP --> NORM
    
    NORM --> TABLE
    TABLE --> MARK
    MARK --> VALID
    VALID --> MD
    VALID --> DATA
    VALID --> META
```

## 📊 3. Conversion Correctness Analysis Results

```mermaid
graph LR
    subgraph "Test Files"
        PDF_FILE[📄 31JOC.pdf<br/>254KB Sales Contract]
        XLS_FILE[📊 31JOC.xlsx<br/>957KB Data Sheet]
    end

    subgraph "Processing Metrics"
        subgraph "PDF Performance"
            PDF_TIME[⏱️ 0.279s]
            PDF_SIZE[📏 913 KB/s]
            PDF_CONTENT[📝 10.2K chars]
        end
        
        subgraph "Excel Performance"
            XLS_TIME[⏱️ 0.293s]
            XLS_SIZE[📏 3,261 KB/s]
            XLS_CONTENT[📝 105.5K chars]
        end
    end

    subgraph "Accuracy Assessment"
        subgraph "PDF Results"
            PDF_TEXT[✅ Text: 95%]
            PDF_TABLE[❌ Tables: 0%]
            PDF_STRUCT[⚠️ Structure: 60%]
        end
        
        subgraph "Excel Results"
            XLS_TEXT[✅ Text: 90%]
            XLS_TABLE[⚠️ Tables: 100%<br/>(empty)]
            XLS_STRUCT[⚠️ Structure: 70%]
        end
    end

    subgraph "Overall Score"
        FINAL[📊 Overall Accuracy: 70.5%<br/>🟡 MODERATE - NEEDS IMPROVEMENT]
    end

    PDF_FILE --> PDF_TIME
    PDF_FILE --> PDF_TEXT
    PDF_FILE --> PDF_TABLE
    PDF_FILE --> PDF_STRUCT
    
    XLS_FILE --> XLS_TIME
    XLS_FILE --> XLS_TEXT
    XLS_FILE --> XLS_TABLE
    XLS_FILE --> XLS_STRUCT
    
    PDF_TEXT --> FINAL
    PDF_TABLE --> FINAL
    PDF_STRUCT --> FINAL
    XLS_TEXT --> FINAL
    XLS_TABLE --> FINAL
    XLS_STRUCT --> FINAL
```

## 🚨 4. Critical Issues Identification

```mermaid
graph TD
    subgraph "Root Cause Analysis"
        subgraph "PDF Issues"
            PDF_ROOT[📄 PDF Processing Failures]
            PDF_CAUSE1[⚠️ Complex Document Structure<br/>Business contracts with embedded tables]
            PDF_CAUSE2[🔍 Table Detection Failure<br/>pdfplumber can't identify boundaries]
            PDF_CAUSE3[🌏 Bilingual Content<br/>Mixed English/Vietnamese text]
            PDF_IMPACT[💥 Critical Impact<br/>Pricing data lost]
        end

        subgraph "Excel Issues"
            XLS_ROOT[📊 Excel Processing Failures]
            XLS_CAUSE1[🏷️ Header Problem<br/>85.9% columns labeled "Unnamed: X"]
            XLS_CAUSE2[📉 Data Sparsity<br/>High missing data percentage]
            XLS_CAUSE3[🔧 Quality Control<br/>No validation/cleaning logic]
            XLS_IMPACT[💥 Critical Impact<br/>Structured data unusable]
        end
    end

    PDF_ROOT --> PDF_CAUSE1
    PDF_ROOT --> PDF_CAUSE2
    PDF_ROOT --> PDF_CAUSE3
    PDF_CAUSE1 --> PDF_IMPACT
    PDF_CAUSE2 --> PDF_IMPACT
    PDF_CAUSE3 --> PDF_IMPACT

    XLS_ROOT --> XLS_CAUSE1
    XLS_ROOT --> XLS_CAUSE2
    XLS_ROOT --> XLS_CAUSE3
    XLS_CAUSE1 --> XLS_IMPACT
    XLS_CAUSE2 --> XLS_IMPACT
    XLS_CAUSE3 --> XLS_IMPACT
```

## 🛠️ 5. Detailed Component Architecture

```mermaid
graph TB
    subgraph "Frontend Components"
        subgraph "Core UI"
            INDEX[index.html<br/>Main Application]
            MAIN[main.js<br/>Application Controller]
            HELPERS[helpers.js<br/>Utility Functions]
        end

        subgraph "Processing"
            PARSERS[file-parsers.js<br/>Client-side Parsing]
            API_INT[api_integration.js<br/>Backend Communication]
            DIFF_VIZ[diff-visualization.js<br/>Display Logic]
        end

        subgraph "Styling"
            MAIN_CSS[main.css<br/>Primary Styles]
            DIFF_CSS[diff.css<br/>Diff Visualization]
        end
    end

    subgraph "Backend Components"
        subgraph "API Layer"
            MAIN_PY[main.py<br/>FastAPI Application]
            FILES_ROUTE[files.py<br/>File Management]
            COMP_ROUTE[comparison.py<br/>Comparison Logic]
            HEALTH[health.py<br/>System Status]
        end

        subgraph "Processing Engines"
            BASE_PROC[base_processor.py<br/>Abstract Base]
            PDF_PROC[pdf_processor.py<br/>PDF Handling]
            XLS_PROC[excel_processor.py<br/>Excel Handling]
            CSV_PROC[csv_processor.py<br/>CSV Handling]
        end

        subgraph "Core Services"
            CONFIG[config.py<br/>Settings]
            MODELS[models.py<br/>Data Models]
            DEPS[dependencies.py<br/>FastAPI Deps]
        end
    end

    subgraph "Data Flow"
        UPLOAD[📤 Upload Process]
        PROCESS[⚙️ Processing Pipeline]
        COMPARE[🔍 Comparison Engine]
        EXPORT[📋 Export Generation]
    end

    INDEX --> MAIN
    MAIN --> API_INT
    MAIN --> DIFF_VIZ
    API_INT --> FILES_ROUTE
    FILES_ROUTE --> PDF_PROC
    FILES_ROUTE --> XLS_PROC
    FILES_ROUTE --> CSV_PROC
    PDF_PROC --> COMP_ROUTE
    XLS_PROC --> COMP_ROUTE
    CSV_PROC --> COMP_ROUTE
```

## 📈 6. Performance Metrics Dashboard

```mermaid
graph LR
    subgraph "Performance Analysis"
        subgraph "Speed Metrics"
            SPEED_TITLE[⚡ Processing Speed]
            PDF_SPEED[📄 PDF: 913 KB/s]
            XLS_SPEED[📊 Excel: 3,261 KB/s]
            AVG_SPEED[📈 Average: 2,087 KB/s]
        end

        subgraph "Efficiency Metrics"
            EFF_TITLE[⏱️ Time Efficiency]
            PDF_EFF[📄 PDF: 0.279s]
            XLS_EFF[📊 Excel: 0.293s]
            AVG_EFF[📈 Average: 0.286s]
        end

        subgraph "Quality Metrics"
            QUAL_TITLE[🎯 Quality Scores]
            TEXT_QUAL[📝 Text Extraction: 92.5%]
            TABLE_QUAL[📋 Table Extraction: 50%]
            STRUCT_QUAL[🏗️ Structure Preservation: 65%]
        end

        subgraph "File Metrics"
            FILE_TITLE[📊 File Analysis]
            SIZE_PDF[📄 PDF: 254KB]
            SIZE_XLS[📊 Excel: 957KB]
            CONTENT_GEN[💾 Content Generated: 115.7KB]
        end
    end

    subgraph "Overall Assessment"
        FINAL_SCORE[🏆 OVERALL SYSTEM SCORE<br/>70.5% ACCURACY<br/>🟡 MODERATE PERFORMANCE]
        RECOMMENDATION[💡 RECOMMENDATION<br/>Immediate improvements required<br/>for production readiness]
    end

    SPEED_TITLE --> FINAL_SCORE
    EFF_TITLE --> FINAL_SCORE
    QUAL_TITLE --> FINAL_SCORE
    FILE_TITLE --> FINAL_SCORE
    FINAL_SCORE --> RECOMMENDATION
```

## 🔧 7. Recommended Improvements Architecture

```mermaid
graph TD
    subgraph "Current State"
        CURRENT[🔴 Current System<br/>70.5% Accuracy]
        ISSUE1[❌ PDF Table Extraction Failed]
        ISSUE2[❌ Excel Header Detection Missing]
        ISSUE3[❌ No Quality Validation]
    end

    subgraph "Phase 1: Immediate Fixes"
        FIX1[🔧 Enhanced PDF Processing<br/>- Multiple table detection algorithms<br/>- OCR for scanned content<br/>- Bilingual support]
        FIX2[🏷️ Smart Excel Headers<br/>- Dynamic header inference<br/>- "Unnamed: X" handling<br/>- Column mapping logic]
        FIX3[✅ Quality Validation Layer<br/>- Data completeness checks<br/>- Conversion accuracy scoring<br/>- Error detection]
    end

    subgraph "Phase 2: Advanced Features"
        ADV1[🤖 ML-Powered Processing<br/>- Document type detection<br/>- Intelligent table recognition<br/>- Context-aware extraction]
        ADV2[🔄 Multi-Strategy Processing<br/>- Fallback algorithms<br/>- Parallel processing<br/>- Result confidence scoring]
        ADV3[📊 Advanced Analytics<br/>- Processing optimization<br/>- Performance monitoring<br/>- Quality metrics dashboard]
    end

    subgraph "Target State"
        TARGET[🟢 Target System<br/>95%+ Accuracy]
        SUCCESS1[✅ Reliable Table Extraction]
        SUCCESS2[✅ Intelligent Data Processing]
        SUCCESS3[✅ Production-Ready Quality]
    end

    CURRENT --> FIX1
    CURRENT --> FIX2
    CURRENT --> FIX3
    
    FIX1 --> ADV1
    FIX2 --> ADV2
    FIX3 --> ADV3
    
    ADV1 --> TARGET
    ADV2 --> TARGET
    ADV3 --> TARGET
```

## 🎯 8. System Flow for File Comparison

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant UI as 🌐 Frontend UI
    participant API as 🚪 API Gateway
    participant FM as 📁 File Manager
    participant P as ⚙️ Processors
    participant C as 🔬 Comparator
    participant S as 💾 Storage

    U->>UI: Upload Files (PDF/Excel/CSV)
    UI->>API: POST /api/files/upload
    API->>FM: Save files
    FM->>S: Store in uploads/
    
    UI->>API: POST /api/files/process/{file_id}
    API->>P: Extract content
    P->>P: Convert to Markdown
    P->>P: Extract structured data
    P->>FM: Return processed data
    FM->>S: Store processed data
    
    UI->>API: POST /api/comparison/compare
    API->>C: Compare structured data
    C->>C: Analyze differences
    C->>FM: Return comparison results
    
    UI->>API: POST /api/comparison/export
    API->>FM: Generate reports
    FM->>S: Save exports
    
    API->>UI: Return results
    UI->>U: Display comparison with diffs
```

## 📊 9. Data Flow Architecture

```mermaid
graph LR
    subgraph "Input Layer"
        INPUT[📥 Raw Input Files<br/>PDF, Excel, CSV]
    end

    subgraph "Processing Layer"
        subgraph "Extraction"
            TEXT[📝 Text Extraction<br/>pandas, pdfplumber]
            TABLE[📋 Table Detection<br/>Algorithm-based]
            META[🏷️ Metadata Capture<br/>File properties]
        end

        subgraph "Normalization"
            CLEAN[🧹 Data Cleaning<br/>Format standardization]
            STRUCT[🏗️ Structure Building<br/>Consistent schema]
            VALID[✅ Validation<br/>Quality checks]
        end
    end

    subgraph "Storage Layer"
        subgraph "Data Stores"
            RAW[📦 Raw Content<br/>Original files]
            PROC[💾 Processed Data<br/>Structured content]
            CACHE[🚀 Cache Layer<br/>Fast access]
        end
    end

    subgraph "Output Layer"
        MD[📄 Markdown Output<br/>Formatted content]
        JSON[🗂️ Structured JSON<br/>Machine-readable]
        REPORT[📊 Comparison Report<br/>Human-readable]
    end

    INPUT --> TEXT
    INPUT --> TABLE
    INPUT --> META
    
    TEXT --> CLEAN
    TABLE --> CLEAN
    META --> CLEAN
    
    CLEAN --> STRUCT
    STRUCT --> VALID
    
    VALID --> RAW
    VALID --> PROC
    VALID --> CACHE
    
    PROC --> MD
    PROC --> JSON
    PROC --> REPORT
```

---

## 📝 Diagram Legend

- **🟢 Green Components:** Working correctly
- **🟡 Yellow Components:** Partial functionality
- **🔴 Red Components:** Critical issues identified
- **⚙️ Blue Components:** Processing elements
- **📊 Purple Components:** Data storage
- **🚪 Orange Components:** API/Interface elements

## 🎯 Key Insights from Diagrams

1. **System Complexity:** Multi-layered architecture with clear separation of concerns
2. **Performance Bottlenecks:** Identified in PDF table extraction and Excel header processing
3. **Scalability Issues:** Current architecture supports scaling but quality control is lacking
4. **Improvement Path:** Clear roadmap from current 70.5% to target 95%+ accuracy

## 📈 Architecture Strengths

✅ **Modular Design:** Clear component separation  
✅ **Async Processing:** Non-blocking operations  
✅ **Multiple Format Support:** Flexible file handling  
✅ **API-First:** RESTful architecture  
✅ **Storage Organization:** Logical file management  

## 🚨 Architecture Weaknesses

❌ **Quality Control:** Missing validation layers  
❌ **Error Recovery:** Limited fallback mechanisms  
❌ **Table Detection:** Poor algorithm performance  
❌ **Data Cleaning:** No normalization processes  
❌ **Monitoring:** Limited observability  

---

**Diagrams Created With:** Mermaid.js  
**Architecture Complexity:** Maximum Depth Analysis  
**Technical Detail:** Component-Level Granularity