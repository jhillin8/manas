# Instagram Data Analyzer for Raycast

A powerful Raycast extension that analyzes Instagram accounts and generates comprehensive reports with demographics, engagement metrics, and actionable insights.

## Installation

### Prerequisites
- macOS with Raycast installed
- Node.js 16 or higher
- npm or yarn

### Setup Instructions

1. **Clone or download this extension**:
   ```bash
   cd /Users/josephhillin/manas/projects/active/instagram-analyzer
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Build the extension**:
   ```bash
   npm run build
   ```

4. **Import to Raycast**:
   ```bash
   npm run dev
   ```
   This will open the extension in Raycast development mode.

5. **For permanent installation**:
   - In Raycast, go to Extensions
   - Click "+" and select "Add Script Directory"
   - Navigate to `/Users/josephhillin/manas/projects/active/instagram-analyzer`
   - Click "Import Extension"

## Usage Instructions

### Quick Start

1. **Open Raycast** (⌘ + Space by default)
2. **Type**: "Analyze Instagram Account"
3. **Press Enter** to open the analyzer

### Analysis Options

#### 1. Account Input
- Enter the Instagram username (without @)
- Example: `brooksnader` or `nike`

#### 2. Timeframe Selection
- **Last 7 Days**: Quick recent activity analysis
- **Last 30 Days**: Standard monthly overview
- **Last 90 Days**: Quarterly trends
- **Last Year**: Annual comprehensive analysis

#### 3. Analysis Depth
- **Quick Analysis**: Basic metrics and top insights (30 seconds)
- **Standard Analysis**: Full demographics and engagement patterns (1-2 minutes)
- **Deep Dive**: Complete analysis with psychographics and predictions (3-5 minutes)

#### 4. Additional Options
- **Include Visual Analytics**: Generate charts and graphs
- **Output Format**: 
  - Markdown Report (readable format)
  - JSON Data (for further processing)
  - Both Formats

### Keyboard Shortcuts

- `⌘ + Enter`: Start analysis
- `⌘ + K`: View previous analyses
- `⌘ + C`: Copy report to clipboard
- `⌘ + S`: Save report to file
- `⌘ + N`: New analysis

### Features

#### Real-time Analysis
- Follower count and growth
- Engagement rate calculation
- Post frequency and timing
- Content type performance

#### Demographics
- Age group distribution
- Gender split analysis
- Geographic locations
- Language preferences

#### Insights & Recommendations
- Peak activity times
- Best performing content types
- Audience behavior patterns
- Growth opportunities
- Strategic recommendations

### Viewing Results

After analysis completes:
1. **Summary View**: Quick overview of key metrics
2. **Detailed Report**: Full markdown report with all insights
3. **Export Options**:
   - Copy to clipboard
   - Save to Desktop
   - Export as JSON

### Managing Previous Analyses

1. From the main form, click "View Previous Analyses" or press `⌘ + K`
2. Browse through past analyses sorted by date
3. Click any analysis to view full report
4. Copy or export historical reports

## Advanced Usage

### Batch Analysis
To analyze multiple accounts:
1. Run individual analyses
2. Use "Previous Analyses" to compare results
3. Export all reports for external processing

### Integration with Other Tools
The JSON export format allows integration with:
- Data visualization tools
- Spreadsheet applications
- Custom analysis scripts
- Marketing automation platforms

## Troubleshooting

### Common Issues

1. **"Analysis Failed" Error**
   - Check internet connection
   - Verify account exists and is public
   - Try again with a shorter timeframe

2. **Slow Performance**
   - Use "Quick Analysis" for faster results
   - Close other Raycast extensions
   - Restart Raycast if needed

3. **Missing Data**
   - Some metrics require public accounts
   - Historical data may be limited
   - Try "Standard" or "Deep Dive" analysis

### Data Storage
- Analyses are stored locally in Raycast
- No data is sent to external servers
- Clear storage in Raycast preferences if needed

## Tips for Best Results

1. **Optimal Analysis Times**
   - Run analyses during off-peak hours
   - Allow 2-3 minutes for deep analysis
   - Use quick analysis for real-time checks

2. **Comparing Accounts**
   - Analyze competitors sequentially
   - Export reports for side-by-side comparison
   - Focus on relative metrics

3. **Tracking Growth**
   - Run weekly analyses for trend tracking
   - Compare month-over-month changes
   - Document significant events

## Privacy & Limitations

- Only analyzes publicly available data
- Respects Instagram's terms of service
- No login or authentication required
- Data is stored locally only

## Support

For issues or feature requests:
- Check Raycast forums
- Submit issues on GitHub
- Contact extension author

## Future Enhancements

Planned features:
- Real Instagram API integration
- Competitor comparison mode
- Automated scheduled analyses
- Custom report templates
- Export to Google Sheets
- Trend predictions
- Hashtag analysis

---

**Note**: This extension currently uses simulated data for demonstration. Full API integration coming soon. 