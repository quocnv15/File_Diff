# 🚪 API Documentation

## Overview
This document describes all available API endpoints in the File Comparison System.

---

## files
**File:** `backend/api/files.py`

34:@router.post("/upload", response_model=FileUploadResponse, tags=["Files"])
144:@router.post("/{file_id}/process", response_model=FileProcessResponse, tags=["Files"])
277:@router.get("/{file_id}", tags=["Files"])
309:@router.delete("/{file_id}", tags=["Files"])
338:@router.get("/supported-formats", tags=["Files"])
399:@router.post("/validate-file", tags=["Files"])

---

## comparison
**File:** `backend/api/comparison.py`

29:@router.post("/compare", response_model=CompareFilesResponse, tags=["Comparison"])
188:@router.get("/{comparison_id}", tags=["Comparison"])
216:@router.get("/{comparison_id}/summary", response_model=ComparisonSummaryResponse, tags=["Comparison"])
280:@router.delete("/{comparison_id}", tags=["Comparison"])
310:@router.get("/comparison-types", tags=["Comparison"])

---

