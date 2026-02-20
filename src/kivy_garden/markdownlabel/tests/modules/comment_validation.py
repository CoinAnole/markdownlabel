"""Comment format validation for property-based test documentation.

This module provides tools for validating comment formats against standardized
patterns and generating standardized comments.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict


# =============================================================================
# ENUMS AND DATA MODELS
# =============================================================================

class StrategyType(Enum):
    """Strategy types for comment format classification."""
    BOOLEAN = "Boolean"
    SMALL_FINITE = "Small finite"
    MEDIUM_FINITE = "Medium finite"
    COMPLEX = "Complex"
    COMBINATION = "Combination"


@dataclass
class CommentPattern:
    """Data model for standardized comment patterns."""
    strategy_type: str
    max_examples: int
    rationale: str
    line_number: Optional[int] = None
    original_comment: Optional[str] = None

    def to_standardized_format(self) -> str:
        """Convert to standardized comment format."""
        return f"# {self.strategy_type} strategy: {self.max_examples} examples ({self.rationale})"


@dataclass
class ValidationResult:
    """Result of comment format validation."""
    is_valid: bool
    error_type: Optional[str]
    message: str
    original_comment: str
    parsed_pattern: Optional[CommentPattern] = None


# =============================================================================
# COMMENT FORMAT VALIDATION
# =============================================================================

class CommentFormatValidator:
    """Validates comment formats against standardized patterns."""

    def __init__(self):
        """Initialize validator with format patterns and templates."""
        self.standard_pattern = re.compile(
            r'^#\s*(\w+(?:\s+\w+)*)\s+strategy:\s*(\d+)\s+examples\s*\(([^)]+)\)\s*$',
            re.IGNORECASE
        )

        self.rationale_templates = {
            StrategyType.BOOLEAN: [
                "True/False coverage",
                "boolean coverage"
            ],
            StrategyType.SMALL_FINITE: [
                r"input space size: \d+",
                r"input space size",
                r"finite coverage"
            ],
            StrategyType.MEDIUM_FINITE: [
                "adequate finite coverage",
                "finite coverage"
            ],
            StrategyType.COMPLEX: [
                "adequate coverage",
                "performance optimized",
                "complexity coverage",
                "CI optimized"
            ],
            StrategyType.COMBINATION: [
                "combination coverage",
                "product coverage",
                "performance optimized",
                "CI optimized"
            ]
        }

        self.valid_strategy_types = {
            strategy_type.value.lower(): strategy_type
            for strategy_type in StrategyType
        }

    def validate_comment_format(self, comment: str) -> ValidationResult:
        """Validate a comment against the standardized format."""
        comment = comment.strip()

        match = self.standard_pattern.match(comment)
        if not match:
            return ValidationResult(
                is_valid=False,
                error_type="FORMAT_VIOLATION",
                message="Comment does not match standard format: "
                "'# [Strategy Type] strategy: [N] examples ([Rationale])'",
                original_comment=comment
            )

        strategy_type_str, max_examples_str, rationale = match.groups()

        strategy_type_lower = strategy_type_str.lower()
        if strategy_type_lower not in self.valid_strategy_types:
            return ValidationResult(
                is_valid=False,
                error_type="INVALID_STRATEGY_TYPE",
                message=f"Invalid strategy type: '{strategy_type_str}'. "
                f"Valid types: {list(self.valid_strategy_types.keys())}",
                original_comment=comment
            )

        try:
            max_examples = int(max_examples_str)
            if max_examples <= 0:
                return ValidationResult(
                    is_valid=False,
                    error_type="INVALID_MAX_EXAMPLES",
                    message=f"max_examples must be positive integer, got: {max_examples}",
                    original_comment=comment
                )
        except ValueError:
            return ValidationResult(
                is_valid=False,
                error_type="INVALID_MAX_EXAMPLES",
                message=f"max_examples must be integer, got: '{max_examples_str}'",
                original_comment=comment
            )

        strategy_type = self.valid_strategy_types[strategy_type_lower]
        if not self._validate_rationale(rationale, strategy_type):
            expected_templates = self.rationale_templates[strategy_type]
            return ValidationResult(
                is_valid=False,
                error_type="INVALID_RATIONALE",
                message=f"Rationale '{rationale}' doesn't match expected "
                f"patterns for {strategy_type.value}: {expected_templates}",
                original_comment=comment
            )

        return ValidationResult(
            is_valid=True,
            error_type=None,
            message="Comment format is valid",
            original_comment=comment,
            parsed_pattern=CommentPattern(
                strategy_type=strategy_type.value,
                max_examples=max_examples,
                rationale=rationale
            )
        )

    def _validate_rationale(self, rationale: str, strategy_type: StrategyType) -> bool:
        """Validate rationale against expected templates for strategy type."""
        templates = self.rationale_templates[strategy_type]
        rationale_lower = rationale.lower().strip()

        for template in templates:
            if template.startswith(r"input space size"):
                if re.match(r"input space size:?\s*\d*", rationale_lower):
                    return True
            else:
                if template.lower() in rationale_lower:
                    return True

        return False

    def generate_standard_comment(
        self,
        strategy_type: StrategyType,
        max_examples: int,
        input_space_size: Optional[int] = None
    ) -> str:
        """Generate a standardized comment for given parameters."""
        if strategy_type == StrategyType.BOOLEAN:
            rationale = "True/False coverage"
        elif strategy_type == StrategyType.SMALL_FINITE:
            if input_space_size is not None:
                rationale = f"input space size: {input_space_size}"
            else:
                rationale = "finite coverage"
        elif strategy_type == StrategyType.MEDIUM_FINITE:
            rationale = "adequate finite coverage"
        elif strategy_type == StrategyType.COMPLEX:
            rationale = "adequate coverage"
        elif strategy_type == StrategyType.COMBINATION:
            rationale = "combination coverage"
        else:
            rationale = "adequate coverage"

        pattern = CommentPattern(
            strategy_type=strategy_type.value,
            max_examples=max_examples,
            rationale=rationale
        )

        return pattern.to_standardized_format()


class CommentFormatRegistry:
    """Registry of format templates and validation rules."""

    def __init__(self):
        """Initialize registry with standard format templates."""
        self.validator = CommentFormatValidator()

        self.format_templates = {
            StrategyType.BOOLEAN: "# Boolean strategy: {max_examples} examples "
            "(True/False coverage)",
            StrategyType.SMALL_FINITE: "# Small finite strategy: {max_examples} "
            "examples (input space size: {input_space_size})",
            StrategyType.MEDIUM_FINITE: "# Medium finite strategy: {max_examples} "
            "examples (adequate finite coverage)",
            StrategyType.COMPLEX: "# Complex strategy: {max_examples} examples "
            "(adequate coverage)",
            StrategyType.COMBINATION: "# Combination strategy: {max_examples} "
            "examples (combination coverage)"
        }

    def get_template(self, strategy_type: StrategyType) -> str:
        """Get format template for strategy type."""
        return self.format_templates.get(strategy_type, self.format_templates[StrategyType.COMPLEX])

    def get_all_templates(self) -> Dict[StrategyType, str]:
        """Get all format templates."""
        return self.format_templates.copy()


__all__ = [
    'StrategyType',
    'CommentPattern',
    'ValidationResult',
    'CommentFormatValidator',
    'CommentFormatRegistry',
]
