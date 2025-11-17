"""
ASYNC SCRAPER TOOL — Concurrent Web Fetching
=============================================

TEACHING PURPOSE:
-----------------
This module demonstrates ASYNC PROGRAMMING for I/O-bound operations.
Compare this file to scraper_tool.py to understand when and why
to use async/await for performance improvements.

WHY ASYNC FOR WEB SCRAPING:
---------------------------
Web scraping is I/O-bound — most time is spent WAITING for:
  • DNS resolution
  • TCP connection establishment
  • HTTP response transmission

Synchronous approach:
  Fetch URL 1 → wait 2s → Fetch URL 2 → wait 2s → Total: 4s

Async approach:
  Fetch URL 1 + Fetch URL 2 concurrently → wait 2s → Total: 2s

For N URLs, async can provide ~N times speedup!

ASCII DIAGRAM:
--------------
SYNCHRONOUS (scraper_tool.py):
  ▼──[Fetch 1]──▶ wait... ──▶ done
                              ▼──[Fetch 2]──▶ wait... ──▶ done
                                                          ▼──[Fetch 3]──▶ wait... ──▶ done
  Total time: ~6 seconds

ASYNCHRONOUS (this file):
  ▼──[Fetch 1]──▶ wait... ──▶ done ──▶┐
  ▼──[Fetch 2]──▶ wait... ──▶ done ──▶┼──▶ All results!
  ▼──[Fetch 3]──▶ wait... ──▶ done ──▶┘
  Total time: ~2 seconds (concurrent!)

KEY CONCEPTS:
-------------
  • async/await: Language-level concurrency support
  • asyncio: Python's async runtime
  • aiohttp: Async HTTP client library
  • Coroutines: Functions that can be suspended and resumed
  • Event loop: Manages concurrent coroutine execution

WHEN TO USE ASYNC:
------------------
✅ USE ASYNC when:
  • Fetching multiple URLs concurrently
  • I/O-bound operations dominate
  • Need to handle many simultaneous connections

❌ DON'T USE ASYNC when:
  • Only fetching 1-2 URLs
  • CPU-bound operations dominate
  • Simpler synchronous code is sufficient
  • Team unfamiliar with async patterns

TEACHING NOTE:
--------------
This demonstrates the TOOL pattern with async/await.
Even async code can be a deterministic TOOL if it has
no decision-making logic. Async doesn't make it an AGENT!

FUTURE EXTENSIONS:
------------------
  • Connection pooling for efficiency
  • Rate limiting across concurrent requests
  • Progress tracking for large batch fetches
  • Timeout per-URL and per-batch

DEBUGGING TIPS:
---------------
  • Use asyncio.run() to run async code from sync context
  • Monitor with asyncio.create_task() for task tracking
  • Be careful with shared state in concurrent code
  • Use asyncio.gather() for batch operations
"""

import asyncio
import aiohttp
import time
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class AsyncScraperTool:
    """
    ASYNC CRAWLER LIMB — Concurrent Web Fetching Tool
    ==================================================

    This is the async version of ScraperTool.
    It remains a TOOL (deterministic, no decisions),
    but uses async/await for concurrent operations.

    PERFORMANCE COMPARISON:
    -----------------------
    For 10 URLs with 2s response time each:
      • ScraperTool (sync):  ~20 seconds (sequential)
      • AsyncScraperTool:    ~2 seconds (concurrent)

    10x speedup for I/O-bound operations!

    TEACHING NOTE:
    --------------
    Compare the method signatures:
      ScraperTool.fetch_url()       → returns result directly
      AsyncScraperTool.fetch_url()  → returns awaitable coroutine

    Using async requires:
      result = await async_scraper.fetch_url(url)
    """

    DEFAULT_USER_AGENT = (
        "Mozilla/5.0 (compatible; ResearchBody/1.0; "
        "+https://github.com/yourusername/research-body) "
        "Educational research crawler (async)"
    )

    def __init__(self, user_agent: Optional[str] = None, debug: bool = False):
        """
        Initialize the Async Scraper Tool.

        Args:
            user_agent: Custom user-agent string
            debug: Enable detailed logging

        TEACHING NOTE:
        --------------
        AsyncScraperTool doesn't create a persistent aiohttp session
        in __init__ because sessions are async context managers.
        Instead, we create sessions in the async methods.
        """
        self.user_agent = user_agent or self.DEFAULT_USER_AGENT
        self.debug = debug
        self._fetch_history = []

    async def fetch_url(
        self,
        url: str,
        timeout: int = 30,
        headers: Optional[Dict[str, str]] = None
    ) -> Tuple[Optional[str], int, str, Dict]:
        """
        Asynchronously fetch raw HTML content from a URL.

        This is an ASYNC COROUTINE — it returns immediately and
        executes concurrently with other coroutines.

        Args:
            url: The URL to fetch
            timeout: Request timeout in seconds
            headers: Optional custom headers

        Returns:
            Tuple of (html_content, status_code, error_message, metadata)

        Example:
            >>> scraper = AsyncScraperTool()
            >>> html, status, error, meta = await scraper.fetch_url("https://example.com")

        TEACHING NOTE:
        --------------
        The 'async' keyword makes this a coroutine function.
        The 'await' keyword is used for async operations (HTTP request).

        This method can be suspended while waiting for network I/O,
        allowing other coroutines to execute in the meantime.
        """
        start_time = time.time()
        metadata = {
            'url': url,
            'timestamp': datetime.now(),
            'response_time': 0.0,
            'content_length': 0,
            'final_url': url,
            'headers': {}
        }

        # Prepare headers
        request_headers = {'User-Agent': self.user_agent}
        if headers:
            request_headers.update(headers)

        if self.debug:
            print(f"\n[ASYNC SCRAPER] Fetching: {url}")

        try:
            # ASYNC I/O: Create session and fetch
            # TEACHING NOTE: aiohttp.ClientSession is the async equivalent
            # of requests.Session. It must be used as async context manager.
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    headers=request_headers,
                    timeout=aiohttp.ClientTimeout(total=timeout),
                    allow_redirects=True
                ) as response:
                    # Calculate response time
                    response_time = time.time() - start_time
                    metadata['response_time'] = response_time
                    metadata['final_url'] = str(response.url)
                    metadata['headers'] = dict(response.headers)

                    # Read response body asynchronously
                    # TEACHING NOTE: response.text() is async, so we await it
                    html_content = await response.text()
                    metadata['content_length'] = len(html_content)

                    # Check for HTTP errors
                    if response.status >= 400:
                        error_msg = f"HTTP {response.status}: {response.reason}"
                        if self.debug:
                            print(f"[ASYNC SCRAPER] ❌ Failed: {error_msg}")

                        self._record_fetch(url, response.status, error_msg, metadata)
                        return (None, response.status, error_msg, metadata)

                    # Success!
                    if self.debug:
                        print(f"[ASYNC SCRAPER] ✓ Success: {len(html_content)} chars in {response_time:.2f}s")

                    self._record_fetch(url, response.status, "", metadata)
                    return (html_content, response.status, "", metadata)

        except asyncio.TimeoutError:
            error_msg = f"Request timeout after {timeout}s"
            if self.debug:
                print(f"[ASYNC SCRAPER] ❌ Timeout: {url}")

            metadata['response_time'] = time.time() - start_time
            self._record_fetch(url, 0, error_msg, metadata)
            return (None, 0, error_msg, metadata)

        except aiohttp.ClientError as e:
            error_msg = f"Client error: {str(e)[:100]}"
            if self.debug:
                print(f"[ASYNC SCRAPER] ❌ Client error: {url}")

            metadata['response_time'] = time.time() - start_time
            self._record_fetch(url, 0, error_msg, metadata)
            return (None, 0, error_msg, metadata)

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)[:100]}"
            if self.debug:
                print(f"[ASYNC SCRAPER] ❌ Unexpected error: {url}")
                print(f"[ASYNC SCRAPER]    {error_msg}")

            metadata['response_time'] = time.time() - start_time
            self._record_fetch(url, 0, error_msg, metadata)
            return (None, 0, error_msg, metadata)

    async def fetch_many(
        self,
        urls: List[str],
        timeout: int = 30
    ) -> List[Tuple[str, Optional[str], int, str, Dict]]:
        """
        Fetch multiple URLs concurrently — THE MAIN ASYNC ADVANTAGE!

        This demonstrates the real power of async: fetching many URLs
        simultaneously instead of one-by-one.

        Args:
            urls: List of URLs to fetch
            timeout: Timeout per URL (in seconds)

        Returns:
            List of (url, html_content, status_code, error, metadata) tuples

        Example:
            >>> scraper = AsyncScraperTool(debug=True)
            >>> urls = ["https://example.com", "https://python.org"]
            >>> results = await scraper.fetch_many(urls)
            >>> for url, html, status, error, meta in results:
            >>>     if html:
            >>>         print(f"{url}: {len(html)} chars")

        TEACHING NOTE:
        --------------
        This is the "killer feature" of async for web scraping.

        Sequential approach (ScraperTool):
          for url in urls:
              fetch(url)  # Wait for each
          # Total time: N * avg_response_time

        Concurrent approach (AsyncScraperTool):
          results = await asyncio.gather(*[fetch(url) for url in urls])
          # Total time: max(response_times)

        For 100 URLs with 1s average response:
          • Sequential: ~100 seconds
          • Concurrent: ~1-2 seconds (depending on max response time)

        asyncio.gather() runs all coroutines concurrently and waits
        for all to complete, returning results in original order.
        """
        if self.debug:
            print(f"\n{'='*60}")
            print(f"ASYNC SCRAPER: Fetching {len(urls)} URLs concurrently")
            print(f"{'='*60}")

        start_time = time.time()

        # Create coroutines for all URLs
        # TEACHING NOTE: This doesn't start fetching yet, just creates tasks
        fetch_tasks = [self.fetch_url(url, timeout) for url in urls]

        # Execute all concurrently and wait for all to complete
        # TEACHING NOTE: asyncio.gather() is the key to concurrent execution
        fetch_results = await asyncio.gather(*fetch_tasks, return_exceptions=True)

        total_time = time.time() - start_time

        # Process results
        results = []
        for url, result in zip(urls, fetch_results):
            if isinstance(result, Exception):
                # Handle exceptions from individual fetches
                results.append((url, None, 0, str(result), {}))
            else:
                html, status, error, metadata = result
                results.append((url, html, status, error, metadata))

        if self.debug:
            successful = sum(1 for _, html, _, _, _ in results if html)
            print(f"\n{'='*60}")
            print(f"ASYNC SCRAPER COMPLETE:")
            print(f"  Total URLs: {len(urls)}")
            print(f"  Successful: {successful}")
            print(f"  Failed: {len(urls) - successful}")
            print(f"  Total time: {total_time:.2f}s")
            print(f"  Avg time/URL: {total_time/len(urls):.2f}s")
            print(f"  Speedup vs sequential: ~{len(urls) * (total_time/len(urls)) / total_time:.1f}x")
            print(f"{'='*60}\n")

        return results

    def _record_fetch(self, url: str, status_code: int, error: str, metadata: Dict):
        """Record fetch attempt in history (not async)."""
        self._fetch_history.append({
            'url': url,
            'status_code': status_code,
            'error': error,
            'metadata': metadata,
            'timestamp': datetime.now()
        })

    def get_fetch_stats(self) -> Dict:
        """Get statistics about fetch history (not async)."""
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


# Convenience function for async batch fetching
async def fetch_many(urls: List[str], timeout: int = 30, debug: bool = False) -> List[Tuple[str, Optional[str], int, str]]:
    """
    Convenience function for concurrent URL fetching.

    Args:
        urls: List of URLs to fetch
        timeout: Timeout per URL
        debug: Enable debug output

    Returns:
        List of (url, html_content, status_code, error) tuples

    Example:
        >>> urls = ["https://example.com", "https://python.org"]
        >>> results = await fetch_many(urls, debug=True)
        >>> for url, html, status, error in results:
        >>>     if html:
        >>>         print(f"Fetched {url}: {len(html)} chars")

    TEACHING NOTE:
    --------------
    This wraps AsyncScraperTool for simple use cases.
    For complex scenarios, use AsyncScraperTool directly.
    """
    scraper = AsyncScraperTool(debug=debug)
    results = await scraper.fetch_many(urls, timeout)
    # Convert to simpler format (remove metadata)
    return [(url, html, status, error) for url, html, status, error, _ in results]


# TEACHING EXAMPLE: Compare sync vs async performance
if __name__ == "__main__":
    async def demo():
        print("""
        ═══════════════════════════════════════════════════════════
        DEMONSTRATION: SYNC vs ASYNC PERFORMANCE
        ═══════════════════════════════════════════════════════════
        """)

        # Test URLs (using httpbin for controlled delays)
        test_urls = [
            "https://httpbin.org/delay/1",  # Each takes ~1 second
            "https://httpbin.org/delay/1",
            "https://httpbin.org/delay/1",
        ]

        print(f"\n📊 Fetching {len(test_urls)} URLs (each with 1s delay)")
        print(f"   Sequential would take: ~{len(test_urls)} seconds")
        print(f"   Concurrent should take: ~1 second\n")

        scraper = AsyncScraperTool(debug=True)

        start = time.time()
        results = await scraper.fetch_many(test_urls, timeout=10)
        elapsed = time.time() - start

        print(f"\n✓ Completed in {elapsed:.2f} seconds")
        print(f"  Speedup: ~{len(test_urls) / elapsed:.1f}x faster than sequential!")

        print("\n" + "=" * 60)
        print("This is why async matters for I/O-bound operations!")
        print("=" * 60 + "\n")

    # Run the async demo
    asyncio.run(demo())
