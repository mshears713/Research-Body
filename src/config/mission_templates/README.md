# Mission Templates

This directory contains pre-configured mission templates for different research domains.

## Available Templates

### 1. **wildfire_research.yaml**
- **Domain**: Environmental Science & Disaster Management
- **Focus**: AI/ML for wildfire detection and early warning
- **Sources**: NASA, USFS, NIFC, NOAA
- **Style**: Technical

### 2. **hardware_security.yaml**
- **Domain**: Cybersecurity & Hardware Engineering
- **Focus**: Hardware vulnerabilities, side-channel attacks
- **Sources**: Academic conferences, security research
- **Style**: Technical (high quality threshold)

### 3. **ai_ethics.yaml**
- **Domain**: Ethics, Policy & Social Impact
- **Focus**: AI fairness, bias, responsible deployment
- **Sources**: Partnership on AI, AI Now Institute
- **Style**: Executive (accessible)

### 4. **quantum_computing.yaml**
- **Domain**: Quantum Computing & Cryptography
- **Focus**: Quantum algorithms, hardware, applications
- **Sources**: IBM, Google, Rigetti, arXiv
- **Style**: Technical

### 5. **climate_modeling.yaml**
- **Domain**: Climate Science & Environmental Modeling
- **Focus**: ML-enhanced climate prediction
- **Sources**: IPCC, NASA, NOAA, ECMWF
- **Style**: Technical

## Usage

### From Python:
```python
import yaml
from pathlib import Path

# Load a template
template_path = Path("src/config/mission_templates/wildfire_research.yaml")
with open(template_path) as f:
    mission_config = yaml.safe_load(f)

# Use with FlowController
from src.pipeline.mission_model import MissionRequest

request = MissionRequest(
    topic=mission_config['topic'],
    max_sources=mission_config['max_sources'],
    summary_style=mission_config['summary_style']
)
```

### From Streamlit Console:
Templates will be available in the Mission Console (Chapter 8) dropdown menu.

## Template Structure

Each template includes:

- **Mission Metadata**: Name, domain, research type
- **Research Topic**: Detailed topic description
- **Target URLs**: Curated starting sources
- **Keywords**: Domain-specific search terms
- **Scraping Config**: Crawling depth, source limits
- **Content Preferences**: Summary style, quality thresholds
- **Output Config**: Storage and export options
- **Focus Areas**: Key research themes
- **Notes**: Usage guidance and context

## Creating Custom Templates

To create your own template:

1. Copy an existing template
2. Modify the fields for your domain
3. Curate high-quality target URLs
4. Define domain-specific keywords
5. Set appropriate quality thresholds
6. Add descriptive notes

## Teaching Note

These templates demonstrate:
- **Domain specialization**: Different research areas need different configurations
- **Source curation**: Quality sources improve results
- **Keyword engineering**: Domain terminology improves relevance filtering
- **Style adaptation**: Technical vs. executive summaries for different audiences

Templates make the Research Body immediately useful for specific research tasks!
