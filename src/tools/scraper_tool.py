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

import requests
import time
from typing import Tuple, Optional, Dict
from datetime import datetime


class ScraperTool:
    """
    THE CRAWLER LIMB — Deterministic Web Fetching Tool
    ==================================================

    This class encapsulates all web scraping functionality.
    It's a TOOL because it has NO autonomous decision-making.

    TOOL CHARACTERISTICS:
    ---------------------
      • Executes fetch commands exactly as given
      • No strategy or planning — just mechanical execution
      • Deterministic: same input → same output (modulo network)
      • Returns raw data without interpretation

    WHY NOT AN AGENT:
    -----------------
    The scraper doesn't decide:
      - Which URLs to fetch
      - When to retry or give up
      - Whether content is relevant
      - What to do next

    It just fetches. Period.

    (In Phase 5, we'll introduce ScraperAgent which CAN make those decisions!)
    """

    # Default user-agent identifying our research organism
    DEFAULT_USER_AGENT = (
        "Mozilla/5.0 (compatible; ResearchBody/1.0; "
        "+https://github.com/yourusername/research-body) "
        "Educational research crawler"
    )

    def __init__(self, user_agent: Optional[str] = None, debug: bool = False):
        """
        Initialize the Scraper Tool.

        Args:
            user_agent: Custom user-agent string (uses default if None)
            debug: Enable detailed logging of fetch operations
        """
        self.user_agent = user_agent or self.DEFAULT_USER_AGENT
        self.debug = debug
        self._fetch_history = []  # Track all fetches for debugging

    def fetch_url(
        self,
        url: str,
        timeout: int = 30,
        headers: Optional[Dict[str, str]] = None
    ) -> Tuple[Optional[str], int, str, Dict]:
        """
        Fetch raw HTML content from a URL.

        This is the core TOOL FUNCTION — deterministic, no decision-making.
        It simply executes the fetch and returns the result.

        Args:
            url: The URL to fetch
            timeout: Request timeout in seconds
            headers: Optional custom headers (merged with defaults)

        Returns:
            Tuple of (html_content, status_code, error_message, metadata)
            - html_content: Raw HTML string, or None if fetch failed
            - status_code: HTTP status code (200, 404, 500, etc.), 0 if network error
            - error_message: Empty string on success, error details on failure
            - metadata: Dict with response_time, content_length, final_url, etc.

        Example:
            >>> scraper = ScraperTool()
            >>> html, status, error, meta = scraper.fetch_url("https://example.com")
            >>> if status == 200:
            >>>     print(f"Fetched {len(html)} characters in {meta['response_time']:.2f}s")
            >>> else:
            >>>     print(f"Failed: {error}")

        TEACHING NOTE:
        --------------
        Compare this to PlannerAgent.create_plan():
          - PlannerAgent makes decisions about WHAT to fetch
          - ScraperTool just executes the fetch mechanically
        This is the key difference between AGENT and TOOL.
        """
        start_time = time.time()
        metadata = {
            'url': url,
            'timestamp': datetime.now(),
            'response_time': 0.0,
            'content_length': 0,
            'final_url': url,  # May differ if redirected
            'headers': {}
        }

        # Prepare headers with user-agent
        request_headers = {'User-Agent': self.user_agent}
        if headers:
            request_headers.update(headers)

        if self.debug:
            print(f"\n[SCRAPER TOOL] Fetching: {url}")
            print(f"[SCRAPER TOOL] User-Agent: {self.user_agent}")
            print(f"[SCRAPER TOOL] Timeout: {timeout}s")

        try:
            # Execute the HTTP GET request
            # TEACHING NOTE: This is the actual "limb reaching out" to the web
            response = requests.get(
                url,
                headers=request_headers,
                timeout=timeout,
                allow_redirects=True
            )

            # Calculate response time
            response_time = time.time() - start_time
            metadata['response_time'] = response_time
            metadata['final_url'] = response.url
            metadata['headers'] = dict(response.headers)
            metadata['content_length'] = len(response.content)

            # Check for HTTP errors (4xx, 5xx)
            if response.status_code >= 400:
                error_msg = f"HTTP {response.status_code}: {response.reason}"
                if self.debug:
                    print(f"[SCRAPER TOOL] ❌ Failed: {error_msg}")

                self._record_fetch(url, response.status_code, error_msg, metadata)
                return (None, response.status_code, error_msg, metadata)

            # Success!
            html_content = response.text
            if self.debug:
                print(f"[SCRAPER TOOL] ✓ Success: {len(html_content)} chars in {response_time:.2f}s")

            self._record_fetch(url, response.status_code, "", metadata)
            return (html_content, response.status_code, "", metadata)

        except requests.exceptions.Timeout:
            error_msg = f"Request timeout after {timeout}s"
            if self.debug:
                print(f"[SCRAPER TOOL] ❌ Timeout: {url}")

            metadata['response_time'] = time.time() - start_time
            self._record_fetch(url, 0, error_msg, metadata)
            return (None, 0, error_msg, metadata)

        except requests.exceptions.ConnectionError as e:
            error_msg = f"Connection error: {str(e)[:100]}"
            if self.debug:
                print(f"[SCRAPER TOOL] ❌ Connection error: {url}")

            metadata['response_time'] = time.time() - start_time
            self._record_fetch(url, 0, error_msg, metadata)
            return (None, 0, error_msg, metadata)

        except requests.exceptions.TooManyRedirects:
            error_msg = "Too many redirects"
            if self.debug:
                print(f"[SCRAPER TOOL] ❌ Too many redirects: {url}")

            metadata['response_time'] = time.time() - start_time
            self._record_fetch(url, 0, error_msg, metadata)
            return (None, 0, error_msg, metadata)

        except requests.exceptions.RequestException as e:
            error_msg = f"Request error: {str(e)[:100]}"
            if self.debug:
                print(f"[SCRAPER TOOL] ❌ Request error: {url}")
                print(f"[SCRAPER TOOL]    {error_msg}")

            metadata['response_time'] = time.time() - start_time
            self._record_fetch(url, 0, error_msg, metadata)
            return (None, 0, error_msg, metadata)

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)[:100]}"
            if self.debug:
                print(f"[SCRAPER TOOL] ❌ Unexpected error: {url}")
                print(f"[SCRAPER TOOL]    {error_msg}")

            metadata['response_time'] = time.time() - start_time
            self._record_fetch(url, 0, error_msg, metadata)
            return (None, 0, error_msg, metadata)

    def _record_fetch(self, url: str, status_code: int, error: str, metadata: Dict):
        """
        Record fetch attempt in history for debugging.

        DEBUGGING HELPER: Useful for analyzing scraper behavior.
        """
        self._fetch_history.append({
            'url': url,
            'status_code': status_code,
            'error': error,
            'metadata': metadata,
            'timestamp': datetime.now()
        })

    def get_fetch_stats(self) -> Dict:
        """
        Get statistics about fetch history.

        DEBUGGING HELPER: Analyze scraper performance and reliability.

        Returns:
            Dict with success_rate, avg_response_time, total_fetches, etc.
        """
        if not self._fetch_history:
            return {
                'total_fetches': 0,
                'success_rate': 0.0,
                'avg_response_time': 0.0
            }

        total = len(self._fetch_history)
        successes = sum(1 for f in self._fetch_history if f['status_code'] == 200)
        response_times = [f['metadata']['response_time'] for f in self._fetch_history]

        return {
            'total_fetches': total,
            'successes': successes,
            'failures': total - successes,
            'success_rate': successes / total if total > 0 else 0.0,
            'avg_response_time': sum(response_times) / len(response_times) if response_times else 0.0,
            'min_response_time': min(response_times) if response_times else 0.0,
            'max_response_time': max(response_times) if response_times else 0.0
        }

    def clear_history(self):
        """Clear fetch history (useful for testing or memory management)."""
        self._fetch_history = []


# Convenience function for simple one-off fetches
def fetch_url(url: str, timeout: int = 30) -> Tuple[Optional[str], int, str]:
    """
    Simple convenience function for one-off URL fetches.

    This wraps the ScraperTool class for backwards compatibility
    and simple use cases where you don't need the full tool interface.

    Args:
        url: The URL to fetch
        timeout: Request timeout in seconds

    Returns:
        Tuple of (html_content, status_code, error_message)

    Example:
        >>> html, status, error = fetch_url("https://example.com")
        >>> if status == 200:
        >>>     print(f"Fetched {len(html)} characters")

    TEACHING NOTE:
    --------------
    This function creates a new ScraperTool instance for each call.
    For repeated fetches, use ScraperTool directly to track history.
    """
    scraper = ScraperTool()
    html, status, error, metadata = scraper.fetch_url(url, timeout)
    return (html, status, error)
