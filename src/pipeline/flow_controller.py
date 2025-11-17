"""
FLOW CONTROLLER — ORCHESTRATION ENGINE
=======================================

ORGAN METAPHOR:
---------------
The Flow Controller is the CIRCULATORY SYSTEM of the research organism.
It coordinates the flow of data between all the organs, ensuring
each step happens in the right order with the right inputs.

ASCII DIAGRAM:
--------------
                   ╔══════════════════════════════════╗
                   ║    FLOW CONTROLLER              ║
                   ║   (CIRCULATORY SYSTEM)          ║
                   ╚══════════════════════════════════╝
                                  │
                 ┌────────────────┼────────────────┐
                 │                │                │
                 ▼                ▼                ▼
        ┌────────────────┐  ┌─────────┐  ┌────────────────┐
        │ PLANNER AGENT  │  │ AGENTS  │  │  SUMMARIZER    │
        │    (MIND)      │  │         │  │   (TONGUE)     │
        └────────┬───────┘  └────┬────┘  └────────┬───────┘
                 │               │                  │
          creates plan     coordinates       creates digest
                 │               │                  │
                 └───────────────┼──────────────────┘
                                 │
                 ┌───────────────┼────────────────┐
                 │               │                │
                 ▼               ▼                ▼
        ┌────────────────┐  ┌─────────┐  ┌────────────────┐
        │ SCRAPER TOOL   │  │ TOOLS   │  │  NOTION HAND   │
        │   (LIMB)       │  │         │  │   (OUTPUT)     │
        └────────┬───────┘  └────┬────┘  └────────┬───────┘
                 │               │                  │
          fetches pages    cleans data      stores results
                 │               │                  │
                 └───────────────┼──────────────────┘
                                 │
                                 ▼
                        ┌────────────────┐
                        │ LOGGER TOOL    │
                        │  (MEMORY)      │
                        └────────────────┘

PURPOSE:
--------
Orchestrate the complete research pipeline:
  Plan → Fetch → Clean → Summarize → Store → Log

RESPONSIBILITIES:
-----------------
  1. Accept a MissionRequest from the user
  2. Invoke the Planner Agent to create a plan
  3. Use the Scraper Tool to fetch each source
  4. Use the Cleaner Tool to extract clean text
  5. Invoke the Summarizer Agent to create digests
  6. Use the Notion Tool to store outputs
  7. Use the Logger Tool to record the mission
  8. Handle errors and retry logic at each stage
  9. Calculate scores for quality and relevance
  10. Provide progress updates throughout execution

TEACHING NOTES:
---------------
The Flow Controller demonstrates ORCHESTRATION — it doesn't do the work,
it coordinates the workers. This is a common pattern in complex systems:
a central coordinator that manages multiple specialized subsystems.

Notice how it calls AGENTS (which make decisions) and TOOLS (which execute
commands) in a specific sequence. The controller knows WHEN to invoke each
component, but not HOW each component does its work.

This separation of concerns is critical:
  • Agents decide WHAT to do
  • Tools execute HOW to do it
  • Controller orchestrates WHEN to do it

PHASE 3 INTEGRATION:
--------------------
Phase 3 adds:
  ✓ Complete mission lifecycle orchestration (Step 21-22)
  ✓ Scoring system integration (Step 23)
  ✓ Error handling and retry logic (Step 24)

FUTURE EXTENSIONS:
------------------
  • Parallel execution of independent tasks
  • Conditional branching (if summary is low-quality, retry)
  • Partial failure recovery (continue mission despite individual fetch failures)
  • Real-time progress updates for UI
  • Async/await for concurrent operations

DEBUGGING TIPS:
---------------
  • Log every stage transition with timestamps
  • Track data transformations at each step
  • Monitor for bottlenecks in the pipeline
  • Test error handling for each stage independently
"""

import time
import traceback
from typing import Dict, List, Optional, Callable
from datetime import datetime
from dataclasses import asdict

from ..agents.planner_agent import PlannerAgent
from ..agents.summarizer_agent import SummarizerAgent
from ..agents.scraper_agent import ScraperAgent  # NEW in Phase 5
from ..tools.scraper_tool import ScraperTool
from ..tools.cleaner_tool import CleanerTool
from ..tools.notion_tool import NotionTool
from ..tools.logger_tool import LoggerTool
from ..utils import scoring
from .mission_model import MissionRequest, MissionPlan, MissionResult


class FlowController:
    """
    THE CIRCULATORY SYSTEM — Pipeline Orchestrator
    ===============================================

    This class orchestrates the complete research pipeline,
    coordinating agents and tools to execute research missions.

    ORCHESTRATION PATTERN:
    ----------------------
    The FlowController follows a choreographed pipeline:

      1. PLAN (Agent)      → PlannerAgent creates strategy
      2. FETCH (Tool)      → ScraperTool gets raw pages
      3. CLEAN (Tool)      → CleanerTool extracts text
      4. SCORE (Utility)   → Scoring functions assess quality
      5. SUMMARIZE (Agent) → SummarizerAgent creates digest
      6. STORE (Tool)      → NotionTool saves to workspace
      7. LOG (Tool)        → LoggerTool records history

    Each stage can:
      • Succeed and continue
      • Fail with retry
      • Fail permanently and abort

    TEACHING NOTE:
    --------------
    This demonstrates the CONTROLLER pattern in software architecture.
    The controller has no domain logic — it just knows the sequence
    and handles errors. Each component does its specialized work.

    Compare to a symphony conductor: doesn't play instruments,
    just coordinates the musicians (agents/tools) for harmony.
    """

    # Retry configuration
    MAX_RETRIES = 3
    RETRY_DELAY = 2.0  # seconds
    TIMEOUT_PER_URL = 30  # seconds

    def __init__(
        self,
        planner: Optional[PlannerAgent] = None,
        scraper: Optional[ScraperTool] = None,
        scraper_agent: Optional[ScraperAgent] = None,  # NEW in Phase 5
        cleaner: Optional[CleanerTool] = None,
        summarizer: Optional[SummarizerAgent] = None,
        notion: Optional[NotionTool] = None,
        logger: Optional[LoggerTool] = None,
        use_intelligent_crawling: bool = False,  # NEW in Phase 5
        debug: bool = False,
        progress_callback: Optional[Callable[[str, float], None]] = None
    ):
        """
        Initialize the Flow Controller.

        Args:
            planner: PlannerAgent instance (creates new if None)
            scraper: ScraperTool instance (creates new if None)
            scraper_agent: ScraperAgent instance for intelligent crawling (Phase 5)
            cleaner: CleanerTool instance (creates new if None)
            summarizer: SummarizerAgent instance (creates new if None)
            notion: NotionTool instance (creates new if None)
            logger: LoggerTool instance (creates new if None)
            use_intelligent_crawling: Enable ScraperAgent mode (Phase 5 feature)
            debug: Enable detailed logging
            progress_callback: Optional function to report progress (message, percent)

        TEACHING NOTE (Phase 5):
        ------------------------
        NEW HYBRIDIZATION PATTERN: The controller now supports TWO modes:

          1. TOOL MODE (Classic):
             - Uses ScraperTool for simple, deterministic fetching
             - Fast and predictable
             - No autonomous exploration

          2. AGENT MODE (Intelligent):
             - Uses ScraperAgent for autonomous crawling
             - Slower but smarter
             - Follows relevant links, retries intelligently
             - Discovers additional high-quality sources

        Toggle between modes with use_intelligent_crawling flag.
        This teaches when to use TOOLS vs AGENTS based on needs.
        """
        # Initialize all organs (agents and tools)
        self.planner = planner or PlannerAgent(debug=debug)
        self.cleaner = cleaner or CleanerTool(debug=debug)
        self.summarizer = summarizer or SummarizerAgent(debug=debug)
        self.notion = notion or NotionTool(debug=debug)
        self.logger = logger or LoggerTool(debug=debug)

        # PHASE 5 HYBRIDIZATION: Support both tool and agent modes
        self.use_intelligent_crawling = use_intelligent_crawling
        self.scraper = scraper or ScraperTool(debug=debug)
        self.scraper_agent = scraper_agent or ScraperAgent(verbose=debug)

        self.debug = debug
        self.progress_callback = progress_callback

        # Execution history
        self._execution_history = []

    def execute_mission(self, request: MissionRequest) -> MissionResult:
        """
        Execute a complete research mission from request to result.

        This is the main orchestration function that coordinates
        all agents and tools through the complete pipeline.

        Args:
            request: MissionRequest with topic, sources, preferences

        Returns:
            MissionResult with summaries, metadata, and status

        Raises:
            Exception: If mission fails catastrophically

        Example:
            >>> controller = FlowController(debug=True)
            >>> request = MissionRequest(
            ...     topic="AI wildfire detection systems",
            ...     max_sources=3,
            ...     summary_style="technical"
            ... )
            >>> result = controller.execute_mission(request)
            >>> print(result.summaries[0])

        TEACHING NOTE:
        --------------
        This method demonstrates the COMPLETE PIPELINE FLOW.
        Watch how data transforms at each stage:
          MissionRequest → MissionPlan → Raw HTML → Clean Text → Summary → MissionResult

        Each transformation is performed by a specialized component.
        """
        start_time = datetime.now()
        self._report_progress("Starting mission", 0.0)

        # Initialize result object
        result = MissionResult(
            mission_id="",
            topic=request.topic,
            status="in_progress"
        )

        try:
            # ═══════════════════════════════════════════════════
            # STAGE 1: PLANNING (Agent Decision-Making)
            # ═══════════════════════════════════════════════════
            self._report_progress("Planning mission", 10.0)
            plan = self._stage_plan(request)
            result.mission_id = plan.mission_id

            if self.debug:
                print(f"\n[FLOW] Mission {plan.mission_id} planned")
                print(f"[FLOW] Target URLs: {len(plan.target_urls)}")

            # ═══════════════════════════════════════════════════
            # STAGE 2: FETCHING (Tool Execution)
            # ═══════════════════════════════════════════════════
            self._report_progress("Fetching sources", 25.0)
            raw_html = self._stage_fetch(plan, result)

            if self.debug:
                print(f"[FLOW] Fetched {len(raw_html)} pages successfully")

            # ═══════════════════════════════════════════════════
            # STAGE 3: CLEANING (Tool Execution)
            # ═══════════════════════════════════════════════════
            self._report_progress("Cleaning content", 50.0)
            clean_text = self._stage_clean(raw_html, result)

            if self.debug:
                print(f"[FLOW] Cleaned {len(clean_text)} pages")
                total_words = sum(len(text.split()) for text in clean_text.values())
                print(f"[FLOW] Total words extracted: {total_words}")

            # ═══════════════════════════════════════════════════
            # STAGE 4: SCORING (Utility Functions)
            # ═══════════════════════════════════════════════════
            self._report_progress("Scoring content", 60.0)
            scores = self._stage_score(clean_text, request)

            if self.debug:
                avg_score = sum(scores.values()) / len(scores) if scores else 0
                print(f"[FLOW] Average quality score: {avg_score:.2f}")

            # ═══════════════════════════════════════════════════
            # STAGE 5: SUMMARIZATION (Agent Decision-Making)
            # ═══════════════════════════════════════════════════
            self._report_progress("Summarizing content", 75.0)
            summaries = self._stage_summarize(clean_text, request, scores)

            result.summaries = summaries

            if self.debug:
                print(f"[FLOW] Generated {len(summaries)} summaries")

            # ═══════════════════════════════════════════════════
            # STAGE 6: STORAGE (Tool Execution)
            # ═══════════════════════════════════════════════════
            self._report_progress("Storing results", 90.0)
            storage_success = self._stage_store(result, request)

            # ═══════════════════════════════════════════════════
            # STAGE 7: LOGGING (Tool Execution)
            # ═══════════════════════════════════════════════════
            result.status = "completed"
            result.completed_at = datetime.now()
            result.metadata = {
                'plan': asdict(plan),
                'scores': scores,
                'storage_success': storage_success,
                'execution_time': (result.completed_at - start_time).total_seconds()
            }

            self._stage_log(result)

            self._report_progress("Mission completed", 100.0)

            if self.debug:
                execution_time = (result.completed_at - start_time).total_seconds()
                print(f"\n[FLOW] ✓ Mission completed in {execution_time:.2f}s")

            # Record in history
            self._record_execution(request, result, success=True)

            return result

        except Exception as e:
            # Handle catastrophic failure
            result.status = "failed"
            result.error_message = f"{type(e).__name__}: {str(e)}"
            result.completed_at = datetime.now()

            if self.debug:
                print(f"\n[FLOW] ✗ Mission failed: {result.error_message}")
                print(traceback.format_exc())

            # Log the failed mission
            self._stage_log(result)

            # Record in history
            self._record_execution(request, result, success=False)

            self._report_progress(f"Mission failed: {str(e)}", 100.0)

            raise

    def _stage_plan(self, request: MissionRequest) -> MissionPlan:
        """
        STAGE 1: Planning

        Invoke the Planner AGENT to create a research plan.

        TEACHING NOTE:
        --------------
        This is an AGENT invocation — we're asking the Planner
        to make decisions about which sources to fetch and why.
        """
        if self.debug:
            print(f"\n{'='*60}")
            print("STAGE 1: PLANNING (Agent)")
            print(f"{'='*60}")

        plan = self.planner.create_plan(request)

        if self.debug:
            print(f"✓ Plan created: {plan.mission_id}")
            print(f"  Strategy: {plan.reasoning[:100]}...")

        return plan

    def _stage_fetch(self, plan: MissionPlan, result: MissionResult) -> Dict[str, str]:
        """
        STAGE 2: Fetching

        Use either ScraperTool (simple) or ScraperAgent (intelligent)
        based on use_intelligent_crawling flag.

        TEACHING NOTE (Phase 5):
        ------------------------
        This demonstrates the TOOL vs AGENT choice in action:

        TOOL MODE (Classic):
          - Fetches exactly the URLs in the plan
          - Fast, simple, deterministic
          - Good for known, high-quality sources

        AGENT MODE (Intelligent):
          - Starts with plan URLs as seeds
          - Autonomously explores related content
          - Follows relevant links
          - Retries with intelligent backoff
          - Returns curated, high-quality content
          - Slower but potentially finds better sources

        The choice teaches: "When do I need autonomy vs simplicity?"

        ERROR HANDLING (Phase 3, Step 24):
        -----------------------------------
        - Retry failed fetches up to MAX_RETRIES times
        - Exponential backoff between retries
        - Continue with partial results if some fetches fail
        - Log all failures for debugging
        """
        if self.debug:
            print(f"\n{'='*60}")
            if self.use_intelligent_crawling:
                print("STAGE 2: INTELLIGENT CRAWLING (Agent)")
                print("  Mode: ScraperAgent - autonomous exploration")
            else:
                print("STAGE 2: FETCHING (Tool)")
                print("  Mode: ScraperTool - simple deterministic fetch")
            print(f"{'='*60}")

        raw_html = {}

        # PHASE 5 HYBRIDIZATION: Choose between tool and agent mode
        if self.use_intelligent_crawling:
            # ═══════════════════════════════════════════════════
            # AGENT MODE: Intelligent crawling with exploration
            # ═══════════════════════════════════════════════════
            if self.debug:
                print("\n🧠 Using AGENT MODE: Intelligent crawling enabled")
                print("   The agent will:")
                print("   • Assess URL relevance before fetching")
                print("   • Follow promising links autonomously")
                print("   • Retry failures with intelligent backoff")
                print("   • Learn from successes to prioritize quality domains\n")

            # Extract keywords from topic for relevance assessment
            keywords = plan.topic.lower().split()

            # Let the agent crawl intelligently
            crawl_results = self.scraper_agent.crawl_intelligently(
                seed_urls=plan.target_urls,
                mission_keywords=keywords,
                max_pages=len(plan.target_urls) * 2  # Allow agent to find 2x sources
            )

            # Convert agent results to dict format
            for url, html in crawl_results:
                raw_html[url] = html

            if self.debug:
                print(f"\n✓ Agent crawled {len(raw_html)} pages")
                metrics = self.scraper_agent.get_performance_metrics()
                print(f"  Success rate: {metrics['success_rate']*100:.1f}%")
                print(f"  Decisions made: {metrics['decisions_made']}")

        else:
            # ═══════════════════════════════════════════════════
            # TOOL MODE: Simple deterministic fetching
            # ═══════════════════════════════════════════════════
            if self.debug:
                print("\n🔧 Using TOOL MODE: Simple deterministic fetch")
                print("   Fetching exactly the URLs provided\n")

            for i, url in enumerate(plan.target_urls):
                if self.debug:
                    print(f"\nFetching {i+1}/{len(plan.target_urls)}: {url}")

                # Attempt fetch with retries
                html, status_code, error = self._fetch_with_retry(url)

                if html:
                    raw_html[url] = html
                    if self.debug:
                        print(f"  ✓ Success: {len(html)} chars")
                else:
                    if self.debug:
                        print(f"  ✗ Failed after {self.MAX_RETRIES} attempts: {error}")
                    # Store error in result metadata
                    if 'fetch_errors' not in result.metadata:
                        result.metadata['fetch_errors'] = {}
                    result.metadata['fetch_errors'][url] = error

        # Store raw HTML in result
        result.raw_html = raw_html

        # Store mode information in metadata
        result.metadata['scraping_mode'] = 'agent' if self.use_intelligent_crawling else 'tool'

        if not raw_html:
            raise Exception("Failed to fetch any sources")

        return raw_html

    def _fetch_with_retry(self, url: str) -> tuple:
        """
        Fetch URL with exponential backoff retry logic.

        RETRY LOGIC (Phase 3, Step 24):
        --------------------------------
        - Attempt 1: immediate
        - Attempt 2: wait 2s
        - Attempt 3: wait 4s
        - Attempt 4: wait 8s (if MAX_RETRIES=3)

        This gives transient network issues time to resolve.
        """
        for attempt in range(self.MAX_RETRIES):
            html, status_code, error, metadata = self.scraper.fetch_url(
                url,
                timeout=self.TIMEOUT_PER_URL
            )

            if html:
                return (html, status_code, "")

            # If not last attempt, wait before retrying
            if attempt < self.MAX_RETRIES - 1:
                delay = self.RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                if self.debug:
                    print(f"  Retry {attempt + 2}/{self.MAX_RETRIES} in {delay}s...")
                time.sleep(delay)

        # All retries exhausted
        return (None, status_code, error)

    def _stage_clean(self, raw_html: Dict[str, str], result: MissionResult) -> Dict[str, str]:
        """
        STAGE 3: Cleaning

        Use the Cleaner TOOL to extract clean text from raw HTML.

        TEACHING NOTE:
        --------------
        This is a TOOL invocation — deterministic text extraction.
        The cleaner applies consistent rules to extract content.
        """
        if self.debug:
            print(f"\n{'='*60}")
            print("STAGE 3: CLEANING (Tool)")
            print(f"{'='*60}")

        clean_text = {}

        for url, html in raw_html.items():
            if self.debug:
                print(f"\nCleaning: {url}")

            try:
                cleaned = self.cleaner.clean_html(html, url)
                clean_text[url] = cleaned['clean_text']

                if self.debug:
                    print(f"  ✓ Extracted {cleaned['word_count']} words")
                    print(f"    Title: {cleaned['title']}")

                # Store metadata
                if 'clean_metadata' not in result.metadata:
                    result.metadata['clean_metadata'] = {}
                result.metadata['clean_metadata'][url] = {
                    'title': cleaned['title'],
                    'word_count': cleaned['word_count'],
                    'metadata': cleaned['metadata']
                }

            except Exception as e:
                if self.debug:
                    print(f"  ✗ Cleaning failed: {str(e)}")
                # Store error but continue with other URLs
                if 'cleaning_errors' not in result.metadata:
                    result.metadata['cleaning_errors'] = {}
                result.metadata['cleaning_errors'][url] = str(e)

        # Store clean text in result
        result.clean_text = clean_text

        if not clean_text:
            raise Exception("Failed to clean any content")

        return clean_text

    def _stage_score(self, clean_text: Dict[str, str], request: MissionRequest) -> Dict[str, float]:
        """
        STAGE 4: Scoring

        Calculate quality and relevance scores for each source.

        SCORING SYSTEM (Phase 3, Step 23):
        -----------------------------------
        For each cleaned text, we calculate:
          1. Keyword relevance (based on topic keywords)
          2. Text quality (readability, completeness)
          3. Composite score (weighted combination)

        These scores help the Summarizer AGENT prioritize content.

        TEACHING NOTE:
        --------------
        Scoring functions are TOOLS (deterministic calculations).
        The Summarizer AGENT uses these scores to make decisions
        about what to emphasize in summaries.
        """
        if self.debug:
            print(f"\n{'='*60}")
            print("STAGE 4: SCORING (Utility)")
            print(f"{'='*60}")

        scores = {}

        # Extract keywords from topic
        keywords = request.topic.lower().split()

        for url, text in clean_text.items():
            if self.debug:
                print(f"\nScoring: {url}")

            # Calculate individual scores
            keyword_score = scoring.score_keyword_relevance(text, keywords)
            quality_score = scoring.score_text_quality(text)
            readability_score = scoring.score_readability(text)

            # Composite score (weighted)
            composite = scoring.score_composite(
                [keyword_score, quality_score, readability_score],
                weights=[2.0, 1.0, 0.5]  # Relevance weighted highest
            )

            scores[url] = composite

            if self.debug:
                print(f"  Keyword relevance: {keyword_score:.2f}")
                print(f"  Text quality: {quality_score:.2f}")
                print(f"  Readability: {readability_score:.2f}")
                print(f"  ✓ Composite score: {composite:.2f}")

        return scores

    def _stage_summarize(
        self,
        clean_text: Dict[str, str],
        request: MissionRequest,
        scores: Dict[str, float]
    ) -> List[str]:
        """
        STAGE 5: Summarization

        Invoke the Summarizer AGENT to create narrative summaries.

        TEACHING NOTE:
        --------------
        This is an AGENT invocation — the Summarizer makes decisions
        about tone, emphasis, and structure based on:
          - Content quality (from scores)
          - Summary style preference
          - Topic context

        The agent uses scores to prioritize high-quality sources.
        """
        if self.debug:
            print(f"\n{'='*60}")
            print("STAGE 5: SUMMARIZATION (Agent)")
            print(f"{'='*60}")

        summaries = []

        # Sort URLs by score (highest first)
        sorted_urls = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        for url, score in sorted_urls:
            if url not in clean_text:
                continue

            text = clean_text[url]

            if self.debug:
                print(f"\nSummarizing: {url}")
                print(f"  Quality score: {score:.2f}")

            try:
                # Agent decides how to summarize based on style and content
                summary_result = self.summarizer.summarize(
                    text=text,
                    topic=request.topic,
                    style=request.summary_style
                )

                summary = summary_result['summary']
                summaries.append(summary)

                if self.debug:
                    print(f"  ✓ Generated {len(summary)} char summary")
                    print(f"    Preview: {summary[:100]}...")

            except Exception as e:
                if self.debug:
                    print(f"  ✗ Summarization failed: {str(e)}")
                # Continue with other sources

        if not summaries:
            raise Exception("Failed to generate any summaries")

        return summaries

    def _stage_store(self, result: MissionResult, request: MissionRequest) -> bool:
        """
        STAGE 6: Storage

        Use the Notion TOOL to store results (or prepare for storage).

        NOTION INTEGRATION (Phase 3, Step 27):
        ---------------------------------------
        Store mission results to Notion workspace:
          - Mission summary
          - Individual summaries
          - Metadata and scores
          - Links to sources

        TEACHING NOTE:
        --------------
        This is a TOOL invocation — deterministic write operation.
        The tool doesn't decide WHAT or HOW to organize content,
        it just executes the write operation.
        """
        if self.debug:
            print(f"\n{'='*60}")
            print("STAGE 6: STORAGE (Tool)")
            print(f"{'='*60}")

        try:
            # Prepare data for Notion
            notion_data = {
                'mission_id': result.mission_id,
                'topic': result.topic,
                'summaries': result.summaries,
                'status': result.status,
                'metadata': result.metadata
            }

            # Write to Notion (or prepare for write if no API key configured)
            success = self.notion.write_mission(notion_data)

            if self.debug:
                if success:
                    print("  ✓ Results stored to Notion")
                else:
                    print("  ⚠ Notion write prepared (no API key configured)")

            return success

        except Exception as e:
            if self.debug:
                print(f"  ✗ Storage failed: {str(e)}")
            return False

    def _stage_log(self, result: MissionResult):
        """
        STAGE 7: Logging

        Use the Logger TOOL to record the mission in the database.

        LOGGER INTEGRATION (Phase 3, Step 28):
        ---------------------------------------
        Log complete mission history:
          - Mission metadata
          - All fetches (success/failure)
          - All summaries
          - Execution time and status

        This creates a complete audit trail for analysis and debugging.

        TEACHING NOTE:
        --------------
        This is a TOOL invocation — deterministic database write.
        The logger just records everything faithfully.
        """
        if self.debug:
            print(f"\n{'='*60}")
            print("STAGE 7: LOGGING (Tool)")
            print(f"{'='*60}")

        try:
            # Convert MissionResult to logger format
            mission_data = {
                'mission_id': result.mission_id,
                'topic': result.topic,
                'status': result.status,
                'source_count': len(result.raw_html) if result.raw_html else 0,
                'summary_count': len(result.summaries) if result.summaries else 0,
                'metadata': result.metadata,
                'completed_at': result.completed_at
            }

            self.logger.log_mission(mission_data)

            if self.debug:
                print(f"  ✓ Mission {result.mission_id} logged to database")

        except Exception as e:
            if self.debug:
                print(f"  ✗ Logging failed: {str(e)}")
                print("  (Mission execution succeeded, but logging failed)")

    def _report_progress(self, message: str, percent: float):
        """Report progress to callback if configured."""
        if self.progress_callback:
            self.progress_callback(message, percent)
        elif self.debug:
            print(f"[PROGRESS] {message} ({percent:.0f}%)")

    def _record_execution(self, request: MissionRequest, result: MissionResult, success: bool):
        """Record execution in controller history for analytics."""
        self._execution_history.append({
            'request': request,
            'result': result,
            'success': success,
            'timestamp': datetime.now()
        })

    def get_execution_stats(self) -> Dict:
        """
        Get statistics about pipeline execution history.

        DEBUGGING HELPER: Analyze controller performance.

        Returns:
            Dict with success_rate, avg_execution_time, total_missions, etc.
        """
        if not self._execution_history:
            return {
                'total_missions': 0,
                'success_rate': 0.0,
                'avg_execution_time': 0.0
            }

        total = len(self._execution_history)
        successes = sum(1 for h in self._execution_history if h['success'])

        execution_times = []
        for h in self._execution_history:
            if h['result'].completed_at and 'execution_time' in h['result'].metadata:
                execution_times.append(h['result'].metadata['execution_time'])

        return {
            'total_missions': total,
            'successes': successes,
            'failures': total - successes,
            'success_rate': successes / total if total > 0 else 0.0,
            'avg_execution_time': sum(execution_times) / len(execution_times) if execution_times else 0.0
        }


# Convenience function for simple mission execution
def execute_mission(topic: str, max_sources: int = 5, style: str = "technical", debug: bool = False) -> MissionResult:
    """
    Convenience function to execute a mission with minimal setup.

    Args:
        topic: Research topic
        max_sources: Maximum number of sources to fetch
        style: Summary style (technical, executive, casual)
        debug: Enable debug logging

    Returns:
        MissionResult

    Example:
        >>> result = execute_mission(
        ...     "AI wildfire detection",
        ...     max_sources=3,
        ...     style="executive"
        ... )
        >>> print(result.summaries[0])

    TEACHING NOTE:
    --------------
    This wraps the full FlowController for simple one-off missions.
    For repeated missions, create a FlowController instance directly
    to reuse components and track history.
    """
    controller = FlowController(debug=debug)
    request = MissionRequest(
        topic=topic,
        max_sources=max_sources,
        summary_style=style
    )
    return controller.execute_mission(request)
