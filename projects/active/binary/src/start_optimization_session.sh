#!/bin/bash
# Auto-generated optimization session starter (location-agnostic)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

PROMPT_FILE="../docs/OPTIMIZATION_PROMPT.md"

echo "🤖 Starting Meta-Agent Optimization Session"
echo "============================================"
echo ""
echo "📋 Optimization prompt: $PROMPT_FILE"
echo "📊 Analysis complete - 2 opportunities identified"
echo ""
echo "Next steps:"
echo "1. Review $PROMPT_FILE"
echo "2. Use Claude Code to implement optimizations"
echo "3. Run './meta_agent.sh analyze' to measure improvements"
echo ""

# Open the prompt file
if command -v code &> /dev/null; then
    code "$PROMPT_FILE"
elif command -v open &> /dev/null; then
    open "$PROMPT_FILE"
else
    echo "📝 Please open $PROMPT_FILE in your editor"
fi
