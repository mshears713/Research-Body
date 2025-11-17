This project builds a fully modular “organ-system research organism” whose body parts map directly onto AI agents and tools, forming a complete information-gathering and summarization pipeline.

The system teaches the critical difference between:
	•	Agents (autonomous, deciding subsystems)
	•	Tools (deterministic, passive functions)

This README defines every module, every phase, and every step that Claude Code will use to build a pedagogical, narrative-lit codebase.

⸻

	1.	TEACHING GOALS

⸻

PRIMARY GOALS:
	•	Understand the difference between AGENTS and TOOLS
	•	Build a real orchestrator using these principles
	•	Learn architecture, modular design, and pipeline flow
	•	Build a Streamlit “Anatomy Console” with 10 chapters
	•	Learn scraping, cleaning, summarization, Notion integration

SECONDARY GOALS:
	•	Async programming
	•	Text extraction patterns
	•	Persistent state via SQLite
	•	Code clarity, debugging strategies
	•	UI state management

⸻

	2.	AGENTS VS TOOLS — CONCEPTUAL METAPHOR

⸻

The system simulates a “research body,” where each organ corresponds to either an Agent or a Tool.

AGENTS (independent decision-making):
	•	Planner Mind — interprets the mission, designs tasks
	•	Summarizer Tongue — converts cleaned content into explanations
	•	(Optional Upgrade) ScraperAgent Limb — learns to choose sources and retry intelligently

TOOLS (deterministic helpers):
	•	Scraper Crawler Limb — fetches raw pages
	•	Cleaner Stomach — extracts relevant content
	•	Notion Hand — writes digests into Notion
	•	History Logger — records mission runs

This split teaches where reasoning belongs.

⸻

	3.	HIGH-LEVEL ARCHITECTURE (ASCII DIAGRAM)
                  THE LIVING RESEARCH BODY
                (AGENT + TOOL ORGANISM MODEL)

                        ┌───────────┐
                        │  MIND     │
                        │PlannerAgent│
                        └─────┬─────┘
                              │ plan
                     ┌────────▼─────────┐
                     │  LIMB (TOOL)     │
                     │ Scraper Crawler  │
                     └────────┬─────────┘
                              │ raw pages
                  ┌───────────▼───────────┐
                  │     STOMACH (TOOL)    │
                  │     Cleaner Tool      │
                  └──────────┬────────────┘
                              │ clean text
                    ┌─────────▼───────────┐
                    │  TONGUE (AGENT)     │
                    │ SummarizerAgent     │
                    └─────────┬───────────┘
                              │ narrative output
               ┌──────────────▼──────────────┐
               │   HAND (TOOL) → Notion       │
               └──────────────┬──────────────┘
                              │
                     ┌────────▼────────┐
                     │ MEMORY LOGGER   │
                     └─────────────────┘	4.	DIRECTORY STRUCTURE

⸻

research_body/
streamlit_app/
Home.py
pages/
01_The_Mind_Planner.py
02_The_Crawler_Limb.py
03_The_Cleaner_Stomach.py
04_The_Summarizer_Tongue.py
05_The_Notion_Hand.py
06_Agent_vs_Tool_Anatomy.py
07_Pipeline_Flow_Visualizer.py
08_Mission_Console.py
09_Mission_Archive.py
10_Engineering_Legacy.py
assets/
src/
agents/
planner_agent.py
summarizer_agent.py
scraper_agent.py (added in Phase 5)
tools/
scraper_tool.py
cleaner_tool.py
notion_tool.py
logger_tool.py
pipeline/
mission_model.py
flow_controller.py
utils/
text_cleaning.py
extraction.py
scoring.py
config/
default_mission.yaml
data/
missions.sqlite
caches/
README.md

⸻

	5.	STREAMLIT ANATOMY CONSOLE (10 CHAPTERS)

⸻

Each chapter teaches a subsystem of the research organism.
	1.	The Mind (PlannerAgent)
	2.	The Crawler Limb (Scraper Tool)
	3.	The Cleaner Stomach
	4.	The Summarizer Tongue
	5.	The Notion Hand
	6.	Anatomy of Agents vs Tools
	7.	The Pipeline Flow Visualizer
	8.	Mission Console (Run a mission)
	9.	Archive Browser
	10.	Engineering Legacy (future extensions)

Each page must include:
	•	Markdown teaching narrative
	•	Interactive sliders, dropdowns, or examples
	•	Inline visualizations (Plotly/Matplotlib)
	•	Code snippets that reference backend modules

⸻

	6.	PHASES + STEPS (FULL 5-PHASE, 50-STEP PLAN)

⸻

Claude Code must not modify the README after Phase 1.
Claude Code must execute exactly the steps in each phase.
All files must include:
	•	narrative header docstring
	•	ASCII diagrams (where relevant)
	•	inline teaching commentary
	•	debugging notes
	•	future extension suggestions

────────────────────────────────────────────────────────────
PHASE 1 — FOUNDATIONS (10 STEPS)
────────────────────────────────────────────────────────────
	1.	Create directory structure exactly as specified.
	2.	Create empty module files for agents and tools.
	3.	Add header docstrings describing the organ metaphor + purpose.
	4.	Add ASCII diagrams to planner, scraper, cleaner, summarizer modules.
	5.	Create mission_model.py with a stub MissionRequest class.
	6.	Create default_mission.yaml with annotated placeholders.
	7.	Initialize scraper_tool.py with a simple “fetch_url(url)” stub.
	8.	Create cleaner_tool.py with HTML/text parsing stubs.
	9.	Create notion_tool.py and logger_tool.py stubs.
	10.	Create Streamlit Home.py with overview narrative.

────────────────────────────────────────────────────────────
PHASE 2 — AGENT & TOOL BASICS (10 STEPS)
────────────────────────────────────────────────────────────
11. Implement PlannerAgent: break a user request into tasks.
12. Implement Scraper Tool: synchronous fetch + user-agent headers.
13. Implement Cleaner Tool: deterministic cleaning + extraction.
14. Implement SummarizerAgent: summarization logic + tone selection.
15. Implement Notion Tool: API client stub + placeholder write action.
16. Implement Logger Tool: timestamped JSON or SQLite entry.
17. Add utils for text extraction and scoring.
18. Add diagrams describing agent/tool data flow.
19. Add debugging helpers to each subsystem.
20. Build Streamlit Chapter 1 (The Mind).

────────────────────────────────────────────────────────────
PHASE 3 — PIPELINE INTEGRATION (10 STEPS)
────────────────────────────────────────────────────────────
21. Implement flow_controller.py to orchestrate all tools/agents.
22. Add mission lifecycle: plan → fetch → clean → summarize.
23. Add scoring system for relevance and quality.
24. Add error handling and retry logic.
25. Extend cleaner to support structured extraction.
26. Extend summarizer with “trend analysis” mode.
27. Connect Notion tool to mission results.
28. Connect Logger to all mission runs.
29. Update Streamlit Chapters 2–5 to visualize each organ system.
30. Build Agent vs Tool Anatomy page.

────────────────────────────────────────────────────────────
PHASE 4 — STREAMLIT CONSOLE (10 STEPS)
────────────────────────────────────────────────────────────
31. Implement Pipeline Flow Visualizer page.
32. Add live run display (fetch → clean → summarize).
33. Add “organ health” widgets showing subsystem performance.
34. Add toggles to switch scraper from TOOL → AGENT mode (Phase 5 preview).
35. Build Mission Console page (run mission interactively).
36. Add caching + rerun logic.
37. Build Archive Browser page.
38. Add Plotly visualizations of extracted text lengths and scores.
39. Add global sidebar linking subsystem pages.
40. Add teaching narratives about orchestration patterns.

────────────────────────────────────────────────────────────
PHASE 5 — HYBRIDIZATION & EXTENSION (10 STEPS)
────────────────────────────────────────────────────────────
41. Implement ScraperAgent upgrade (autonomous crawling logic).
42. Update flow_controller to optionally use ScraperAgent.
43. Add async variants of scraper, cleaner, summarizer.
44. Add mission templates for wildfire research, hardware security, etc.
45. Add cross-mission trend library.
46. Add a final chapter: “Evolution of Agents.”
47. Add debugging suite for agent decision-making.
48. Improve logger to store metadata and summaries.
49. Add export/import for mission configs.
50. Add future-improvements summary across entire codebase.

⸻

	7.	IMPLEMENTATION RULES FOR CLAUDE CODE

⸻

	•	Never modify this README after Phase 1.
	•	Only implement the phase requested by the user.
	•	Each file must include:
	•	narrative header docstring
	•	ASCII diagram (if relevant)
	•	inline teaching commentary
	•	debugging notes
	•	future extension notes
	•	Keep code educational, not minimal.
	•	Follow the directory structure exactly.
	•	Do not skip or merge steps.
	•	Do not add or remove subsystems unless instructed.

⸻

	8.	DEVELOPER SETUP

⸻

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app/Home.py

⸻

	9.	SYSTEM FLOW SUMMARY

⸻

	1.	PlannerAgent interprets request
	2.	Scraper Tool fetches pages
	3.	Cleaner Tool extracts relevant text
	4.	SummarizerAgent produces digests
	5.	Notion Tool stores output
	6.	Logger Tool records run
	7.	Streamlit Console teaches subsystem internals
