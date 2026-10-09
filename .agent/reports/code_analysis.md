# 🧠 Code Components Analysis

*Generated on 2025-10-15 21:56:34*

## 📊 Summary

- **Total Components**: 496
- **Classes**: 72
- **Functions**: 424
- **Average Complexity**: 7.1

---

## Functions

### create_product_comparison_csv
**File:** `archive/tests/create_test_csv.py:11`
**Complexity:** 3
**Documentation:**
```
Create CSV files with product comparison data
```
**Dependencies:** open, writer, writerows, join

---

### create_invoice_csv
**File:** `archive/tests/create_test_csv.py:46`
**Complexity:** 3
**Documentation:**
```
Create CSV files with invoice data
```
**Dependencies:** open, writer, writerows, join

---

### create_edge_cases_csv
**File:** `archive/tests/create_test_csv.py:80`
**Complexity:** 2
**Documentation:**
```
Create CSV file with edge cases
```
**Dependencies:** open, writer, writerows, join

---

### create_decimal_precision_csv
**File:** `archive/tests/create_test_csv.py:101`
**Complexity:** 2
**Documentation:**
```
Create CSV file to test decimal precision
```
**Dependencies:** open, writer, writerows, join

---

### create_different_delimiters_csv
**File:** `archive/tests/create_test_csv.py:119`
**Complexity:** 3
**Documentation:**
```
Create CSV files with different delimiters
```
**Dependencies:** open, writer, writerows, join

---

### create_large_dataset_csv
**File:** `archive/tests/create_test_csv.py:148`
**Complexity:** 3
**Documentation:**
```
Create large CSV file for performance testing
```
**Dependencies:** append, writer, open, range, len
*...and 3 more*

---

### create_product_comparison_excel
**File:** `archive/tests/create_test_excel.py:13`
**Complexity:** 2
**Documentation:**
```
Create Excel file with product comparison data
```
**Dependencies:** DataFrame, to_excel, ExcelWriter, join

---

### create_invoice_excel
**File:** `archive/tests/create_test_excel.py:136`
**Complexity:** 3
**Documentation:**
```
Create Excel file with invoice data
```
**Dependencies:** DataFrame, to_excel, ExcelWriter, join

---

### create_multi_sheet_excel
**File:** `archive/tests/create_test_excel.py:271`
**Complexity:** 2
**Documentation:**
```
Create Excel file with multiple sheets for complex testing
```
**Dependencies:** DataFrame, to_excel, ExcelWriter, join

---

### create_edge_cases_excel
**File:** `archive/tests/create_test_excel.py:322`
**Complexity:** 1
**Documentation:**
```
Create Excel file with edge cases
```
**Dependencies:** DataFrame, to_excel, join

---

### create_decimal_precision_excel
**File:** `archive/tests/create_test_excel.py:394`
**Complexity:** 1
**Documentation:**
```
Create Excel file to test decimal precision
```
**Dependencies:** DataFrame, to_excel, join

---

### create_product_comparison_pdf1
**File:** `archive/tests/create_test_pdfs.py:19`
**Complexity:** 1
**Documentation:**
```
Create first product comparison PDF
```
**Dependencies:** append, build, setStyle, Spacer, getSampleStyleSheet
*...and 5 more*

---

### create_product_comparison_pdf2
**File:** `archive/tests/create_test_pdfs.py:82`
**Complexity:** 1
**Documentation:**
```
Create second product comparison PDF with differences
```
**Dependencies:** append, build, setStyle, Spacer, getSampleStyleSheet
*...and 5 more*

---

### create_invoice_pdf1
**File:** `archive/tests/create_test_pdfs.py:144`
**Complexity:** 1
**Documentation:**
```
Create first invoice PDF
```
**Dependencies:** append, build, setStyle, Spacer, getSampleStyleSheet
*...and 5 more*

---

### create_invoice_pdf2
**File:** `archive/tests/create_test_pdfs.py:225`
**Complexity:** 1
**Documentation:**
```
Create second invoice PDF with differences
```
**Dependencies:** append, build, setStyle, Spacer, getSampleStyleSheet
*...and 5 more*

---

### create_multi_table_pdf
**File:** `archive/tests/create_test_pdfs.py:307`
**Complexity:** 1
**Documentation:**
```
Create PDF with multiple tables for complex testing
```
**Dependencies:** append, build, setStyle, Spacer, getSampleStyleSheet
*...and 5 more*

---

### create_edge_case_pdf
**File:** `archive/tests/create_test_pdfs.py:400`
**Complexity:** 1
**Documentation:**
```
Create PDF with edge cases (empty cells, special characters, etc.)
```
**Dependencies:** append, build, setStyle, Spacer, getSampleStyleSheet
*...and 5 more*

---

### test_health_endpoint
**File:** `archive/tests/demo_api_test.py:20`
**Complexity:** 4
**Documentation:**
```
Test health check endpoint
```
**Dependencies:** print, json, get

---

### test_root_endpoint
**File:** `archive/tests/demo_api_test.py:55`
**Complexity:** 3
**Documentation:**
```
Test root endpoint
```
**Dependencies:** print, json, get

---

### test_supported_formats
**File:** `archive/tests/demo_api_test.py:79`
**Complexity:** 9
**Documentation:**
```
Test supported formats endpoint
```
**Dependencies:** print, get, len, json, join

---

### test_comparison_types
**File:** `archive/tests/demo_api_test.py:119`
**Complexity:** 6
**Documentation:**
```
Test comparison types endpoint
```
**Dependencies:** len, print, json, get

---

### test_file_validation
**File:** `archive/tests/demo_api_test.py:154`
**Complexity:** 10
**Documentation:**
```
Test file validation endpoint
```
**Dependencies:** print, get, startswith, json, join
*...and 1 more*

---

### test_error_handling
**File:** `archive/tests/demo_api_test.py:239`
**Complexity:** 7
**Documentation:**
```
Test error handling with invalid endpoints
```
**Dependencies:** isinstance, print, get, post

---

### test_response_times
**File:** `archive/tests/demo_api_test.py:299`
**Complexity:** 8
**Documentation:**
```
Test API response times
```
**Dependencies:** print, total_seconds, append, get, min
*...and 4 more*

---

### main
**File:** `archive/tests/demo_api_test.py:353`
**Complexity:** 6
**Documentation:**
```
Run all API demo tests
```
**Dependencies:** test_func, print, append, len

---

### create_sample_csv_file
**File:** `archive/tests/demo_file_processing_test.py:19`
**Complexity:** 2
**Documentation:**
```
Create a sample CSV file for testing
```
**Dependencies:** print, writer, mkdtemp, open, len
*...and 2 more*

---

### test_csv_processor
**File:** `archive/tests/demo_file_processing_test.py:47`
**Complexity:** 12
**Documentation:**
```
Test CSV processor functionality
```
**Dependencies:** print, validate_file, rmtree, get, split
*...and 7 more*

---

### test_data_comparison
**File:** `archive/tests/demo_file_processing_test.py:116`
**Complexity:** 6
**Documentation:**
```
Test data comparison functionality
```
**Dependencies:** run_comparison, print, close, get, set_event_loop
*...and 5 more*

---

### test_file_operations
**File:** `archive/tests/demo_file_processing_test.py:191`
**Complexity:** 4
**Documentation:**
```
Test file operation utilities
```
**Dependencies:** calculate_file_hash, print, generate_file_id, is_supported_file, get_file_type_from_content
*...and 1 more*

---

### test_error_handling
**File:** `archive/tests/demo_file_processing_test.py:253`
**Complexity:** 5
**Documentation:**
```
Test error handling functionality
```
**Dependencies:** print, CorruptedFileError, FileSizeExceededError, create_http_exception, UnsupportedFileTypeError

---

### test_configuration
**File:** `archive/tests/demo_file_processing_test.py:299`
**Complexity:** 3
**Documentation:**
```
Test configuration loading
```
**Dependencies:** print, get_settings, exists, create_directories

---

### main
**File:** `archive/tests/demo_file_processing_test.py:347`
**Complexity:** 6
**Documentation:**
```
Run all file processing demo tests
```
**Dependencies:** test_func, print, append, len

---

### test_logging_basic
**File:** `archive/tests/demo_logging_test.py:16`
**Complexity:** 2
**Documentation:**
```
Test basic logging functionality
```
**Dependencies:** print, start_process, get_process_logger, end_process, log_step

---

### test_file_operations
**File:** `archive/tests/demo_logging_test.py:50`
**Complexity:** 2
**Documentation:**
```
Test file operation logging
```
**Dependencies:** isoformat, print, log_file_operation, now

---

### test_comparison_operations
**File:** `archive/tests/demo_logging_test.py:96`
**Complexity:** 2
**Documentation:**
```
Test comparison operation logging
```
**Dependencies:** log_comparison_operation, print

---

### test_error_logging
**File:** `archive/tests/demo_logging_test.py:145`
**Complexity:** 3
**Documentation:**
```
Test error logging functionality
```
**Dependencies:** print, start_process, get_process_logger, end_process, ValueError
*...and 2 more*

---

### test_nested_processes
**File:** `archive/tests/demo_logging_test.py:186`
**Complexity:** 2
**Documentation:**
```
Test nested process logging
```
**Dependencies:** print, start_process, get_process_logger, end_process, log_step

---

### test_performance_logging
**File:** `archive/tests/demo_logging_test.py:227`
**Complexity:** 2
**Documentation:**
```
Test performance logging with timing
```
**Dependencies:** print, start_process, get_process_logger, end_process, sleep

---

### main
**File:** `archive/tests/demo_logging_test.py:262`
**Complexity:** 6
**Documentation:**
```
Run all demo tests
```
**Dependencies:** test_func, print, append, len

---

### __init__
**File:** `archive/tests/test_api_comparisons.py:21`
**Complexity:** 1
**Dependencies:** cwd, TestClient

---

### print_summary
**File:** `archive/tests/test_api_comparisons.py:211`
**Complexity:** 6
**Documentation:**
```
Print API comparison test summary
```
**Dependencies:** sum, print, len

---

### __init__
**File:** `archive/tests/test_comparison_functionality.py:24`
**Complexity:** 1
**Dependencies:** ExcelProcessor, Path, PDFProcessor, CSVProcessor, DataComparator

---

### print_summary
**File:** `archive/tests/test_comparison_functionality.py:296`
**Complexity:** 18
**Documentation:**
```
Print comparison test summary
```
**Dependencies:** isinstance, print, abs, sum, len

---

### __init__
**File:** `archive/tests/test_comparison_types.py:24`
**Complexity:** 1
**Dependencies:** cwd, ExcelProcessor, PDFProcessor, CSVProcessor, DataComparator

---

### print_summary
**File:** `archive/tests/test_comparison_types.py:252`
**Complexity:** 10
**Documentation:**
```
Print comprehensive comparison test summary
```
**Dependencies:** print, upper, sum, items, len

---

### __init__
**File:** `archive/tests/test_file_processing.py:23`
**Complexity:** 1
**Dependencies:** CSVProcessor, ExcelProcessor, Path, PDFProcessor

---

### print_summary
**File:** `archive/tests/test_file_processing.py:140`
**Complexity:** 9
**Documentation:**
```
Print test summary
```
**Dependencies:** print, upper, split, lower, sum
*...and 2 more*

---

### __init__
**File:** `archive/tests/test_master_suite.py:27`
**Complexity:** 1
**Dependencies:** ExcelProcessor, get_process_logger, Path, PDFProcessor, CSVProcessor
*...and 1 more*

---

### log_test
**File:** `archive/tests/test_master_suite.py:47`
**Complexity:** 8
**Documentation:**
```
Log test result
```
**Dependencies:** isinstance, print, append, upper, isoformat
*...and 2 more*

---

### generate_report
**File:** `archive/tests/test_master_suite.py:351`
**Complexity:** 17
**Documentation:**
```
Generate comprehensive test report
```
**Dependencies:** print, upper, get, time, isoformat
*...and 5 more*

---

### __init__
**File:** `archive/tests/test_new_samples.py:30`
**Complexity:** 1
**Dependencies:** ExcelProcessor, get_process_logger, Path, PDFProcessor, CSVProcessor
*...and 1 more*

---

### log_test_result
**File:** `archive/tests/test_new_samples.py:47`
**Complexity:** 5
**Documentation:**
```
Log test result
```
**Dependencies:** items, print, append

---

### print_summary
**File:** `archive/tests/test_new_samples.py:450`
**Complexity:** 10
**Documentation:**
```
Print test summary
```
**Dependencies:** split, items, print, get

---

### _create_file_info
**File:** `backend/api/routes/comparison.py:449`
**Complexity:** 1
**Documentation:**
```
Create file info object
```
**Dependencies:** FileInfo, len, now, get

---

### get_settings
**File:** `backend/app/config.py:83`
**Complexity:** 1
**Documentation:**
```
Get application settings
```

---

### create_directories
**File:** `backend/app/config.py:88`
**Complexity:** 4
**Documentation:**
```
Create necessary directories if they don't exist
```
**Dependencies:** dirname, makedirs, exists

---

### get_storage_path
**File:** `backend/app/dependencies.py:104`
**Complexity:** 1
**Documentation:**
```
Get storage path based on file type
```
**Dependencies:** get

---

### get_file_extension
**File:** `backend/app/dependencies.py:133`
**Complexity:** 1
**Documentation:**
```
Get file extension from filename
```
**Dependencies:** split, lower

---

### is_supported_file
**File:** `backend/app/dependencies.py:138`
**Complexity:** 2
**Documentation:**
```
Check if file is supported
```
**Dependencies:** get_file_extension

---

### create_application
**File:** `backend/app/main.py:58`
**Complexity:** 1
**Documentation:**
```
Create and configure FastAPI application
```
**Dependencies:** setup_events, setup_routes, setup_middleware, setup_exception_handlers, FastAPI

---

### setup_middleware
**File:** `backend/app/main.py:85`
**Complexity:** 2
**Documentation:**
```
Setup application middleware
```
**Dependencies:** middleware, add_middleware

---

### setup_exception_handlers
**File:** `backend/app/main.py:105`
**Complexity:** 1
**Documentation:**
```
Setup exception handlers
```
**Dependencies:** exception_handler, getattr, JSONResponse, isoformat, error
*...and 2 more*

---

### setup_routes
**File:** `backend/app/main.py:161`
**Complexity:** 10
**Documentation:**
```
Setup application routes
```
**Dependencies:** insert, error, HealthResponse, now, get
*...and 14 more*

---

### setup_events
**File:** `backend/app/main.py:284`
**Complexity:** 1
**Documentation:**
```
Setup application startup and shutdown events
```

---

### round_accuracy_rate
**File:** `backend/app/models.py:119`
**Complexity:** 1
**Dependencies:** round

---

### __init__
**File:** `backend/comparators/base_comparator.py:17`
**Complexity:** 1
**Dependencies:** get_process_logger

---

### _normalize_value
**File:** `backend/comparators/base_comparator.py:40`
**Complexity:** 4
**Documentation:**
```
Normalize value for comparison
```
**Dependencies:** isinstance, strip, float, lower, str

---

### _is_numeric
**File:** `backend/comparators/base_comparator.py:51`
**Complexity:** 2
**Documentation:**
```
Check if value is numeric
```
**Dependencies:** float

---

### _parse_numeric
**File:** `backend/comparators/base_comparator.py:59`
**Complexity:** 3
**Documentation:**
```
Parse value as number
```
**Dependencies:** replace, isinstance, strip, float

---

### _compare_numbers
**File:** `backend/comparators/base_comparator.py:70`
**Complexity:** 5
**Documentation:**
```
Compare two numbers with tolerance
```
**Dependencies:** max, abs

---

### _calculate_percentage_difference
**File:** `backend/comparators/base_comparator.py:80`
**Complexity:** 4
**Documentation:**
```
Calculate percentage difference between two numbers
```
**Dependencies:** abs

---

### _determine_severity
**File:** `backend/comparators/base_comparator.py:89`
**Complexity:** 11
**Documentation:**
```
Determine severity level of difference
```
**Dependencies:** any, lower

---

### get_comparator_info
**File:** `backend/comparators/base_comparator.py:119`
**Complexity:** 1
**Documentation:**
```
Get comparator information
```

---

### __init__
**File:** `backend/comparators/data_comparator.py:24`
**Complexity:** 1
**Dependencies:** __init__, super

---

### _extract_table_data
**File:** `backend/comparators/data_comparator.py:74`
**Complexity:** 4
**Documentation:**
```
Extract table data from structured data
```
**Dependencies:** error, get

---

### _values_match
**File:** `backend/comparators/data_comparator.py:239`
**Complexity:** 9
**Documentation:**
```
Check if two values match based on field type and comparison options
```
**Dependencies:** strip, _is_numeric, _compare_numbers, lower, _get_field_tolerance
*...and 3 more*

---

### _get_field_tolerance
**File:** `backend/comparators/data_comparator.py:268`
**Complexity:** 3
**Documentation:**
```
Get tolerance setting for a specific field
```
**Dependencies:** items, lower

---

### _create_difference_detail
**File:** `backend/comparators/data_comparator.py:280`
**Complexity:** 6
**Documentation:**
```
Create a difference detail object
```
**Dependencies:** _is_numeric, DifferenceDetail, abs, DifferenceSeverity, _determine_severity
*...and 4 more*

---

### _get_max_severity
**File:** `backend/comparators/data_comparator.py:317`
**Complexity:** 4
**Documentation:**
```
Get maximum severity from list of differences
```
**Dependencies:** get

---

### _apply_field_mapping
**File:** `backend/comparators/data_comparator.py:336`
**Complexity:** 1
**Documentation:**
```
Apply custom field mapping
```

---

### __init__
**File:** `backend/comparators/diff_analyzer.py:17`
**Complexity:** 1

---

### analyze_differences
**File:** `backend/comparators/diff_analyzer.py:25`
**Complexity:** 7
**Documentation:**
```
Analyze differences and return summary statistics
```
**Dependencies:** get, values, sum, len, _generate_summary
*...and 2 more*

---

### _generate_summary
**File:** `backend/comparators/diff_analyzer.py:74`
**Complexity:** 10
**Documentation:**
```
Generate human-readable summary of differences
```
**Dependencies:** append, get, error, max, join

---

### categorize_differences
**File:** `backend/comparators/diff_analyzer.py:113`
**Complexity:** 4
**Documentation:**
```
Categorize differences by type and severity
```
**Dependencies:** append, error, str

---

### get_field_analysis
**File:** `backend/comparators/diff_analyzer.py:134`
**Complexity:** 8
**Documentation:**
```
Get detailed analysis for each field
```
**Dependencies:** append, _is_numeric_difference, sum, _get_max_severity, items
*...and 5 more*

---

### _is_numeric_difference
**File:** `backend/comparators/diff_analyzer.py:186`
**Complexity:** 2
**Documentation:**
```
Check if difference is numeric
```

---

### _get_max_severity
**File:** `backend/comparators/diff_analyzer.py:190`
**Complexity:** 4
**Documentation:**
```
Get maximum severity from differences
```
**Dependencies:** get

---

### generate_recommendations
**File:** `backend/comparators/diff_analyzer.py:209`
**Complexity:** 12
**Documentation:**
```
Generate recommendations based on differences
```
**Dependencies:** append, get, get_field_analysis, categorize_differences, items
*...and 1 more*

---

### create_comparison_report
**File:** `backend/comparators/diff_analyzer.py:250`
**Complexity:** 2
**Documentation:**
```
Create comprehensive comparison report
```
**Dependencies:** analyze_differences, get_field_analysis, isoformat, _get_top_issues, categorize_differences
*...and 4 more*

---

### _get_top_issues
**File:** `backend/comparators/diff_analyzer.py:276`
**Complexity:** 4
**Documentation:**
```
Get top issues based on severity and impact
```
**Dependencies:** append, sorted, error, get

---

### __init__
**File:** `backend/processors/base_processor.py:17`
**Complexity:** 1
**Dependencies:** get_process_logger

---

### validate_file
**File:** `backend/processors/base_processor.py:40`
**Complexity:** 1
**Documentation:**
```
Validate if file can be processed by this processor

Args:
    file_path: Path to the file to validate

Returns:
    True if file can be processed, False otherwise
```

---

### get_processor_info
**File:** `backend/processors/base_processor.py:52`
**Complexity:** 1
**Documentation:**
```
Get processor information
```

---

### _create_markdown_table
**File:** `backend/processors/base_processor.py:60`
**Complexity:** 7
**Documentation:**
```
Create markdown table from headers and rows
```
**Dependencies:** ljust, append, range, len, enumerate
*...and 3 more*

---

### _extract_metadata
**File:** `backend/processors/base_processor.py:97`
**Complexity:** 2
**Documentation:**
```
Extract basic metadata from file
```
**Dependencies:** stat, start_process, end_process, isoformat, log_step
*...and 5 more*

---

### __init__
**File:** `backend/processors/csv_processor.py:24`
**Complexity:** 1
**Dependencies:** __init__, super

---

### validate_file
**File:** `backend/processors/csv_processor.py:92`
**Complexity:** 6
**Documentation:**
```
Validate CSV file
```
**Dependencies:** endswith, exists, open, lower, read
*...and 1 more*

---

### _clean_dataframe
**File:** `backend/processors/csv_processor.py:224`
**Complexity:** 3
**Documentation:**
```
Clean and prepare DataFrame
```
**Dependencies:** all, strip, eq, apply, astype
*...and 2 more*

---

### _format_cell_value
**File:** `backend/processors/csv_processor.py:244`
**Complexity:** 6
**Documentation:**
```
Format cell value for display
```
**Dependencies:** str, isinstance, strip, isna

---

### _convert_to_markdown
**File:** `backend/processors/csv_processor.py:257`
**Complexity:** 5
**Documentation:**
```
Convert CSV data to Markdown
```
**Dependencies:** append, get, pop, len, error
*...and 3 more*

---

### _create_structured_data
**File:** `backend/processors/csv_processor.py:299`
**Complexity:** 4
**Documentation:**
```
Create structured data from CSV data
```
**Dependencies:** len, append, error, get

---

### _extract_csv_metadata
**File:** `backend/processors/csv_processor.py:322`
**Complexity:** 2
**Documentation:**
```
Extract CSV-specific metadata
```
**Dependencies:** update, stat, _detect_line_ending, error

---

### _detect_line_ending
**File:** `backend/processors/csv_processor.py:340`
**Complexity:** 6
**Documentation:**
```
Detect line ending format
```
**Dependencies:** read, open, error

---

### __init__
**File:** `backend/processors/excel_processor.py:24`
**Complexity:** 1
**Dependencies:** __init__, super

---

### validate_file
**File:** `backend/processors/excel_processor.py:88`
**Complexity:** 9
**Documentation:**
```
Validate Excel file
```
**Dependencies:** close, exists, Path, load_workbook, lower
*...and 3 more*

---

### _get_sheet_names
**File:** `backend/processors/excel_processor.py:189`
**Complexity:** 3
**Documentation:**
```
Get all sheet names from Excel file
```
**Dependencies:** close, endswith, load_workbook, ExcelFile, error

---

### _clean_dataframe
**File:** `backend/processors/excel_processor.py:246`
**Complexity:** 13
**Documentation:**
```
Clean and prepare DataFrame
```
**Dependencies:** all, fillna, iterrows, any, strip
*...and 9 more*

---

### _format_cell_value
**File:** `backend/processors/excel_processor.py:297`
**Complexity:** 7
**Documentation:**
```
Format cell value for display
```
**Dependencies:** isinstance, strip, int, str, isna
*...and 1 more*

---

### _convert_to_markdown
**File:** `backend/processors/excel_processor.py:314`
**Complexity:** 7
**Documentation:**
```
Convert Excel data to Markdown
```
**Dependencies:** append, _create_markdown_table, get, pop, items
*...and 4 more*

---

### _create_structured_data
**File:** `backend/processors/excel_processor.py:361`
**Complexity:** 5
**Documentation:**
```
Create structured data from Excel data
```
**Dependencies:** append, get, len, items, error

---

### _extract_excel_metadata
**File:** `backend/processors/excel_processor.py:384`
**Complexity:** 4
**Documentation:**
```
Extract Excel-specific metadata
```
**Dependencies:** getattr, hasattr, close, Path, load_workbook
*...and 5 more*

---

### __init__
**File:** `backend/processors/pdf_processor.py:21`
**Complexity:** 1
**Dependencies:** __init__, super

---

### validate_file
**File:** `backend/processors/pdf_processor.py:79`
**Complexity:** 6
**Documentation:**
```
Validate PDF file
```
**Dependencies:** endswith, exists, open, lower, read
*...and 2 more*

---

### _create_placeholder_markdown
**File:** `backend/processors/pdf_processor.py:171`
**Complexity:** 1
**Documentation:**
```
Create placeholder Markdown when PDF conversion fails
```
**Dependencies:** getsize, time, Path, str, hash

---

### _parse_markdown_to_structured_data
**File:** `backend/processors/pdf_processor.py:210`
**Complexity:** 21
**Documentation:**
```
Parse Markdown content to extract structured data
```
**Dependencies:** info, all, extend, append, strip
*...and 6 more*

---

### _parse_invoice_structure
**File:** `backend/processors/pdf_processor.py:295`
**Complexity:** 14
**Documentation:**
```
Parse invoice-like structure from PDF content
```
**Dependencies:** info, all, strip, upper, print_exc
*...and 5 more*

---

### _looks_like_data_row
**File:** `backend/processors/pdf_processor.py:373`
**Complexity:** 7
**Documentation:**
```
Check if a line looks like invoice data row
```
**Dependencies:** strip, upper, any, isdigit, lower
*...and 2 more*

---

### _parse_invoice_row
**File:** `backend/processors/pdf_processor.py:395`
**Complexity:** 10
**Documentation:**
```
Parse a single invoice row into columns
```
**Dependencies:** start, append, strip, group, split
*...and 6 more*

---

### _parse_columnar_data
**File:** `backend/processors/pdf_processor.py:441`
**Complexity:** 5
**Documentation:**
```
Parse column-based invoice data where items and values are on separate lines
```
**Dependencies:** info, _reconstruct_columnar_table, append, strip, any
*...and 4 more*

---

### _reconstruct_columnar_table
**File:** `backend/processors/pdf_processor.py:466`
**Complexity:** 32
**Documentation:**
```
Reconstruct table from columnar PDF layout
```
**Dependencies:** info, append, isdigit, print_exc, range
*...and 8 more*

---

### _parse_single_item
**File:** `backend/processors/pdf_processor.py:577`
**Complexity:** 14
**Documentation:**
```
Parse a single item's data from its component lines
```
**Dependencies:** append, isdigit, _looks_like_product_description, lower, len
*...and 4 more*

---

### _parse_by_pattern_detection
**File:** `backend/processors/pdf_processor.py:629`
**Complexity:** 10
**Documentation:**
```
Alternative parsing method when sequence numbers aren't clear
```
**Dependencies:** append, _parse_single_item, _looks_like_product_description, lower, len
*...and 2 more*

---

### _looks_like_product_description
**File:** `backend/processors/pdf_processor.py:664`
**Complexity:** 4
**Documentation:**
```
Check if line looks like a product description
```
**Dependencies:** len, lower, any, _is_number

---

### _normalize_row_data
**File:** `backend/processors/pdf_processor.py:682`
**Complexity:** 17
**Documentation:**
```
Normalize row data to have consistent columns
```
**Dependencies:** append, isdigit, lower, len, enumerate
*...and 4 more*

---

### _is_number
**File:** `backend/processors/pdf_processor.py:735`
**Complexity:** 2
**Documentation:**
```
Check if text represents a number
```
**Dependencies:** replace, strip, float

---

### _extract_pdf_metadata
**File:** `backend/processors/pdf_processor.py:745`
**Complexity:** 5
**Documentation:**
```
Extract PDF-specific metadata
```
**Dependencies:** hasattr, get, open, PdfReader, len
*...and 3 more*

---

### run_command
**File:** `backend/run_tests.py:12`
**Complexity:** 4
**Documentation:**
```
Run a command and handle the result
```
**Dependencies:** print, run, join

---

### main
**File:** `backend/run_tests.py:34`
**Complexity:** 13
**Documentation:**
```
Main test runner
```
**Dependencies:** extend, chdir, append, print, add_argument
*...and 6 more*

---

### test_file_structure
**File:** `backend/simple_test.py:9`
**Complexity:** 4
**Documentation:**
```
Test that all required files and directories exist
```
**Dependencies:** print, append, exists

---

### test_sample_files
**File:** `backend/simple_test.py:47`
**Complexity:** 2
**Documentation:**
```
Test that sample files exist
```
**Dependencies:** print, any, endswith, exists, listdir

---

### test_basic_logic
**File:** `backend/simple_test.py:68`
**Complexity:** 8
**Documentation:**
```
Test basic comparison logic without external dependencies
```
**Dependencies:** compare_numbers, print, abs, max

---

### compare_numbers
**File:** `backend/simple_test.py:74`
**Complexity:** 5
**Dependencies:** max, abs

---

### test_project_structure
**File:** `backend/simple_test.py:107`
**Complexity:** 3
**Documentation:**
```
Test overall project structure
```
**Dependencies:** exists, print, join

---

### main
**File:** `backend/simple_test.py:131`
**Complexity:** 4
**Documentation:**
```
Run all tests
```
**Dependencies:** test, print, len

---

### mock_file_data
**File:** `backend/tests/conftest.py:17`
**Complexity:** 1
**Documentation:**
```
Mock file data for testing
```

---

### mock_structured_data
**File:** `backend/tests/conftest.py:30`
**Complexity:** 1
**Documentation:**
```
Mock structured data for testing
```

---

### mock_comparison_result
**File:** `backend/tests/conftest.py:46`
**Complexity:** 1
**Documentation:**
```
Mock comparison result for testing
```

---

### mock_user
**File:** `backend/tests/conftest.py:74`
**Complexity:** 1
**Documentation:**
```
Mock authenticated user
```
**Dependencies:** now

---

### temp_file
**File:** `backend/tests/conftest.py:86`
**Complexity:** 3
**Documentation:**
```
Create a temporary file for testing
```
**Dependencies:** exists, Path, open, gettempdir, write
*...and 1 more*

---

### mock_logger
**File:** `backend/tests/conftest.py:98`
**Complexity:** 1
**Documentation:**
```
Mock logger for testing
```
**Dependencies:** Mock

---

### sample_log_entries
**File:** `backend/tests/conftest.py:109`
**Complexity:** 1
**Documentation:**
```
Sample log entries for testing
```
**Dependencies:** isoformat, now

---

### create_excel_data
**File:** `backend/tests/conftest.py:136`
**Complexity:** 2
**Documentation:**
```
Create mock Excel data
```
**Dependencies:** append, range

---

### create_csv_data
**File:** `backend/tests/conftest.py:148`
**Complexity:** 2
**Documentation:**
```
Create mock CSV data
```
**Dependencies:** str, append, range, join

---

### create_mock_file
**File:** `backend/tests/conftest.py:165`
**Complexity:** 1
**Documentation:**
```
Create mock file data
```
**Dependencies:** uuid4, update, now, str

---

### create_mock_comparison_result
**File:** `backend/tests/conftest.py:180`
**Complexity:** 1
**Documentation:**
```
Create mock comparison result
```
**Dependencies:** uuid4, update, str

---

### test_data_factory
**File:** `backend/tests/conftest.py:200`
**Complexity:** 1
**Documentation:**
```
Provide test data factory
```

---

### pytest_configure
**File:** `backend/tests/conftest.py:206`
**Complexity:** 1
**Documentation:**
```
Register custom markers
```
**Dependencies:** addinivalue_line

---

### client
**File:** `backend/tests/test_api_endpoints.py:28`
**Complexity:** 1
**Documentation:**
```
Create test client
```
**Dependencies:** TestClient

---

### mock_user
**File:** `backend/tests/test_api_endpoints.py:33`
**Complexity:** 1
**Documentation:**
```
Mock authenticated user
```

---

### sample_excel_file
**File:** `backend/tests/test_api_endpoints.py:42`
**Complexity:** 2
**Documentation:**
```
Create sample Excel file for testing
```
**Dependencies:** NamedTemporaryFile, write, close, unlink

---

### test_file_upload_success
**File:** `backend/tests/test_api_endpoints.py:62`
**Complexity:** 2
**Documentation:**
```
Test successful file upload
```
**Dependencies:** patch, open, json, post

---

### test_file_upload_no_file
**File:** `backend/tests/test_api_endpoints.py:99`
**Complexity:** 1
**Documentation:**
```
Test file upload with no file provided
```
**Dependencies:** patch, json, post

---

### test_file_upload_unsupported_type
**File:** `backend/tests/test_api_endpoints.py:115`
**Complexity:** 1
**Documentation:**
```
Test file upload with unsupported file type
```
**Dependencies:** patch, json, post

---

### test_get_supported_formats
**File:** `backend/tests/test_api_endpoints.py:130`
**Complexity:** 1
**Documentation:**
```
Test getting supported file formats
```
**Dependencies:** json, get

---

### test_validate_file_success
**File:** `backend/tests/test_api_endpoints.py:147`
**Complexity:** 1
**Documentation:**
```
Test file validation with valid file
```
**Dependencies:** patch, json, post

---

### test_process_file_success
**File:** `backend/tests/test_api_endpoints.py:167`
**Complexity:** 1
**Documentation:**
```
Test successful file processing
```
**Dependencies:** patch, json, post

---

### client
**File:** `backend/tests/test_api_endpoints.py:198`
**Complexity:** 1
**Documentation:**
```
Create test client
```
**Dependencies:** TestClient

---

### mock_user
**File:** `backend/tests/test_api_endpoints.py:203`
**Complexity:** 1
**Documentation:**
```
Mock authenticated user
```

---

### sample_comparison_request
**File:** `backend/tests/test_api_endpoints.py:212`
**Complexity:** 1
**Documentation:**
```
Sample comparison request data
```

---

### mock_file_data
**File:** `backend/tests/test_api_endpoints.py:230`
**Complexity:** 1
**Documentation:**
```
Mock file data for comparison
```

---

### test_compare_files_success
**File:** `backend/tests/test_api_endpoints.py:253`
**Complexity:** 1
**Documentation:**
```
Test successful file comparison
```
**Dependencies:** AsyncMock, Mock, patch, json, post

---

### test_compare_files_missing_ids
**File:** `backend/tests/test_api_endpoints.py:301`
**Complexity:** 1
**Documentation:**
```
Test comparison with missing file IDs
```
**Dependencies:** patch, json, post

---

### test_compare_files_same_file
**File:** `backend/tests/test_api_endpoints.py:317`
**Complexity:** 1
**Documentation:**
```
Test comparison with same file IDs
```
**Dependencies:** patch, json, post

---

### test_get_comparison_types
**File:** `backend/tests/test_api_endpoints.py:332`
**Complexity:** 2
**Documentation:**
```
Test getting available comparison types
```
**Dependencies:** isinstance, json, get

---

### client
**File:** `backend/tests/test_api_endpoints.py:364`
**Complexity:** 1
**Documentation:**
```
Create test client
```
**Dependencies:** TestClient

---

### test_health_check
**File:** `backend/tests/test_api_endpoints.py:368`
**Complexity:** 2
**Documentation:**
```
Test health check endpoint
```
**Dependencies:** patch, json, get

---

### test_root_endpoint
**File:** `backend/tests/test_api_endpoints.py:390`
**Complexity:** 1
**Documentation:**
```
Test root endpoint
```
**Dependencies:** json, get

---

### setup_method
**File:** `backend/tests/test_core_functionality.py:19`
**Complexity:** 1
**Documentation:**
```
Setup test logger
```
**Dependencies:** ProcessLogger

---

### test_start_process
**File:** `backend/tests/test_core_functionality.py:24`
**Complexity:** 1
**Documentation:**
```
Test starting a new process
```
**Dependencies:** len, start_process

---

### test_end_process
**File:** `backend/tests/test_core_functionality.py:33`
**Complexity:** 2
**Documentation:**
```
Test ending a process
```
**Dependencies:** object, start_process, end_process, assert_called_once, len

---

### test_log_step
**File:** `backend/tests/test_core_functionality.py:47`
**Complexity:** 2
**Documentation:**
```
Test logging a step
```
**Dependencies:** log_step, object, assert_called_once, start_process

---

### test_log_error
**File:** `backend/tests/test_core_functionality.py:59`
**Complexity:** 2
**Documentation:**
```
Test error logging
```
**Dependencies:** object, start_process, ValueError, assert_called_once, log_error

---

### test_structured_formatter
**File:** `backend/tests/test_core_functionality.py:79`
**Complexity:** 1
**Documentation:**
```
Test JSON structured logging formatter
```
**Dependencies:** StructuredFormatter, LogRecord, format, loads

---

### test_colored_formatter
**File:** `backend/tests/test_core_functionality.py:103`
**Complexity:** 1
**Documentation:**
```
Test colored console formatter
```
**Dependencies:** LogRecord, format, ColoredFormatter

---

### test_file_operation_logging
**File:** `backend/tests/test_core_functionality.py:125`
**Complexity:** 2
**Documentation:**
```
Test file operation logging
```
**Dependencies:** patch, assert_called_once, Mock, log_file_operation

---

### test_comparison_operation_logging
**File:** `backend/tests/test_core_functionality.py:140`
**Complexity:** 2
**Documentation:**
```
Test comparison operation logging
```
**Dependencies:** log_comparison_operation, patch, assert_called_once, Mock

---

### setup_method
**File:** `backend/tests/test_core_functionality.py:162`
**Complexity:** 5
**Documentation:**
```
Setup mock processor
```
**Dependencies:** stat, MockProcessor, append, Mock, len
*...and 3 more*

---

### __init__
**File:** `backend/tests/test_core_functionality.py:165`
**Complexity:** 1
**Dependencies:** Mock

---

### _create_markdown_table
**File:** `backend/tests/test_core_functionality.py:169`
**Complexity:** 4
**Dependencies:** len, str, append, join

---

### _extract_metadata
**File:** `backend/tests/test_core_functionality.py:181`
**Complexity:** 2
**Dependencies:** stat, fromtimestamp

---

### test_validate_file_extensions
**File:** `backend/tests/test_core_functionality.py:198`
**Complexity:** 1
**Documentation:**
```
Test file validation by extension
```
**Dependencies:** validate_file, endswith

---

### validate_file
**File:** `backend/tests/test_core_functionality.py:201`
**Complexity:** 1
**Dependencies:** endswith

---

### test_create_markdown_table
**File:** `backend/tests/test_core_functionality.py:210`
**Complexity:** 1
**Documentation:**
```
Test markdown table creation
```
**Dependencies:** _create_markdown_table

---

### test_create_markdown_table_empty
**File:** `backend/tests/test_core_functionality.py:227`
**Complexity:** 1
**Documentation:**
```
Test markdown table with empty data
```
**Dependencies:** _create_markdown_table

---

### setup_method
**File:** `backend/tests/test_core_functionality.py:242`
**Complexity:** 14
**Documentation:**
```
Setup mock comparator
```
**Dependencies:** isinstance, strip, abs, float, Mock
*...and 5 more*

---

### __init__
**File:** `backend/tests/test_core_functionality.py:245`
**Complexity:** 1
**Dependencies:** Mock

---

### _normalize_value
**File:** `backend/tests/test_core_functionality.py:253`
**Complexity:** 4
**Dependencies:** isinstance, strip, float, lower, str

---

### _is_numeric
**File:** `backend/tests/test_core_functionality.py:263`
**Complexity:** 2
**Dependencies:** float

---

### _parse_numeric
**File:** `backend/tests/test_core_functionality.py:270`
**Complexity:** 3
**Dependencies:** replace, isinstance, strip, float

---

### _compare_numbers
**File:** `backend/tests/test_core_functionality.py:279`
**Complexity:** 5
**Dependencies:** max, abs

---

### _calculate_percentage_difference
**File:** `backend/tests/test_core_functionality.py:288`
**Complexity:** 4
**Dependencies:** abs

---

### test_normalize_value
**File:** `backend/tests/test_core_functionality.py:298`
**Complexity:** 1
**Documentation:**
```
Test value normalization
```
**Dependencies:** _normalize_value

---

### test_is_numeric
**File:** `backend/tests/test_core_functionality.py:306`
**Complexity:** 1
**Documentation:**
```
Test numeric value detection
```
**Dependencies:** _is_numeric

---

### test_parse_numeric
**File:** `backend/tests/test_core_functionality.py:315`
**Complexity:** 1
**Documentation:**
```
Test numeric value parsing
```
**Dependencies:** _parse_numeric

---

### test_compare_numbers
**File:** `backend/tests/test_core_functionality.py:323`
**Complexity:** 1
**Documentation:**
```
Test number comparison with tolerance
```
**Dependencies:** _compare_numbers

---

### test_calculate_percentage_difference
**File:** `backend/tests/test_core_functionality.py:330`
**Complexity:** 1
**Documentation:**
```
Test percentage difference calculation
```
**Dependencies:** _calculate_percentage_difference

---

### test_tolerance_settings
**File:** `backend/tests/test_core_functionality.py:338`
**Complexity:** 1
**Documentation:**
```
Test tolerance settings
```

---

### __init__
**File:** `backend/utils/exceptions.py:10`
**Complexity:** 1
**Dependencies:** __init__, super

---

### __init__
**File:** `backend/utils/exceptions.py:18`
**Complexity:** 1
**Dependencies:** __init__, super

---

### __init__
**File:** `backend/utils/exceptions.py:27`
**Complexity:** 1
**Dependencies:** __init__, super

---

### __init__
**File:** `backend/utils/exceptions.py:36`
**Complexity:** 1
**Dependencies:** __init__, super

---

### __init__
**File:** `backend/utils/exceptions.py:42`
**Complexity:** 1
**Dependencies:** __init__, super

---

### __init__
**File:** `backend/utils/exceptions.py:52`
**Complexity:** 1
**Dependencies:** __init__, super

---

### __init__
**File:** `backend/utils/exceptions.py:60`
**Complexity:** 1
**Dependencies:** __init__, super

---

### __init__
**File:** `backend/utils/exceptions.py:66`
**Complexity:** 1
**Dependencies:** __init__, super

---

### __init__
**File:** `backend/utils/exceptions.py:72`
**Complexity:** 1
**Dependencies:** __init__, super

---

### __init__
**File:** `backend/utils/exceptions.py:80`
**Complexity:** 1
**Dependencies:** __init__, super

---

### __init__
**File:** `backend/utils/exceptions.py:90`
**Complexity:** 1
**Dependencies:** __init__, super

---

### create_http_exception
**File:** `backend/utils/exceptions.py:98`
**Complexity:** 3
**Documentation:**
```
Create HTTPException with standard format
```
**Dependencies:** HTTPException

---

### generate_file_id
**File:** `backend/utils/file_utils.py:20`
**Complexity:** 1
**Documentation:**
```
Generate unique file ID
```
**Dependencies:** uuid4, str

---

### calculate_file_hash
**File:** `backend/utils/file_utils.py:25`
**Complexity:** 1
**Documentation:**
```
Calculate MD5 hash of file content
```
**Dependencies:** hexdigest, md5

---

### get_file_extension
**File:** `backend/utils/file_utils.py:30`
**Complexity:** 1
**Documentation:**
```
Get file extension from filename
```
**Dependencies:** Path, lower, lstrip

---

### validate_file_size
**File:** `backend/utils/file_utils.py:35`
**Complexity:** 2
**Documentation:**
```
Validate file size against maximum allowed size
```
**Dependencies:** FileSizeExceededError

---

### is_supported_file
**File:** `backend/utils/file_utils.py:42`
**Complexity:** 2
**Documentation:**
```
Check if file is supported
```
**Dependencies:** get_file_extension

---

### get_file_type_from_content
**File:** `backend/utils/file_utils.py:58`
**Complexity:** 1
**Documentation:**
```
Determine file type from content type and filename
```
**Dependencies:** get_file_extension, get

---

### delete_file
**File:** `backend/utils/file_utils.py:106`
**Complexity:** 3
**Documentation:**
```
Delete file from storage
```
**Dependencies:** info, remove, error, exists

---

### get_storage_path
**File:** `backend/utils/file_utils.py:119`
**Complexity:** 1
**Documentation:**
```
Get storage path based on file type
```
**Dependencies:** get

---

### ensure_directory_exists
**File:** `backend/utils/file_utils.py:129`
**Complexity:** 1
**Documentation:**
```
Ensure directory exists
```
**Dependencies:** Path, mkdir

---

### cleanup_old_files
**File:** `backend/utils/file_utils.py:134`
**Complexity:** 6
**Documentation:**
```
Clean up old files in directory
```
**Dependencies:** info, exists, time, remove, listdir
*...and 4 more*

---

### get_file_info
**File:** `backend/utils/file_utils.py:161`
**Complexity:** 2
**Documentation:**
```
Get file information
```
**Dependencies:** stat

---

### validate_file_integrity
**File:** `backend/utils/file_utils.py:179`
**Complexity:** 7
**Documentation:**
```
Validate file integrity
```
**Dependencies:** calculate_file_hash, getsize, exists, open, access
*...and 2 more*

---

### __init__
**File:** `backend/utils/logger.py:18`
**Complexity:** 1
**Dependencies:** getLogger

---

### start_process
**File:** `backend/utils/logger.py:22`
**Complexity:** 1
**Documentation:**
```
Start a new process and return process ID
```
**Dependencies:** info, uuid4, append, time, isoformat
*...and 3 more*

---

### end_process
**File:** `backend/utils/logger.py:52`
**Complexity:** 4
**Documentation:**
```
End a process (with optional process ID)
```
**Dependencies:** info, append, pop, time, round
*...and 3 more*

---

### log_step
**File:** `backend/utils/logger.py:82`
**Complexity:** 2
**Documentation:**
```
Log a step within the current process
```
**Dependencies:** info, time, round, isoformat, update
*...and 2 more*

---

### log_error
**File:** `backend/utils/logger.py:106`
**Complexity:** 2
**Documentation:**
```
Log an error with process context
```
**Dependencies:** type, time, round, isoformat, update
*...and 4 more*

---

### log_warning
**File:** `backend/utils/logger.py:131`
**Complexity:** 2
**Documentation:**
```
Log a warning with process context
```
**Dependencies:** time, round, isoformat, update, items
*...and 2 more*

---

### get_current_process_id
**File:** `backend/utils/logger.py:155`
**Complexity:** 1
**Documentation:**
```
Get the current process ID
```

---

### with_process_logging
**File:** `backend/utils/logger.py:160`
**Complexity:** 6
**Documentation:**
```
Decorator to add process logging to functions
```
**Dependencies:** type, start_process, get_process_logger, end_process, wraps
*...and 6 more*

---

### decorator
**File:** `backend/utils/logger.py:162`
**Complexity:** 6
**Dependencies:** type, start_process, get_process_logger, end_process, wraps
*...and 6 more*

---

### sync_wrapper
**File:** `backend/utils/logger.py:184`
**Complexity:** 3
**Dependencies:** type, start_process, get_process_logger, end_process, wraps
*...and 5 more*

---

### process_context
**File:** `backend/utils/logger.py:214`
**Complexity:** 2
**Documentation:**
```
Context manager for process logging
```
**Dependencies:** end_process, start_process, log_error

---

### get_process_logger
**File:** `backend/utils/logger.py:230`
**Complexity:** 2
**Documentation:**
```
Get or create a process logger instance
```
**Dependencies:** ProcessLogger

---

### log_file_operation
**File:** `backend/utils/logger.py:237`
**Complexity:** 2
**Documentation:**
```
Log file operations with consistent format
```
**Dependencies:** info, isoformat, now, getLogger

---

### log_comparison_operation
**File:** `backend/utils/logger.py:253`
**Complexity:** 1
**Documentation:**
```
Log comparison operations with consistent format
```
**Dependencies:** info, isoformat, now, getLogger

---

### format
**File:** `backend/utils/logger.py:274`
**Complexity:** 7
**Dependencies:** getMessage, hasattr, isoformat, str, fromtimestamp
*...and 2 more*

---

### format
**File:** `backend/utils/logger.py:322`
**Complexity:** 2
**Dependencies:** formatTime, formatException, get, getMessage

---

### setup_logging
**File:** `backend/utils/logger.py:340`
**Complexity:** 3
**Documentation:**
```
Setup enhanced logging configuration
```
**Dependencies:** getattr, RotatingFileHandler, print, Path, StreamHandler
*...and 9 more*

---

### debounce
**File:** `backend/venv/lib/python3.13/site-packages/coverage/htmlfiles/coverage_html.js:11`
**Complexity:** 1

---

### checkVisible
**File:** `backend/venv/lib/python3.13/site-packages/coverage/htmlfiles/coverage_html.js:21`
**Complexity:** 2

---

### on_click
**File:** `backend/venv/lib/python3.13/site-packages/coverage/htmlfiles/coverage_html.js:28`
**Complexity:** 2

---

### getCellValue
**File:** `backend/venv/lib/python3.13/site-packages/coverage/htmlfiles/coverage_html.js:36`
**Complexity:** 6

---

### rowComparator
**File:** `backend/venv/lib/python3.13/site-packages/coverage/htmlfiles/coverage_html.js:50`
**Complexity:** 3

---

### sortColumn
**File:** `backend/venv/lib/python3.13/site-packages/coverage/htmlfiles/coverage_html.js:59`
**Complexity:** 18

---

### updateHeader
**File:** `backend/venv/lib/python3.13/site-packages/coverage/htmlfiles/coverage_html.js:697`
**Complexity:** 3

---

### check_response_structure
**File:** `check_response_structure.py:9`
**Complexity:** 4
**Documentation:**
```
Check exact API response structure
```
**Dependencies:** print, get, len, list, keys
*...and 3 more*

---

### __init__
**File:** `doc_mapper.py:36`
**Complexity:** 1
**Dependencies:** Path, resolve, defaultdict

---

### log
**File:** `doc_mapper.py:42`
**Complexity:** 1
**Documentation:**
```
Log messages with timestamps
```
**Dependencies:** strftime, print, now

---

### scan_python_files
**File:** `doc_mapper.py:47`
**Complexity:** 2
**Documentation:**
```
Find all Python files in the project
```
**Dependencies:** extend, any, len, str, log
*...and 1 more*

---

### scan_javascript_files
**File:** `doc_mapper.py:63`
**Complexity:** 2
**Documentation:**
```
Find all JavaScript files in the project
```
**Dependencies:** extend, any, len, str, log
*...and 1 more*

---

### analyze_python_file
**File:** `doc_mapper.py:78`
**Complexity:** 6
**Documentation:**
```
Analyze a Python file and extract components
```
**Dependencies:** walk, isinstance, relative_to, append, open
*...and 8 more*

---

### analyze_javascript_file
**File:** `doc_mapper.py:119`
**Complexity:** 5
**Documentation:**
```
Analyze a JavaScript file and extract components
```
**Dependencies:** start, relative_to, append, group, count
*...and 8 more*

---

### calculate_complexity
**File:** `doc_mapper.py:158`
**Complexity:** 5
**Documentation:**
```
Calculate cyclomatic complexity for a node
```
**Dependencies:** walk, isinstance, len

---

### extract_dependencies
**File:** `doc_mapper.py:172`
**Complexity:** 5
**Documentation:**
```
Extract dependencies from a node
```
**Dependencies:** walk, isinstance, set, append, list

---

### extract_js_docstring
**File:** `doc_mapper.py:185`
**Complexity:** 4
**Documentation:**
```
Extract JavaScript docstring near a function
```
**Dependencies:** strip, split, reversed, find, rfind

---

### estimate_js_complexity
**File:** `doc_mapper.py:202`
**Complexity:** 7
**Documentation:**
```
Estimate JavaScript function complexity
```
**Dependencies:** start, enumerate, find, count

---

### get_git_changes
**File:** `doc_mapper.py:233`
**Complexity:** 7
**Documentation:**
```
Get uncommitted git changes
```
**Dependencies:** append, strip, split, log, run

---

### generate_component_documentation
**File:** `doc_mapper.py:267`
**Complexity:** 8
**Documentation:**
```
Generate documentation for all components
```
**Dependencies:** extend, append, strip, title, strftime
*...and 7 more*

---

### generate_api_documentation
**File:** `doc_mapper.py:329`
**Complexity:** 6
**Documentation:**
```
Generate API documentation from backend code
```
**Dependencies:** findall, extend, relative_to, upper, strftime
*...and 7 more*

---

### save_mappings
**File:** `doc_mapper.py:372`
**Complexity:** 2
**Documentation:**
```
Save mappings to JSON file
```
**Dependencies:** open, isoformat, mkdir, len, dump
*...and 3 more*

---

### run_full_analysis
**File:** `doc_mapper.py:399`
**Complexity:** 7
**Documentation:**
```
Run complete code analysis and documentation generation
```
**Dependencies:** save_mappings, extend, any, analyze_python_file, scan_javascript_files
*...and 12 more*

---

### generate_git_changes_doc
**File:** `doc_mapper.py:446`
**Complexity:** 7
**Documentation:**
```
Generate documentation for git changes
```
**Dependencies:** extend, append, strftime, len, now
*...and 1 more*

---

### main
**File:** `doc_mapper.py:492`
**Complexity:** 7
**Documentation:**
```
Main entry point
```
**Dependencies:** run_full_analysis, extend, print, DocumentationMapper, scan_javascript_files
*...and 7 more*

---

### generateCSVData
**File:** `frontend/create_test_files.js:12`
**Complexity:** 7

---

### generateLargeCSVData
**File:** `frontend/create_test_files.js:35`
**Complexity:** 2

---

### generateEdgeCaseCSV
**File:** `frontend/create_test_files.js:49`
**Complexity:** 1

---

### generateMalformedCSV
**File:** `frontend/create_test_files.js:64`
**Complexity:** 1

---

### generateEmptyAndNullCSV
**File:** `frontend/create_test_files.js:77`
**Complexity:** 1

---

### create_test_files
**File:** `frontend/create_test_files.py:11`
**Complexity:** 1
**Documentation:**
```
Create two test Excel files with slight differences
```
**Dependencies:** DataFrame, to_csv, print, to_excel

---

### apiRequest
**File:** `frontend/scripts/api_integration.js:37`
**Complexity:** 1
**Documentation:**
```
/**
 * API Helper Functions
 */
```

---

### apiRequest
**File:** `frontend/scripts/api_integration.js:37`
**Complexity:** 1
**Documentation:**
```
/**
 * API Helper Functions
 */
```

---

### uploadFile
**File:** `frontend/scripts/api_integration.js:59`
**Complexity:** 12

---

### uploadFile
**File:** `frontend/scripts/api_integration.js:59`
**Complexity:** 12

---

### processFile
**File:** `frontend/scripts/api_integration.js:83`
**Complexity:** 17

---

### processFile
**File:** `frontend/scripts/api_integration.js:83`
**Complexity:** 17

---

### compareFilesApi
**File:** `frontend/scripts/api_integration.js:111`
**Complexity:** 1

---

### compareFilesApi
**File:** `frontend/scripts/api_integration.js:111`
**Complexity:** 1

---

### checkBackendHealth
**File:** `frontend/scripts/api_integration.js:139`
**Complexity:** 3
**Documentation:**
```
/**
 * Backend connection functions
 */
```

---

### checkBackendHealth
**File:** `frontend/scripts/api_integration.js:139`
**Complexity:** 3
**Documentation:**
```
/**
 * Backend connection functions
 */
```

---

### processUploadedFiles
**File:** `frontend/scripts/api_integration.js:150`
**Complexity:** 6

---

### processUploadedFiles
**File:** `frontend/scripts/api_integration.js:150`
**Complexity:** 6

---

### createStatusElement
**File:** `frontend/scripts/api_integration.js:197`
**Complexity:** 3

---

### displayBackendResults
**File:** `frontend/scripts/api_integration.js:213`
**Complexity:** 27
**Documentation:**
```
/**
 * Display backend results
 */
```

---

### displayBackendDifferences
**File:** `frontend/scripts/api_integration.js:256`
**Complexity:** 78

---

### getSeverityIcon
**File:** `frontend/scripts/api_integration.js:342`
**Complexity:** 2

---

### getSeverityText
**File:** `frontend/scripts/api_integration.js:352`
**Complexity:** 2

---

### formatFieldValue
**File:** `frontend/scripts/api_integration.js:362`
**Complexity:** 3

---

### populateBackendComparisonTable
**File:** `frontend/scripts/api_integration.js:379`
**Complexity:** 30

---

### compareFilesWithBackend
**File:** `frontend/scripts/api_integration.js:424`
**Complexity:** 4
**Documentation:**
```
/**
 * Enhanced comparison function with backend integration
 */
```

---

### compareFilesWithBackend
**File:** `frontend/scripts/api_integration.js:424`
**Complexity:** 4
**Documentation:**
```
/**
 * Enhanced comparison function with backend integration
 */
```

---

### compareFilesFrontend
**File:** `frontend/scripts/api_integration.js:445`
**Complexity:** 2
**Documentation:**
```
/**
 * Fallback to frontend comparison if backend is unavailable
 */
```

---

### compareFiles
**File:** `frontend/scripts/api_integration.js:469`
**Complexity:** 10
**Documentation:**
```
/**
 * Main comparison function with backend fallback
 */
```

---

### compareFiles
**File:** `frontend/scripts/api_integration.js:469`
**Complexity:** 10
**Documentation:**
```
/**
 * Main comparison function with backend fallback
 */
```

---

### exportBackendReport
**File:** `frontend/scripts/api_integration.js:503`
**Complexity:** 7
**Documentation:**
```
/**
 * Export enhanced functionality
 */
```

---

### generateBackendCSVContent
**File:** `frontend/scripts/api_integration.js:519`
**Complexity:** 20

---

### generateBackendPDFReport
**File:** `frontend/scripts/api_integration.js:536`
**Complexity:** 5
**Documentation:**
```
/**
 * Generate PDF report from backend results
 */
```

---

### generateBackendPDFReport
**File:** `frontend/scripts/api_integration.js:536`
**Complexity:** 5
**Documentation:**
```
/**
 * Generate PDF report from backend results
 */
```

---

### generateBackendHTMLReport
**File:** `frontend/scripts/api_integration.js:554`
**Complexity:** 47
**Documentation:**
```
/**
 * Generate HTML report from backend results
 */
```

---

### initializeBackendIntegration
**File:** `frontend/scripts/api_integration.js:676`
**Complexity:** 4
**Documentation:**
```
/**
 * Initialize backend integration
 */
```

---

### switchDiffView
**File:** `frontend/scripts/diff-visualization.js:19`
**Complexity:** 26
**Documentation:**
```
/**
 * Switch between different diff views
 */
```

---

### generateSideBySideDiff
**File:** `frontend/scripts/diff-visualization.js:68`
**Complexity:** 22
**Documentation:**
```
/**
 * Generate side-by-side diff view
 */
```

---

### generateUnifiedDiff
**File:** `frontend/scripts/diff-visualization.js:109`
**Complexity:** 15
**Documentation:**
```
/**
 * Generate unified diff view
 */
```

---

### createDiffLine
**File:** `frontend/scripts/diff-visualization.js:130`
**Complexity:** 10
**Documentation:**
```
/**
 * Create a diff line element
 */
```

---

### createUnifiedDiffLine
**File:** `frontend/scripts/diff-visualization.js:163`
**Complexity:** 23
**Documentation:**
```
/**
 * Create unified diff line
 */
```

---

### formatDataItem
**File:** `frontend/scripts/diff-visualization.js:200`
**Complexity:** 6
**Documentation:**
```
/**
 * Format data item for display
 */
```

---

### compareDataItems
**File:** `frontend/scripts/diff-visualization.js:208`
**Complexity:** 30
**Documentation:**
```
/**
 * Compare two data items
 */
```

---

### highlightDifferences
**File:** `frontend/scripts/diff-visualization.js:249`
**Complexity:** 4
**Documentation:**
```
/**
 * Highlight differences in content
 */
```

---

### exportDiff
**File:** `frontend/scripts/diff-visualization.js:273`
**Complexity:** 81
**Documentation:**
```
/**
 * Export diff report
 */
```

---

### highlightDifferencesEnhanced
**File:** `frontend/scripts/diff-visualization.js:370`
**Complexity:** 5
**Documentation:**
```
/**
 * Enhanced diff highlighting with better visual indicators
 */
```

---

### navigateDiff
**File:** `frontend/scripts/diff-visualization.js:393`
**Complexity:** 13
**Documentation:**
```
/**
 * Navigation functions for diff lines
 */
```

---

### scrollToDiffLine
**File:** `frontend/scripts/diff-visualization.js:415`
**Complexity:** 3

---

### highlightLine
**File:** `frontend/scripts/diff-visualization.js:423`
**Complexity:** 3

---

### updateNavigationState
**File:** `frontend/scripts/diff-visualization.js:439`
**Complexity:** 8

---

### searchDiff
**File:** `frontend/scripts/diff-visualization.js:450`
**Complexity:** 7
**Documentation:**
```
/**
 * Search functionality
 */
```

---

### clearSearch
**File:** `frontend/scripts/diff-visualization.js:472`
**Complexity:** 4

---

### showSearchResults
**File:** `frontend/scripts/diff-visualization.js:483`
**Complexity:** 1

---

### hideSearchResults
**File:** `frontend/scripts/diff-visualization.js:487`
**Complexity:** 1

---

### showTooltip
**File:** `frontend/scripts/diff-visualization.js:494`
**Complexity:** 7
**Documentation:**
```
/**
 * Enhanced tooltip system
 */
```

---

### hideTooltip
**File:** `frontend/scripts/diff-visualization.js:524`
**Complexity:** 4

---

### createDiffLineEnhanced
**File:** `frontend/scripts/diff-visualization.js:539`
**Complexity:** 12
**Documentation:**
```
/**
 * Enhanced diff line generation with better formatting
 */
```

---

### getLineTooltipMessage
**File:** `frontend/scripts/diff-visualization.js:583`
**Complexity:** 14

---

### generateSideBySideDiffEnhanced
**File:** `frontend/scripts/diff-visualization.js:604`
**Complexity:** 33
**Documentation:**
```
/**
 * Enhanced side-by-side diff generation
 */
```

---

### compareDataItemsEnhanced
**File:** `frontend/scripts/diff-visualization.js:661`
**Complexity:** 35
**Documentation:**
```
/**
 * Enhanced comparison with better diff detection
 */
```

---

### addDiffAnimations
**File:** `frontend/scripts/diff-visualization.js:716`
**Complexity:** 5
**Documentation:**
```
/**
 * Add CSS animation keyframes
 */
```

---

### handleFileSelect
**File:** `frontend/scripts/main.js:20`
**Complexity:** 9
**Documentation:**
```
/**
 * File handling functions
 */
```

---

### checkFilesReady
**File:** `frontend/scripts/main.js:57`
**Complexity:** 4

---

### initializeDragAndDrop
**File:** `frontend/scripts/main.js:76`
**Complexity:** 9
**Documentation:**
```
/**
 * Drag and drop functionality
 */
```

---

### compareFiles
**File:** `frontend/scripts/main.js:132`
**Complexity:** 10
**Documentation:**
```
/**
 * Main comparison function - now uses backend API only
 */
```

---

### compareFiles
**File:** `frontend/scripts/main.js:132`
**Complexity:** 10
**Documentation:**
```
/**
 * Main comparison function - now uses backend API only
 */
```

---

### performComparison
**File:** `frontend/scripts/main.js:159`
**Complexity:** 87
**Documentation:**
```
/**
 * Perform enhanced data comparison
 */
```

---

### findMatchingRow
**File:** `frontend/scripts/main.js:183`
**Complexity:** 10

---

### calculateStringSimilarity
**File:** `frontend/scripts/main.js:333`
**Complexity:** 3
**Documentation:**
```
/**
 * Calculate string similarity using Levenshtein distance
 */
```

---

### levenshteinDistance
**File:** `frontend/scripts/main.js:347`
**Complexity:** 7
**Documentation:**
```
/**
 * Simple Levenshtein distance calculation
 */
```

---

### displayRawData
**File:** `frontend/scripts/main.js:378`
**Complexity:** 23
**Documentation:**
```
/**
 * Display raw extracted data for verification
 */
```

---

### createDataRow
**File:** `frontend/scripts/main.js:412`
**Complexity:** 14

---

### extractDataFromStructured
**File:** `frontend/scripts/main.js:440`
**Complexity:** 24
**Documentation:**
```
/**
 * Extract data from structured data returned by backend
 */
```

---

### toggleRawDataSection
**File:** `frontend/scripts/main.js:492`
**Complexity:** 3
**Documentation:**
```
/**
 * Toggle raw data section visibility
 */
```

---

### toggleRawDataView
**File:** `frontend/scripts/main.js:505`
**Complexity:** 1
**Documentation:**
```
/**
 * Toggle raw data view within section
 */
```

---

### exportToMarkdown
**File:** `frontend/scripts/main.js:513`
**Complexity:** 47
**Documentation:**
```
/**
 * Export raw data to Markdown for verification
 */
```

---

### displayResults
**File:** `frontend/scripts/main.js:597`
**Complexity:** 40
**Documentation:**
```
/**
 * Display comparison results
 */
```

---

### populateComparisonTable
**File:** `frontend/scripts/main.js:669`
**Complexity:** 20
**Documentation:**
```
/**
 * Populate comparison table
 */
```

---

### displayDifferences
**File:** `frontend/scripts/main.js:712`
**Complexity:** 37
**Documentation:**
```
/**
 * Display detailed differences
 */
```

---

### updateDiffSummaryBadges
**File:** `frontend/scripts/main.js:753`
**Complexity:** 25
**Documentation:**
```
/**
 * Update diff summary badges
 */
```

---

### exportReport
**File:** `frontend/scripts/main.js:780`
**Complexity:** 14
**Documentation:**
```
/**
 * Export functionality - now uses backend API
 */
```

---

### generateCSVContent
**File:** `frontend/scripts/main.js:802`
**Complexity:** 11

---

### downloadFile
**File:** `frontend/scripts/main.js:818`
**Complexity:** 1

---

### generatePDFReport
**File:** `frontend/scripts/main.js:833`
**Complexity:** 38
**Documentation:**
```
/**
 * Generate PDF report using jsPDF library
 */
```

---

### generatePDFReport
**File:** `frontend/scripts/main.js:833`
**Complexity:** 38
**Documentation:**
```
/**
 * Generate PDF report using jsPDF library
 */
```

---

### loadJSPDFLibrary
**File:** `frontend/scripts/main.js:932`
**Complexity:** 1
**Documentation:**
```
/**
 * Load jsPDF library dynamically
 */
```

---

### loadJSPDFLibrary
**File:** `frontend/scripts/main.js:932`
**Complexity:** 1
**Documentation:**
```
/**
 * Load jsPDF library dynamically
 */
```

---

### generateHTMLReport
**File:** `frontend/scripts/main.js:946`
**Complexity:** 2
**Documentation:**
```
/**
 * Generate HTML report as PDF fallback
 */
```

---

### generateHTMLReportContent
**File:** `frontend/scripts/main.js:965`
**Complexity:** 25
**Documentation:**
```
/**
 * Generate HTML report content
 */
```

---

### showSuccessMessage
**File:** `frontend/scripts/main.js:1051`
**Complexity:** 8
**Documentation:**
```
/**
 * Show success message
 */
```

---

### toggleTheme
**File:** `frontend/scripts/main.js:1094`
**Complexity:** 1
**Documentation:**
```
/**
 * Toggle theme with cycle: System → Light → Dark → System
 */
```

---

### getCurrentThemeMode
**File:** `frontend/scripts/main.js:1121`
**Complexity:** 1
**Documentation:**
```
/**
 * Get current theme mode
 */
```

---

### setThemeMode
**File:** `frontend/scripts/main.js:1128`
**Complexity:** 1
**Documentation:**
```
/**
 * Set theme mode and apply it
 */
```

---

### applyTheme
**File:** `frontend/scripts/main.js:1136`
**Complexity:** 4
**Documentation:**
```
/**
 * Apply theme based on mode
 */
```

---

### getSystemPreference
**File:** `frontend/scripts/main.js:1156`
**Complexity:** 2
**Documentation:**
```
/**
 * Get system color scheme preference
 */
```

---

### updateThemeUI
**File:** `frontend/scripts/main.js:1167`
**Complexity:** 4
**Documentation:**
```
/**
 * Update UI elements based on current theme
 */
```

---

### saveThemePreference
**File:** `frontend/scripts/main.js:1206`
**Complexity:** 3
**Documentation:**
```
/**
 * Save theme preference to localStorage
 */
```

---

### loadThemePreference
**File:** `frontend/scripts/main.js:1217`
**Complexity:** 4
**Documentation:**
```
/**
 * Load theme preference from localStorage
 */
```

---

### updateMetaThemeColor
**File:** `frontend/scripts/main.js:1230`
**Complexity:** 3
**Documentation:**
```
/**
 * Update meta theme-color for mobile browsers
 */
```

---

### setupSystemThemeListener
**File:** `frontend/scripts/main.js:1250`
**Complexity:** 3
**Documentation:**
```
/**
 * Listen for system theme changes
 */
```

---

### initTheme
**File:** `frontend/scripts/main.js:1265`
**Complexity:** 2
**Documentation:**
```
/**
 * Initialize theme system with system preference detection
 */
```

---

### setupThemeKeyboardShortcuts
**File:** `frontend/scripts/main.js:1286`
**Complexity:** 13
**Documentation:**
```
/**
 * Setup keyboard shortcuts for theme switching
 */
```

---

### addThemeTransitionEffects
**File:** `frontend/scripts/main.js:1307`
**Complexity:** 4
**Documentation:**
```
/**
 * Add smooth transition effects for theme changes
 */
```

---

### getThemeInfo
**File:** `frontend/scripts/main.js:1343`
**Complexity:** 2
**Documentation:**
```
/**
 * Get theme information for debugging
 */
```

---

### resetThemeToSystem
**File:** `frontend/scripts/main.js:1356`
**Complexity:** 1
**Documentation:**
```
/**
 * Reset theme to system preference
 */
```

---

### enhancedInitTheme
**File:** `frontend/scripts/main.js:1363`
**Complexity:** 9

---

### parseCSVLine
**File:** `frontend/test_csv_fix.js:10`
**Complexity:** 8

---

### parseExcelFile
**File:** `frontend/utils/file-parsers.js:9`
**Complexity:** 29
**Documentation:**
```
/**
 * Parse Excel files (XLSX, XLS)
 */
```

---

### parseExcelFile
**File:** `frontend/utils/file-parsers.js:9`
**Complexity:** 29
**Documentation:**
```
/**
 * Parse Excel files (XLSX, XLS)
 */
```

---

### parseCSVFile
**File:** `frontend/utils/file-parsers.js:54`
**Complexity:** 50
**Documentation:**
```
/**
 * Parse CSV files
 */
```

---

### parseCSVFile
**File:** `frontend/utils/file-parsers.js:54`
**Complexity:** 50
**Documentation:**
```
/**
 * Parse CSV files
 */
```

---

### detectDelimiter
**File:** `frontend/utils/file-parsers.js:159`
**Complexity:** 4
**Documentation:**
```
/**
 * Detect CSV delimiter
 */
```

---

### parseCSVLine
**File:** `frontend/utils/file-parsers.js:182`
**Complexity:** 8

---

### parsePDFFile
**File:** `frontend/utils/file-parsers.js:229`
**Complexity:** 9
**Documentation:**
```
/**
 * Parse PDF files using PDF.js library
 * Enhanced implementation with table extraction capabilities
 */
```

---

### parsePDFFile
**File:** `frontend/utils/file-parsers.js:229`
**Complexity:** 9
**Documentation:**
```
/**
 * Parse PDF files using PDF.js library
 * Enhanced implementation with table extraction capabilities
 */
```

---

### loadPDFJSLibrary
**File:** `frontend/utils/file-parsers.js:282`
**Complexity:** 1
**Documentation:**
```
/**
 * Load PDF.js library dynamically
 */
```

---

### loadPDFJSLibrary
**File:** `frontend/utils/file-parsers.js:282`
**Complexity:** 1
**Documentation:**
```
/**
 * Load PDF.js library dynamically
 */
```

---

### extractTableDataFromPDFText
**File:** `frontend/utils/file-parsers.js:300`
**Complexity:** 10
**Documentation:**
```
/**
 * Extract table data from PDF text
 */
```

---

### parsePDFTextToData
**File:** `frontend/utils/file-parsers.js:346`
**Complexity:** 11
**Documentation:**
```
/**
 * Parse PDF text to structured data using smart extraction
 */
```

---

### isHeaderOrFooter
**File:** `frontend/utils/file-parsers.js:382`
**Complexity:** 1
**Documentation:**
```
/**
 * Check if line is header or footer
 */
```

---

### extractDataFromLine
**File:** `frontend/utils/file-parsers.js:396`
**Complexity:** 4
**Documentation:**
```
/**
 * Extract data from line using patterns
 */
```

---

### extractDescriptionFromLine
**File:** `frontend/utils/file-parsers.js:412`
**Complexity:** 1
**Documentation:**
```
/**
 * Extract description from line
 */
```

---

### cleanText
**File:** `frontend/utils/file-parsers.js:428`
**Complexity:** 3
**Documentation:**
```
/**
 * Clean text from unwanted characters
 */
```

---

### parseNumber
**File:** `frontend/utils/file-parsers.js:439`
**Complexity:** 2
**Documentation:**
```
/**
 * Parse number from string
 */
```

---

### generateFallbackPDFData
**File:** `frontend/utils/file-parsers.js:451`
**Complexity:** 1
**Documentation:**
```
/**
 * Generate fallback PDF data when parsing fails
 */
```

---

### parseFile
**File:** `frontend/utils/file-parsers.js:466`
**Complexity:** 15
**Documentation:**
```
/**
 * Main file parser function with enhanced error handling
 */
```

---

### parseFile
**File:** `frontend/utils/file-parsers.js:466`
**Complexity:** 15
**Documentation:**
```
/**
 * Main file parser function with enhanced error handling
 */
```

---

### validateParsedData
**File:** `frontend/utils/file-parsers.js:528`
**Complexity:** 5
**Documentation:**
```
/**
 * Validate parsed data
 */
```

---

### formatDataForComparison
**File:** `frontend/utils/file-parsers.js:553`
**Complexity:** 4
**Documentation:**
```
/**
 * Format data for comparison
 */
```

---

### formatFileSize
**File:** `frontend/utils/helpers.js:8`
**Complexity:** 2
**Documentation:**
```
/**
 * Format file size to human readable format
 */
```

---

### getFileName
**File:** `frontend/utils/helpers.js:21`
**Complexity:** 3
**Documentation:**
```
/**
 * Extract just the filename from full path (handles different OS path formats)
 */
```

---

### debounce
**File:** `frontend/utils/helpers.js:29`
**Complexity:** 1
**Documentation:**
```
/**
 * Debounce function to limit function calls
 */
```

---

### executedFunction
**File:** `frontend/utils/helpers.js:31`
**Complexity:** 1

---

### later
**File:** `frontend/utils/helpers.js:32`
**Complexity:** 1

---

### throttle
**File:** `frontend/utils/helpers.js:44`
**Complexity:** 2
**Documentation:**
```
/**
 * Throttle function to limit function calls
 */
```

---

### generateId
**File:** `frontend/utils/helpers.js:60`
**Complexity:** 1
**Documentation:**
```
/**
 * Generate unique ID
 */
```

---

### isValidFileType
**File:** `frontend/utils/helpers.js:67`
**Complexity:** 1
**Documentation:**
```
/**
 * Validate file type
 */
```

---

### parseCSV
**File:** `frontend/utils/helpers.js:75`
**Complexity:** 5
**Documentation:**
```
/**
 * Parse CSV content to JSON
 */
```

---

### jsonToCSV
**File:** `frontend/utils/helpers.js:99`
**Complexity:** 6
**Documentation:**
```
/**
 * Convert JSON to CSV
 */
```

---

### getSeverityColor
**File:** `frontend/utils/helpers.js:122`
**Complexity:** 2
**Documentation:**
```
/**
 * Get color based on severity
 */
```

---

### getStatusIcon
**File:** `frontend/utils/helpers.js:135`
**Complexity:** 4
**Documentation:**
```
/**
 * Get status icon based on status
 */
```

---

### showNotification
**File:** `frontend/utils/helpers.js:149`
**Complexity:** 25
**Documentation:**
```
/**
 * Show notification message
 */
```

---

### deepClone
**File:** `frontend/utils/helpers.js:203`
**Complexity:** 7
**Documentation:**
```
/**
 * Deep clone an object
 */
```

---

### objectsEqual
**File:** `frontend/utils/helpers.js:220`
**Complexity:** 3
**Documentation:**
```
/**
 * Check if two objects are equal
 */
```

---

### roundTo
**File:** `frontend/utils/helpers.js:227`
**Complexity:** 1
**Documentation:**
```
/**
 * Round number to specified decimal places
 */
```

---

### calculatePercentage
**File:** `frontend/utils/helpers.js:234`
**Complexity:** 2
**Documentation:**
```
/**
 * Calculate percentage
 */
```

---

### getCurrentDate
**File:** `frontend/utils/helpers.js:242`
**Complexity:** 1
**Documentation:**
```
/**
 * Get current date in YYYY-MM-DD format
 */
```

---

### getCurrentTime
**File:** `frontend/utils/helpers.js:253`
**Complexity:** 1
**Documentation:**
```
/**
 * Get current time in HH:MM:SS format
 */
```

---

### escapeHtml
**File:** `frontend/utils/helpers.js:264`
**Complexity:** 1
**Documentation:**
```
/**
 * Escape HTML characters
 */
```

---

### unescapeHtml
**File:** `frontend/utils/helpers.js:278`
**Complexity:** 1
**Documentation:**
```
/**
 * Unescape HTML characters
 */
```

---

### __init__
**File:** `run_project.py:16`
**Complexity:** 1
**Dependencies:** Path

---

### check_prerequisites
**File:** `run_project.py:22`
**Complexity:** 6
**Documentation:**
```
Check if all prerequisites are met
```
**Dependencies:** print, exists

---

### run_backend
**File:** `run_project.py:60`
**Complexity:** 10
**Documentation:**
```
Run backend server
```
**Dependencies:** print, iter, strip, exists, Popen
*...and 7 more*

---

### run_frontend
**File:** `run_project.py:119`
**Complexity:** 7
**Documentation:**
```
Run frontend server
```
**Dependencies:** print, iter, wait, strip, str
*...and 4 more*

---

### run_tests
**File:** `run_project.py:175`
**Complexity:** 12
**Documentation:**
```
Run tests before starting
```
**Dependencies:** print, strip, exists, lower, startswith
*...and 4 more*

---

### run_browser
**File:** `run_project.py:250`
**Complexity:** 2
**Documentation:**
```
Open browser after servers are ready
```
**Dependencies:** open, print, sleep

---

### cleanup
**File:** `run_project.py:263`
**Complexity:** 4
**Documentation:**
```
Clean up processes
```
**Dependencies:** terminate, kill, print, wait

---

### signal_handler
**File:** `run_project.py:277`
**Complexity:** 1
**Documentation:**
```
Handle Ctrl+C
```
**Dependencies:** exit, print, cleanup

---

### kill_existing_servers
**File:** `run_project.py:283`
**Complexity:** 14
**Documentation:**
```
Kill any existing servers on ports 3000 and 8000
```
**Dependencies:** print, strip, terminate, split, wait
*...and 3 more*

---

### run
**File:** `run_project.py:335`
**Complexity:** 5
**Documentation:**
```
Main run method
```
**Dependencies:** start, print, run_tests, Thread, sleep
*...and 4 more*

---

### main
**File:** `run_project.py:388`
**Complexity:** 11
**Documentation:**
```
Main entry point
```
**Dependencies:** print, run_tests, ProjectRunner, run_backend, lower
*...and 6 more*

---

## Classs

### APIComparisonTestRunner
**File:** `archive/tests/test_api_comparisons.py:18`
**Complexity:** 23
**Documentation:**
```
Test runner for API-based file comparisons
```
**Dependencies:** append, upper, open, test_api_comparison, test_same_format_api_comparisons
*...and 17 more*

---

### ComparisonTestRunner
**File:** `archive/tests/test_comparison_functionality.py:21`
**Complexity:** 49
**Documentation:**
```
Test runner for file comparison functionality
```
**Dependencies:** ExcelProcessor, append, lstrip, process, test_invoice_comparisons
*...and 21 more*

---

### ComparisonTypeTestRunner
**File:** `archive/tests/test_comparison_types.py:21`
**Complexity:** 27
**Documentation:**
```
Test runner for comparing different file types
```
**Dependencies:** ExcelProcessor, append, upper, test_same_format_comparisons, lstrip
*...and 22 more*

---

### SimpleFileTestRunner
**File:** `archive/tests/test_file_processing.py:20`
**Complexity:** 22
**Documentation:**
```
Simple test runner focusing on file processing
```
**Dependencies:** ExcelProcessor, append, upper, split, lstrip
*...and 23 more*

---

### MasterTestRunner
**File:** `archive/tests/test_master_suite.py:24`
**Complexity:** 49
**Documentation:**
```
Master test runner for comprehensive file comparison system testing
```
**Dependencies:** ExcelProcessor, append, run_cross_format_tests, upper, isoformat
*...and 35 more*

---

### ComprehensiveTestRunner
**File:** `archive/tests/test_new_samples.py:27`
**Complexity:** 49
**Documentation:**
```
Comprehensive test runner for new sample files
```
**Dependencies:** ExcelProcessor, append, upper, split, lstrip
*...and 28 more*

---

### Settings
**File:** `backend/app/config.py:10`
**Complexity:** 1
**Documentation:**
```
Application settings
```
**Dependencies:** SettingsConfigDict

---

### ProcessingStatus
**File:** `backend/app/models.py:11`
**Complexity:** 1
**Documentation:**
```
File processing status
```

---

### FileType
**File:** `backend/app/models.py:20`
**Complexity:** 1
**Documentation:**
```
Supported file types
```

---

### DifferenceSeverity
**File:** `backend/app/models.py:28`
**Complexity:** 1
**Documentation:**
```
Difference severity levels
```

---

### ExportFormat
**File:** `backend/app/models.py:36`
**Complexity:** 1
**Documentation:**
```
Export formats
```

---

### ComparisonType
**File:** `backend/app/models.py:44`
**Complexity:** 1
**Documentation:**
```
Comparison types
```

---

### FileInfo
**File:** `backend/app/models.py:53`
**Complexity:** 1
**Documentation:**
```
File information model
```
**Dependencies:** isoformat

---

### ProcessingOptions
**File:** `backend/app/models.py:76`
**Complexity:** 1
**Documentation:**
```
File processing options
```

---

### ToleranceSettings
**File:** `backend/app/models.py:88`
**Complexity:** 1
**Documentation:**
```
Tolerance settings for numerical comparison
```

---

### ComparisonOptions
**File:** `backend/app/models.py:97`
**Complexity:** 1
**Documentation:**
```
Comparison configuration options
```
**Dependencies:** ToleranceSettings

---

### ComparisonSummary
**File:** `backend/app/models.py:109`
**Complexity:** 1
**Documentation:**
```
Comparison summary statistics
```
**Dependencies:** round

---

### DifferenceDetail
**File:** `backend/app/models.py:123`
**Complexity:** 1
**Documentation:**
```
Detailed difference information
```

---

### ComparisonResult
**File:** `backend/app/models.py:136`
**Complexity:** 1
**Documentation:**
```
Complete comparison result
```
**Dependencies:** isoformat

---

### ComparisonSummaryResponse
**File:** `backend/app/models.py:153`
**Complexity:** 1
**Documentation:**
```
Comparison summary response
```

---

### ExportOptions
**File:** `backend/app/models.py:162`
**Complexity:** 1
**Documentation:**
```
Export configuration options
```

---

### FormattingOptions
**File:** `backend/app/models.py:174`
**Complexity:** 1
**Documentation:**
```
Export formatting options
```

---

### ExportRequest
**File:** `backend/app/models.py:183`
**Complexity:** 1
**Documentation:**
```
Export request model
```
**Dependencies:** ExportOptions

---

### ExportResponse
**File:** `backend/app/models.py:191`
**Complexity:** 1
**Documentation:**
```
Export response model
```
**Dependencies:** isoformat

---

### FileUploadResponse
**File:** `backend/app/models.py:209`
**Complexity:** 1
**Documentation:**
```
File upload response
```

---

### FileProcessResponse
**File:** `backend/app/models.py:215`
**Complexity:** 1
**Documentation:**
```
File processing response
```

---

### CompareFilesRequest
**File:** `backend/app/models.py:221`
**Complexity:** 1
**Documentation:**
```
Compare files request
```
**Dependencies:** ComparisonOptions

---

### CompareFilesResponse
**File:** `backend/app/models.py:228`
**Complexity:** 1
**Documentation:**
```
Compare files response
```

---

### ValidationError
**File:** `backend/app/models.py:234`
**Complexity:** 1
**Documentation:**
```
Validation error model
```

---

### APIError
**File:** `backend/app/models.py:241`
**Complexity:** 1
**Documentation:**
```
API error response
```
**Dependencies:** isoformat

---

### HealthResponse
**File:** `backend/app/models.py:255`
**Complexity:** 1
**Documentation:**
```
Health check response
```
**Dependencies:** isoformat

---

### SupportedFormat
**File:** `backend/app/models.py:271`
**Complexity:** 1
**Documentation:**
```
Supported file format model
```

---

### SupportedFormatsResponse
**File:** `backend/app/models.py:280`
**Complexity:** 1
**Documentation:**
```
Supported formats response
```

---

### FileValidationRequest
**File:** `backend/app/models.py:286`
**Complexity:** 1
**Documentation:**
```
File validation request
```

---

### FileValidationResponse
**File:** `backend/app/models.py:294`
**Complexity:** 1
**Documentation:**
```
File validation response
```

---

### StatisticsCard
**File:** `backend/app/models.py:303`
**Complexity:** 1
**Documentation:**
```
Statistics card model
```

---

### TableData
**File:** `backend/app/models.py:310`
**Complexity:** 1
**Documentation:**
```
Table data model
```

---

### TableRow
**File:** `backend/app/models.py:317`
**Complexity:** 1
**Documentation:**
```
Table row model
```

---

### BaseComparator
**File:** `backend/comparators/base_comparator.py:14`
**Complexity:** 24
**Documentation:**
```
Abstract base class for data comparators
```
**Dependencies:** isinstance, any, strip, abs, float
*...and 5 more*

---

### DataComparator
**File:** `backend/comparators/data_comparator.py:21`
**Complexity:** 38
**Documentation:**
```
Main data comparator implementation
```
**Dependencies:** uuid4, append, _extract_table_data, _perform_comparison, min
*...and 35 more*

---

### DiffAnalyzer
**File:** `backend/comparators/diff_analyzer.py:14`
**Complexity:** 45
**Documentation:**
```
Utility class for analyzing differences and generating reports
```
**Dependencies:** append, isoformat, _is_numeric_difference, categorize_differences, _generate_summary
*...and 17 more*

---

### BaseProcessor
**File:** `backend/processors/base_processor.py:14`
**Complexity:** 8
**Documentation:**
```
Abstract base class for file processors
```
**Dependencies:** ljust, append, isoformat, error, max
*...and 14 more*

---

### CSVProcessor
**File:** `backend/processors/csv_processor.py:21`
**Complexity:** 45
**Documentation:**
```
CSV file processor using pandas
```
**Dependencies:** hasattr, append, count, CorruptedFileError, open
*...and 43 more*

---

### ExcelProcessor
**File:** `backend/processors/excel_processor.py:21`
**Complexity:** 53
**Documentation:**
```
Excel file processor using pandas and openpyxl
```
**Dependencies:** getattr, fillna, append, _get_workbook_info, close
*...and 50 more*

---

### PDFProcessor
**File:** `backend/processors/pdf_processor.py:18`
**Complexity:** 145
**Documentation:**
```
PDF file processor using markitdown
```
**Dependencies:** hasattr, append, upper, _fallback_pdf_conversion, float
*...and 53 more*

---

### TestDataFactory
**File:** `backend/tests/conftest.py:132`
**Complexity:** 3
**Documentation:**
```
Factory for creating test data
```
**Dependencies:** uuid4, append, range, update, str
*...and 2 more*

---

### TestFileUploadAPI
**File:** `backend/tests/test_api_endpoints.py:24`
**Complexity:** 3
**Documentation:**
```
Test file upload API endpoints
```
**Dependencies:** close, get, skipif, NamedTemporaryFile, open
*...and 6 more*

---

### TestComparisonAPI
**File:** `backend/tests/test_api_endpoints.py:194`
**Complexity:** 2
**Documentation:**
```
Test comparison API endpoints
```
**Dependencies:** AsyncMock, isinstance, get, skipif, Mock
*...and 4 more*

---

### TestHealthAPI
**File:** `backend/tests/test_api_endpoints.py:360`
**Complexity:** 2
**Documentation:**
```
Test health check API endpoints
```
**Dependencies:** get, skipif, TestClient, patch, json

---

### TestProcessLogger
**File:** `backend/tests/test_core_functionality.py:16`
**Complexity:** 4
**Documentation:**
```
Test ProcessLogger functionality
```
**Dependencies:** object, start_process, end_process, ValueError, ProcessLogger
*...and 4 more*

---

### TestLoggingUtilities
**File:** `backend/tests/test_core_functionality.py:76`
**Complexity:** 3
**Documentation:**
```
Test logging utility functions
```
**Dependencies:** format, loads, LogRecord, Mock, assert_called_once
*...and 5 more*

---

### TestBaseProcessor
**File:** `backend/tests/test_core_functionality.py:159`
**Complexity:** 5
**Documentation:**
```
Test BaseProcessor functionality
```
**Dependencies:** stat, MockProcessor, append, validate_file, endswith
*...and 6 more*

---

### MockProcessor
**File:** `backend/tests/test_core_functionality.py:164`
**Complexity:** 5
**Dependencies:** stat, append, Mock, len, str
*...and 2 more*

---

### TestBaseComparator
**File:** `backend/tests/test_core_functionality.py:239`
**Complexity:** 14
**Documentation:**
```
Test BaseComparator functionality
```
**Dependencies:** isinstance, _is_numeric, strip, abs, float
*...and 10 more*

---

### MockComparator
**File:** `backend/tests/test_core_functionality.py:244`
**Complexity:** 14
**Dependencies:** isinstance, strip, abs, float, Mock
*...and 4 more*

---

### FileProcessingError
**File:** `backend/utils/exceptions.py:8`
**Complexity:** 1
**Documentation:**
```
Base exception for file processing errors
```
**Dependencies:** __init__, super

---

### UnsupportedFileTypeError
**File:** `backend/utils/exceptions.py:16`
**Complexity:** 1
**Documentation:**
```
Raised when file type is not supported
```
**Dependencies:** __init__, super

---

### FileSizeExceededError
**File:** `backend/utils/exceptions.py:25`
**Complexity:** 1
**Documentation:**
```
Raised when file size exceeds limit
```
**Dependencies:** __init__, super

---

### CorruptedFileError
**File:** `backend/utils/exceptions.py:34`
**Complexity:** 1
**Documentation:**
```
Raised when file is corrupted or invalid
```
**Dependencies:** __init__, super

---

### ProcessingFailedError
**File:** `backend/utils/exceptions.py:40`
**Complexity:** 1
**Documentation:**
```
Raised when file processing fails
```
**Dependencies:** __init__, super

---

### ComparisonError
**File:** `backend/utils/exceptions.py:50`
**Complexity:** 1
**Documentation:**
```
Base exception for comparison errors
```
**Dependencies:** __init__, super

---

### InvalidComparisonDataError
**File:** `backend/utils/exceptions.py:58`
**Complexity:** 1
**Documentation:**
```
Raised when comparison data is invalid
```
**Dependencies:** __init__, super

---

### ComparisonFailedError
**File:** `backend/utils/exceptions.py:64`
**Complexity:** 1
**Documentation:**
```
Raised when comparison process fails
```
**Dependencies:** __init__, super

---

### ExportError
**File:** `backend/utils/exceptions.py:70`
**Complexity:** 1
**Documentation:**
```
Base exception for export errors
```
**Dependencies:** __init__, super

---

### ExportGenerationError
**File:** `backend/utils/exceptions.py:78`
**Complexity:** 1
**Documentation:**
```
Raised when export generation fails
```
**Dependencies:** __init__, super

---

### InvalidExportFormatError
**File:** `backend/utils/exceptions.py:88`
**Complexity:** 1
**Documentation:**
```
Raised when export format is invalid
```
**Dependencies:** __init__, super

---

### ProcessLogger
**File:** `backend/utils/logger.py:15`
**Complexity:** 7
**Documentation:**
```
Enhanced logger for process tracking with structured data
```
**Dependencies:** info, uuid4, type, append, pop
*...and 10 more*

---

### StructuredFormatter
**File:** `backend/utils/logger.py:271`
**Complexity:** 7
**Documentation:**
```
Structured JSON formatter for better log parsing
```
**Dependencies:** getMessage, hasattr, isoformat, str, fromtimestamp
*...and 2 more*

---

### ColoredFormatter
**File:** `backend/utils/logger.py:310`
**Complexity:** 2
**Documentation:**
```
Colored console formatter for development
```
**Dependencies:** formatTime, formatException, get, getMessage

---

### CodeComponent
**File:** `doc_mapper.py:22`
**Complexity:** 1
**Documentation:**
```
Represents a code component extracted from source files
```

---

### DocumentationMapper
**File:** `doc_mapper.py:33`
**Complexity:** 60
**Documentation:**
```
Advanced documentation mapping and analysis system
```
**Dependencies:** walk, set, save_mappings, append, upper
*...and 55 more*

---

### ProjectRunner
**File:** `run_project.py:15`
**Complexity:** 53
**Dependencies:** iter, terminate, open, Thread, split
*...and 23 more*

---
