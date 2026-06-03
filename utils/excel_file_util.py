import pandas as pd
from pathlib import Path
from typing import List, Any
from models.test_case_model import TestCase


class ExcelUtil:

    def __init__(self, file_path: str = "test_cases.xlsx"):
        self.file_path = Path(file_path)

    def safe_steps(steps):
        if not steps:
            return ""

        cleaned = []

        for s in steps:
            if isinstance(s, str):
                cleaned.append(s)
            elif hasattr(s, "title"):   # mistakenly nested TestCase
                cleaned.append(s.title)
            else:
                cleaned.append(str(s))

        return "\n".join(cleaned)

    safe_steps = staticmethod(safe_steps)

    def _normalize(self, tc: Any, idx: int) -> dict:
        """
        Convert any LLM output format into a clean dict.
        Supports:
        - Pydantic TestCase
        - dict
        - tuple
        """

        # Case 1: Pydantic model (v2) or Pydantic v1 (`dict()`)
        if hasattr(tc, "model_dump"):
            tc = tc.model_dump()
        elif hasattr(tc, "dict"):
            # pydantic v1
            tc = tc.dict()

        # Case 2: tuple (your error case)
        elif isinstance(tc, tuple):
            tc = {
                "title": tc[0] if len(tc) > 0 else "",
                "steps": tc[1] if len(tc) > 1 else [],
                "expected_result": tc[2] if len(tc) > 2 else ""
            }

        # Case 3: already dict
        elif isinstance(tc, dict):
            tc = tc

        else:
            raise TypeError(f"Unsupported test case type: {type(tc)}")

        # Ensure required keys exist
        return {
            "test_case_id": tc.get("test_case_id", f"TC-{idx:03d}"),
            "title": tc.get("title", ""),
            "steps": tc.get("steps", []),
            "expected_result": tc.get("expected_result", "")
        }

    def export(self, test_cases: List[Any]) -> str:

        # Accept a Pydantic model (e.g., TestSuite) or a dict with a `test_cases` key
        if hasattr(test_cases, "model_dump"):
            dumped = test_cases.model_dump()
            if isinstance(dumped, dict) and "test_cases" in dumped:
                test_cases = dumped["test_cases"]
        elif isinstance(test_cases, dict) and "test_cases" in test_cases:
            test_cases = test_cases["test_cases"]

        if not test_cases:
            raise ValueError("No test cases provided")

        rows = []

        for idx, tc in enumerate(test_cases, start=1):
            data = self._normalize(tc, idx)

            rows.append({
                "Test Case ID": data["test_case_id"],
                "Title": data["title"],
                "Steps": self.safe_steps(data["steps"]) if isinstance(data["steps"], list) else str(data["steps"]),
                "Expected Result": data["expected_result"]
            })

        # Create DataFrame with fixed column order to avoid accidental duplicate/misaligned columns
        columns = ["Test Case ID", "Title", "Steps", "Expected Result"]
        df = pd.DataFrame(rows)
        # Reindex ensures columns are in the desired order and missing columns appear as empty
        df = df.reindex(columns=columns)

        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        df.to_excel(self.file_path, index=False)

        return str(self.file_path)