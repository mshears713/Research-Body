"""
MISSION CONSOLE — CHAPTER 8
============================

This Streamlit page provides an interactive mission execution interface:
  • Configure and launch research missions
  • Live progress updates during execution
  • Real-time visualization of each pipeline stage
  • Organ health monitoring
  • Results display and export
"""

import streamlit as st
import sys
from pathlib import Path
import time
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from pipeline.flow_controller import FlowController
from pipeline.mission_model import MissionRequest

# Page configuration
st.set_page_config(
    page_title="Chapter 8: Mission Console",
    page_icon="🎮",
    layout="wide"
)

# Initialize session state for mission history
if 'mission_history' not in st.session_state:
    st.session_state.mission_history = []
if 'current_mission' not in st.session_state:
    st.session_state.current_mission = None
if 'mission_running' not in st.session_state:
    st.session_state.mission_running = False

# ============================================================================
# TITLE AND INTRODUCTION
# ============================================================================

st.title("🎮 Chapter 8: Mission Console")
st.subheader("*Launch and Monitor Research Missions in Real-Time*")

st.markdown("---")

st.markdown("""
## Welcome to the Control Room

This is where you **bring the research organism to life**. Configure a research
mission, launch it, and watch as data flows through each organ — from raw web
pages to polished summaries.

You'll see the organism "breathing" as it works:
- 🧠 **The Mind** plans the strategy
- 🦾 **The Limb** fetches sources
- 🫀 **The Stomach** digests content
- 👅 **The Tongue** narrates findings
- ✋ **The Hand** preserves knowledge
- 💾 **The Memory** records history
""")

st.markdown("---")

# ============================================================================
# MISSION CONFIGURATION
# ============================================================================

st.markdown("## ⚙️ Mission Configuration")

col1, col2 = st.columns([2, 1])

with col1:
    mission_topic = st.text_input(
        "Research Topic",
        value="AI-powered wildfire detection systems",
        help="What do you want to research? Be specific for better results.",
        placeholder="e.g., 'quantum computing breakthroughs 2024'"
    )

    specific_sources = st.text_area(
        "Specific Sources (Optional)",
        value="",
        help="Enter specific URLs to research, one per line. Leave empty to let the Planner decide.",
        placeholder="https://example.com/article1\nhttps://example.org/article2"
    )

with col2:
    max_sources = st.slider(
        "Maximum Sources",
        min_value=1,
        max_value=10,
        value=3,
        help="How many web pages to fetch and analyze"
    )

    summary_style = st.selectbox(
        "Summary Style",
        options=["technical", "executive", "casual"],
        index=0,
        help="How should the Summarizer Agent present findings?"
    )

    debug_mode = st.checkbox(
        "Debug Mode",
        value=False,
        help="Show detailed execution logs"
    )

# ============================================================================
# SCRAPER MODE TOGGLE (Step 34: Phase 5 Preview)
# ============================================================================

st.markdown("---")

st.markdown("## 🔬 Advanced Configuration (Phase 5 Preview)")

st.info("""
**Phase 5 Feature Preview:** In Phase 5, the Scraper will be upgraded from a
deterministic **TOOL** to an intelligent **AGENT** that can make autonomous
decisions about which links to follow, how to retry failures, and when to skip
low-quality sources.
""")

scraper_mode = st.radio(
    "Scraper Mode",
    options=["Tool Mode (Current)", "Agent Mode (Phase 5 Preview)"],
    index=0,
    help="Toggle between deterministic Tool and intelligent Agent scraping"
)

if scraper_mode == "Agent Mode (Phase 5 Preview)":
    st.warning("""
    ⚠️ **Agent Mode is not yet implemented.**

    When available, the Scraper Agent will:
    - **Intelligently crawl** related pages beyond the initial list
    - **Retry failures** with adaptive strategies (retry count, delay)
    - **Filter low-quality** sources before fetching (based on domain reputation)
    - **Learn from patterns** (which sources are most valuable)
    - **Adapt crawling depth** based on relevance scores

    This demonstrates the evolution from **TOOL → AGENT**:
    - **Tool:** "Fetch exactly these URLs, nothing more, nothing less"
    - **Agent:** "Research this topic intelligently, deciding which sources to pursue"
    """)

    # Phase 5 agent configuration options (preview)
    col1, col2 = st.columns(2)
    with col1:
        max_crawl_depth = st.slider(
            "Max Crawl Depth",
            min_value=1,
            max_value=3,
            value=1,
            help="How many link levels to follow (Agent decides which links)",
            disabled=True
        )

    with col2:
        min_relevance_threshold = st.slider(
            "Min Relevance Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            help="Agent skips sources below this relevance score",
            disabled=True
        )

else:
    st.success("""
    ✅ **Tool Mode Active**

    The Scraper Tool will:
    - **Fetch exactly** the URLs specified (by user or Planner Agent)
    - **No decision-making** about which sources to pursue
    - **Deterministic behavior** for predictable results
    - **Simple retry logic** with fixed exponential backoff

    This is the current implementation (Phases 1-4).
    """)

st.markdown("---")

# ============================================================================
# MISSION LAUNCH CONTROLS
# ============================================================================

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    launch_button = st.button(
        "🚀 Launch Mission",
        type="primary",
        disabled=st.session_state.mission_running or not mission_topic.strip(),
        use_container_width=True
    )

with col2:
    if st.session_state.mission_running:
        st.warning("Mission Running...")
    elif st.session_state.current_mission:
        st.success("Mission Complete!")

with col3:
    if st.button("Clear Results", use_container_width=True):
        st.session_state.current_mission = None
        st.rerun()

st.markdown("---")

# ============================================================================
# MISSION EXECUTION (LIVE RUN DISPLAY)
# ============================================================================

if launch_button and not st.session_state.mission_running:
    st.session_state.mission_running = True
    st.session_state.current_mission = None

    # Parse sources
    source_list = []
    if specific_sources.strip():
        source_list = [url.strip() for url in specific_sources.split('\n') if url.strip()]

    # Create mission request
    request = MissionRequest(
        topic=mission_topic,
        sources=source_list,
        max_sources=max_sources,
        summary_style=summary_style
    )

    # ========================================================================
    # LIVE EXECUTION WITH PROGRESS TRACKING
    # ========================================================================

    st.markdown("## 🔴 LIVE MISSION EXECUTION")

    # Create progress placeholders
    progress_bar = st.progress(0)
    status_text = st.empty()
    stage_container = st.container()

    # Stage indicators
    stage_status = {
        'Planning': '⏳',
        'Fetching': '⏳',
        'Cleaning': '⏳',
        'Scoring': '⏳',
        'Summarizing': '⏳',
        'Storage': '⏳',
        'Logging': '⏳'
    }
    stage_display = st.empty()

    def update_progress(message: str, percent: float):
        """Progress callback for live updates."""
        progress_bar.progress(percent / 100.0)
        status_text.markdown(f"**Status:** {message}")

        # Update stage indicators
        if "Planning" in message:
            stage_status['Planning'] = '🟢'
        elif "Fetching" in message:
            stage_status['Planning'] = '✅'
            stage_status['Fetching'] = '🟢'
        elif "Cleaning" in message:
            stage_status['Fetching'] = '✅'
            stage_status['Cleaning'] = '🟢'
        elif "Scoring" in message:
            stage_status['Cleaning'] = '✅'
            stage_status['Scoring'] = '🟢'
        elif "Summarizing" in message:
            stage_status['Scoring'] = '✅'
            stage_status['Summarizing'] = '🟢'
        elif "Storing" in message:
            stage_status['Summarizing'] = '✅'
            stage_status['Storage'] = '🟢'
        elif "completed" in message.lower():
            stage_status['Storage'] = '✅'
            stage_status['Logging'] = '✅'

        # Display stage status
        stage_display.markdown(f"""
        **Pipeline Stages:**
        - {stage_status['Planning']} Planning (Planner Agent)
        - {stage_status['Fetching']} Fetching (Scraper Tool)
        - {stage_status['Cleaning']} Cleaning (Cleaner Tool)
        - {stage_status['Scoring']} Scoring (Utility Functions)
        - {stage_status['Summarizing']} Summarizing (Summarizer Agent)
        - {stage_status['Storage']} Storage (Notion Tool)
        - {stage_status['Logging']} Logging (Logger Tool)

        *Legend: ⏳ Waiting | 🟢 In Progress | ✅ Complete*
        """)

        # Force UI update
        time.sleep(0.1)

    # Execute mission
    try:
        with stage_container:
            st.markdown("### 📋 Execution Log")
            log_placeholder = st.empty()

            # Create controller with progress callback
            controller = FlowController(
                debug=debug_mode,
                progress_callback=update_progress
            )

            # Execute mission
            start_time = time.time()
            result = controller.execute_mission(request)
            execution_time = time.time() - start_time

            # Store result
            st.session_state.current_mission = {
                'request': request,
                'result': result,
                'execution_time': execution_time,
                'timestamp': datetime.now()
            }

            # Add to history
            st.session_state.mission_history.append(st.session_state.current_mission)

            # Show success
            status_text.markdown("**Status:** ✅ Mission completed successfully!")
            progress_bar.progress(1.0)

    except Exception as e:
        status_text.markdown(f"**Status:** ❌ Mission failed: {str(e)}")
        st.error(f"Mission execution failed: {str(e)}")

        # Store failed mission
        st.session_state.current_mission = {
            'request': request,
            'result': None,
            'error': str(e),
            'execution_time': time.time() - start_time,
            'timestamp': datetime.now()
        }

    finally:
        st.session_state.mission_running = False

st.markdown("---")

# ============================================================================
# MISSION RESULTS DISPLAY
# ============================================================================

if st.session_state.current_mission and st.session_state.current_mission.get('result'):
    mission = st.session_state.current_mission
    result = mission['result']

    st.markdown("## 📊 Mission Results")

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Execution Time",
            f"{mission['execution_time']:.1f}s",
            help="Total time from start to finish"
        )

    with col2:
        sources_fetched = len(result.raw_html) if result.raw_html else 0
        st.metric(
            "Sources Fetched",
            sources_fetched,
            help="Number of web pages successfully retrieved"
        )

    with col3:
        summaries_count = len(result.summaries) if result.summaries else 0
        st.metric(
            "Summaries Created",
            summaries_count,
            help="Number of summaries generated"
        )

    with col4:
        avg_score = 0.0
        if result.metadata and 'scores' in result.metadata:
            scores = result.metadata['scores'].values()
            avg_score = sum(scores) / len(scores) if scores else 0.0
        st.metric(
            "Avg Quality Score",
            f"{avg_score:.2f}",
            help="Average quality score across all sources"
        )

    st.markdown("---")

    # ========================================================================
    # SUMMARIES
    # ========================================================================

    st.markdown("### 📝 Generated Summaries")

    if result.summaries:
        for i, summary in enumerate(result.summaries, 1):
            with st.expander(f"**Summary {i}**", expanded=(i == 1)):
                st.markdown(summary)
    else:
        st.warning("No summaries were generated.")

    st.markdown("---")

    # ========================================================================
    # VISUALIZATIONS (Step 38: Plotly visualizations)
    # ========================================================================

    st.markdown("### 📈 Data Analysis")

    # Text length analysis
    if result.clean_text:
        text_lengths = {
            url: len(text.split())
            for url, text in result.clean_text.items()
        }

        # Create DataFrame for visualization
        viz_data = []
        for url in result.clean_text.keys():
            words = len(result.clean_text[url].split())
            score = result.metadata.get('scores', {}).get(url, 0.0)
            viz_data.append({
                'URL': url.split('//')[-1][:30] + '...',  # Shorten URL
                'Word Count': words,
                'Quality Score': score
            })

        df = pd.DataFrame(viz_data)

        # Word count chart
        col1, col2 = st.columns(2)

        with col1:
            fig_words = px.bar(
                df,
                x='URL',
                y='Word Count',
                title='Extracted Text Length by Source',
                color='Quality Score',
                color_continuous_scale='viridis'
            )
            fig_words.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_words, use_container_width=True)

        with col2:
            fig_scores = px.bar(
                df,
                x='URL',
                y='Quality Score',
                title='Quality Scores by Source',
                color='Quality Score',
                color_continuous_scale='RdYlGn'
            )
            fig_scores.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_scores, use_container_width=True)

    st.markdown("---")

    # ========================================================================
    # SOURCE DETAILS
    # ========================================================================

    st.markdown("### 🔍 Source Details")

    if result.clean_text:
        for url, text in result.clean_text.items():
            with st.expander(f"**Source:** {url}"):
                # Metadata
                metadata = result.metadata.get('clean_metadata', {}).get(url, {})
                score = result.metadata.get('scores', {}).get(url, 0.0)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Title:** {metadata.get('title', 'N/A')}")
                with col2:
                    st.markdown(f"**Words:** {metadata.get('word_count', 0)}")
                with col3:
                    st.markdown(f"**Score:** {score:.2f}")

                # Text preview
                st.markdown("**Text Preview:**")
                preview = text[:500] + "..." if len(text) > 500 else text
                st.text(preview)

    st.markdown("---")

    # ========================================================================
    # EXPORT OPTIONS
    # ========================================================================

    st.markdown("### 💾 Export Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Export summaries as text
        summaries_text = "\n\n---\n\n".join(result.summaries)
        st.download_button(
            label="📄 Download Summaries (TXT)",
            data=summaries_text,
            file_name=f"summaries_{result.mission_id}.txt",
            mime="text/plain"
        )

    with col2:
        # Export metadata as JSON
        import json
        metadata_json = json.dumps(result.metadata, indent=2, default=str)
        st.download_button(
            label="📋 Download Metadata (JSON)",
            data=metadata_json,
            file_name=f"metadata_{result.mission_id}.json",
            mime="application/json"
        )

    with col3:
        # Export full result
        full_export = {
            'mission_id': result.mission_id,
            'topic': result.topic,
            'summaries': result.summaries,
            'status': result.status,
            'metadata': result.metadata,
            'execution_time': mission['execution_time']
        }
        full_json = json.dumps(full_export, indent=2, default=str)
        st.download_button(
            label="📦 Download Full Result (JSON)",
            data=full_json,
            file_name=f"mission_{result.mission_id}.json",
            mime="application/json"
        )

elif st.session_state.current_mission and st.session_state.current_mission.get('error'):
    st.error(f"❌ Mission Failed: {st.session_state.current_mission['error']}")

st.markdown("---")

# ============================================================================
# RECENT MISSIONS
# ============================================================================

if st.session_state.mission_history:
    st.markdown("## 📚 Recent Missions")

    st.markdown(f"*You've run {len(st.session_state.mission_history)} missions in this session.*")

    # Create summary table
    history_data = []
    for mission in reversed(st.session_state.mission_history[-5:]):  # Last 5
        result = mission.get('result')
        history_data.append({
            'Topic': mission['request'].topic[:40] + '...',
            'Time': mission['timestamp'].strftime('%H:%M:%S'),
            'Duration': f"{mission['execution_time']:.1f}s",
            'Status': '✅ Success' if result else '❌ Failed',
            'Summaries': len(result.summaries) if result and result.summaries else 0
        })

    if history_data:
        df_history = pd.DataFrame(history_data)
        st.dataframe(df_history, use_container_width=True, hide_index=True)

st.markdown("---")

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

st.markdown("""
## 🎯 What You Just Experienced

### The Living Organism in Action

You just witnessed a complete research mission flow through the organism:

1. **🧠 The Mind (Planner)** received your topic and decided which sources to fetch
2. **🦾 The Limb (Scraper)** fetched raw HTML from the web
3. **🫀 The Stomach (Cleaner)** digested HTML into clean text
4. **📊 Scoring Functions** calculated quality and relevance
5. **👅 The Tongue (Summarizer)** crafted narrative summaries
6. **✋ The Hand (Notion)** prepared results for storage
7. **💾 The Memory (Logger)** recorded everything to the database

### Agent vs Tool in Practice

Notice how:
- **Agents** (Planner, Summarizer) made **decisions** based on context
- **Tools** (Scraper, Cleaner, Logger) **executed** deterministically
- The **Flow Controller** **orchestrated** the entire sequence

### What Makes This Powerful

This architecture is:
- **Modular:** Each component can be upgraded independently
- **Testable:** Each organ can be tested in isolation
- **Observable:** Every stage can be monitored and logged
- **Resilient:** Errors in one stage don't crash the whole system
- **Extensible:** New organs can be added without changing existing ones

---

### Next Steps:

- **Chapter 9:** Browse the mission archive to analyze past executions
- **Chapter 10:** Learn about extending the organism with new capabilities

---

*"You've just seen the difference between code that runs and code that teaches."*
""")

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### 🎮 Console Status")

    if st.session_state.mission_running:
        st.warning("⏳ Mission Running")
    elif st.session_state.current_mission:
        st.success("✅ Mission Complete")
    else:
        st.info("💤 Ready to Launch")

    st.markdown("---")

    st.markdown("### 📊 Session Stats")
    st.metric("Missions Run", len(st.session_state.mission_history))

    if st.session_state.mission_history:
        successful = sum(1 for m in st.session_state.mission_history if m.get('result'))
        st.metric("Success Rate", f"{successful}/{len(st.session_state.mission_history)}")

    st.markdown("---")

    st.markdown("### 💡 Pro Tips")
    st.markdown("""
    - Be specific with topics
    - Use 3-5 sources for balance
    - Try different summary styles
    - Enable debug for learning
    """)
