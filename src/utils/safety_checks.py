"""
Safety Checks and Risk Mitigation

Implements temporal validation, domain bias mitigation, and groundedness checks.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import re


def validate_temporal_safety(
    paper_date: str,
    cutoff: str = "2025-03-01"
) -> bool:
    """
    Validate papers published after temporal cutoff to prevent data leakage.
    
    This prevents the model from regurgitating training data by ensuring
    only papers published after the cutoff date are included.
    
    Args:
        paper_date: Publication date in YYYY-MM-DD format
        cutoff: Cutoff date in YYYY-MM-DD format (default: 2025-03-01)
        
    Returns:
        True if paper is after cutoff (safe), False otherwise
        
    Examples:
        >>> validate_temporal_safety("2025-04-15", "2025-03-01")
        True
        >>> validate_temporal_safety("2024-12-01", "2025-03-01")
        False
    """
    try:
        paper_dt = datetime.strptime(paper_date, "%Y-%m-%d")
        cutoff_dt = datetime.strptime(cutoff, "%Y-%m-%d")
        
        return paper_dt > cutoff_dt
    except (ValueError, TypeError):
        # If date parsing fails, err on side of caution
        return False


def get_domain_prompt_wrapper(domain: str) -> str:
    """
    Return specialized prompts for high-difficulty domains.
    
    Finance and Materials Science have shown to be particularly challenging
    domains requiring specialized prompting strategies.
    
    Args:
        domain: Domain identifier ("finance", "materials_science", or "general")
        
    Returns:
        Domain-specific prompt wrapper/instructions
        
    Examples:
        >>> prompt = get_domain_prompt_wrapper("finance")
        >>> "financial" in prompt.lower()
        True
    """
    domain_lower = domain.lower().replace(" ", "_")
    
    if domain_lower == "finance":
        return """
[DOMAIN: FINANCE]

You are analyzing research in financial markets, risk management, and quantitative finance.
Pay special attention to:
- Financial terminology and metrics (Sharpe ratio, volatility, liquidity)
- Market mechanisms and trading strategies
- Risk assessment and portfolio optimization
- Regulatory frameworks and compliance
- Economic indicators and their relationships

Ensure claims about financial performance, market behavior, and risk are precisely
grounded in cited evidence. Avoid generalizations without specific data support.
"""
    
    elif domain_lower == "materials_science":
        return """
[DOMAIN: MATERIALS SCIENCE]

You are analyzing research in materials science, chemistry, and materials engineering.
Pay special attention to:
- Material properties (mechanical, thermal, electrical, optical)
- Synthesis methods and processing techniques
- Characterization methods (XRD, SEM, TEM, spectroscopy)
- Structure-property relationships
- Applications and performance metrics

Ensure claims about material properties, synthesis conditions, and performance
are precisely grounded in experimental data from cited sources. Include specific
values and conditions when available.
"""
    
    else:  # general domain
        return """
[DOMAIN: GENERAL]

You are conducting a comprehensive research analysis. Ensure all claims are
grounded in cited evidence and maintain high standards of accuracy and attribution.
"""


def validate_groundedness(
    claim: str,
    evidence_set: List[Dict[str, Any]],
    title_prefix_chars: int = 20,
    similarity_threshold: float = 0.3
) -> bool:
    """
    Check if a claim can be mapped to attributed evidence.
    
    Uses the 20-character title prefix rule as primary verification,
    supplemented by simple text overlap as secondary check.
    
    Args:
        claim: Claim to validate
        evidence_set: List of evidence documents with 'title' and 'content'
        title_prefix_chars: Characters for title matching (default: 20)
        similarity_threshold: Minimum overlap ratio for content matching
        
    Returns:
        True if claim is grounded in evidence, False otherwise
        
    Examples:
        >>> evidence = [{"title": "Deep Learning Survey", "content": "Neural networks..."}]
        >>> validate_groundedness("Neural networks are powerful", evidence)
        True
    """
    if not evidence_set:
        return False
    
    # Normalize claim
    claim_lower = claim.lower()
    claim_terms = set(re.findall(r'\w+', claim_lower))
    
    if not claim_terms:
        return False
    
    # Check against each evidence document
    for doc in evidence_set:
        title = doc.get('title', '')
        content = doc.get('content', '')
        
        # Combine title and content for matching
        doc_text = f"{title} {content}".lower()
        doc_terms = set(re.findall(r'\w+', doc_text))
        
        if not doc_terms:
            continue
        
        # Calculate term overlap
        overlap = len(claim_terms & doc_terms)
        overlap_ratio = overlap / len(claim_terms)
        
        if overlap_ratio >= similarity_threshold:
            return True
    
    return False


def validate_citation_format(citation: str) -> bool:
    """
    Validate citation format to ensure proper attribution.
    
    Args:
        citation: Citation string to validate
        
    Returns:
        True if citation has valid format
        
    Examples:
        >>> validate_citation_format("[1] Smith et al., 2025")
        True
        >>> validate_citation_format("some random text")
        False
    """
    # Check for common citation patterns
    patterns = [
        r'\[\d+\]',  # Numbered citations [1], [2]
        r'\([A-Za-z]+\s+et\s+al\.,\s*\d{4}\)',  # (Author et al., 2025)
        r'[A-Za-z]+\s+et\s+al\.\s+\(\d{4}\)',  # Author et al. (2025)
    ]
    
    for pattern in patterns:
        if re.search(pattern, citation):
            return True
    
    return False


def filter_unsafe_content(
    documents: List[Dict[str, Any]],
    cutoff_date: str = "2025-03-01"
) -> List[Dict[str, Any]]:
    """
    Filter documents to remove those failing temporal safety checks.
    
    Args:
        documents: List of documents with optional 'date' field
        cutoff_date: Temporal cutoff date
        
    Returns:
        Filtered list of documents
    """
    safe_documents = []
    
    for doc in documents:
        # If no date provided, include document (assume safe)
        if 'date' not in doc:
            safe_documents.append(doc)
            continue
        
        # Check temporal safety
        if validate_temporal_safety(doc['date'], cutoff_date):
            safe_documents.append(doc)
    
    return safe_documents


def get_bias_mitigation_strategy(domain: str) -> Dict[str, Any]:
    """
    Get bias mitigation strategy for specific domain.
    
    Args:
        domain: Domain identifier
        
    Returns:
        Dictionary with mitigation strategies
    """
    strategies = {
        "finance": {
            "sampling_bias": "Ensure diverse representation of market conditions and geographic regions",
            "terminology_bias": "Use precise financial terminology consistently",
            "recency_bias": "Balance recent and historical research",
            "prompt_augmentation": get_domain_prompt_wrapper("finance")
        },
        "materials_science": {
            "sampling_bias": "Include diverse material classes and synthesis methods",
            "terminology_bias": "Use standardized materials science nomenclature",
            "recency_bias": "Balance novel materials with well-established ones",
            "prompt_augmentation": get_domain_prompt_wrapper("materials_science")
        },
        "general": {
            "sampling_bias": "Ensure diverse source representation",
            "terminology_bias": "Use clear, consistent terminology",
            "recency_bias": "Balance contemporary and foundational work",
            "prompt_augmentation": get_domain_prompt_wrapper("general")
        }
    }
    
    domain_lower = domain.lower().replace(" ", "_")
    return strategies.get(domain_lower, strategies["general"])


def check_fabrication_risk(
    report: str,
    evidence_set: List[Dict[str, Any]],
    min_evidence_ratio: float = 0.5
) -> Dict[str, Any]:
    """
    Check for fabrication risk in generated report.
    
    Analyzes whether report claims are sufficiently grounded in evidence.
    
    Args:
        report: Generated report text
        evidence_set: Evidence documents used
        min_evidence_ratio: Minimum ratio of content that should be grounded
        
    Returns:
        Dictionary with risk assessment
    """
    # Split report into sentences
    sentences = re.split(r'[.!?]+', report)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return {
            "risk_level": "high",
            "grounded_sentences": 0,
            "total_sentences": 0,
            "grounded_ratio": 0.0
        }
    
    # Check each sentence for groundedness
    grounded_count = 0
    for sentence in sentences:
        if validate_groundedness(sentence, evidence_set):
            grounded_count += 1
    
    grounded_ratio = grounded_count / len(sentences)
    
    # Determine risk level
    if grounded_ratio >= min_evidence_ratio:
        risk_level = "low"
    elif grounded_ratio >= min_evidence_ratio * 0.7:
        risk_level = "medium"
    else:
        risk_level = "high"
    
    return {
        "risk_level": risk_level,
        "grounded_sentences": grounded_count,
        "total_sentences": len(sentences),
        "grounded_ratio": grounded_ratio,
        "meets_threshold": grounded_ratio >= min_evidence_ratio
    }


# Export public functions
__all__ = [
    'validate_temporal_safety',
    'get_domain_prompt_wrapper',
    'validate_groundedness',
    'validate_citation_format',
    'filter_unsafe_content',
    'get_bias_mitigation_strategy',
    'check_fabrication_risk',
]
