"""
MISSION MODEL — DATA STRUCTURES
================================

PURPOSE:
--------
This module defines the core data structures for research missions.
A Mission represents a complete research task from planning to completion.

KEY CLASSES:
------------
  • MissionRequest: User input (topic, sources, preferences)
  • MissionPlan: Output from Planner Agent (task breakdown)
  • MissionResult: Final output (summaries, metadata, status)

TEACHING NOTES:
---------------
These data structures act as contracts between the different organs.
The Planner produces a MissionPlan, which the pipeline uses to coordinate
fetching, cleaning, and summarization. The final MissionResult is what
gets logged and written to Notion.

Think of these as the "nervous system signals" passed between organs.

FUTURE EXTENSIONS:
------------------
  • Validation schemas (Pydantic models)
  • Versioning for backwards compatibility
  • Support for complex multi-step missions
  • Status tracking and progress updates

DEBUGGING TIPS:
---------------
  • Validate all required fields are present
  • Log data structure contents at each pipeline stage
  • Monitor for schema drift as the system evolves
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class MissionRequest:
    """
    User input for a research mission.

    This represents the raw user intent before any processing.
    The Planner Agent will receive this and transform it into a MissionPlan.
    """
    topic: str                          # Research topic or question
    sources: List[str] = field(default_factory=list)  # Optional specific URLs
    max_sources: int = 5                # Maximum number of sources to fetch
    summary_style: str = "technical"    # technical, executive, casual
    output_format: str = "markdown"     # markdown, plain, html

    # TEACHING NOTE: This is a simple data container. No logic, just state.


@dataclass
class MissionPlan:
    """
    Output from the Planner Agent.

    This represents the decomposed research strategy:
    which URLs to fetch, in what order, and why.
    """
    mission_id: str                     # Unique identifier for this mission
    topic: str                          # Original research topic
    target_urls: List[str]              # URLs to fetch, in priority order
    reasoning: str = ""                 # Why these sources were chosen
    created_at: datetime = field(default_factory=datetime.now)

    # TEACHING NOTE: Notice how this includes "reasoning" — that's the
    # Planner Agent's decision-making made explicit.


@dataclass
class MissionResult:
    """
    Final output from the complete pipeline.

    This contains everything: raw data, cleaned data, summaries,
    metadata, and status information.
    """
    mission_id: str                     # Links back to the MissionPlan
    topic: str                          # Original research topic
    summaries: List[str] = field(default_factory=list)  # Generated summaries
    raw_html: Dict[str, str] = field(default_factory=dict)  # URL → HTML
    clean_text: Dict[str, str] = field(default_factory=dict)  # URL → text
    metadata: Dict[str, any] = field(default_factory=dict)   # Scores, timestamps
    status: str = "pending"             # pending, in_progress, completed, failed
    error_message: Optional[str] = None # If status == failed
    completed_at: Optional[datetime] = None

    # TEACHING NOTE: This is the "receipt" for a completed mission.
    # Everything needed for logging, display, or analysis is here.
