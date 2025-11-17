"""
THE TONGUE — SUMMARIZER AGENT
==============================

ORGAN METAPHOR:
---------------
The Summarizer is the TONGUE of the research organism.
It tastes the cleaned content and produces narrative explanations,
digests, and summaries tailored to the mission's purpose.

ASCII DIAGRAM:
--------------
                ┌──────────────────────────┐
                │   CLEAN TEXT INPUT       │
                │   (from Cleaner)         │
                └────────────┬─────────────┘
                             │
                             ▼
                ┌──────────────────────────┐
                │   SUMMARIZER AGENT       │
                │       (TONGUE)           │
                │    [AUTONOMOUS]          │
                │                          │
                │  ╔════════════════╗      │
                │  ║  DECIDE:       ║      │
                │  ║  • Tone        ║      │
                │  ║  • Length      ║      │
                │  ║  • Focus       ║      │
                │  ╚════════════════╝      │
                └────────────┬─────────────┘
                             │
                ┌────────────┼────────────┐
                ▼            ▼            ▼
          [Technical]  [Executive]  [Casual]
             style       summary      digest
                             │
                             ▼
                ┌──────────────────────────┐
                │   NARRATIVE OUTPUT       │
                │   "AI wildfire systems   │
                │    use thermal imaging"  │
                └──────────────────────────┘

AGENT vs TOOL:
--------------
This is an AGENT because it:
  • Makes decisions about tone, length, and focus
  • Chooses what to emphasize or omit
  • Adapts output style based on mission context (technical, casual, trend-focused)
  • Exhibits creative and editorial judgment

RESPONSIBILITIES:
-----------------
  1. Receive cleaned text from the Cleaner Tool
  2. Analyze content for key insights and themes
  3. Generate narrative summaries in the requested style
  4. Format output for consumption by humans or downstream tools
  5. Score the quality and relevance of the summary

TEACHING NOTES:
---------------
The Summarizer demonstrates "creative intelligence" — it doesn't just extract,
it interprets and narrates. This is what separates it from a simple keyword
extractor or text truncator.

FUTURE EXTENSIONS:
------------------
  • Multi-perspective summaries (technical vs. executive)
  • Trend analysis across multiple sources
  • Integration with LLM APIs for advanced summarization
  • Sentiment and tone detection

DEBUGGING TIPS:
---------------
  • Compare summaries against source text for accuracy
  • Monitor for hallucinations or over-generalization
  • Track summary length vs. source length ratios
"""

pass
