"""
THE CLEANER STOMACH — CLEANER TOOL CHAPTER
===========================================

This Streamlit page teaches about the CleanerTool:
  • What makes it a TOOL (not an AGENT)
  • How it performs deterministic HTML cleaning
  • Interactive demonstration of cleaning logic
  • Visualizations of text extraction
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from src.tools.cleaner_tool import CleanerTool

# Page configuration
st.set_page_config(
    page_title="Chapter 3: The Cleaner Stomach (Cleaner Tool)",
    page_icon="🫀",
    layout="wide"
)

# Title and introduction
st.title("🫀 Chapter 3: The Cleaner Stomach — Cleaner Tool")

st.markdown("""
---

## The Research Organism's Digestive System

The **CleanerTool** is the **STOMACH** of our research organism.
It digests raw HTML and extracts the nutritious content (relevant text),
discarding the waste (ads, navigation, boilerplate).

But what makes it a **TOOL** rather than an **AGENT**?

""")

# Tool vs Agent comparison
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🔧 TOOL Characteristics

    The CleanerTool exhibits:
    - **Deterministic extraction rules**
    - **No content judgment**
    - **Mechanical parsing**
    - **Same HTML → Same output**

    It doesn't judge — it **extracts**.
    """)

with col2:
    st.markdown("""
    ### 🤖 vs. AGENT Characteristics

    An agent would:
    - Decide WHAT content is important
    - Adapt extraction strategy per site
    - Learn from content patterns
    - Judge relevance and quality

    Agents understand context; tools follow rules.
    """)

st.markdown("""
---

## Extraction Process

The CleanerTool performs **deterministic operations**:

1. **Parse HTML**: Convert raw HTML to structured DOM
2. **Remove Boilerplate**: Strip navigation, ads, footers
3. **Extract Content**: Find main text in article/main tags
4. **Clean Text**: Normalize whitespace, remove scripts
5. **No Judgment**: Never decides if content is relevant

Each step applies **consistent rules** — no intelligence required.

---

## Interactive Demo: Watch the Stomach Digest

Try it yourself! Give the Cleaner raw HTML and watch it extract clean text.
""")

# Interactive demonstration
st.subheader("🎮 Try the Cleaner Tool")

# Sample HTML for demo
sample_html = """<!DOCTYPE html>
<html>
<head>
    <title>AI Wildfire Detection Research</title>
    <style>.ad { display: none; }</style>
    <script>console.log('analytics');</script>
</head>
<body>
    <nav class="navigation">
        <a href="/">Home</a> | <a href="/about">About</a>
    </nav>

    <article>
        <h1>AI-Powered Wildfire Detection Systems</h1>
        <p>Machine learning techniques are revolutionizing wildfire detection.
        Early detection systems now use satellite imagery and computer vision
        to identify smoke and fire patterns with 94% accuracy.</p>

        <p>Recent advances in convolutional neural networks have enabled
        real-time monitoring across vast wilderness areas. These systems
        can alert authorities within minutes of fire ignition.</p>
    </article>

    <aside class="sidebar-ad">
        <div class="advertisement">Buy our product!</div>
    </aside>

    <footer>
        <p>© 2024 Example Site | <a href="/privacy">Privacy</a></p>
    </footer>
</body>
</html>"""

# Input controls
html_input = st.text_area(
    "Raw HTML Input",
    value=sample_html,
    height=300,
    help="Enter raw HTML to clean"
)

url_input = st.text_input(
    "Source URL (optional)",
    value="https://example.com/wildfire-ai",
    help="URL helps with metadata extraction"
)

# Run cleaner button
if st.button("🫀 Clean HTML", type="primary"):
    st.markdown("### Cleaning in Progress...")

    # Create cleaner with debug mode
    cleaner = CleanerTool(debug=False)

    # Show operation details
    with st.expander("📋 Cleaning Operation Details", expanded=False):
        st.json({
            "html_length": len(html_input),
            "url": url_input
        })

    # Execute cleaning
    with st.spinner("Cleaner digesting HTML..."):
        result = cleaner.clean_html(html_input, url_input)

    # Display results
    st.success("✅ Cleaning Complete!")

    # Show the results
    st.markdown("### 📊 Cleaning Results")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Input Size", f"{len(html_input):,} chars")
    with col2:
        st.metric("Output Size", f"{result['word_count']:,} words")
    with col3:
        reduction = (1 - len(result['clean_text']) / len(html_input)) * 100
        st.metric("Boilerplate Removed", f"{reduction:.0f}%")

    # Extracted content
    st.markdown("#### 📄 Extracted Content")
    st.markdown(f"**Title**: {result['title']}")
    st.markdown(f"**Clean Text**: (first 500 chars)")
    st.code(result['clean_text'][:500] + ("..." if len(result['clean_text']) > 500 else ""))

    # Metadata
    st.markdown("#### 🔍 Extraction Metadata")
    st.json({
        'title': result['title'],
        'word_count': result['word_count'],
        'url': result.get('url', 'N/A'),
        'extracted_at': str(result.get('timestamp', 'N/A'))
    })

    # Tool characteristics box
    with st.expander("🔍 Tool Behavior Analysis", expanded=True):
        st.markdown("""
        **What the Tool Did:**

        1. **Parsed HTML**: Converted raw HTML to structured DOM
        2. **Removed Boilerplate**: Stripped `<nav>`, `<footer>`, `<aside>`, `<script>`, `<style>`
        3. **Extracted Content**: Found text in `<article>` and `<p>` tags
        4. **Cleaned Text**: Normalized whitespace, removed excess newlines
        5. **No Judgment**: Didn't evaluate if content was good/relevant

        **What the Tool DID NOT Do:**
        - ❌ Decide which paragraphs are important
        - ❌ Judge content quality or relevance
        - ❌ Adapt extraction strategy based on topic
        - ❌ Summarize or interpret the content
        - ❌ Choose what to extract based on context

        This is **pure rule-based extraction** — the hallmark of a TOOL.
        """)

    # Cleaner statistics
    st.markdown("#### 📊 Cleaner Statistics")
    stats = cleaner.get_cleaning_stats()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Cleanings", stats['total_cleanings'])
    with col2:
        st.metric("Avg Words Extracted", f"{stats['avg_word_count']:.0f}")
    with col3:
        st.metric("Avg Cleanup Ratio", f"{stats['avg_reduction_ratio']*100:.0f}%")

st.markdown("""
---

## Code Example: How the Tool Works

Here's a simplified view of the CleanerTool's extraction:

```python
class CleanerTool:
    BOILERPLATE_TAGS = ['nav', 'header', 'footer', 'aside',
                        'script', 'style', 'ad']

    def clean_html(self, raw_html: str, url: str = "") -> Dict:
        # Parse HTML into structured DOM
        soup = BeautifulSoup(raw_html, 'html.parser')

        # RULE 1: Remove boilerplate tags
        for tag in soup.find_all(self.BOILERPLATE_TAGS):
            tag.decompose()

        # RULE 2: Extract main content
        main_content = soup.find(['article', 'main']) or soup.find('body')

        # RULE 3: Extract text and clean whitespace
        clean_text = main_content.get_text(separator=' ', strip=True)
        clean_text = re.sub(r'\\s+', ' ', clean_text)

        # Return structured result (no interpretation)
        return {
            'title': soup.title.string if soup.title else 'Untitled',
            'clean_text': clean_text,
            'word_count': len(clean_text.split())
        }
```

Notice how there are **NO decision points**:
- No "is this paragraph important?"
- No "does this match the research topic?"
- No "should I extract this table?"

Just **pure rule-based extraction**.

---

## Key Takeaway: Tools vs. Agents

| Aspect | Tool (Cleaner) | Agent (Summarizer) |
|--------|----------------|---------------------|
| **Purpose** | Extract text mechanically | Decide what's important |
| **Input** | Raw HTML | Clean text + context |
| **Logic** | Rule-based extraction | Judgment & synthesis |
| **Output** | All main text | Prioritized summary |
| **Adaptation** | Same rules always | Adapts to topic |

The CleanerTool is a **TOOL** because it exhibits:
- **Rule-based extraction**: No thinking, just parsing
- **Determinism**: Same HTML → Same output
- **No judgment**: Doesn't evaluate content
- **Simple responsibility**: Extract and clean

---

## What Gets Removed vs Kept

The Cleaner uses deterministic rules to decide what to remove:

### ❌ REMOVED (Boilerplate):
- Navigation menus (`<nav>`)
- Headers and footers
- Advertisements and sidebars
- Scripts and styles
- Social media buttons
- Cookie notices
- Related articles sections

### ✅ KEPT (Content):
- Article text (`<article>`, `<main>`)
- Paragraphs (`<p>`)
- Headings (`<h1>` - `<h6>`)
- Lists (`<ul>`, `<ol>`)
- Main body text

These rules are **ALWAYS THE SAME** — no adaptation, no learning.

---

## Next Steps

Continue to **Chapter 4: The Summarizer Tongue** to see how clean text
is transformed into intelligent summaries — this is where we meet our second AGENT!

Or try pasting different HTML above to see consistent cleaning behavior!
""")

# Sidebar with navigation
with st.sidebar:
    st.markdown("## 📚 Chapter Navigation")
    st.markdown("""
    **Previous**: Chapter 2 - The Crawler Limb

    **Current**: Chapter 3 - The Cleaner Stomach

    **Next Chapters**:
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
    - ✅ How HTML cleaning works
    - ✅ What boilerplate means
    - ✅ Why cleaning is deterministic
    - ✅ The difference between extraction and interpretation
    """)
