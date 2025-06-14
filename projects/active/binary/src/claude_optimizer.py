#!/usr/bin/env python3
"""
Meta-Agent Claude Integration
Handles AI-driven optimization via Claude Code integration
"""

import json
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from meta_agent_config import MetaAgentConfig, ProjectAnalyzer

class ClaudeOptimizer:
    def __init__(self):
        self.config = MetaAgentConfig()
        self.analyzer = ProjectAnalyzer(self.config.project_root)
    
    def generate_claude_optimization_prompt(self, analysis):
        """Generate a comprehensive optimization prompt for Claude"""
        
        # Read current project files for context
        context_files = {}
        for file in self.config.monitored_files:
            filepath = self.config.project_root / file
            if filepath.exists():
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        context_files[file] = f.read()[:2000]  # First 2000 chars
                except:
                    context_files[file] = "[Unable to read file]"
        
        # Build comprehensive prompt
        prompt = f"""# Meta-Agent Optimization Request

**Project:** Brooks Nader Monetization System
**Analysis Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Objective:** Optimize execution to maximize revenue generation velocity

## Current Performance Metrics
- **Task Completion Rate:** {analysis['task_metrics']['completion_rate']:.1%}
- **Execution Velocity:** {analysis['task_metrics']['velocity']:.1%} 
- **Research/Monetization Focus Ratio:** {analysis['drift_metrics']['drift_score']:.2f}
- **Total Tasks:** {analysis['task_metrics']['total']} ({analysis['task_metrics']['completed']} completed, {analysis['task_metrics']['in_progress']} in progress)

## Identified Optimization Opportunities
"""
        
        for i, opp in enumerate(analysis['opportunities'], 1):
            prompt += f"""
### {i}. {opp['type']} (Priority: {opp['priority']})
**Issue:** {opp['description']}
**Suggested Action:** {opp['action']}
"""
        
        prompt += f"""

## Project Context Files
"""
        
        for filename, content in context_files.items():
            prompt += f"""
### {filename}
```
{content}
{'...' if len(content) >= 2000 else ''}
```
"""
        
        prompt += f"""

## Optimization Request

As the Meta-Agent optimizer, provide specific actionable directives to:

1. **Increase Revenue Velocity** - What specific tasks should be prioritized/deprioritized?
2. **Reduce Analysis Paralysis** - Which research tasks can be consolidated or eliminated?
3. **Improve Execution Flow** - What process improvements will accelerate completion?

For each directive, provide:
- **ACTION:** Specific task/change
- **RATIONALE:** Why this will improve revenue generation
- **IMPLEMENTATION:** Exact steps to execute
- **IMPACT:** Expected improvement metric

Focus ruthlessly on revenue generation. The goal is $8K+ monthly recurring revenue.

**Current bottlenecks to address:**
{self._identify_bottlenecks(analysis)}

**Expected outcome:** Clear optimization plan that increases task completion velocity by 40%+ within 1 week.
"""
        
        return prompt
    
    def _identify_bottlenecks(self, analysis):
        """Identify specific bottlenecks from analysis"""
        bottlenecks = []
        
        if analysis['task_metrics']['completion_rate'] < 0.3:
            bottlenecks.append("- Low task completion suggests execution blockers or unclear task definitions")
        
        if analysis['drift_metrics']['drift_score'] > 2.0:
            bottlenecks.append("- High research-to-monetization ratio indicates over-analysis")
        
        if analysis['task_metrics']['velocity'] < 0.2:
            bottlenecks.append("- Low in-progress task ratio suggests poor task flow management")
        
        if not bottlenecks:
            bottlenecks.append("- No major bottlenecks detected, focus on velocity optimization")
        
        return "\n".join(bottlenecks)
    
    def create_optimization_session(self):
        """Create a Claude Code session with optimization context"""
        
        # Run analysis
        analysis = self.analyzer.analyze_task_completion_rate()
        drift_analysis = self.analyzer.detect_execution_drift()
        opportunities = self.analyzer.identify_optimization_opportunities()
        
        full_analysis = {
            "task_metrics": analysis,
            "drift_metrics": drift_analysis, 
            "opportunities": opportunities
        }
        
        # Generate optimization prompt
        optimization_prompt = self.generate_claude_optimization_prompt(full_analysis)
        
        # Save to file
        prompt_file = self.config.project_root / "OPTIMIZATION_PROMPT.md"
        with open(prompt_file, 'w') as f:
            f.write(optimization_prompt)
        
        # Create optimization session script
        session_script = self.config.project_root / "start_optimization_session.sh"
        with open(session_script, 'w') as f:
            f.write(f"""#!/bin/bash
# Auto-generated optimization session starter

cd "{self.config.project_root}"

echo "🤖 Starting Meta-Agent Optimization Session"
echo "============================================"
echo ""
echo "📋 Optimization prompt: OPTIMIZATION_PROMPT.md"
echo "📊 Analysis complete - {len(opportunities)} opportunities identified"
echo ""
echo "Next steps:"
echo "1. Review OPTIMIZATION_PROMPT.md"
echo "2. Use Claude Code to implement optimizations"
echo "3. Run './meta_agent.sh analyze' to measure improvements"
echo ""

# Open the prompt file
if command -v code &> /dev/null; then
    code OPTIMIZATION_PROMPT.md
elif command -v open &> /dev/null; then
    open OPTIMIZATION_PROMPT.md
else
    echo "📝 Please open OPTIMIZATION_PROMPT.md in your editor"
fi
""")
        
        # Make executable
        subprocess.run(['chmod', '+x', str(session_script)])
        
        return {
            "prompt_file": str(prompt_file),
            "session_script": str(session_script),
            "analysis": full_analysis,
            "optimization_count": len(opportunities)
        }
    
    def apply_optimization_directive(self, directive):
        """Apply a specific optimization directive to the project"""
        
        # This would integrate with your project files to make actual changes
        # For now, it logs the directive for manual implementation
        
        log_entry = {
            "timestamp": str(datetime.now()),
            "directive": directive,
            "status": "LOGGED_FOR_IMPLEMENTATION"
        }
        
        # Append to optimization log
        log_file = self.config.project_root / "optimization_log.json"
        
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        return log_entry

class OptimizationAutomator:
    """Handles automatic optimization implementation"""
    
    def __init__(self):
        self.config = MetaAgentConfig()
    
    def auto_consolidate_research_tasks(self):
        """Automatically consolidate redundant research tasks"""
        
        # Read PROJECT_ARCHITECTURE.md
        arch_file = self.config.project_root / "PROJECT_ARCHITECTURE.md"
        content = arch_file.read_text()
        
        # Find research tasks that can be consolidated
        research_lines = [line for line in content.split('\n') if 'research' in line.lower() and '[PENDING]' in line]
        
        if len(research_lines) > 5:  # If more than 5 pending research tasks
            consolidation_note = f"""
## AUTO-OPTIMIZATION APPLIED: Research Consolidation
**Applied:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Rationale:** {len(research_lines)} pending research tasks detected - consolidating to prevent analysis paralysis

**Recommended Consolidation:**
- Merge similar research tasks into single comprehensive analyses
- Focus on revenue-impacting research only
- Defer non-critical research until after MVP launch

"""
            
            # Append to architecture file
            with open(arch_file, 'a') as f:
                f.write(consolidation_note)
            
            return {"action": "RESEARCH_CONSOLIDATED", "tasks_affected": len(research_lines)}
        
        return {"action": "NO_CONSOLIDATION_NEEDED"}

if __name__ == "__main__":
    optimizer = ClaudeOptimizer()
    result = optimizer.create_optimization_session()
    
    print(f"🤖 Meta-Agent Optimization Session Created")
    print(f"📋 Prompt: {result['prompt_file']}")
    print(f"🚀 Session: {result['session_script']}")
    print(f"📊 Opportunities: {result['optimization_count']}")
    print(f"")
    print(f"Run: {result['session_script']}")
