"""
THE HAND — NOTION TOOL
======================

ORGAN METAPHOR:
---------------
The Notion Tool is the HAND of the research organism.
It writes the final digests and summaries into Notion,
creating a persistent knowledge base.

AGENT vs TOOL:
--------------
This is a TOOL because it:
  • Performs deterministic write operations
  • Does not decide WHAT to write or WHERE, only HOW to write it
  • Has no autonomous decision-making capability
  • Simply executes the write command and confirms success

RESPONSIBILITIES:
-----------------
  1. Authenticate with the Notion API
  2. Format summaries into Notion block structure
  3. Write content to specified pages or databases
  4. Handle errors and retry failed writes
  5. Return write confirmation and page URLs

TEACHING NOTES:
---------------
The Notion Tool is purely mechanical. It receives formatted content
and writes it exactly as instructed. It does not judge whether the
content is good, or decide where to put it — those are decisions
made by upstream agents.

FUTURE EXTENSIONS:
------------------
  • Support for rich formatting (tables, images, embeds)
  • Template-based page creation
  • Automatic tagging and categorization
  • Integration with other platforms (Slack, email)

DEBUGGING TIPS:
---------------
  • Log all write attempts with timestamps
  • Monitor API rate limits and quotas
  • Validate Notion block structure before writing
"""

import os
import re
from typing import Dict, List, Optional
from datetime import datetime


class NotionTool:
    """
    THE HAND — Deterministic Notion Writing Tool
    =============================================

    This class encapsulates all Notion API interactions.
    It's a TOOL because it has NO autonomous decision-making.

    TOOL CHARACTERISTICS:
    ---------------------
      • Executes write commands exactly as given
      • No strategy about WHAT or WHERE to write
      • Deterministic: formats content consistently
      • Returns write status without interpretation

    WHY NOT AN AGENT:
    -----------------
    The Notion Tool doesn't decide:
      - What content is worth writing
      - Where to write it
      - How to organize it
      - What to do if writes fail

    It just writes. Period.

    TEACHING NOTE:
    --------------
    This Phase 2 implementation uses a stub API client.
    In production, you would integrate the official Notion SDK.
    But even as a stub, the TOOL behavior is clear: no decisions, just execution.
    """

    def __init__(self, api_key: Optional[str] = None, debug: bool = False):
        """
        Initialize the Notion Tool.

        Args:
            api_key: Notion API key (uses env var NOTION_API_KEY if None)
            debug: Enable detailed logging of write operations
        """
        self.api_key = api_key or os.getenv('NOTION_API_KEY', '')
        self.debug = debug
        self._write_history = []  # Track all writes for debugging
        self._is_authenticated = bool(self.api_key)

    def write_to_notion(
        self,
        content: str,
        page_id: str,
        title: str = "Research Summary"
    ) -> Dict[str, any]:
        """
        Write content to a Notion page.

        This is the core TOOL FUNCTION — deterministic write operation.
        It formats content and sends it to Notion via API (stubbed for now).

        Args:
            content: Markdown or plain text content to write
            page_id: Notion page or database ID
            title: Title for the content block

        Returns:
            Dictionary containing:
            - success: True if write succeeded
            - page_url: URL of the created/updated Notion page
            - blocks_written: Number of blocks written
            - error: Error message if write failed (None on success)
            - metadata: Additional write metadata

        Example:
            >>> notion = NotionTool(api_key="secret_...")
            >>> result = notion.write_to_notion(summary, "abc123", "Wildfire AI Summary")
            >>> if result['success']:
            >>>     print(f"Written to: {result['page_url']}")

        TEACHING NOTE:
        --------------
        This is a STUB implementation for Phase 2.
        In production, you would use the official Notion SDK:
          from notion_client import Client
          notion = Client(auth=self.api_key)
          notion.blocks.children.append(page_id, children=blocks)

        Even as a stub, this demonstrates TOOL behavior: pure execution, no decisions.
        """
        if self.debug:
            print(f"\n[NOTION TOOL] Writing to Notion")
            print(f"[NOTION TOOL] Page ID: {page_id}")
            print(f"[NOTION TOOL] Title: {title}")
            print(f"[NOTION TOOL] Content length: {len(content)} chars")

        # Check authentication (stub)
        if not self._is_authenticated:
            error_msg = "No Notion API key configured. Set NOTION_API_KEY environment variable."
            if self.debug:
                print(f"[NOTION TOOL] ❌ {error_msg}")

            result = {
                'success': False,
                'page_url': None,
                'blocks_written': 0,
                'error': error_msg,
                'metadata': {'timestamp': datetime.now()}
            }
            self._record_write(page_id, title, result)
            return result

        # Format content into Notion blocks
        blocks = self._format_content_blocks(content, title)

        # STUB: Simulate API call
        # In production, this would be:
        # try:
        #     response = self.notion_client.blocks.children.append(
        #         page_id, children=blocks
        #     )
        #     ...
        # except APIResponseError as e:
        #     return error response

        # Simulate successful write
        page_url = f"https://notion.so/{page_id}"

        result = {
            'success': True,
            'page_url': page_url,
            'blocks_written': len(blocks),
            'error': None,
            'metadata': {
                'timestamp': datetime.now(),
                'api_key_present': bool(self.api_key),
                'content_size': len(content),
                'block_count': len(blocks)
            }
        }

        if self.debug:
            print(f"[NOTION TOOL] ✓ Success: {len(blocks)} blocks written")
            print(f"[NOTION TOOL]   URL: {page_url}")

        self._record_write(page_id, title, result)
        return result

    def _format_content_blocks(self, content: str, title: str) -> List[Dict]:
        """
        Format content into Notion block structure.

        DETERMINISTIC FORMATTING:
          • Parse markdown-like syntax
          • Convert to Notion block format
          • Headings → heading blocks
          • Bullet lists → bulleted_list_item blocks
          • Paragraphs → paragraph blocks

        Args:
            content: Raw content string
            title: Title for the first heading

        Returns:
            List of Notion block objects

        TEACHING NOTE:
        --------------
        This is mechanical transformation. No decisions about content,
        just consistent formatting rules applied deterministically.
        """
        blocks = []

        # Add title as heading_1
        if title:
            blocks.append(self._create_heading_block(title, level=1))

        # Split content into lines
        lines = content.split('\n')
        current_paragraph = []

        for line in lines:
            line = line.strip()

            # Skip empty lines
            if not line:
                if current_paragraph:
                    # Flush current paragraph
                    blocks.append(self._create_paragraph_block(' '.join(current_paragraph)))
                    current_paragraph = []
                continue

            # Check for markdown-style headings
            if line.startswith('# '):
                if current_paragraph:
                    blocks.append(self._create_paragraph_block(' '.join(current_paragraph)))
                    current_paragraph = []
                blocks.append(self._create_heading_block(line[2:], level=1))
            elif line.startswith('## '):
                if current_paragraph:
                    blocks.append(self._create_paragraph_block(' '.join(current_paragraph)))
                    current_paragraph = []
                blocks.append(self._create_heading_block(line[3:], level=2))
            elif line.startswith('### '):
                if current_paragraph:
                    blocks.append(self._create_paragraph_block(' '.join(current_paragraph)))
                    current_paragraph = []
                blocks.append(self._create_heading_block(line[4:], level=3))
            # Check for bullet points
            elif line.startswith('- ') or line.startswith('• '):
                if current_paragraph:
                    blocks.append(self._create_paragraph_block(' '.join(current_paragraph)))
                    current_paragraph = []
                blocks.append(self._create_bullet_block(line[2:]))
            # Regular paragraph text
            else:
                current_paragraph.append(line)

        # Flush any remaining paragraph
        if current_paragraph:
            blocks.append(self._create_paragraph_block(' '.join(current_paragraph)))

        return blocks

    def _create_heading_block(self, text: str, level: int = 1) -> Dict:
        """Create a Notion heading block."""
        heading_type = f"heading_{level}"
        return {
            "object": "block",
            "type": heading_type,
            heading_type: {
                "rich_text": [{"type": "text", "text": {"content": text[:2000]}}]  # Notion limit
            }
        }

    def _create_paragraph_block(self, text: str) -> Dict:
        """Create a Notion paragraph block."""
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": text[:2000]}}]
            }
        }

    def _create_bullet_block(self, text: str) -> Dict:
        """Create a Notion bulleted list item block."""
        return {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": text[:2000]}}]
            }
        }

    def _record_write(self, page_id: str, title: str, result: Dict):
        """Record write operation in history for debugging."""
        self._write_history.append({
            'page_id': page_id,
            'title': title,
            'success': result['success'],
            'blocks_written': result.get('blocks_written', 0),
            'error': result.get('error'),
            'timestamp': datetime.now()
        })

    def get_write_stats(self) -> Dict:
        """
        Get statistics about write history.

        DEBUGGING HELPER: Analyze write performance and reliability.

        Returns:
            Dict with success_rate, total_writes, total_blocks, etc.
        """
        if not self._write_history:
            return {
                'total_writes': 0,
                'success_rate': 0.0,
                'total_blocks_written': 0
            }

        total = len(self._write_history)
        successes = sum(1 for w in self._write_history if w['success'])
        total_blocks = sum(w['blocks_written'] for w in self._write_history)

        return {
            'total_writes': total,
            'successes': successes,
            'failures': total - successes,
            'success_rate': successes / total if total > 0 else 0.0,
            'total_blocks_written': total_blocks,
            'avg_blocks_per_write': total_blocks / total if total > 0 else 0.0
        }


# Convenience function for simple one-off writes
def write_to_notion(content: str, page_id: str, title: str = "Research Summary") -> Dict[str, any]:
    """
    Simple convenience function for one-off Notion writes.

    This wraps the NotionTool class for backwards compatibility
    and simple use cases.

    Args:
        content: Markdown or plain text content to write
        page_id: Notion page or database ID
        title: Title for the content block

    Returns:
        Dictionary with success, page_url, blocks_written, error, metadata

    Example:
        >>> result = write_to_notion(summary, "abc123", "Wildfire AI Summary")
        >>> if result['success']:
        >>>     print(f"Written to: {result['page_url']}")

    TEACHING NOTE:
    --------------
    This function creates a new NotionTool instance for each call.
    For repeated writes, use NotionTool directly to track history.
    """
    notion = NotionTool()
    return notion.write_to_notion(content, page_id, title)
