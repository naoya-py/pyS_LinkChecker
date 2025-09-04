"""Documentation-only stub for mytool module.

This module contains PEP 257 docstrings describing the public API used by
pyS_LinkChecker. It intentionally does not implement network calls or
third-party imports; it's safe to import in a documentation build or tests.
"""

from typing import Iterable, List, Dict


def fetch(session, url: str, sem, timeout: int = 15) -> Dict:
    """Perform an HTTP GET for a single URL and return status information.

    Parameters
    ----------
    session : object
        A session-like object (documentation-only placeholder).
    url : str
        The URL to request.
    sem : object
        A semaphore-like object used to limit concurrency.
    timeout : int, optional
        Request timeout in seconds (default: 15).

    Returns
    -------
    dict
        A dictionary with the keys:
        - ``url`` (str): requested URL
        - ``status`` (int|None): HTTP status code or ``None`` on failure
        - ``reason`` (str|None): textual HTTP reason or error message
        - ``elapsed_ms`` (float|None): elapsed time in milliseconds
        - ``ok`` (bool): True for 2xx responses
    """
    raise NotImplementedError("Documentation-only stub")


def check_urls(urls: Iterable[str], concurrency: int = 10, timeout: int = 15, console=None) -> List[Dict]:
    """Check multiple URLs concurrently and return results list.

    Parameters
    ----------
    urls : Iterable[str]
        Iterable of URL strings to check.
    concurrency : int, optional
        Maximum number of concurrent workers (default: 10).
    timeout : int, optional
        Per-request timeout in seconds (default: 15).
    console : object, optional
        Optional console object for progress output (documentation-only).

    Returns
    -------
    List[dict]
        A list of result dictionaries as returned by :func:`fetch`.
    """
    raise NotImplementedError("Documentation-only stub")


def read_urls(path: str) -> List[str]:
    """Read URLs from a text file, ignoring blank lines and comments.

    Parameters
    ----------
    path : str
        Path to a newline-separated text file of URLs.

    Returns
    -------
    List[str]
        Parsed list of URLs.
    """
    raise NotImplementedError("Documentation-only stub")


def write_csv(path: str, rows: List[Dict], checked_at: str) -> None:
    """Write results to a CSV file using UTF-8 encoding.

    Parameters
    ----------
    path : str
        Target CSV file path.
    rows : List[dict]
        Rows to write (each row is a dict with keys described in :func:`fetch`).
    checked_at : str
        ISO 8601 timestamp representing the run time to write with each row.
    """
    raise NotImplementedError("Documentation-only stub")


def write_json(path: str, rows: List[Dict], checked_at: str) -> None:
    """Write results to a JSON file (UTF-8 text).

    Parameters
    ----------
    path : str
        Target JSON file path.
    rows : List[dict]
        Rows to write.
    checked_at : str
        ISO 8601 timestamp representing the run time.
    """
    raise NotImplementedError("Documentation-only stub")


def print_summary(rows: List[Dict]) -> None:
    """Render a summary table to the terminal (documentation-only).

    Parameters
    ----------
    rows : List[dict]
        Results to summarize.
    """
    raise NotImplementedError("Documentation-only stub")


__all__ = [
    "fetch",
    "check_urls",
    "read_urls",
    "write_csv",
    "write_json",
    "print_summary",
]
