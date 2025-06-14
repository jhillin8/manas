#!/usr/bin/env python3
"""
Meta-Agent Configuration & Orchestrator
Monitors and optimizes the Brooks Nader monetization project
"""

import json
import time
import os
from datetime import datetime, timedelta
from pathlib import Path
import hashlib

class MetaAgentConfig:
    def __init__(self, project_root="/Users/josephhillin/manas/projects/active/binary"):
        self.project_root = Path(project_root)
        self.config_file = self.project_root / "meta_agent_state.json"
        self.monitored_files = [
            "PROJECT_ARCHITECTURE.md",
            "CLAUDE.md", 
            "DATA_COLLECTION_INSIGHTS.md",
            "PHASE_A_IDEARECORD.md",
            "BINARY_EXECUTION_LOG.md"
        ]
        self.monitoring_interval = 300  # 5 minutes
        self.optimization_triggers = {
            "task_completion_threshold": 0.7,  # When 70% of tasks in a phase complete
            "data_collection_stagnation": 24,  # Hours without progress
            "research_depth_overflow": 50,     # Too many sub-tasks spawned
            "execution_drift_score": 0.3       # When execution diverges from objectives
        }
        
    def load_state(self):
        """Load previous monitoring state"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            "last_optimization": None,
            "file_hashes": {},
            "performance_metrics": {},
            "optimization_history": []
        }
    
    def save_state(self, state):
        """Save current monitoring state"""
        with open(self.config_file, 'w') as f:
            json.dump(state, f, indent=2, default=str)

    def calculate_file_hash(self, filepath):
        """Calculate MD5 hash of file for change detection"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None

class ProjectAnalyzer:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
    
    def analyze_task_completion_rate(self):
        """Analyze completion rates across project phases"""
        architecture_file = self.project_root / "PROJECT_ARCHITECTURE.md"
        if not architecture_file.exists():
            return {"error": "PROJECT_ARCHITECTURE.md not found"}
        
        content = architecture_file.read_text()
        
        # Parse completed vs pending tasks
        completed_tasks = content.count("[COMPLETED]")
        in_progress_tasks = content.count("[IN PROGRESS]") 
        pending_tasks = content.count("[PENDING]")
        
        total_tasks = completed_tasks + in_progress_tasks + pending_tasks
        
        return {
            "completed": completed_tasks,
            "in_progress": in_progress_tasks, 
            "pending": pending_tasks,
            "total": total_tasks,
            "completion_rate": completed_tasks / total_tasks if total_tasks > 0 else 0,
            "velocity": in_progress_tasks / total_tasks if total_tasks > 0 else 0
        }
    
    def detect_execution_drift(self):
        """Detect if execution is drifting from core objectives"""
        # Analyze if current tasks align with monetization goals
        architecture_file = self.project_root / "PROJECT_ARCHITECTURE.md"
        content = architecture_file.read_text()
        
        # Key monetization indicators
        monetization_keywords = [
            "revenue", "subscription", "monetization", "pricing", 
            "conversion", "payment", "customer", "acquisition"
        ]
        
        # Research depth indicators (potential over-analysis)
        research_keywords = [
            "analyze", "research", "study", "investigate", "examine"
        ]
        
        monetization_density = sum(content.lower().count(kw) for kw in monetization_keywords)
        research_density = sum(content.lower().count(kw) for kw in research_keywords)
        
        drift_score = research_density / (monetization_density + 1)  # Higher = more drift
        
        return {
            "drift_score": drift_score,
            "monetization_focus": monetization_density,
            "research_intensity": research_density,
            "recommendation": "REFOCUS" if drift_score > 3.0 else "CONTINUE"
        }
    
    def identify_optimization_opportunities(self):
        """Identify specific areas for optimization"""
        task_analysis = self.analyze_task_completion_rate()
        drift_analysis = self.detect_execution_drift()
        
        opportunities = []
        
        # Task completion opportunities
        if task_analysis["completion_rate"] < 0.3:
            opportunities.append({
                "type": "EXECUTION_BOTTLENECK",
                "priority": "HIGH",
                "description": "Low task completion rate suggests execution bottlenecks",
                "action": "Identify and remove blockers, simplify tasks"
            })
        
        # Research depth opportunities  
        if drift_analysis["drift_score"] > 2.0:
            opportunities.append({
                "type": "RESEARCH_OPTIMIZATION",
                "priority": "MEDIUM", 
                "description": "High research-to-monetization ratio",
                "action": "Consolidate research, focus on revenue-driving activities"
            })
        
        # Velocity opportunities
        if task_analysis["velocity"] < 0.2:
            opportunities.append({
                "type": "VELOCITY_IMPROVEMENT",
                "priority": "HIGH",
                "description": "Low task velocity indicates process inefficiencies",
                "action": "Parallelize tasks, automate data collection"
            })
        
        return opportunities

# Meta-Agent Prompt Templates
META_AGENT_PROMPTS = {
    "optimization_analysis": """
    You are the Meta-Agent for the Brooks Nader monetization project. 
    
    Current Project State:
    - Task Completion: {completion_rate:.1%}
    - Execution Velocity: {velocity:.1%} 
    - Drift Score: {drift_score:.2f}
    
    Optimization Opportunities:
    {opportunities}
    
    Your mission: Generate 3 specific, actionable optimization directives that will:
    1. Increase revenue-generating task completion rate
    2. Reduce research overhead without losing strategic insight
    3. Improve execution velocity
    
    Format as:
    DIRECTIVE 1: [Action] 
    DIRECTIVE 2: [Action]
    DIRECTIVE 3: [Action]
    """,
    
    "strategic_pivot_detection": """
    Analyze the current project execution against the original monetization objectives.
    
    Original Target: $8K+ monthly recurring revenue via subscription model
    Current Execution Focus: {current_focus}
    
    Determine if a strategic pivot is needed. If yes, provide:
    1. What to STOP doing
    2. What to START doing  
    3. What to CONTINUE doing
    
    Be ruthlessly focused on revenue generation.
    """
}

if __name__ == "__main__":
    print("Meta-Agent Configuration Complete")
    print("Run 'python meta_agent_monitor.py' to start monitoring")
