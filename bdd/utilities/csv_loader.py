"""
utilities/csv_loader.py
───────────────────────
Loads test data from  test_data/test_data.csv  and returns it as a
list of dicts — one dict per row.

Expected CSV columns:
    test_name | category | expected_url | sort_option | brand

Empty / NaN cells in sort_option and brand are normalised to "".

Usage
-----
    from utilities.csv_loader import load_test_data

    rows = load_test_data()          # uses default path
    rows = load_test_data("test_data/test_data.csv")   # explicit
"""

import os
import csv
from pathlib import Path


# ── default path relative to project root ────────────────────────────────────
_DEFAULT_CSV = Path(__file__).resolve().parent.parent / "test_data" / "test_data.csv"


def load_test_data(csv_path: str | Path | None = None) -> list[dict]:
    """
    Read test_data.csv and return a list of row dicts.

    Parameters
    ----------
    csv_path : str | Path | None
        Path to the CSV file.  Defaults to ``test_data/test_data.csv``
        relative to the project root (two levels above this file).

    Returns
    -------
    list[dict]
        One dict per CSV row.  Keys are column headers.
        ``sort_option`` and ``brand`` are always str (never None).

    Raises
    ------
    FileNotFoundError
        When the CSV file does not exist at the resolved path.
    ValueError
        When a required column is missing from the CSV.
    """
    path = Path(csv_path) if csv_path else _DEFAULT_CSV

    if not path.exists():
        raise FileNotFoundError(
            f"Test data CSV not found at: {path}\n"
            f"Make sure 'test_data/test_data.csv' exists in your project root."
        )

    required_columns = {"test_name", "category", "expected_url"}
    optional_columns = {"sort_option", "brand"}

    rows: list[dict] = []

    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)

        # ── validate headers ──────────────────────────────────────────────
        headers = set(reader.fieldnames or [])
        missing = required_columns - headers
        if missing:
            raise ValueError(
                f"CSV is missing required column(s): {missing}. "
                f"Found columns: {headers}"
            )

        for raw in reader:
            row = {k: (v or "").strip() for k, v in raw.items()}

            # normalise optional columns to "" when absent or blank
            for col in optional_columns:
                row.setdefault(col, "")

            rows.append(row)

    return rows


def positive_rows(rows: list[dict] | None = None) -> list[dict]:
    """Return only rows whose test_name does NOT end with '_negative'."""
    data = rows if rows is not None else load_test_data()
    return [r for r in data if not r["test_name"].endswith("_negative")]


def negative_rows(rows: list[dict] | None = None) -> list[dict]:
    """Return only rows whose test_name ends with '_negative'."""
    data = rows if rows is not None else load_test_data()
    return [r for r in data if r["test_name"].endswith("_negative")]


def row_by_name(name: str, rows: list[dict] | None = None) -> dict:
    """
    Return the single row matching *name* (exact, case-sensitive).

    Raises KeyError when the name is not found.
    """
    data = rows if rows is not None else load_test_data()
    for r in data:
        if r["test_name"] == name:
            return r
    raise KeyError(f"No test row with test_name='{name}' found in CSV.")