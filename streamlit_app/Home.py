"""
THE ANATOMY CONSOLE — HOME PAGE
================================

This is the main entry point for the Research Body Anatomy Console.
A pedagogical Streamlit application that teaches the difference between
AGENTS and TOOLS through an anatomical metaphor.
"""

import streamlit as st
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Research Body Anatomy Console",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# HEADER: WELCOME & OVERVIEW
# ============================================================================

st.title("🧬 The Research Body Anatomy Console")
st.subheader("*A Living System for Information Gathering*")

st.markdown("---")

# ============================================================================
# INTRODUCTION
# ============================================================================

st.markdown("""
## Welcome to the Research Organism

This application teaches **the critical difference between AGENTS and TOOLS**
by building a fully modular research system where each component maps to a
biological organ.

Just as a body has specialized organs working together, our research system
has specialized components that collaborate to gather, process, and summarize
information from the web.
""")

# ============================================================================
# THE CORE CONCEPT
# ============================================================================

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🧠 AGENTS (Autonomous Decision-Makers)

    Agents are **autonomous subsystems** that:
    - Make independent decisions
    - Exhibit reasoning and judgment
    - Adapt their behavior to context
    - Plan and strategize

    **Examples in our system:**
    - **The Mind** (Planner Agent)
    - **The Tongue** (Summarizer Agent)
    """)

with col2:
    st.markdown("""
    ### 🔧 TOOLS (Deterministic Executors)

    Tools are **passive functions** that:
    - Perform deterministic operations
    - Execute exactly as instructed
    - Have no decision-making capability
    - Process input → produce output

    **Examples in our system:**
    - **The Limb** (Scraper Tool)
    - **The Stomach** (Cleaner Tool)
    - **The Hand** (Notion Tool)
    - **The Memory** (Logger Tool)
    """)

st.markdown("---")

# ============================================================================
# SYSTEM ARCHITECTURE DIAGRAM
# ============================================================================

st.markdown("""
## 🏗️ System Architecture

Here's how the organs work together to complete a research mission:
""")

st.code("""
                        ┌───────────┐
                        │  MIND     │
                        │PlannerAgent│ ← AGENT (decides WHAT to research)
                        └─────┬─────┘
                              │ Creates plan with target URLs
                     ┌────────▼─────────┐
                     │  LIMB (TOOL)     │
                     │ Scraper Crawler  │ ← TOOL (fetches as instructed)
                     └────────┬─────────┘
                              │ Raw HTML pages
                  ┌───────────▼───────────┐
                  │     STOMACH (TOOL)    │
                  │     Cleaner Tool      │ ← TOOL (extracts deterministically)
                  └──────────┬────────────┘
                              │ Clean text
                    ┌─────────▼───────────┐
                    │  TONGUE (AGENT)     │
                    │ SummarizerAgent     │ ← AGENT (decides HOW to summarize)
                    └─────────┬───────────┘
                              │ Narrative summaries
               ┌──────────────▼──────────────┐
               │   HAND (TOOL) → Notion       │ ← TOOL (writes as instructed)
               └──────────────┬──────────────┘
                              │
                     ┌────────▼────────┐
                     │ MEMORY (TOOL)   │ ← TOOL (logs everything)
                     │  Logger Tool    │
                     └─────────────────┘
""", language="text")

st.markdown("---")

# ============================================================================
# THE PIPELINE FLOW
# ============================================================================

st.markdown("""
## 🔄 The Research Pipeline

When you run a mission, here's what happens:

1. **🧠 The Mind (Planner)** receives your research topic
   - *Decision*: Which sources are most relevant?
   - *Output*: A prioritized list of URLs to fetch

2. **🦾 The Limb (Scraper)** fetches raw web pages
   - *Execution*: HTTP GET requests to target URLs
   - *Output*: Raw HTML content

3. **🫀 The Stomach (Cleaner)** digests the HTML
   - *Execution*: Parse DOM, extract text, remove boilerplate
   - *Output*: Clean text ready for analysis

4. **👅 The Tongue (Summarizer)** creates narratives
   - *Decision*: What tone? What length? What to emphasize?
   - *Output*: Tailored summaries

5. **✋ The Hand (Notion Writer)** saves the results
   - *Execution*: Format and write to Notion
   - *Output*: Persistent knowledge base

6. **🧠 The Memory (Logger)** records everything
   - *Execution*: Store in SQLite database
   - *Output*: Complete audit trail
""")

st.markdown("---")

# ============================================================================
# NAVIGATION GUIDE
# ============================================================================

st.markdown("""
## 📚 Explore the Anatomy

Use the **sidebar** to navigate to different chapters:

### **Part I: The Organs**
- **Chapter 1:** The Mind (Planner Agent)
- **Chapter 2:** The Crawler Limb (Scraper Tool)
- **Chapter 3:** The Cleaner Stomach
- **Chapter 4:** The Summarizer Tongue
- **Chapter 5:** The Notion Hand

### **Part II: Understanding the System**
- **Chapter 6:** Agent vs Tool Anatomy
- **Chapter 7:** Pipeline Flow Visualizer
- **Chapter 8:** Mission Console (Run missions!)
- **Chapter 9:** Mission Archive
- **Chapter 10:** Engineering Legacy

Each chapter includes:
- 📖 Teaching narratives
- 🎮 Interactive demonstrations
- 📊 Visualizations
- 💻 Code examples
""")

st.markdown("---")

# ============================================================================
# TEACHING GOALS
# ============================================================================

st.markdown("""
## 🎯 What You'll Learn

By the end of this tutorial, you'll understand:

1. **The fundamental difference between Agents and Tools**
   - When to use autonomous decision-making (agents)
   - When to use deterministic execution (tools)

2. **How to build modular, composable systems**
   - Separation of concerns
   - Clear interfaces between components
   - Reusable building blocks

3. **Real-world orchestration patterns**
   - Pipeline coordination
   - Error handling and retry logic
   - State management

4. **Practical skills**
   - Web scraping and content extraction
   - Text processing and summarization
   - API integration (Notion)
   - Data persistence (SQLite)
   - UI development (Streamlit)
""")

st.markdown("---")

# ============================================================================
# CURRENT PHASE STATUS
# ============================================================================

st.markdown("""
## 🚧 Development Status

This system is being built in **5 phases**:

- ✅ **Phase 1: Foundations** — Directory structure, stubs, docstrings
- 🔲 **Phase 2: Agent & Tool Basics** — Core implementation
- 🔲 **Phase 3: Pipeline Integration** — Flow controller, orchestration
- 🔲 **Phase 4: Streamlit Console** — All 10 chapters
- 🔲 **Phase 5: Hybridization** — Advanced features, ScraperAgent

**Current Phase:** Phase 1 Complete! 🎉
""")

# Display phase progress
progress_col1, progress_col2, progress_col3 = st.columns([1, 2, 1])
with progress_col2:
    st.progress(0.2)  # 20% complete (Phase 1 of 5)

st.markdown("---")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("""
## 🚀 Ready to Begin?

**Choose a chapter from the sidebar** to start exploring the anatomy of our
research organism.

We recommend starting with **Chapter 1: The Mind** to understand how the
Planner Agent makes decisions.

---

*Built with Streamlit • Teaching AI Engineering Through Metaphor*
""")

# ============================================================================
# SIDEBAR: QUICK STATS
# ============================================================================

with st.sidebar:
    st.markdown("### 📊 System Overview")

    st.metric("Total Agents", "2", help="Planner, Summarizer")
    st.metric("Total Tools", "4", help="Scraper, Cleaner, Notion, Logger")
    st.metric("Pipeline Stages", "6", help="Plan → Fetch → Clean → Summarize → Store → Log")

    st.markdown("---")
    st.markdown("### 🎓 Learning Path")
    st.markdown("""
    1. Read the Home page
    2. Explore each organ (Chapters 1-5)
    3. Understand Agent vs Tool (Chapter 6)
    4. Visualize the pipeline (Chapter 7)
    5. Run a mission! (Chapter 8)
    """)
