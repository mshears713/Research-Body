"""
SIDEBAR NAVIGATION — GLOBAL COMPONENT
======================================

This module provides a consistent sidebar navigation component
for all Streamlit pages in the Research Body application.

Usage:
    from sidebar_nav import render_sidebar_navigation

    render_sidebar_navigation()
"""

import streamlit as st


def render_sidebar_navigation():
    """
    Render a consistent sidebar navigation across all pages.

    This provides quick links to all chapters and key information
    about the research organism.
    """

    with st.sidebar:
        st.markdown("## 🧬 Research Body")
        st.markdown("*The Living Research Organism*")

        st.markdown("---")

        # ====================================================================
        # QUICK NAVIGATION
        # ====================================================================

        st.markdown("### 📖 Navigation")

        st.markdown("""
        **Part I: The Organs**
        - [🏠 Home](/)
        - [🧠 Ch 1: The Mind (Planner Agent)](01_The_Mind_Planner)
        - [🦾 Ch 2: The Crawler Limb (Scraper Tool)](02_The_Crawler_Limb)
        - [🫀 Ch 3: The Cleaner Stomach](03_The_Cleaner_Stomach)
        - [👅 Ch 4: The Summarizer Tongue](04_The_Summarizer_Tongue)
        - [✋ Ch 5: The Notion Hand](05_The_Notion_Hand)

        **Part II: The System**
        - [⚖️ Ch 6: Agent vs Tool Anatomy](06_Agent_vs_Tool_Anatomy)
        - [🔄 Ch 7: Pipeline Flow Visualizer](07_Pipeline_Flow_Visualizer)
        - [🎮 Ch 8: Mission Console](08_Mission_Console) ⭐
        - [📚 Ch 9: Mission Archive](09_Mission_Archive)
        - [🚀 Ch 10: Engineering Legacy](10_Engineering_Legacy)
        """)

        st.markdown("---")

        # ====================================================================
        # ORGANISM STATUS
        # ====================================================================

        st.markdown("### 🏥 Organism Status")

        # Check if there are any missions in session
        if 'mission_history' in st.session_state and st.session_state.mission_history:
            total_missions = len(st.session_state.mission_history)
            successful = sum(1 for m in st.session_state.mission_history if m.get('result'))
            success_rate = (successful / total_missions * 100) if total_missions > 0 else 0

            st.metric("Missions This Session", total_missions)
            st.metric("Success Rate", f"{success_rate:.0f}%")

            if success_rate >= 90:
                st.success("🟢 Healthy")
            elif success_rate >= 70:
                st.warning("🟡 Warning")
            else:
                st.error("🔴 Needs Attention")
        else:
            st.info("No missions yet\nRun missions in Ch 8!")

        st.markdown("---")

        # ====================================================================
        # QUICK REFERENCE
        # ====================================================================

        st.markdown("### 💡 Quick Reference")

        with st.expander("Agent vs Tool"):
            st.markdown("""
            **🤖 Agents** (Decision-Makers)
            - Planner (Mind)
            - Summarizer (Tongue)

            **🔧 Tools** (Executors)
            - Scraper (Limb)
            - Cleaner (Stomach)
            - Notion (Hand)
            - Logger (Memory)
            """)

        with st.expander("Pipeline Stages"):
            st.markdown("""
            1. Plan (Agent)
            2. Fetch (Tool)
            3. Clean (Tool)
            4. Score (Tool)
            5. Summarize (Agent)
            6. Store (Tool)
            7. Log (Tool)
            """)

        st.markdown("---")

        # ====================================================================
        # PHASE PROGRESS
        # ====================================================================

        st.markdown("### 🚧 Development Phases")

        phases = [
            ("Phase 1", "Foundations", True),
            ("Phase 2", "Agent & Tool Basics", True),
            ("Phase 3", "Pipeline Integration", True),
            ("Phase 4", "Streamlit Console", True),
            ("Phase 5", "Hybridization", False)
        ]

        for phase, name, completed in phases:
            if completed:
                st.markdown(f"✅ **{phase}:** {name}")
            else:
                st.markdown(f"⏳ **{phase}:** {name}")

        st.markdown("---")

        # ====================================================================
        # HELP & INFO
        # ====================================================================

        st.markdown("### ℹ️ About")

        st.caption("""
        This application teaches the critical difference between
        **Agents** (autonomous decision-makers) and **Tools**
        (deterministic executors) through a biological metaphor.

        Built with Streamlit • Educational AI Architecture
        """)


def render_minimal_sidebar():
    """
    Render a minimal sidebar for pages that don't need full navigation.
    """

    with st.sidebar:
        st.markdown("## 🧬 Research Body")
        st.markdown("[← Back to Home](/)")

        st.markdown("---")

        st.markdown("### 💡 Quick Tip")
        st.info("""
        **Agents** make decisions.
        **Tools** execute commands.
        **Controllers** orchestrate.
        """)
