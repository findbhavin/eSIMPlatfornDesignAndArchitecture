"""
Module ρ: Retriever - Multi-Source Evidence Acquisition

Async interface for keyword, semantic, and hierarchical "chunk-read" retrieval
with budget constraints and domain-specific strategies.
"""

import asyncio
from typing import List, Dict, Optional, Set, Any
from dataclasses import dataclass
import re


@dataclass
class RetrievalResult:
    """Container for retrieval results"""
    doc_id: str
    title: str
    content: str
    score: float
    metadata: Dict[str, Any]


class ResearchRetriever:
    """
    Retrieval module (ρ) for ADRA-Bank framework.
    
    Supports:
    - Keyword search
    - Semantic search  
    - Hierarchical chunk-read
    - 20-character title prefix verification
    - Token budget constraints
    - Domain-specific strategies
    
    Performance Target: ~76s latency (Pareto-optimal)
    """
    
    def __init__(
        self,
        max_tool_calls: int = 10,
        token_budget: int = 10000,
        title_prefix_chars: int = 20,
        target_latency: float = 76.0
    ):
        """
        Initialize retriever with budget constraints.
        
        Args:
            max_tool_calls: Maximum tool calls per subtask
            token_budget: Token budget for retrieval
            title_prefix_chars: Characters for title matching (default: 20)
            target_latency: Target latency in seconds
        """
        self.max_tool_calls = max_tool_calls
        self.token_budget = token_budget
        self.title_prefix_chars = title_prefix_chars
        self.target_latency = target_latency
        self.tool_call_count = 0
    
    async def keyword_search(
        self,
        query: str,
        corpus: List[Dict[str, Any]],
        budget: Optional[int] = None
    ) -> List[RetrievalResult]:
        """
        Perform keyword-based search over corpus.
        
        Args:
            query: Search query
            corpus: List of documents to search
            budget: Optional token budget override
            
        Returns:
            List of RetrievalResult objects ranked by relevance
        """
        self.tool_call_count += 1
        
        if self.tool_call_count > self.max_tool_calls:
            return []
        
        budget = budget or self.token_budget
        results = []
        
        # Simple keyword matching (placeholder implementation)
        # In production, this would use proper IR techniques
        query_terms = set(query.lower().split())
        
        for doc in corpus:
            doc_text = f"{doc.get('title', '')} {doc.get('content', '')}".lower()
            
            # Calculate simple overlap score
            doc_terms = set(doc_text.split())
            overlap = len(query_terms & doc_terms)
            
            if overlap > 0:
                result = RetrievalResult(
                    doc_id=doc.get('id', ''),
                    title=doc.get('title', ''),
                    content=doc.get('content', ''),
                    score=float(overlap) / len(query_terms),
                    metadata={
                        'method': 'keyword',
                        'overlap_terms': overlap
                    }
                )
                results.append(result)
        
        # Sort by score descending
        results.sort(key=lambda x: x.score, reverse=True)
        
        # Apply budget constraints (simplified)
        total_tokens = 0
        filtered_results = []
        
        for result in results:
            # Rough token estimate: ~4 chars per token
            result_tokens = len(result.content) // 4
            
            if total_tokens + result_tokens <= budget:
                filtered_results.append(result)
                total_tokens += result_tokens
            else:
                break
        
        # Simulate async operation
        await asyncio.sleep(0.1)
        
        return filtered_results
    
    async def semantic_search(
        self,
        query: str,
        corpus: List[Dict[str, Any]],
        budget: Optional[int] = None
    ) -> List[RetrievalResult]:
        """
        Perform semantic search over corpus.
        
        In production, this would use embeddings and vector similarity.
        
        Args:
            query: Search query
            corpus: List of documents to search
            budget: Optional token budget override
            
        Returns:
            List of RetrievalResult objects ranked by semantic similarity
        """
        self.tool_call_count += 1
        
        if self.tool_call_count > self.max_tool_calls:
            return []
        
        budget = budget or self.token_budget
        
        # Placeholder: Falls back to keyword search
        # In production, would use sentence transformers or similar
        results = await self.keyword_search(query, corpus, budget)
        
        # Update metadata
        for result in results:
            result.metadata['method'] = 'semantic'
        
        return results
    
    async def chunk_read(
        self,
        doc_id: str,
        section: Optional[str] = None,
        corpus: Optional[List[Dict[str, Any]]] = None
    ) -> Optional[str]:
        """
        Hierarchical chunk-read for detailed document access.
        
        Args:
            doc_id: Document identifier
            section: Optional section to read
            corpus: Document corpus
            
        Returns:
            Content string or None if not found
        """
        self.tool_call_count += 1
        
        if self.tool_call_count > self.max_tool_calls:
            return None
        
        if not corpus:
            return None
        
        # Find document by ID
        doc = None
        for d in corpus:
            if d.get('id') == doc_id:
                doc = d
                break
        
        if not doc:
            return None
        
        content = doc.get('content', '')
        
        # If section specified, try to extract it
        if section and content:
            # Simple section extraction (placeholder)
            # In production, would parse document structure
            pattern = rf"{re.escape(section)}.*?(?=\n\n|\Z)"
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            
            if match:
                content = match.group(0)
        
        # Simulate async operation
        await asyncio.sleep(0.05)
        
        return content
    
    def verify_citation_match(
        self,
        predicted_title: str,
        ground_truth: str,
        threshold: Optional[int] = None
    ) -> bool:
        """
        Verify citation match using 20-character prefix rule.
        
        Handles truncation and URL inconsistencies by comparing
        normalized title prefixes.
        
        Args:
            predicted_title: Title from retrieval
            ground_truth: Ground truth title
            threshold: Character threshold (default: self.title_prefix_chars)
            
        Returns:
            True if titles match within threshold
        """
        threshold = threshold or self.title_prefix_chars
        
        # Normalize titles: lowercase, remove extra whitespace
        pred_norm = ' '.join(predicted_title.lower().split())
        gt_norm = ' '.join(ground_truth.lower().split())
        
        # Compare prefixes
        pred_prefix = pred_norm[:threshold]
        gt_prefix = gt_norm[:threshold]
        
        return pred_prefix == gt_prefix
    
    async def retrieve_for_subtask(
        self,
        subtask: str,
        corpus: List[Dict[str, Any]],
        strategy: str = "hybrid",
        domain: Optional[str] = None
    ) -> List[RetrievalResult]:
        """
        Retrieve evidence for a single research sub-task.
        
        Args:
            subtask: Research sub-task description
            corpus: Document corpus
            strategy: Retrieval strategy ("keyword", "semantic", "hybrid")
            domain: Optional domain for specialized strategies
            
        Returns:
            List of relevant documents
        """
        # Reset tool call counter for this subtask
        self.tool_call_count = 0
        
        # Apply domain-specific strategies
        if domain:
            query = self._apply_domain_strategy(subtask, domain)
        else:
            query = subtask
        
        results = []
        
        if strategy == "keyword":
            results = await self.keyword_search(query, corpus)
        elif strategy == "semantic":
            results = await self.semantic_search(query, corpus)
        elif strategy == "hybrid":
            # Combine both approaches
            keyword_results = await self.keyword_search(query, corpus)
            semantic_results = await self.semantic_search(query, corpus)
            
            # Merge and deduplicate
            seen_ids = set()
            for result in keyword_results + semantic_results:
                if result.doc_id not in seen_ids:
                    results.append(result)
                    seen_ids.add(result.doc_id)
            
            # Re-sort by score
            results.sort(key=lambda x: x.score, reverse=True)
        
        return results
    
    def _apply_domain_strategy(self, query: str, domain: str) -> str:
        """
        Apply domain-specific query refinement.
        
        Args:
            query: Original query
            domain: Domain identifier ("finance", "materials_science")
            
        Returns:
            Refined query
        """
        domain_lower = domain.lower()
        
        if domain_lower == "finance":
            # Add financial terminology
            return f"{query} financial markets risk management"
        elif domain_lower == "materials_science":
            # Add materials science terminology  
            return f"{query} materials properties synthesis characterization"
        
        return query
    
    def get_retrieval_stats(self) -> Dict[str, Any]:
        """
        Get retrieval statistics for diagnostics.
        
        Returns:
            Dictionary with retrieval metrics
        """
        return {
            'tool_calls_used': self.tool_call_count,
            'tool_calls_limit': self.max_tool_calls,
            'token_budget': self.token_budget,
            'title_prefix_chars': self.title_prefix_chars,
        }


# Export main class
__all__ = ['ResearchRetriever', 'RetrievalResult']
