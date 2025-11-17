"""
THE MIND — PLANNER AGENT CHAPTER
================================

This Streamlit page teaches about the PlannerAgent:
  • What makes it an AGENT (not a TOOL)
  • How it makes autonomous decisions
  • Interactive demonstration of planning logic
  • Visualizations of decision-making process
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from agents.planner_agent import PlannerAgent
from pipeline.mission_model import MissionRequest

# Page configuration
st.set_page_config(
    page_title="Chapter 1: The Mind (Planner Agent)",
    page_icon="🧠",
    layout="wide"
)

# Title and introduction
st.title("🧠 Chapter 1: The Mind — Planner Agent")

st.markdown("""
---

## The Research Organism's Brain

The **PlannerAgent** is the **MIND** of our research organism.
It receives high-level research missions and breaks them down into actionable plans.

But what makes it an **AGENT** rather than just a **TOOL**?

""")

# Agent vs Tool comparison
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🤖 AGENT Characteristics

    The PlannerAgent exhibits:
    - **Autonomous decision-making**
    - **Strategic reasoning**
    - **Adaptive planning**
    - **Self-explanation** of choices

    It doesn't just execute — it **strategizes**.
    """)

with col2:
    st.markdown("""
    ### 🔧 vs. TOOL Characteristics

    A simple tool would just:
    - Accept URLs and return them
    - No judgment or prioritization
    - No source discovery
    - No reasoning about quality

    Just mechanical execution, no intelligence.
    """)

st.markdown("""
---

## Decision-Making Process

The PlannerAgent makes **multiple autonomous decisions**:

1. **Source Strategy**: Should it use provided URLs or discover new ones?
2. **Discovery Method**: Academic sources? News? Technical docs?
3. **Prioritization**: Which sources are highest quality?
4. **Constraint Application**: How to respect max_sources limit?
5. **Reasoning Generation**: Why were these choices made?

Each decision point demonstrates **AGENT INTELLIGENCE**.

---

## Interactive Demo: Watch the Mind Work

Try it yourself! Give the Planner a research topic and watch it make decisions.
""")

# Interactive demonstration
st.subheader("🎮 Try the Planner Agent")

# Input controls
topic = st.text_input(
    "Research Topic",
    value="AI-powered wildfire detection systems",
    help="Enter any research topic you're interested in"
)

col1, col2 = st.columns(2)
with col1:
    max_sources = st.slider(
        "Maximum Sources",
        min_value=1,
        max_value=10,
        value=5,
        help="How many sources should the planner select?"
    )

with col2:
    summary_style = st.selectbox(
        "Summary Style",
        options=["technical", "executive", "casual"],
        help="What style of summary do you want?"
    )

# Option to provide custom URLs
provide_urls = st.checkbox("Provide custom URLs (otherwise planner discovers them)")

custom_urls = []
if provide_urls:
    urls_text = st.text_area(
        "Custom URLs (one per line)",
        value="https://scholar.google.com/\nhttps://arxiv.org/\nhttps://news.google.com/",
        height=100
    )
    custom_urls = [url.strip() for url in urls_text.split('\n') if url.strip()]

# Run planning button
if st.button("🧠 Run Planner Agent", type="primary"):
    st.markdown("### Planning in Progress...")

    # Create planner with debug mode
    planner = PlannerAgent(debug=False)  # We'll show our own debug info

    # Create mission request
    request = MissionRequest(
        topic=topic,
        sources=custom_urls,
        max_sources=max_sources,
        summary_style=summary_style
    )

    # Show request details
    with st.expander("📋 Mission Request Details", expanded=False):
        st.json({
            "topic": request.topic,
            "provided_sources": len(request.sources),
            "max_sources": request.max_sources,
            "summary_style": request.summary_style
        })

    # Execute planning
    with st.spinner("Planner thinking..."):
        plan = planner.create_plan(request)

    # Display results
    st.success("✅ Planning Complete!")

    # Show the plan
    st.markdown("### 📋 Generated Mission Plan")

    st.info(f"**Mission ID**: `{plan.mission_id}`")

    # Reasoning box
    st.markdown("#### 🤔 Agent's Reasoning")
    st.markdown(f"> {plan.reasoning}")

    # Target URLs
    st.markdown(f"#### 🎯 Selected Sources ({len(plan.target_urls)})")

    for i, url in enumerate(plan.target_urls, 1):
        # Try to determine source type for better display
        if 'scholar.google' in url or 'arxiv' in url:
            icon = "📚"
            source_type = "Academic"
        elif 'news' in url or 'reuters' in url or 'bbc' in url:
            icon = "📰"
            source_type = "News"
        elif 'stackoverflow' in url or 'github' in url:
            icon = "💻"
            source_type = "Technical"
        else:
            icon = "🌐"
            source_type = "General"

        st.markdown(f"{i}. {icon} **{source_type}**: `{url}`")

    # Planning statistics
    st.markdown("#### 📊 Planning Statistics")

    stats = planner.get_planning_stats()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Plans Created", stats['total_plans'])
    with col2:
        st.metric("Avg Sources/Plan", f"{stats['avg_sources_per_plan']:.1f}")
    with col3:
        st.metric("Topics Planned", len(stats['topics_planned']))

    # Decision breakdown
    with st.expander("🔍 Decision-Making Breakdown", expanded=True):
        st.markdown("""
        **Decision Points the Agent Made:**

        1. **Source Strategy Decision**:
        """)

        if request.sources:
            st.markdown(f"   - ✓ User provided {len(request.sources)} sources")
            st.markdown("   - ✓ Applied quality scoring and prioritization")
            st.markdown("   - ✓ Validated and deduplicated URLs")
        else:
            st.markdown("   - ✓ No sources provided — autonomous discovery required")
            st.markdown("   - ✓ Analyzed topic for research type (academic, news, technical)")
            st.markdown("   - ✓ Generated appropriate search URLs")

        st.markdown(f"""
        2. **Prioritization Decision**:
           - ✓ Scored each source for quality
           - ✓ Preferred HTTPS and reliable domains
           - ✓ Applied max_sources constraint ({max_sources})

        3. **Transparency Decision**:
           - ✓ Generated human-readable reasoning
           - ✓ Explained strategy and source selection
           - ✓ Provided traceable decision trail
        """)

st.markdown("""
---

## Code Example: How the Agent Works

Here's a simplified view of the PlannerAgent's decision-making:

```python
class PlannerAgent:
    def create_plan(self, request: MissionRequest) -> MissionPlan:
        # DECISION POINT 1: Determine strategy
        if request.sources:
            # User provided sources — validate and prioritize
            urls = self._prioritize_user_sources(request.sources)
        else:
            # No sources — discover autonomously
            urls = self._discover_sources(request.topic)

        # DECISION POINT 2: Apply intelligence
        urls = self._apply_constraints(urls, request.max_sources)

        # DECISION POINT 3: Explain reasoning
        reasoning = self._explain_source_selection(request, urls)

        return MissionPlan(
            mission_id=self._generate_mission_id(),
            topic=request.topic,
            target_urls=urls,
            reasoning=reasoning
        )
```

Notice how each method represents a **decision point** where the agent
**chooses** a strategy, rather than just executing predetermined logic.

---

## Key Takeaway: Agents vs. Tools

| Aspect | Tool (e.g., Scraper) | Agent (e.g., Planner) |
|--------|---------------------|----------------------|
| **Purpose** | Execute specific function | Make strategic decisions |
| **Input** | Explicit parameters | High-level goals |
| **Logic** | Deterministic | Heuristic + adaptive |
| **Output** | Raw data | Reasoned plan |
| **Transparency** | Logs execution | Explains reasoning |

The PlannerAgent is an **AGENT** because it exhibits:
- **Autonomy**: Makes decisions independently
- **Intelligence**: Applies heuristics and reasoning
- **Adaptability**: Changes strategy based on context
- **Transparency**: Explains its choices

---

## Next Steps

Continue to **Chapter 2: The Crawler Limb** to see how a **TOOL** differs
from an agent, and why that distinction matters for building intelligent systems.

Or try modifying the topic above and see how the Planner's decisions change!
""")

# Sidebar with navigation
with st.sidebar:
    st.markdown("## 📚 Chapter Navigation")
    st.markdown("""
    **Current**: Chapter 1 - The Mind

    **Next Chapters**:
    - Ch 2: The Crawler Limb
    - Ch 3: The Cleaner Stomach
    - Ch 4: The Summarizer Tongue
    - Ch 5: The Notion Hand
    - Ch 6: Agent vs Tool Anatomy
    - Ch 7: Pipeline Flow Visualizer
    - Ch 8: Mission Console
    - Ch 9: Mission Archive
    - Ch 10: Engineering Legacy
    """)

    st.markdown("---")
    st.markdown("### 🎓 Learning Objectives")
    st.markdown("""
    By the end of this chapter, you should understand:
    - ✅ What makes something an AGENT
    - ✅ How agents make decisions
    - ✅ Why reasoning matters
    - ✅ The difference between agents and tools
    """)
