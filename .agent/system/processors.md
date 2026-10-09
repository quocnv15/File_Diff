# ⚙️ File Processors Documentation

## Overview
This document describes all file processing components in the system.

---

## csv processor
**File:** `backend/processors/csv_processor.py`
**Class:** `csv processor`

24:    def __init__(self):
29:    async def process(self, file_path: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
92:    def validate_file(self, file_path: str) -> bool:
115:    async def _detect_encoding(self, file_path: str) -> str:
143:    async def _detect_delimiter(self, file_path: str, encoding: str) -> str:

---

## base processor
**File:** `backend/processors/base_processor.py`
**Class:** `base processor`

17:    def __init__(self):
23:    async def process(self, file_path: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
40:    def validate_file(self, file_path: str) -> bool:
52:    def get_processor_info(self) -> Dict[str, Any]:
60:    def _create_markdown_table(self, headers: List[str], rows: List[List[str]]) -> str:

---

## pdf processor
**File:** `backend/processors/pdf_processor.py`
**Class:** `pdf processor`

21:    def __init__(self):
26:    async def process(self, file_path: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
79:    def validate_file(self, file_path: str) -> bool:
102:    async def _convert_pdf_to_markdown(self, file_path: str, options: Dict[str, Any]) -> str:
136:    async def _fallback_pdf_conversion(self, file_path: str, options: Dict[str, Any]) -> str:

---

## excel processor
**File:** `backend/processors/excel_processor.py`
**Class:** `excel processor`

24:    def __init__(self):
32:    async def process(self, file_path: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
88:    def validate_file(self, file_path: str) -> bool:
130:    async def _extract_excel_data(self, file_path: str, options: Dict[str, Any]) -> Dict[str, Any]:
161:    async def _get_workbook_info(self, file_path: str) -> Dict[str, Any]:

---

