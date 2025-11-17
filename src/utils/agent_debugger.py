"""
AGENT DEBUGGING SUITE
=====================

TEACHING PURPOSE:
-----------------
This module provides debugging tools for understanding agent decision-making.

When agents make autonomous decisions, we need visibility into:
  • WHY did the agent make this choice?
  • WHAT information influenced the decision?
  • HOW did the agent's state change?
  • WHEN did the decision occur?

KEY CONCEPTS:
-------------
  • Decision logging and replay
  • State inspection and visualization
  • Performance profiling
  • Decision tree reconstruction

USE CASES:
----------
  • Debugging unexpected agent behavior
  • Optimizing agent strategies
  • Auditing agent decisions for compliance
  • Teaching how agents reason
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from pathlib import Path


class AgentDebugger:
    """
    Debugging suite for agent decision-making.

    Captures and analyzes agent decisions for:
      • Transparency
      • Optimization
      • Auditing
      • Learning
    """

    def __init__(self, agent_name: str, log_file: Optional[Path] = None):
        """
        Initialize debugger for an agent.

        Args:
            agent_name: Name of the agent being debugged
            log_file: Optional path to save debug logs
        """
        self.agent_name = agent_name
        self.log_file = log_file
        self.decision_history: List[Dict] = []
        self.state_snapshots: List[Dict] = []

    def log_decision(
        self,
        decision_type: str,
        inputs: Dict[str, Any],
        output: Any,
        reasoning: str,
        metadata: Optional[Dict] = None
    ):
        """
        Log an agent decision for analysis.

        Args:
            decision_type: Type of decision (e.g., "crawl", "summarize")
            inputs: Input data that influenced the decision
            output: Decision output
            reasoning: Explanation of why this decision was made
            metadata: Additional contextual information

        Example:
            >>> debugger = AgentDebugger("ScraperAgent")
            >>> debugger.log_decision(
            ...     decision_type="url_relevance",
            ...     inputs={"url": "https://example.com", "keywords": ["AI"]},
            ...     output=0.75,
            ...     reasoning="URL contains 2/3 keywords, domain is .edu"
            ... )
        """
        decision = {
            'timestamp': datetime.now().isoformat(),
            'decision_type': decision_type,
            'inputs': inputs,
            'output': output,
            'reasoning': reasoning,
            'metadata': metadata or {}
        }

        self.decision_history.append(decision)

        if self.log_file:
            self._persist_decision(decision)

    def snapshot_state(self, state: Dict[str, Any], label: str = ""):
        """
        Capture agent state at a point in time.

        Args:
            state: Agent's current state
            label: Optional description of this snapshot
        """
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'label': label,
            'state': state
        }

        self.state_snapshots.append(snapshot)

    def get_decision_summary(self) -> Dict:
        """
        Get summary statistics of agent decisions.

        Returns:
            Dict with decision counts, types, success rates
        """
        if not self.decision_history:
            return {'total_decisions': 0}

        decision_types = {}
        for decision in self.decision_history:
            dtype = decision['decision_type']
            decision_types[dtype] = decision_types.get(dtype, 0) + 1

        return {
            'total_decisions': len(self.decision_history),
            'decision_types': decision_types,
            'first_decision': self.decision_history[0]['timestamp'],
            'last_decision': self.decision_history[-1]['timestamp']
        }

    def replay_decisions(self, decision_type: Optional[str] = None) -> List[Dict]:
        """
        Replay recorded decisions for analysis.

        Args:
            decision_type: Filter by specific decision type

        Returns:
            List of decision records
        """
        if decision_type:
            return [d for d in self.decision_history
                   if d['decision_type'] == decision_type]
        return self.decision_history

    def generate_debug_report(self) -> str:
        """
        Generate human-readable debug report.

        Returns:
            Markdown-formatted debug report
        """
        report = [f"# Agent Debug Report: {self.agent_name}\n"]
        report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        summary = self.get_decision_summary()
        report.append(f"\n## Decision Summary\n")
        report.append(f"- Total Decisions: {summary.get('total_decisions', 0)}\n")

        if 'decision_types' in summary:
            report.append(f"\n### Decision Types\n")
            for dtype, count in summary['decision_types'].items():
                report.append(f"- {dtype}: {count}\n")

        report.append(f"\n## Recent Decisions\n")
        for decision in self.decision_history[-10:]:
            report.append(f"\n### {decision['decision_type']} @ {decision['timestamp']}\n")
            report.append(f"**Reasoning**: {decision['reasoning']}\n")
            report.append(f"**Output**: {decision['output']}\n")

        return ''.join(report)

    def _persist_decision(self, decision: Dict):
        """Save decision to log file."""
        if self.log_file:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(decision) + '\n')


# Decorator for automatic decision logging
def log_agent_decision(decision_type: str):
    """
    Decorator to automatically log agent decisions.

    Example:
        >>> class MyAgent:
        >>>     def __init__(self):
        >>>         self.debugger = AgentDebugger("MyAgent")
        >>>
        >>>     @log_agent_decision("url_assessment")
        >>>     def assess_url(self, url, keywords):
        >>>         score = self._calculate_score(url, keywords)
        >>>         return score
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)

            # Log if agent has debugger
            if hasattr(self, 'debugger'):
                self.debugger.log_decision(
                    decision_type=decision_type,
                    inputs={'args': args, 'kwargs': kwargs},
                    output=result,
                    reasoning=f"Decision made by {func.__name__}"
                )

            return result
        return wrapper
    return decorator
