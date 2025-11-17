"""
FLOW CONTROLLER — ORCHESTRATION ENGINE
=======================================

ORGAN METAPHOR:
---------------
The Flow Controller is the CIRCULATORY SYSTEM of the research organism.
It coordinates the flow of data between all the organs, ensuring
each step happens in the right order with the right inputs.

PURPOSE:
--------
Orchestrate the complete research pipeline:
  Plan → Fetch → Clean → Summarize → Store → Log

RESPONSIBILITIES:
-----------------
  1. Accept a MissionRequest from the user
  2. Invoke the Planner Agent to create a plan
  3. Use the Scraper Tool to fetch each source
  4. Use the Cleaner Tool to extract clean text
  5. Invoke the Summarizer Agent to create digests
  6. Use the Notion Tool to store outputs
  7. Use the Logger Tool to record the mission
  8. Handle errors and retry logic at each stage

TEACHING NOTES:
---------------
The Flow Controller demonstrates ORCHESTRATION — it doesn't do the work,
it coordinates the workers. This is a common pattern in complex systems:
a central coordinator that manages multiple specialized subsystems.

Notice how it calls AGENTS (which make decisions) and TOOLS (which execute
commands) in a specific sequence. The controller knows WHEN to invoke each
component, but not HOW each component does its work.

FUTURE EXTENSIONS:
------------------
  • Parallel execution of independent tasks
  • Conditional branching (if summary is low-quality, retry)
  • Partial failure recovery (continue mission despite individual fetch failures)
  • Real-time progress updates for UI

DEBUGGING TIPS:
---------------
  • Log every stage transition with timestamps
  • Track data transformations at each step
  • Monitor for bottlenecks in the pipeline
  • Test error handling for each stage independently
"""

pass
