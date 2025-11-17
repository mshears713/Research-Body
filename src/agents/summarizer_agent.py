"""
THE TONGUE — SUMMARIZER AGENT
==============================

ORGAN METAPHOR:
---------------
The Summarizer is the TONGUE of the research organism.
It tastes the cleaned content and produces narrative explanations,
digests, and summaries tailored to the mission's purpose.

ASCII DIAGRAM:
--------------
                ┌──────────────────────────┐
                │   CLEAN TEXT INPUT       │
                │   (from Cleaner)         │
                └────────────┬─────────────┘
                             │
                             ▼
                ┌──────────────────────────┐
                │   SUMMARIZER AGENT       │
                │       (TONGUE)           │
                │    [AUTONOMOUS]          │
                │                          │
                │  ╔════════════════╗      │
                │  ║  DECIDE:       ║      │
                │  ║  • Tone        ║      │
                │  ║  • Length      ║      │
                │  ║  • Focus       ║      │
                │  ╚════════════════╝      │
                └────────────┬─────────────┘
                             │
                ┌────────────┼────────────┐
                ▼            ▼            ▼
          [Technical]  [Executive]  [Casual]
             style       summary      digest
                             │
                             ▼
                ┌──────────────────────────┐
                │   NARRATIVE OUTPUT       │
                │   "AI wildfire systems   │
                │    use thermal imaging"  │
                └──────────────────────────┘

AGENT vs TOOL:
--------------
This is an AGENT because it:
  • Makes decisions about tone, length, and focus
  • Chooses what to emphasize or omit
  • Adapts output style based on mission context (technical, casual, trend-focused)
  • Exhibits creative and editorial judgment

RESPONSIBILITIES:
-----------------
  1. Receive cleaned text from the Cleaner Tool
  2. Analyze content for key insights and themes
  3. Generate narrative summaries in the requested style
  4. Format output for consumption by humans or downstream tools
  5. Score the quality and relevance of the summary

TEACHING NOTES:
---------------
The Summarizer demonstrates "creative intelligence" — it doesn't just extract,
it interprets and narrates. This is what separates it from a simple keyword
extractor or text truncator.

FUTURE EXTENSIONS:
------------------
  • Multi-perspective summaries (technical vs. executive)
  • Trend analysis across multiple sources
  • Integration with LLM APIs for advanced summarization
  • Sentiment and tone detection

DEBUGGING TIPS:
---------------
  • Compare summaries against source text for accuracy
  • Monitor for hallucinations or over-generalization
  • Track summary length vs. source length ratios
"""

import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from collections import Counter


class SummarizerAgent:
    """
    THE TONGUE — Autonomous Summarization Agent
    ============================================

    This agent demonstrates AUTONOMOUS EDITORIAL JUDGMENT.
    It doesn't just extract — it interprets and narrates.

    DECISION-MAKING CAPABILITIES:
    -----------------------------
      • Chooses summarization strategy based on style preference
      • Decides what content to emphasize or omit
      • Adapts tone (technical, executive, casual)
      • Determines appropriate summary length
      • Scores its own output for quality

    WHY THIS IS AN AGENT (NOT A TOOL):
    ----------------------------------
    Compare this to a simple text truncator that just takes first N sentences.
    The SummarizerAgent actually THINKS about:
      - What are the most important points?
      - How should I phrase this for the intended audience?
      - What tone and style is most appropriate?
      - Is this summary comprehensive enough?

    This editorial judgment and decision-making is what makes it an AGENT.

    TEACHING NOTE:
    --------------
    In this Phase 2 implementation, we use rule-based heuristics.
    In Phase 5, we could integrate LLM APIs for more sophisticated summarization.
    But even with rules, the AGENT behavior is clear: it makes choices.
    """

    # Summary styles with different characteristics
    STYLES = {
        'technical': {
            'tone': 'formal and precise',
            'focus': 'methodology, data, specifics',
            'sentence_count': (5, 10),
            'bullet_points': True
        },
        'executive': {
            'tone': 'concise and actionable',
            'focus': 'key insights, implications',
            'sentence_count': (3, 5),
            'bullet_points': True
        },
        'casual': {
            'tone': 'conversational and accessible',
            'focus': 'main ideas, storytelling',
            'sentence_count': (4, 8),
            'bullet_points': False
        },
        'trend_analysis': {
            'tone': 'analytical and comparative',
            'focus': 'patterns, changes, emerging themes',
            'sentence_count': (6, 12),
            'bullet_points': True
        }
    }

    def __init__(self, default_style: str = "technical", debug: bool = False):
        """
        Initialize the Summarizer Agent.

        Args:
            default_style: Default summary style (technical, executive, casual)
            debug: Enable detailed logging of summarization decisions
        """
        self.default_style = default_style
        self.debug = debug
        self._summary_history = []  # Track all summaries for analysis

    def summarize(
        self,
        clean_text: str,
        title: str = "",
        style: Optional[str] = None,
        max_length: Optional[int] = None
    ) -> Dict[str, any]:
        """
        Generate a summary from clean text.

        This is where the AUTONOMOUS DECISION-MAKING happens.
        The agent analyzes content and strategizes how to summarize it.

        Args:
            clean_text: Cleaned text from Cleaner Tool
            title: Optional title for context
            style: Summary style (technical, executive, casual) or None for default
            max_length: Optional maximum character length

        Returns:
            Dictionary containing:
            - summary: Generated summary text
            - style: Style used
            - key_points: List of key points extracted
            - word_count: Words in summary
            - score: Quality score (0-1)
            - reasoning: Explanation of decisions made

        TEACHING NOTE:
        --------------
        Notice how this method doesn't just process text mechanically.
        It makes decisions, applies strategy, and explains its reasoning.
        This is the hallmark of an AGENT.
        """
        # DECISION POINT 1: Choose style
        chosen_style = style or self.default_style
        if chosen_style not in self.STYLES:
            chosen_style = self.default_style

        style_config = self.STYLES[chosen_style]

        if self.debug:
            print(f"\n[SUMMARIZER AGENT] Starting summarization")
            print(f"[SUMMARIZER AGENT] Style: {chosen_style}")
            print(f"[SUMMARIZER AGENT] Input: {len(clean_text)} chars")

        # DECISION POINT 2: Extract key sentences
        sentences = self._extract_sentences(clean_text)
        scored_sentences = self._score_sentences(sentences, title)

        # DECISION POINT 3: Select most important sentences
        min_sent, max_sent = style_config['sentence_count']
        key_sentences = self._select_key_sentences(
            scored_sentences,
            min_count=min_sent,
            max_count=max_sent
        )

        # DECISION POINT 4: Extract key points
        key_points = self._extract_key_points(clean_text, key_sentences)

        # DECISION POINT 5: Format summary based on style
        summary_text = self._format_summary(
            key_sentences,
            key_points,
            style_config,
            title
        )

        # DECISION POINT 6: Apply length constraint if specified
        if max_length and len(summary_text) > max_length:
            summary_text = self._truncate_summary(summary_text, max_length)

        # DECISION POINT 7: Score the summary quality
        quality_score = self._score_summary(summary_text, clean_text, key_points)

        # Generate reasoning explanation
        reasoning = self._explain_summarization(
            chosen_style,
            len(sentences),
            len(key_sentences),
            quality_score
        )

        result = {
            'summary': summary_text,
            'style': chosen_style,
            'key_points': key_points,
            'word_count': len(summary_text.split()),
            'score': quality_score,
            'reasoning': reasoning,
            'metadata': {
                'source_length': len(clean_text),
                'source_sentences': len(sentences),
                'summary_sentences': len(key_sentences),
                'compression_ratio': len(summary_text) / len(clean_text) if clean_text else 0
            }
        }

        if self.debug:
            print(f"[SUMMARIZER AGENT] ✓ Generated {result['word_count']} word summary")
            print(f"[SUMMARIZER AGENT]   Quality score: {quality_score:.2f}")
            print(f"[SUMMARIZER AGENT]   Key points: {len(key_points)}")

        # Record summary history
        self._record_summary(result)

        return result

    def _extract_sentences(self, text: str) -> List[str]:
        """
        Extract sentences from text.

        HEURISTIC: Split on period, exclamation, question mark.
        Filter out very short sentences (< 20 chars).
        """
        # Simple sentence splitting
        sentence_pattern = r'[.!?]+\s+'
        sentences = re.split(sentence_pattern, text)

        # Filter and clean
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

        return sentences

    def _score_sentences(self, sentences: List[str], title: str) -> List[Tuple[str, float]]:
        """
        Score sentences for importance.

        AGENT DECISION: Apply multiple heuristics to rank sentences.
          - Position (earlier sentences often more important)
          - Length (moderate length preferred)
          - Title overlap (sentences mentioning title topics)
          - Keyword density (sentences with important terms)

        Returns:
            List of (sentence, score) tuples
        """
        if not sentences:
            return []

        # Extract title keywords for relevance scoring
        title_keywords = set(self._extract_keywords(title.lower())) if title else set()

        scored = []
        for i, sentence in enumerate(sentences):
            score = 0.0

            # Heuristic 1: Position bias (earlier = more important)
            position_score = 1.0 - (i / len(sentences)) * 0.5
            score += position_score * 0.3

            # Heuristic 2: Length (prefer moderate length)
            length = len(sentence.split())
            if 10 <= length <= 30:
                score += 0.3
            elif length > 30:
                score += 0.15

            # Heuristic 3: Title keyword overlap
            if title_keywords:
                sentence_words = set(self._extract_keywords(sentence.lower()))
                overlap = len(title_keywords & sentence_words)
                score += min(overlap * 0.15, 0.4)

            # Heuristic 4: Contains numbers/data (often important)
            if re.search(r'\d+', sentence):
                score += 0.1

            scored.append((sentence, score))

        # Sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)

        return scored

    def _select_key_sentences(
        self,
        scored_sentences: List[Tuple[str, float]],
        min_count: int,
        max_count: int
    ) -> List[str]:
        """
        Select key sentences based on scores.

        AGENT DECISION: Choose how many sentences to include
        based on quality threshold and count constraints.
        """
        if not scored_sentences:
            return []

        # Take top-scored sentences up to max_count
        selected = scored_sentences[:max_count]

        # Filter out low-quality sentences (score < 0.3) if we have enough
        if len(selected) > min_count:
            selected = [(s, sc) for s, sc in selected if sc >= 0.3]

        # Ensure we have at least min_count
        if len(selected) < min_count:
            selected = scored_sentences[:min_count]

        # Extract just the sentences (drop scores)
        return [s for s, score in selected]

    def _extract_key_points(self, text: str, key_sentences: List[str]) -> List[str]:
        """
        Extract bullet-point key insights.

        AGENT DECISION: Identify the most important standalone points.
        """
        # For now, use key sentences as key points
        # Could be enhanced with more sophisticated extraction
        key_points = []

        for sentence in key_sentences[:5]:  # Limit to top 5
            # Simplify and shorten if needed
            point = sentence.strip()
            if len(point) > 150:
                point = point[:147] + "..."
            key_points.append(point)

        return key_points

    def _format_summary(
        self,
        key_sentences: List[str],
        key_points: List[str],
        style_config: Dict,
        title: str
    ) -> str:
        """
        Format summary based on style configuration.

        AGENT DECISION: Choose how to structure and present the summary.
        """
        summary_parts = []

        # Add title if available
        if title:
            summary_parts.append(f"# {title}\n")

        # Format based on style
        if style_config.get('bullet_points'):
            # Bullet point format
            summary_parts.append("## Key Points:\n")
            for point in key_points:
                summary_parts.append(f"- {point}")

            if len(key_sentences) > len(key_points):
                summary_parts.append("\n## Details:\n")
                remaining = [s for s in key_sentences if s not in key_points]
                summary_parts.append(' '.join(remaining[:3]))
        else:
            # Narrative format
            summary_parts.append(' '.join(key_sentences))

        return '\n'.join(summary_parts)

    def _truncate_summary(self, summary: str, max_length: int) -> str:
        """
        Truncate summary to max length while preserving coherence.

        AGENT DECISION: Choose where to cut while maintaining readability.
        """
        if len(summary) <= max_length:
            return summary

        # Try to cut at sentence boundary
        truncated = summary[:max_length]
        last_period = truncated.rfind('.')
        if last_period > max_length * 0.7:  # If we have a good cut point
            return truncated[:last_period + 1]
        else:
            return truncated[:max_length - 3] + "..."

    def _score_summary(self, summary: str, source_text: str, key_points: List[str]) -> float:
        """
        Score the quality of the generated summary.

        AGENT SELF-EVALUATION: Assess the quality of own output.

        Scoring criteria:
          - Compression ratio (not too short, not too long)
          - Key point coverage
          - Coherence indicators
        """
        score = 0.5  # Base score

        # Criterion 1: Compression ratio
        compression = len(summary) / len(source_text) if source_text else 0
        if 0.1 <= compression <= 0.3:  # Good compression
            score += 0.2
        elif compression < 0.1:  # Too aggressive
            score -= 0.1

        # Criterion 2: Key point coverage
        if len(key_points) >= 3:
            score += 0.2

        # Criterion 3: Not too short
        word_count = len(summary.split())
        if word_count >= 30:
            score += 0.1

        return max(0.0, min(1.0, score))  # Clamp to [0, 1]

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text."""
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that',
            'these', 'those', 'it', 'its'
        }

        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [w for w in words if w not in stopwords and len(w) > 3]

        return keywords

    def _explain_summarization(
        self,
        style: str,
        source_sentences: int,
        summary_sentences: int,
        score: float
    ) -> str:
        """
        Generate explanation of summarization decisions.

        TRANSPARENCY: Good agents explain their reasoning.
        """
        reasoning = f"Applied {style} style summarization. "
        reasoning += f"Analyzed {source_sentences} source sentences, "
        reasoning += f"selected {summary_sentences} key sentences. "

        style_config = self.STYLES[style]
        reasoning += f"Used {style_config['tone']} tone, "
        reasoning += f"focusing on {style_config['focus']}. "

        reasoning += f"Quality score: {score:.2f}."

        return reasoning

    def analyze_trends(
        self,
        texts: List[str],
        topic: str,
        titles: Optional[List[str]] = None
    ) -> Dict[str, any]:
        """
        Analyze trends across multiple texts (Phase 3, Step 26).

        This demonstrates AGENT DECISION-MAKING for trend identification.
        The agent compares multiple sources to find:
          - Common themes
          - Emerging patterns
          - Keyword trends
          - Sentiment shifts
          - Coverage diversity

        Args:
            texts: List of cleaned text strings from multiple sources
            topic: Research topic for context
            titles: Optional list of titles corresponding to texts

        Returns:
            Dictionary containing:
            - trend_summary: Narrative summary of trends
            - common_themes: Most frequent themes across sources
            - emerging_keywords: Keywords gaining prominence
            - diversity_score: How diverse the sources are
            - trend_analysis: Detailed analysis

        Example:
            >>> summarizer = SummarizerAgent()
            >>> texts = [text1, text2, text3]
            >>> result = summarizer.analyze_trends(texts, "AI research")
            >>> print(result['trend_summary'])
            >>> print(result['common_themes'])

        PHASE 3 EXTENSION (Step 26):
        -----------------------------
        This adds TREND ANALYSIS MODE — going beyond single-document
        summarization to identify patterns across multiple sources.

        TEACHING NOTE:
        --------------
        This demonstrates advanced AGENT behavior: comparative analysis.
        The agent doesn't just process each text independently — it
        synthesizes insights across multiple sources to identify trends.

        Compare this to simple summarization:
          - Summarization: "What does THIS say?"
          - Trend Analysis: "What are ALL of these saying TOGETHER?"

        This is higher-level intelligence — seeing the forest, not just trees.
        """
        if self.debug:
            print(f"\n[SUMMARIZER AGENT] Trend analysis across {len(texts)} sources")
            print(f"[SUMMARIZER AGENT] Topic: {topic}")

        if not texts:
            return {
                'trend_summary': "No texts provided for analysis.",
                'common_themes': [],
                'emerging_keywords': [],
                'diversity_score': 0.0,
                'trend_analysis': {}
            }

        # DECISION POINT 1: Extract keywords from all sources
        all_keywords = []
        text_keywords = []
        for text in texts:
            keywords = self._extract_keywords(text)
            text_keywords.append(keywords)
            all_keywords.extend(keywords)

        # DECISION POINT 2: Identify common themes (most frequent keywords)
        keyword_freq = Counter(all_keywords)
        common_themes = [word for word, count in keyword_freq.most_common(10)]

        # DECISION POINT 3: Identify emerging keywords (appear in later sources)
        emerging_keywords = self._identify_emerging_keywords(text_keywords)

        # DECISION POINT 4: Calculate diversity across sources
        from ..utils import scoring
        diversity_score = scoring.score_diversity(texts)

        # DECISION POINT 5: Identify consensus vs. divergence
        consensus_points = self._find_consensus(texts, common_themes)

        # DECISION POINT 6: Generate trend narrative
        trend_summary = self._generate_trend_narrative(
            topic=topic,
            num_sources=len(texts),
            common_themes=common_themes,
            emerging_keywords=emerging_keywords,
            diversity_score=diversity_score,
            consensus_points=consensus_points
        )

        # Compile trend analysis data
        trend_analysis = {
            'num_sources': len(texts),
            'total_keywords': len(all_keywords),
            'unique_keywords': len(set(all_keywords)),
            'keyword_frequency': dict(keyword_freq.most_common(20)),
            'consensus_points': consensus_points,
            'divergence_areas': self._find_divergence(texts, text_keywords)
        }

        result = {
            'trend_summary': trend_summary,
            'common_themes': common_themes,
            'emerging_keywords': emerging_keywords,
            'diversity_score': diversity_score,
            'trend_analysis': trend_analysis,
            'metadata': {
                'num_sources': len(texts),
                'avg_source_length': sum(len(t) for t in texts) / len(texts),
                'topic': topic
            }
        }

        if self.debug:
            print(f"[SUMMARIZER AGENT] ✓ Trend analysis complete")
            print(f"  Common themes: {len(common_themes)}")
            print(f"  Emerging keywords: {len(emerging_keywords)}")
            print(f"  Diversity score: {diversity_score:.2f}")

        return result

    def _identify_emerging_keywords(self, text_keywords: List[List[str]]) -> List[str]:
        """
        Identify keywords that appear more in later sources (emerging trends).

        AGENT HEURISTIC: Compare first half vs. second half of sources.
        Keywords appearing more frequently in later sources are "emerging".

        Args:
            text_keywords: List of keyword lists, one per text in order

        Returns:
            List of emerging keywords
        """
        if len(text_keywords) < 2:
            return []

        # Split into first half and second half
        mid_point = len(text_keywords) // 2
        first_half = text_keywords[:mid_point]
        second_half = text_keywords[mid_point:]

        # Count keywords in each half
        first_freq = Counter([kw for keywords in first_half for kw in keywords])
        second_freq = Counter([kw for keywords in second_half for kw in keywords])

        # Find keywords more prominent in second half
        emerging = []
        for keyword in second_freq:
            first_count = first_freq.get(keyword, 0)
            second_count = second_freq[keyword]

            # Emerging if appears at least 2x more in second half
            if second_count >= first_count * 2 and second_count >= 2:
                emerging.append(keyword)

        return sorted(emerging, key=lambda k: second_freq[k], reverse=True)[:5]

    def _find_consensus(self, texts: List[str], common_themes: List[str]) -> List[str]:
        """
        Find points of consensus across sources.

        AGENT DECISION: Identify sentences/ideas that appear across multiple sources.

        Args:
            texts: List of text strings
            common_themes: List of common keywords

        Returns:
            List of consensus points (sentences appearing in multiple sources)
        """
        consensus_points = []

        # For each common theme, find sentences mentioning it
        for theme in common_themes[:5]:  # Top 5 themes
            theme_sentences = []

            for text in texts:
                sentences = self._extract_sentences(text)
                # Find sentences containing this theme
                for sentence in sentences:
                    if theme.lower() in sentence.lower():
                        theme_sentences.append(sentence)
                        break  # One per source

            # If multiple sources mention this theme, it's a consensus point
            if len(theme_sentences) >= len(texts) * 0.5:  # 50%+ of sources
                # Pick the clearest/shortest sentence
                best_sentence = min(theme_sentences, key=len)
                if len(best_sentence) < 200:
                    consensus_points.append(best_sentence)

        return consensus_points[:5]  # Top 5 consensus points

    def _find_divergence(self, texts: List[str], text_keywords: List[List[str]]) -> List[str]:
        """
        Find areas where sources diverge (unique perspectives).

        AGENT DECISION: Identify keywords that are unique to individual sources.

        Args:
            texts: List of text strings
            text_keywords: List of keyword lists

        Returns:
            List of divergence descriptions
        """
        divergence_areas = []

        # Find keywords unique to each source
        for i, keywords in enumerate(text_keywords):
            # Find keywords not in other sources
            other_keywords = set()
            for j, other_kw in enumerate(text_keywords):
                if i != j:
                    other_keywords.update(other_kw)

            unique_keywords = [kw for kw in keywords if kw not in other_keywords]

            if len(unique_keywords) >= 3:
                # This source has unique perspective
                divergence_areas.append(
                    f"Source {i+1} uniquely discusses: {', '.join(unique_keywords[:3])}"
                )

        return divergence_areas[:5]

    def _generate_trend_narrative(
        self,
        topic: str,
        num_sources: int,
        common_themes: List[str],
        emerging_keywords: List[str],
        diversity_score: float,
        consensus_points: List[str]
    ) -> str:
        """
        Generate narrative summary of trends.

        AGENT DECISION: Synthesize findings into coherent narrative.

        Args:
            topic: Research topic
            num_sources: Number of sources analyzed
            common_themes: Common keywords
            emerging_keywords: Emerging keywords
            diversity_score: Source diversity score
            consensus_points: Consensus sentences

        Returns:
            Narrative string describing trends
        """
        narrative_parts = []

        # Opening
        narrative_parts.append(f"# Trend Analysis: {topic}\n")
        narrative_parts.append(f"Analyzed {num_sources} sources to identify patterns and trends.\n")

        # Diversity assessment
        if diversity_score > 0.7:
            narrative_parts.append(
                "**Source Diversity**: High — sources cover diverse perspectives and topics."
            )
        elif diversity_score > 0.4:
            narrative_parts.append(
                "**Source Diversity**: Moderate — sources share some common ground with varied details."
            )
        else:
            narrative_parts.append(
                "**Source Diversity**: Low — sources are highly similar and overlapping."
            )

        # Common themes
        narrative_parts.append("\n## Common Themes:\n")
        if common_themes:
            narrative_parts.append("The following themes appear consistently across sources:")
            for i, theme in enumerate(common_themes[:5], 1):
                narrative_parts.append(f"{i}. **{theme.capitalize()}**")
        else:
            narrative_parts.append("No strong common themes identified.")

        # Emerging trends
        if emerging_keywords:
            narrative_parts.append("\n## Emerging Trends:\n")
            narrative_parts.append(
                "These topics are gaining prominence in more recent sources:"
            )
            for keyword in emerging_keywords:
                narrative_parts.append(f"- {keyword.capitalize()}")

        # Consensus points
        if consensus_points:
            narrative_parts.append("\n## Points of Consensus:\n")
            for point in consensus_points:
                narrative_parts.append(f"- {point[:150]}...")

        # Conclusion
        narrative_parts.append("\n## Summary:\n")
        if common_themes and emerging_keywords:
            narrative_parts.append(
                f"The research on {topic} shows convergence around {common_themes[0]}, "
                f"with emerging focus on {emerging_keywords[0] if emerging_keywords else 'new developments'}."
            )
        elif common_themes:
            narrative_parts.append(
                f"The research consistently emphasizes {common_themes[0]}, "
                f"though sources vary in their specific approaches."
            )
        else:
            narrative_parts.append(
                f"The research on {topic} shows significant diversity with "
                f"limited overlap between sources."
            )

        return '\n'.join(narrative_parts)

    def _record_summary(self, result: Dict):
        """Record summarization in history for debugging."""
        self._summary_history.append({
            'summary': result['summary'],
            'style': result['style'],
            'score': result['score'],
            'word_count': result['word_count'],
            'timestamp': datetime.now()
        })

    def get_summary_stats(self) -> Dict:
        """
        Get statistics about summarization history.

        DEBUGGING HELPER: Analyze agent performance over time.
        """
        if not self._summary_history:
            return {
                'total_summaries': 0,
                'avg_quality_score': 0.0,
                'avg_word_count': 0.0
            }

        total = len(self._summary_history)
        scores = [s['score'] for s in self._summary_history]
        word_counts = [s['word_count'] for s in self._summary_history]

        # Count style distribution
        styles = [s['style'] for s in self._summary_history]
        style_distribution = dict(Counter(styles))

        return {
            'total_summaries': total,
            'avg_quality_score': sum(scores) / total,
            'min_quality_score': min(scores),
            'max_quality_score': max(scores),
            'avg_word_count': sum(word_counts) / total,
            'style_distribution': style_distribution
        }
