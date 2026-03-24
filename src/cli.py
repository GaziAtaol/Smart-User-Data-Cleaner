from __future__ import annotations
import typer

app = typer.Typer(
    name="smdc",
    help="Smart User Data Cleaner — automated data cleaning pipeline.",
    add_completion=False,
)

@app.command()
def profile(
    input_path: str = typer.Option(..., "--input", "-i", help="Path to input data file."),
) -> None:
    """Print a statistical profile of the input dataset."""
    typer.echo(f"[profile] Input: {input_path}  — not yet implemented.")

@app.command()
def clean(
    input_path: str = typer.Option(..., "--input", "-i", help="Path to input data file."),
    config_path: str = typer.Option("config/rules.json", "--config", "-c"),
    output_path: str = typer.Option(..., "--output", "-o"),
) -> None:
    """Run the full cleaning pipeline on the input dataset."""
    typer.echo(f"[clean] Input: {input_path}  Config: {config_path}  Output: {output_path}  — not yet implemented.")

@app.command()
def validate(
    input_path: str = typer.Option(..., "--input", "-i"),
    schema_path: str = typer.Option(..., "--schema", "-s"),
) -> None:
    """Validate an input dataset against a Pydantic schema."""
    typer.echo(f"[validate] Input: {input_path}  Schema: {schema_path}  — not yet implemented.")

@app.command()
def report(
    input_path: str = typer.Option(..., "--input", "-i"),
    output_dir: str = typer.Option("reports/", "--output", "-o"),
    fmt: str = typer.Option("html", "--format", "-f"),
) -> None:
    """Generate a cleaning report from a processed dataset."""
    typer.echo(f"[report] Input: {input_path}  Output: {output_dir}  Format: {fmt}  — not yet implemented.")

if __name__ == "__main__":
    app()
