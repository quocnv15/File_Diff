"""
Main data comparator for comparing structured data
"""

import logging
import time
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

from comparators.base_comparator import BaseComparator
from app.models import (
    ComparisonResult, ComparisonSummary, DifferenceDetail,
    DifferenceSeverity, ProcessingStatus
)
from utils.exceptions import ComparisonFailedError

logger = logging.getLogger(__name__)


class DataComparator(BaseComparator):
    """Main data comparator implementation"""

    def __init__(self):
        super().__init__()
        self.field_mappings = {
            "product_name": ["description", "product", "item", "name", "mô tả", "sản phẩm"],
            "quantity": ["quantity", "qty", "amount", "count", "số lượng"],
            "unit_price": ["unit_price", "price", "rate", "đơn giá", "giá"],
            "total_amount": ["amount", "total", "sum", "thành tiền", "tổng"]
        }

    async def compare(self, data1: List[Dict], data2: List[Dict], options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Compare two datasets and return detailed comparison results

        Args:
            data1: First dataset (list of structured data)
            data2: Second dataset (list of structured data)
            options: Comparison options including tolerance settings

        Returns:
            Dictionary containing comparison results
        """
        try:
            start_time = time.time()
            options = options or {}

            logger.info(f"Starting comparison between {len(data1)} and {len(data2)} data items")

            # Extract table data from structured data
            table1 = self._extract_table_data(data1)
            table2 = self._extract_table_data(data2)

            if not table1 or not table2:
                raise ComparisonFailedError("No valid table data found for comparison")

            # Perform comparison
            comparison_result = await self._perform_comparison(table1, table2, options)

            # Add metadata
            comparison_result["processing_time"] = time.time() - start_time
            comparison_result["comparison_id"] = str(uuid.uuid4())
            comparison_result["processed_at"] = datetime.now()

            logger.info(f"Comparison completed in {comparison_result['processing_time']:.2f}s")

            return comparison_result

        except Exception as e:
            logger.error(f"Comparison failed: {e}", exc_info=True)
            raise ComparisonFailedError(f"Comparison failed: {str(e)}")

    def _extract_table_data(self, structured_data: List[Dict]) -> Optional[Dict[str, Any]]:
        """Extract table data from structured data"""
        try:
            # Find the first table in structured data
            for item in structured_data:
                if item.get("type") == "table":
                    return {
                        "headers": item.get("headers", []),
                        "rows": item.get("rows", []),
                        "row_count": item.get("row_count", 0),
                        "column_count": item.get("column_count", 0)
                    }
            return None

        except Exception as e:
            logger.error(f"Failed to extract table data: {e}")
            return None

    async def _perform_comparison(self, table1: Dict, table2: Dict, options: Dict[str, Any]) -> Dict[str, Any]:
        """Perform actual comparison between two tables"""
        try:
            # Initialize results
            matches = []
            differences = []
            missing_rows = []

            # Get tolerance settings
            tolerance_settings = options.get("tolerance_settings", {})
            self.tolerance_settings.update(tolerance_settings)

            # Determine comparison method
            exact_match = options.get("exact_match", True)
            ignore_formatting = options.get("ignore_formatting", True)

            # Create field mapping if provided
            field_mapping = options.get("field_mapping")
            if field_mapping:
                self._apply_field_mapping(field_mapping)

            # Row-by-row comparison
            max_rows = max(len(table1["rows"]), len(table2["rows"]))

            for row_index in range(max_rows):
                row1_data = table1["rows"][row_index] if row_index < len(table1["rows"]) else None
                row2_data = table2["rows"][row_index] if row_index < len(table2["rows"]) else None

                if row1_data is None and row2_data is None:
                    continue

                # Handle missing rows
                if row1_data is None:
                    missing_rows.append({
                        "type": "missing_in_file1",
                        "row_number": row_index + 1,
                        "data": row2_data,
                        "headers": table2["headers"]
                    })
                    continue

                if row2_data is None:
                    missing_rows.append({
                        "type": "missing_in_file2",
                        "row_number": row_index + 1,
                        "data": row1_data,
                        "headers": table1["headers"]
                    })
                    continue

                # Compare the two rows
                comparison = await self._compare_rows(
                    row1_data, row2_data, table1["headers"], table2["headers"],
                    exact_match, ignore_formatting
                )
                # Set the row number
                comparison["row_number"] = row_index + 1

                if comparison["status"] == "match":
                    matches.append(comparison)
                else:
                    differences.append(comparison)

            # Calculate summary statistics
            total_rows = max_rows
            matching_rows = len(matches)
            different_rows = len(differences)
            missing_count = len(missing_rows)
            accuracy_rate = (matching_rows / total_rows * 100) if total_rows > 0 else 0

            summary = ComparisonSummary(
                total_rows_compared=total_rows,
                matching_rows=matching_rows,
                different_rows=different_rows,
                missing_rows=missing_count,
                accuracy_rate=round(accuracy_rate, 2),
                total_differences=len(differences) + len(missing_rows),
                comparison_time=0.0  # Will be updated by caller
            )

            return {
                "matches": matches,
                "differences": differences,
                "missing_rows": missing_rows,
                "summary": summary.dict(),
                "table1_info": {
                    "row_count": len(table1["rows"]),
                    "column_count": len(table1["headers"])
                },
                "table2_info": {
                    "row_count": len(table2["rows"]),
                    "column_count": len(table2["headers"])
                }
            }

        except Exception as e:
            logger.error(f"Failed to perform comparison: {e}")
            raise

    async def _compare_rows(self, row1: List, row2: List, headers1: List, headers2: List,
                          exact_match: bool, ignore_formatting: bool) -> Dict[str, Any]:
        """Compare two rows"""
        try:
            comparison = {
                "row_number": 0,  # Will be set by caller
                "status": "match",
                "differences": [],
                "row1_data": dict(zip(headers1, row1)),
                "row2_data": dict(zip(headers2, row2))
            }

            # Compare each field
            min_cols = min(len(headers1), len(headers2))

            for col_index in range(min_cols):
                field_name = headers1[col_index].lower()
                value1 = self._normalize_value(row1[col_index]) if ignore_formatting else row1[col_index]
                value2 = self._normalize_value(row2[col_index]) if ignore_formatting else row2[col_index]

                # Check if values match
                if not self._values_match(value1, value2, field_name, exact_match):
                    # Create difference detail
                    difference = self._create_difference_detail(
                        field_name, value1, value2, headers1[col_index], comparison.get("row_number", 0)
                    )
                    comparison["differences"].append(difference)

            # Determine overall status
            if comparison["differences"]:
                comparison["status"] = "difference"
                # Determine severity based on differences
                max_severity = self._get_max_severity(comparison["differences"])
                comparison["severity"] = max_severity
            else:
                comparison["status"] = "match"
                comparison["severity"] = "info"

            return comparison

        except Exception as e:
            logger.error(f"Failed to compare rows: {e}")
            return {
                "status": "error",
                "differences": [],
                "error": str(e)
            }

    def _values_match(self, val1: Any, val2: Any, field_name: str, exact_match: bool) -> bool:
        """Check if two values match based on field type and comparison options"""
        try:
            # Handle empty values
            if val1 in ["", None] and val2 in ["", None]:
                return True
            if val1 in ["", None] or val2 in ["", None]:
                return False

            # Exact match for text fields
            if not exact_match:
                return str(val1).strip().lower() == str(val2).strip().lower()

            # Numeric comparison with tolerance
            if self._is_numeric(val1) and self._is_numeric(val2):
                num1 = self._parse_numeric(val1)
                num2 = self._parse_numeric(val2)

                # Determine tolerance based on field name
                tolerance = self._get_field_tolerance(field_name)
                return self._compare_numbers(num1, num2, tolerance)

            # Text comparison
            return str(val1).strip() == str(val2).strip()

        except Exception as e:
            logger.error(f"Error comparing values: {e}")
            return False

    def _get_field_tolerance(self, field_name: str) -> float:
        """Get tolerance setting for a specific field"""
        field_name = field_name.lower()

        # Check if field name contains any keywords
        for key, tolerance in self.tolerance_settings.items():
            if key in field_name:
                return tolerance

        # Default tolerance
        return 0.0

    def _create_difference_detail(self, field_name: str, val1: Any, val2: Any, display_name: str, row_number: int = 0) -> DifferenceDetail:
        """Create a difference detail object"""
        try:
            # Calculate difference for numeric values
            absolute_diff = None
            percentage_diff = None

            if self._is_numeric(val1) and self._is_numeric(val2):
                num1 = self._parse_numeric(val1)
                num2 = self._parse_numeric(val2)
                absolute_diff = abs(num2 - num1)
                percentage_diff = self._calculate_percentage_difference(num1, num2)

            # Determine severity
            severity_str = self._determine_severity(field_name, percentage_diff or 0, absolute_diff or 0)
            severity = DifferenceSeverity(severity_str)

            return DifferenceDetail(
                row_number=row_number,
                field=field_name,
                value1=val1,
                value2=val2,
                difference=absolute_diff,
                percentage_diff=percentage_diff,
                severity=severity
            )

        except Exception as e:
            logger.error(f"Error creating difference detail: {e}")
            return DifferenceDetail(
                row_number=row_number,
                field=field_name,
                value1=str(val1),
                value2=str(val2),
                severity=DifferenceSeverity.ERROR
            )

    def _get_max_severity(self, differences: List[DifferenceDetail]) -> str:
        """Get maximum severity from list of differences"""
        if not differences:
            return "info"

        severity_order = {
            DifferenceSeverity.INFO: 0,
            DifferenceSeverity.WARNING: 1,
            DifferenceSeverity.ERROR: 2,
            DifferenceSeverity.CRITICAL: 3
        }

        max_severity = DifferenceSeverity.INFO
        for diff in differences:
            if severity_order.get(diff.severity, 0) > severity_order.get(max_severity, 0):
                max_severity = diff.severity

        return max_severity.value

    def _apply_field_mapping(self, field_mapping: Dict[str, List[str]]):
        """Apply custom field mapping"""
        # This method can be used to customize field mappings
        # For now, we'll keep the default mappings
        pass