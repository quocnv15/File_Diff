"""
Abstract base comparator for data comparison
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging

from utils.logger import get_process_logger

logger = logging.getLogger(__name__)


class BaseComparator(ABC):
    """Abstract base class for data comparators"""

    def __init__(self):
        self.tolerance_settings = {
            "quantity": 0.1,      # 10% tolerance
            "unit_price": 0.01,   # 1% tolerance
            "amount": 0.01        # 1% tolerance
        }
        self.process_logger = get_process_logger(f"{__name__}.{self.__class__.__name__}")

    @abstractmethod
    async def compare(self, data1: List[Dict], data2: List[Dict], options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Compare two datasets

        Args:
            data1: First dataset
            data2: Second dataset
            options: Comparison options

        Returns:
            Dictionary containing comparison results
        """
        pass

    def _normalize_value(self, value: Any) -> Any:
        """Normalize value for comparison"""
        if value is None:
            return ""
        elif isinstance(value, str):
            return value.strip().lower()
        elif isinstance(value, (int, float)):
            return float(value)
        else:
            return str(value).strip().lower()

    def _is_numeric(self, value: Any) -> bool:
        """Check if value is numeric"""
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    def _parse_numeric(self, value: Any) -> float:
        """Parse value as number"""
        try:
            # Remove common formatting characters
            if isinstance(value, str):
                clean_value = value.replace(',', '').replace('$', '').strip()
                return float(clean_value)
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def _compare_numbers(self, val1: float, val2: float, tolerance: float = 0.0) -> bool:
        """Compare two numbers with tolerance"""
        if val1 == 0 and val2 == 0:
            return True
        elif val1 == 0 or val2 == 0:
            return abs(val1 - val2) < tolerance
        else:
            relative_diff = abs(val1 - val2) / max(abs(val1), abs(val2))
            return relative_diff <= tolerance

    def _calculate_percentage_difference(self, val1: float, val2: float) -> float:
        """Calculate percentage difference between two numbers"""
        if val1 == 0 and val2 == 0:
            return 0.0
        elif val1 == 0:
            return 100.0 if val2 != 0 else 0.0
        else:
            return abs((val2 - val1) / val1) * 100

    def _determine_severity(self, field_name: str, diff_percentage: float, absolute_diff: float) -> str:
        """Determine severity level of difference"""
        # Critical fields
        critical_fields = ["amount", "total", "price", "cost"]
        if any(field in field_name.lower() for field in critical_fields):
            if diff_percentage > 5 or absolute_diff > 1000:
                return "critical"
            elif diff_percentage > 1 or absolute_diff > 100:
                return "error"
            else:
                return "warning"

        # Warning fields
        warning_fields = ["quantity", "qty", "count"]
        if any(field in field_name.lower() for field in warning_fields):
            if diff_percentage > 10:
                return "error"
            elif diff_percentage > 5:
                return "warning"
            else:
                return "info"

        # Default severity based on difference
        if diff_percentage > 20:
            return "error"
        elif diff_percentage > 10:
            return "warning"
        else:
            return "info"

    def get_comparator_info(self) -> Dict[str, Any]:
        """Get comparator information"""
        return {
            "name": self.__class__.__name__,
            "tolerance_settings": self.tolerance_settings
        }