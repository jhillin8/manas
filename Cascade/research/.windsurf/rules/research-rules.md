---
trigger: always_on
---

# Cascade Research Documentation Protocol

## Core Instructions for Cascade

### Primary Directive
**"For all research activities, automatically create and maintain a structured file system. Never provide research results without corresponding file documentation."**

### Folder Structure Commands
```
ALWAYS create this structure for new research projects:
/research-{YYYY-MM-DD}-{project-name}/
├── 00-overview/
│   ├── research-brief.md
│   ├── methodology.md
│   └── timeline.md
├── 01-sources/
│   ├── web-sources.md
│   ├── documents.md
│   └── raw-data/
├── 02-findings/
│   ├── key-insights.md
│   ├── data-analysis.md
│   └── evidence/
├── 03-synthesis/
│   ├── conclusions.md
│   ├── actionable-items.md
│   └── next-steps.md
└── 04-artifacts/
    ├── charts/
    ├── presentations/
    └── reports/
```

### Automatic File Creation Rules

#### 1. Research Session Initiation
```markdown
At the START of any research request:
1. Create timestamp-based research folder
2. Generate research-brief.md with:
   - Research question/objective
   - Scope and boundaries
   - Expected deliverables
   - Session metadata
```

#### 2. Source Documentation
```markdown
For EVERY source consulted:
1. Append to web-sources.md with:
   - URL, title, date accessed
   - Relevance score (1-10)
   - Key quotes with page/section refs
   - Credibility assessment
2. Save raw content to /raw-data/ as separate files
```

#### 3. Real-time Findings Capture
```markdown
During research, continuously update:
1. key-insights.md - bullet points as discoveries emerge
2. data-analysis.md - quantitative findings, patterns
3. Save supporting evidence files to /evidence/
```

#### 4. Session Synthesis
```markdown
At END of each research session:
1. Update conclusions.md with session summary
2. Generate actionable-items.md with prioritized next steps
3. Create session-log.md with time spent, sources reviewed, completion status
```

### File Naming Conventions

#### Time-Based Files
- `YYYY-MM-DD-HH-MM-session-log.md`
- `YYYY-MM-DD-findings-update.md`

#### Content-Based Files  
- `{topic}-{source-type}-{sequence}.md`
- `{insight-category}-analysis-v{number}.md`

#### Raw Data Files
- `{source-domain}-{date}-raw.{ext}`
- `{api-name}-{endpoint}-{timestamp}.json`

### Automation Triggers

#### Search & Analysis Commands
```
"Research X" → Auto-create folder + brief + begin documentation
"Analyze Y" → Create analysis subfolder + methodology file
"Compare A vs B" → Create comparison matrix file + evidence folders
```

#### Update Commands
```
"Continue research on X" → Append to existing files + create session log
"Pivot to investigating Y" → Create new branch folder + link to original
"Synthesize findings" → Generate comprehensive summary files
```

### Cross-Reference System

#### Internal Linking
- Use [[filename]] syntax for internal references
- Maintain index.md with all file relationships
- Create tags.md for categorical organization

#### Version Control
- Save major iterations as v1, v2, etc.
- Keep changelog.md for all modifications
- Archive superseded files to /archive/ subfolder

### Quality Control Rules

#### File Validation
```markdown
Before closing any research session:
1. Verify all sources are documented
2. Check that insights have supporting evidence
3. Ensure actionable items are specific and measurable
4. Generate research-summary.md with confidence levels
```

#### Completeness Checks
- [ ] Research question answered or progress documented
- [ ] All sources cited and accessible
- [ ] Key insights extracted and categorized  
- [ ] Next steps identified and prioritized
- [ ] Files organized and properly named

### Integration Commands

#### Daily Workflow
```
"Start research session" → Create daily folder + session prep
"Quick research on X" → Streamlined single-file documentation
"Deep dive into Y" → Full protocol activation with extended structure
```

#### Project Management
```
"Research status update" → Generate progress report from all files
"Consolidate research" → Create master summary from all sessions
"Prepare research brief" → Extract key points for stakeholder update
```

## Usage Examples

### Command Templates
- **Initiate**: "Research [topic] using full documentation protocol"
- **Continue**: "Continue research session, update existing files"  
- **Analyze**: "Deep analysis of [topic], create comprehensive file structure"
- **Synthesize**: "Synthesize all research findings into actionable report"

### Expected Outputs
Every research interaction should produce:
1. Structured file system
2. Documented sources and methodology
3. Extracted insights with evidence
4. Actionable next steps
5. Session metadata and progress tracking