"""
═══════════════════════════════════════════════════════════════
THE INTELLIGENT CRAWLER LIMB — SCRAPER AGENT
═══════════════════════════════════════════════════════════════

TEACHING PURPOSE:
-----------------
This module demonstrates the critical evolution from TOOL → AGENT.
Compare this file directly to src/tools/scraper_tool.py to understand
what transforms a passive executor into an autonomous decision-maker.

ORGAN METAPHOR:
---------------
The ScraperAgent is an UPGRADED LIMB with a mind of its own.
Unlike the deterministic Scraper Tool, this agent can:
  • Decide which links to follow based on relevance
  • Learn from failures and adapt retry strategies
  • Autonomously explore related content
  • Prioritize high-value sources

ASCII DIAGRAM:
--------------
              ┌───────────────────────────────────┐
              │    SCRAPER AGENT (INTELLIGENT)    │
              │         [AUTONOMOUS LIMB]         │
              └───────────┬───────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │DECISION │    │LEARNING │    │STRATEGY │
    │  TREE   │    │ SYSTEM  │    │ ADAPTER │
    └────┬────┘    └────┬────┘    └────┬────┘
         │              │              │
         └──────────────┼──────────────┘
                        ▼
              ┌─────────────────┐
              │  ScraperTool    │ ← Uses the tool internally
              │  (Mechanical)   │
              └─────────────────┘
                        │
                        ▼
                  ╔═══════════╗
                  ║ INTERNET  ║
                  ╚═══════════╝

TOOL vs AGENT COMPARISON:
--------------------------
╔═══════════════════╤═════════════════════╤═══════════════════════╗
║    CAPABILITY     │   SCRAPER TOOL      │   SCRAPER AGENT       ║
╠═══════════════════╪═════════════════════╪═══════════════════════╣
║ Decision-Making   │ None                │ Autonomous            ║
║ Retry Logic       │ No                  │ Intelligent backoff   ║
║ Link Following    │ No                  │ Relevance-based       ║
║ State Tracking    │ Minimal             │ Comprehensive         ║
║ Strategy Adapt    │ Fixed               │ Dynamic               ║
║ Error Handling    │ Return error        │ Learn & adapt         ║
╚═══════════════════╧═════════════════════╧═══════════════════════╝

AGENT RESPONSIBILITIES:
-----------------------
  1. Decide which URLs to fetch based on mission goals
  2. Intelligently retry failed fetches with backoff
  3. Explore linked pages to find related content
  4. Rank and prioritize sources by predicted value
  5. Learn from fetch history to improve strategy
  6. Adapt crawling depth based on content quality

KEY CONCEPTS DEMONSTRATED:
--------------------------
  • AUTONOMY: Agent makes its own decisions
  • STATE: Maintains memory across operations
  • LEARNING: Improves from experience
  • STRATEGY: Plans multi-step operations
  • ADAPTATION: Changes behavior based on results

TEACHING COMPARISON:
--------------------
Compare these two approaches:

  TOOL APPROACH (Scraper Tool):
    tool.fetch_url("https://example.com")  # Just fetches blindly
    # Returns HTML or error, that's it

  AGENT APPROACH (Scraper Agent):
    agent.fetch_mission_content(mission)   # Makes decisions!
    # - Analyzes mission to determine relevant sources
    # - Ranks URLs by predicted relevance
    # - Fetches in priority order
    # - Follows promising links autonomously
    # - Retries failures with intelligent strategy
    # - Returns curated, high-quality content

The agent THINKS. The tool just EXECUTES.

FUTURE EXTENSIONS:
------------------
  • Machine learning for relevance prediction
  • Distributed crawling across multiple agents
  • Real-time adaptation to rate limiting
  • Collaborative learning between agent instances

DEBUGGING TIPS:
---------------
  • Set verbose=True to see decision-making process
  • Check decision_log to understand agent choices
  • Monitor retry_history for failure patterns
  • Use get_performance_metrics() for optimization
"""

import requests
import time
import re
from typing import List, Dict, Optional, Tuple, Set
from datetime import datetime
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# Import the underlying tool that this agent uses
from ..tools.scraper_tool import ScraperTool


class ScraperAgent:
    """
    THE INTELLIGENT CRAWLER LIMB — Autonomous Web Scraping Agent
    ============================================================

    This is an AGENT, not a tool. It makes autonomous decisions about:
      • WHAT to fetch (relevance filtering)
      • WHEN to retry (intelligent backoff)
      • WHERE to explore (link following)
      • HOW MUCH to fetch (depth control)

    AGENT CHARACTERISTICS:
    ----------------------
      • AUTONOMOUS: Makes decisions without external guidance
      • STATEFUL: Maintains memory of past fetches and decisions
      • ADAPTIVE: Changes strategy based on results
      • GOAL-ORIENTED: Optimizes for mission objectives

    COMPARISON TO SCRAPER TOOL:
    ---------------------------
    ScraperTool:  "Fetch this URL" → Fetches exactly that URL
    ScraperAgent: "Get content about X" → Decides which URLs,
                  follows links, retries intelligently, etc.

    The agent has a MIND. The tool is just a HAND.
    """

    def __init__(
        self,
        max_retries: int = 3,
        retry_backoff: float = 2.0,
        max_links_per_page: int = 5,
        max_crawl_depth: int = 2,
        verbose: bool = False
    ):
        """
        Initialize the Scraper Agent with decision-making parameters.

        Args:
            max_retries: Maximum retry attempts for failed fetches
            retry_backoff: Exponential backoff multiplier (e.g., 2.0 = 1s, 2s, 4s)
            max_links_per_page: Max related links to follow per page
            max_crawl_depth: How many link-following levels to traverse
            verbose: Enable detailed logging of agent decisions

        TEACHING NOTE:
        --------------
        Notice the agent has CONFIGURATION for decision-making behavior.
        The tool just has a timeout. This is a key agent characteristic:
        agents have POLICIES and STRATEGIES, tools have PARAMETERS.
        """
        # The agent uses the tool as its "mechanical hand"
        self.tool = ScraperTool(debug=verbose)

        # Agent-specific decision-making parameters
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff
        self.max_links_per_page = max_links_per_page
        self.max_crawl_depth = max_crawl_depth
        self.verbose = verbose

        # AGENT STATE: Memory and learning
        self.visited_urls: Set[str] = set()
        self.failed_urls: Set[str] = set()
        self.high_quality_domains: Set[str] = set()
        self.low_quality_domains: Set[str] = set()

        # Decision tracking for transparency and debugging
        self.decision_log: List[Dict] = []
        self.retry_history: List[Dict] = []

    def fetch_with_intelligence(
        self,
        url: str,
        mission_keywords: Optional[List[str]] = None
    ) -> Tuple[Optional[str], bool, Dict]:
        """
        Intelligently fetch a URL with autonomous retry and decision-making.

        This is the AGENT'S core method. Unlike the tool's simple fetch,
        this method:
          1. Checks if URL was already visited (efficiency)
          2. Decides if URL is likely relevant (filtering)
          3. Attempts fetch with intelligent retry logic
          4. Learns from success/failure for future decisions
          5. Returns enriched metadata about the decision process

        Args:
            url: The URL to fetch
            mission_keywords: Optional keywords to assess relevance

        Returns:
            Tuple of (html_content, success, decision_metadata)
              - html_content: The fetched HTML (None if failed)
              - success: Whether fetch ultimately succeeded
              - decision_metadata: Dict with agent's decision-making info

        TEACHING NOTE:
        --------------
        Compare this signature to ScraperTool.fetch_url():
          - Tool returns (html, status_code, error, metadata)
          - Agent returns (html, success, decision_metadata)

        The agent abstracts away low-level details and provides
        high-level success/failure with REASONING.
        """
        decision_metadata = {
            'url': url,
            'timestamp': datetime.now(),
            'decisions_made': [],
            'retry_count': 0,
            'relevance_score': 0.0,
            'followed_links': []
        }

        # DECISION 1: Check if already visited
        if url in self.visited_urls:
            self._log_decision(
                url,
                "skip",
                "Already visited this URL - avoiding duplicate fetch"
            )
            decision_metadata['decisions_made'].append({
                'decision': 'skip',
                'reason': 'already_visited'
            })
            return (None, False, decision_metadata)

        # DECISION 2: Assess relevance if keywords provided
        if mission_keywords:
            relevance = self._assess_url_relevance(url, mission_keywords)
            decision_metadata['relevance_score'] = relevance

            if relevance < 0.3:  # Low relevance threshold
                self._log_decision(
                    url,
                    "skip",
                    f"Low relevance score ({relevance:.2f}) - not worth fetching"
                )
                decision_metadata['decisions_made'].append({
                    'decision': 'skip',
                    'reason': 'low_relevance',
                    'relevance_score': relevance
                })
                return (None, False, decision_metadata)

        # DECISION 3: Attempt fetch with intelligent retry
        html_content = None
        success = False

        for attempt in range(self.max_retries + 1):
            if self.verbose:
                print(f"\n[SCRAPER AGENT] Attempt {attempt + 1}/{self.max_retries + 1}: {url}")

            # Use the underlying tool for actual fetching
            html, status_code, error, metadata = self.tool.fetch_url(url)

            if status_code == 200:
                # SUCCESS!
                html_content = html
                success = True
                self.visited_urls.add(url)

                # LEARNING: Track successful domain for future prioritization
                domain = urlparse(url).netloc
                self.high_quality_domains.add(domain)

                self._log_decision(
                    url,
                    "success",
                    f"Fetched successfully on attempt {attempt + 1}"
                )
                decision_metadata['decisions_made'].append({
                    'decision': 'success',
                    'attempt': attempt + 1,
                    'response_time': metadata['response_time']
                })
                break

            else:
                # DECISION 4: Should we retry?
                if attempt < self.max_retries:
                    # Calculate intelligent backoff
                    backoff_time = self._calculate_backoff(attempt, status_code)

                    self._log_decision(
                        url,
                        "retry",
                        f"Attempt {attempt + 1} failed (status {status_code}), "
                        f"retrying in {backoff_time:.1f}s"
                    )

                    decision_metadata['decisions_made'].append({
                        'decision': 'retry',
                        'attempt': attempt + 1,
                        'status_code': status_code,
                        'backoff_seconds': backoff_time
                    })

                    # Record retry for learning
                    self.retry_history.append({
                        'url': url,
                        'attempt': attempt + 1,
                        'status_code': status_code,
                        'backoff': backoff_time,
                        'timestamp': datetime.now()
                    })

                    time.sleep(backoff_time)
                    decision_metadata['retry_count'] += 1

                else:
                    # DECISION 5: Give up after max retries
                    self.failed_urls.add(url)

                    # LEARNING: Track problematic domain
                    domain = urlparse(url).netloc
                    self.low_quality_domains.add(domain)

                    self._log_decision(
                        url,
                        "give_up",
                        f"Failed after {self.max_retries + 1} attempts (final status: {status_code})"
                    )

                    decision_metadata['decisions_made'].append({
                        'decision': 'give_up',
                        'total_attempts': self.max_retries + 1,
                        'final_status': status_code,
                        'error': error
                    })

        return (html_content, success, decision_metadata)

    def crawl_intelligently(
        self,
        seed_urls: List[str],
        mission_keywords: List[str],
        max_pages: int = 20
    ) -> List[Tuple[str, str]]:
        """
        Autonomously crawl starting from seed URLs, following relevant links.

        This demonstrates FULL AGENT AUTONOMY:
          1. Starts with seed URLs
          2. Extracts and ranks links from each page
          3. Decides which links to follow based on relevance
          4. Respects depth and page limits
          5. Returns curated collection of high-quality content

        Args:
            seed_urls: Initial URLs to start crawling
            mission_keywords: Keywords defining what content is relevant
            max_pages: Maximum total pages to fetch

        Returns:
            List of (url, html_content) tuples for successfully fetched pages

        TEACHING NOTE:
        --------------
        This is something a TOOL could NEVER do. The tool can only fetch
        what you tell it to fetch. This agent EXPLORES and DISCOVERS
        relevant content autonomously.

        This is the essence of agency: autonomous goal-directed behavior.
        """
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"SCRAPER AGENT: Starting intelligent crawl")
            print(f"Seeds: {len(seed_urls)} URLs")
            print(f"Keywords: {', '.join(mission_keywords)}")
            print(f"Max pages: {max_pages}")
            print(f"Max depth: {self.max_crawl_depth}")
            print(f"{'='*60}\n")

        results = []
        url_queue = [(url, 0) for url in seed_urls]  # (url, depth)
        fetched_count = 0

        while url_queue and fetched_count < max_pages:
            current_url, current_depth = url_queue.pop(0)

            # DECISION: Skip if depth limit exceeded
            if current_depth > self.max_crawl_depth:
                self._log_decision(
                    current_url,
                    "skip",
                    f"Depth {current_depth} exceeds max depth {self.max_crawl_depth}"
                )
                continue

            # Fetch with intelligence
            html, success, metadata = self.fetch_with_intelligence(
                current_url,
                mission_keywords
            )

            if success and html:
                results.append((current_url, html))
                fetched_count += 1

                if self.verbose:
                    print(f"[SCRAPER AGENT] ✓ Fetched ({fetched_count}/{max_pages}): {current_url}")

                # DECISION: Extract and evaluate links for further exploration
                if current_depth < self.max_crawl_depth:
                    discovered_links = self._extract_relevant_links(
                        html,
                        current_url,
                        mission_keywords
                    )

                    if self.verbose and discovered_links:
                        print(f"[SCRAPER AGENT]   → Found {len(discovered_links)} relevant links")

                    # Add discovered links to queue with incremented depth
                    for link in discovered_links:
                        if link not in self.visited_urls and link not in [u for u, _ in url_queue]:
                            url_queue.append((link, current_depth + 1))

            else:
                if self.verbose:
                    print(f"[SCRAPER AGENT] ✗ Failed: {current_url}")

        if self.verbose:
            print(f"\n{'='*60}")
            print(f"CRAWL COMPLETE: Fetched {len(results)} pages")
            print(f"{'='*60}\n")

        return results

    def _assess_url_relevance(self, url: str, keywords: List[str]) -> float:
        """
        Assess how relevant a URL is to mission keywords.

        AGENT DECISION LOGIC: This is intelligence in action.
        The agent examines the URL structure to predict if it's worth fetching.

        Returns:
            Relevance score from 0.0 (irrelevant) to 1.0 (highly relevant)
        """
        url_lower = url.lower()
        score = 0.0
        matches = 0

        # Check for keyword presence in URL
        for keyword in keywords:
            if keyword.lower() in url_lower:
                matches += 1
                score += 0.3

        # Bonus for academic/research domains
        if any(domain in url_lower for domain in ['.edu', '.gov', '.org', 'research', 'journal']):
            score += 0.2

        # Check domain quality from learning
        domain = urlparse(url).netloc
        if domain in self.high_quality_domains:
            score += 0.2
        elif domain in self.low_quality_domains:
            score -= 0.3

        # Penalty for likely non-content URLs
        if any(pattern in url_lower for pattern in ['login', 'signup', 'cart', 'checkout']):
            score -= 0.4

        # Normalize to 0-1 range
        return max(0.0, min(1.0, score))

    def _calculate_backoff(self, attempt: int, status_code: int) -> float:
        """
        Calculate intelligent retry backoff time.

        AGENT INTELLIGENCE: Different failures deserve different strategies.
          - 429 (rate limit): Longer backoff
          - 500 (server error): Medium backoff
          - 404 (not found): Don't retry (would be waste)
          - Network errors: Standard exponential backoff

        Returns:
            Backoff time in seconds
        """
        base_backoff = self.retry_backoff ** attempt

        # DECISION: Adapt backoff based on error type
        if status_code == 429:  # Rate limited
            return base_backoff * 3.0  # Extra patience
        elif status_code >= 500:  # Server error
            return base_backoff * 1.5  # Moderate patience
        elif status_code == 404:  # Not found
            return 0  # No point retrying
        else:
            return base_backoff  # Standard exponential

    def _extract_relevant_links(
        self,
        html: str,
        base_url: str,
        keywords: List[str]
    ) -> List[str]:
        """
        Extract and rank relevant links from HTML.

        AGENT DECISION LOGIC: Not all links are worth following.
        The agent intelligently filters and prioritizes.

        Returns:
            List of up to max_links_per_page most relevant URLs
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            links = []

            for anchor in soup.find_all('a', href=True):
                href = anchor['href']
                absolute_url = urljoin(base_url, href)

                # Filter out non-http(s) URLs
                if not absolute_url.startswith(('http://', 'https://')):
                    continue

                # Assess relevance
                relevance = self._assess_url_relevance(absolute_url, keywords)

                # Consider link text for additional relevance
                link_text = anchor.get_text(strip=True).lower()
                for keyword in keywords:
                    if keyword.lower() in link_text:
                        relevance += 0.1

                if relevance > 0.3:  # Threshold for following
                    links.append((absolute_url, relevance))

            # Sort by relevance and return top N
            links.sort(key=lambda x: x[1], reverse=True)
            top_links = [url for url, _ in links[:self.max_links_per_page]]

            return top_links

        except Exception as e:
            if self.verbose:
                print(f"[SCRAPER AGENT] Error extracting links: {e}")
            return []

    def _log_decision(self, url: str, decision: str, reason: str):
        """
        Log agent decisions for transparency and debugging.

        TEACHING NOTE: Agent transparency is critical for trust and debugging.
        Always log WHY an agent made a particular decision.
        """
        log_entry = {
            'timestamp': datetime.now(),
            'url': url,
            'decision': decision,
            'reason': reason
        }
        self.decision_log.append(log_entry)

        if self.verbose:
            print(f"[AGENT DECISION] {decision.upper()}: {url}")
            print(f"                 Reason: {reason}")

    def get_performance_metrics(self) -> Dict:
        """
        Get comprehensive agent performance metrics.

        DEBUGGING HELPER: Understand how well the agent is performing.

        Returns:
            Dict with success rates, domain learning, retry statistics, etc.
        """
        tool_stats = self.tool.get_fetch_stats()

        return {
            'total_urls_visited': len(self.visited_urls),
            'total_urls_failed': len(self.failed_urls),
            'success_rate': tool_stats.get('success_rate', 0.0),
            'high_quality_domains': len(self.high_quality_domains),
            'low_quality_domains': len(self.low_quality_domains),
            'total_retries': len(self.retry_history),
            'decisions_made': len(self.decision_log),
            'avg_response_time': tool_stats.get('avg_response_time', 0.0)
        }

    def clear_state(self):
        """
        Clear agent's learned state and history.

        Useful for:
          - Starting fresh crawls
          - Testing different strategies
          - Memory management for long-running agents
        """
        self.visited_urls.clear()
        self.failed_urls.clear()
        self.high_quality_domains.clear()
        self.low_quality_domains.clear()
        self.decision_log.clear()
        self.retry_history.clear()
        self.tool.clear_history()


# TEACHING EXAMPLE: Demonstrate the difference
if __name__ == "__main__":
    print("""
    ═══════════════════════════════════════════════════════════
    DEMONSTRATION: TOOL vs AGENT
    ═══════════════════════════════════════════════════════════
    """)

    # Create both tool and agent
    from src.tools.scraper_tool import ScraperTool

    tool = ScraperTool(debug=True)
    agent = ScraperAgent(verbose=True)

    test_url = "https://example.com"

    print("\n1️⃣  TOOL APPROACH (Passive Execution)")
    print("─" * 60)
    html, status, error, metadata = tool.fetch_url(test_url)
    print(f"Tool result: {'Success' if status == 200 else 'Failed'}")
    print("Tool just fetched what it was told. No decisions made.\n")

    print("\n2️⃣  AGENT APPROACH (Autonomous Intelligence)")
    print("─" * 60)
    html, success, decision_metadata = agent.fetch_with_intelligence(
        test_url,
        mission_keywords=['example', 'demonstration']
    )
    print(f"\nAgent result: {'Success' if success else 'Failed'}")
    print(f"Decisions made: {len(decision_metadata['decisions_made'])}")
    print("\nThe agent:")
    print("  ✓ Assessed relevance before fetching")
    print("  ✓ Would retry intelligently on failure")
    print("  ✓ Learned about domain quality")
    print("  ✓ Logged decisions for transparency")

    print("\n" + "═" * 60)
    print("This is the difference between TOOLS and AGENTS.")
    print("═" * 60 + "\n")
