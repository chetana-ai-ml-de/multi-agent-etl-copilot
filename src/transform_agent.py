"""
transform_agent.py

TransformAgent converts a logical mapping into runnable pandas code.

In the notebook, an ADK LlmAgent takes mapping_json + schema and emits
a code block. Here we rely on Gemini directly and return the code as text.
"""

from __future__ import annotations

from dataclasses import dataclass

from google import genai

client = genai.Client()


@dataclass
class TransformResult:
    """Holds the ETL code string produced by the LLM."""
    code: str


TRANSFORM_SYSTEM_PROMPT = """
You are a senior Python data engineer.

You are given:
- A logical mapping (in JSON) from source columns to target fields.
- The target schema (list of fields in final DataFrame).

Write clean, idiomatic pandas code that:

1. Assumes there is an input DataFrame named `df`.
2. Creates a new DataFrame named `df_out`.
3. Renames or derives columns to produce ALL target fields.
4. Uses .fillna(0) for numeric aggregates where appropriate.
5. Avoids referencing any column that does not exist in the mapping.
6. Ends with df_out containing ONLY the target columns in the correct order.

Return ONLY a Python code block; no explanation.
"""


def generate_transformation_code(
    mapping_json: str,
    target_schema_text: str,
    model_name: str = "gemini-1.5-flash",
) -> TransformResult:
    """
    Ask Gemini to generate pandas transformation code for df → df_out.

    Parameters
    ----------
    mapping_json : str
        JSON object describing how to derive each target field.
    target_schema_text : str
        Target field list, one per line.
    model_name : str
        Gemini model name.

    Returns
    -------
    TransformResult
    """
    prompt = f"""
{TRANSFORM_SYSTEM_PROMPT}

TARGET_SCHEMA:
{target_schema_text}

MAPPING_JSON:
```json
{mapping_json}
