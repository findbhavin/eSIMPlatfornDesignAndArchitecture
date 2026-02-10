"""
Integration tests for ADRA-Bank framework
Tests end-to-end pipeline and mode switching
"""

import pytest
import asyncio
import os
from src.orchestrator import ResearchOrchestrator, ResearchResult
from src.modules.planner import ResearchPlanner
from src.modules.retriever import ResearchRetriever
from src.modules.reasoner import ResearchReasoner
from src.evaluation.adra_eval import ADRAEvaluator


class TestOrchestrator:
    """Test cases for Research Orchestrator"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.sample_corpus = [
            {
                'id': 'paper1',
                'title': 'Advances in Deep Learning for Natural Language Processing',
                'content': 'This paper surveys recent advances in deep learning techniques for NLP tasks including transformers and attention mechanisms.',
                'date': '2025-04-15'
            },
            {
                'id': 'paper2',
                'title': 'Neural Architecture Search Methods',
                'content': 'We present novel methods for automated neural architecture search using reinforcement learning and evolutionary algorithms.',
                'date': '2025-05-20'
            },
            {
                'id': 'paper3',
                'title': 'Efficient Training of Large Language Models',
                'content': 'This work explores efficient training strategies for large-scale language models including mixed precision and gradient checkpointing.',
                'date': '2025-06-10'
            },
        ]
    
    def test_orchestrator_initialization_default(self):
        """Test orchestrator initialization with defaults"""
        orchestrator = ResearchOrchestrator(mode="end-to-end")
        
        assert orchestrator.mode == "end-to-end"
        assert orchestrator.planner is not None
        assert orchestrator.retriever is not None
        assert orchestrator.reasoner is not None
    
    def test_orchestrator_initialization_custom(self):
        """Test orchestrator initialization with custom modules"""
        planner = ResearchPlanner(min_subtasks=5, max_subtasks=8)
        retriever = ResearchRetriever(max_tool_calls=5)
        reasoner = ResearchReasoner(target_token_output=10000)
        
        orchestrator = ResearchOrchestrator(
            planner=planner,
            retriever=retriever,
            reasoner=reasoner,
            mode="end-to-end"
        )
        
        assert orchestrator.planner == planner
        assert orchestrator.retriever == retriever
        assert orchestrator.reasoner == reasoner
    
    def test_orchestrator_invalid_mode(self):
        """Test orchestrator with invalid mode"""
        with pytest.raises(ValueError) as exc_info:
            ResearchOrchestrator(mode="invalid_mode")
        
        assert "Invalid mode" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_end_to_end_pipeline(self):
        """Test complete end-to-end pipeline"""
        orchestrator = ResearchOrchestrator(mode="end-to-end")
        
        query = "What are the latest advances in deep learning for NLP?"
        
        result = await orchestrator.execute_research(
            query=query,
            corpus=self.sample_corpus,
            domain="general"
        )
        
        # Verify result structure
        assert isinstance(result, ResearchResult)
        assert result.query == query
        assert result.plan is not None
        assert len(result.plan.ordered_subtasks) >= 5
        assert isinstance(result.evidence, list)
        assert result.synthesis is not None
        assert result.mode == "end-to-end"
        assert result.metadata['mode'] == "end-to-end"
        assert result.metadata['pipeline_complete']
    
    @pytest.mark.asyncio
    async def test_isolated_planning_mode(self):
        """Test isolated planning mode with gold evidence"""
        orchestrator = ResearchOrchestrator(mode="isolated_planning")
        
        query = "How do transformers work in NLP?"
        
        gold_evidence = [
            {
                'id': 'gold1',
                'title': 'Attention Is All You Need',
                'content': 'The transformer architecture uses self-attention mechanisms.',
                'score': 1.0
            }
        ]
        
        result = await orchestrator.execute_research(
            query=query,
            gold_evidence=gold_evidence
        )
        
        assert result.mode == "isolated_planning"
        assert result.metadata['used_gold_evidence']
        assert len(result.evidence) > 0
    
    @pytest.mark.asyncio
    async def test_isolated_retrieval_mode(self):
        """Test isolated retrieval mode with gold plan"""
        orchestrator = ResearchOrchestrator(mode="isolated_retrieval")
        
        query = "What are neural architecture search methods?"
        
        gold_plan = [
            "Review fundamental concepts of neural architecture search and optimization methods.",
            "Identify key challenges in automated architecture design for neural networks.",
            "Examine various methodologies used in reinforcement learning based architecture search.",
            "Analyze performance metrics and results from evolutionary algorithm based approaches.",
            "Explore potential applications of neural architecture search in various industries.",
        ]
        
        result = await orchestrator.execute_research(
            query=query,
            corpus=self.sample_corpus,
            gold_plan=gold_plan
        )
        
        assert result.mode == "isolated_retrieval"
        assert result.metadata['used_gold_plan']
        assert len(result.plan.ordered_subtasks) == len(gold_plan)
        assert result.evidence is not None
    
    @pytest.mark.asyncio
    async def test_isolated_retrieval_mode_missing_gold_plan(self):
        """Test isolated retrieval mode without gold plan raises error"""
        orchestrator = ResearchOrchestrator(mode="isolated_retrieval")
        
        with pytest.raises(ValueError) as exc_info:
            await orchestrator.execute_research(
                query="test query",
                corpus=self.sample_corpus
            )
        
        assert "requires gold_plan" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_isolated_reasoning_mode(self):
        """Test isolated reasoning mode with gold plan and evidence"""
        orchestrator = ResearchOrchestrator(mode="isolated_reasoning")
        
        query = "How do large language models work?"
        
        gold_plan = [
            "Review fundamental concepts of language modeling and neural networks.",
            "Identify key architectural components of transformer based models.",
            "Examine training methodologies for large scale language models.",
            "Analyze performance and capabilities of state of the art models.",
            "Explore applications and limitations of large language models.",
        ]
        
        gold_evidence = [
            {
                'id': 'gold1',
                'title': 'Language Models Are Few-Shot Learners',
                'content': 'Large language models demonstrate strong few-shot learning capabilities.',
                'score': 1.0
            }
        ]
        
        result = await orchestrator.execute_research(
            query=query,
            gold_plan=gold_plan,
            gold_evidence=gold_evidence
        )
        
        assert result.mode == "isolated_reasoning"
        assert result.metadata['used_gold_plan']
        assert result.metadata['used_gold_evidence']
        assert result.synthesis is not None
        assert result.synthesis.report is not None
    
    @pytest.mark.asyncio
    async def test_isolated_reasoning_mode_missing_inputs(self):
        """Test isolated reasoning mode without required inputs raises error"""
        orchestrator = ResearchOrchestrator(mode="isolated_reasoning")
        
        with pytest.raises(ValueError) as exc_info:
            await orchestrator.execute_research(query="test query")
        
        assert "requires gold_plan and gold_evidence" in str(exc_info.value)
    
    def test_mode_switching(self):
        """Test switching between modes"""
        orchestrator = ResearchOrchestrator(mode="end-to-end")
        assert orchestrator.mode == "end-to-end"
        
        orchestrator.set_mode("isolated_planning")
        assert orchestrator.mode == "isolated_planning"
        
        orchestrator.set_mode("isolated_retrieval")
        assert orchestrator.mode == "isolated_retrieval"
        
        orchestrator.set_mode("isolated_reasoning")
        assert orchestrator.mode == "isolated_reasoning"
    
    def test_mode_switching_invalid(self):
        """Test switching to invalid mode raises error"""
        orchestrator = ResearchOrchestrator(mode="end-to-end")
        
        with pytest.raises(ValueError):
            orchestrator.set_mode("invalid_mode")


class TestIntegrationEvaluation:
    """Test integration between modules and evaluation"""
    
    @pytest.mark.asyncio
    async def test_evaluation_with_orchestrator(self):
        """Test evaluation of orchestrator results"""
        orchestrator = ResearchOrchestrator(mode="end-to-end")
        evaluator = ADRAEvaluator(export_format="markdown")
        
        query = "What are the key concepts in quantum computing?"
        
        corpus = [
            {
                'id': 'q1',
                'title': 'Quantum Computing Fundamentals',
                'content': 'Quantum computing uses qubits and superposition for computation.',
                'date': '2025-04-01'
            }
        ]
        
        result = await orchestrator.execute_research(
            query=query,
            corpus=corpus
        )
        
        # Evaluate planning
        gold_subtasks = [
            "Review fundamental concepts of quantum mechanics and computation.",
            "Identify key challenges in building scalable quantum computers.",
            "Examine quantum algorithms and their applications today.",
            "Analyze error correction methods for quantum systems.",
            "Explore future potential of quantum computing technology.",
        ]
        
        planning_eval = evaluator.evaluate_planning(
            result.plan.ordered_subtasks,
            gold_subtasks
        )
        
        assert planning_eval.module == "planning"
        assert "jaccard" in planning_eval.metrics
        assert "recall" in planning_eval.metrics
        assert "precision" in planning_eval.metrics
    
    def test_evaluation_export_markdown(self):
        """Test exporting evaluation results to markdown"""
        evaluator = ADRAEvaluator(export_format="markdown")
        
        # Add some dummy evaluations
        evaluator.evaluate_planning(
            ["Task one with eight words here.", "Task two with eight words here."],
            ["Task one with eight words here.", "Task three different eight words here."]
        )
        
        markdown = evaluator.export_results()
        
        assert "# ADRA-Bank Evaluation Results" in markdown
        assert "Planning Module" in markdown
        assert "Jaccard" in markdown or "jaccard" in markdown.lower()


class TestSafetyIntegration:
    """Test safety checks integration with pipeline"""
    
    @pytest.mark.asyncio
    async def test_temporal_safety_filtering(self):
        """Test that temporal safety filtering works in pipeline"""
        from src.utils.safety_checks import filter_unsafe_content
        
        corpus_with_dates = [
            {
                'id': 'old1',
                'title': 'Old Paper',
                'content': 'Content from before cutoff.',
                'date': '2024-12-01'  # Before cutoff
            },
            {
                'id': 'new1',
                'title': 'New Paper',
                'content': 'Content from after cutoff.',
                'date': '2025-04-15'  # After cutoff
            },
        ]
        
        safe_docs = filter_unsafe_content(corpus_with_dates, cutoff_date="2025-03-01")
        
        # Should only include new paper
        assert len(safe_docs) == 1
        assert safe_docs[0]['id'] == 'new1'
    
    @pytest.mark.asyncio
    async def test_domain_strategy_in_retrieval(self):
        """Test domain-specific strategies are applied"""
        orchestrator = ResearchOrchestrator(mode="end-to-end")
        
        corpus = [
            {
                'id': 'fin1',
                'title': 'Risk Management in Financial Markets',
                'content': 'This paper discusses risk assessment and portfolio optimization.',
                'date': '2025-05-01'
            }
        ]
        
        result = await orchestrator.execute_research(
            query="How does risk management work in finance?",
            corpus=corpus,
            domain="finance"
        )
        
        assert result.metadata['domain'] == "finance"
        assert result.synthesis is not None


class TestEndToEndScenarios:
    """End-to-end scenario tests"""
    
    @pytest.mark.asyncio
    async def test_complete_research_workflow(self):
        """Test complete research workflow from query to report"""
        # Setup
        orchestrator = ResearchOrchestrator(mode="end-to-end")
        
        query = "What are the latest advances in materials science?"
        
        corpus = [
            {
                'id': 'mat1',
                'title': 'Advanced Materials for Energy Storage',
                'content': 'Novel lithium-ion battery materials with improved capacity and cycle life.',
                'date': '2025-04-10'
            },
            {
                'id': 'mat2',
                'title': 'Nanomaterials for Catalysis',
                'content': 'Nanostructured catalysts show enhanced activity for chemical reactions.',
                'date': '2025-05-15'
            },
        ]
        
        # Execute research
        result = await orchestrator.execute_research(
            query=query,
            corpus=corpus,
            domain="materials_science"
        )
        
        # Verify complete pipeline execution
        assert result.query == query
        assert len(result.plan.ordered_subtasks) >= 5
        assert len(result.evidence) > 0
        assert result.synthesis.report is not None
        assert len(result.synthesis.citations) > 0
        
        # Check that report contains expected sections
        report = result.synthesis.report
        assert "Background" in report
        assert "Problem" in report or "Problem Statement" in report
        assert "Methodology" in report
        assert "Results" in report
        assert "Future" in report
        
        # Check diagnostics
        assert len(result.synthesis.diagnostic_responses) > 0
        
        # Token count should be reasonable
        assert result.synthesis.token_count > 100
    
    @pytest.mark.asyncio
    async def test_diagnostic_isolation_workflow(self):
        """Test diagnostic workflow with isolated modes"""
        # Test each mode independently
        
        # 1. Isolated Planning
        planner_orch = ResearchOrchestrator(mode="isolated_planning")
        gold_evidence = [
            {'id': 'g1', 'title': 'Test', 'content': 'Test content', 'score': 1.0}
        ]
        
        plan_result = await planner_orch.execute_research(
            query="Test query for planning?",
            gold_evidence=gold_evidence
        )
        
        assert plan_result.mode == "isolated_planning"
        
        # 2. Isolated Retrieval
        retrieval_orch = ResearchOrchestrator(mode="isolated_retrieval")
        gold_plan = [
            "Review fundamental concepts and principles in the field of study.",
            "Identify key challenges and significant research gaps to address.",
            "Examine various methodologies and approaches used in recent research studies.",
            "Analyze main findings and key results from relevant published papers.",
            "Explore future directions and identify potential applications in practice.",
        ]
        
        corpus = [
            {'id': 't1', 'title': 'Test Doc', 'content': 'Test content here.'}
        ]
        
        retrieval_result = await retrieval_orch.execute_research(
            query="Test query for retrieval?",
            corpus=corpus,
            gold_plan=gold_plan
        )
        
        assert retrieval_result.mode == "isolated_retrieval"
        
        # 3. Isolated Reasoning
        reasoning_orch = ResearchOrchestrator(mode="isolated_reasoning")
        
        reasoning_result = await reasoning_orch.execute_research(
            query="Test query for reasoning?",
            gold_plan=gold_plan,
            gold_evidence=gold_evidence
        )
        
        assert reasoning_result.mode == "isolated_reasoning"


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
