"""
THE MIND — PLANNER AGENT
========================

ORGAN METAPHOR:
---------------
The Planner is the MIND of the research organism.
It receives a high-level research mission and breaks it down into actionable tasks.

ASCII DIAGRAM:
--------------
                     ┌─────────────────────┐
                     │   USER REQUEST      │
                     │ "Research wildfire  │
                     │   containment AI"   │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │   PLANNER AGENT     │
                     │      (MIND)         │
                     │   [AUTONOMOUS]      │
                     └──────────┬──────────┘
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
              ┌──────────┐ ┌────────┐ ┌──────────┐
              │ Task 1:  │ │Task 2: │ │ Task 3:  │
              │Fetch URL1│ │URL2    │ │ URL3     │
              └──────────┘ └────────┘ └──────────┘
                    │           │           │
                    └───────────┼───────────┘
                                ▼
                        [MISSION PLAN]

AGENT vs TOOL:
--------------
This is an AGENT because it:
  • Makes autonomous decisions about how to decompose a mission
  • Chooses which sources to prioritize
  • Adapts its plan based on mission context
  • Exhibits reasoning and strategic thinking

RESPONSIBILITIES:
-----------------
  1. Parse user mission requests
  2. Identify key topics and research angles
  3. Generate a list of target URLs or search queries
  4. Prioritize sources by relevance
  5. Create a task list for downstream organs

TEACHING NOTES:
---------------
The Planner demonstrates "planning intelligence" — it doesn't just execute,
it designs the research strategy. Compare this to the Scraper TOOL, which
simply fetches what it's told to fetch.

FUTURE EXTENSIONS:
------------------
  • Multi-turn planning (iterative refinement)
  • Integration with search APIs for dynamic source discovery
  • Learning from past mission success rates

DEBUGGING TIPS:
---------------
  • Log the full plan before execution
  • Track which URLs were selected and why
  • Monitor edge cases: vague missions, overly broad topics
"""

pass
