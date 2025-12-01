
---

## 📁 5. `src/documentation_agent.py`

```python
"""
documentation_agent.py

DocumentationAgent builds a final Markdown report describing the ETL pipeline:
- problem statement
- schema summary
- mapping table
- generated code
- validation summary

This mirrors what you wrote in the Kaggle project description, but generated
programmatically so the agent system can be reused on any dataset.
"""

from __future__ import annotations

from dataclasses import dataclass

from google import genai

client = genai.Client()


@dataclass
class DocumentationResult:
    markdown: str


DOCUMENTATION_SYSTEM_PROMPT = """
You are a technical writer for data engineering teams.

You will be given:
- A problem description (one paragraph).
- Source schema summary.
- Target schema.
- Mapping summary.
- Transformation code.
- Validation summary.

Write a clear, concise Markdown document that includes:
1. Short problem statement.
2. Overview of the solution (multi-agent ETL copilot).
3. Source vs Target schema section.
4. Mapping table or bullet list.
5. Code snippet section with the ETL code.
6. Validation summary (PASS/FAIL and main issues).
7. Short conclusion.

This document will be stored as docs/final_documentation.md in a GitHub repo.
"""


def generate_documentation(
    problem_statement: str,
    source_schema_text: str,
    target_schema_text: str,
    mapping_summary_text: str,
    transformation_code: str,
    validation_text: str,
    model_name: str = "gemini-1.5-flash",
) -> DocumentationResult:
    """
    Ask Gemini to generate a final Markdown documentation file.
    """
    prompt = f"""
{DOCUMENTATION_SYSTEM_PROMPT}

PROBLEM STATEMENT:
{problem_statement}

SOURCE SCHEMA:
{source_schema_text}

TARGET SCHEMA:
{target_schema_text}

MAPPING SUMMARY:
{mapping_summary_text}

TRANSFORMATION CODE:
```python
{transformation_code}
