
---

## 📁 6. `src/orchestrator.py`

```python
"""
orchestrator.py

High-level orchestration for the Multi-Agent ETL Copilot.

This module ties together:
- SchemaAgent
- MappingAgent
- TransformAgent
- ValidationAgent
- DocumentationAgent

In the Kaggle notebook you wrap each step in Google ADK LlmAgents and
InMemoryRunner; here we keep a simple synchronous orchestrator so the
judges can easily understand the flow.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any

import pandas as pd

from .schema_agent import SchemaAgent
from .mapping_agent import generate_mapping
from .transform_agent import generate_transformation_code
from .validation_agent import validate_transformation_code
from .documentation_agent import generate_documentation


DEFAULT_TARGET_SCHEMA = """
facility_id
facility_name
state
county_name
quarter
work_date
resident_census
rn_hours_total
lpn_hours_total
cna_hours_total
total_nursing_hours
""".strip()


PROBLEM_STATEMENT = """
Many teams receive raw tabular data with inconsistent schemas across files
and sources. They must repeatedly map columns, write pandas ETL code,
validate logic, and document the pipeline. This Multi-Agent ETL Copilot
automates those steps using LLM-powered agents built on Google ADK.
""".strip()


@dataclass
class PipelineOutput:
    df: pd.DataFrame
    source_schema_text: str
    target_schema_text: str
    mapping_text: str
    transformation_code: str
    validation_text: str
    documentation_markdown: str


def run_pipeline(
    csv_path: str,
    target_schema_text: str = DEFAULT_TARGET_SCHEMA,
) -> PipelineOutput:
    """
    Main convenience function used by the Kaggle notebook and for the GitHub repo.

    Parameters
    ----------
    csv_path : str
        Path to source CSV file.
    target_schema_text : str
        Target schema (one field per line). Default is the nursing example.

    Returns
    -------
    PipelineOutput
    """
    csv_path = str(Path(csv_path))
    df = pd.read_csv(csv_path)

    # 1. SchemaAgent
    schema_agent = SchemaAgent()
    schema_summary = schema_agent.summarize(df)
    source_schema_text = schema_summary.schema_text

    # 2. MappingAgent
    mapping_result = generate_mapping(
        source_schema_text=source_schema_text,
        target_schema_text=target_schema_text,
    )
    mapping_text = mapping_result.raw_text

    # (Optional) you can parse mapping_json from mapping_text using regex in notebook.

    # 3. TransformAgent
    # For GitHub we pass the whole mapping_text; in notebook you extract mapping_json.
    transformation_result = generate_transformation_code(
        mapping_json=mapping_text,
        target_schema_text=target_schema_text,
    )
    transformation_code = transformation_result.code

    # 4. ValidationAgent
    validation_result = validate_transformation_code(
        mapping_json=mapping_text,
        target_schema_text=target_schema_text,
        transformation_code=transformation_code,
    )
    validation_text = validation_result.raw_text

    # 5. DocumentationAgent
    documentation_result = generate_documentation(
        problem_statement=PROBLEM_STATEMENT,
        source_schema_text=source_schema_text,
        target_schema_text=target_schema_text,
        mapping_summary_text=mapping_text,
        transformation_code=transformation_code,
        validation_text=validation_text,
    )
    documentation_markdown = documentation_result.markdown

    return PipelineOutput(
        df=df,
        source_schema_text=source_schema_text,
        target_schema_text=target_schema_text,
        mapping_text=mapping_text,
        transformation_code=transformation_code,
        validation_text=validation_text,
        documentation_markdown=documentation_markdown,
    )


def run_pipeline_as_dict(csv_path: str) -> Dict[str, Any]:
    """
    Helper that returns a plain dict, convenient for notebooks / JSON export.
    """
    out = run_pipeline(csv_path)
    return {
        "source_schema_text": out.source_schema_text,
        "target_schema_text": out.target_schema_text,
        "mapping_text": out.mapping_text,
        "transformation_code": out.transformation_code,
        "validation_text": out.validation_text,
        "documentation_markdown": out.documentation_markdown,
    }
