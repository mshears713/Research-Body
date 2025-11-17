"""
THE NOTION HAND — NOTION TOOL CHAPTER
======================================

This Streamlit page teaches about the NotionTool:
  • What makes it a TOOL (not an AGENT)
  • How it performs deterministic write operations
  • Interactive demonstration of Notion integration
  • Visualizations of write operations
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from src.tools.notion_tool import NotionTool

# Page configuration
st.set_page_config(
    page_title="Chapter 5: The Notion Hand (Notion Tool)",
    page_icon="✋",
    layout="wide"
)

# Title and introduction
st.title("✋ Chapter 5: The Notion Hand — Notion Tool")

st.markdown("""
---

## The Research Organism's Writing Hand

The **NotionTool** is the **HAND** of our research organism.
It writes the final summaries and research results into Notion,
creating a persistent knowledge base.

But what makes it a **TOOL** rather than an **AGENT**?

""")

# Tool vs Agent comparison
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🔧 TOOL Characteristics

    The NotionTool exhibits:
    - **Deterministic write execution**
    - **No content judgment**
    - **Mechanical API calls**
    - **Same input → Same output**

    It doesn't decide — it **writes**.
    """)

with col2:
    st.markdown("""
    ### 🤖 vs. AGENT Characteristics

    An agent would:
    - Decide WHERE to write content
    - Choose HOW to organize knowledge
    - Adapt formatting to context
    - Learn optimal structures

    Agents organize; tools transcribe.
    """)

st.markdown("""
---

## Write Process

The NotionTool performs **deterministic operations**:

1. **Receive Content**: Accept formatted text to write
2. **Authenticate**: Connect to Notion API
3. **Format Blocks**: Convert content to Notion block structure
4. **Execute Write**: Make API call to create/update page
5. **Report Status**: Return success/failure and URL

Each step is **mechanical** — no intelligence required.

---

## Interactive Demo: Watch the Hand Write

Try it yourself! Give the Notion Tool content and watch it prepare the write operation.

**Note**: This is a demo environment. Actual writes to Notion require API credentials.
""")

# Interactive demonstration
st.subheader("🎮 Try the Notion Tool")

# Sample content for demo
sample_content = """# AI Wildfire Detection Summary

Machine learning-based wildfire detection systems have achieved 94% accuracy in identifying fire events from satellite imagery. These systems process real-time data from thermal cameras and meteorological sensors, enabling detection within minutes of fire ignition.

Key technologies:
- Convolutional Neural Networks (CNNs) for smoke pattern recognition
- Edge computing for real-time processing in remote areas
- IoT sensor integration for comprehensive monitoring

**Real-world impact**: Average response time reduced from 45 minutes to under 10 minutes in deployed systems."""

# Input controls
content_input = st.text_area(
    "Content to Write",
    value=sample_content,
    height=200,
    help="Enter formatted content to write to Notion"
)

col1, col2 = st.columns(2)
with col1:
    page_id = st.text_input(
        "Notion Page ID",
        value="abc123def456",
        help="Target Notion page or database ID"
    )

with col2:
    title = st.text_input(
        "Content Title",
        value="Wildfire AI Research Summary",
        help="Title for the Notion page"
    )

# Demo mode indicator
st.info("🔒 **Demo Mode**: This simulation shows how the tool would work. Actual Notion writes require API credentials.")

# Run notion tool button
if st.button("✋ Write to Notion (Demo)", type="primary"):
    st.markdown("### Write Operation in Progress...")

    # Create notion tool
    notion = NotionTool(debug=False)

    # Show operation details
    with st.expander("📋 Write Operation Details", expanded=False):
        st.json({
            "page_id": page_id,
            "title": title,
            "content_length": len(content_input),
            "blocks_to_write": len(content_input.split('\n'))
        })

    # Execute write (demo mode)
    with st.spinner("Notion Tool preparing write..."):
        result = notion.write_to_notion(content_input, page_id, title)

    # Display results
    if result['success']:
        st.success("✅ Write Operation Completed!")

        # Show the results
        st.markdown("### 📊 Write Results")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Status", "Success ✓")
        with col2:
            st.metric("Blocks Written", result['blocks_written'])
        with col3:
            st.metric("Content Size", f"{len(content_input):,} chars")

        # Page URL
        st.markdown("#### 🔗 Notion Page")
        st.code(result['page_url'])

        # Metadata
        st.markdown("#### 🔍 Write Metadata")
        st.json({
            'page_id': page_id,
            'title': title,
            'blocks_written': result['blocks_written'],
            'timestamp': result.get('timestamp', 'N/A')
        })

        # Tool characteristics box
        with st.expander("🔍 Tool Behavior Analysis", expanded=True):
            st.markdown("""
            **What the Tool Did:**

            1. **Received Content**: Accepted formatted content and parameters
            2. **Authenticated**: (Would) Connect to Notion API with credentials
            3. **Formatted Blocks**: Converted content to Notion block structure
            4. **Executed Write**: (Would) Make API call to write blocks
            5. **Reported Status**: Returned success confirmation and URL

            **What the Tool DID NOT Do:**
            - ❌ Decide where to organize this content
            - ❌ Choose how to format or structure it
            - ❌ Judge if content is worth writing
            - ❌ Adapt behavior based on content type
            - ❌ Learn from previous writes

            This is **pure write execution** — the hallmark of a TOOL.
            """)
    else:
        st.error(f"❌ Write Failed: {result['error']}")

        with st.expander("🔍 Tool Behavior on Failure", expanded=True):
            st.markdown("""
            **What the Tool Did:**

            1. **Attempted Write**: Tried to execute the command
            2. **Encountered Error**: API or authentication issue
            3. **Reported Failure**: Returned error details
            4. **No Retry**: Didn't attempt alternative strategies

            **What an AGENT Would Do Differently:**
            - Try writing to a different location
            - Adapt format based on error type
            - Learn that this approach doesn't work
            - Decide whether to continue or abort

            Tools just report — Agents adapt.
            """)

    # Notion Tool statistics
    st.markdown("#### 📊 Notion Tool Statistics")
    stats = notion.get_write_stats()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Writes", stats['total_writes'])
    with col2:
        st.metric("Success Rate", f"{stats['success_rate']*100:.0f}%")
    with col3:
        st.metric("Avg Blocks/Write", f"{stats['avg_blocks_per_write']:.0f}")

st.markdown("""
---

## Code Example: How the Tool Works

Here's a simplified view of the NotionTool's execution:

```python
class NotionTool:
    def write_to_notion(self, content: str, page_id: str, title: str) -> Dict:
        # EXECUTION: Just write, no decisions

        # Step 1: Authenticate (or check credentials)
        if not self.api_key:
            return {'success': False, 'error': 'No API key'}

        # Step 2: Format content into Notion blocks
        blocks = self._format_content_to_blocks(content)

        # Step 3: Execute API call
        try:
            # In production: notion_client.blocks.children.append(page_id, blocks)
            response = self._call_notion_api(page_id, title, blocks)

            # Step 4: Return status (no interpretation)
            return {
                'success': True,
                'page_url': f"https://notion.so/{page_id}",
                'blocks_written': len(blocks)
            }

        except Exception as e:
            # Report failure but don't try to fix it
            return {'success': False, 'error': str(e)}
```

Notice how there are **NO decision points**:
- No "should I write this content?"
- No "where should I organize this?"
- No "how should I format this differently?"

Just **pure mechanical writing**.

---

## Key Takeaway: Tools vs. Agents

| Aspect | Tool (Notion) | Agent (Planner) |
|--------|---------------|-----------------|
| **Purpose** | Execute writes mechanically | Decide what to research |
| **Input** | Formatted content + target | High-level topic |
| **Logic** | Deterministic API calls | Strategic planning |
| **Output** | Write confirmation | Research plan |
| **Failures** | Reports error, stops | Adapts strategy, continues |

The NotionTool is a **TOOL** because it exhibits:
- **Mechanical execution**: No thinking, just API calls
- **Determinism**: Same input → Same output
- **No autonomy**: Can't make decisions
- **Simple responsibility**: Write and report

---

## Real-World Integration

In a production environment, the Notion Tool would:

### ✅ Setup Requirements:
1. Notion API key from notion.so/my-integrations
2. Share target pages/databases with your integration
3. Configure NOTION_API_KEY environment variable
4. Install notion-client SDK: `pip install notion-client`

### ✅ Typical Usage:
```python
from src.tools.notion_tool import NotionTool

# Initialize with API key
notion = NotionTool(api_key="secret_...")

# Write summary to Notion
result = notion.write_to_notion(
    content=summary,
    page_id="abc123def456",
    title="Weekly Research Digest"
)

if result['success']:
    print(f"Written to: {result['page_url']}")
else:
    print(f"Failed: {result['error']}")
```

### ✅ Integration Points:
- Called by the Flow Controller after summarization
- Receives formatted summaries from SummarizerAgent
- Writes to pre-configured Notion databases
- Returns URLs for tracking and reference

---

## Why Not Make It an Agent?

You might wonder: "Why not make Notion Tool an agent that decides where to organize content?"

**Answer**: **Separation of concerns!**

- The **PlannerAgent** decides WHAT to research
- The **SummarizerAgent** decides HOW to present it
- The **NotionTool** just executes the write

This separation makes the system:
- **Easier to test** (mock tools, test agents independently)
- **More maintainable** (change storage without touching logic)
- **More flexible** (swap Notion for another platform)
- **More predictable** (tools always behave the same)

**If you needed organization decisions**, you would create an **OrganizationAgent** that:
- Decides where content belongs
- Chooses optimal database structures
- Learns from usage patterns
- Then uses NotionTool to execute writes

This is the **Agent-Tool pattern** in action!

---

## Next Steps

Continue to **Chapter 6: Agent vs Tool Anatomy** for a deep dive into the
fundamental distinction between agents and tools — the core architectural principle!

Or explore how all these components work together in **Chapter 7: Pipeline Flow Visualizer**.
""")

# Sidebar with navigation
with st.sidebar:
    st.markdown("## 📚 Chapter Navigation")
    st.markdown("""
    **Previous**: Chapter 4 - The Summarizer Tongue

    **Current**: Chapter 5 - The Notion Hand

    **Next Chapters**:
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
    - ✅ What makes Notion Tool a TOOL
    - ✅ How tools execute without decisions
    - ✅ Why separation of concerns matters
    - ✅ When to use Agent-Tool pattern
    """)
