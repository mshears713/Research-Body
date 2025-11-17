"""
THE STOMACH — CLEANER TOOL
===========================

ORGAN METAPHOR:
---------------
The Cleaner is the STOMACH of the research organism.
It digests raw HTML and extracts the nutritious content (relevant text),
discarding the waste (ads, navigation, boilerplate).

ASCII DIAGRAM:
--------------
                ┌──────────────────────────┐
                │   RAW HTML INPUT         │
                │ <html><nav>...</nav>     │
                │ <article>CONTENT</...>   │
                └────────────┬─────────────┘
                             │
                             ▼
                ┌──────────────────────────┐
                │    CLEANER TOOL          │
                │      (STOMACH)           │
                │   [DETERMINISTIC]        │
                │                          │
                │  ╔════════════════╗      │
                │  ║ DIGEST & PARSE ║      │
                │  ╚════════════════╝      │
                └────────────┬─────────────┘
                             │
                ┌────────────┼────────────┐
                ▼            ▼            ▼
           [DISCARD]    [EXTRACT]    [DISCARD]
           ads, nav     main text    footers
                             │
                             ▼
                ┌──────────────────────────┐
                │   CLEAN TEXT OUTPUT      │
                │   "Main article content" │
                └──────────────────────────┘

AGENT vs TOOL:
--------------
This is a TOOL because it:
  • Applies deterministic text extraction rules
  • Does not decide WHAT is relevant, only HOW to extract it
  • Has no autonomous decision-making capability
  • Simply processes input and returns clean output

RESPONSIBILITIES:
-----------------
  1. Parse raw HTML into structured DOM
  2. Extract main content (articles, text blocks)
  3. Remove boilerplate (headers, footers, ads, navigation)
  4. Clean whitespace, normalize text encoding
  5. Return structured clean text ready for summarization

TEACHING NOTES:
---------------
The Cleaner TOOL is deterministic. It applies rules consistently:
"Remove all <nav> tags", "Extract text from <article>", etc.
It has no judgment about whether the content is good or relevant —
that's the job of the Summarizer AGENT.

FUTURE EXTENSIONS:
------------------
  • Machine learning-based content extraction
  • Support for PDF, DOCX, and other formats
  • Intelligent table and list extraction
  • Metadata extraction (author, date, keywords)

DEBUGGING TIPS:
---------------
  • Compare raw HTML to cleaned output for accuracy
  • Monitor for over-aggressive or under-aggressive cleaning
  • Track extraction success rates by site structure
"""

from typing import Dict, Optional


def clean_html(raw_html: str, url: str = "") -> Dict[str, any]:
    """
    Extract clean text from raw HTML.

    This is a TOOL FUNCTION — deterministic text extraction.
    It applies consistent rules to remove boilerplate and extract content.

    Args:
        raw_html: Raw HTML string from scraper
        url: Source URL (for context and metadata)

    Returns:
        Dictionary containing:
        - clean_text: Extracted main content
        - title: Page title
        - metadata: Dict of extracted metadata (author, date, etc.)
        - word_count: Number of words in clean text

    Example:
        >>> result = clean_html(html_string, "https://example.com")
        >>> print(result['clean_text'])
        >>> print(f"Extracted {result['word_count']} words")

    TEACHING NOTE:
    --------------
    This is a stub implementation. In Phase 2, we'll add:
      • BeautifulSoup or lxml for HTML parsing
      • Heuristics to identify main content vs. boilerplate
      • Removal of <nav>, <footer>, <aside>, ads
      • Text normalization (whitespace, encoding)
      • Metadata extraction (Open Graph, Schema.org)
    """
    # STUB: Return placeholder data
    # In Phase 2, this will use BeautifulSoup to actually parse HTML

    print(f"[CLEANER TOOL] Cleaning HTML from: {url}")

    # Simple placeholder extraction (in reality, we'd parse the HTML)
    placeholder_text = f"""
    This is placeholder cleaned text from {url}.

    In Phase 2, this will contain the actual extracted article content,
    with all navigation, ads, and boilerplate removed.

    The cleaner will intelligently identify the main content area
    and extract only the relevant text for summarization.
    """

    return {
        "clean_text": placeholder_text.strip(),
        "title": "Placeholder Article Title",
        "metadata": {
            "url": url,
            "author": "Unknown",
            "date": None,
            "keywords": []
        },
        "word_count": len(placeholder_text.split())
    }


def extract_main_content(html: str) -> str:
    """
    Extract main content from HTML (stub).

    In Phase 2, this will use heuristics to identify the main content area:
      • Look for <article>, <main> tags
      • Identify largest text block
      • Remove navigation, sidebars, footers

    Args:
        html: Raw HTML string

    Returns:
        Extracted main content text
    """
    # STUB: placeholder implementation
    return "Placeholder main content"


def remove_boilerplate(html: str) -> str:
    """
    Remove common boilerplate elements (stub).

    In Phase 2, this will remove:
      • Navigation menus
      • Advertisements
      • Social media widgets
      • Cookie notices
      • Related article links

    Args:
        html: Raw HTML string

    Returns:
        HTML with boilerplate removed
    """
    # STUB: placeholder implementation
    return html


# FUTURE: Add these functions in Phase 2
# def extract_metadata(html: str) -> Dict:
#     """Extract Open Graph, Schema.org metadata"""
#     pass
#
# def detect_content_blocks(html: str) -> List[str]:
#     """Identify distinct content blocks for extraction"""
#     pass
