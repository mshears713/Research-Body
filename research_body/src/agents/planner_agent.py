"""
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
THE MIND  PlannerAgent
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP

ORGAN METAPHOR:
    The Mind is the strategic decision-making center of the Research Body.
    Just as the brain interprets sensory input and creates action plans,
    the PlannerAgent interprets a user's research mission and breaks it down
    into actionable tasks for the rest of the organism.

PURPOSE:
    " Parse user missions (e.g., "Research wildfire trends in California")
    " Break down complex requests into structured tasks
    " Determine which sources to investigate
    " Set priorities and orchestrate the pipeline

AGENT vs TOOL:
     AGENT  Makes autonomous decisions about task breakdown
     NOT a tool  Does not passively transform input to output

    The PlannerAgent reasons about:
    - What sources are most relevant
    - How to prioritize multiple research angles
    - When to expand or narrow the search scope

TEACHING GOALS:
    This module demonstrates what makes something an "agent":
    1. Decision-making logic (not just data transformation)
    2. Context-aware planning
    3. Strategic reasoning about mission objectives

FUTURE EXTENSIONS:
    " Multi-step refinement (iterative planning)
    " Learning from past mission results
    " Integration with external knowledge bases
    " Cost-aware planning (prioritize by effort vs value)

DEBUGGING NOTES:
    " Log all planning decisions with reasoning
    " Track which tasks were generated and why
    " Monitor plan quality metrics over time

PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
"""


"""
ASCII DIAGRAM — THE MIND AT WORK:

                        ┌─────────────────────────────┐
                        │   USER MISSION REQUEST      │
                        │  "Research wildfire trends  │
                        │   in California 2024"       │
                        └─────────────┬───────────────┘
                                      │
                                      ▼
                        ┌─────────────────────────────┐
                        │     PLANNER AGENT MIND      │
                        │    ╔═══════════════════╗    │
                        │    ║  REASONING ENGINE ║    │
                        │    ║  • Analyze intent ║    │
                        │    ║  • Identify topics║    │
                        │    ║  • Prioritize     ║    │
                        │    ║  • Generate plan  ║    │
                        │    ╚═══════════════════╝    │
                        └─────────────┬───────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    ▼                                   ▼
          ┌──────────────────┐              ┌──────────────────┐
          │  TASK 1          │              │  TASK 2          │
          │  Fetch: CA.gov   │              │  Fetch: news.com │
          │  Priority: HIGH  │              │  Priority: MED   │
          └──────────────────┘              └──────────────────┘
                    │                                   │
                    └─────────────────┬─────────────────┘
                                      ▼
                          [ Pipeline Execution ]

Key Insight: The Mind doesn't fetch or clean data itself.
             It DECIDES what to do and delegates execution to tools.
"""


# Implementation begins in Phase 2
