"""
CROSS-MISSION TREND ANALYSIS LIBRARY
=====================================

TEACHING PURPOSE:
-----------------
This module demonstrates how to analyze trends across multiple research
missions to identify patterns, recurring themes, and knowledge evolution.

KEY CONCEPTS:
-------------
  • Aggregating data across missions
  • Temporal trend detection
  • Keyword frequency analysis
  • Quality metrics over time
  • Cross-domain pattern recognition

USE CASES:
----------
  1. Track how research topics evolve over time
  2. Identify emerging themes across domains
  3. Compare quality of sources by domain
  4. Detect seasonal patterns in research areas
  5. Recommend related missions based on similarity

TEACHING NOTE:
--------------
This library processes HISTORICAL DATA (from logged missions)
to extract insights. It's a powerful example of "meta-analysis"
where we analyze our own research process.

FUTURE EXTENSIONS:
------------------
  • Machine learning for trend prediction
  • Anomaly detection in research patterns
  • Automated research gap identification
  • Citation network analysis
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import re


class TrendAnalyzer:
    """
    Cross-Mission Trend Analysis Engine
    ====================================

    Analyzes patterns across multiple completed missions to identify:
      • Popular research topics
      • Quality trends over time
      • Keyword evolution
      • Domain-specific patterns
      • Source reliability metrics

    TEACHING NOTE:
    --------------
    This is a UTILITY (not an agent or tool) because it performs
    deterministic analysis on historical data. No decisions, just
    computation and aggregation.
    """

    def __init__(self, mission_history: List[Dict], debug: bool = False):
        """
        Initialize trend analyzer with mission history.

        Args:
            mission_history: List of completed mission records
            debug: Enable detailed logging

        TEACHING NOTE:
        --------------
        Mission history comes from LoggerTool. This demonstrates
        how different system components work together:
          LoggerTool → records missions
          TrendAnalyzer → analyzes recorded missions
        """
        self.missions = mission_history
        self.debug = debug

    def analyze_keyword_trends(self, time_window_days: int = 30) -> Dict:
        """
        Analyze keyword frequency trends over time.

        Returns most popular keywords in recent missions and
        how their frequency is changing.

        Args:
            time_window_days: Compare recent period to previous period

        Returns:
            Dict with trending_up, trending_down, stable keywords

        Example:
            >>> analyzer = TrendAnalyzer(mission_history)
            >>> trends = analyzer.analyze_keyword_trends(30)
            >>> print(trends['trending_up'])
            [('quantum computing', 0.45), ('wildfire detection', 0.32)]

        TEACHING NOTE:
        --------------
        Trend detection algorithm:
          1. Split missions into recent vs previous time windows
          2. Count keyword frequency in each window
          3. Calculate relative change
          4. Categorize as trending up/down/stable
        """
        cutoff_date = datetime.now() - timedelta(days=time_window_days)
        comparison_date = cutoff_date - timedelta(days=time_window_days)

        # Divide missions into time periods
        recent_missions = [m for m in self.missions
                          if m.get('completed_at', datetime.min) >= cutoff_date]
        previous_missions = [m for m in self.missions
                           if comparison_date <= m.get('completed_at', datetime.min) < cutoff_date]

        # Extract keywords from missions
        recent_keywords = self._extract_keywords(recent_missions)
        previous_keywords = self._extract_keywords(previous_missions)

        # Calculate trends
        trends = {
            'trending_up': [],
            'trending_down': [],
            'stable': [],
            'new': []  # Keywords that appeared only in recent period
        }

        all_keywords = set(recent_keywords.keys()) | set(previous_keywords.keys())

        for keyword in all_keywords:
            recent_count = recent_keywords.get(keyword, 0)
            previous_count = previous_keywords.get(keyword, 0)

            # Normalize by mission count
            recent_freq = recent_count / len(recent_missions) if recent_missions else 0
            previous_freq = previous_count / len(previous_missions) if previous_missions else 0

            if previous_freq == 0 and recent_freq > 0:
                trends['new'].append((keyword, recent_freq))
            elif previous_freq > 0:
                change_rate = (recent_freq - previous_freq) / previous_freq

                if change_rate > 0.2:  # 20% increase
                    trends['trending_up'].append((keyword, change_rate))
                elif change_rate < -0.2:  # 20% decrease
                    trends['trending_down'].append((keyword, change_rate))
                else:
                    trends['stable'].append((keyword, recent_freq))

        # Sort by magnitude
        for category in trends:
            trends[category] = sorted(trends[category], key=lambda x: abs(x[1]), reverse=True)

        if self.debug:
            print(f"\n[TREND ANALYSIS] Keyword Trends ({time_window_days} days)")
            print(f"  Trending up: {len(trends['trending_up'])} keywords")
            print(f"  Trending down: {len(trends['trending_down'])} keywords")
            print(f"  New keywords: {len(trends['new'])}")

        return trends

    def analyze_quality_trends(self) -> Dict:
        """
        Analyze quality score trends over time.

        Tracks how average mission quality changes over time,
        potentially indicating learning and improvement.

        Returns:
            Dict with quality metrics by time period

        TEACHING NOTE:
        --------------
        This can reveal:
          • Source quality improving as we learn better URLs
          • Scraping effectiveness over time
          • Summary quality trends
        """
        quality_by_month = defaultdict(list)

        for mission in self.missions:
            if 'metadata' not in mission or 'scores' not in mission['metadata']:
                continue

            # Extract month
            completed = mission.get('completed_at')
            if not completed:
                continue

            month_key = f"{completed.year}-{completed.month:02d}"

            # Get average quality score
            scores = mission['metadata']['scores']
            if scores:
                avg_score = sum(scores.values()) / len(scores)
                quality_by_month[month_key].append(avg_score)

        # Calculate statistics per month
        quality_stats = {}
        for month, scores in sorted(quality_by_month.items()):
            quality_stats[month] = {
                'avg_quality': sum(scores) / len(scores),
                'min_quality': min(scores),
                'max_quality': max(scores),
                'mission_count': len(scores)
            }

        if self.debug:
            print(f"\n[TREND ANALYSIS] Quality Trends")
            for month, stats in list(quality_stats.items())[-3:]:
                print(f"  {month}: avg={stats['avg_quality']:.2f}, missions={stats['mission_count']}")

        return quality_stats

    def find_similar_missions(self, topic: str, top_k: int = 5) -> List[Dict]:
        """
        Find historically similar missions to a given topic.

        Uses keyword overlap to identify related past research.

        Args:
            topic: Research topic to find similar missions for
            top_k: Number of similar missions to return

        Returns:
            List of similar missions with similarity scores

        Example:
            >>> similar = analyzer.find_similar_missions("quantum computing", top_k=3)
            >>> for mission in similar:
            >>>     print(f"{mission['topic']}: {mission['similarity']:.2f}")

        TEACHING NOTE:
        --------------
        Simple similarity metric: keyword overlap.
        Could be enhanced with:
          • TF-IDF weighting
          • Word embeddings (word2vec, BERT)
          • Topic modeling (LDA)
        """
        topic_keywords = set(self._tokenize(topic.lower()))

        similarities = []

        for mission in self.missions:
            mission_topic = mission.get('topic', '')
            mission_keywords = set(self._tokenize(mission_topic.lower()))

            # Calculate Jaccard similarity
            if not topic_keywords or not mission_keywords:
                continue

            intersection = len(topic_keywords & mission_keywords)
            union = len(topic_keywords | mission_keywords)
            similarity = intersection / union if union > 0 else 0

            if similarity > 0:
                similarities.append({
                    'mission_id': mission.get('mission_id'),
                    'topic': mission_topic,
                    'similarity': similarity,
                    'completed_at': mission.get('completed_at'),
                    'status': mission.get('status')
                })

        # Sort by similarity and return top K
        similarities.sort(key=lambda x: x['similarity'], reverse=True)

        if self.debug:
            print(f"\n[TREND ANALYSIS] Similar Missions to: {topic}")
            for i, sim in enumerate(similarities[:top_k], 1):
                print(f"  {i}. {sim['topic'][:50]}... (similarity: {sim['similarity']:.2f})")

        return similarities[:top_k]

    def analyze_domain_patterns(self) -> Dict:
        """
        Analyze patterns by research domain.

        Groups missions by domain and computes:
          • Average quality scores
          • Common keywords
          • Success rates
          • Source reliability

        Returns:
            Dict mapping domain → statistics

        TEACHING NOTE:
        --------------
        This helps identify which domains:
          • Have higher quality sources
          • Are researched more frequently
          • Have better success rates
        """
        domains = defaultdict(lambda: {
            'missions': [],
            'avg_quality': 0.0,
            'success_rate': 0.0,
            'common_keywords': Counter()
        })

        for mission in self.missions:
            # Extract domain from metadata or infer from topic
            domain = mission.get('metadata', {}).get('domain', 'general')

            domains[domain]['missions'].append(mission)

            # Aggregate quality scores
            scores = mission.get('metadata', {}).get('scores', {})
            if scores:
                avg_score = sum(scores.values()) / len(scores)
                domains[domain]['avg_quality'] += avg_score

            # Track success
            if mission.get('status') == 'completed':
                domains[domain]['success_rate'] += 1

            # Collect keywords
            keywords = self._extract_keywords([mission])
            domains[domain]['common_keywords'].update(keywords)

        # Calculate final statistics
        domain_stats = {}
        for domain, data in domains.items():
            mission_count = len(data['missions'])
            if mission_count > 0:
                domain_stats[domain] = {
                    'mission_count': mission_count,
                    'avg_quality': data['avg_quality'] / mission_count,
                    'success_rate': data['success_rate'] / mission_count,
                    'top_keywords': data['common_keywords'].most_common(10)
                }

        if self.debug:
            print(f"\n[TREND ANALYSIS] Domain Patterns")
            for domain, stats in domain_stats.items():
                print(f"  {domain}:")
                print(f"    Missions: {stats['mission_count']}")
                print(f"    Avg quality: {stats['avg_quality']:.2f}")
                print(f"    Success rate: {stats['success_rate']*100:.1f}%")

        return domain_stats

    def detect_emerging_topics(self, min_mentions: int = 3) -> List[Tuple[str, int]]:
        """
        Detect emerging research topics from recent missions.

        Identifies keywords that:
          • Appear frequently in recent missions
          • Weren't common in older missions
          • Meet minimum mention threshold

        Args:
            min_mentions: Minimum times keyword must appear

        Returns:
            List of (keyword, mention_count) for emerging topics

        TEACHING NOTE:
        --------------
        This is "trend mining" - finding signals of emerging
        research areas before they become mainstream.
        """
        # Split into recent (last 30 days) and historical
        cutoff = datetime.now() - timedelta(days=30)

        recent = [m for m in self.missions
                 if m.get('completed_at', datetime.min) >= cutoff]
        historical = [m for m in self.missions
                     if m.get('completed_at', datetime.min) < cutoff]

        recent_keywords = self._extract_keywords(recent)
        historical_keywords = self._extract_keywords(historical)

        # Find keywords that are new or significantly more common
        emerging = []

        for keyword, recent_count in recent_keywords.items():
            if recent_count < min_mentions:
                continue

            historical_count = historical_keywords.get(keyword, 0)

            # Emerging if: new OR 3x more common than before
            if historical_count == 0:
                emerging.append((keyword, recent_count))
            elif recent_count / len(recent) > 3 * (historical_count / max(len(historical), 1)):
                emerging.append((keyword, recent_count))

        # Sort by mention count
        emerging.sort(key=lambda x: x[1], reverse=True)

        if self.debug:
            print(f"\n[TREND ANALYSIS] Emerging Topics")
            for keyword, count in emerging[:10]:
                print(f"  {keyword}: {count} recent mentions")

        return emerging

    def _extract_keywords(self, missions: List[Dict]) -> Counter:
        """Extract and count keywords from mission topics."""
        keywords = Counter()

        for mission in missions:
            topic = mission.get('topic', '')
            tokens = self._tokenize(topic.lower())

            # Filter stopwords and short tokens
            filtered = [t for t in tokens
                       if len(t) > 3 and t not in self._get_stopwords()]

            keywords.update(filtered)

        return keywords

    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization (split on non-alphanumeric)."""
        return re.findall(r'\b\w+\b', text)

    def _get_stopwords(self) -> set:
        """Basic English stopwords."""
        return {
            'the', 'and', 'for', 'with', 'from', 'this', 'that',
            'are', 'was', 'were', 'been', 'have', 'has', 'had',
            'will', 'would', 'could', 'should', 'about', 'into'
        }

    def generate_trend_report(self) -> str:
        """
        Generate comprehensive trend analysis report.

        Returns:
            Markdown-formatted report with all trend analyses

        TEACHING NOTE:
        --------------
        This demonstrates how to package analysis results
        into a human-readable report. Perfect for sharing
        insights with stakeholders.
        """
        report = ["# Cross-Mission Trend Analysis Report\n"]
        report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        report.append(f"**Missions Analyzed**: {len(self.missions)}\n")

        # Keyword trends
        report.append("\n## 📈 Keyword Trends (Last 30 Days)\n")
        keyword_trends = self.analyze_keyword_trends(30)

        report.append("\n### Trending Up\n")
        for keyword, change in keyword_trends['trending_up'][:5]:
            report.append(f"- **{keyword}**: +{change*100:.1f}%\n")

        report.append("\n### New Topics\n")
        for keyword, freq in keyword_trends['new'][:5]:
            report.append(f"- {keyword}\n")

        # Emerging topics
        report.append("\n## 🌟 Emerging Topics\n")
        emerging = self.detect_emerging_topics()
        for keyword, count in emerging[:10]:
            report.append(f"- {keyword} ({count} mentions)\n")

        # Domain patterns
        report.append("\n## 🎯 Domain Analysis\n")
        domains = self.analyze_domain_patterns()
        for domain, stats in sorted(domains.items(), key=lambda x: x[1]['mission_count'], reverse=True):
            report.append(f"\n### {domain.title()}\n")
            report.append(f"- Missions: {stats['mission_count']}\n")
            report.append(f"- Avg Quality: {stats['avg_quality']:.2f}/1.0\n")
            report.append(f"- Success Rate: {stats['success_rate']*100:.1f}%\n")
            report.append(f"- Top Keywords: {', '.join([k for k, _ in stats['top_keywords'][:5]])}\n")

        # Quality trends
        report.append("\n## 📊 Quality Trends\n")
        quality = self.analyze_quality_trends()
        for month, stats in list(quality.items())[-6:]:
            report.append(f"- **{month}**: {stats['avg_quality']:.2f} avg ({stats['mission_count']} missions)\n")

        return ''.join(report)


# Convenience function
def analyze_trends(mission_history: List[Dict], debug: bool = False) -> TrendAnalyzer:
    """
    Create trend analyzer from mission history.

    Example:
        >>> from src.tools.logger_tool import LoggerTool
        >>> logger = LoggerTool()
        >>> history = logger.get_all_missions()
        >>> analyzer = analyze_trends(history, debug=True)
        >>> report = analyzer.generate_trend_report()
        >>> print(report)
    """
    return TrendAnalyzer(mission_history, debug=debug)
