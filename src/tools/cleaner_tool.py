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

from bs4 import BeautifulSoup
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class CleanerTool:
    """
    THE STOMACH — Deterministic HTML Cleaning Tool
    ===============================================

    This class encapsulates all HTML cleaning and text extraction.
    It's a TOOL because it applies DETERMINISTIC RULES consistently.

    TOOL CHARACTERISTICS:
    ---------------------
      • Applies consistent extraction rules to all HTML
      • No judgment about content quality or relevance
      • Deterministic: same HTML → same clean text
      • No decision-making, just mechanical processing

    WHY NOT AN AGENT:
    -----------------
    The cleaner doesn't decide:
      - Whether content is important or relevant
      - What kind of content to prioritize
      - How to adapt extraction for different topics
      - What to do with the extracted content

    It just cleans. Period.

    TEACHING NOTE:
    --------------
    Compare to the Summarizer AGENT (Phase 2, Step 14):
    The Summarizer will DECIDE what to emphasize, what tone to use,
    and how to structure the output. That's agent behavior.
    The Cleaner just mechanically extracts text.
    """

    # Tags that typically contain boilerplate/navigation
    BOILERPLATE_TAGS = [
        'nav', 'header', 'footer', 'aside', 'script', 'style',
        'noscript', 'iframe', 'form', 'button'
    ]

    # Classes/IDs that often indicate ads or non-content
    BOILERPLATE_PATTERNS = [
        'nav', 'menu', 'sidebar', 'ad', 'advertisement', 'banner',
        'footer', 'header', 'social', 'share', 'comment', 'related',
        'cookie', 'popup', 'modal', 'promo'
    ]

    # Tags that typically contain main content
    CONTENT_TAGS = ['article', 'main', 'section', 'div', 'p']

    def __init__(self, debug: bool = False):
        """
        Initialize the Cleaner Tool.

        Args:
            debug: Enable detailed logging of cleaning operations
        """
        self.debug = debug
        self._cleaning_history = []  # Track all cleanings for analysis

    def clean_html(self, raw_html: str, url: str = "") -> Dict[str, any]:
        """
        Extract clean text from raw HTML.

        This is the core TOOL FUNCTION — deterministic text extraction.
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
            - extraction_stats: Statistics about the cleaning process

        Example:
            >>> cleaner = CleanerTool()
            >>> result = cleaner.clean_html(html_string, "https://example.com")
            >>> print(result['clean_text'])
            >>> print(f"Extracted {result['word_count']} words")

        TEACHING NOTE:
        --------------
        This method orchestrates multiple deterministic steps:
          1. Parse HTML → BeautifulSoup object
          2. Extract metadata → structured data
          3. Remove boilerplate → cleaned HTML
          4. Extract main content → text
          5. Normalize text → final clean text

        Each step is deterministic and repeatable.
        """
        if self.debug:
            print(f"\n[CLEANER TOOL] Processing: {url}")
            print(f"[CLEANER TOOL] Raw HTML size: {len(raw_html)} chars")

        # Parse HTML
        soup = BeautifulSoup(raw_html, 'html.parser')

        # Extract metadata
        title = self._extract_title(soup, url)
        metadata = self._extract_metadata(soup, url)

        # Remove boilerplate elements
        soup_cleaned = self._remove_boilerplate(soup)

        # Extract main content
        main_content = self._extract_main_content(soup_cleaned)

        # Normalize and clean text
        clean_text = self._normalize_text(main_content)

        # Calculate statistics
        word_count = len(clean_text.split())
        extraction_stats = {
            'raw_html_length': len(raw_html),
            'clean_text_length': len(clean_text),
            'word_count': word_count,
            'compression_ratio': len(clean_text) / len(raw_html) if raw_html else 0,
            'title_extracted': bool(title),
            'metadata_fields': len(metadata)
        }

        result = {
            'clean_text': clean_text,
            'title': title,
            'metadata': metadata,
            'word_count': word_count,
            'extraction_stats': extraction_stats
        }

        if self.debug:
            print(f"[CLEANER TOOL] ✓ Extracted {word_count} words")
            print(f"[CLEANER TOOL]   Title: {title}")
            print(f"[CLEANER TOOL]   Compression: {extraction_stats['compression_ratio']:.1%}")

        # Record cleaning history
        self._record_cleaning(url, result)

        return result

    def _extract_title(self, soup: BeautifulSoup, url: str) -> str:
        """
        Extract page title using multiple strategies.

        DETERMINISTIC HEURISTIC:
          1. Try Open Graph title (og:title)
          2. Try <title> tag
          3. Try first <h1>
          4. Fallback to URL
        """
        # Strategy 1: Open Graph title
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            return og_title['content'].strip()

        # Strategy 2: <title> tag
        title_tag = soup.find('title')
        if title_tag and title_tag.string:
            return title_tag.string.strip()

        # Strategy 3: First <h1>
        h1_tag = soup.find('h1')
        if h1_tag:
            return h1_tag.get_text().strip()

        # Fallback: Extract from URL
        return url.split('/')[-1] or "Untitled"

    def _extract_metadata(self, soup: BeautifulSoup, url: str) -> Dict:
        """
        Extract metadata from HTML using Open Graph, Schema.org, and meta tags.

        DETERMINISTIC EXTRACTION: Always checks the same tags in the same order.
        """
        metadata = {
            'url': url,
            'author': None,
            'date_published': None,
            'description': None,
            'keywords': [],
            'image': None,
            'site_name': None
        }

        # Extract Open Graph metadata
        og_description = soup.find('meta', property='og:description')
        if og_description:
            metadata['description'] = og_description.get('content', '').strip()

        og_image = soup.find('meta', property='og:image')
        if og_image:
            metadata['image'] = og_image.get('content', '').strip()

        og_site = soup.find('meta', property='og:site_name')
        if og_site:
            metadata['site_name'] = og_site.get('content', '').strip()

        # Extract author
        author_meta = soup.find('meta', attrs={'name': 'author'})
        if author_meta:
            metadata['author'] = author_meta.get('content', '').strip()

        # Extract description (if not from OG)
        if not metadata['description']:
            desc_meta = soup.find('meta', attrs={'name': 'description'})
            if desc_meta:
                metadata['description'] = desc_meta.get('content', '').strip()

        # Extract keywords
        keywords_meta = soup.find('meta', attrs={'name': 'keywords'})
        if keywords_meta:
            keywords_str = keywords_meta.get('content', '')
            metadata['keywords'] = [k.strip() for k in keywords_str.split(',') if k.strip()]

        # Extract publication date
        date_meta = soup.find('meta', property='article:published_time')
        if date_meta:
            metadata['date_published'] = date_meta.get('content', '').strip()

        return metadata

    def _remove_boilerplate(self, soup: BeautifulSoup) -> BeautifulSoup:
        """
        Remove boilerplate elements from HTML.

        DETERMINISTIC RULE APPLICATION:
          - Remove all navigation, headers, footers
          - Remove scripts, styles, ads
          - Remove elements with boilerplate class/id patterns

        Args:
            soup: BeautifulSoup object

        Returns:
            Cleaned BeautifulSoup object (modifies in place)

        TEACHING NOTE:
        --------------
        This is pure mechanical filtering. No judgment about content quality.
        """
        # Remove boilerplate tags
        for tag_name in self.BOILERPLATE_TAGS:
            for tag in soup.find_all(tag_name):
                tag.decompose()

        # Remove elements with boilerplate class/id patterns
        for element in soup.find_all(True):  # Find all tags
            class_str = ' '.join(element.get('class', [])).lower()
            id_str = element.get('id', '').lower()

            # Check if class or id matches boilerplate patterns
            for pattern in self.BOILERPLATE_PATTERNS:
                if pattern in class_str or pattern in id_str:
                    element.decompose()
                    break

        return soup

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """
        Extract main content from cleaned HTML.

        DETERMINISTIC HEURISTIC:
          1. Try <article> tag
          2. Try <main> tag
          3. Try role="main"
          4. Find largest text block
          5. Fallback to all <p> tags

        Args:
            soup: BeautifulSoup object (already cleaned of boilerplate)

        Returns:
            Extracted main content as text

        TEACHING NOTE:
        --------------
        These heuristics are DETERMINISTIC rules, not intelligent decisions.
        The same HTML structure will always produce the same result.
        """
        # Strategy 1: <article> tag
        article = soup.find('article')
        if article:
            return article.get_text(separator=' ', strip=True)

        # Strategy 2: <main> tag
        main = soup.find('main')
        if main:
            return main.get_text(separator=' ', strip=True)

        # Strategy 3: role="main"
        main_role = soup.find(attrs={'role': 'main'})
        if main_role:
            return main_role.get_text(separator=' ', strip=True)

        # Strategy 4: Find largest text block
        content_candidates = []
        for tag_name in self.CONTENT_TAGS:
            for tag in soup.find_all(tag_name):
                text = tag.get_text(separator=' ', strip=True)
                if len(text) > 100:  # Minimum content threshold
                    content_candidates.append((len(text), text, tag))

        if content_candidates:
            # Sort by text length and take the largest
            content_candidates.sort(reverse=True)
            return content_candidates[0][1]

        # Strategy 5: Fallback to all paragraphs
        paragraphs = soup.find_all('p')
        if paragraphs:
            return ' '.join(p.get_text(strip=True) for p in paragraphs)

        # Last resort: all text
        return soup.get_text(separator=' ', strip=True)

    def _normalize_text(self, text: str) -> str:
        """
        Normalize and clean extracted text.

        DETERMINISTIC TEXT PROCESSING:
          - Collapse multiple whitespaces
          - Remove excessive newlines
          - Strip leading/trailing whitespace
          - Normalize unicode characters

        Args:
            text: Raw extracted text

        Returns:
            Normalized clean text

        TEACHING NOTE:
        --------------
        Pure string manipulation. No semantic understanding.
        """
        # Collapse multiple spaces
        text = re.sub(r'\s+', ' ', text)

        # Remove excessive newlines (more than 2)
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Strip leading/trailing whitespace
        text = text.strip()

        return text

    def _record_cleaning(self, url: str, result: Dict):
        """Record cleaning operation in history for debugging."""
        self._cleaning_history.append({
            'url': url,
            'word_count': result['word_count'],
            'stats': result['extraction_stats'],
            'timestamp': datetime.now()
        })

    def get_cleaning_stats(self) -> Dict:
        """
        Get statistics about cleaning history.

        DEBUGGING HELPER: Analyze cleaner performance and effectiveness.

        Returns:
            Dict with avg_word_count, avg_compression_ratio, total_cleanings, etc.
        """
        if not self._cleaning_history:
            return {
                'total_cleanings': 0,
                'avg_word_count': 0.0,
                'avg_compression_ratio': 0.0
            }

        total = len(self._cleaning_history)
        word_counts = [c['word_count'] for c in self._cleaning_history]
        compression_ratios = [c['stats']['compression_ratio'] for c in self._cleaning_history]

        return {
            'total_cleanings': total,
            'avg_word_count': sum(word_counts) / total,
            'min_word_count': min(word_counts),
            'max_word_count': max(word_counts),
            'avg_compression_ratio': sum(compression_ratios) / total,
        }


# Convenience function for simple one-off cleaning
def clean_html(raw_html: str, url: str = "") -> Dict[str, any]:
    """
    Simple convenience function for one-off HTML cleaning.

    This wraps the CleanerTool class for backwards compatibility
    and simple use cases.

    Args:
        raw_html: Raw HTML string from scraper
        url: Source URL (for context and metadata)

    Returns:
        Dictionary with clean_text, title, metadata, word_count, extraction_stats

    Example:
        >>> result = clean_html(html_string, "https://example.com")
        >>> print(result['clean_text'])
        >>> print(f"Extracted {result['word_count']} words")

    TEACHING NOTE:
    --------------
    This function creates a new CleanerTool instance for each call.
    For repeated cleanings, use CleanerTool directly to track history.
    """
    cleaner = CleanerTool()
    return cleaner.clean_html(raw_html, url)
