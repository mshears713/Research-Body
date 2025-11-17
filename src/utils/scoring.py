"""
SCORING UTILITIES
==================

PURPOSE:
--------
Shared helper functions for scoring content quality, relevance,
and other metrics. Used throughout the pipeline to assess
the value of fetched and processed content.

RESPONSIBILITIES:
-----------------
  1. Calculate relevance scores (keyword matching)
  2. Assess content quality (readability, completeness)
  3. Compute diversity metrics (uniqueness vs. overlap)
  4. Score summary quality (coverage, coherence)
  5. Generate composite scores for ranking

TEACHING NOTES:
---------------
These are SCORING FUNCTIONS — they take content and return
numerical assessments. They're used by AGENTS to make decisions
("Is this summary good enough?" "Which source is most relevant?")
but the functions themselves are deterministic calculations.

This demonstrates the symbiosis between TOOLS (scoring functions)
and AGENTS (decision-makers that use those scores).

FUTURE EXTENSIONS:
------------------
  • Machine learning-based quality scoring
  • Domain-specific relevance models
  • User feedback integration (learning from ratings)
  • Comparative scoring across multiple sources

DEBUGGING TIPS:
---------------
  • Validate score ranges (0-1, 0-100, etc.)
  • Test with known good/bad examples
  • Monitor score distributions over time
  • Ensure scores correlate with human judgments
"""

import re
from typing import List, Set
from collections import Counter


def score_keyword_relevance(text: str, keywords: List[str]) -> float:
    """
    Score text relevance based on keyword presence.

    Calculates what percentage of keywords appear in the text.

    Args:
        text: Text to score
        keywords: List of target keywords

    Returns:
        Relevance score from 0.0 to 1.0

    Example:
        >>> score_keyword_relevance("AI and ML are cool", ["ai", "ml", "robots"])
        0.67  # 2 out of 3 keywords present

    TEACHING NOTE:
    --------------
    This is a simple DETERMINISTIC SCORING FUNCTION.
    The Planner or Summarizer AGENT uses this score to make decisions.
    """
    if not keywords:
        return 0.0

    text_lower = text.lower()
    keywords_lower = [k.lower() for k in keywords]

    # Count how many keywords are present
    matches = sum(1 for keyword in keywords_lower if keyword in text_lower)

    # Return percentage of keywords found
    return matches / len(keywords)


def score_text_quality(text: str) -> float:
    """
    Score overall text quality based on heuristics.

    Considers:
      - Length (too short = low quality)
      - Sentence variety (repeated sentences = low quality)
      - Word variety (vocabulary richness)
      - Capitalization (all caps = low quality)

    Args:
        text: Text to score

    Returns:
        Quality score from 0.0 to 1.0

    Example:
        >>> score_text_quality("This is good text. Varied sentences.")
        0.75  # Reasonably good

    TEACHING NOTE:
    --------------
    This combines multiple heuristics into a composite score.
    Each heuristic is deterministic, so the composite is too.
    """
    if not text or len(text) < 20:
        return 0.0

    score = 0.5  # Base score

    # Criterion 1: Length (prefer 100-5000 characters)
    if 100 <= len(text) <= 5000:
        score += 0.15
    elif len(text) > 5000:
        score += 0.10

    # Criterion 2: Not all uppercase (screaming = bad quality)
    uppercase_ratio = sum(1 for c in text if c.isupper()) / len(text)
    if uppercase_ratio < 0.3:  # Less than 30% uppercase is good
        score += 0.15

    # Criterion 3: Sentence variety (not all same length)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if len(sentences) >= 2:
        sentence_lengths = [len(s) for s in sentences]
        avg_length = sum(sentence_lengths) / len(sentence_lengths)
        variance = sum((l - avg_length) ** 2 for l in sentence_lengths) / len(sentence_lengths)
        if variance > 100:  # Some variety in sentence length
            score += 0.10

    # Criterion 4: Word variety (vocabulary richness)
    words = text.lower().split()
    if len(words) > 0:
        unique_words = len(set(words))
        word_variety = unique_words / len(words)
        if word_variety > 0.5:  # More than 50% unique words
            score += 0.10

    return min(1.0, score)  # Cap at 1.0


def score_readability(text: str) -> float:
    """
    Score text readability (simplified version).

    Based on average sentence and word length.
    Shorter sentences and words = higher readability.

    Args:
        text: Text to score

    Returns:
        Readability score from 0.0 (hard) to 1.0 (easy)

    Example:
        >>> score_readability("Short words. Easy to read.")
        0.85  # High readability

    TEACHING NOTE:
    --------------
    This is a simplified Flesch reading ease approximation.
    For production, use textstat library for accurate scores.
    """
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return 0.0

    words = text.split()
    if not words:
        return 0.0

    # Calculate averages
    avg_sentence_length = len(words) / len(sentences)
    avg_word_length = sum(len(word) for word in words) / len(words)

    # Score based on averages (simpler = better)
    # Ideal: 15-20 words per sentence, 4-6 letters per word
    sentence_score = 1.0 - min(abs(avg_sentence_length - 17.5) / 50, 1.0)
    word_score = 1.0 - min(abs(avg_word_length - 5) / 10, 1.0)

    # Combine scores
    readability = (sentence_score + word_score) / 2

    return max(0.0, min(1.0, readability))


def score_diversity(texts: List[str]) -> float:
    """
    Score diversity across multiple texts.

    Measures how different the texts are from each other.
    High diversity = good (not redundant).

    Args:
        texts: List of text strings to compare

    Returns:
        Diversity score from 0.0 (identical) to 1.0 (completely different)

    Example:
        >>> score_diversity(["AI is cool", "ML is great", "Robots are nice"])
        0.80  # High diversity

    TEACHING NOTE:
    --------------
    This uses Jaccard distance on word sets to measure diversity.
    Useful for the Planner AGENT to avoid selecting redundant sources.
    """
    if len(texts) < 2:
        return 1.0  # Single text is maximally "diverse"

    # Convert each text to a set of words
    word_sets = []
    for text in texts:
        words = set(text.lower().split())
        word_sets.append(words)

    # Calculate pairwise Jaccard distances
    distances = []
    for i in range(len(word_sets)):
        for j in range(i + 1, len(word_sets)):
            set_i, set_j = word_sets[i], word_sets[j]

            # Jaccard distance = 1 - (intersection / union)
            intersection = len(set_i & set_j)
            union = len(set_i | set_j)

            if union > 0:
                distance = 1.0 - (intersection / union)
                distances.append(distance)

    # Average distance = diversity score
    if distances:
        return sum(distances) / len(distances)
    else:
        return 0.0


def score_summary_coverage(summary: str, source: str) -> float:
    """
    Score how well a summary covers the source content.

    Measures keyword overlap between summary and source.

    Args:
        summary: Summary text
        source: Original source text

    Returns:
        Coverage score from 0.0 to 1.0

    Example:
        >>> score_summary_coverage("AI is cool", "AI systems are cool and useful")
        0.75  # Good coverage

    TEACHING NOTE:
    --------------
    This helps the Summarizer AGENT self-evaluate its output.
    The agent can decide: "Is this summary covering enough?"
    """
    # Extract keywords from source
    source_words = set(source.lower().split())

    # Remove common stopwords
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were'
    }
    source_words = {w for w in source_words if w not in stopwords and len(w) > 3}

    if not source_words:
        return 0.0

    # Count how many source keywords appear in summary
    summary_lower = summary.lower()
    covered_words = sum(1 for word in source_words if word in summary_lower)

    # Coverage = percentage of source keywords in summary
    coverage = covered_words / len(source_words)

    return min(1.0, coverage)


def score_composite(scores: List[float], weights: List[float] = None) -> float:
    """
    Combine multiple scores into a weighted composite.

    Args:
        scores: List of individual scores (0.0 to 1.0)
        weights: Optional weights for each score (defaults to equal weight)

    Returns:
        Composite score from 0.0 to 1.0

    Example:
        >>> score_composite([0.8, 0.6, 0.9], weights=[2, 1, 1])
        0.775  # Weighted average

    TEACHING NOTE:
    --------------
    This allows combining multiple scoring dimensions.
    Agents use this to make holistic quality judgments.
    """
    if not scores:
        return 0.0

    if weights is None:
        weights = [1.0] * len(scores)

    if len(weights) != len(scores):
        raise ValueError("Number of weights must match number of scores")

    # Weighted average
    weighted_sum = sum(score * weight for score, weight in zip(scores, weights))
    total_weight = sum(weights)

    return weighted_sum / total_weight if total_weight > 0 else 0.0
