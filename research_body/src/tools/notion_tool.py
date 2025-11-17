"""
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
THE HAND  Notion Tool
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP

ORGAN METAPHOR:
    The Hand writes down and organizes research findings.
    Just as a hand records notes and organizes information,
    the Notion Tool takes processed summaries and stores them
    in a structured, searchable Notion database.

PURPOSE:
    " Connect to Notion API
    " Create or update database entries
    " Format summaries for Notion's block structure
    " Manage metadata (tags, dates, sources)
    " Handle authentication and rate limits

AGENT vs TOOL:
     NOT an agent  Does not decide what to write or how to organize
     TOOL  Deterministic data storage operation

    The Notion Tool:
    - Takes formatted content and writes it to Notion
    - Does not decide what information is important
    - Does not reorganize or restructure content
    - Simply executes the write operation

TEACHING GOALS:
    This module demonstrates:
    1. API integration as a tool
    2. Deterministic output operations
    3. Separation of content generation from storage
    4. Error handling for external services

INTEGRATION NOTES:
    " Requires Notion API key (environment variable)
    " Requires database ID for target location
    " Supports both pages and database entries
    " Can include rich formatting (headings, lists, links)

FUTURE EXTENSIONS:
    " Support for other output targets (Obsidian, Roam, Google Docs)
    " Batch writing for multiple summaries
    " Template-based page creation
    " Automatic linking between related entries
    " Version control and edit history

DEBUGGING NOTES:
    " Log all API calls and responses
    " Track write success/failure rates
    " Monitor rate limiting and retry logic
    " Validate API key and permissions on startup

PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
"""


# ═══════════════════════════════════════════════════════════════════════════
# IMPLEMENTATION — Phase 1 Stub
# ═══════════════════════════════════════════════════════════════════════════

from typing import Optional, Dict, Any
from dataclasses import dataclass
import os


@dataclass
class NotionWriteResult:
    """
    Result of writing to Notion.

    Attributes:
        success: Whether the write succeeded
        page_id: Notion page ID (if created)
        url: URL to the created page
        error: Error message if failed
        metadata: Additional info
    """

    success: bool
    page_id: Optional[str] = None
    url: Optional[str] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    def __repr__(self) -> str:
        status = "success" if self.success else "failed"
        return f"NotionWriteResult(status={status}, page_id={self.page_id})"


def write_to_notion(
    summary: str,
    title: str,
    tags: Optional[list] = None,
    api_key: Optional[str] = None,
    database_id: Optional[str] = None,
) -> NotionWriteResult:
    """
    Write a research summary to Notion.

    This is a STUB implementation for Phase 1.
    Full Notion API integration comes in Phase 2.

    Args:
        summary: The text content to write
        title: Page title
        tags: Optional tags to apply
        api_key: Notion API key (or use environment variable)
        database_id: Target database ID (or use environment variable)

    Returns:
        NotionWriteResult: Object indicating success/failure

    Example:
        result = write_to_notion(
            summary="AI is advancing rapidly...",
            title="AI Trends 2024",
            tags=["research", "ai"]
        )
        if result.success:
            print(f"Created page: {result.url}")

    Teaching Notes:
        This is a deterministic TOOL function:
        • Takes content → Writes to external service (side effect)
        • Does not decide what to write or how to organize
        • Simply executes the write operation
        • No strategic decisions about content

        Integration considerations:
        - API authentication and error handling
        - Rate limiting (Notion has rate limits)
        - Retry logic for transient failures
        - Content formatting (Markdown → Notion blocks)
    """
    # Get API credentials from environment if not provided
    if api_key is None:
        api_key = os.getenv("NOTION_API_KEY")

    if database_id is None:
        database_id = os.getenv("NOTION_DATABASE_ID")

    # Phase 1: Just log what we would do
    print(f"[NOTION STUB] Would write to Notion:")
    print(f"[NOTION STUB]   Title: {title}")
    print(f"[NOTION STUB]   Summary length: {len(summary)} chars")
    print(f"[NOTION STUB]   Tags: {tags or []}")
    print(f"[NOTION STUB]   API key: {'***' if api_key else 'NOT SET'}")
    print(f"[NOTION STUB]   Database ID: {database_id or 'NOT SET'}")

    # Simulate success
    fake_page_id = "stub_page_12345"
    fake_url = f"https://notion.so/{fake_page_id}"

    return NotionWriteResult(
        success=True,
        page_id=fake_page_id,
        url=fake_url,
        metadata={
            "stub": True,
            "title": title,
            "summary_length": len(summary),
            "tags": tags or [],
        },
    )


def format_for_notion(text: str) -> Dict[str, Any]:
    """
    Convert plain text to Notion block format.

    STUB for Phase 1. Phase 2 will implement proper block formatting.

    Args:
        text: Plain text or Markdown

    Returns:
        dict: Notion block structure

    Teaching Notes:
        Notion uses a block-based content model:
        • Each paragraph, heading, list is a separate block
        • Blocks have types: "paragraph", "heading_1", "bulleted_list_item"
        • Blocks contain rich text arrays with formatting

        Example block structure:
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Hello world"}
                }]
            }
        }
    """
    print(f"[NOTION STUB] format_for_notion: Would format {len(text)} chars")

    # Stub: return simple structure
    return {
        "stub": True,
        "blocks": [
            {
                "type": "paragraph",
                "content": text[:100] + "..." if len(text) > 100 else text,
            }
        ],
    }


# ═══════════════════════════════════════════════════════════════════════════
# FUTURE IMPLEMENTATION NOTES (Phase 2)
# ═══════════════════════════════════════════════════════════════════════════

"""
Phase 2 Implementation Plan:

1. Install Notion SDK:
   pip install notion-client

2. Initialize client:
   from notion_client import Client
   notion = Client(auth=os.environ["NOTION_API_KEY"])

3. Create page in database:
   response = notion.pages.create(
       parent={"database_id": database_id},
       properties={
           "Name": {"title": [{"text": {"content": title}}]},
           "Tags": {"multi_select": [{"name": tag} for tag in tags]}
       },
       children=blocks  # Content blocks
   )

4. Convert Markdown to Notion blocks:
   • Parse Markdown (use markdown parser)
   • Convert headings → heading blocks
   • Convert paragraphs → paragraph blocks
   • Convert lists → list item blocks
   • Convert code → code blocks

5. Handle rich text formatting:
   • **bold** → bold rich text
   • *italic* → italic rich text
   • [links](url) → link annotations
   • Inline code → code annotations

6. Error handling:
   • Invalid API key → clear error message
   • Rate limiting → exponential backoff
   • Invalid database ID → validation on startup
   • Network errors → retry logic

7. Advanced features:
   • Update existing pages instead of always creating new
   • Add relations between pages (link related research)
   • Add custom properties (date, status, priority)
   • Batch operations for multiple summaries

Example Phase 2 implementation:
    from notion_client import Client
    import os

    def write_to_notion(summary, title, tags=None):
        notion = Client(auth=os.environ["NOTION_API_KEY"])

        # Create page
        response = notion.pages.create(
            parent={"database_id": os.environ["NOTION_DATABASE_ID"]},
            properties={
                "Name": {"title": [{"text": {"content": title}}]},
                "Tags": {"multi_select": [{"name": t} for t in (tags or [])]}
            },
            children=[
                {
                    "object": "block",
                    "paragraph": {
                        "rich_text": [{"text": {"content": summary}}]
                    }
                }
            ]
        )

        return NotionWriteResult(
            success=True,
            page_id=response["id"],
            url=response["url"]
        )
"""
