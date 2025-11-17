"""
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
THE TONGUE  SummarizerAgent
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP

ORGAN METAPHOR:
    The Tongue translates raw information into digestible narratives.
    Just as the tongue processes food and helps communicate, the SummarizerAgent
    converts cleaned text into meaningful summaries, explanations, and insights
    that can be easily consumed and shared.

PURPOSE:
    " Transform cleaned content into concise summaries
    " Adapt tone and style to mission requirements
    " Extract key insights and trends
    " Generate narrative explanations of research findings

AGENT vs TOOL:
     AGENT  Makes editorial decisions about what to emphasize
     NOT a tool  Does not mechanically extract text

    The SummarizerAgent reasons about:
    - What information is most important to highlight
    - How to structure narratives for clarity
    - What tone matches the audience and purpose
    - How to connect disparate pieces of information

TEACHING GOALS:
    This module demonstrates autonomous summarization:
    1. Strategic content selection (not just truncation)
    2. Tone and style adaptation
    3. Insight synthesis from multiple sources
    4. Context-aware explanation generation

FUTURE EXTENSIONS:
    " Multi-document synthesis
    " Trend analysis across time periods
    " Citation tracking and source attribution
    " Customizable summary templates
    " Fact-checking and verification layers

DEBUGGING NOTES:
    " Log summarization decisions and reasoning
    " Track summary quality metrics
    " Monitor tone consistency
    " Compare summaries against source material

PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
"""


"""
ASCII DIAGRAM — THE TONGUE SPEAKS:

                    ┌────────────────────────────┐
                    │   CLEANED TEXT INPUT       │
                    │  (from Cleaner Tool)       │
                    │  • Article paragraphs      │
                    │  • Key facts               │
                    │  • Statistics              │
                    └──────────┬─────────────────┘
                               │
                               ▼
                    ┌────────────────────────────┐
                    │  SUMMARIZER AGENT TONGUE   │
                    │  ┌──────────────────────┐  │
                    │  │ EDITORIAL REASONING  │  │
                    │  │ • Select key points  │  │
                    │  │ • Choose tone/style  │  │
                    │  │ • Structure narrative│  │
                    │  │ • Synthesize insights│  │
                    │  └──────────────────────┘  │
                    └──────────┬─────────────────┘
                               │
                 ┌─────────────┴──────────────┐
                 ▼                            ▼
        ┌─────────────────┐         ┌─────────────────┐
        │ BRIEF SUMMARY   │         │ DETAILED REPORT │
        │ (100 words)     │         │ (500 words)     │
        │ For quick read  │         │ For deep dive   │
        └─────────────────┘         └─────────────────┘
                 │                            │
                 └─────────────┬──────────────┘
                               ▼
                    [ Notion Hand writes it ]

Key Insight: The Tongue doesn't just truncate text.
             It UNDERSTANDS and RESHAPES content with purpose.
"""


# Implementation begins in Phase 2
