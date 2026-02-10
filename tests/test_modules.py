"""
Unit tests for ADRA-Bank modules (Planning, Retrieval, Reasoning)
"""

import pytest
import asyncio
from src.modules.planner import ResearchPlanner, ResearchPlan
from src.modules.retriever import ResearchRetriever, RetrievalResult
from src.modules.reasoner import ResearchReasoner, DIAGNOSTIC_ASPECTS
from pydantic import ValidationError


class TestPlanner:
    """Test cases for Planning module (π)"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.planner = ResearchPlanner(min_subtasks=5, max_subtasks=10)
    
    def test_planner_initialization(self):
        """Test planner initialization"""
        assert self.planner.min_subtasks == 5
        assert self.planner.max_subtasks == 10
    
    def test_research_plan_validation_valid(self):
        """Test valid research plan"""
        valid_subtasks = [
            "Review the fundamental concepts and background of machine learning algorithms.",
            "Identify key challenges and research gaps in deep neural networks.",
            "Examine primary methodologies used in recent natural language processing studies.",
            "Analyze main findings from state of the art transformer models research.",
            "Explore potential future applications of large language models in industry.",
        ]
        
        plan = ResearchPlan(ordered_subtasks=valid_subtasks)
        assert len(plan.ordered_subtasks) == 5
        assert all(task.endswith('.') for task in plan.ordered_subtasks)
    
    def test_research_plan_validation_too_few_tasks(self):
        """Test plan with too few sub-tasks"""
        with pytest.raises(ValidationError) as exc_info:
            ResearchPlan(ordered_subtasks=[
                "Review the fundamental concepts of machine learning algorithms.",
                "Identify key challenges in deep learning research today.",
            ])
        
        assert "at least 5 items" in str(exc_info.value).lower()
    
    def test_research_plan_validation_too_many_tasks(self):
        """Test plan with too many sub-tasks"""
        too_many = [
            f"This is sub task number {i} with enough words to be valid."
            for i in range(15)
        ]
        
        with pytest.raises(ValidationError):
            ResearchPlan(ordered_subtasks=too_many)
    
    def test_research_plan_validation_word_count_too_few(self):
        """Test sub-task with too few words"""
        with pytest.raises(ValidationError) as exc_info:
            ResearchPlan(ordered_subtasks=[
                "Short task.",
                "Another short one.",
                "Review the fundamental concepts of machine learning algorithms.",
                "Identify key challenges in deep learning research today.",
                "Examine methodologies used in natural language processing studies.",
            ])
        
        assert "minimum is 8" in str(exc_info.value)
    
    def test_research_plan_validation_word_count_too_many(self):
        """Test sub-task with too many words"""
        with pytest.raises(ValidationError) as exc_info:
            ResearchPlan(ordered_subtasks=[
                "Review the fundamental concepts of machine learning algorithms including supervised unsupervised and reinforcement learning methods today.",
                "Identify key challenges and research gaps in deep learning research studies today.",
                "This is a very long sub task with way too many words that exceeds the maximum allowed limit here now definitely.",
                "Examine various methodologies and approaches used in natural language processing studies.",
                "Explore potential applications of large language models in various industries and domains.",
            ])
        
        assert "maximum is 20" in str(exc_info.value)
    
    def test_research_plan_validation_no_punctuation(self):
        """Test sub-task without proper punctuation"""
        with pytest.raises(ValidationError) as exc_info:
            ResearchPlan(ordered_subtasks=[
                "Review the fundamental concepts of machine learning algorithms",
                "Identify key challenges in deep learning research today.",
                "Examine methodologies used in natural language processing studies.",
                "Analyze main findings from transformer models research papers.",
                "Explore potential applications of language models in industry.",
            ])
        
        assert "complete sentence ending with punctuation" in str(exc_info.value)
    
    def test_research_plan_validation_citation_markers(self):
        """Test sub-task with forbidden citation markers"""
        with pytest.raises(ValidationError) as exc_info:
            ResearchPlan(ordered_subtasks=[
                "Review the concepts from paper [23] about neural networks.",
                "Identify key challenges in deep learning research today.",
                "Examine methodologies used in natural language processing studies.",
                "Analyze main findings from transformer models research papers.",
                "Explore potential applications of language models in industry.",
            ])
        
        assert "low-level details" in str(exc_info.value)
    
    def test_planner_plan_generation(self):
        """Test plan generation"""
        query = "What are the latest advances in quantum computing?"
        plan = self.planner.plan(query)
        
        assert isinstance(plan, ResearchPlan)
        assert len(plan.ordered_subtasks) >= 5
        assert len(plan.ordered_subtasks) <= 10
    
    def test_planner_validate_plan(self):
        """Test plan validation method"""
        valid_tasks = [
            "Review fundamental concepts of quantum computing and their applications.",
            "Identify key challenges in building scalable quantum computers today.",
            "Examine methodologies used in quantum algorithm development studies.",
            "Analyze main findings from quantum error correction research.",
            "Explore potential applications of quantum computing in industry.",
        ]
        
        assert self.planner.validate_plan(valid_tasks)
        
        invalid_tasks = ["Too short.", "Also short."]
        assert not self.planner.validate_plan(invalid_tasks)
    
    def test_planner_get_planning_prompt(self):
        """Test planning prompt generation"""
        query = "What are recent advances in robotics?"
        prompt = self.planner.get_planning_prompt(query)
        
        assert query in prompt
        assert "8-20 words" in prompt
        assert "complete sentence" in prompt


class TestRetriever:
    """Test cases for Retrieval module (ρ)"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.retriever = ResearchRetriever(
            max_tool_calls=10,
            token_budget=10000,
            title_prefix_chars=20
        )
        
        self.sample_corpus = [
            {
                'id': 'doc1',
                'title': 'Deep Learning for Computer Vision',
                'content': 'This paper presents advances in convolutional neural networks for image recognition.',
            },
            {
                'id': 'doc2',
                'title': 'Natural Language Processing with Transformers',
                'content': 'We introduce a new transformer architecture for language understanding tasks.',
            },
            {
                'id': 'doc3',
                'title': 'Quantum Computing Algorithms',
                'content': 'This work explores quantum algorithms for optimization problems.',
            },
        ]
    
    def test_retriever_initialization(self):
        """Test retriever initialization"""
        assert self.retriever.max_tool_calls == 10
        assert self.retriever.token_budget == 10000
        assert self.retriever.title_prefix_chars == 20
    
    @pytest.mark.asyncio
    async def test_keyword_search(self):
        """Test keyword search"""
        results = await self.retriever.keyword_search(
            "deep learning neural networks",
            self.sample_corpus
        )
        
        assert isinstance(results, list)
        assert len(results) > 0
        assert all(isinstance(r, RetrievalResult) for r in results)
        
        # Check that relevant doc is found
        doc_ids = [r.doc_id for r in results]
        assert 'doc1' in doc_ids
    
    @pytest.mark.asyncio
    async def test_semantic_search(self):
        """Test semantic search"""
        results = await self.retriever.semantic_search(
            "language models",
            self.sample_corpus
        )
        
        assert isinstance(results, list)
        assert len(results) > 0
    
    @pytest.mark.asyncio
    async def test_chunk_read(self):
        """Test chunk reading"""
        content = await self.retriever.chunk_read(
            'doc1',
            corpus=self.sample_corpus
        )
        
        assert content is not None
        assert 'convolutional neural networks' in content
    
    @pytest.mark.asyncio
    async def test_chunk_read_nonexistent(self):
        """Test chunk reading for non-existent document"""
        content = await self.retriever.chunk_read(
            'doc999',
            corpus=self.sample_corpus
        )
        
        assert content is None
    
    def test_verify_citation_match_exact(self):
        """Test exact citation matching"""
        assert self.retriever.verify_citation_match(
            "Deep Learning for Computer Vision",
            "Deep Learning for Computer Vision",
            threshold=20
        )
    
    def test_verify_citation_match_prefix(self):
        """Test prefix citation matching with 20 chars"""
        # First 20 chars: "deep learning for co"
        assert self.retriever.verify_citation_match(
            "Deep Learning for Computer Vision and Applications",
            "Deep Learning for Computer Vision Systems",
            threshold=20
        )
    
    def test_verify_citation_match_different(self):
        """Test non-matching citations"""
        assert not self.retriever.verify_citation_match(
            "Quantum Computing Algorithms",
            "Deep Learning for Computer Vision",
            threshold=20
        )
    
    @pytest.mark.asyncio
    async def test_retrieve_for_subtask(self):
        """Test retrieval for single subtask"""
        subtask = "Examine advances in deep learning for computer vision applications."
        
        results = await self.retriever.retrieve_for_subtask(
            subtask,
            self.sample_corpus,
            strategy="hybrid"
        )
        
        assert isinstance(results, list)
        assert len(results) > 0
    
    @pytest.mark.asyncio
    async def test_budget_enforcement(self):
        """Test that max tool calls are enforced"""
        retriever = ResearchRetriever(max_tool_calls=2)
        
        # Make multiple calls
        await retriever.keyword_search("test", self.sample_corpus)
        await retriever.semantic_search("test", self.sample_corpus)
        
        # This should return empty due to budget
        results = await retriever.keyword_search("test", self.sample_corpus)
        assert len(results) == 0
    
    def test_domain_strategy_finance(self):
        """Test domain-specific query refinement for finance"""
        query = "risk management"
        refined = self.retriever._apply_domain_strategy(query, "finance")
        
        assert "financial" in refined.lower()
        assert query in refined
    
    def test_domain_strategy_materials_science(self):
        """Test domain-specific query refinement for materials science"""
        query = "material properties"
        refined = self.retriever._apply_domain_strategy(query, "materials_science")
        
        assert "materials" in refined.lower()
        assert query in refined


class TestReasoner:
    """Test cases for Reasoning module (σ)"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.reasoner = ResearchReasoner(target_token_output=13000)
        
        self.sample_evidence = [
            {
                'id': 'doc1',
                'title': 'Machine Learning Survey',
                'content': 'Machine learning has transformed various industries through automated decision making.',
                'score': 0.95
            },
            {
                'id': 'doc2',
                'title': 'Deep Learning Applications',
                'content': 'Deep learning models achieve state-of-the-art performance in computer vision tasks.',
                'score': 0.87
            },
        ]
        
        self.sample_subtasks = [
            "Review fundamental concepts of machine learning algorithms.",
            "Identify key challenges in deep learning research.",
            "Examine methodologies used in neural network training.",
        ]
    
    def test_reasoner_initialization(self):
        """Test reasoner initialization"""
        assert self.reasoner.target_token_output == 13000
        assert self.reasoner.diagnostic_aspects == DIAGNOSTIC_ASPECTS
    
    def test_synthesize_report(self):
        """Test report synthesis"""
        query = "What are the advances in machine learning?"
        
        result = self.reasoner.synthesize_report(
            query,
            self.sample_subtasks,
            self.sample_evidence
        )
        
        assert result.report is not None
        assert len(result.report) > 0
        assert isinstance(result.citations, list)
        assert isinstance(result.diagnostic_responses, dict)
        assert isinstance(result.ungrounded_claims, list)
        assert result.token_count > 0
    
    def test_diagnostic_aspects_structure(self):
        """Test diagnostic aspects have correct structure"""
        assert "Background" in DIAGNOSTIC_ASPECTS
        assert "Problem" in DIAGNOSTIC_ASPECTS
        assert "Methodology" in DIAGNOSTIC_ASPECTS
        assert "Results" in DIAGNOSTIC_ASPECTS
        assert "Future" in DIAGNOSTIC_ASPECTS
        
        # Each aspect should have 3-4 questions
        for aspect, questions in DIAGNOSTIC_ASPECTS.items():
            assert len(questions) >= 3
            assert len(questions) <= 4
            assert all(isinstance(q, str) for q in questions)
    
    def test_extract_citations(self):
        """Test citation extraction"""
        citations = self.reasoner._extract_citations(self.sample_evidence)
        
        assert len(citations) == len(self.sample_evidence)
        assert all(c.doc_id for c in citations)
        assert all(c.title for c in citations)
    
    def test_evaluate_diagnostics(self):
        """Test diagnostic evaluation"""
        report = """
        # Background
        This report reviews machine learning fundamentals.
        
        # Problem
        Several challenges exist in deep learning.
        
        # Methodology  
        Various approaches are used in training.
        
        # Results
        State-of-the-art performance was achieved.
        
        # Future
        Future directions include more research.
        """
        
        diagnostics = self.reasoner._evaluate_diagnostics(report)
        
        assert isinstance(diagnostics, dict)
        assert len(diagnostics) > 0
        assert all(isinstance(v, bool) for v in diagnostics.values())
    
    def test_calculate_reasoning_metrics(self):
        """Test reasoning metrics calculation"""
        predicted = {
            "q1": True,
            "q2": False,
            "q3": True,
            "q4": True,
        }
        
        gold = {
            "q1": True,
            "q2": True,
            "q3": True,
            "q4": False,
        }
        
        metrics = self.reasoner.calculate_reasoning_metrics(predicted, gold)
        
        assert "accuracy" in metrics
        assert "f1" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        
        # Should be 2/4 = 0.5 accuracy
        assert metrics["accuracy"] == 0.5
    
    def test_identify_ungrounded_claims(self):
        """Test ungrounded claim identification"""
        # Long report with empty evidence should flag
        long_report = "Some claims about things. " * 100  # Make it long enough
        
        # With empty evidence and long report, should flag
        ungrounded = self.reasoner._identify_ungrounded_claims(long_report, [])
        assert len(ungrounded) > 0
        
        # With evidence, should not flag
        ungrounded = self.reasoner._identify_ungrounded_claims(
            "Machine learning has transformed industries.",
            self.sample_evidence
        )
        # May or may not flag depending on heuristics (not testing specific result)


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
