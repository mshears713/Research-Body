# Claude Code Development Guide for Research-Body Project

## Project Overview

This is an **educational AI orchestration project** that teaches the critical difference between **Agents** (autonomous, decision-making subsystems) and **Tools** (deterministic, passive functions) through a biological metaphor of a "research organism."

The system is intentionally **pedagogical** — every file should teach, demonstrate, and guide learners through proper architecture patterns for building AI-powered research pipelines.

---

## Core Philosophy

### The Living Organism Metaphor

```
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
                     └─────────────────┘
```

### Agents vs Tools

**AGENTS** (Decision-Makers):
- Have internal reasoning/planning logic
- Make autonomous decisions
- Adapt to context
- Examples: PlannerAgent, SummarizerAgent, ScraperAgent (Phase 5)

**TOOLS** (Deterministic Helpers):
- Execute predefined tasks
- No decision-making autonomy
- Consistent, predictable output
- Examples: ScraperTool, CleanerTool, NotionTool, LoggerTool

---

## Critical Implementation Rules

### 1. **NEVER Modify README.md After Phase 1**

The README.md is the **master specification**. Once Phase 1 is complete, the README becomes immutable. All subsequent work references it but does not alter it.

### 2. **Follow Phases Sequentially**

The project is divided into 5 phases with 50 total steps:

- **Phase 1**: Foundations (Steps 1-10)
- **Phase 2**: Agent & Tool Basics (Steps 11-20)
- **Phase 3**: Pipeline Integration (Steps 21-30)
- **Phase 4**: Streamlit Console (Steps 31-40)
- **Phase 5**: Hybridization & Extension (Steps 41-50)

**DO NOT skip ahead or merge steps.** Each step builds deliberately on previous work.

### 3. **Mandatory File Components**

Every Python file must include:

1. **Narrative Header Docstring**
   ```python
   """
   ═══════════════════════════════════════════════════════════════
   MODULE NAME: The Organ Name (Agent/Tool)
   ═══════════════════════════════════════════════════════════════

   TEACHING PURPOSE:
   [Explain what this module teaches about agents/tools/orchestration]

   BIOLOGICAL METAPHOR:
   [Describe the organ this represents]

   TECHNICAL RESPONSIBILITY:
   [What this module actually does]

   KEY CONCEPTS:
   - Concept 1
   - Concept 2

   ═══════════════════════════════════════════════════════════════
   """
   ```

2. **ASCII Diagrams** (where relevant)
   - Show data flow
   - Illustrate system position
   - Demonstrate internal logic

3. **Inline Teaching Commentary**
   ```python
   # TEACHING NOTE: This pattern demonstrates how agents maintain state
   # while tools remain stateless. Notice how the planner keeps context
   # across multiple calls, unlike the scraper which resets each time.
   ```

4. **Debugging Notes**
   ```python
   # DEBUG: If planning fails, check the YAML mission format
   # Common issues: missing 'goal' field, invalid URL list
   ```

5. **Future Extension Suggestions**
   ```python
   # FUTURE: Could add multi-language support here
   # FUTURE: Consider implementing rate-limiting for API calls
   ```

### 4. **Code Style Requirements**

- **Educational over minimal**: Add explanatory variable names, comments, and examples
- **Clarity over cleverness**: Use straightforward patterns
- **Narrative over terse**: Help learners understand *why*, not just *what*
- **ASCII art encouraged**: Visual diagrams aid understanding

---

## Directory Structure Reference

```
research_body/
├── streamlit_app/
│   ├── Home.py                          # Landing page with overview
│   └── pages/
│       ├── 01_The_Mind_Planner.py       # Chapter 1: PlannerAgent
│       ├── 02_The_Crawler_Limb.py       # Chapter 2: Scraper Tool
│       ├── 03_The_Cleaner_Stomach.py    # Chapter 3: Cleaner Tool
│       ├── 04_The_Summarizer_Tongue.py  # Chapter 4: SummarizerAgent
│       ├── 05_The_Notion_Hand.py        # Chapter 5: Notion Tool
│       ├── 06_Agent_vs_Tool_Anatomy.py  # Chapter 6: Conceptual comparison
│       ├── 07_Pipeline_Flow_Visualizer.py # Chapter 7: Flow visualization
│       ├── 08_Mission_Console.py        # Chapter 8: Interactive runner
│       ├── 09_Mission_Archive.py        # Chapter 9: History browser
│       └── 10_Engineering_Legacy.py     # Chapter 10: Extensions
│   └── assets/                          # Images, diagrams, etc.
├── src/
│   ├── agents/
│   │   ├── planner_agent.py             # AGENT: Interprets missions
│   │   ├── summarizer_agent.py          # AGENT: Creates narratives
│   │   └── scraper_agent.py             # AGENT: Intelligent crawling (Phase 5)
│   ├── tools/
│   │   ├── scraper_tool.py              # TOOL: Fetches raw pages
│   │   ├── cleaner_tool.py              # TOOL: Extracts clean text
│   │   ├── notion_tool.py               # TOOL: Writes to Notion
│   │   └── logger_tool.py               # TOOL: Records history
│   ├── pipeline/
│   │   ├── mission_model.py             # Data models for missions
│   │   └── flow_controller.py           # Orchestration logic
│   ├── utils/
│   │   ├── text_cleaning.py             # Cleaning utilities
│   │   ├── extraction.py                # Content extraction
│   │   └── scoring.py                   # Quality metrics
│   └── config/
│       └── default_mission.yaml         # Template mission config
├── data/
│   ├── missions.sqlite                  # Mission history database
│   └── caches/                          # Cached scraper results
└── README.md                            # Master specification (immutable)
```

---

## Development Workflow

### Phase-by-Phase Approach

When the user requests a specific phase:

1. **Read the README section** for that phase carefully
2. **Create a TODO list** with all 10 steps for that phase
3. **Implement each step sequentially**, marking as complete
4. **Test each component** after implementation
5. **Commit with clear messages** referencing step numbers

Example workflow for Phase 1:

```bash
# Step 1: Create directory structure
mkdir -p src/{agents,tools,pipeline,utils,config}
mkdir -p streamlit_app/pages
mkdir -p data/caches

# Step 2: Create empty module files
touch src/agents/{planner_agent,summarizer_agent}.py
touch src/tools/{scraper_tool,cleaner_tool,notion_tool,logger_tool}.py

# Continue through all 10 steps...
```

### Git Practices

**Branch**: Always develop on `claude/create-claude-documentation-016f9UW4ooYASGQbwCTLQcJj`

**Commit messages should follow this pattern**:
```
Phase X, Step Y: [Brief description]

[Longer explanation of what was implemented and why]
```

Example:
```
Phase 1, Step 3: Add header docstrings with organ metaphor

Added narrative docstrings to all agent and tool modules explaining:
- The biological metaphor (which organ they represent)
- Their role in the pipeline
- The agent vs tool distinction
```

**Push when complete**:
```bash
git add .
git commit -m "Phase 1: Complete foundation setup (Steps 1-10)"
git push -u origin claude/create-claude-documentation-016f9UW4ooYASGQbwCTLQcJj
```

---

## Streamlit Console Guidelines

Each of the 10 Streamlit pages is a **teaching chapter**. They should:

### Structure Requirements

1. **Title and Chapter Number**
   ```python
   st.title("Chapter 1: The Mind — PlannerAgent")
   ```

2. **Opening Narrative** (2-3 paragraphs)
   - Introduce the organ metaphor
   - Explain the technical role
   - Connect to the overall system

3. **Interactive Demonstration**
   - Sliders for parameters
   - Text inputs for testing
   - Buttons to trigger actions
   - Live output displays

4. **Visual Diagrams**
   - Use Plotly, Matplotlib, or Graphviz
   - Show data flow
   - Illustrate decision trees (for agents)

5. **Code Examples**
   ```python
   with st.expander("View Source Code"):
       st.code('''
       # Actual code from the module with annotations
       ''', language='python')
   ```

6. **Key Takeaways Box**
   ```python
   st.info("""
   ### Key Takeaways
   - Point 1
   - Point 2
   - Point 3
   """)
   ```

### Teaching Narrative Examples

**For Tools** (deterministic):
> "The Cleaner Stomach is a **tool**, not an agent. It doesn't decide *what* to clean—it just cleans what it's given. Notice how it has no internal state, no decision logic, just deterministic transformation rules..."

**For Agents** (autonomous):
> "Unlike the Cleaner, the Planner Mind is a true **agent**. It interprets the mission goal, decides how to break it into tasks, and adapts its strategy based on the research domain. Watch how it reasons..."

---

## Common Patterns and Anti-Patterns

### ✅ DO THIS

**Agent Pattern**:
```python
class PlannerAgent:
    """
    AGENT: Makes decisions about task breakdown
    """
    def __init__(self):
        self.context = {}  # Agents can maintain state

    def plan_mission(self, mission_request):
        # Decision logic here
        # Reasoning, branching, adaptation
        pass
```

**Tool Pattern**:
```python
def scraper_tool(url: str) -> str:
    """
    TOOL: Deterministically fetches a URL
    No decision-making, just execution
    """
    # Pure transformation: URL → HTML
    response = requests.get(url)
    return response.text
```

### ❌ DON'T DO THIS

**Mixing concerns**:
```python
# BAD: Tool making decisions
def scraper_tool(url: str) -> str:
    if "research" in url:
        # Deciding to change behavior = agent behavior
        return fetch_with_retries(url)
    else:
        return fetch_simple(url)
```

**Missing teaching commentary**:
```python
# BAD: No explanation
def clean(html):
    soup = BeautifulSoup(html)
    return soup.get_text()
```

**Correct version**:
```python
# GOOD: Educational
def clean(html: str) -> str:
    """
    TOOL: Deterministic HTML → clean text transformation

    TEACHING NOTE: This is a tool because it applies the same
    cleaning rules regardless of content. It doesn't "decide"
    what's important—that's the SummarizerAgent's job.
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Remove script and style elements
    # (These usually don't contain useful research content)
    for script in soup(["script", "style"]):
        script.decompose()

    return soup.get_text()
```

---

## Testing and Validation

### Per-Phase Validation

After completing each phase, verify:

1. **All files exist** according to directory structure
2. **All files have required components** (docstrings, diagrams, comments)
3. **Code runs without errors** (even if stub/placeholder)
4. **Streamlit pages load** and display correctly
5. **Git commits are clear** and reference specific steps

### Quick Test Commands

```bash
# Validate Python syntax
python -m py_compile src/**/*.py

# Check imports
python -c "from src.agents.planner_agent import PlannerAgent"

# Run Streamlit
streamlit run streamlit_app/Home.py

# Test specific module
python src/tools/scraper_tool.py  # Should have if __name__ == "__main__" block
```

---

## Special Considerations

### Phase 5: The Hybrid ScraperAgent

Phase 5 introduces a special challenge: converting the Scraper from a **Tool** to an **Agent**.

This teaches:
- When to upgrade a tool to an agent
- How to preserve backward compatibility
- The cost/benefit of autonomy

Implementation notes:
```python
# scraper_agent.py (Phase 5)
"""
TEACHING NOTE: Compare this to scraper_tool.py

The ScraperAgent doesn't just fetch URLs—it:
- Decides which links to follow
- Retries intelligently on failures
- Adapts crawling strategy based on content
- Maintains state across multiple fetches

This is the evolution from TOOL → AGENT
"""
```

### Async Patterns (Phase 5)

When adding async variants:
- Keep synchronous versions for teaching comparison
- Add clear comments explaining concurrency
- Show performance differences in Streamlit

---

## Working with User Requests

### Common Request Types

**"Implement Phase X"**
1. Read README Phase X section
2. Create TODO with 10 steps
3. Execute sequentially
4. Commit with phase reference
5. Push to branch

**"Add [feature] to [module]"**
1. Check which phase this belongs to
2. Verify not skipping ahead
3. Implement with full teaching narrative
4. Update relevant Streamlit chapter
5. Add to "Future Extensions" if beyond current phase

**"Fix bug in [module]"**
1. Preserve teaching narrative
2. Add debugging notes
3. Explain the fix pedagogically
4. Update tests/examples

**"Explain how [component] works"**
1. Reference the docstring narrative
2. Point to relevant Streamlit chapter
3. Provide ASCII diagram
4. Show code examples

---

## Debugging Guide

### Common Issues

**Import errors**:
- Verify `__init__.py` files exist
- Check relative vs absolute imports
- Ensure virtual environment is activated

**Streamlit not finding pages**:
- Pages must be in `streamlit_app/pages/`
- Must start with number: `01_Name.py`
- Must have `.py` extension

**Mission execution fails**:
- Check `default_mission.yaml` format
- Verify scraper can reach URLs
- Check cleaner handles HTML variants
- Ensure summarizer has valid input

### Debug Logging Pattern

```python
import logging

logger = logging.getLogger(__name__)

# TEACHING NOTE: Logging helps learners see the pipeline flow
# Add verbose logging to show each transformation step

def process(data):
    logger.info(f"Input type: {type(data)}, length: {len(data)}")
    result = transform(data)
    logger.info(f"Output type: {type(result)}, length: {len(result)}")
    return result
```

---

## Environment Setup

### Initial Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate (Linux/Mac)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Streamlit console
streamlit run streamlit_app/Home.py
```

### Required Dependencies

Create `requirements.txt`:
```
streamlit>=1.28.0
requests>=2.31.0
beautifulsoup4>=4.12.0
pyyaml>=6.0
plotly>=5.17.0
pandas>=2.1.0
notion-client>=2.2.0  # For Notion integration
```

---

## Questions to Ask Before Implementation

When user requests work, verify:

1. **Which phase does this belong to?**
   - Don't implement Phase 3 features during Phase 1

2. **Is this an Agent or a Tool?**
   - Will it make decisions or just transform data?

3. **What does this teach?**
   - Every addition should demonstrate a concept

4. **Where does this fit in the organism?**
   - Which organ/body part is this?

5. **What's the narrative?**
   - How will we explain this in teaching comments?

---

## Success Criteria

### For Each Phase

- [ ] All 10 steps completed in order
- [ ] All files have teaching docstrings
- [ ] ASCII diagrams included where relevant
- [ ] Inline comments explain concepts
- [ ] Code runs without errors
- [ ] Streamlit chapters are interactive
- [ ] Git commits reference specific steps
- [ ] No modifications to README after Phase 1

### For Overall Project

- [ ] Clear distinction between agents and tools
- [ ] Educational narrative throughout
- [ ] Working end-to-end pipeline
- [ ] 10 interactive Streamlit chapters
- [ ] Comprehensive inline documentation
- [ ] Future extension suggestions
- [ ] Debug helpers in place

---

## Example Session Flow

```
User: "Let's implement Phase 1"

Claude:
1. Creates TODO list with Steps 1-10
2. Marks Step 1 as in_progress
3. Creates directory structure
4. Completes Step 1, marks completed
5. Moves to Step 2...
6. [Continues through all 10 steps]
7. Commits: "Phase 1: Complete foundation setup"
8. Pushes to branch

User: "Now add the PlannerAgent implementation"

Claude:
1. Checks README - this is Phase 2, Step 11
2. Verifies Phase 1 is complete
3. Implements with full docstring
4. Adds ASCII diagram
5. Includes teaching commentary
6. Tests import
7. Updates Chapter 1 Streamlit page
8. Commits: "Phase 2, Step 11: Implement PlannerAgent"
```

---

## Key Reminders

1. **This is a TEACHING PROJECT** — verbose, narrative code is better than terse code
2. **The README is IMMUTABLE** after Phase 1 — reference but don't modify
3. **Phases are SEQUENTIAL** — don't skip ahead
4. **Every file is a LESSON** — include teaching narrative
5. **The metaphor MATTERS** — consistently use organ terminology
6. **Agents DECIDE, Tools EXECUTE** — maintain this distinction rigorously

---

## Resources and References

### Internal References
- `README.md` - Master specification
- `streamlit_app/Home.py` - Project overview
- `src/agents/` - Agent implementations
- `src/tools/` - Tool implementations

### External Learning Resources
- Streamlit docs: https://docs.streamlit.io
- BeautifulSoup docs: https://www.crummy.com/software/BeautifulSoup/
- Notion API: https://developers.notion.com

---

## Final Notes

This project is **deliberately pedagogical**. Every line of code, every comment, every diagram serves the goal of teaching proper AI orchestration architecture.

When in doubt:
- Add more explanation, not less
- Draw more diagrams
- Write longer docstrings
- Include more examples
- Make it visual and interactive

The goal is for someone to clone this repo and **learn by reading**, not just by running.

**Happy building! 🧬**
