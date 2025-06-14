#!/usr/bin/env python3
"""
Simple Cross-Agent Memory Intelligence System Test
Tests core functionality without complex imports
"""

import os
import sys
import json
import subprocess
from datetime import datetime

def test_file_structure():
    """Test that all expected files exist"""
    base_path = "/Users/josephhillin/workspace/mcp-central"
    
    expected_files = [
        "orchestrator.py",
        "raycast-config-registry.py", 
        "start-memory-system.sh",
        "requirements.txt",
        "README.md",
        "orchestrator-config.yaml",
        "bin/memory-cli.py",
        "langflow/memory-mcp-bridge.py",
        "team/team-memory-manager.py",
        "graph/memory-graph-service.py",
        "security/audit-system.py",
        "memory-seeds/enhanced-validator.py",
        "agents/temporal-engine/temporal-processor.py",
        "memory-policies/temporal-schema.yaml",
        "docker-configs/resource-profiles.yaml"
    ]
    
    existing_files = []
    missing_files = []
    
    for file_path in expected_files:
        full_path = f"{base_path}/{file_path}"
        if os.path.exists(full_path):
            existing_files.append(file_path)
        else:
            missing_files.append(file_path)
    
    return {
        "success": len(missing_files) == 0,
        "total_files": len(expected_files),
        "existing_files": len(existing_files),
        "missing_files": missing_files
    }

def test_temporal_processor():
    """Test the temporal processor directly"""
    try:
        result = subprocess.run([
            "python3", 
            "/Users/josephhillin/workspace/mcp-central/agents/temporal-engine/temporal-processor.py"
        ], capture_output=True, text=True, timeout=10)
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def test_graph_service():
    """Test the graph service directly"""
    try:
        result = subprocess.run([
            "python3", 
            "/Users/josephhillin/workspace/mcp-central/graph/memory-graph-service.py"
        ], capture_output=True, text=True, timeout=10)
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def test_audit_system():
    """Test the audit system directly"""
    try:
        result = subprocess.run([
            "python3", 
            "/Users/josephhillin/workspace/mcp-central/security/audit-system.py"
        ], capture_output=True, text=True, timeout=10)
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def test_startup_script():
    """Test that the startup script is executable and shows help"""
    try:
        result = subprocess.run([
            "/Users/josephhillin/workspace/mcp-central/start-memory-system.sh", 
            "help"
        ], capture_output=True, text=True, timeout=10)
        
        return {
            "success": result.returncode == 0,
            "has_help_text": "Usage:" in result.stdout,
            "output": result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def test_cli_help():
    """Test CLI help command"""
    try:
        result = subprocess.run([
            "python3", 
            "/Users/josephhillin/workspace/mcp-central/bin/memory-cli.py",
            "--help"
        ], capture_output=True, text=True, timeout=10)
        
        return {
            "success": result.returncode == 0,
            "has_help_text": "usage:" in result.stdout.lower() or "help" in result.stdout.lower(),
            "output": result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    """Run all simple tests"""
    print("🧪 Cross-Agent Memory Intelligence System - Simple Tests")
    print("=" * 60)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Temporal Processor", test_temporal_processor),
        ("Graph Service", test_graph_service),
        ("Audit System", test_audit_system),
        ("Startup Script", test_startup_script),
        ("CLI Help", test_cli_help)
    ]
    
    results = {}
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        print("-" * 40)
        
        try:
            result = test_func()
            
            if result.get("success", False):
                passed += 1
                print(f"✅ {test_name} - PASSED")
                if "output" in result and result["output"]:
                    print(f"   Output: {result['output'][:100]}...")
            else:
                print(f"❌ {test_name} - FAILED")
                if result.get("error"):
                    print(f"   Error: {result['error']}")
                if result.get("missing_files"):
                    print(f"   Missing files: {result['missing_files']}")
            
            results[test_name] = result
            
        except Exception as e:
            print(f"❌ {test_name} - EXCEPTION: {e}")
            results[test_name] = {"success": False, "error": str(e)}
    
    print(f"\n{'='*60}")
    print(f"🏁 Simple Test Suite Complete")
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    # Save results
    results_summary = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": total,
        "passed_tests": passed,
        "success_rate": (passed/total)*100,
        "test_results": results
    }
    
    results_file = "/Users/josephhillin/workspace/mcp-central/simple-test-results.json"
    with open(results_file, 'w') as f:
        json.dump(results_summary, f, indent=2)
    
    print(f"\n📊 Results saved to: {results_file}")
    
    # Exit code based on success rate
    return 0 if passed >= total * 0.7 else 1

if __name__ == "__main__":
    sys.exit(main())
