
---

## 📁 4. `src/validation_agent.py`

```python
"""
validation_agent.py

ValidationAgent inspects the generated pandas code and compares it against
the target schema / mapping instructions, returning a structured PASS/FAIL
result plus any issues.

In the notebook this is an ADK LlmAgent; here we call Gemini directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from google import genai

client = genai.Client()


@dataclass
class ValidationIssue:
    issue_type: str
    description: str


@dataclass
class ValidationResult:
    status: str  # "PASS" or "FAIL"
    issues: List[ValidationIssue]
    raw_text: str


VALIDATION_SYSTEM_PROMPT = """
You are a strict code reviewer for data pipelines.

You will receive:
- TARGET_SCHEMA: list of expected columns
- MAPPING_JSON: JSON with mapping meta
- TRANSFORMATION_CODE: pandas code that builds df_out

Your task:
1. Check whether all target fields are created.
2. Flag any references to non-existent columns.
3. Flag suspicious logic (e.g., missing components in aggregations).
4. Summarize issues in structured JSON with:
   - validation_result: "PASS" or "FAIL"
   - issues: list of {issue_type, description}

Be conservative and prioritize correctness.
"""


def validate_transformation_code(
    mapping_json: str,
    target_schema_text: str,
    transformation_code: str,
    model_name: str = "gemini-1.5-flash",
) -> ValidationResult:
    """
    Ask Gemini to validate the ETL code vs the mapping/target schema.

    Returns a ValidationResult with parsed issues (best-effort parsing).
    """
    prompt = f"""
{VALIDATION_SYSTEM_PROMPT}

TARGET_SCHEMA:
{target_schema_text}

MAPPING_JSON:
```json
{mapping_json}
