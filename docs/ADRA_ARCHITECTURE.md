# ADRA-Bank Framework Architecture

## Overview

The **ADRA-Bank** (Autonomous Deep Research Agent - Bank) framework is a modular, diagnostic-ready system for academic research synthesis. It transforms traditional "black box" research workflows into transparent, verifiable pipelines through the composition of three independent modules:

**A ≡ σ ∘ ρ ∘ π**

Where:
- **π (Planning)**: Task decomposition module
- **ρ (Retrieval)**: Multi-source evidence acquisition module
- **σ (Reasoning)**: Synthesis and reporting module

## Design Principles

### 1. Modularity & Composability
Each module (π, ρ, σ) is independently testable and can be evaluated in isolation or as part of the complete pipeline. This enables:
- Pinpoint failure diagnosis
- Gold-standard input testing
- Transparent bottleneck identification

### 2. Diagnostic-Ready Architecture
The framework supports two operational modes:

#### End-to-End Mode
Sequential module chaining for holistic performance evaluation:
```
Query → Planning (π) → Retrieval (ρ) → Reasoning (σ) → Report
```

#### Isolated Modes
Gold-standard input testing for individual module diagnosis:
- **Isolated Planning**: Test planner with gold retrieval/reasoning
- **Isolated Retrieval**: Inject gold plan, test retriever
- **Isolated Reasoning**: Inject gold plan + evidence, test reasoner

### 3. Verifiability & Groundedness
All claims in generated reports must be attributable to source evidence through:
- 20-character title prefix matching
- Groundedness validation
- Ungrounded claim detection and flagging

## Module Specifications

### Module π: Planner (Task Decomposition)

**File**: `src/modules/planner.py`

**Purpose**: Transform user queries into structured, high-level research roadmaps.

**Key Features**:
- Generates 5-10 ordered sub-tasks
- Enforces 8-20 word limit per task
- Validates complete sentences with proper punctuation
- Prevents low-level details (citations, dataset IDs)
- Uses Pydantic v2 for validation

**Validation Rules**:
```python
ResearchPlan:
  - min_subtasks: 5
  - max_subtasks: 10
  - word_count: [8, 20] per task
  - complete_sentences: True
  - no_citations: True
  - no_dataset_ids: True
```

**Strategic Focus**: Overcomes the "planning bottleneck" in foundational LLMs by forcing comprehensive conceptual roadmaps with high Recall.

**Example Output**:
```
1. Review fundamental concepts of neural architecture search and optimization.
2. Identify key challenges in automated architecture design for networks.
3. Examine methodologies used in reinforcement learning based search.
4. Analyze performance metrics from evolutionary algorithm approaches.
5. Explore potential applications of neural architecture search.
```

### Module ρ: Retriever (Evidence Acquisition)

**File**: `src/modules/retriever.py`

**Purpose**: Acquire relevant evidence through multi-strategy retrieval.

**Key Features**:
- Async interface using `asyncio`
- Multiple retrieval strategies:
  - Keyword search
  - Semantic search (embedding-based)
  - Hierarchical chunk-read
- 20-character title prefix verification
- Token budget constraints (default: 10,000 tokens)
- Max tool-calls enforcement (default: 10 per subtask)
- Domain-specific strategies (Finance, Materials Science)

**Performance Targets**:
- Latency: ~76 seconds (Pareto-optimal)
- Accuracy: >39.81% (baseline: Grok Deeper Search)

**Verification Rule**:
```python
def verify_citation_match(predicted_title, ground_truth, threshold=20):
    """
    20-character normalized title prefix matching
    Handles truncation and URL inconsistencies
    """
    pred_norm = normalize(predicted_title)[:20]
    gt_norm = normalize(ground_truth)[:20]
    return pred_norm == gt_norm
```

**Domain Strategies**:
- **Finance**: Add financial terminology (risk, markets, portfolio)
- **Materials Science**: Add materials terms (synthesis, properties, characterization)

### Module σ: Reasoner (Synthesis & Reporting)

**File**: `src/modules/reasoner.py`

**Purpose**: Synthesize evidence into factually grounded research reports.

**Key Features**:
- Evidence-to-report synthesis
- 15-20 Boolean diagnostic validations
- 5-aspect coverage:
  - Background (3-4 diagnostics)
  - Problem Statement (3-4 diagnostics)
  - Methodology (3-4 diagnostics)
  - Results (3-4 diagnostics)
  - Future Directions (3-4 diagnostics)
- Citation tracking and attribution
- Ungrounded claim detection

**Performance Targets**:
- Reasoning Accuracy: >59% (baseline: o3-deep-research)
- Token Output: ~13,000 tokens (efficiency: Gemini-2.5-pro)

**Diagnostic Structure**:
```python
DIAGNOSTIC_ASPECTS = {
    "Background": [
        "Does the report provide relevant historical context?",
        "Are fundamental concepts clearly explained?",
        "Is the problem domain adequately introduced?",
        "Are key terminology and definitions provided?"
    ],
    "Problem": [
        "Is the research problem clearly stated?",
        "Are research gaps identified?",
        "Is the motivation for the research explained?",
        "Are limitations of existing approaches discussed?"
    ],
    # ... (3 more aspects)
}
```

**Fabrication Safeguard**: All claims must map to evidence via 20-character rule. Ungrounded claims are flagged and excluded.

## Pipeline Orchestration

### ResearchOrchestrator

**File**: `src/orchestrator.py`

**Purpose**: Coordinate module execution in different operational modes.

**Supported Modes**:

1. **End-to-End**
   ```python
   orchestrator = ResearchOrchestrator(mode="end-to-end")
   result = await orchestrator.execute_research(
       query="What are advances in quantum computing?",
       corpus=documents
   )
   ```

2. **Isolated Planning**
   ```python
   orchestrator = ResearchOrchestrator(mode="isolated_planning")
   result = await orchestrator.execute_research(
       query=query,
       gold_evidence=expert_evidence  # Bypass retrieval
   )
   ```

3. **Isolated Retrieval**
   ```python
   orchestrator = ResearchOrchestrator(mode="isolated_retrieval")
   result = await orchestrator.execute_research(
       query=query,
       gold_plan=expert_plan,  # Bypass planning
       corpus=documents
   )
   ```

4. **Isolated Reasoning**
   ```python
   orchestrator = ResearchOrchestrator(mode="isolated_reasoning")
   result = await orchestrator.execute_research(
       query=query,
       gold_plan=expert_plan,        # Bypass planning
       gold_evidence=expert_evidence  # Bypass retrieval
   )
   ```

**Configuration**: Loads from `src/config/research_config.yaml`

## Evaluation & Metrics

### File: `src/evaluation/adra_eval.py`

#### Planning & Retrieval Metrics (Jaccard/IoU)

```python
def calculate_jaccard(predicted: Set, gold: Set) -> Dict[str, float]:
    """
    Returns:
      - jaccard: IoU score (intersection over union)
      - recall: Coverage (% of gold items found)
      - precision: Structural correctness (% predicted items correct)
    
    Note: True Negatives undefined in retrieval sets
    """
```

**Interpretation**:
- **Recall (Coverage)**: Measures comprehensiveness
- **Precision**: Penalizes duplicates/irrelevant items
- **Jaccard**: Harmonic balance of both

#### Reasoning Metrics (F1-Score)

```python
def calculate_reasoning_f1(
    predicted_diagnostics: Dict[str, bool],
    gold_diagnostics: Dict[str, bool]
) -> Dict[str, float]:
    """
    Returns:
      - accuracy: % correct Boolean judgments
      - f1: Harmonic mean of precision and recall
      - precision: Of positive predictions, % correct
      - recall: Of actual positives, % found
    """
```

**LLM-as-a-Judge Support**: Compatible with o3-deep-research, Gemini-2.5-pro

#### Export Formats
- **Markdown**: Tables with module-specific metrics
- **JSON**: Structured data for programmatic access

## Safety & Risk Mitigation

### File: `src/utils/safety_checks.py`

#### 1. Temporal Validation
Prevents data leakage from training set:
```python
def validate_temporal_safety(paper_date: str, cutoff="2025-03-01") -> bool:
    """Only papers published AFTER cutoff are safe"""
```

#### 2. Domain Bias Mitigation
Specialized prompts for underrepresented domains:
- Finance: Emphasize financial metrics, regulatory context
- Materials Science: Focus on properties, synthesis, characterization

#### 3. Groundedness Validation
```python
def validate_groundedness(claim: str, evidence_set: List[Dict]) -> bool:
    """
    Check if claim maps to evidence via:
    - 20-character title matching
    - Term overlap ratio (threshold: 30%)
    """
```

#### 4. Fabrication Risk Assessment
```python
def check_fabrication_risk(report: str, evidence_set: List[Dict]) -> Dict:
    """
    Returns:
      - risk_level: "low", "medium", "high"
      - grounded_ratio: % of sentences grounded in evidence
      - meets_threshold: Boolean (>50% required)
    """
```

## Configuration

### File: `src/config/research_config.yaml`

```yaml
retrieval:
  target_latency_seconds: 76
  accuracy_baseline: 0.3981  # Grok Deeper Search
  max_tool_calls_per_subtask: 10
  title_prefix_match_chars: 20

reasoning:
  target_accuracy: 0.59  # o3-deep-research
  target_token_output: 13000  # Gemini-2.5-pro

planning:
  min_subtasks: 5
  max_subtasks: 10
  min_words_per_task: 8
  max_words_per_task: 20

safety:
  temporal_cutoff: "2025-03-01"
  enable_groundedness_check: true
  enable_domain_bias_mitigation: true
```

## Testing Strategy

### Unit Tests (`tests/test_modules.py`)

**Coverage**: 30 tests across all modules
- Planner validation (word count, punctuation, citations)
- Retriever functionality (search, budget enforcement, domain strategies)
- Reasoner synthesis (diagnostics, metrics, groundedness)

### Integration Tests (`tests/integration_test.py`)

**Coverage**: 17 tests for end-to-end scenarios
- Complete research workflows
- Mode switching
- Safety integration
- Evaluation integration

**Test Execution**:
```bash
# Unit tests
pytest tests/test_modules.py -v

# Integration tests  
pytest tests/integration_test.py -v

# All tests
pytest tests/ -v
```

## Performance Benchmarks

| Module | Metric | Target | Baseline Model |
|--------|--------|--------|----------------|
| Planner (π) | Recall | TBD | Expert annotation |
| Retriever (ρ) | Latency | ~76s | Grok Deeper Search |
| Retriever (ρ) | Accuracy | >39.81% | Grok Deeper Search |
| Reasoner (σ) | Accuracy | >59% | o3-deep-research |
| Reasoner (σ) | Token Output | ~13k | Gemini-2.5-pro |

## Usage Examples

### Basic End-to-End Research

```python
from src.orchestrator import ResearchOrchestrator

# Initialize
orchestrator = ResearchOrchestrator(mode="end-to-end")

# Define corpus
corpus = [
    {
        'id': 'doc1',
        'title': 'Deep Learning Survey',
        'content': 'Recent advances in neural networks...',
        'date': '2025-04-15'
    }
]

# Execute research
result = await orchestrator.execute_research(
    query="What are recent advances in deep learning?",
    corpus=corpus,
    domain="general"
)

# Access results
print(result.plan.ordered_subtasks)
print(result.synthesis.report)
print(result.synthesis.diagnostic_responses)
```

### Diagnostic Mode Testing

```python
# Test planning in isolation
orchestrator = ResearchOrchestrator(mode="isolated_planning")

gold_evidence = [...]  # Expert-curated evidence

result = await orchestrator.execute_research(
    query=query,
    gold_evidence=gold_evidence
)

# Evaluate planner performance
evaluator = ADRAEvaluator()
planning_metrics = evaluator.evaluate_planning(
    predicted=result.plan.ordered_subtasks,
    gold=expert_subtasks
)
```

### Safety-Checked Research

```python
from src.utils.safety_checks import (
    filter_unsafe_content,
    check_fabrication_risk
)

# Filter temporally unsafe documents
safe_corpus = filter_unsafe_content(
    corpus,
    cutoff_date="2025-03-01"
)

# Execute with safe corpus
result = await orchestrator.execute_research(
    query=query,
    corpus=safe_corpus
)

# Check fabrication risk
risk_assessment = check_fabrication_risk(
    result.synthesis.report,
    result.evidence
)

if risk_assessment['risk_level'] == 'high':
    print("Warning: High fabrication risk detected")
```

## Implementation Notes

### Async/Await Patterns
All retrieval operations use async/await for optimal performance:
```python
# Concurrent retrieval for multiple subtasks
results = await asyncio.gather(*[
    retriever.retrieve_for_subtask(task, corpus)
    for task in subtasks
])
```

### Type Hints
All functions include comprehensive type hints (mypy-compliant):
```python
async def keyword_search(
    self,
    query: str,
    corpus: List[Dict[str, Any]],
    budget: Optional[int] = None
) -> List[RetrievalResult]:
```

### Logging
Comprehensive logging for diagnostic traceability:
```python
import logging

logger = logging.getLogger(__name__)
logger.info(f"Planning completed: {len(plan.ordered_subtasks)} tasks")
```

## Extensibility

### Adding New Retrieval Sources
```python
class CustomRetriever(ResearchRetriever):
    async def database_search(self, query: str, db: Database):
        """Add custom retrieval method"""
        pass
```

### Custom Diagnostic Aspects
```python
CUSTOM_DIAGNOSTICS = {
    "Reproducibility": [
        "Are experimental details sufficient for reproduction?",
        "Are data and code availability mentioned?",
        "Are hyperparameters clearly specified?",
    ]
}
```

### Domain-Specific Strategies
```python
def _apply_domain_strategy(self, query: str, domain: str) -> str:
    if domain == "biology":
        return f"{query} molecular mechanisms pathways"
    # Add more domains...
```

## References

- **Pydantic v2**: https://docs.pydantic.dev/
- **Asyncio**: https://docs.python.org/3/library/asyncio.html
- **Pytest**: https://docs.pytest.org/

## Future Enhancements

1. **LLM Integration**: Connect actual language models for generation
2. **Embedding Models**: Add semantic search with sentence transformers
3. **Advanced Chunking**: Implement hierarchical document structures
4. **Multi-Language Support**: Extend to non-English research
5. **Collaborative Filtering**: User feedback integration
6. **Real-Time Updates**: Streaming results as they're generated

---

**Version**: 1.0  
**Last Updated**: 2026-02-10  
**Maintainers**: eSim Platform Team
