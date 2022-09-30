"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Grammar-Vocabulary Notebook Log."""


if __name__ == "__main__":
    main(prog_name="gvnl")  # pragma: no cover
