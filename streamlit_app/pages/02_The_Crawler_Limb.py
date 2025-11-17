"""
THE CRAWLER LIMB — SCRAPER TOOL CHAPTER
========================================

This Streamlit page teaches about the ScraperTool:
  • What makes it a TOOL (not an AGENT)
  • How it performs deterministic fetching
  • Interactive demonstration of scraping logic
  • Visualizations of fetch operations
"""

import streamlit as st
import sys
from pathlib import Path
import time

# Add project root to path for imports
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from src.tools.scraper_tool import ScraperTool

# Page configuration
st.set_page_config(
    page_title="Chapter 2: The Crawler Limb (Scraper Tool)",
    page_icon="🦾",
    layout="wide"
)

# Title and introduction
st.title("🦾 Chapter 2: The Crawler Limb — Scraper Tool")

st.markdown("""
---

## The Research Organism's Limb

The **ScraperTool** is the **LIMB** of our research organism.
It reaches out to the web and fetches pages exactly as instructed.

But what makes it a **TOOL** rather than an **AGENT**?

""")

# Tool vs Agent comparison
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🔧 TOOL Characteristics

    The ScraperTool exhibits:
    - **Deterministic execution**
    - **No strategic decision-making**
    - **Mechanical fetching**
    - **Same input → Same output**

    It doesn't strategize — it **executes**.
    """)

with col2:
    st.markdown("""
    ### 🤖 vs. AGENT Characteristics

    An agent would:
    - Decide WHICH URLs to fetch
    - Choose when to retry
    - Adapt crawling strategy
    - Learn from failures

    Agents think; tools just do.
    """)

st.markdown("""
---

## Execution Process

The ScraperTool performs **deterministic operations**:

1. **Receive URL**: Accept exact URL to fetch
2. **Send Request**: Make HTTP GET request with proper headers
3. **Handle Response**: Return raw HTML or error
4. **Report Status**: Return status code and metadata
5. **No Judgment**: Never decides if content is good/bad

Each step is **mechanical** — no intelligence required.

---

## Interactive Demo: Watch the Limb Reach

Try it yourself! Give the Scraper a URL and watch it fetch.
""")

# Interactive demonstration
st.subheader("🎮 Try the Scraper Tool")

# Input controls
url = st.text_input(
    "URL to Fetch",
    value="https://example.com",
    help="Enter any accessible URL"
)

col1, col2 = st.columns(2)
with col1:
    timeout = st.slider(
        "Timeout (seconds)",
        min_value=5,
        max_value=60,
        value=30,
        help="How long to wait before giving up"
    )

with col2:
    show_html = st.checkbox("Show raw HTML content", value=False)

# Run scraper button
if st.button("🦾 Fetch URL", type="primary"):
    st.markdown("### Fetching in Progress...")

    # Create scraper with debug mode
    scraper = ScraperTool(debug=False)

    # Show operation details
    with st.expander("📋 Fetch Operation Details", expanded=False):
        st.json({
            "url": url,
            "timeout": timeout,
            "user_agent": scraper.user_agent
        })

    # Execute fetch
    start_time = time.time()
    with st.spinner("Scraper reaching out..."):
        html_content, status_code, error_msg, metadata = scraper.fetch_url(url, timeout)
    fetch_time = time.time() - start_time

    # Display results
    if status_code == 200:
        st.success("✅ Fetch Complete!")

        # Show the results
        st.markdown("### 📊 Fetch Results")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Status Code", status_code)
        with col2:
            st.metric("Response Time", f"{metadata['response_time']:.2f}s")
        with col3:
            st.metric("Content Length", f"{len(html_content):,} chars")

        # Metadata
        st.markdown("#### 🔍 Response Metadata")
        st.json({
            'final_url': metadata['final_url'],
            'content_length': metadata['content_length'],
            'response_time': f"{metadata['response_time']:.3f}s"
        })

        # Optional HTML display
        if show_html:
            st.markdown("#### 📄 Raw HTML Content")
            st.code(html_content[:1000] + ("..." if len(html_content) > 1000 else ""), language="html")

        # Tool characteristics box
        with st.expander("🔍 Tool Behavior Analysis", expanded=True):
            st.markdown("""
            **What the Tool Did:**

            1. **Received Command**: Got URL and timeout parameters
            2. **Executed Mechanically**: Made HTTP GET request
            3. **Returned Data**: Provided raw HTML without interpretation
            4. **No Decisions**: Didn't judge if content was good/useful
            5. **Reported Metadata**: Status, timing, content length

            **What the Tool DID NOT Do:**
            - ❌ Decide whether to fetch this URL
            - ❌ Choose an alternate source if this failed
            - ❌ Retry on failure (just reported it)
            - ❌ Extract or interpret content
            - ❌ Judge content quality or relevance

            This is **pure execution** — the hallmark of a TOOL.
            """)
    else:
        st.error("❌ Fetch Failed!")

        st.markdown(f"**Error**: {error_msg}")
        st.markdown(f"**Status Code**: {status_code}")

        with st.expander("🔍 Tool Behavior on Failure", expanded=True):
            st.markdown("""
            **What the Tool Did:**

            1. **Attempted Fetch**: Tried to execute the command
            2. **Encountered Error**: Network/HTTP issue occurred
            3. **Reported Failure**: Returned error details
            4. **No Retry**: Didn't attempt alternative strategies

            **What an AGENT Would Do Differently:**
            - Try an alternate source
            - Use exponential backoff retry
            - Learn that this domain is unreliable
            - Decide whether to continue or abort mission

            Tools just report — Agents adapt.
            """)

    # Scraper statistics
    st.markdown("#### 📊 Scraper Statistics")
    stats = scraper.get_fetch_stats()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Fetches", stats['total_fetches'])
    with col2:
        st.metric("Success Rate", f"{stats['success_rate']*100:.0f}%")
    with col3:
        st.metric("Avg Response Time", f"{stats['avg_response_time']:.2f}s")

st.markdown("""
---

## Code Example: How the Tool Works

Here's a simplified view of the ScraperTool's execution:

```python
class ScraperTool:
    def fetch_url(self, url: str, timeout: int = 30) -> Tuple:
        # EXECUTION: Just fetch, no decisions
        try:
            response = requests.get(
                url,
                headers={'User-Agent': self.user_agent},
                timeout=timeout
            )

            # Return raw data without interpretation
            return (response.text, response.status_code, "", metadata)

        except Exception as e:
            # Report failure but don't try to fix it
            return (None, 0, str(e), metadata)
```

Notice how there are **NO decision points**:
- No "should I retry?"
- No "is this URL worth fetching?"
- No "is the content good quality?"

Just **pure mechanical execution**.

---

## Key Takeaway: Tools vs. Agents

| Aspect | Tool (Scraper) | Agent (Planner) |
|--------|----------------|-----------------|
| **Purpose** | Execute fetch commands | Decide what to fetch |
| **Input** | Explicit URL | High-level research topic |
| **Logic** | Deterministic HTTP GET | Strategic source selection |
| **Output** | Raw HTML | Prioritized URL plan |
| **Failures** | Reports error, stops | Adapts strategy, continues |

The ScraperTool is a **TOOL** because it exhibits:
- **Mechanical execution**: No thinking, just doing
- **Determinism**: Same input → Same output
- **No autonomy**: Can't make decisions
- **Simple responsibility**: Fetch and report

---

## When to Upgrade Tool → Agent

In **Phase 5**, we introduce **ScraperAgent** which CAN:
- Decide whether to retry failed fetches
- Choose alternative sources automatically
- Adapt crawling depth based on content
- Learn which domains are reliable

This demonstrates the **evolution from TOOL to AGENT**.

---

## Next Steps

Continue to **Chapter 3: The Cleaner Stomach** to see how raw HTML
is transformed into clean text — another TOOL that works with the Scraper.

Or try fetching different URLs above to see consistent tool behavior!
""")

# Sidebar with navigation
with st.sidebar:
    st.markdown("## 📚 Chapter Navigation")
    st.markdown("""
    **Previous**: Chapter 1 - The Mind

    **Current**: Chapter 2 - The Crawler Limb

    **Next Chapters**:
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
    - ✅ What makes something a TOOL
    - ✅ How tools execute deterministically
    - ✅ Why tools don't make decisions
    - ✅ The difference between tools and agents
    """)
