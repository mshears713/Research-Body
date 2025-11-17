"""
PIPELINE FLOW VISUALIZER — CHAPTER 7
=====================================

This Streamlit page teaches about pipeline orchestration:
  • How data flows through the research organism
  • Transformations at each stage
  • The role of the Flow Controller
  • Interactive visualization of the complete pipeline
"""

import streamlit as st
import sys
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

# Add project root to path for imports
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

# Page configuration
st.set_page_config(
    page_title="Chapter 7: Pipeline Flow Visualizer",
    page_icon="🔄",
    layout="wide"
)

# ============================================================================
# TITLE AND INTRODUCTION
# ============================================================================

st.title("🔄 Chapter 7: Pipeline Flow Visualizer")
st.subheader("*Understanding the Research Organism's Circulatory System*")

st.markdown("---")

st.markdown("""
## The Living Pipeline

Just as blood flows through an organism, delivering nutrients and removing waste,
**data flows through our research organism** — transforming from raw web pages into
polished knowledge.

The **Flow Controller** acts as the **circulatory system**, orchestrating the
movement of information through each organ in the proper sequence.

This chapter visualizes that flow, showing you exactly how a research mission travels
through the body from **conception to completion**.
""")

st.markdown("---")

# ============================================================================
# THE SEVEN STAGES
# ============================================================================

st.markdown("""
## 🎭 The Seven Stages of a Research Mission

Every mission passes through seven distinct stages. Each stage has a specific
purpose and transforms the data in a particular way.
""")

# Create expandable sections for each stage
stages = [
    {
        "number": 1,
        "name": "PLANNING",
        "organ": "The Mind (Planner Agent)",
        "type": "🤖 AGENT",
        "input": "MissionRequest (user's research topic)",
        "output": "MissionPlan (prioritized URLs and strategy)",
        "description": """
**Decision-Making Process:**
- Analyzes the research topic
- Identifies relevant domains and sources
- Prioritizes URLs based on expected relevance
- Creates a reasoning explanation for the strategy

**Key Insight:** This is an AGENT because it makes autonomous decisions about
WHICH sources to fetch and WHY, adapting its strategy based on the topic.
        """
    },
    {
        "number": 2,
        "name": "FETCHING",
        "organ": "The Limb (Scraper Tool)",
        "type": "🔧 TOOL",
        "input": "List of target URLs",
        "output": "Raw HTML pages",
        "description": """
**Execution Process:**
- Makes HTTP GET requests to each URL
- Handles network errors with retry logic
- Captures response status codes and metadata
- Returns raw HTML content

**Key Insight:** This is a TOOL because it executes deterministically — given
a URL, it always performs the same fetch operation with no decision-making.
        """
    },
    {
        "number": 3,
        "name": "CLEANING",
        "organ": "The Stomach (Cleaner Tool)",
        "type": "🔧 TOOL",
        "input": "Raw HTML pages",
        "output": "Clean text (title, content, metadata)",
        "description": """
**Transformation Process:**
- Parses HTML DOM structure
- Removes boilerplate (scripts, styles, navigation)
- Extracts main content text
- Identifies title and metadata

**Key Insight:** This is a TOOL because it applies consistent extraction rules
regardless of content — no judgment about what's "important", just extraction.
        """
    },
    {
        "number": 4,
        "name": "SCORING",
        "organ": "Utility Functions",
        "type": "🔧 TOOL",
        "input": "Clean text from all sources",
        "output": "Quality and relevance scores",
        "description": """
**Calculation Process:**
- Measures keyword relevance (how often topic terms appear)
- Assesses text quality (readability, completeness)
- Calculates readability scores
- Produces composite score (weighted combination)

**Key Insight:** These are TOOLS because they apply mathematical formulas
deterministically — no subjective judgment, just calculations.
        """
    },
    {
        "number": 5,
        "name": "SUMMARIZATION",
        "organ": "The Tongue (Summarizer Agent)",
        "type": "🤖 AGENT",
        "input": "Clean text + quality scores",
        "output": "Tailored narrative summaries",
        "description": """
**Creative Process:**
- Decides what tone to use (technical, executive, casual)
- Determines what to emphasize based on scores
- Adapts length and structure to content
- Synthesizes insights across sources

**Key Insight:** This is an AGENT because it makes subjective decisions about
HOW to present information, adapting its style and emphasis to the context.
        """
    },
    {
        "number": 6,
        "name": "STORAGE",
        "organ": "The Hand (Notion Tool)",
        "type": "🔧 TOOL",
        "input": "Mission results and summaries",
        "output": "Notion database entry",
        "description": """
**Write Process:**
- Formats data for Notion API
- Creates database entry with structured properties
- Stores summaries as page content
- Links related metadata

**Key Insight:** This is a TOOL because it executes a predetermined write
operation — no decisions about WHAT or HOW to organize, just execution.
        """
    },
    {
        "number": 7,
        "name": "LOGGING",
        "organ": "The Memory (Logger Tool)",
        "type": "🔧 TOOL",
        "input": "Complete mission record",
        "output": "SQLite database entry",
        "description": """
**Recording Process:**
- Serializes mission data to JSON
- Stores in SQLite database with timestamp
- Captures success/failure status
- Preserves complete audit trail

**Key Insight:** This is a TOOL because it faithfully records everything
exactly as given — no filtering, no interpretation, just preservation.
        """
    }
]

for stage in stages:
    with st.expander(f"**Stage {stage['number']}: {stage['name']}** — {stage['organ']} ({stage['type']})"):
        st.markdown(f"**Input:** `{stage['input']}`")
        st.markdown(f"**Output:** `{stage['output']}`")
        st.markdown(stage['description'])

st.markdown("---")

# ============================================================================
# INTERACTIVE FLOW DIAGRAM
# ============================================================================

st.markdown("""
## 🗺️ Interactive Flow Diagram

This diagram shows the complete pipeline flow with data transformations at each stage.
Notice how **agents make decisions** (branching logic) while **tools execute deterministically**
(straight-through processing).
""")

# Create a Sankey diagram showing the flow
def create_sankey_diagram():
    """Create a Sankey diagram showing data flow through the pipeline."""

    # Define nodes (stages)
    labels = [
        "User Request",          # 0
        "Planner Agent",         # 1
        "Mission Plan",          # 2
        "Scraper Tool",          # 3
        "Raw HTML",              # 4
        "Cleaner Tool",          # 5
        "Clean Text",            # 6
        "Scoring Utils",         # 7
        "Quality Scores",        # 8
        "Summarizer Agent",      # 9
        "Summaries",             # 10
        "Notion Tool",           # 11
        "Logger Tool",           # 12
        "Stored Results"         # 13
    ]

    # Define connections (source -> target)
    sources = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 10, 10, 11, 12]
    targets =  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 11, 12, 13, 13]
    values =   [1, 1, 5, 5, 5, 5, 5, 5, 5,  3,  3,  3,  3,  3,  3]  # Relative flow amounts

    # Color nodes by type (agent vs tool)
    node_colors = [
        "lightblue",   # User Request
        "lightcoral",  # Planner Agent (AGENT)
        "lightgray",   # Mission Plan
        "lightgreen",  # Scraper Tool (TOOL)
        "lightgray",   # Raw HTML
        "lightgreen",  # Cleaner Tool (TOOL)
        "lightgray",   # Clean Text
        "lightgreen",  # Scoring Utils (TOOL)
        "lightgray",   # Quality Scores
        "lightcoral",  # Summarizer Agent (AGENT)
        "lightgray",   # Summaries
        "lightgreen",  # Notion Tool (TOOL)
        "lightgreen",  # Logger Tool (TOOL)
        "lightyellow"  # Stored Results
    ]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=node_colors
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color="rgba(0,0,0,0.2)"
        )
    )])

    fig.update_layout(
        title="Pipeline Data Flow (Red=Agent, Green=Tool, Gray=Data)",
        font=dict(size=12),
        height=600
    )

    return fig

st.plotly_chart(create_sankey_diagram(), use_container_width=True)

st.info("""
**Legend:**
- 🔴 **Red nodes** = AGENTS (decision-makers)
- 🟢 **Green nodes** = TOOLS (executors)
- ⚪ **Gray nodes** = DATA (transformations)
- 🟡 **Yellow node** = FINAL OUTPUT
""")

st.markdown("---")

# ============================================================================
# STAGE-BY-STAGE DATA TRANSFORMATIONS
# ============================================================================

st.markdown("""
## 📊 Data Transformations

At each stage, data is transformed from one format to another.
Let's trace a sample research mission through the entire pipeline.
""")

# Sample data transformation
sample_topic = st.text_input(
    "Enter a sample research topic:",
    value="AI wildfire detection systems",
    help="We'll show how this topic transforms through each stage"
)

if st.button("Trace Pipeline Flow", type="primary"):
    st.markdown("### 🔬 Pipeline Trace")

    # Stage 1: User Request
    st.markdown("#### Stage 1: User Request")
    st.code(f"""
MissionRequest(
    topic="{sample_topic}",
    max_sources=5,
    summary_style="technical"
)
    """, language="python")
    st.markdown("⬇️ *Sent to Planner Agent*")

    # Stage 2: Planner Agent
    st.markdown("#### Stage 2: Planner Agent Decision-Making")
    st.code(f"""
MissionPlan(
    mission_id="mission_20231117_abc123",
    topic="{sample_topic}",
    target_urls=[
        "https://example.com/ai-wildfire-research",
        "https://example.org/detection-systems",
        "https://university.edu/fire-ai-paper"
    ],
    reasoning="Selected academic and industry sources focusing on
               AI/ML techniques for wildfire detection. Prioritized
               recent research and practical implementations."
)
    """, language="python")
    st.markdown("⬇️ *URLs sent to Scraper Tool*")

    # Stage 3: Scraper Tool
    st.markdown("#### Stage 3: Scraper Tool Fetches HTML")
    st.code("""
raw_html = {
    "https://example.com/ai-wildfire-research": "<html><head>...</head><body>...</body></html>",
    "https://example.org/detection-systems": "<html>... [50KB of HTML] ...</html>",
    "https://university.edu/fire-ai-paper": "<html>... [120KB of HTML] ...</html>"
}
    """, language="python")
    st.markdown("⬇️ *HTML sent to Cleaner Tool*")

    # Stage 4: Cleaner Tool
    st.markdown("#### Stage 4: Cleaner Tool Extracts Text")
    st.code("""
clean_text = {
    "https://example.com/ai-wildfire-research": {
        "title": "AI-Powered Wildfire Detection: A Survey",
        "clean_text": "Wildfires pose a significant threat to ecosystems...
                       Machine learning techniques, particularly convolutional
                       neural networks... [2,500 words of clean text]",
        "word_count": 2500
    },
    "https://example.org/detection-systems": { ... },
    "https://university.edu/fire-ai-paper": { ... }
}
    """, language="python")
    st.markdown("⬇️ *Clean text sent to Scoring*")

    # Stage 5: Scoring
    st.markdown("#### Stage 5: Scoring Calculates Quality")
    st.code("""
scores = {
    "https://example.com/ai-wildfire-research": 0.87,  # High relevance + quality
    "https://example.org/detection-systems": 0.72,     # Good relevance
    "https://university.edu/fire-ai-paper": 0.91       # Excellent academic source
}
    """, language="python")
    st.markdown("⬇️ *Text + scores sent to Summarizer Agent*")

    # Stage 6: Summarizer Agent
    st.markdown("#### Stage 6: Summarizer Agent Creates Narrative")
    st.code("""
summaries = [
    "AI-powered wildfire detection systems leverage machine learning to
     identify fire events early. Key techniques include satellite imagery
     analysis, smoke detection via computer vision, and thermal anomaly
     detection. Recent advances in CNNs have improved accuracy to 94%...",

    "Industrial detection systems integrate IoT sensors with AI models
     for real-time monitoring. Edge computing enables sub-second response
     times critical for early warning systems...",

    "Academic research demonstrates that multi-modal approaches combining
     visual, thermal, and meteorological data outperform single-sensor
     methods by 23% in detection accuracy..."
]
    """, language="python")
    st.markdown("⬇️ *Results sent to Notion and Logger*")

    # Stage 7: Final Storage
    st.markdown("#### Stage 7: Storage & Logging")
    st.code("""
MissionResult(
    mission_id="mission_20231117_abc123",
    topic="AI wildfire detection systems",
    summaries=[...3 summaries...],
    status="completed",
    metadata={
        'execution_time': 12.4,
        'sources_fetched': 3,
        'avg_quality_score': 0.83
    }
)

✓ Stored to Notion workspace
✓ Logged to SQLite database
    """, language="python")

    st.success("✅ Mission completed successfully!")

st.markdown("---")

# ============================================================================
# ORCHESTRATION PATTERNS
# ============================================================================

st.markdown("""
## 🎼 Orchestration Patterns

The Flow Controller implements several important **software architecture patterns**:

### 1. **Pipeline Pattern**
Data flows through a sequence of stages, each transforming it further.
- **Benefit:** Clear separation of concerns, easy to debug
- **Tradeoff:** Sequential processing can be slower than parallel

### 2. **Dependency Injection**
Components (agents/tools) are provided to the controller, not created internally.
- **Benefit:** Easy to test with mock components, flexible configuration
- **Tradeoff:** More verbose initialization code

### 3. **Error Handling with Retry Logic**
Failed operations (like network fetches) are retried with exponential backoff.
- **Benefit:** Resilient to transient failures
- **Tradeoff:** Adds latency when failures occur

### 4. **Progress Reporting**
The controller calls a progress callback at each stage.
- **Benefit:** Enables real-time UI updates, better user experience
- **Tradeoff:** Tight coupling between controller and UI (if not abstracted)

### 5. **Audit Trail**
Every mission is logged completely for debugging and analysis.
- **Benefit:** Complete history for debugging, compliance, analytics
- **Tradeoff:** Storage overhead, potential performance impact
""")

st.markdown("---")

# ============================================================================
# PERFORMANCE METRICS
# ============================================================================

st.markdown("""
## ⚡ Pipeline Performance

Understanding the time and resource costs of each stage helps optimize the system.
""")

# Sample performance data
import pandas as pd

perf_data = pd.DataFrame({
    'Stage': ['Planning', 'Fetching', 'Cleaning', 'Scoring', 'Summarizing', 'Storage', 'Logging'],
    'Avg Time (s)': [0.5, 8.2, 1.3, 0.4, 2.1, 0.6, 0.2],
    'CPU Usage': [10, 5, 20, 15, 30, 5, 10],
    'Type': ['Agent', 'Tool', 'Tool', 'Tool', 'Agent', 'Tool', 'Tool']
})

# Time breakdown chart
fig_time = px.bar(
    perf_data,
    x='Stage',
    y='Avg Time (s)',
    color='Type',
    title='Average Execution Time by Stage',
    color_discrete_map={'Agent': 'lightcoral', 'Tool': 'lightgreen'}
)
st.plotly_chart(fig_time, use_container_width=True)

# CPU usage chart
fig_cpu = px.bar(
    perf_data,
    x='Stage',
    y='CPU Usage',
    color='Type',
    title='CPU Usage by Stage (%)',
    color_discrete_map={'Agent': 'lightcoral', 'Tool': 'lightgreen'}
)
st.plotly_chart(fig_cpu, use_container_width=True)

st.info("""
**Key Insights:**
- **Fetching** is the slowest stage (network I/O bound)
- **Summarizing** uses the most CPU (LLM/NLP processing)
- **Tools** are generally faster and lighter than **Agents**
- Total pipeline time: ~13 seconds for 3 sources
""")

st.markdown("---")

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

st.markdown("""
## 🎯 Key Takeaways

### What You Learned:

1. **Pipeline Architecture**
   - Data flows through 7 distinct stages
   - Each stage has a single, clear responsibility
   - The Flow Controller orchestrates without doing the work

2. **Data Transformations**
   - User Request → Plan → HTML → Text → Scores → Summary → Storage
   - Each transformation is performed by a specialized component
   - Agents transform through decision-making, Tools through execution

3. **Orchestration Patterns**
   - Pipeline pattern for sequential processing
   - Dependency injection for testability
   - Retry logic for resilience
   - Progress callbacks for UI integration
   - Audit trail for debugging

4. **Performance Characteristics**
   - Fetching dominates execution time (network bound)
   - Summarization dominates CPU usage (compute bound)
   - Tools are generally faster and lighter than Agents

### Next Steps:

- **Chapter 8:** Run a real mission in the Mission Console!
- **Chapter 9:** Explore past missions in the Archive Browser
- **Chapter 6:** Deep dive into Agent vs Tool anatomy

---

*"The organism is more than the sum of its organs — it's the orchestration that creates life."*
""")

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### 🔄 Pipeline Stages")
    st.markdown("""
    1. 🧠 Planning (Agent)
    2. 🦾 Fetching (Tool)
    3. 🫀 Cleaning (Tool)
    4. 📊 Scoring (Tool)
    5. 👅 Summarizing (Agent)
    6. ✋ Storage (Tool)
    7. 💾 Logging (Tool)
    """)

    st.markdown("---")
    st.markdown("### 💡 Quick Tips")
    st.markdown("""
    - Agents = Decision-makers
    - Tools = Executors
    - Controller = Orchestrator
    - Pipeline = Sequential flow
    """)
