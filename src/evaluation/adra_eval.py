"""
ADRA Evaluation and Metrics

Implements Jaccard Index for Planning/Retrieval and F1-Score for Reasoning.
Supports LLM-as-a-Judge automation and exports results in Markdown format.
"""

from typing import Set, Dict, List, Any, Optional
from dataclasses import dataclass


def calculate_jaccard(predicted: Set, gold: Set) -> Dict[str, float]:
    """
    Calculate Jaccard Index (IoU) for Planning and Retrieval metrics.
    
    Note: True Negatives are undefined in retrieval sets, so we focus on
    Recall (coverage) and Precision (structural correctness).
    
    Args:
        predicted: Set of predicted items
        gold: Set of gold-standard items
        
    Returns:
        Dictionary with jaccard, recall, and precision scores
        
    Examples:
        >>> pred = {"task1", "task2", "task3"}
        >>> gold = {"task1", "task2", "task4", "task5"}
        >>> metrics = calculate_jaccard(pred, gold)
        >>> metrics['recall']  # 2/4 = 0.5
        0.5
    """
    if not gold:
        return {
            "jaccard": 0.0,
            "recall": 0.0,
            "precision": 0.0
        }
    
    intersection = predicted & gold
    union = predicted | gold
    
    # Jaccard Index (IoU)
    jaccard = len(intersection) / len(union) if union else 0.0
    
    # Recall (Coverage): What fraction of gold items were found?
    recall = len(intersection) / len(gold) if gold else 0.0
    
    # Precision: What fraction of predicted items were correct?
    precision = len(intersection) / len(predicted) if predicted else 0.0
    
    return {
        "jaccard": jaccard,
        "recall": recall,
        "precision": precision
    }


def calculate_reasoning_f1(
    predicted_diagnostics: Dict[str, bool],
    gold_diagnostics: Dict[str, bool]
) -> Dict[str, float]:
    """
    Calculate F1-Score for Boolean diagnostic reasoning.
    
    Computes accuracy and F1 as harmonic mean of coverage and correctness.
    
    Args:
        predicted_diagnostics: Model's Boolean responses to diagnostic questions
        gold_diagnostics: Ground truth Boolean responses
        
    Returns:
        Dictionary with accuracy, f1, precision, and recall
        
    Examples:
        >>> pred = {"q1": True, "q2": False, "q3": True}
        >>> gold = {"q1": True, "q2": True, "q3": True}
        >>> metrics = calculate_reasoning_f1(pred, gold)
        >>> metrics['accuracy']  # 2/3 correct
        0.6666...
    """
    if not gold_diagnostics:
        return {
            "accuracy": 0.0,
            "f1": 0.0,
            "precision": 0.0,
            "recall": 0.0
        }
    
    correct = 0
    total = 0
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    
    for question, gold_value in gold_diagnostics.items():
        if question not in predicted_diagnostics:
            # Missing prediction counts as incorrect
            total += 1
            if gold_value:
                false_negatives += 1
            continue
        
        pred_value = predicted_diagnostics[question]
        total += 1
        
        if pred_value == gold_value:
            correct += 1
        
        if pred_value and gold_value:
            true_positives += 1
        elif pred_value and not gold_value:
            false_positives += 1
        elif not pred_value and gold_value:
            false_negatives += 1
    
    # Accuracy: Overall correct rate
    accuracy = correct / total if total > 0 else 0.0
    
    # Precision: Of positive predictions, how many were correct?
    precision = (
        true_positives / (true_positives + false_positives)
        if (true_positives + false_positives) > 0
        else 0.0
    )
    
    # Recall: Of actual positives, how many were found?
    recall = (
        true_positives / (true_positives + false_negatives)
        if (true_positives + false_negatives) > 0
        else 0.0
    )
    
    # F1: Harmonic mean of precision and recall
    f1 = (
        2 * (precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )
    
    return {
        "accuracy": accuracy,
        "f1": f1,
        "precision": precision,
        "recall": recall
    }


@dataclass
class EvaluationResult:
    """Container for evaluation results"""
    module: str
    metrics: Dict[str, float]
    details: Dict[str, Any]


class ADRAEvaluator:
    """
    Comprehensive evaluator for ADRA-Bank framework.
    
    Supports:
    - Planning evaluation (Jaccard/IoU)
    - Retrieval evaluation (Jaccard/IoU)
    - Reasoning evaluation (F1-Score)
    - LLM-as-a-Judge automation
    - Markdown export
    """
    
    def __init__(
        self,
        use_llm_judge: bool = False,
        export_format: str = "markdown"
    ):
        """
        Initialize evaluator.
        
        Args:
            use_llm_judge: Whether to use LLM-as-a-Judge for evaluation
            export_format: Output format ("markdown", "json", "csv")
        """
        self.use_llm_judge = use_llm_judge
        self.export_format = export_format
        self.results: List[EvaluationResult] = []
    
    def evaluate_planning(
        self,
        predicted_subtasks: List[str],
        gold_subtasks: List[str]
    ) -> EvaluationResult:
        """
        Evaluate planning module output.
        
        Args:
            predicted_subtasks: Generated sub-tasks
            gold_subtasks: Expert-annotated sub-tasks
            
        Returns:
            EvaluationResult with Jaccard metrics
        """
        # Normalize to sets for comparison
        pred_set = set(self._normalize_subtasks(predicted_subtasks))
        gold_set = set(self._normalize_subtasks(gold_subtasks))
        
        metrics = calculate_jaccard(pred_set, gold_set)
        
        result = EvaluationResult(
            module="planning",
            metrics=metrics,
            details={
                "predicted_count": len(predicted_subtasks),
                "gold_count": len(gold_subtasks),
                "overlap_count": len(pred_set & gold_set)
            }
        )
        
        self.results.append(result)
        return result
    
    def evaluate_retrieval(
        self,
        predicted_citations: List[str],
        gold_citations: List[str],
        title_prefix_chars: int = 20
    ) -> EvaluationResult:
        """
        Evaluate retrieval module output.
        
        Uses 20-character title prefix matching for verification.
        
        Args:
            predicted_citations: Retrieved document titles
            gold_citations: Expert-annotated citations
            title_prefix_chars: Characters for prefix matching
            
        Returns:
            EvaluationResult with Jaccard metrics
        """
        # Normalize titles to prefixes
        pred_set = set(
            self._normalize_title(title, title_prefix_chars)
            for title in predicted_citations
        )
        gold_set = set(
            self._normalize_title(title, title_prefix_chars)
            for title in gold_citations
        )
        
        metrics = calculate_jaccard(pred_set, gold_set)
        
        result = EvaluationResult(
            module="retrieval",
            metrics=metrics,
            details={
                "predicted_count": len(predicted_citations),
                "gold_count": len(gold_citations),
                "overlap_count": len(pred_set & gold_set),
                "prefix_chars": title_prefix_chars
            }
        )
        
        self.results.append(result)
        return result
    
    def evaluate_reasoning(
        self,
        predicted_diagnostics: Dict[str, bool],
        gold_diagnostics: Dict[str, bool]
    ) -> EvaluationResult:
        """
        Evaluate reasoning module output.
        
        Args:
            predicted_diagnostics: Generated diagnostic responses
            gold_diagnostics: Ground truth diagnostic responses
            
        Returns:
            EvaluationResult with F1 metrics
        """
        metrics = calculate_reasoning_f1(predicted_diagnostics, gold_diagnostics)
        
        result = EvaluationResult(
            module="reasoning",
            metrics=metrics,
            details={
                "total_diagnostics": len(gold_diagnostics),
                "correct_predictions": int(metrics["accuracy"] * len(gold_diagnostics)),
            }
        )
        
        self.results.append(result)
        return result
    
    def _normalize_subtasks(self, subtasks: List[str]) -> List[str]:
        """
        Normalize sub-tasks for comparison.
        
        Removes punctuation, lowercases, strips whitespace.
        
        Args:
            subtasks: List of sub-task strings
            
        Returns:
            Normalized sub-tasks
        """
        normalized = []
        for task in subtasks:
            # Lowercase and strip
            task = task.lower().strip()
            # Remove trailing punctuation
            task = task.rstrip('.!?')
            # Normalize whitespace
            task = ' '.join(task.split())
            normalized.append(task)
        return normalized
    
    def _normalize_title(self, title: str, prefix_chars: int) -> str:
        """
        Normalize title to prefix for matching.
        
        Args:
            title: Document title
            prefix_chars: Number of characters to use
            
        Returns:
            Normalized prefix
        """
        # Lowercase, normalize whitespace
        normalized = ' '.join(title.lower().split())
        # Extract prefix
        return normalized[:prefix_chars]
    
    def export_results(self, filepath: Optional[str] = None) -> str:
        """
        Export evaluation results in specified format.
        
        Args:
            filepath: Optional file path to write results
            
        Returns:
            Formatted results string
        """
        if self.export_format == "markdown":
            output = self._export_markdown()
        elif self.export_format == "json":
            output = self._export_json()
        else:
            output = self._export_markdown()  # Default
        
        if filepath:
            with open(filepath, 'w') as f:
                f.write(output)
        
        return output
    
    def _export_markdown(self) -> str:
        """Export results as Markdown table"""
        output = "# ADRA-Bank Evaluation Results\n\n"
        
        if not self.results:
            output += "No evaluation results available.\n"
            return output
        
        # Planning results
        planning_results = [r for r in self.results if r.module == "planning"]
        if planning_results:
            output += "## Planning Module (π)\n\n"
            output += "| Metric | Value |\n"
            output += "|--------|-------|\n"
            for result in planning_results:
                for metric, value in result.metrics.items():
                    output += f"| {metric.capitalize()} | {value:.4f} |\n"
            output += "\n"
        
        # Retrieval results
        retrieval_results = [r for r in self.results if r.module == "retrieval"]
        if retrieval_results:
            output += "## Retrieval Module (ρ)\n\n"
            output += "| Metric | Value |\n"
            output += "|--------|-------|\n"
            for result in retrieval_results:
                for metric, value in result.metrics.items():
                    output += f"| {metric.capitalize()} | {value:.4f} |\n"
            output += "\n"
        
        # Reasoning results
        reasoning_results = [r for r in self.results if r.module == "reasoning"]
        if reasoning_results:
            output += "## Reasoning Module (σ)\n\n"
            output += "| Metric | Value |\n"
            output += "|--------|-------|\n"
            for result in reasoning_results:
                for metric, value in result.metrics.items():
                    output += f"| {metric.capitalize()} | {value:.4f} |\n"
            output += "\n"
        
        output += "---\n\n"
        output += "*Note: Metrics use Jaccard/IoU for Planning and Retrieval, "
        output += "F1-Score for Reasoning*\n"
        
        return output
    
    def _export_json(self) -> str:
        """Export results as JSON"""
        import json
        
        data = {
            "results": [
                {
                    "module": r.module,
                    "metrics": r.metrics,
                    "details": r.details
                }
                for r in self.results
            ]
        }
        
        return json.dumps(data, indent=2)
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics across all evaluations.
        
        Returns:
            Dictionary with summary metrics
        """
        if not self.results:
            return {}
        
        summary = {}
        
        for module in ["planning", "retrieval", "reasoning"]:
            module_results = [r for r in self.results if r.module == module]
            
            if module_results:
                # Average metrics across runs
                avg_metrics = {}
                metric_keys = module_results[0].metrics.keys()
                
                for key in metric_keys:
                    values = [r.metrics[key] for r in module_results]
                    avg_metrics[key] = sum(values) / len(values)
                
                summary[module] = avg_metrics
        
        return summary


# Export main classes and functions
__all__ = [
    'calculate_jaccard',
    'calculate_reasoning_f1',
    'ADRAEvaluator',
    'EvaluationResult',
]
