import typer

from .app import ATopApp

app = typer.Typer(
    name="a-top",
    help="A modern Linux process and system monitor.",
)


@app.callback(invoke_without_command=True)
def monitor(ctx: typer.Context):
    """Start A-top."""

    if ctx.invoked_subcommand is None:
        ATopApp().run()


def main():
    app()