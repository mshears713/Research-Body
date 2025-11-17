"""
ASYNC PROCESSING UTILITIES — When to Use Async
===============================================

TEACHING PURPOSE:
-----------------
This module demonstrates WHEN and WHEN NOT to use async/await.

KEY TEACHING POINTS:
--------------------
1. Async is GREAT for I/O-bound operations (network, disk, database)
2. Async is NOT helpful for CPU-bound operations (parsing, computation)
3. Async can coordinate I/O-bound and CPU-bound work together

ASYNC BENEFITS BY OPERATION TYPE:
----------------------------------
╔═══════════════════════╤═══════════╤═══════════════════════════╗
║ OPERATION             │ ASYNC?    │ REASON                    ║
╠═══════════════════════╪═══════════╪═══════════════════════════╣
║ HTTP requests         │ ✅ YES    │ I/O-bound, much waiting   ║
║ Database queries      │ ✅ YES    │ I/O-bound, network wait   ║
║ File reading          │ ✅ YES    │ I/O-bound, disk wait      ║
║ HTML parsing          │ ❌ NO     │ CPU-bound, no waiting     ║
║ Text processing       │ ❌ NO     │ CPU-bound, pure compute   ║
║ Math calculations     │ ❌ NO     │ CPU-bound, pure compute   ║
║ API calls (external)  │ ✅ YES    │ I/O-bound, network wait   ║
╚═══════════════════════╧═══════════╧═══════════════════════════╝

TEACHING NOTE:
--------------
Don't use async just because it seems "modern" or "fast".
Use it when you have I/O-bound operations that can run concurrently.

If your code is CPU-bound, async won't help and may make it slower
due to context-switching overhead.
"""

import asyncio
from typing import List, Dict
from ..tools.cleaner_tool import CleanerTool
from ..agents.summarizer_agent import SummarizerAgent


class AsyncCleanerWrapper:
    """
    TEACHING EXAMPLE: Async wrapper for CPU-bound cleaning.

    ⚠️  WARNING: This is for TEACHING purposes only!
    ⚠️  Cleaning is CPU-bound, so async doesn't help performance.

    WHEN WOULD THIS BE USEFUL:
    ---------------------------
    If you need to clean HTML while waiting for other async operations:
      async with aiohttp.ClientSession() as session:
          html = await session.get(url)  # I/O-bound (async helps!)
          clean = await async_cleaner.clean_html(html)  # CPU-bound (async doesn't help)
          summary = await async_summarizer.summarize(clean)  # Could be I/O if external API

    The async wrapper allows coordination, but doesn't speed up cleaning itself.

    TEACHING NOTE:
    --------------
    This demonstrates that you can wrap synchronous code in async
    for coordination, but it won't make CPU-bound code faster.

    For true parallelism of CPU-bound work, use multiprocessing or threading,
    not async/await.
    """

    def __init__(self, debug: bool = False):
        self.cleaner = CleanerTool(debug=debug)

    async def clean_html(self, html: str, url: str = "") -> Dict:
        """
        Async wrapper for HTML cleaning.

        TEACHING NOTE:
        --------------
        This runs the synchronous cleaning in an executor to avoid
        blocking the event loop. But it doesn't make cleaning faster!

        For CPU-bound work, consider:
          • multiprocessing for true parallelism
          • Optimizing the algorithm itself
          • Using compiled extensions (Cython, Rust)

        Don't expect async to magically speed up CPU-bound code.
        """
        loop = asyncio.get_event_loop()
        # Run in executor to avoid blocking event loop
        result = await loop.run_in_executor(
            None,
            self.cleaner.clean_html,
            html,
            url
        )
        return result

    async def clean_many(self, html_list: List[tuple]) -> List[Dict]:
        """
        Clean multiple HTML documents concurrently.

        Args:
            html_list: List of (html, url) tuples

        TEACHING NOTE:
        --------------
        This runs cleaning "concurrently" but not truly in parallel.
        Python's GIL (Global Interpreter Lock) means only one Python
        operation runs at a time.

        For true parallel cleaning of multiple documents, use:
          multiprocessing.Pool.map(cleaner.clean_html, html_list)

        Async/await is about CONCURRENCY (managing multiple tasks),
        not PARALLELISM (simultaneous execution).
        """
        tasks = [self.clean_html(html, url) for html, url in html_list]
        results = await asyncio.gather(*tasks)
        return results


class AsyncSummarizerWrapper:
    """
    Async wrapper for Summarizer Agent.

    WHEN THIS IS USEFUL:
    --------------------
    If SummarizerAgent called an external API (OpenAI, Anthropic, etc.),
    async would provide significant speedup for batch summarization:

      # Sequential: 10 summaries * 2s each = 20s
      for text in texts:
          summary = summarizer.summarize(text)

      # Concurrent: 10 summaries in parallel = ~2s
      summaries = await async_summarizer.summarize_many(texts)

    Currently, our summarizer is rule-based (CPU-bound), so async
    doesn't help much. But this shows the pattern for future API integration.

    TEACHING NOTE:
    --------------
    When you integrate with external APIs, async becomes VERY valuable.
    LLM API calls are I/O-bound and benefit greatly from concurrency.
    """

    def __init__(self, debug: bool = False):
        self.summarizer = SummarizerAgent(debug=debug)

    async def summarize(
        self,
        text: str,
        topic: str = "",
        style: str = "technical"
    ) -> Dict:
        """
        Async wrapper for summarization.

        FUTURE ENHANCEMENT:
        -------------------
        Replace with actual async API call:
          async with aiohttp.ClientSession() as session:
              response = await session.post(
                  "https://api.openai.com/v1/chat/completions",
                  json={"model": "gpt-4", "messages": [...]},
                  headers={"Authorization": f"Bearer {api_key}"}
              )
              summary = await response.json()

        Then async would provide real performance benefits!
        """
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            self.summarizer.summarize,
            text,
            topic,
            style
        )
        return result

    async def summarize_many(
        self,
        texts: List[str],
        topic: str = "",
        style: str = "technical"
    ) -> List[Dict]:
        """
        Summarize multiple texts concurrently.

        TEACHING EXAMPLE:
        -----------------
        If summarizer called an external API, this would be VERY fast:

        10 API calls at 2s each:
          • Sequential: 20 seconds
          • Concurrent (this method): ~2 seconds

        That's a 10x speedup!

        Currently (rule-based summarizer):
          • Sequential: 0.1s
          • Concurrent: 0.1s (no benefit, GIL-limited)

        Async shines when you have I/O wait time to exploit.
        """
        tasks = [self.summarize(text, topic, style) for text in texts]
        results = await asyncio.gather(*tasks)
        return results


# TEACHING EXAMPLE: Demonstrate when async helps vs doesn't
if __name__ == "__main__":
    import time

    async def demo():
        print("""
        ═══════════════════════════════════════════════════════════
        TEACHING: When Does Async Help?
        ═══════════════════════════════════════════════════════════

        This demo shows the difference between:
          1. I/O-bound operations (async helps!)
          2. CPU-bound operations (async doesn't help)
        """)

        # Simulate I/O-bound operation
        async def io_bound_task(n):
            """Simulates network request or disk I/O"""
            await asyncio.sleep(0.1)  # Simulates waiting for I/O
            return n * 2

        # CPU-bound operation
        def cpu_bound_task(n):
            """Simulates parsing or computation"""
            result = 0
            for i in range(1000000):  # Simulates heavy computation
                result += i
            return n * 2

        print("\n1️⃣  I/O-BOUND: Async provides speedup")
        print("─" * 60)

        start = time.time()
        # Concurrent I/O
        results = await asyncio.gather(*[io_bound_task(i) for i in range(10)])
        io_concurrent_time = time.time() - start

        print(f"   10 I/O tasks concurrently: {io_concurrent_time:.3f}s")
        print(f"   Sequential would take: ~1.0s")
        print(f"   ✓ Speedup: ~{1.0 / io_concurrent_time:.1f}x\n")

        print("2️⃣  CPU-BOUND: Async provides NO speedup")
        print("─" * 60)

        start = time.time()
        # "Concurrent" CPU (but GIL limits to sequential)
        results = await asyncio.gather(*[
            asyncio.get_event_loop().run_in_executor(None, cpu_bound_task, i)
            for i in range(10)
        ])
        cpu_concurrent_time = time.time() - start

        print(f"   10 CPU tasks 'concurrently': {cpu_concurrent_time:.3f}s")
        print(f"   ⚠️  No speedup due to GIL (Global Interpreter Lock)")
        print(f"   For CPU parallelism, use multiprocessing instead!\n")

        print("=" * 60)
        print("KEY TAKEAWAY:")
        print("  • Async = Great for I/O-bound (network, disk, database)")
        print("  • Async ≠ Helpful for CPU-bound (parsing, computation)")
        print("=" * 60 + "\n")

    asyncio.run(demo())
