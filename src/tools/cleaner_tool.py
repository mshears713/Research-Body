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

    def extract_structured(self, raw_html: str, url: str = "") -> Dict[str, any]:
        """
        Extract structured data from HTML (Phase 3, Step 25).

        In addition to clean text, this extracts:
          - Headings with hierarchy
          - Lists (ordered and unordered)
          - Tables as structured data
          - Links with context
          - Sections organized by headings

        Args:
            raw_html: Raw HTML string from scraper
            url: Source URL (for context and metadata)

        Returns:
            Dictionary containing:
            - clean_text: Extracted main content
            - structured_data: Dict with headings, lists, tables, links, sections
            - title: Page title
            - metadata: Extracted metadata
            - word_count: Number of words

        Example:
            >>> cleaner = CleanerTool()
            >>> result = cleaner.extract_structured(html, "https://example.com")
            >>> print(result['structured_data']['headings'])
            >>> print(result['structured_data']['tables'])

        PHASE 3 EXTENSION (Step 25):
        -----------------------------
        This demonstrates STRUCTURED EXTRACTION — going beyond plain text
        to preserve the document structure (headings, lists, tables).

        This is still a TOOL (deterministic extraction rules) but with
        richer output that preserves semantic structure.

        TEACHING NOTE:
        --------------
        Compare to clean_html() which flattens everything to text.
        Structured extraction preserves document organization, making it
        easier for the Summarizer AGENT to understand document hierarchy.
        """
        if self.debug:
            print(f"\n[CLEANER TOOL] Structured extraction: {url}")

        # Parse HTML
        soup = BeautifulSoup(raw_html, 'html.parser')

        # Extract basic data (same as clean_html)
        title = self._extract_title(soup, url)
        metadata = self._extract_metadata(soup, url)

        # Remove boilerplate
        soup_cleaned = self._remove_boilerplate(soup)

        # Extract structured data (Phase 3 enhancement)
        headings = self._extract_headings(soup_cleaned)
        lists = self._extract_lists(soup_cleaned)
        tables = self._extract_tables(soup_cleaned)
        links = self._extract_links(soup_cleaned, url)
        sections = self._extract_sections(soup_cleaned)

        # Also extract clean text for backward compatibility
        main_content = self._extract_main_content(soup_cleaned)
        clean_text = self._normalize_text(main_content)

        # Calculate statistics
        word_count = len(clean_text.split())

        structured_data = {
            'headings': headings,
            'lists': lists,
            'tables': tables,
            'links': links,
            'sections': sections
        }

        extraction_stats = {
            'raw_html_length': len(raw_html),
            'clean_text_length': len(clean_text),
            'word_count': word_count,
            'num_headings': len(headings),
            'num_lists': len(lists),
            'num_tables': len(tables),
            'num_links': len(links),
            'num_sections': len(sections)
        }

        result = {
            'clean_text': clean_text,
            'structured_data': structured_data,
            'title': title,
            'metadata': metadata,
            'word_count': word_count,
            'extraction_stats': extraction_stats
        }

        if self.debug:
            print(f"[CLEANER TOOL] ✓ Structured extraction complete")
            print(f"  Headings: {len(headings)}")
            print(f"  Lists: {len(lists)}")
            print(f"  Tables: {len(tables)}")
            print(f"  Links: {len(links)}")
            print(f"  Sections: {len(sections)}")

        return result

    def _extract_headings(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract all headings with their hierarchy.

        STRUCTURED EXTRACTION (Phase 3, Step 25):
        ------------------------------------------
        Extracts h1-h6 tags with:
          - Level (1-6)
          - Text content
          - Position in document

        Returns:
            List of dicts: [{'level': 1, 'text': 'Heading', 'position': 0}, ...]

        TEACHING NOTE:
        --------------
        This preserves document structure, helping the Summarizer AGENT
        understand the organization and importance hierarchy of content.
        """
        headings = []
        for i, tag_name in enumerate(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            level = int(tag_name[1])
            for tag in soup.find_all(tag_name):
                text = tag.get_text(strip=True)
                if text:  # Only include non-empty headings
                    headings.append({
                        'level': level,
                        'text': text,
                        'position': len(headings)  # Document order
                    })
        return headings

    def _extract_lists(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract ordered and unordered lists.

        STRUCTURED EXTRACTION (Phase 3, Step 25):
        ------------------------------------------
        Extracts <ul> and <ol> lists with all items.

        Returns:
            List of dicts: [{'type': 'ul', 'items': ['item1', 'item2']}, ...]

        TEACHING NOTE:
        --------------
        Lists often contain key points or steps. Preserving them helps
        the Summarizer AGENT identify structured information like:
          - Key findings
          - Step-by-step procedures
          - Feature lists
        """
        lists = []

        # Extract unordered lists
        for ul in soup.find_all('ul'):
            items = [li.get_text(strip=True) for li in ul.find_all('li', recursive=False)]
            if items:  # Only include non-empty lists
                lists.append({
                    'type': 'unordered',
                    'items': items
                })

        # Extract ordered lists
        for ol in soup.find_all('ol'):
            items = [li.get_text(strip=True) for li in ol.find_all('li', recursive=False)]
            if items:
                lists.append({
                    'type': 'ordered',
                    'items': items
                })

        return lists

    def _extract_tables(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract tables as structured data.

        STRUCTURED EXTRACTION (Phase 3, Step 25):
        ------------------------------------------
        Extracts <table> elements with headers and rows.

        Returns:
            List of dicts: [{'headers': [...], 'rows': [[...], [...]]}, ...]

        TEACHING NOTE:
        --------------
        Tables contain structured data that's lost when flattened to text.
        Preserving table structure helps the Summarizer AGENT understand:
          - Comparisons
          - Specifications
          - Research data
        """
        tables = []

        for table in soup.find_all('table'):
            # Extract headers
            headers = []
            thead = table.find('thead')
            if thead:
                header_row = thead.find('tr')
                if header_row:
                    headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]

            # If no thead, try first row
            if not headers:
                first_row = table.find('tr')
                if first_row:
                    headers = [th.get_text(strip=True) for th in first_row.find_all('th')]

            # Extract rows
            rows = []
            tbody = table.find('tbody') or table
            for tr in tbody.find_all('tr'):
                # Skip header row if we already got it
                if tr.find('th') and headers:
                    continue

                cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                if cells:  # Only include non-empty rows
                    rows.append(cells)

            if rows:  # Only include tables with data
                tables.append({
                    'headers': headers,
                    'rows': rows,
                    'num_rows': len(rows),
                    'num_cols': len(rows[0]) if rows else 0
                })

        return tables

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """
        Extract links with context.

        STRUCTURED EXTRACTION (Phase 3, Step 25):
        ------------------------------------------
        Extracts <a> tags with link text and URL.

        Args:
            soup: BeautifulSoup object
            base_url: Base URL for resolving relative links

        Returns:
            List of dicts: [{'text': 'link text', 'url': 'https://...', 'type': 'internal'}, ...]

        TEACHING NOTE:
        --------------
        Links show relationships between content and sources.
        The Summarizer AGENT can use this to:
          - Identify cited sources
          - Follow related content
          - Understand document connections
        """
        from urllib.parse import urljoin, urlparse

        links = []
        base_domain = urlparse(base_url).netloc if base_url else ""

        for a_tag in soup.find_all('a', href=True):
            text = a_tag.get_text(strip=True)
            href = a_tag['href']

            # Resolve relative URLs
            absolute_url = urljoin(base_url, href) if base_url else href

            # Classify as internal or external
            link_domain = urlparse(absolute_url).netloc
            link_type = 'internal' if link_domain == base_domain else 'external'

            if text and href:  # Only include links with text and href
                links.append({
                    'text': text,
                    'url': absolute_url,
                    'type': link_type
                })

        return links

    def _extract_sections(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract content sections organized by headings.

        STRUCTURED EXTRACTION (Phase 3, Step 25):
        ------------------------------------------
        Organizes content into sections based on heading hierarchy.
        Each section contains the heading and associated content until
        the next heading of equal or higher level.

        Returns:
            List of dicts: [{'heading': 'Section Title', 'level': 2, 'content': '...'}, ...]

        TEACHING NOTE:
        --------------
        Sections preserve document organization, making it much easier
        for the Summarizer AGENT to:
          - Understand topic boundaries
          - Generate section-wise summaries
          - Maintain narrative flow
        """
        sections = []
        current_section = None

        # Iterate through all elements
        for element in soup.descendants:
            if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                # Start new section
                if current_section:
                    # Finish previous section
                    sections.append(current_section)

                level = int(element.name[1])
                heading_text = element.get_text(strip=True)

                current_section = {
                    'heading': heading_text,
                    'level': level,
                    'content': []
                }

            elif current_section is not None and element.name in ['p', 'div', 'span']:
                # Add content to current section
                text = element.get_text(strip=True)
                if text and len(text) > 20:  # Only meaningful content
                    current_section['content'].append(text)

        # Add final section
        if current_section and current_section['content']:
            sections.append(current_section)

        # Join content lists into strings
        for section in sections:
            section['content'] = ' '.join(section['content'])

        return sections

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
