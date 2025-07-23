from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt
import asyncio
from coordination import ResearchCoordinator

load_dotenv()
console = Console()


async def main():
    console.print("[bold cyan]Deep Research Toll[/bold cyan] - Console Edition")
    console.print("This tool performs in-depth research on any topic using AI agents.")

    query = Prompt.ask("\n[bold] What would you like to research?[/bold]")
    if not query.strip():
        console.print("[bold red]Error:[/bold red] please provide a valid query.")


    research_coordinator = ResearchCoordinator(query)
    report = await research_coordinator.research()

    print(report)


if __name__ == "__main__":
    asyncio.run(main())