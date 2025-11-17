"""
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
THE STOMACH  Cleaner Tool
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP

ORGAN METAPHOR:
    The Stomach digests and extracts nutrients from raw food.
    Similarly, the Cleaner Tool processes raw HTML, removing noise
    (ads, scripts, navigation) and extracting the valuable textual content
    that can be used for analysis and summarization.

PURPOSE:
    " Remove HTML boilerplate, ads, and navigation elements
    " Extract main content text from web pages
    " Parse structured data (headings, lists, tables)
    " Normalize whitespace and formatting
    " Output clean, processable text

AGENT vs TOOL:
     NOT an agent  Does not decide what is "important"
     TOOL  Applies deterministic cleaning rules

    The Cleaner Tool:
    - Takes raw HTML and returns cleaned text (pure transformation)
    - Uses heuristics and patterns (not reasoning)
    - Does not interpret content meaning
    - Does not make strategic extraction decisions

TEACHING GOALS:
    This module demonstrates:
    1. Deterministic text processing
    2. Rule-based extraction vs reasoning
    3. Separation of parsing from interpretation
    4. Composable data transformation pipelines

TECHNIQUES USED:
    " HTML parsing (BeautifulSoup, lxml, html5lib)
    " Content extraction (readability, trafilatura)
    " Text normalization and cleaning
    " Structured data extraction

FUTURE EXTENSIONS:
    " PDF and document parsing
    " Table extraction with structure preservation
    " Image text extraction (OCR)
    " Multi-language support
    " Custom extraction templates per domain

DEBUGGING NOTES:
    " Log extraction success rate per source
    " Track content length before/after cleaning
    " Monitor parsing failures
    " Sample outputs for manual quality checks

PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
"""


"""
ASCII DIAGRAM — THE STOMACH DIGESTS:

            ┌──────────────────────────────────┐
            │   RAW HTML INPUT                 │
            │  <html>                          │
            │    <nav>Menu</nav> ← NOISE       │
            │    <article>                     │
            │      <p>Important content</p>    │
            │    </article>                    │
            │    <ads>Buy now!</ads> ← NOISE   │
            │  </html>                         │
            └──────────────┬───────────────────┘
                           │
                           ▼
            ┌──────────────────────────────────┐
            │   CLEANER TOOL STOMACH           │
            │  ┌────────────────────────────┐  │
            │  │ clean_html()               │  │
            │  │ • Parse HTML               │  │
            │  │ • Remove <nav>, <ads>      │  │
            │  │ • Extract <article> text   │  │
            │  │ • Normalize whitespace     │  │
            │  │ • Return clean text        │  │
            │  └────────────────────────────┘  │
            └──────────────┬───────────────────┘
                           │
                           ▼
            ┌──────────────────────────────────┐
            │   CLEAN TEXT OUTPUT              │
            │  "Important content"             │
            │  (structured, readable)          │
            └──────────────────────────────────┘
                           │
                           ▼
            [ Summarizer Tongue processes ]

Key Insight: The Stomach applies RULES to extract content.
             It doesn't UNDERSTAND the content or make decisions
             about what's important conceptually (that's the Tongue's job).

Example Transformation:
    INPUT:  <html><nav>Home</nav><article><p>AI is growing</p></article><ads>...</ads></html>
    OUTPUT: "AI is growing"
"""


# ═══════════════════════════════════════════════════════════════════════════
# IMPLEMENTATION — Phase 1 Stub
# ═══════════════════════════════════════════════════════════════════════════

from typing import Optional, List, Dict, Any
from dataclasses import dataclass


@dataclass
class CleanedContent:
    """
    Result of cleaning HTML content.

    Attributes:
        text: The cleaned, plain-text content
        title: Page title (if found)
        headings: List of headings found in content
        word_count: Number of words in cleaned text
        metadata: Additional extraction results
        error: Error message if cleaning failed
    """

    text: str
    title: Optional[str] = None
    headings: List[str] = None
    word_count: int = 0
    metadata: Dict[str, Any] = None
    error: Optional[str] = None

    def __post_init__(self):
        if self.headings is None:
            self.headings = []
        if self.metadata is None:
            self.metadata = {}
        if self.word_count == 0 and self.text:
            self.word_count = len(self.text.split())

    @property
    def success(self) -> bool:
        """Check if cleaning was successful."""
        return self.error is None and len(self.text) > 0

    def __repr__(self) -> str:
        return f"CleanedContent(words={self.word_count}, title={self.title!r})"


def clean_html(
    html: str,
    remove_elements: Optional[List[str]] = None,
    min_length: int = 100,
) -> CleanedContent:
    """
    Clean HTML and extract main text content.

    This is a STUB implementation for Phase 1.
    Full implementation with BeautifulSoup/Trafilatura comes in Phase 2.

    Args:
        html: Raw HTML string to clean
        remove_elements: List of HTML tags to remove (e.g., ['nav', 'footer'])
        min_length: Minimum character length for valid content

    Returns:
        CleanedContent: Object containing cleaned text and metadata

    Example:
        html = "<html><body><h1>Title</h1><p>Content</p></body></html>"
        result = clean_html(html)
        print(result.text)  # "Title\n\nContent"

    Teaching Notes:
        This is a deterministic TOOL function:
        • Takes HTML → Returns plain text (pure transformation)
        • Uses rules and heuristics (not reasoning)
        • Doesn't interpret content meaning
        • Doesn't decide what's "important" conceptually

        The Cleaner applies SYNTACTIC rules:
        - Remove <script>, <style>, <nav>
        - Extract text from <article>, <main>, <p>
        - Normalize whitespace

        The Summarizer (Agent) applies SEMANTIC understanding:
        - Decides which sentences are important
        - Chooses tone and style
        - Synthesizes insights
    """
    if remove_elements is None:
        remove_elements = ["nav", "footer", "aside", "script", "style"]

    # Phase 1: Simple stub that strips basic tags
    # Phase 2 will use BeautifulSoup or Trafilatura for proper parsing

    print(f"[CLEANER STUB] Processing {len(html)} chars of HTML")
    print(f"[CLEANER STUB] Would remove elements: {remove_elements}")

    # Simple tag stripping (very naive, just for demonstration)
    import re

    # Extract title if present
    title_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
    title = title_match.group(1) if title_match else None

    # Extract headings (h1-h6)
    headings = re.findall(r"<h[1-6]>(.*?)</h[1-6]>", html, re.IGNORECASE)

    # Naive text extraction: remove all HTML tags
    # Phase 2 will do this properly with a parser
    text = re.sub(r"<[^>]+>", " ", html)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Add structure back
    if title:
        text = f"{title}\n\n{text}"

    # Check minimum length
    if len(text) < min_length:
        return CleanedContent(
            text="",
            title=title,
            error=f"Content too short ({len(text)} < {min_length} chars)",
        )

    return CleanedContent(
        text=text,
        title=title,
        headings=headings,
        word_count=len(text.split()),
        metadata={
            "stub": True,
            "original_length": len(html),
            "cleaned_length": len(text),
            "compression_ratio": len(text) / len(html) if html else 0,
        },
    )


def extract_main_content(html: str) -> str:
    """
    Extract just the main content from HTML (article, main sections).

    STUB for Phase 1. Phase 2 will use readability or trafilatura.

    Args:
        html: Raw HTML string

    Returns:
        str: Main content text

    Teaching Notes:
        This function demonstrates content extraction heuristics:
        • Prioritize <article>, <main> tags
        • Look for content density patterns
        • Filter out boilerplate (navigation, ads, footers)

        Phase 2 libraries like Trafilatura use:
        - Text density analysis
        - DOM tree traversal
        - Machine learning models (in some cases)
    """
    print("[CLEANER STUB] extract_main_content: Using basic extraction")

    # Stub: just return cleaned HTML
    result = clean_html(html)
    return result.text if result.success else ""


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text.

    Args:
        text: Text with irregular whitespace

    Returns:
        str: Text with normalized whitespace

    Teaching Notes:
        Simple utility function demonstrating text normalization:
        • Collapse multiple spaces → single space
        • Collapse multiple newlines → double newline (paragraph breaks)
        • Strip leading/trailing whitespace
        • Remove other control characters
    """
    import re

    # Collapse multiple spaces
    text = re.sub(r" +", " ", text)

    # Collapse multiple newlines (keep paragraph breaks)
    text = re.sub(r"\n\n+", "\n\n", text)

    # Strip whitespace
    text = text.strip()

    return text


# ═══════════════════════════════════════════════════════════════════════════
# FUTURE IMPLEMENTATION NOTES (Phase 2)
# ═══════════════════════════════════════════════════════════════════════════

"""
Phase 2 Implementation Plan:

1. Use BeautifulSoup for HTML parsing:
   from bs4 import BeautifulSoup
   soup = BeautifulSoup(html, 'lxml')
   # Remove unwanted elements
   for tag in soup(['script', 'style', 'nav']):
       tag.decompose()

2. Use Trafilatura for smart content extraction:
   import trafilatura
   text = trafilatura.extract(html)
   # Trafilatura is excellent at finding main content

3. Use readability-lxml for article extraction:
   from readability import Document
   doc = Document(html)
   title = doc.title()
   content = doc.summary()

4. Structured extraction:
   • Extract headings: soup.find_all(['h1', 'h2', 'h3'])
   • Extract lists: soup.find_all(['ul', 'ol'])
   • Extract tables: soup.find_all('table')
   • Extract links: soup.find_all('a', href=True)

5. Advanced cleaning:
   • Remove duplicate paragraphs
   • Detect and remove boilerplate (copyright notices, etc.)
   • Detect language and handle encoding
   • Handle malformed HTML gracefully

6. Quality scoring:
   • Text density (content vs markup ratio)
   • Readability scores (Flesch-Kincaid)
   • Content structure (has headings, paragraphs?)
   • Link density (too many links = spam)

Example Phase 2 implementation:
    from bs4 import BeautifulSoup
    import trafilatura

    def clean_html(html):
        # Try Trafilatura first (best results)
        text = trafilatura.extract(html)

        if text:
            return CleanedContent(text=text)

        # Fallback to BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')
        for tag in soup(['script', 'style', 'nav', 'footer']):
            tag.decompose()

        text = soup.get_text(separator='\\n', strip=True)
        return CleanedContent(text=normalize_whitespace(text))
"""
