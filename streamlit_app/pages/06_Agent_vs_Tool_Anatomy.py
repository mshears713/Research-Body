"""
═══════════════════════════════════════════════════════════════
CHAPTER 6: AGENT VS TOOL ANATOMY
═══════════════════════════════════════════════════════════════

TEACHING PURPOSE:
-----------------
This chapter demonstrates the CORE DISTINCTION between Agents and Tools —
the foundational concept of the entire Research Body project.

Through interactive examples, visualizations, and comparisons, learners
will understand:
  • What makes something an AGENT vs a TOOL
  • When to use each pattern
  • How they work together in the pipeline
  • Real examples from the codebase

This is the MOST IMPORTANT chapter for understanding the architecture.

EDUCATIONAL STRATEGY:
---------------------
1. Clear definitions with examples
2. Side-by-side comparisons
3. Interactive demonstrations
4. Decision trees for choosing Agent vs Tool
5. Code examples from the actual codebase

═══════════════════════════════════════════════════════════════
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from src.agents.planner_agent import PlannerAgent
from src.agents.summarizer_agent import SummarizerAgent
from src.tools.scraper_tool import ScraperTool
from src.tools.cleaner_tool import CleanerTool
from src.pipeline.mission_model import MissionRequest


# Page configuration
st.set_page_config(
    page_title="Agent vs Tool Anatomy",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 Chapter 6: Agent vs Tool Anatomy")

st.markdown("""
## The Core Distinction

The Research Body is built on a fundamental architectural principle:
**separating decision-making (AGENTS) from execution (TOOLS)**.

This chapter teaches you to recognize the difference and apply it in your own systems.
""")

# ═══════════════════════════════════════════════════════════════
# SECTION 1: DEFINITIONS
# ═══════════════════════════════════════════════════════════════

st.header("📖 Definitions")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🧠 AGENTS")
    st.markdown("""
    **Agents are AUTONOMOUS DECISION-MAKERS.**

    Characteristics:
    - **Make decisions** based on context
    - **Have internal logic** for reasoning
    - **Adapt behavior** to different situations
    - **Maintain state** across operations
    - **Explain their reasoning**

    Examples in Research Body:
    - **PlannerAgent** (The Mind)
    - **SummarizerAgent** (The Tongue)
    - **ScraperAgent** (Phase 5 upgrade)

    Think of agents as **intelligent workers** who understand
    the *why* behind their actions.
    """)

with col2:
    st.subheader("🔧 TOOLS")
    st.markdown("""
    **Tools are DETERMINISTIC EXECUTORS.**

    Characteristics:
    - **Execute commands** exactly as given
    - **No decision-making** capability
    - **Consistent behavior** (same input → same output)
    - **Stateless** (no memory between calls)
    - **Fast and predictable**

    Examples in Research Body:
    - **ScraperTool** (The Crawler Limb)
    - **CleanerTool** (The Stomach)
    - **NotionTool** (The Hand)
    - **LoggerTool** (The Memory)

    Think of tools as **reliable machines** that do exactly
    what they're told, every time.
    """)

# ═══════════════════════════════════════════════════════════════
# SECTION 2: SIDE-BY-SIDE COMPARISON
# ═══════════════════════════════════════════════════════════════

st.header("⚖️ Side-by-Side Comparison")

comparison_data = {
    "Characteristic": [
        "Decision Making",
        "Internal Logic",
        "Adaptability",
        "State",
        "Predictability",
        "Speed",
        "Complexity",
        "Testing",
        "Example Task"
    ],
    "AGENT 🧠": [
        "YES - Makes autonomous choices",
        "YES - Has reasoning/planning logic",
        "HIGH - Adapts to context",
        "Stateful - Remembers context",
        "Variable - Depends on input",
        "Slower (more processing)",
        "Higher complexity",
        "Harder - Multiple paths",
        "\"Decide which sources to fetch\""
    ],
    "TOOL 🔧": [
        "NO - Executes commands",
        "NO - Pure transformation",
        "LOW - Consistent behavior",
        "Stateless - No memory",
        "High - Same in → same out",
        "Faster (direct execution)",
        "Lower complexity",
        "Easier - Deterministic",
        "\"Fetch this specific URL\""
    ]
}

st.table(comparison_data)

# ═══════════════════════════════════════════════════════════════
# SECTION 3: INTERACTIVE DEMONSTRATIONS
# ═══════════════════════════════════════════════════════════════

st.header("🎮 Interactive Demonstrations")

st.markdown("### Demonstration 1: PlannerAgent vs Simple URL List")

demo_topic = st.text_input(
    "Enter a research topic:",
    value="AI wildfire detection systems",
    key="demo_topic"
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("🧠 AGENT: PlannerAgent")
    st.markdown("**Decision-making in action:**")

    if st.button("Run PlannerAgent", key="run_planner"):
        with st.spinner("Planner is thinking..."):
            planner = PlannerAgent(debug=False)
            request = MissionRequest(
                topic=demo_topic,
                max_sources=3
            )
            plan = planner.create_plan(request)

            st.success("Plan created!")
            st.write(f"**Mission ID:** `{plan.mission_id}`")
            st.write(f"**Reasoning:**\n{plan.reasoning}")
            st.write("**Selected URLs:**")
            for i, url in enumerate(plan.target_urls, 1):
                st.write(f"{i}. `{url}`")

            st.info("""
            **Notice:** The agent DECIDED which URLs to use based on:
            - Topic analysis
            - Source quality heuristics
            - Strategic thinking about research needs
            """)

with col2:
    st.subheader("🔧 TOOL: Simple URL List")
    st.markdown("**Deterministic execution:**")

    urls_input = st.text_area(
        "Provide specific URLs (one per line):",
        value="https://example.com/page1\nhttps://example.com/page2\nhttps://example.com/page3",
        key="urls_input"
    )

    if st.button("Process URLs", key="run_tool"):
        urls = [url.strip() for url in urls_input.split('\n') if url.strip()]

        st.success("URLs processed!")
        st.write("**URLs to fetch:**")
        for i, url in enumerate(urls, 1):
            st.write(f"{i}. `{url}`")

        st.info("""
        **Notice:** The tool just takes what you give it.
        No decisions, no reasoning, just execution.
        If you give it bad URLs, it will try to fetch them anyway.
        """)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════
# SECTION 4: DECISION TREE
# ═══════════════════════════════════════════════════════════════

st.header("🌳 Decision Tree: Agent or Tool?")

st.markdown("""
Use this decision tree when designing new components:
""")

st.code("""
┌─────────────────────────────────────┐
│  Does the component need to make    │
│  DECISIONS based on context?        │
└───────────┬─────────────────────────┘
            │
      ┌─────┴─────┐
      │           │
    YES          NO
      │           │
      ▼           ▼
  ┌───────┐   ┌──────┐
  │ AGENT │   │ TOOL │
  └───┬───┘   └──┬───┘
      │          │
      ▼          ▼
Examples:     Examples:
• Planner     • Scraper
• Summarizer  • Cleaner
• Analyzer    • Logger
              • Notion

Ask yourself:
─────────────
1. Does it choose WHAT to do? → AGENT
2. Does it decide HOW MUCH?   → AGENT
3. Does it adapt strategy?    → AGENT

4. Does it just transform?    → TOOL
5. Same input → Same output?  → TOOL
6. No reasoning required?     → TOOL
""", language="text")

# ═══════════════════════════════════════════════════════════════
# SECTION 5: CODE EXAMPLES
# ═══════════════════════════════════════════════════════════════

st.header("💻 Code Examples from the Codebase")

st.markdown("### Agent Example: PlannerAgent")

st.code('''
class PlannerAgent:
    """AGENT: Makes decisions about research strategy"""

    def create_plan(self, request: MissionRequest) -> MissionPlan:
        """
        AUTONOMOUS DECISION-MAKING:
        - Analyzes the topic
        - CHOOSES which sources to fetch
        - DECIDES how to prioritize them
        - GENERATES reasoning
        """
        # DECISION POINT 1: User sources or discover our own?
        if request.sources:
            target_urls = self._prioritize_user_sources(...)
        else:
            target_urls = self._discover_sources(...)  # AGENT DECIDES

        # DECISION POINT 2: Quality scoring
        scored_sources = [(url, self._score_source_quality(url))
                          for url in target_urls]

        # DECISION POINT 3: Selection and prioritization
        final_urls = self._apply_constraints(...)

        return MissionPlan(
            mission_id=self._generate_mission_id(),
            target_urls=final_urls,
            reasoning=self._explain_source_selection(...)  # EXPLAINS WHY
        )
''', language='python')

st.markdown("### Tool Example: ScraperTool")

st.code('''
class ScraperTool:
    """TOOL: Deterministically fetches URLs"""

    def fetch_url(self, url: str) -> Tuple[str, int, str]:
        """
        DETERMINISTIC EXECUTION:
        - Given a URL, fetch it
        - No decisions about WHAT to fetch
        - No adaptation based on content
        - Just mechanical HTTP GET
        """
        try:
            response = requests.get(
                url,
                headers={'User-Agent': self.user_agent},
                timeout=timeout
            )

            # No decisions - just return what we got
            return (response.text, response.status_code, "")

        except Exception as e:
            # No retry logic - just report failure
            return (None, 0, str(e))
''', language='python')

# ═══════════════════════════════════════════════════════════════
# SECTION 6: WHEN TO UPGRADE TOOL → AGENT
# ═══════════════════════════════════════════════════════════════

st.header("📈 When to Upgrade a Tool to an Agent")

st.markdown("""
Sometimes a TOOL should become an AGENT. This happens when:

1. **You need adaptive behavior** - "Should I retry? Which alternative to try?"
2. **Context matters** - "This source looks low-quality, try another"
3. **Strategic decisions** - "These three links are most relevant"
4. **Learning from feedback** - "This approach worked better last time"

### Example: ScraperTool → ScraperAgent (Phase 5)

In Phase 5, we introduce **ScraperAgent** that can:
- DECIDE whether to retry failed fetches
- CHOOSE alternative sources if primary fails
- ADAPT crawling depth based on content quality
- LEARN which sources are most reliable

This is the evolution from TOOL → AGENT.
""")

st.info("""
**Rule of Thumb:**
- If you find yourself adding lots of if/else logic to a tool → Consider making it an agent
- If a tool needs to "remember" past operations → Consider making it an agent
- If behavior should vary based on context → Consider making it an agent
""")

# ═══════════════════════════════════════════════════════════════
# SECTION 7: HOW THEY WORK TOGETHER
# ═══════════════════════════════════════════════════════════════

st.header("🤝 How Agents and Tools Work Together")

st.markdown("""
The Research Body orchestrates Agents and Tools in a coordinated pipeline:
""")

st.code("""
PIPELINE FLOW:
══════════════

1. PlannerAgent (🧠)          → DECIDES what to research
   ↓
2. ScraperTool (🔧)           → EXECUTES fetching
   ↓
3. CleanerTool (🔧)           → EXECUTES cleaning
   ↓
4. SummarizerAgent (🧠)       → DECIDES how to summarize
   ↓
5. NotionTool (🔧)            → EXECUTES writing
   ↓
6. LoggerTool (🔧)            → EXECUTES logging

PATTERN:
--------
Agents decide WHAT and WHY
Tools execute HOW

This separation of concerns creates:
• Testable components
• Reusable tools
• Explainable decisions
• Maintainable architecture
""", language="text")

# ═══════════════════════════════════════════════════════════════
# SECTION 8: KEY TAKEAWAYS
# ═══════════════════════════════════════════════════════════════

st.header("🎯 Key Takeaways")

st.success("""
### Remember These Principles:

**1. Agents Decide, Tools Execute**
- Agents have autonomy and reasoning
- Tools are deterministic and reliable

**2. Not Everything Needs to be an Agent**
- Start simple with tools
- Upgrade to agents only when decisions are needed

**3. Separation of Concerns**
- Keep decision logic in agents
- Keep transformations in tools
- Don't mix the two

**4. Agents Use Tools**
- Agents make decisions *about* what tools to use
- Agents don't do the work themselves
- Tools are the "hands" that agents command

**5. Both Are Essential**
- A system of only agents is chaotic
- A system of only tools is inflexible
- The combination creates intelligent automation
""")

st.markdown("---")

st.markdown("""
### Next Steps

Now that you understand Agents vs Tools, explore:
- **Chapter 7**: Pipeline Flow Visualizer - See them work together
- **Chapter 8**: Mission Console - Run complete missions
- **Chapter 10**: Engineering Legacy - Design your own agents and tools

### Further Reading

Check the source code:
- `src/agents/` - Agent implementations
- `src/tools/` - Tool implementations
- `src/pipeline/flow_controller.py` - Orchestration logic
""")

# Footer
st.markdown("---")
st.caption("Research Body - Phase 3: Pipeline Integration | Chapter 6: Agent vs Tool Anatomy")
