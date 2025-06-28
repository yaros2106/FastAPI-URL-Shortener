import typer

from rich import print
from typing import Annotated

from rich.panel import Panel
from rich.console import Console

from api.api_v1.auth.services import redis_tokens


app = typer.Typer(
    name="token",
    help="Token management command",
    rich_markup_mode="rich",
    no_args_is_help=True,
)


@app.command(
    help="Check if [bold red]token[/bold red] is valid - exists or not",
)
def check(
    token: Annotated[
        str,
        typer.Argument(help="The token to check."),
    ],
):
    print(
        f"Token [bold]{token}[/bold]",
        (
            "[bold green]exists[/bold green]"
            if redis_tokens.token_exists(token)
            else "[bold red]doesn't exist[/bold red]"
        ),
    )


@app.command(
    name="list",
    help="[bold red]Get all[/bold red] existing tokens.",
)
def list_tokens():
    tokens = redis_tokens.get_tokens()
    if not tokens:
        print("[bold red]No tokens found.[/bold red]")
        return

    console = Console()
    print()
    console.rule("[bold cyan]Available API tokens[/bold cyan]")

    for token in tokens:
        print(Panel(f"[green]{token}[/green]", title="Token"))
