import importlib.metadata

from rich import print as rprint
import typer


def register_version(app: typer.Typer):
    @app.command()
    def version() -> None:
        """Show the FLOW-3D manager version."""
        try:
            version = importlib.metadata.version("FLOW-3D")
            rprint(f"✅ FLOW-3D manager version {version}")
        except importlib.metadata.PackageNotFoundError:
            rprint(
                "⚠️  [yellow]FLOW-3D version unknown (package not installed)[/yellow]"
            )
            raise typer.Exit()
    return version


