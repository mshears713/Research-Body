"""
THE CRAWLER LIMB — SCRAPER TOOL
================================

ORGAN METAPHOR:
---------------
The Scraper is a LIMB of the research organism.
It reaches out to fetch web pages exactly as instructed.

ASCII DIAGRAM:
--------------
                     ┌─────────────────────┐
                     │   MISSION PLAN      │
                     │   Task: Fetch URL   │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │   SCRAPER TOOL      │
                     │      (LIMB)         │
                     │  [DETERMINISTIC]    │
                     └──────────┬──────────┘
                                │
                                ▼
                        ╔═══════════════╗
                        ║   INTERNET    ║
                        ║   🌐 → HTML   ║
                        ╚═══════════════╝
                                │
                                ▼
                     ┌─────────────────────┐
                     │   RAW HTML OUTPUT   │
                     │   <html>...</html>  │
                     └─────────────────────┘

AGENT vs TOOL:
--------------
This is a TOOL because it:
  • Performs deterministic fetching operations
  • Does not decide WHAT to fetch, only HOW to fetch it
  • Has no autonomous decision-making capability
  • Simply executes the fetch command and returns raw HTML

RESPONSIBILITIES:
-----------------
  1. Fetch raw HTML from a given URL
  2. Handle HTTP headers (user-agent, timeouts)
  3. Return raw page content or error status
  4. Log fetch metadata (status code, response time)

TEACHING NOTES:
---------------
The Scraper TOOL is purely mechanical. It's like a robotic arm — it does
exactly what it's told, with no judgment or planning. Compare this to
the Planner AGENT, which decides what to fetch in the first place.

In Phase 5, we'll introduce a SCRAPER AGENT that can autonomously decide
to retry, crawl linked pages, or choose alternate sources. This upgrade
demonstrates the transition from TOOL → AGENT.

FUTURE EXTENSIONS:
------------------
  • Async fetching for concurrent requests
  • Retry logic with exponential backoff
  • Caching to avoid redundant fetches
  • robots.txt compliance checking

DEBUGGING TIPS:
---------------
  • Log all fetch attempts with timestamps
  • Monitor for rate limiting or blocked requests
  • Track success/failure rates by domain
"""

from typing import Tuple, Optional


def fetch_url(url: str, timeout: int = 30) -> Tuple[Optional[str], int, str]:
    """
    Fetch raw HTML content from a URL.

    This is a TOOL FUNCTION — deterministic, no decision-making.
    It simply executes the fetch and returns the result.

    Args:
        url: The URL to fetch
        timeout: Request timeout in seconds

    Returns:
        Tuple of (html_content, status_code, error_message)
        - html_content: Raw HTML string, or None if fetch failed
        - status_code: HTTP status code (200, 404, 500, etc.)
        - error_message: Empty string on success, error details on failure

    Example:
        >>> html, status, error = fetch_url("https://example.com")
        >>> if status == 200:
        >>>     print(f"Fetched {len(html)} characters")
        >>> else:
        >>>     print(f"Failed: {error}")

    TEACHING NOTE:
    --------------
    This is a stub implementation. In Phase 2, we'll add:
      • Actual HTTP request using requests library
      • User-agent headers to identify our scraper
      • Error handling for network failures
      • Response time tracking
    """
    # STUB: Return placeholder data
    # In Phase 2, this will be replaced with actual HTTP requests

    print(f"[SCRAPER TOOL] Fetching URL: {url}")

    # Placeholder return — simulates a successful fetch
    placeholder_html = f"""
    <html>
        <head><title>Placeholder Content</title></head>
        <body>
            <h1>This is stub content for: {url}</h1>
            <p>In Phase 2, this will be real HTML fetched from the web.</p>
        </body>
    </html>
    """

    return (placeholder_html, 200, "")


# FUTURE: Add these functions in Phase 2
# def fetch_with_retry(url: str, max_retries: int = 3) -> ...:
#     """Fetch with exponential backoff retry logic"""
#     pass
#
# def check_robots_txt(url: str) -> bool:
#     """Check if URL is allowed by robots.txt"""
#     pass
