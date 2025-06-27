import typer

from typing import Annotated
from rich import print

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
