"""
Module π: Planner - Task Decomposition
Transform user query (Q) into structured research roadmap (T)

This module addresses the "planning bottleneck" in foundational LLMs by
generating comprehensive, high-level research task decompositions.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
import re


class ResearchPlan(BaseModel):
    """
    Pydantic model for validated research plans.
    
    Enforces:
    - 5-10 ordered sub-tasks
    - 8-20 words per task
    - Complete sentences (ending with punctuation)
    - High-level strategic focus
    """
    ordered_subtasks: List[str] = Field(
        ...,
        min_length=5,
        max_length=10,
        description="Ordered list of research sub-tasks"
    )
    
    @field_validator('ordered_subtasks')
    @classmethod
    def validate_subtasks(cls, subtasks: List[str]) -> List[str]:
        """
        Validate each sub-task meets requirements:
        - 8-20 words
        - Complete sentences
        - No low-level details, dataset numbers, or citation markers
        """
        validated = []
        
        for i, task in enumerate(subtasks):
            # Strip whitespace
            task = task.strip()
            
            # Check if task ends with proper punctuation
            if not task or task[-1] not in '.!?':
                raise ValueError(
                    f"Sub-task {i+1} must be a complete sentence ending with punctuation: '{task}'"
                )
            
            # Count words (split on whitespace)
            words = task.split()
            word_count = len(words)
            
            if word_count < 8:
                raise ValueError(
                    f"Sub-task {i+1} has {word_count} words, minimum is 8: '{task}'"
                )
            
            if word_count > 20:
                raise ValueError(
                    f"Sub-task {i+1} has {word_count} words, maximum is 20: '{task}'"
                )
            
            # Check for low-level patterns to avoid (citations, dataset IDs)
            low_level_patterns = [
                r'\[\d+\]',  # Citation markers like [1], [2]
                r'dataset\s+\d+',  # Dataset numbers
                r'figure\s+\d+',  # Figure references
                r'table\s+\d+',  # Table references
            ]
            
            for pattern in low_level_patterns:
                if re.search(pattern, task, re.IGNORECASE):
                    raise ValueError(
                        f"Sub-task {i+1} contains low-level details (citations/dataset numbers): '{task}'"
                    )
            
            validated.append(task)
        
        return validated
    
    def __str__(self) -> str:
        """String representation of research plan"""
        return "\n".join([f"{i+1}. {task}" for i, task in enumerate(self.ordered_subtasks)])


class ResearchPlanner:
    """
    Planning module (π) for ADRA-Bank framework.
    
    Transforms user queries into structured, high-level research roadmaps
    with 5-10 coarse-grained sub-tasks designed to overcome the "planning
    bottleneck" in foundational LLMs.
    
    Key Features:
    - Strategic decomposition (not tactical)
    - High Recall focus (comprehensive coverage)
    - Validated output via Pydantic models
    """
    
    def __init__(self, min_subtasks: int = 5, max_subtasks: int = 10):
        """
        Initialize planner with configurable constraints.
        
        Args:
            min_subtasks: Minimum number of sub-tasks (default: 5)
            max_subtasks: Maximum number of sub-tasks (default: 10)
        """
        self.min_subtasks = min_subtasks
        self.max_subtasks = max_subtasks
    
    def plan(self, query: str, context: Optional[str] = None) -> ResearchPlan:
        """
        Generate a structured research plan from a user query.
        
        This is a placeholder implementation that demonstrates the expected
        structure. In production, this would integrate with an LLM to generate
        actual research plans.
        
        Args:
            query: User's research question
            context: Optional contextual information
            
        Returns:
            ResearchPlan: Validated research plan with ordered sub-tasks
            
        Raises:
            ValueError: If generated plan fails validation
        """
        # Placeholder implementation - generates example sub-tasks
        # In production, this would call an LLM with carefully crafted prompts
        
        subtasks = self._generate_placeholder_subtasks(query)
        
        # Validate and return structured plan
        return ResearchPlan(ordered_subtasks=subtasks)
    
    def _generate_placeholder_subtasks(self, query: str) -> List[str]:
        """
        Generate placeholder sub-tasks for demonstration.
        
        In production, this would be replaced with LLM-based generation
        using prompts designed for high Recall and strategic planning.
        
        Args:
            query: User's research question
            
        Returns:
            List of sub-tasks meeting validation criteria
        """
        # Extract key terms from query (simple heuristic)
        query_lower = query.lower()
        
        # Generate generic research workflow sub-tasks
        subtasks = [
            f"Review the fundamental concepts and background related to {query[:50]}.",
            "Identify the key challenges and research gaps in the existing literature.",
            "Examine the primary methodologies and approaches used in recent studies.",
            "Analyze the main findings and results from relevant research papers.",
            "Explore potential applications and future research directions in this area.",
            "Compare different theoretical frameworks and their effectiveness in addressing problems.",
            "Synthesize insights from multiple sources to identify common patterns.",
        ]
        
        # Ensure we meet minimum requirements
        if len(subtasks) < self.min_subtasks:
            subtasks.extend([
                "Evaluate the limitations and constraints of current approaches.",
                "Investigate emerging trends and novel techniques in the field.",
            ])
        
        # Trim to max_subtasks
        return subtasks[:self.max_subtasks]
    
    def validate_plan(self, subtasks: List[str]) -> bool:
        """
        Validate a list of sub-tasks against requirements.
        
        Args:
            subtasks: List of sub-task strings
            
        Returns:
            True if valid, False otherwise
        """
        try:
            ResearchPlan(ordered_subtasks=subtasks)
            return True
        except ValueError:
            return False
    
    def get_planning_prompt(self, query: str) -> str:
        """
        Generate a strategic planning prompt for LLM integration.
        
        This prompt is designed to elicit high-level, comprehensive planning
        with focus on Recall over precision.
        
        Args:
            query: User's research question
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""You are an expert research strategist. Your task is to decompose the following research question into a comprehensive, high-level research plan.

Research Question: {query}

Requirements:
1. Generate {self.min_subtasks}-{self.max_subtasks} ordered sub-tasks
2. Each sub-task must be 8-20 words and a complete sentence
3. Focus on STRATEGIC, high-level tasks (not tactical details)
4. Ensure COMPREHENSIVE coverage (high Recall)
5. Avoid citations, dataset numbers, or figure references
6. Sub-tasks should be coarse-grained conceptual steps

Examples of GOOD sub-tasks:
- "Review the fundamental theoretical frameworks underlying neural architecture search."
- "Identify key challenges in scaling transformer models to longer contexts."
- "Examine recent advances in few-shot learning for natural language tasks."

Examples of BAD sub-tasks:
- "Read paper [23] about transformers." (too specific, has citation)
- "Look at dataset 5." (too low-level, has dataset number)
- "Review transformers." (too brief, under 8 words)

Generate the research plan now, with each sub-task on a new line, numbered."""

        return prompt


# Export main classes
__all__ = ['ResearchPlanner', 'ResearchPlan']
