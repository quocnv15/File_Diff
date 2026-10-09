"""
Difference analysis and reporting utilities
"""

import logging
from typing import Dict, Any, List
from datetime import datetime

from app.models import DifferenceDetail, DifferenceSeverity

logger = logging.getLogger(__name__)


class DiffAnalyzer:
    """Utility class for analyzing differences and generating reports"""

    def __init__(self):
        self.severity_weights = {
            DifferenceSeverity.INFO: 1,
            DifferenceSeverity.WARNING: 5,
            DifferenceSeverity.ERROR: 10,
            DifferenceSeverity.CRITICAL: 20
        }

    def analyze_differences(self, differences: List[DifferenceDetail]) -> Dict[str, Any]:
        """Analyze differences and return summary statistics"""
        try:
            if not differences:
                return {
                    "total_differences": 0,
                    "severity_breakdown": {},
                    "field_breakdown": {},
                    "summary": "No differences found"
                }

            # Count by severity
            severity_counts = {}
            severity_scores = {}

            for diff in differences:
                severity = diff.severity
                severity_counts[severity.value] = severity_counts.get(severity.value, 0) + 1
                severity_scores[severity.value] = severity_scores.get(severity.value, 0) + self.severity_weights.get(severity, 1)

            # Count by field
            field_counts = {}
            field_severity = {}

            for diff in differences:
                field = diff.field
                field_counts[field] = field_counts.get(field, 0) + 1
                if field not in field_severity or self.severity_weights.get(diff.severity, 1) > self.severity_weights.get(field_severity[field], 1):
                    field_severity[field] = diff.severity

            # Calculate total score
            total_score = sum(severity_scores.values())

            # Generate summary
            summary = self._generate_summary(severity_counts, field_counts, total_score)

            return {
                "total_differences": len(differences),
                "severity_breakdown": severity_counts,
                "field_breakdown": field_counts,
                "field_severity": field_severity,
                "total_score": total_score,
                "summary": summary
            }

        except Exception as e:
            logger.error(f"Failed to analyze differences: {e}")
            return {"error": str(e)}

    def _generate_summary(self, severity_counts: Dict[str, int], field_counts: Dict[str, int], total_score: int) -> str:
        """Generate human-readable summary of differences"""
        try:
            parts = []

            if total_score == 0:
                return "No significant differences found"

            # Overall assessment
            if total_score >= 50:
                parts.append("Major differences detected")
            elif total_score >= 20:
                parts.append("Significant differences found")
            elif total_score >= 10:
                parts.append("Some differences detected")
            else:
                parts.append("Minor differences detected")

            # Severity breakdown
            if severity_counts.get(DifferenceSeverity.CRITICAL.value, 0) > 0:
                parts.append(f"{severity_counts[DifferenceSeverity.CRITICAL.value]} critical issues")

            if severity_counts.get(DifferenceSeverity.ERROR.value, 0) > 0:
                parts.append(f"{severity_counts[DifferenceSeverity.ERROR.value]} errors")

            if severity_counts.get(DifferenceSeverity.WARNING.value, 0) > 0:
                parts.append(f"{severity_counts[DifferenceSeverity.WARNING.value]} warnings")

            # Most affected fields
            if field_counts:
                most_affected_field = max(field_counts, key=field_counts.get)
                parts.append(f"'{most_affected_field}' has the most differences ({field_counts[most_affected_field]})")

            return ". ".join(parts) + "."

        except Exception as e:
            logger.error(f"Failed to generate summary: {e}")
            return "Unable to generate summary"

    def categorize_differences(self, differences: List[DifferenceDetail]) -> Dict[str, List[DifferenceDetail]]:
        """Categorize differences by type and severity"""
        try:
            categorized = {
                "critical": [],
                "errors": [],
                "warnings": [],
                "info": []
            }

            for diff in differences:
                severity = diff.severity
                if severity in categorized:
                    categorized[severity.value].append(diff)

            return categorized

        except Exception as e:
            logger.error(f"Failed to categorize differences: {e}")
            return {"error": str(e)}

    def get_field_analysis(self, differences: List[DifferenceDetail]) -> Dict[str, Dict[str, Any]]:
        """Get detailed analysis for each field"""
        try:
            field_analysis = {}

            # Group differences by field
            field_groups = {}
            for diff in differences:
                field = diff.field
                if field not in field_groups:
                    field_groups[field] = []
                field_groups[field].append(diff)

            # Analyze each field
            for field, diffs in field_groups.items():
                numeric_diffs = [d for d in diffs if self._is_numeric_difference(d)]
                text_diffs = [d for d in diffs if not self._is_numeric_difference(d)]

                # Calculate statistics for numeric differences
                numeric_stats = {}
                if numeric_diffs:
                    absolute_diffs = [d.difference for d in numeric_diffs if d.difference is not None]
                    percent_diffs = [d.percentage_diff for d in numeric_diffs if d.percentage_diff is not None]

                    if absolute_diffs:
                        numeric_stats = {
                            "avg_absolute_diff": sum(absolute_diffs) / len(absolute_diffs),
                            "max_absolute_diff": max(absolute_diffs),
                            "total_absolute_diff": sum(absolute_diffs)
                        }

                    if percent_diffs:
                        numeric_stats.update({
                            "avg_percent_diff": sum(percent_diffs) / len(percent_diffs),
                            "max_percent_diff": max(percent_diffs)
                        })

                field_analysis[field] = {
                    "total_differences": len(diffs),
                    "numeric_differences": len(numeric_diffs),
                    "text_differences": len(text_diffs),
                    "max_severity": self._get_max_severity(diffs),
                    "numeric_stats": numeric_stats,
                    "samples": diffs[:3]  # First 3 differences as samples
                }

            return field_analysis

        except Exception as e:
            logger.error(f"Failed to get field analysis: {e}")
            return {"error": str(e)}

    def _is_numeric_difference(self, diff: DifferenceDetail) -> bool:
        """Check if difference is numeric"""
        return diff.difference is not None and diff.percentage_diff is not None

    def _get_max_severity(self, differences: List[DifferenceDetail]) -> str:
        """Get maximum severity from differences"""
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

    def generate_recommendations(self, differences: List[DifferenceDetail]) -> List[str]:
        """Generate recommendations based on differences"""
        try:
            recommendations = []
            categorized = self.categorize_differences(differences)
            field_analysis = self.get_field_analysis(differences)

            # Critical issues
            if categorized["critical"]:
                recommendations.append("URGENT: Review critical differences immediately")

            # High-impact fields
            high_impact_fields = ["amount", "total", "price", "cost", "quantity"]
            for field in high_impact_fields:
                if field in field_analysis:
                    analysis = field_analysis[field]
                    if analysis["max_severity"] in ["error", "critical"]:
                        recommendations.append(f"Review {field} field - {analysis['total_differences']} differences found")

            # Multiple differences in same field
            for field, analysis in field_analysis.items():
                if analysis["total_differences"] > 5:
                    recommendations.append(f"Field '{field}' has {analysis['total_differences']} differences - consider data validation")

            # Large numeric differences
            for field, analysis in field_analysis.items():
                if analysis["numeric_stats"]:
                    stats = analysis["numeric_stats"]
                    if stats.get("max_percent_diff", 0) > 50:
                        recommendations.append(f"Large percentage differences detected in {field} field")

            # No differences
            if not differences:
                recommendations.append("Data comparison successful - no differences found")

            return recommendations[:5]  # Limit to top 5 recommendations

        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}")
            return ["Unable to generate recommendations"]

    def create_comparison_report(self, differences: List[DifferenceDetail], summary_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive comparison report"""
        try:
            # Analyze differences
            analysis = self.analyze_differences(differences)
            categorized = self.categorize_differences(differences)
            field_analysis = self.get_field_analysis(differences)
            recommendations = self.generate_recommendations(differences)

            # Create report
            report = {
                "generated_at": datetime.now().isoformat(),
                "summary_statistics": summary_stats,
                "difference_analysis": analysis,
                "categorized_differences": categorized,
                "field_analysis": field_analysis,
                "recommendations": recommendations,
                "top_issues": self._get_top_issues(differences)
            }

            return report

        except Exception as e:
            logger.error(f"Failed to create comparison report: {e}")
            return {"error": str(e), "generated_at": datetime.now().isoformat()}

    def _get_top_issues(self, differences: List[DifferenceDetail]) -> List[Dict[str, Any]]:
        """Get top issues based on severity and impact"""
        try:
            # Sort differences by severity and difference magnitude
            sorted_diffs = sorted(
                differences,
                key=lambda d: (
                    -self.severity_weights.get(d.severity, 1),
                    -(d.percentage_diff or 0)
                )
            )

            top_issues = []
            for diff in sorted_diffs[:10]:  # Top 10 issues
                issue = {
                    "field": diff.field,
                    "severity": diff.severity.value,
                    "value1": diff.value1,
                    "value2": diff.value2,
                    "difference": diff.difference,
                    "percentage_diff": diff.percentage_diff
                }
                top_issues.append(issue)

            return top_issues

        except Exception as e:
            logger.error(f"Failed to get top issues: {e}")
            return []