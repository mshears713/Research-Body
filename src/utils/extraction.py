"""
TEXT EXTRACTION UTILITIES
==========================

PURPOSE:
--------
Shared helper functions for extracting structured information
from raw text. Used by the Cleaner Tool and Summarizer Agent.

RESPONSIBILITIES:
-----------------
  1. Extract keywords and key phrases
  2. Identify named entities (people, places, organizations)
  3. Extract dates and numbers
  4. Identify section headings and structure
  5. Extract citations and references

TEACHING NOTES:
---------------
These are PATTERN-MATCHING UTILITIES — they use regex and heuristics
to find specific types of information in text. They're deterministic
but more complex than simple string operations.

The Summarizer AGENT uses these utilities to identify important
content, but makes the decision about WHICH extractions to include
in the final summary.

FUTURE EXTENSIONS:
------------------
  • NLP-based entity extraction
  • Relationship extraction (subject-verb-object)
  • Coreference resolution
  • Domain-specific extraction (chemical formulas, gene names)

DEBUGGING TIPS:
---------------
  • Test extraction patterns against diverse text samples
  • Monitor precision vs. recall tradeoffs
  • Log extraction failures for pattern refinement
"""

import re
from typing import List, Dict, Tuple
from collections import Counter


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract keywords from text using frequency analysis.

    Simple keyword extraction based on word frequency,
    filtering out common stopwords.

    Args:
        text: Text to extract keywords from
        max_keywords: Maximum number of keywords to return

    Returns:
        List of keywords sorted by importance

    Example:
        >>> extract_keywords("AI systems use AI for analysis")
        ['ai', 'systems', 'analysis']

    TEACHING NOTE:
    --------------
    This is a DETERMINISTIC HEURISTIC. Not ML-based, just frequency counting.
    """
    # Common English stopwords
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that',
        'these', 'those', 'it', 'its', 'they', 'them', 'their', 'we', 'us',
        'our', 'you', 'your', 'he', 'him', 'his', 'she', 'her', 'who', 'what',
        'when', 'where', 'why', 'how', 'all', 'each', 'every', 'some', 'any'
    }

    # Extract words (alphanumeric only)
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())

    # Filter stopwords
    words = [w for w in words if w not in stopwords]

    # Count frequencies
    word_counts = Counter(words)

    # Get top keywords
    top_keywords = [word for word, count in word_counts.most_common(max_keywords)]

    return top_keywords


def extract_numbers(text: str) -> List[float]:
    """
    Extract all numbers from text.

    Finds integers and decimals, including those with commas.

    Args:
        text: Text to extract numbers from

    Returns:
        List of numbers as floats

    Example:
        >>> extract_numbers("Costs $1,234.56 or 789 units")
        [1234.56, 789.0]
    """
    # Pattern for numbers with optional commas and decimals
    number_pattern = r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b'
    number_strings = re.findall(number_pattern, text)

    # Convert to floats, removing commas
    numbers = [float(n.replace(',', '')) for n in number_strings]

    return numbers


def extract_dates(text: str) -> List[str]:
    """
    Extract date-like strings from text.

    Finds common date patterns (simplified version).

    Args:
        text: Text to extract dates from

    Returns:
        List of date strings

    Example:
        >>> extract_dates("Meeting on Jan 15, 2024 or 03/20/2024")
        ['Jan 15, 2024', '03/20/2024']

    TEACHING NOTE:
    --------------
    This is a simple regex-based extractor. For production,
    use a library like dateutil.parser for robust date parsing.
    """
    date_patterns = [
        r'\b[A-Z][a-z]{2,8}\s+\d{1,2},?\s+\d{4}\b',  # Jan 15, 2024
        r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',              # 03/20/2024
        r'\b\d{4}-\d{2}-\d{2}\b',                     # 2024-03-20
    ]

    dates = []
    for pattern in date_patterns:
        dates.extend(re.findall(pattern, text))

    return dates


def extract_urls(text: str) -> List[str]:
    """
    Extract URLs from text.

    Finds http, https, and www URLs.

    Args:
        text: Text to extract URLs from

    Returns:
        List of URL strings

    Example:
        >>> extract_urls("Visit https://example.com or www.test.com")
        ['https://example.com', 'www.test.com']
    """
    # URL pattern (simplified)
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+|www\.[^\s<>"{}|\\^`\[\]]+'
    urls = re.findall(url_pattern, text)

    return urls


def extract_emails(text: str) -> List[str]:
    """
    Extract email addresses from text.

    Args:
        text: Text to extract emails from

    Returns:
        List of email addresses

    Example:
        >>> extract_emails("Contact user@example.com or admin@test.org")
        ['user@example.com', 'admin@test.org']
    """
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)

    return emails


def extract_capitalized_phrases(text: str, min_length: int = 2) -> List[str]:
    """
    Extract capitalized phrases (potential named entities).

    Finds sequences of capitalized words, which often indicate
    proper nouns, names, organizations, etc.

    Args:
        text: Text to extract from
        min_length: Minimum number of words in phrase

    Returns:
        List of capitalized phrases

    Example:
        >>> extract_capitalized_phrases("Apple Inc. and Microsoft Corporation announced")
        ['Apple Inc.', 'Microsoft Corporation']

    TEACHING NOTE:
    --------------
    This is a simple heuristic for entity extraction. Not as accurate
    as NLP-based NER, but useful and deterministic.
    """
    # Pattern: sequence of capitalized words
    phrase_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b'
    phrases = re.findall(phrase_pattern, text)

    # Filter by minimum length
    phrases = [p for p in phrases if len(p.split()) >= min_length]

    # Deduplicate while preserving order
    seen = set()
    unique_phrases = []
    for phrase in phrases:
        if phrase not in seen:
            seen.add(phrase)
            unique_phrases.append(phrase)

    return unique_phrases


def extract_headings(text: str) -> List[Tuple[int, str]]:
    """
    Extract markdown-style headings from text.

    Finds lines starting with # (heading level 1), ## (level 2), etc.

    Args:
        text: Text to extract headings from

    Returns:
        List of (level, heading_text) tuples

    Example:
        >>> extract_headings("# Title\\n## Section\\nContent")
        [(1, 'Title'), (2, 'Section')]
    """
    headings = []
    lines = text.split('\n')

    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            # Count heading level
            level = 0
            for char in line:
                if char == '#':
                    level += 1
                else:
                    break

            # Extract heading text (after the #'s)
            heading_text = line[level:].strip()
            if heading_text:
                headings.append((level, heading_text))

    return headings


def extract_sentences_with_keywords(text: str, keywords: List[str]) -> List[str]:
    """
    Extract sentences that contain any of the given keywords.

    Useful for finding relevant sentences in a document.

    Args:
        text: Text to search
        keywords: List of keywords to look for

    Returns:
        List of sentences containing keywords

    Example:
        >>> extract_sentences_with_keywords(
        >>>     "AI is great. Machine learning too. Weather is nice.",
        >>>     ["ai", "learning"]
        >>> )
        ['AI is great.', 'Machine learning too.']

    TEACHING NOTE:
    --------------
    This utility is used by the Summarizer AGENT to find relevant
    sentences. The agent DECIDES which keywords to search for.
    """
    # Simple sentence splitting
    sentence_pattern = r'[.!?]+\s+'
    sentences = re.split(sentence_pattern, text)

    # Normalize keywords for case-insensitive matching
    keywords_lower = [k.lower() for k in keywords]

    # Find sentences with keywords
    matching_sentences = []
    for sentence in sentences:
        sentence_lower = sentence.lower()
        if any(keyword in sentence_lower for keyword in keywords_lower):
            matching_sentences.append(sentence.strip())

    return matching_sentences
