"""
THE MIND — PLANNER AGENT
========================

ORGAN METAPHOR:
---------------
The Planner is the MIND of the research organism.
It receives a high-level research mission and breaks it down into actionable tasks.

ASCII DIAGRAM:
--------------
                     ┌─────────────────────┐
                     │   USER REQUEST      │
                     │ "Research wildfire  │
                     │   containment AI"   │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │   PLANNER AGENT     │
                     │      (MIND)         │
                     │   [AUTONOMOUS]      │
                     └──────────┬──────────┘
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
              ┌──────────┐ ┌────────┐ ┌──────────┐
              │ Task 1:  │ │Task 2: │ │ Task 3:  │
              │Fetch URL1│ │URL2    │ │ URL3     │
              └──────────┘ └────────┘ └──────────┘
                    │           │           │
                    └───────────┼───────────┘
                                ▼
                        [MISSION PLAN]

AGENT vs TOOL:
--------------
This is an AGENT because it:
  • Makes autonomous decisions about how to decompose a mission
  • Chooses which sources to prioritize
  • Adapts its plan based on mission context
  • Exhibits reasoning and strategic thinking

RESPONSIBILITIES:
-----------------
  1. Parse user mission requests
  2. Identify key topics and research angles
  3. Generate a list of target URLs or search queries
  4. Prioritize sources by relevance
  5. Create a task list for downstream organs

TEACHING NOTES:
---------------
The Planner demonstrates "planning intelligence" — it doesn't just execute,
it designs the research strategy. Compare this to the Scraper TOOL, which
simply fetches what it's told to fetch.

FUTURE EXTENSIONS:
------------------
  • Multi-turn planning (iterative refinement)
  • Integration with search APIs for dynamic source discovery
  • Learning from past mission success rates

DEBUGGING TIPS:
---------------
  • Log the full plan before execution
  • Track which URLs were selected and why
  • Monitor edge cases: vague missions, overly broad topics
"""

import uuid
from typing import List, Dict
from datetime import datetime
from ..pipeline.mission_model import MissionRequest, MissionPlan


class PlannerAgent:
    """
    THE MIND — Autonomous Planning Agent
    ====================================

    This agent demonstrates AUTONOMOUS DECISION-MAKING.
    It doesn't just execute — it strategizes.

    DECISION-MAKING CAPABILITIES:
    -----------------------------
      • Analyzes mission scope and complexity
      • Generates relevant search queries from topics
      • Selects and prioritizes information sources
      • Adapts strategy based on available vs. requested sources
      • Provides reasoning for its choices

    WHY THIS IS AN AGENT (NOT A TOOL):
    ----------------------------------
    Compare this to a simple function that just takes URLs and returns them.
    The PlannerAgent actually THINKS about:
      - What sources are most relevant?
      - How many sources are needed?
      - What's the best order to fetch them?
      - What search terms capture the user's intent?

    This reasoning and decision-making is what makes it an AGENT.
    """

    def __init__(self, debug: bool = False):
        """
        Initialize the Planner Agent.

        Args:
            debug: Enable detailed logging of planning decisions
        """
        self.debug = debug
        self._planning_history = []  # Track all plans for analysis

    def create_plan(self, request: MissionRequest) -> MissionPlan:
        """
        Create a research plan from a mission request.

        This is where the AUTONOMOUS DECISION-MAKING happens.
        The agent analyzes the request and strategizes how to fulfill it.

        Args:
            request: MissionRequest with topic and optional sources

        Returns:
            MissionPlan with prioritized URLs and reasoning

        TEACHING NOTE:
        --------------
        Notice how this method doesn't just pass data through.
        It makes decisions, applies heuristics, and generates new information.
        This is the hallmark of an AGENT.
        """
        mission_id = self._generate_mission_id()

        # DECISION POINT 1: Determine source strategy
        if request.sources:
            # User provided specific sources — validate and prioritize them
            target_urls = self._prioritize_user_sources(request.sources, request.max_sources)
            reasoning = self._explain_source_selection(request, target_urls, user_provided=True)
        else:
            # No sources provided — agent must discover them autonomously
            target_urls = self._discover_sources(request.topic, request.max_sources)
            reasoning = self._explain_source_selection(request, target_urls, user_provided=False)

        # DECISION POINT 2: Apply intelligence and constraints
        target_urls = self._apply_constraints(target_urls, request.max_sources)

        plan = MissionPlan(
            mission_id=mission_id,
            topic=request.topic,
            target_urls=target_urls,
            reasoning=reasoning,
            created_at=datetime.now()
        )

        # Track planning history for debugging and learning
        self._planning_history.append({
            'mission_id': mission_id,
            'request': request,
            'plan': plan,
            'timestamp': datetime.now()
        })

        if self.debug:
            self._log_planning_decision(request, plan)

        return plan

    def _generate_mission_id(self) -> str:
        """Generate unique mission identifier."""
        return f"mission_{uuid.uuid4().hex[:12]}"

    def _prioritize_user_sources(self, sources: List[str], max_sources: int) -> List[str]:
        """
        Prioritize user-provided sources.

        AGENT DECISION: Even with user sources, we apply intelligence:
          - Remove duplicates
          - Validate URL format
          - Prioritize by likely relevance (heuristic scoring)
          - Respect max_sources limit

        TEACHING NOTE: A simple TOOL would just return sources[:max_sources].
        An AGENT applies reasoning and validation.
        """
        # Remove duplicates while preserving order
        seen = set()
        unique_sources = []
        for url in sources:
            if url not in seen:
                seen.add(url)
                unique_sources.append(url)

        # Score and prioritize (heuristic: prefer HTTPS, known domains, etc.)
        scored_sources = []
        for url in unique_sources:
            score = self._score_source_quality(url)
            scored_sources.append((url, score))

        # Sort by score (descending)
        scored_sources.sort(key=lambda x: x[1], reverse=True)

        # Extract just the URLs
        prioritized = [url for url, score in scored_sources]

        return prioritized[:max_sources]

    def _discover_sources(self, topic: str, max_sources: int) -> List[str]:
        """
        Autonomously discover sources for a research topic.

        AGENT INTELLIGENCE: This is where real decision-making happens.
        The agent generates search queries and constructs URLs based on
        understanding of the topic.

        CURRENT IMPLEMENTATION: Rule-based source generation
        FUTURE UPGRADE: Could integrate with search APIs, use ML for source discovery

        TEACHING NOTE:
        --------------
        This method shows how an agent can CREATE new information,
        not just transform input → output deterministically.
        """
        # Extract key terms from topic
        keywords = self._extract_keywords(topic)

        # Generate search URLs for common research platforms
        discovered_urls = []

        # Strategy 1: Academic sources (if topic seems research-oriented)
        if self._is_academic_topic(topic):
            discovered_urls.extend(self._generate_academic_urls(keywords, max_sources // 2))

        # Strategy 2: News sources (for current events, trends)
        if self._is_news_topic(topic):
            discovered_urls.extend(self._generate_news_urls(keywords, max_sources // 2))

        # Strategy 3: Documentation and technical sources
        if self._is_technical_topic(topic):
            discovered_urls.extend(self._generate_technical_urls(keywords, max_sources // 2))

        # Strategy 4: General web search (fallback)
        if len(discovered_urls) < max_sources:
            discovered_urls.extend(self._generate_general_urls(keywords, max_sources - len(discovered_urls)))

        # Deduplicate and limit
        unique_urls = list(dict.fromkeys(discovered_urls))  # Preserve order

        return unique_urls[:max_sources]

    def _extract_keywords(self, topic: str) -> List[str]:
        """Extract key search terms from topic."""
        # Simple keyword extraction (could be enhanced with NLP)
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = topic.lower().split()
        keywords = [w for w in words if w not in stopwords and len(w) > 2]
        return keywords[:5]  # Limit to top 5 keywords

    def _is_academic_topic(self, topic: str) -> bool:
        """Heuristic: Does this topic seem academic/research-oriented?"""
        academic_indicators = ['research', 'study', 'analysis', 'theory', 'methodology', 'paper', 'journal']
        return any(indicator in topic.lower() for indicator in academic_indicators)

    def _is_news_topic(self, topic: str) -> bool:
        """Heuristic: Does this topic seem news/current events oriented?"""
        news_indicators = ['latest', 'recent', 'current', 'news', 'update', '2024', '2025', 'trend']
        return any(indicator in topic.lower() for indicator in news_indicators)

    def _is_technical_topic(self, topic: str) -> bool:
        """Heuristic: Does this topic seem technical/documentation oriented?"""
        tech_indicators = ['api', 'documentation', 'tutorial', 'guide', 'implementation', 'code', 'framework']
        return any(indicator in topic.lower() for indicator in tech_indicators)

    def _generate_academic_urls(self, keywords: List[str], limit: int) -> List[str]:
        """Generate URLs for academic sources."""
        query = '+'.join(keywords)
        return [
            f"https://scholar.google.com/scholar?q={query}",
            f"https://arxiv.org/search/?query={query}",
            f"https://www.researchgate.net/search/publication?q={query}"
        ][:limit]

    def _generate_news_urls(self, keywords: List[str], limit: int) -> List[str]:
        """Generate URLs for news sources."""
        query = '+'.join(keywords)
        return [
            f"https://news.google.com/search?q={query}",
            f"https://www.reuters.com/site-search/?query={query}",
            f"https://www.bbc.com/search?q={query}"
        ][:limit]

    def _generate_technical_urls(self, keywords: List[str], limit: int) -> List[str]:
        """Generate URLs for technical documentation."""
        query = '+'.join(keywords)
        return [
            f"https://stackoverflow.com/search?q={query}",
            f"https://github.com/search?q={query}",
            f"https://dev.to/search?q={query}"
        ][:limit]

    def _generate_general_urls(self, keywords: List[str], limit: int) -> List[str]:
        """Generate general web search URLs."""
        query = '+'.join(keywords)
        return [
            f"https://www.google.com/search?q={query}",
            f"https://duckduckgo.com/?q={query}",
            f"https://en.wikipedia.org/wiki/Special:Search?search={query}"
        ][:limit]

    def _score_source_quality(self, url: str) -> float:
        """
        Score a source URL for quality and relevance.

        AGENT HEURISTIC: Apply rules to assess source quality.
        This is a simple version; could be much more sophisticated.
        """
        score = 0.5  # Base score

        # Prefer HTTPS
        if url.startswith('https://'):
            score += 0.2

        # Prefer known reliable domains
        reliable_domains = ['.edu', '.gov', '.org', 'arxiv.org', 'scholar.google', 'ieee.org']
        if any(domain in url for domain in reliable_domains):
            score += 0.3

        # Slight penalty for very long URLs (often have tracking params)
        if len(url) > 200:
            score -= 0.1

        return max(0.0, min(1.0, score))  # Clamp to [0, 1]

    def _apply_constraints(self, urls: List[str], max_sources: int) -> List[str]:
        """Apply final constraints and validation."""
        # Ensure we don't exceed max_sources
        urls = urls[:max_sources]

        # Filter out invalid URLs (basic validation)
        valid_urls = [url for url in urls if url.startswith('http')]

        return valid_urls

    def _explain_source_selection(self, request: MissionRequest, urls: List[str], user_provided: bool) -> str:
        """
        Generate explanation for source selection.

        TRANSPARENCY: Good agents explain their reasoning.
        This builds trust and enables debugging.
        """
        if user_provided:
            reasoning = f"User provided {len(request.sources)} source(s). "
            reasoning += f"Selected top {len(urls)} after quality scoring and deduplication."
        else:
            reasoning = f"Autonomously discovered sources for topic: '{request.topic}'. "
            reasoning += f"Applied multi-strategy approach: "

            # Identify which strategies were used
            strategies = []
            if self._is_academic_topic(request.topic):
                strategies.append("academic research")
            if self._is_news_topic(request.topic):
                strategies.append("news/current events")
            if self._is_technical_topic(request.topic):
                strategies.append("technical documentation")

            if strategies:
                reasoning += f"{', '.join(strategies)}. "
            else:
                reasoning += "general web search. "

            reasoning += f"Selected {len(urls)} high-quality sources."

        return reasoning

    def _log_planning_decision(self, request: MissionRequest, plan: MissionPlan):
        """Debug logging for planning decisions."""
        print(f"\n{'='*60}")
        print(f"PLANNER AGENT — DECISION LOG")
        print(f"{'='*60}")
        print(f"Mission ID: {plan.mission_id}")
        print(f"Topic: {plan.topic}")
        print(f"Requested max sources: {request.max_sources}")
        print(f"Selected sources: {len(plan.target_urls)}")
        print(f"\nReasoning:\n{plan.reasoning}")
        print(f"\nTarget URLs:")
        for i, url in enumerate(plan.target_urls, 1):
            print(f"  {i}. {url}")
        print(f"{'='*60}\n")

    def get_planning_stats(self) -> Dict:
        """
        Get statistics about planning history.

        DEBUGGING HELPER: Useful for understanding agent behavior over time.
        """
        if not self._planning_history:
            return {"total_plans": 0}

        return {
            "total_plans": len(self._planning_history),
            "avg_sources_per_plan": sum(len(p['plan'].target_urls) for p in self._planning_history) / len(self._planning_history),
            "topics_planned": [p['request'].topic for p in self._planning_history]
        }
