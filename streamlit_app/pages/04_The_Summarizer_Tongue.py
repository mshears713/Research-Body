"""
THE SUMMARIZER TONGUE — SUMMARIZER AGENT CHAPTER
=================================================

This Streamlit page teaches about the SummarizerAgent:
  • What makes it an AGENT (not a TOOL)
  • How it makes autonomous summarization decisions
  • Interactive demonstration of summarization logic
  • Visualizations of editorial decision-making
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from src.agents.summarizer_agent import SummarizerAgent

# Page configuration
st.set_page_config(
    page_title="Chapter 4: The Summarizer Tongue (Summarizer Agent)",
    page_icon="👅",
    layout="wide"
)

# Title and introduction
st.title("👅 Chapter 4: The Summarizer Tongue — Summarizer Agent")

st.markdown("""
---

## The Research Organism's Voice

The **SummarizerAgent** is the **TONGUE** of our research organism.
It tastes the cleaned content and produces narrative explanations,
choosing tone, focus, and style based on the mission's purpose.

But what makes it an **AGENT** rather than a **TOOL**?

""")

# Agent vs Tool comparison
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🤖 AGENT Characteristics

    The SummarizerAgent exhibits:
    - **Autonomous editorial decisions**
    - **Adaptive tone and style**
    - **Content judgment**
    - **Creative narration**

    It doesn't just extract — it **interprets**.
    """)

with col2:
    st.markdown("""
    ### 🔧 vs. TOOL Characteristics

    A simple tool would just:
    - Take first N sentences
    - No tone adaptation
    - No content prioritization
    - No judgment about importance

    Tools truncate; agents narrate.
    """)

st.markdown("""
---

## Decision-Making Process

The SummarizerAgent makes **autonomous editorial decisions**:

1. **Style Selection**: Technical, executive, or casual tone?
2. **Content Prioritization**: What should be emphasized?
3. **Length Determination**: How much detail is appropriate?
4. **Focus Adaptation**: Methodology, insights, or storytelling?
5. **Quality Judgment**: Is this summary comprehensive?

Each decision demonstrates **AGENT INTELLIGENCE**.

---

## Interactive Demo: Watch the Tongue Narrate

Try it yourself! Give the Summarizer clean text and watch it create different styles.
""")

# Interactive demonstration
st.subheader("🎮 Try the Summarizer Agent")

# Sample clean text for demo
sample_text = """AI-Powered Wildfire Detection Systems have revolutionized how we monitor and respond to forest fires. Traditional detection methods relied on human spotters and satellite imagery with significant delays. Modern machine learning systems now process real-time data from multiple sources including thermal cameras, smoke detectors, and meteorological sensors.

Convolutional Neural Networks (CNNs) form the backbone of these detection systems. Researchers at Stanford University demonstrated 94% accuracy in identifying smoke patterns from satellite imagery. The system processes images every 15 minutes, detecting fires within minutes of ignition compared to hours with traditional methods.

Edge computing plays a crucial role in deployment. Remote sensor networks run lightweight AI models directly on devices, enabling sub-second response times without requiring constant cloud connectivity. This is critical in wilderness areas with limited internet infrastructure.

Integration with IoT sensor networks creates a comprehensive monitoring ecosystem. Temperature sensors, humidity monitors, and wind speed detectors feed data into predictive models that forecast fire spread patterns. Emergency response teams use these predictions to allocate resources and plan evacuation routes.

Real-world deployment shows impressive results. California's ALERTCalifornia program uses AI detection across 1000+ cameras, identifying fires before they spread beyond initial containment. Australia's FireWatch system covers 3 million hectares with automated monitoring. These systems have reduced average response time from 45 minutes to under 10 minutes."""

# Input controls
text_input = st.text_area(
    "Clean Text Input",
    value=sample_text,
    height=200,
    help="Enter clean text to summarize"
)

col1, col2 = st.columns(2)
with col1:
    style = st.selectbox(
        "Summary Style",
        options=["technical", "executive", "casual", "trend_analysis"],
        help="Choose the tone and focus of the summary"
    )

with col2:
    show_reasoning = st.checkbox("Show agent reasoning", value=True)

# Run summarizer button
if st.button("👅 Generate Summary", type="primary"):
    st.markdown("### Summarization in Progress...")

    # Create summarizer
    summarizer = SummarizerAgent(default_style=style, debug=False)

    # Show operation details
    with st.expander("📋 Summarization Request Details", expanded=False):
        st.json({
            "text_length": len(text_input),
            "word_count": len(text_input.split()),
            "style": style
        })

    # Execute summarization
    with st.spinner("Summarizer making editorial decisions..."):
        summary = summarizer.summarize(text_input, style=style)

    # Display results
    st.success("✅ Summary Generated!")

    # Show the summary
    st.markdown("### 📝 Generated Summary")
    st.markdown(summary)

    # Style characteristics
    style_config = SummarizerAgent.STYLES[style]
    st.markdown(f"**Style Applied**: {style}")
    st.markdown(f"**Tone**: {style_config['tone']}")
    st.markdown(f"**Focus**: {style_config['focus']}")

    # Agent decision analysis
    if show_reasoning:
        with st.expander("🔍 Agent Decision-Making Analysis", expanded=True):
            st.markdown(f"""
            **Decisions the Agent Made:**

            1. **Style Decision**: Chose **{style}** style
               - Tone: {style_config['tone']}
               - Focus: {style_config['focus']}
               - Format: {'Bullet points' if style_config['bullet_points'] else 'Narrative'}

            2. **Content Prioritization**:
               - Analyzed source text for key themes
               - Identified most important concepts to emphasize
               - Decided what details to include vs. omit

            3. **Length Determination**:
               - Target: {style_config['sentence_count'][0]}-{style_config['sentence_count'][1]} sentences
               - Actual: {len(summary.split('.'))} sentences
               - Adapted based on source complexity

            4. **Tone Adaptation**:
               - Applied {style_config['tone']} language patterns
               - Chose appropriate vocabulary level
               - Structured narrative for target audience

            **What a TOOL Would Do Differently:**
            - ❌ Just take first N sentences (no judgment)
            - ❌ Same output regardless of style parameter
            - ❌ No content prioritization or emphasis
            - ❌ No adaptation to audience needs

            This is **autonomous editorial judgment** — the hallmark of an AGENT.
            """)

    # Comparison with other styles
    st.markdown("#### 📊 Try Different Styles")
    st.info("""
    The same source text produces different summaries based on the agent's style decision.
    Try selecting different styles above to see how the agent adapts its output!
    """)

    # Summarizer statistics
    st.markdown("#### 📊 Summarizer Statistics")
    stats = summarizer.get_summarization_stats()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Summaries", stats['total_summaries'])
    with col2:
        st.metric("Avg Compression", f"{stats['avg_compression_ratio']*100:.0f}%")
    with col3:
        st.metric("Avg Summary Length", f"{stats['avg_summary_length']:.0f} words")

st.markdown("""
---

## Code Example: How the Agent Works

Here's a simplified view of the SummarizerAgent's decision-making:

```python
class SummarizerAgent:
    STYLES = {
        'technical': {'tone': 'formal', 'focus': 'methodology'},
        'executive': {'tone': 'concise', 'focus': 'key insights'},
        'casual': {'tone': 'conversational', 'focus': 'storytelling'}
    }

    def summarize(self, text: str, style: str) -> str:
        # DECISION POINT 1: Choose style parameters
        style_config = self.STYLES[style]

        # DECISION POINT 2: Analyze and prioritize content
        key_sentences = self._identify_important_content(text)

        # DECISION POINT 3: Adapt tone and language
        if style == 'technical':
            summary = self._create_technical_narrative(key_sentences)
        elif style == 'executive':
            summary = self._create_executive_summary(key_sentences)
        else:
            summary = self._create_casual_narrative(key_sentences)

        # DECISION POINT 4: Validate and adjust length
        summary = self._ensure_appropriate_length(summary, style_config)

        return summary
```

Notice the **multiple decision points**:
- Which style parameters to apply?
- What content is most important?
- How should I phrase this?
- Is the length appropriate?

This is **creative intelligence** — not just execution.

---

## Key Takeaway: Agents vs. Tools

| Aspect | Agent (Summarizer) | Tool (Cleaner) |
|--------|---------------------|----------------|
| **Purpose** | Create intelligent narrative | Extract text mechanically |
| **Input** | Clean text + style | Raw HTML |
| **Logic** | Editorial judgment | Rule-based extraction |
| **Output** | Adaptive summary | All extracted text |
| **Adaptation** | Changes by audience | Same rules always |

The SummarizerAgent is an **AGENT** because it exhibits:
- **Autonomous decisions**: Chooses tone, focus, length
- **Adaptation**: Changes output based on context
- **Creative judgment**: Interprets and narrates
- **Self-evaluation**: Scores its own quality

---

## Style Comparison

The agent supports multiple styles, each with different characteristics:

### 🔬 Technical Style
- **Tone**: Formal and precise
- **Focus**: Methodology, data, specifics
- **Length**: 5-10 sentences
- **Format**: Often includes bullet points
- **Use Case**: Academic research, engineering docs

### 💼 Executive Style
- **Tone**: Concise and actionable
- **Focus**: Key insights, implications
- **Length**: 3-5 sentences
- **Format**: Bullet points with highlights
- **Use Case**: Leadership briefings, reports

### 💬 Casual Style
- **Tone**: Conversational and accessible
- **Focus**: Main ideas, storytelling
- **Length**: 4-8 sentences
- **Format**: Narrative paragraphs
- **Use Case**: Blog posts, general audience

### 📈 Trend Analysis Style
- **Tone**: Analytical and comparative
- **Focus**: Patterns, changes, emerging themes
- **Length**: 6-12 sentences
- **Format**: Structured analysis with bullets
- **Use Case**: Market research, trend reports

---

## Next Steps

Continue to **Chapter 5: The Notion Hand** to see how summaries and results
are stored in external systems — another TOOL that executes the agent's output!

Or try the same text with different styles above to see agent adaptation!
""")

# Sidebar with navigation
with st.sidebar:
    st.markdown("## 📚 Chapter Navigation")
    st.markdown("""
    **Previous**: Chapter 3 - The Cleaner Stomach

    **Current**: Chapter 4 - The Summarizer Tongue

    **Next Chapters**:
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
    - ✅ What makes the summarizer an AGENT
    - ✅ How agents make editorial decisions
    - ✅ Why adaptation matters
    - ✅ The difference between extraction and interpretation
    """)
