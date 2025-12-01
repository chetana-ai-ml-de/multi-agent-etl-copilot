"""
schema_agent.py

Lightweight "SchemaAgent" responsible for turning a pandas DataFrame
into a compact, LLM-friendly schema description.

In the Kaggle notebook, this output is passed into LlmAgents built
with Google ADK; here we keep the core logic as a plain Python module.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass
class SchemaSummary:
    """Container for the schema text and structured info."""
    schema_text: str
    columns: List[str]


class SchemaAgent:
    """
    Agent that inspects a DataFrame and emits a clean schema summary
    suitable for prompting an LLM / ADK LlmAgent.
    """

    def __init__(self, max_columns: int = 50) -> None:
        self.max_columns = max_columns

    def summarize(self, df: pd.DataFrame) -> SchemaSummary:
        """
        Build a bullet-style schema summary like:

        PROVNUM: object
        PROVNAME: object
        Hrs_RN: float64
        ...

        Parameters
        ----------
        df : pandas.DataFrame

        Returns
        -------
        SchemaSummary
        """
        lines: List[str] = []
        cols = list(df.columns)

        if len(cols) > self.max_columns:
            cols = cols[: self.max_columns]

        for col in cols:
            dtype = str(df[col].dtype)
            lines.append(f"{col}: {dtype}")

        schema_text = "\n".join(lines)
        return SchemaSummary(schema_text=schema_text, columns=list(df.columns))
