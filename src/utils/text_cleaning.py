"""
TEXT CLEANING UTILITIES
========================

PURPOSE:
--------
Shared helper functions for text normalization and cleaning.
Used by the Cleaner Tool and other components that need to
process raw text.

RESPONSIBILITIES:
-----------------
  1. Remove excessive whitespace
  2. Normalize unicode characters
  3. Strip HTML entities
  4. Remove special characters (optionally)
  5. Sentence and paragraph segmentation

TEACHING NOTES:
---------------
These are pure UTILITY FUNCTIONS — deterministic transformations
with no state or side effects. They're the building blocks used
by higher-level tools and agents.

FUTURE EXTENSIONS:
------------------
  • Language detection
  • Character encoding detection and conversion
  • Smart quote and dash normalization
  • Markdown preservation during cleaning

DEBUGGING TIPS:
---------------
  • Test with edge cases (emoji, unicode, mixed encodings)
  • Verify idempotency (cleaning twice = cleaning once)
  • Monitor for unintended character loss
"""

import re
import html
from typing import List


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text.

    Collapses multiple spaces, tabs, and newlines into single spaces.
    Preserves intentional paragraph breaks (double newlines).

    Args:
        text: Raw text with irregular whitespace

    Returns:
        Text with normalized whitespace

    Example:
        >>> normalize_whitespace("Hello    world\\n\\n\\nNew paragraph")
        'Hello world\\n\\nNew paragraph'

    TEACHING NOTE:
    --------------
    This is a DETERMINISTIC UTILITY. Same input → same output, always.
    No decisions, just consistent transformation rules.
    """
    # Collapse multiple spaces/tabs to single space
    text = re.sub(r'[ \t]+', ' ', text)

    # Collapse multiple newlines (keep max 2 for paragraph breaks)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Remove trailing/leading whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)

    return text.strip()


def remove_html_entities(text: str) -> str:
    """
    Decode HTML entities to regular characters.

    Converts &nbsp;, &lt;, &gt;, &quot;, etc. to their actual characters.

    Args:
        text: Text containing HTML entities

    Returns:
        Text with entities decoded

    Example:
        >>> remove_html_entities("AT&amp;T says &quot;Hello&quot;")
        'AT&T says "Hello"'
    """
    return html.unescape(text)


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Text containing special characters
        keep_punctuation: If True, keep basic punctuation (.,!?;:)

    Returns:
        Text with special characters removed

    Example:
        >>> remove_special_characters("Hello © World™", keep_punctuation=True)
        'Hello  World'
    """
    if keep_punctuation:
        # Keep alphanumeric, spaces, and basic punctuation
        text = re.sub(r'[^a-zA-Z0-9\s.,!?;:\-\'\"()]', '', text)
    else:
        # Keep only alphanumeric and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    return normalize_whitespace(text)


def segment_sentences(text: str) -> List[str]:
    """
    Segment text into sentences.

    Simple sentence segmentation based on punctuation.
    More sophisticated than just splitting on periods.

    Args:
        text: Text to segment

    Returns:
        List of sentences

    Example:
        >>> segment_sentences("Dr. Smith said hello. How are you?")
        ['Dr. Smith said hello.', 'How are you?']

    TEACHING NOTE:
    --------------
    This is a heuristic-based segmentation. Not perfect, but deterministic.
    Could be improved with NLP libraries like spaCy or NLTK.
    """
    # Basic sentence splitting pattern
    # Handles ., !, ? followed by space and capital letter
    sentence_pattern = r'(?<=[.!?])\s+(?=[A-Z])'
    sentences = re.split(sentence_pattern, text)

    # Clean and filter
    sentences = [s.strip() for s in sentences if s.strip()]

    return sentences


def segment_paragraphs(text: str) -> List[str]:
    """
    Segment text into paragraphs.

    Splits on double newlines or more.

    Args:
        text: Text to segment

    Returns:
        List of paragraphs

    Example:
        >>> segment_paragraphs("Paragraph 1.\\n\\nParagraph 2.")
        ['Paragraph 1.', 'Paragraph 2.']
    """
    # Split on multiple newlines
    paragraphs = re.split(r'\n{2,}', text)

    # Clean and filter
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    return paragraphs


def clean_text(text: str, aggressive: bool = False) -> str:
    """
    Apply all cleaning operations in sequence.

    This is a convenience function that applies multiple cleaning steps.

    Args:
        text: Raw text to clean
        aggressive: If True, removes all special characters

    Returns:
        Cleaned text

    Example:
        >>> clean_text("  Hello&nbsp;&nbsp;World!  \\n\\n\\n  ")
        'Hello  World!'

    TEACHING NOTE:
    --------------
    This function composes multiple utilities into a pipeline.
    Each step is deterministic, so the whole pipeline is deterministic.
    """
    # Step 1: Decode HTML entities
    text = remove_html_entities(text)

    # Step 2: Remove special characters (if aggressive)
    if aggressive:
        text = remove_special_characters(text, keep_punctuation=True)

    # Step 3: Normalize whitespace
    text = normalize_whitespace(text)

    return text
