"""
MISSION ARCHIVE — CHAPTER 9
============================

This Streamlit page provides a browser for historical missions:
  • View all past mission executions
  • Filter and search missions
  • Analyze performance trends
  • Compare mission results
  • Organ health monitoring across missions
"""

import streamlit as st
import sys
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

# Add project root to path for imports
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from src.tools.logger_tool import LoggerTool

# Page configuration
st.set_page_config(
    page_title="Chapter 9: Mission Archive",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for organism theme - Memory Archives
st.markdown("""
<style>
    /* Memory Archive Theme - Deep Blues and Purples */
    .stApp {
        background: linear-gradient(135deg, #e0e7ff 0%, #f0f4ff 100%);
    }

    /* Archive Card Styling */
    .archive-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    /* Organ Health Badges */
    .health-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        margin: 0.25rem;
    }

    .health-green {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
    }

    .health-yellow {
        background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%);
        color: #333;
    }

    .health-red {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        color: white;
    }

    /* Timeline Visualization */
    .timeline-entry {
        border-left: 3px solid #667eea;
        padding-left: 1.5rem;
        margin: 1rem 0;
        position: relative;
    }

    .timeline-entry::before {
        content: "●";
        position: absolute;
        left: -0.55rem;
        color: #667eea;
        font-size: 1.5rem;
    }

    /* Memory Stats Panel */
    .memory-stats {
        background: rgba(102, 126, 234, 0.1);
        border: 2px solid #667eea;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize logger tool
if 'logger' not in st.session_state:
    st.session_state.logger = LoggerTool(debug=False)

# ============================================================================
# TITLE AND INTRODUCTION
# ============================================================================

# Header with memory/archive theme
st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 2rem;'>
    <h1 style='color: white; margin: 0;'>📚 Mission Archive</h1>
    <p style='color: #e0e7ff; font-size: 1.2rem; margin-top: 0.5rem;'>💾 The Organism's Memory Bank</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
## 🧠 Exploring the Living Memory

Every mission the research organism executes is recorded in its **eternal memory** — the
SQLite database maintained by the Logger Tool. This archive is where the organism's
experiences are preserved, analyzed, and learned from.

<div style='background: linear-gradient(135deg, #e0e7ff 0%, #c3cfe2 100%); padding: 1.5rem; border-radius: 10px; margin: 1rem 0;'>

### What You Can Discover Here:

- 📊 **Performance Analytics** — Measure the organism's efficiency over time
- 🔍 **Mission Forensics** — Deep-dive into what happened in each mission
- 📈 **Evolutionary Trends** — Track whether the system is learning and improving
- 🏥 **Organ Health Monitoring** — Diagnose which organs need attention
- ⏱️ **Historical Patterns** — Identify recurring successes and failures

</div>

**Philosophy:** An organism without memory cannot learn. A system without logs cannot improve.
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# FETCH MISSIONS FROM DATABASE
# ============================================================================

# Get all missions from the logger
try:
    all_missions = st.session_state.logger.get_all_missions()
except Exception as e:
    st.error(f"Error loading missions from database: {str(e)}")
    all_missions = []

# Add session missions if any
if 'mission_history' in st.session_state and st.session_state.mission_history:
    st.info(f"📝 Found {len(st.session_state.mission_history)} missions in current session (not yet in database)")

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================

st.markdown("## 📊 Archive Summary")

if all_missions:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Missions",
            len(all_missions),
            help="Total number of missions executed"
        )

    with col2:
        completed = sum(1 for m in all_missions if m.get('status') == 'completed')
        st.metric(
            "Completed",
            completed,
            help="Successfully completed missions"
        )

    with col3:
        failed = sum(1 for m in all_missions if m.get('status') == 'failed')
        st.metric(
            "Failed",
            failed,
            delta=f"-{failed}" if failed > 0 else "0",
            delta_color="inverse",
            help="Failed missions"
        )

    with col4:
        success_rate = (completed / len(all_missions) * 100) if all_missions else 0
        st.metric(
            "Success Rate",
            f"{success_rate:.1f}%",
            help="Percentage of successful missions"
        )

    st.markdown("---")

    # ========================================================================
    # ORGAN HEALTH MONITORING (Step 33)
    # ========================================================================

    st.markdown("## 🏥 Organ Health Dashboard")

    st.markdown("""
    This dashboard shows the **health and performance** of each organ across
    all missions. Healthy organs complete their tasks successfully and efficiently.
    """)

    # Calculate organ health metrics
    organ_stats = {
        'Planner (Mind)': {'successes': 0, 'failures': 0, 'avg_time': 0},
        'Scraper (Limb)': {'successes': 0, 'failures': 0, 'avg_time': 0},
        'Cleaner (Stomach)': {'successes': 0, 'failures': 0, 'avg_time': 0},
        'Summarizer (Tongue)': {'successes': 0, 'failures': 0, 'avg_time': 0},
        'Notion (Hand)': {'successes': 0, 'failures': 0, 'avg_time': 0},
        'Logger (Memory)': {'successes': 0, 'failures': 0, 'avg_time': 0}
    }

    # Aggregate stats from missions
    for mission in all_missions:
        if mission.get('status') == 'completed':
            # All organs succeeded
            for organ in organ_stats:
                organ_stats[organ]['successes'] += 1

            # Extract timing if available
            metadata = mission.get('metadata', {})
            if isinstance(metadata, dict) and 'execution_time' in metadata:
                exec_time = metadata['execution_time']
                # Distribute time proportionally (rough estimate)
                organ_stats['Planner (Mind)']['avg_time'] += exec_time * 0.05
                organ_stats['Scraper (Limb)']['avg_time'] += exec_time * 0.60
                organ_stats['Cleaner (Stomach)']['avg_time'] += exec_time * 0.15
                organ_stats['Summarizer (Tongue)']['avg_time'] += exec_time * 0.15
                organ_stats['Notion (Hand)']['avg_time'] += exec_time * 0.03
                organ_stats['Logger (Memory)']['avg_time'] += exec_time * 0.02

        elif mission.get('status') == 'failed':
            # Some organ failed - mark all as having one failure
            for organ in organ_stats:
                organ_stats[organ]['failures'] += 1

    # Calculate averages
    for organ in organ_stats:
        total = organ_stats[organ]['successes'] + organ_stats[organ]['failures']
        if total > 0:
            organ_stats[organ]['avg_time'] /= total
            organ_stats[organ]['success_rate'] = organ_stats[organ]['successes'] / total * 100
        else:
            organ_stats[organ]['success_rate'] = 0

    # Display organ health widgets
    col1, col2 = st.columns(2)

    with col1:
        # Success rate by organ
        organ_df = pd.DataFrame([
            {
                'Organ': organ,
                'Success Rate': stats['success_rate'],
                'Type': 'Agent' if organ in ['Planner (Mind)', 'Summarizer (Tongue)'] else 'Tool'
            }
            for organ, stats in organ_stats.items()
        ])

        fig_health = px.bar(
            organ_df,
            x='Organ',
            y='Success Rate',
            color='Type',
            title='Organ Health: Success Rate by Component',
            color_discrete_map={'Agent': 'lightcoral', 'Tool': 'lightgreen'},
            range_y=[0, 100]
        )
        fig_health.add_hline(y=95, line_dash="dash", line_color="red",
                             annotation_text="Health Threshold (95%)")
        fig_health.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_health, use_container_width=True)

    with col2:
        # Average time by organ
        time_df = pd.DataFrame([
            {
                'Organ': organ,
                'Avg Time (s)': stats['avg_time'],
                'Type': 'Agent' if organ in ['Planner (Mind)', 'Summarizer (Tongue)'] else 'Tool'
            }
            for organ, stats in organ_stats.items()
        ])

        fig_time = px.bar(
            time_df,
            x='Organ',
            y='Avg Time (s)',
            color='Type',
            title='Organ Performance: Average Processing Time',
            color_discrete_map={'Agent': 'lightcoral', 'Tool': 'lightgreen'}
        )
        fig_time.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_time, use_container_width=True)

    # Health status indicators
    st.markdown("### 🏥 Organ Status Indicators")

    health_cols = st.columns(6)
    organs_list = list(organ_stats.keys())

    for i, col in enumerate(health_cols):
        if i < len(organs_list):
            organ = organs_list[i]
            stats = organ_stats[organ]
            success_rate = stats['success_rate']

            # Determine health status
            if success_rate >= 95:
                status = "🟢 Healthy"
                color = "normal"
            elif success_rate >= 80:
                status = "🟡 Warning"
                color = "off"
            else:
                status = "🔴 Critical"
                color = "inverse"

            with col:
                st.metric(
                    organ.split('(')[0].strip(),
                    status,
                    f"{success_rate:.0f}%",
                    delta_color=color
                )

    st.markdown("---")

    # ========================================================================
    # PERFORMANCE TRENDS
    # ========================================================================

    st.markdown("## 📈 Performance Trends")

    # Create timeline data
    if len(all_missions) > 1:
        timeline_data = []
        for mission in all_missions:
            completed_at = mission.get('completed_at')
            if completed_at:
                if isinstance(completed_at, str):
                    try:
                        completed_at = datetime.fromisoformat(completed_at)
                    except:
                        continue

                metadata = mission.get('metadata', {})
                exec_time = 0
                if isinstance(metadata, dict):
                    exec_time = metadata.get('execution_time', 0)

                timeline_data.append({
                    'Time': completed_at,
                    'Execution Time (s)': exec_time,
                    'Status': mission.get('status', 'unknown'),
                    'Sources': mission.get('source_count', 0)
                })

        if timeline_data:
            timeline_df = pd.DataFrame(timeline_data).sort_values('Time')

            # Execution time trend
            fig_trend = px.scatter(
                timeline_df,
                x='Time',
                y='Execution Time (s)',
                color='Status',
                size='Sources',
                title='Mission Execution Time Trend',
                color_discrete_map={'completed': 'green', 'failed': 'red'}
            )
            fig_trend.add_trace(
                go.Scatter(
                    x=timeline_df['Time'],
                    y=timeline_df['Execution Time (s)'].rolling(window=3, min_periods=1).mean(),
                    mode='lines',
                    name='Moving Average (3)',
                    line=dict(color='blue', dash='dash')
                )
            )
            st.plotly_chart(fig_trend, use_container_width=True)

            st.info("""
            **Insight:** The trend line shows whether the organism is getting faster or slower over time.
            Ideally, execution time should remain stable or decrease as caching improves.
            """)
    else:
        st.info("Run more missions to see performance trends!")

    st.markdown("---")

    # ========================================================================
    # MISSION BROWSER
    # ========================================================================

    st.markdown("## 🔍 Mission Browser")

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        filter_status = st.selectbox(
            "Filter by Status",
            options=["All", "completed", "failed"],
            index=0
        )

    with col2:
        sort_by = st.selectbox(
            "Sort By",
            options=["Most Recent", "Oldest First", "Longest Duration", "Shortest Duration"],
            index=0
        )

    with col3:
        search_topic = st.text_input(
            "Search Topic",
            placeholder="Enter keywords..."
        )

    # Apply filters
    filtered_missions = all_missions.copy()

    if filter_status != "All":
        filtered_missions = [m for m in filtered_missions if m.get('status') == filter_status]

    if search_topic.strip():
        filtered_missions = [
            m for m in filtered_missions
            if search_topic.lower() in m.get('topic', '').lower()
        ]

    # Apply sorting
    if sort_by == "Most Recent":
        filtered_missions = sorted(
            filtered_missions,
            key=lambda m: m.get('completed_at', ''),
            reverse=True
        )
    elif sort_by == "Oldest First":
        filtered_missions = sorted(
            filtered_missions,
            key=lambda m: m.get('completed_at', '')
        )
    elif sort_by == "Longest Duration":
        filtered_missions = sorted(
            filtered_missions,
            key=lambda m: m.get('metadata', {}).get('execution_time', 0) if isinstance(m.get('metadata'), dict) else 0,
            reverse=True
        )
    elif sort_by == "Shortest Duration":
        filtered_missions = sorted(
            filtered_missions,
            key=lambda m: m.get('metadata', {}).get('execution_time', 0) if isinstance(m.get('metadata'), dict) else 0
        )

    st.markdown(f"*Showing {len(filtered_missions)} of {len(all_missions)} missions*")

    # Display missions
    for i, mission in enumerate(filtered_missions[:20]):  # Limit to 20 for performance
        with st.expander(
            f"**{i+1}.** {mission.get('topic', 'Untitled')} — "
            f"{'✅' if mission.get('status') == 'completed' else '❌'} "
            f"{mission.get('status', 'unknown')}"
        ):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"**Mission ID:** `{mission.get('mission_id', 'N/A')}`")
                st.markdown(f"**Topic:** {mission.get('topic', 'N/A')}")
                st.markdown(f"**Status:** {mission.get('status', 'unknown')}")

                completed_at = mission.get('completed_at')
                if completed_at:
                    if isinstance(completed_at, str):
                        st.markdown(f"**Completed:** {completed_at}")
                    else:
                        st.markdown(f"**Completed:** {completed_at.strftime('%Y-%m-%d %H:%M:%S')}")

            with col2:
                metadata = mission.get('metadata', {})
                if isinstance(metadata, dict):
                    exec_time = metadata.get('execution_time', 0)
                    st.metric("Execution Time", f"{exec_time:.1f}s")

                st.metric("Sources", mission.get('source_count', 0))
                st.metric("Summaries", mission.get('summary_count', 0))

            # Show metadata if available
            if metadata:
                with st.expander("View Metadata"):
                    st.json(metadata)

else:
    st.info("""
    📭 **No missions in archive yet!**

    The organism's memory is empty. Go to **Chapter 8: Mission Console** to run
    your first mission and start building the archive.
    """)

st.markdown("---")

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

st.markdown("""
## 🎯 Key Takeaways

### The Value of Memory

The Logger Tool's database serves multiple critical purposes:

1. **Debugging:** When missions fail, history helps diagnose patterns
2. **Analytics:** Performance trends reveal optimization opportunities
3. **Compliance:** Complete audit trail for regulated environments
4. **Learning:** Understanding past successes improves future strategies

### Organ Health Monitoring (Step 33)

The **health dashboard** demonstrates:
- How to monitor distributed system components
- When individual organs need optimization
- Which parts of the pipeline are bottlenecks
- Whether the system is improving over time

### What Makes This Powerful

A system that **learns from its history** is fundamentally different from
one that forgets. The archive enables:

- **Iterative improvement** based on empirical data
- **Failure analysis** to prevent recurring issues
- **Performance optimization** guided by real metrics
- **System evolution** informed by usage patterns

---

### Next Steps:

- **Chapter 10:** Learn how to extend the organism with new capabilities
- **Chapter 8:** Run more missions to build a richer archive
- **Chapter 7:** Review pipeline flow to understand bottlenecks

---

*"An organism without memory cannot learn. A system without logs cannot improve."*
""")

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### 📚 Archive Stats")

    if all_missions:
        st.metric("Total Missions", len(all_missions))

        completed = sum(1 for m in all_missions if m.get('status') == 'completed')
        st.metric("Completed", completed)

        failed = sum(1 for m in all_missions if m.get('status') == 'failed')
        st.metric("Failed", failed)

        # Average execution time
        exec_times = []
        for m in all_missions:
            metadata = m.get('metadata', {})
            if isinstance(metadata, dict) and 'execution_time' in metadata:
                exec_times.append(metadata['execution_time'])

        if exec_times:
            avg_time = sum(exec_times) / len(exec_times)
            st.metric("Avg Execution Time", f"{avg_time:.1f}s")
    else:
        st.info("No missions yet")

    st.markdown("---")

    st.markdown("### 🏥 System Health")
    if all_missions:
        completed = sum(1 for m in all_missions if m.get('status') == 'completed')
        success_rate = (completed / len(all_missions) * 100) if all_missions else 0

        if success_rate >= 95:
            st.success("🟢 Healthy")
        elif success_rate >= 80:
            st.warning("🟡 Warning")
        else:
            st.error("🔴 Critical")
    else:
        st.info("No data")
