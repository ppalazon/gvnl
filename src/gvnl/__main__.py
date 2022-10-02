"""Command-line interface."""
import click

from gvnl import pretty_json
from gvnl import pretty_table
from gvnl import wr_scrap


@click.group()
@click.option("-x", "--debug/--no-debug", default=False)
@click.option("-j", "--output-json", "output_json", is_flag=True, default=False)
@click.version_option()
@click.pass_context
def main(ctx, debug, output_json) -> None:
    """Grammar-Vocabulary Notebook Log."""
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug
    # TODO: Format output with json
    ctx.obj["OUT_JSON"] = output_json


@main.command("lookup")
@click.option(
    "-e", "--expression", required=True, help="Expression to look up on Wordreference"
)
@click.pass_context
def main_look_up(ctx, expression):
    """Look up an expression on wordreference."""
    click.echo(f"Looking '{expression}' up on Wordreference ...")
    translations = wr_scrap.lookup(expression)

    if ctx.obj["OUT_JSON"]:
        click.echo(pretty_json.dumps(translations))
    else:
        trans_maps = [x.__dict__ for x in translations]
        click.echo(
            pretty_table.tabulate_list_json_keys(
                trans_maps, ["expression", "type", "context", "translations"]
            )
        )


@main.command("gui")
@click.pass_context
def main_gui(ctx):
    """Open GUI interface."""
    print("Opening gui...")


if __name__ == "__main__":
    main(prog_name="gvnl")  # pragma: no cover
