import re
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.text import Text

ARCH_PATH = Path("PROJECT_ARCHITECTURE.md")
CLAUDE_PATH = Path("CLAUDE.md")
console = Console()

def parse_project_architecture():
    data = ARCH_PATH.read_text(encoding="utf-8")
    status = re.search(r"\*\*Status:\*\* (.+?)\s", data)
    target = re.search(r"\*\*Target:\*\* (.+?)\s", data)
    phase = re.search(r"### \*\*(Phase [A-Z]: .+?)\*\*", data)
    tasks = re.findall(r"\[(COMPLETED|IN_PROGRESS|PENDING)\] (.+)", data)
    followers = re.search(r"\*\*Followers:\*\* (.+?)\s", data)
    engagement = re.search(r"\*\*Engagement Rate:\*\* (.+?)\s", data)
    growth = re.search(r"\*\*Growth Rate:\*\* (.+?)\s", data)
    post_value = re.search(r"\*\*Post Value:\*\* (.+?)\s", data)
    return {
        "status": status.group(1) if status else "",
        "target": target.group(1) if target else "",
        "phase": phase.group(1) if phase else "",
        "tasks": tasks,
        "followers": followers.group(1) if followers else "",
        "engagement": engagement.group(1) if engagement else "",
        "growth": growth.group(1) if growth else "",
        "post_value": post_value.group(1) if post_value else "",
    }

def parse_claude():
    data = CLAUDE_PATH.read_text(encoding="utf-8")
    agent = re.search(r"\*\*Agent Name:\*\* (.+?)\s", data)
    mission = re.search(r"\*\*Mission:\*\* (.+?)\s", data)
    log_example = re.search(r"(<task>.+?</task>)", data, re.DOTALL)
    return {
        "agent": agent.group(1) if agent else "",
        "mission": mission.group(1) if mission else "",
        "log_example": log_example.group(1) if log_example else "",
    }

def make_dashboard():
    arch = parse_project_architecture()
    claude = parse_claude()
    layout = Layout()
    header = f"[bold cyan]Brooks Nader Audience Monetization System[/bold cyan]\n"
    header += f"[bold]Phase:[/bold] {arch['phase']}    [bold]Status:[/bold] {arch['status']}    [bold]Target:[/bold] {arch['target']}"
    layout.split_column(
        Layout(Panel(header, style="bold white on blue"), name="header", size=3),
        Layout(name="body"),
    )
    body = layout["body"]
    body.split_row(
        Layout(name="left"),
        Layout(name="right"),
    )
    tasks_table = Table(title="Active Research Tasks", show_header=True, header_style="bold magenta")
    tasks_table.add_column("Status", style="cyan", width=12)
    tasks_table.add_column("Task", style="white")
    for status, task in arch["tasks"]:
        tasks_table.add_row(status, task)
    metrics = (
        f"[bold]Followers:[/bold] {arch['followers']}\n"
        f"[bold]Engagement Rate:[/bold] {arch['engagement']}\n"
        f"[bold]Growth Rate:[/bold] {arch['growth']}\n"
        f"[bold]Post Value:[/bold] {arch['post_value']}"
    )
    left_panel = Panel(metrics, title="Key Metrics", border_style="green")
    body["left"].split_column(
        Layout(Panel(tasks_table), size=10),
        Layout(left_panel)
    )
    agent_info = (
        f"[bold]Agent:[/bold] {claude['agent']}\n"
        f"[bold]Mission:[/bold] {claude['mission']}\n"
    )
    log_panel = Panel(Text(claude['log_example'], style="yellow"), title="Execution Log Example", border_style="yellow")
    body["right"].split_column(
        Layout(Panel(agent_info, title="Agent Info", border_style="blue"), size=6),
        Layout(log_panel)
    )
    console.print(layout)

if __name__ == "__main__":
    make_dashboard() 