"""
mapping_agent.py

MappingAgent calls an LLM (Gemini) to propose a mapping
from a source schema to a desired target schema.

In the notebook, this logic is wrapped inside a Google ADK LlmAgent
and invoked via InMemoryRunner. Here we expose a simple function API
that the orchestrator can call.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from google import genai  # pip install google-genai

# Simple client; in the notebook you set GOOGLE_API_KEY in env or Kaggle secrets.
client = genai.Client()


@dataclass
class MappingResult:
    """Raw text mapping produced by the LLM."""
    raw_text: str


MAPPING_SYSTEM_PROMPT = """
You are a senior data engineer helping to map a SOURCE dataset to a TARGET schema.

You will be given:
- SOURCE_SCHEMA: list of source columns with dtypes
- TARGET_SCHEMA: list of target field names

Your job:
1. For each target field, decide how it can be produced from the source columns.
2. Classify each mapping as one of:
   - DIRECT: single source column maps directly to target.
   - DERIVED: computed from several source columns.
   - NO_MATCH: cannot be produced from the given source.
3. Return the result as a clear, human-readable table in Markdown,
   followed by a JSON block called `mapping_json` that can be used by code.

Keep mappings conservative. Do not hallucinate columns that do not exist
in the source schema.
"""


def generate_mapping(
    source_schema_text: str,
    target_schema_text: str,
    model_name: str = "gemini-1.5-flash",
) -> MappingResult:
    """
    Call Gemini to generate a mapping between source and target schemas.

    Parameters
    ----------
    source_schema_text : str
        Bullet-style schema (e.g. produced by SchemaAgent).
    target_schema_text : str
        Target field list, one per line.
    model_name : str
        Gemini model name.

    Returns
    -------
    MappingResult
    """
    prompt = f"""
{MAPPING_SYSTEM_PROMPT}

SOURCE_SCHEMA:
{source_schema_text}

TARGET_SCHEMA:
{target_schema_text}

Please respond with:
1. A Markdown table mapping target → source with mapping_type and notes.
2. A JSON object named `mapping_json` that my Python code can parse.
"""
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )

    # In most cases, .text will contain the full answer.
    text = getattr(response, "text", str(response))
    return MappingResult(raw_text=text)
