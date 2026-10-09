# 📊 Data Models Documentation

## Overview
This document describes all data models used in the system.

---

## Pydantic Models
**File:** `backend/app/models.py`

### ProcessingStatus
11:class ProcessingStatus(str, Enum):

### FileType
20:class FileType(str, Enum):

### DifferenceSeverity
28:class DifferenceSeverity(str, Enum):

### ExportFormat
36:class ExportFormat(str, Enum):

### ComparisonType
44:class ComparisonType(str, Enum):

### FileInfo
53:class FileInfo(BaseModel):

### ProcessingOptions
76:class ProcessingOptions(BaseModel):

### ToleranceSettings
88:class ToleranceSettings(BaseModel):

### ComparisonOptions
97:class ComparisonOptions(BaseModel):

### ComparisonSummary
109:class ComparisonSummary(BaseModel):

### DifferenceDetail
123:class DifferenceDetail(BaseModel):

### ComparisonResult
136:class ComparisonResult(BaseModel):

### ComparisonSummaryResponse
153:class ComparisonSummaryResponse(BaseModel):

### ExportOptions
162:class ExportOptions(BaseModel):

### FormattingOptions
174:class FormattingOptions(BaseModel):

### ExportRequest
183:class ExportRequest(BaseModel):

### ExportResponse
191:class ExportResponse(BaseModel):

### FileUploadResponse
209:class FileUploadResponse(BaseModel):

### FileProcessResponse
215:class FileProcessResponse(BaseModel):

### CompareFilesRequest
221:class CompareFilesRequest(BaseModel):

### CompareFilesResponse
228:class CompareFilesResponse(BaseModel):

### ValidationError
234:class ValidationError(BaseModel):

### APIError
241:class APIError(BaseModel):

### HealthResponse
255:class HealthResponse(BaseModel):

### SupportedFormat
271:class SupportedFormat(BaseModel):

### SupportedFormatsResponse
280:class SupportedFormatsResponse(BaseModel):

### FileValidationRequest
286:class FileValidationRequest(BaseModel):

### FileValidationResponse
294:class FileValidationResponse(BaseModel):

### StatisticsCard
303:class StatisticsCard(BaseModel):

### TableData
310:class TableData(BaseModel):

### TableRow
317:class TableRow(BaseModel):

