import typer

from rich import print
from typing import Annotated

from rich.panel import Panel
from rich.console import Console

from api.api_v1.auth.services import redis_tokens as tokens


app = typer.Typer(
    name="token",
    help="Token management command",
    rich_markup_mode="rich",
    no_args_is_help=True,
)


@app.command(
    help="[bold red]Check if token is valid - exists or not[/bold red]",
)
def check(
    token: Annotated[
        str,
        typer.Argument(help="The token to check."),
    ],
) -> None:
    print(
        f"Token [bold]{token}[/bold]",
        (
            "[bold green]exists[/bold green]"
            if tokens.token_exists(token)
            else "[bold red]doesn't exist[/bold red]"
        ),
    )


@app.command(
    name="list",
    help="[bold red]Get all existing tokens.[/bold red]",
)
def list_tokens() -> None:
    all_tokens = tokens.get_tokens()
    if not tokens:
        print("[bold red]No tokens found.[/bold red]")
        return

    console = Console()
    print()
    console.rule("[bold cyan]Available API tokens[/bold cyan]")

    for token in all_tokens:
        print(Panel(f"[green]{token}[/green]", title="Token"))


@app.command(
    help="[bold red]Create and add a new token.[/bold red]",
)
def create() -> None:
    new_token = tokens.generate_and_save_token()
    print(Panel(f"Created and added token: [green]{new_token}[/green]"))


@app.command(
    help="[bold red]Add a new token.[/bold red]",
)
def add(
    token: Annotated[
        str,
        typer.Argument(help="Your token to add"),
    ],
) -> None:
    tokens.add_token(token)
    print(Panel(f"Token: [green]{token}[/green] added"))


@app.command(
    help="[bold red]Delete existing token.[/bold red]",
)
def delete(
    token: Annotated[
        str,
        typer.Argument(help="Your token to delete"),
    ],
) -> None:
    if not tokens.token_exists(token):
        print(f"[bold red]Token: [green]{token}[/green] not found.[/bold red]")
        return

    tokens.delete_token(token)
    print(Panel(f"Token: [green]{token}[/green] deleted"))
