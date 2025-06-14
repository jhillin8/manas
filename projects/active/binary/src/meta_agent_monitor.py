#!/usr/bin/env python3
"""
Meta-Agent Monitor - Continuous optimization daemon
Runs every 5 minutes, analyzes project state, triggers optimizations
"""

import time
import json
import subprocess
from datetime import datetime
from meta_agent_config import MetaAgentConfig, ProjectAnalyzer, META_AGENT_PROMPTS

class MetaAgentMonitor:
    def __init__(self):
        self.config = MetaAgentConfig()
        self.analyzer = ProjectAnalyzer(self.config.project_root)
        self.state = self.config.load_state()
        
    def monitor_file_changes(self):
        """Monitor for file changes and trigger analysis"""
        current_hashes = {}
        changes_detected = False
        
        for file in self.config.monitored_files:
            filepath = self.config.project_root / file
            if filepath.exists():
                current_hash = self.config.calculate_file_hash(filepath)
                current_hashes[file] = current_hash
                
                # Check if file changed
                if file in self.state["file_hashes"]:
                    if self.state["file_hashes"][file] != current_hash:
                        changes_detected = True
                        print(f"📝 Change detected in {file}")
                else:
                    changes_detected = True
                    print(f"🆕 New file detected: {file}")
        
        self.state["file_hashes"] = current_hashes
        return changes_detected
    
    def run_analysis(self):
        """Run comprehensive project analysis"""
        print("⚡ Running Meta-Agent analysis...")
        
        # Get current metrics
        task_metrics = self.analyzer.analyze_task_completion_rate()
        drift_metrics = self.analyzer.detect_execution_drift()
        opportunities = self.analyzer.identify_optimization_opportunities()
        
        analysis_result = {
            "timestamp": str(datetime.now()),
            "task_metrics": task_metrics,
            "drift_metrics": drift_metrics,
            "opportunities": opportunities
        }
        
        # Store in state
        self.state["performance_metrics"] = analysis_result
        
        return analysis_result
    
    def generate_optimization_directives(self, analysis):
        """Generate optimization directives using Claude via prompt"""
        if not analysis["opportunities"]:
            return {"status": "NO_OPTIMIZATIONS_NEEDED"}
            
        # Format opportunities for prompt
        opportunities_text = "\n".join([
            f"- {opp['type']} (Priority: {opp['priority']}): {opp['description']}"
            for opp in analysis["opportunities"]
        ])
        
        # Create optimization prompt
        prompt = META_AGENT_PROMPTS["optimization_analysis"].format(
            completion_rate=analysis["task_metrics"]["completion_rate"],
            velocity=analysis["task_metrics"]["velocity"],
            drift_score=analysis["drift_metrics"]["drift_score"],
            opportunities=opportunities_text
        )
        
        # Write prompt to file for manual execution
        prompt_file = self.config.project_root / "meta_agent_prompt.md"
        with open(prompt_file, 'w') as f:
            f.write(f"# Meta-Agent Optimization Analysis\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(prompt)
        
        return {
            "status": "PROMPT_GENERATED",
            "prompt_file": str(prompt_file),
            "analysis": analysis
        }
    
    def check_optimization_triggers(self, analysis):
        """Check if optimization should be triggered"""
        triggers = []
        
        # Task completion trigger
        if analysis["task_metrics"]["completion_rate"] < self.config.optimization_triggers["task_completion_threshold"]:
            triggers.append("LOW_COMPLETION_RATE")
        
        # Drift trigger  
        if analysis["drift_metrics"]["drift_score"] > self.config.optimization_triggers["execution_drift_score"]:
            triggers.append("EXECUTION_DRIFT")
        
        # Velocity trigger
        if analysis["task_metrics"]["velocity"] < 0.2:
            triggers.append("LOW_VELOCITY")
        
        return triggers
    
    def run_monitoring_cycle(self):
        """Single monitoring cycle"""
        print(f"\n🔍 Meta-Agent Monitor - {datetime.now().strftime('%H:%M:%S')}")
        
        # Check for file changes
        changes = self.monitor_file_changes()
        
        # Always run analysis (every cycle)
        analysis = self.run_analysis()
        
        # Check optimization triggers
        triggers = self.check_optimization_triggers(analysis)
        
        if triggers:
            print(f"⚠️  Optimization triggers activated: {', '.join(triggers)}")
            optimization_result = self.generate_optimization_directives(analysis)
            
            # Log optimization
            self.state["optimization_history"].append({
                "timestamp": str(datetime.now()),
                "triggers": triggers,
                "result": optimization_result
            })
            
            print(f"📋 Optimization prompt generated: {optimization_result.get('prompt_file', 'N/A')}")
        else:
            print("✅ Project performance within acceptable parameters")
        
        # Update state
        self.state["last_optimization"] = str(datetime.now())
        self.config.save_state(self.state)
        
        # Print summary
        print(f"📊 Tasks: {analysis['task_metrics']['completed']}/{analysis['task_metrics']['total']} completed")
        print(f"⚡ Velocity: {analysis['task_metrics']['velocity']:.1%}")
        print(f"🎯 Focus Score: {1/analysis['drift_metrics']['drift_score']:.2f}")
    
    def run_daemon(self):
        """Run continuous monitoring daemon"""
        print("🚀 Meta-Agent Monitor starting...")
        print(f"📂 Monitoring: {self.config.project_root}")
        print(f"⏱️  Interval: {self.config.monitoring_interval} seconds")
        
        try:
            while True:
                self.run_monitoring_cycle()
                print(f"😴 Sleeping for {self.config.monitoring_interval//60} minutes...\n")
                time.sleep(self.config.monitoring_interval)
        except KeyboardInterrupt:
            print("\n⛔ Meta-Agent Monitor stopped by user")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            raise

if __name__ == "__main__":
    monitor = MetaAgentMonitor()
    
    # Run single cycle or daemon based on args
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        monitor.run_monitoring_cycle()
    else:
        monitor.run_daemon()
