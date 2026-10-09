# File Comparison API Endpoints Documentation

## Base Configuration

- **Base URL**: `http://localhost:8000/api`
- **API Version**: v1
- **Content-Type**: `application/json` (except file uploads)
- **File Upload**: `multipart/form-data`
- **Documentation**: `/docs` (Swagger UI)
- **OpenAPI Spec**: `/openapi.json`

## API Endpoints

### Health Check

#### GET `/health`
Check system health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-13T10:00:00Z",
  "version": "1.0.0",
  "storage": {
    "uploads": "available",
    "processed": "available",
    "exports": "available"
  }
}
```

### File Management

#### POST `/files/upload`
Upload files for comparison.

**Request:** `multipart/form-data`
- `file`: File to upload (CSV, Excel, PDF)
- `description`: Optional file description

**Response:**
```json
{
  "file_id": "uuid-string",
  "filename": "example.csv",
  "file_type": "csv",
  "size": 1024,
  "upload_time": "2025-10-13T10:00:00Z",
  "status": "uploaded"
}
```

#### GET `/files/{file_id}`
Get information about uploaded file.

**Response:**
```json
{
  "file_id": "uuid-string",
  "filename": "example.csv",
  "file_type": "csv",
  "size": 1024,
  "upload_time": "2025-10-13T10:00:00Z",
  "status": "processed",
  "rows": 100,
  "columns": 5,
  "preview": [
    {"column1": "value1", "column2": "value2"},
    {"column1": "value3", "column2": "value4"}
  ]
}
```

#### DELETE `/files/{file_id}`
Delete uploaded file.

**Response:**
```json
{
  "message": "File deleted successfully",
  "file_id": "uuid-string"
}
```

### Comparison Operations

#### POST `/comparison/compare`
Compare two uploaded files.

**Request:**
```json
{
  "file1_id": "uuid-string-1",
  "file2_id": "uuid-string-2",
  "comparison_config": {
    "case_sensitive": false,
    "ignore_whitespace": true,
    "compare_columns": ["*"],
    "sensitivity": "medium"
  }
}
```

**Response:**
```json
{
  "comparison_id": "uuid-string",
  "status": "processing",
  "file1_info": {
    "file_id": "uuid-string-1",
    "filename": "file1.csv",
    "rows": 100,
    "columns": 5
  },
  "file2_info": {
    "file_id": "uuid-string-2",
    "filename": "file2.csv",
    "rows": 105,
    "columns": 5
  }
}
```

#### GET `/comparison/{comparison_id}`
Get comparison results.

**Response:**
```json
{
  "comparison_id": "uuid-string",
  "status": "completed",
  "summary": {
    "total_differences": 15,
    "added_rows": 5,
    "removed_rows": 3,
    "modified_cells": 7,
    "accuracy_percentage": 95.5
  },
  "differences": [
    {
      "row": 3,
      "column": "name",
      "file1_value": "John",
      "file2_value": "Jane",
      "difference_type": "modified",
      "severity": "medium"
    }
  ],
  "file1_data": [...],
  "file2_data": [...]
}
```

#### GET `/comparison/{comparison_id}/status`
Check comparison processing status.

**Response:**
```json
{
  "comparison_id": "uuid-string",
  "status": "processing|completed|failed",
  "progress_percentage": 75,
  "estimated_completion": "2025-10-13T10:05:00Z",
  "message": "Processing row 750 of 1000"
}
```

### Export Operations

#### GET `/comparison/{comparison_id}/export`
Export comparison results in different formats.

**Query Parameters:**
- `format`: `excel|pdf|html|json`
- `include_data`: `true|false` (include full data or just differences)

**Response:** File download with appropriate MIME type

**Formats:**
- `excel`: `.xlsx` file with comparison tables and highlighting
- `pdf`: PDF report with comparison summary and highlighted differences
- `html`: HTML report with interactive comparison table
- `json`: JSON format for programmatic use

## Error Handling

### Standard Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid file format",
    "details": {
      "supported_formats": [".csv", ".xlsx", ".xls", ".pdf"],
      "received_format": ".txt"
    }
  },
  "timestamp": "2025-10-13T10:00:00Z",
  "request_id": "uuid-string"
}
```

### Common Error Codes
- `VALIDATION_ERROR`: Invalid input data
- `FILE_NOT_FOUND`: Requested file does not exist
- `FILE_TOO_LARGE`: File exceeds size limit (100MB)
- `UNSUPPORTED_FORMAT`: File format not supported
- `PROCESSING_ERROR`: Error during file processing
- `COMPARISON_ERROR`: Error during comparison
- `STORAGE_ERROR`: File system/storage issue
- `RATE_LIMIT_EXCEEDED`: Too many requests

## Request Limits

- **File Size**: Maximum 100MB per file
- **Concurrent Comparisons**: 5 per user
- **Rate Limiting**: 100 requests per minute
- **Storage Duration**: Files deleted after 24 hours

## Performance Considerations

### Large File Handling
- Files > 10MB processed asynchronously
- Progress tracking available via status endpoint
- Memory-efficient streaming for data processing
- Automatic cleanup of temporary files

### Caching
- Comparison results cached for 1 hour
- File metadata cached for 30 minutes
- Export results cached for 15 minutes

## Integration Examples

### Python Example
```python
import requests
import json

# Upload files
with open('file1.csv', 'rb') as f:
    file1_response = requests.post(
        'http://localhost:8000/api/files/upload',
        files={'file': f}
    )
    file1_id = file1_response.json()['file_id']

# Compare files
comparison_response = requests.post(
    'http://localhost:8000/api/comparison/compare',
    json={
        'file1_id': file1_id,
        'file2_id': file2_id,
        'comparison_config': {
            'case_sensitive': False,
            'ignore_whitespace': True
        }
    }
)
comparison_id = comparison_response.json()['comparison_id']

# Get results
results = requests.get(
    f'http://localhost:8000/api/comparison/{comparison_id}'
)
```

### JavaScript Example
```javascript
// Upload file using FormData
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const uploadResponse = await fetch('/api/files/upload', {
    method: 'POST',
    body: formData
});
const { file_id } = await uploadResponse.json();

// Compare files
const comparisonResponse = await fetch('/api/comparison/compare', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        file1_id: fileId1,
        file2_id: fileId2,
        comparison_config: {
            case_sensitive: false,
            ignore_whitespace: true
        }
    })
});
const { comparison_id } = await comparisonResponse.json();
```

## Related Documentation
- Project Architecture: `system/project_architecture.md`
- File Processing: `system/file_processing.md`
- Development Workflow: `sops/file_comparison_dev_workflow.md`