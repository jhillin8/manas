import {
  ActionPanel,
  Action,
  Form,
  showToast,
  Toast,
  List,
  Detail,
  useNavigation,
  LocalStorage,
  Icon,
  Color,
} from "@raycast/api";
import { useState, useEffect } from "react";
import { useForm, FormValidation } from "@raycast/utils";

interface AnalysisConfig {
  account: string;
  timeframe: string;
  depth: string;
  includeVisuals: boolean;
  outputFormat: string;
}

interface AnalysisResult {
  account: string;
  timestamp: string;
  metrics: {
    followers: number;
    engagement: number;
    posts: number;
  };
  demographics: {
    ageGroups: Record<string, number>;
    genderSplit: Record<string, number>;
    topLocations: string[];
  };
  insights: string[];
  recommendations: string[];
}

export default function AnalyzeCommand() {
  const { push } = useNavigation();
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const { handleSubmit, itemProps } = useForm<AnalysisConfig>({
    onSubmit: async (values) => {
      setIsAnalyzing(true);
      const toast = await showToast({
        style: Toast.Style.Animated,
        title: "Analyzing Instagram Account",
        message: `Processing @${values.account}...`,
      });

      try {
        // Simulate analysis process
        const result = await performAnalysis(values);
        
        // Save to local storage
        await LocalStorage.setItem(
          `analysis-${values.account}-${Date.now()}`,
          JSON.stringify(result)
        );

        toast.style = Toast.Style.Success;
        toast.title = "Analysis Complete";
        toast.message = `Successfully analyzed @${values.account}`;

        // Navigate to results view
        push(<AnalysisResults result={result} config={values} />);
      } catch (error) {
        toast.style = Toast.Style.Failure;
        toast.title = "Analysis Failed";
        toast.message = error instanceof Error ? error.message : "Unknown error";
      } finally {
        setIsAnalyzing(false);
      }
    },
    validation: {
      account: FormValidation.Required,
    },
  });

  return (
    <Form
      isLoading={isAnalyzing}
      actions={
        <ActionPanel>
          <Action.SubmitForm
            title="Analyze Account"
            icon={Icon.MagnifyingGlass}
            onSubmit={handleSubmit}
          />
          <Action.Push
            title="View Previous Analyses"
            icon={Icon.List}
            target={<PreviousAnalyses />}
          />
        </ActionPanel>
      }
    >
      <Form.TextField
        title="Instagram Account"
        placeholder="username (without @)"
        {...itemProps.account}
      />
      <Form.Dropdown title="Timeframe" {...itemProps.timeframe}>
        <Form.Dropdown.Item value="7d" title="Last 7 Days" />
        <Form.Dropdown.Item value="30d" title="Last 30 Days" />
        <Form.Dropdown.Item value="90d" title="Last 90 Days" />
        <Form.Dropdown.Item value="1y" title="Last Year" />
      </Form.Dropdown>
      <Form.Dropdown title="Analysis Depth" {...itemProps.depth}>
        <Form.Dropdown.Item value="quick" title="Quick Analysis" />
        <Form.Dropdown.Item value="standard" title="Standard Analysis" />
        <Form.Dropdown.Item value="deep" title="Deep Dive" />
      </Form.Dropdown>
      <Form.Checkbox
        label="Include Visual Analytics"
        {...itemProps.includeVisuals}
      />
      <Form.Dropdown title="Output Format" {...itemProps.outputFormat}>
        <Form.Dropdown.Item value="markdown" title="Markdown Report" />
        <Form.Dropdown.Item value="json" title="JSON Data" />
        <Form.Dropdown.Item value="both" title="Both Formats" />
      </Form.Dropdown>
    </Form>
  );
}

function AnalysisResults({ result, config }: { result: AnalysisResult; config: AnalysisConfig }) {
  const markdown = generateMarkdownReport(result, config);

  return (
    <Detail
      markdown={markdown}
      navigationTitle={`@${result.account} Analysis`}
      actions={
        <ActionPanel>
          <Action.CopyToClipboard
            title="Copy Report"
            content={markdown}
            icon={Icon.Clipboard}
          />
          <Action.OpenInBrowser
            title="Export to File"
            url={`file://${process.env.HOME}/Desktop/${result.account}_analysis.md`}
            icon={Icon.Download}
          />
          <Action.Push
            title="New Analysis"
            icon={Icon.Plus}
            target={<AnalyzeCommand />}
          />
        </ActionPanel>
      }
    />
  );
}

function PreviousAnalyses() {
  const [analyses, setAnalyses] = useState<AnalysisResult[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadPreviousAnalyses();
  }, []);

  async function loadPreviousAnalyses() {
    try {
      const allItems = await LocalStorage.allItems();
      const analysisItems = Object.entries(allItems)
        .filter(([key]) => key.startsWith("analysis-"))
        .map(([_, value]) => JSON.parse(value) as AnalysisResult)
        .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
      
      setAnalyses(analysisItems);
    } catch (error) {
      showToast({
        style: Toast.Style.Failure,
        title: "Failed to load analyses",
      });
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <List isLoading={isLoading} navigationTitle="Previous Analyses">
      {analyses.map((analysis, index) => (
        <List.Item
          key={index}
          title={`@${analysis.account}`}
          subtitle={new Date(analysis.timestamp).toLocaleDateString()}
          accessories={[
            { text: `${analysis.metrics.followers.toLocaleString()} followers` },
            { text: `${analysis.metrics.engagement}% engagement` },
          ]}
          actions={
            <ActionPanel>
              <Action.Push
                title="View Analysis"
                icon={Icon.Eye}
                target={<AnalysisResults result={analysis} config={{} as AnalysisConfig} />}
              />
              <Action.CopyToClipboard
                title="Copy Report"
                content={generateMarkdownReport(analysis, {} as AnalysisConfig)}
              />
            </ActionPanel>
          }
        />
      ))}
    </List>
  );
}

async function performAnalysis(config: AnalysisConfig): Promise<AnalysisResult> {
  // This is a mock implementation
  // In a real implementation, this would call Instagram APIs or scraping services
  
  await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate API call

  return {
    account: config.account,
    timestamp: new Date().toISOString(),
    metrics: {
      followers: Math.floor(Math.random() * 1000000) + 10000,
      engagement: Math.floor(Math.random() * 10) + 1,
      posts: Math.floor(Math.random() * 1000) + 100,
    },
    demographics: {
      ageGroups: {
        "18-24": 25,
        "25-34": 35,
        "35-44": 20,
        "45-54": 15,
        "55+": 5,
      },
      genderSplit: {
        "Female": 65,
        "Male": 35,
      },
      topLocations: ["New York", "Los Angeles", "Miami", "Chicago", "Houston"],
    },
    insights: [
      "High engagement rate during evening hours (6-9 PM EST)",
      "Fashion and lifestyle content performs best",
      "Strong female audience aged 25-34",
      "Peak activity on weekdays",
      "Video content generates 3x more engagement than photos",
    ],
    recommendations: [
      "Post more video content to capitalize on higher engagement",
      "Schedule posts between 6-9 PM EST for maximum reach",
      "Create content targeting female millennials",
      "Collaborate with fashion and lifestyle brands",
      "Use location tags for major metropolitan areas",
    ],
  };
}

function generateMarkdownReport(result: AnalysisResult, config: AnalysisConfig): string {
  return `# Instagram Analysis Report: @${result.account}

## Overview
- **Date**: ${new Date(result.timestamp).toLocaleString()}
- **Followers**: ${result.metrics.followers.toLocaleString()}
- **Engagement Rate**: ${result.metrics.engagement}%
- **Total Posts**: ${result.metrics.posts}

## Demographics

### Age Distribution
${Object.entries(result.demographics.ageGroups)
  .map(([age, percent]) => `- ${age}: ${percent}%`)
  .join("\n")}

### Gender Split
${Object.entries(result.demographics.genderSplit)
  .map(([gender, percent]) => `- ${gender}: ${percent}%`)
  .join("\n")}

### Top Locations
${result.demographics.topLocations.map((loc, i) => `${i + 1}. ${loc}`).join("\n")}

## Key Insights
${result.insights.map(insight => `- ${insight}`).join("\n")}

## Recommendations
${result.recommendations.map(rec => `- ${rec}`).join("\n")}

---
*Generated by Instagram Analyzer for Raycast*`;
} 