"""
Research Orchestrator - Pipeline Coordinator

Implements end-to-end and isolated diagnostic modes for the ADRA-Bank framework.
Coordinates Planning (π), Retrieval (ρ), and Reasoning (σ) modules.
"""

import asyncio
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import yaml
import os

from src.modules.planner import ResearchPlanner, ResearchPlan
from src.modules.retriever import ResearchRetriever, RetrievalResult
from src.modules.reasoner import ResearchReasoner, SynthesisResult


@dataclass
class ResearchResult:
    """Container for complete research pipeline results"""
    query: str
    plan: ResearchPlan
    evidence: List[Dict[str, Any]]
    synthesis: SynthesisResult
    mode: str
    metadata: Dict[str, Any]


class ResearchOrchestrator:
    """
    Pipeline coordinator for ADRA-Bank framework.
    
    Composition: A ≡ σ ∘ ρ ∘ π
    
    Modes:
    - "end-to-end": Sequential module chaining for holistic performance
    - "isolated_planning": Test planner with gold retrieval/reasoning
    - "isolated_retrieval": Inject gold plan, test retriever
    - "isolated_reasoning": Inject gold plan + evidence, test reasoner
    """
    
    def __init__(
        self,
        planner: Optional[ResearchPlanner] = None,
        retriever: Optional[ResearchRetriever] = None,
        reasoner: Optional[ResearchReasoner] = None,
        mode: str = "end-to-end",
        config_path: Optional[str] = None
    ):
        """
        Initialize orchestrator with modules and configuration.
        
        Args:
            planner: Planning module (π)
            retriever: Retrieval module (ρ)
            reasoner: Reasoning module (σ)
            mode: Operational mode
            config_path: Path to configuration file
        """
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize modules
        self.planner = planner or self._create_default_planner()
        self.retriever = retriever or self._create_default_retriever()
        self.reasoner = reasoner or self._create_default_reasoner()
        
        # Set mode
        valid_modes = [
            "end-to-end",
            "isolated_planning",
            "isolated_retrieval",
            "isolated_reasoning"
        ]
        
        if mode not in valid_modes:
            raise ValueError(f"Invalid mode: {mode}. Must be one of {valid_modes}")
        
        self.mode = mode
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """
        Load configuration from YAML file.
        
        Args:
            config_path: Path to config file
            
        Returns:
            Configuration dictionary
        """
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        
        # Try default location
        default_path = os.path.join(
            os.path.dirname(__file__),
            'config',
            'research_config.yaml'
        )
        
        if os.path.exists(default_path):
            with open(default_path, 'r') as f:
                return yaml.safe_load(f)
        
        # Return default config
        return {
            'planning': {
                'min_subtasks': 5,
                'max_subtasks': 10
            },
            'retrieval': {
                'max_tool_calls_per_subtask': 10,
                'token_budget': 10000
            },
            'reasoning': {
                'target_token_output': 13000
            }
        }
    
    def _create_default_planner(self) -> ResearchPlanner:
        """Create default planner from config"""
        planning_config = self.config.get('planning', {})
        
        return ResearchPlanner(
            min_subtasks=planning_config.get('min_subtasks', 5),
            max_subtasks=planning_config.get('max_subtasks', 10)
        )
    
    def _create_default_retriever(self) -> ResearchRetriever:
        """Create default retriever from config"""
        retrieval_config = self.config.get('retrieval', {})
        
        return ResearchRetriever(
            max_tool_calls=retrieval_config.get('max_tool_calls_per_subtask', 10),
            token_budget=retrieval_config.get('token_budget', 10000),
            title_prefix_chars=retrieval_config.get('title_prefix_match_chars', 20),
            target_latency=retrieval_config.get('target_latency_seconds', 76.0)
        )
    
    def _create_default_reasoner(self) -> ResearchReasoner:
        """Create default reasoner from config"""
        reasoning_config = self.config.get('reasoning', {})
        
        return ResearchReasoner(
            target_token_output=reasoning_config.get('target_token_output', 13000)
        )
    
    async def execute_research(
        self,
        query: str,
        corpus: Optional[List[Dict[str, Any]]] = None,
        gold_plan: Optional[List[str]] = None,
        gold_evidence: Optional[List[Dict[str, Any]]] = None,
        domain: Optional[str] = None
    ) -> ResearchResult:
        """
        Execute research pipeline in configured mode.
        
        Args:
            query: Research query
            corpus: Document corpus for retrieval (required for retrieval modes)
            gold_plan: Gold-standard plan for isolated modes
            gold_evidence: Gold-standard evidence for isolated modes
            domain: Optional domain for specialized strategies
            
        Returns:
            ResearchResult with complete pipeline output
        """
        metadata = {
            "mode": self.mode,
            "domain": domain
        }
        
        if self.mode == "end-to-end":
            return await self._execute_end_to_end(query, corpus, domain, metadata)
        
        elif self.mode == "isolated_planning":
            return await self._execute_isolated_planning(
                query, gold_evidence, domain, metadata
            )
        
        elif self.mode == "isolated_retrieval":
            if not gold_plan:
                raise ValueError("isolated_retrieval mode requires gold_plan")
            return await self._execute_isolated_retrieval(
                query, gold_plan, corpus, domain, metadata
            )
        
        elif self.mode == "isolated_reasoning":
            if not gold_plan or not gold_evidence:
                raise ValueError(
                    "isolated_reasoning mode requires gold_plan and gold_evidence"
                )
            return await self._execute_isolated_reasoning(
                query, gold_plan, gold_evidence, metadata
            )
        
        else:
            raise ValueError(f"Unknown mode: {self.mode}")
    
    async def _execute_end_to_end(
        self,
        query: str,
        corpus: Optional[List[Dict[str, Any]]],
        domain: Optional[str],
        metadata: Dict[str, Any]
    ) -> ResearchResult:
        """
        Execute full end-to-end pipeline: A ≡ σ ∘ ρ ∘ π
        
        Args:
            query: Research query
            corpus: Document corpus
            domain: Optional domain
            metadata: Result metadata
            
        Returns:
            Complete research result
        """
        # Step 1: Planning (π)
        plan = self.planner.plan(query)
        
        # Step 2: Retrieval (ρ)
        if corpus:
            evidence = await self._retrieve_evidence(
                plan.ordered_subtasks,
                corpus,
                domain
            )
        else:
            evidence = []
        
        # Step 3: Reasoning (σ)
        synthesis = self.reasoner.synthesize_report(
            query,
            plan.ordered_subtasks,
            evidence
        )
        
        metadata['pipeline_complete'] = True
        
        return ResearchResult(
            query=query,
            plan=plan,
            evidence=evidence,
            synthesis=synthesis,
            mode=self.mode,
            metadata=metadata
        )
    
    async def _execute_isolated_planning(
        self,
        query: str,
        gold_evidence: Optional[List[Dict[str, Any]]],
        domain: Optional[str],
        metadata: Dict[str, Any]
    ) -> ResearchResult:
        """
        Test planner with gold retrieval/reasoning.
        
        Args:
            query: Research query
            gold_evidence: Gold-standard evidence
            domain: Optional domain
            metadata: Result metadata
            
        Returns:
            Research result with real planning, gold retrieval/reasoning
        """
        # Real planning
        plan = self.planner.plan(query)
        
        # Use gold evidence if provided
        evidence = gold_evidence or []
        
        # Real reasoning on gold evidence
        synthesis = self.reasoner.synthesize_report(
            query,
            plan.ordered_subtasks,
            evidence
        )
        
        metadata['used_gold_evidence'] = gold_evidence is not None
        
        return ResearchResult(
            query=query,
            plan=plan,
            evidence=evidence,
            synthesis=synthesis,
            mode=self.mode,
            metadata=metadata
        )
    
    async def _execute_isolated_retrieval(
        self,
        query: str,
        gold_plan: List[str],
        corpus: Optional[List[Dict[str, Any]]],
        domain: Optional[str],
        metadata: Dict[str, Any]
    ) -> ResearchResult:
        """
        Test retriever with gold plan.
        
        Args:
            query: Research query
            gold_plan: Gold-standard plan
            corpus: Document corpus
            domain: Optional domain
            metadata: Result metadata
            
        Returns:
            Research result with gold planning, real retrieval
        """
        # Use gold plan
        from src.modules.planner import ResearchPlan
        plan = ResearchPlan(ordered_subtasks=gold_plan)
        
        # Real retrieval
        if corpus:
            evidence = await self._retrieve_evidence(
                gold_plan,
                corpus,
                domain
            )
        else:
            evidence = []
        
        # Real reasoning
        synthesis = self.reasoner.synthesize_report(
            query,
            gold_plan,
            evidence
        )
        
        metadata['used_gold_plan'] = True
        
        return ResearchResult(
            query=query,
            plan=plan,
            evidence=evidence,
            synthesis=synthesis,
            mode=self.mode,
            metadata=metadata
        )
    
    async def _execute_isolated_reasoning(
        self,
        query: str,
        gold_plan: List[str],
        gold_evidence: List[Dict[str, Any]],
        metadata: Dict[str, Any]
    ) -> ResearchResult:
        """
        Test reasoner with gold plan and evidence.
        
        Args:
            query: Research query
            gold_plan: Gold-standard plan
            gold_evidence: Gold-standard evidence
            metadata: Result metadata
            
        Returns:
            Research result with gold planning/retrieval, real reasoning
        """
        # Use gold plan
        from src.modules.planner import ResearchPlan
        plan = ResearchPlan(ordered_subtasks=gold_plan)
        
        # Use gold evidence
        evidence = gold_evidence
        
        # Real reasoning
        synthesis = self.reasoner.synthesize_report(
            query,
            gold_plan,
            evidence
        )
        
        metadata['used_gold_plan'] = True
        metadata['used_gold_evidence'] = True
        
        return ResearchResult(
            query=query,
            plan=plan,
            evidence=evidence,
            synthesis=synthesis,
            mode=self.mode,
            metadata=metadata
        )
    
    async def _retrieve_evidence(
        self,
        subtasks: List[str],
        corpus: List[Dict[str, Any]],
        domain: Optional[str]
    ) -> List[Dict[str, Any]]:
        """
        Retrieve evidence for all sub-tasks.
        
        Args:
            subtasks: Research sub-tasks
            corpus: Document corpus
            domain: Optional domain
            
        Returns:
            Aggregated evidence list
        """
        all_evidence = []
        seen_doc_ids = set()
        
        # Retrieve for each subtask
        for subtask in subtasks:
            results = await self.retriever.retrieve_for_subtask(
                subtask,
                corpus,
                strategy="hybrid",
                domain=domain
            )
            
            # Add unique results
            for result in results:
                if result.doc_id not in seen_doc_ids:
                    all_evidence.append({
                        'id': result.doc_id,
                        'title': result.title,
                        'content': result.content,
                        'score': result.score,
                        'metadata': result.metadata
                    })
                    seen_doc_ids.add(result.doc_id)
        
        return all_evidence
    
    def set_mode(self, mode: str):
        """
        Change operational mode.
        
        Args:
            mode: New mode to set
        """
        valid_modes = [
            "end-to-end",
            "isolated_planning",
            "isolated_retrieval",
            "isolated_reasoning"
        ]
        
        if mode not in valid_modes:
            raise ValueError(f"Invalid mode: {mode}. Must be one of {valid_modes}")
        
        self.mode = mode


# Export main classes
__all__ = ['ResearchOrchestrator', 'ResearchResult']
