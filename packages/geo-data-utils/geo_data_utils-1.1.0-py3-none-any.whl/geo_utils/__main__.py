import click
import sys
from loguru import logger
from .utils import filter_data_by_ranges_from_file, down_hole_signal_plots


@click.group()
@logger.catch
def cli():
    logger.remove()

    logger.add(
        sys.stdout,
        enqueue=True,
        level="DEBUG",
        format="<green>{time:HH:mm:ss}</green> | <cyan>{process}</cyan> | <level>{message}</level>",
    )


@cli.command()
@click.argument("data_file_path", type=click.Path(exists=True))
@click.argument("filter_file_path", type=click.Path(exists=True))
@click.option(
    "--from", "-f", "from_", default="From", help="Filter Range From Column", type=str
)
@click.option("--to", "-t", default="To", help="Filter Range To Column", type=str)
@click.option("--column", "-c", default="Depth", help="Data Filter Column", type=str)
@click.option(
    "--output", "-o", default="output.xlsx", help="File to output to", type=click.Path()
)
def filter(data_file_path, filter_file_path, from_, to, column, output):
    logger.debug("Filtering data from {} by range", data_file_path)
    logger.debug("Filter File {}", filter_file_path)
    logger.debug("Filter Range Columns From: {} To: {}", from_, to)
    logger.debug("Data File Filter Column: {}", column)

    filter_data_by_ranges_from_file(
        data_file_path, filter_file_path, from_, to, column, output
    )
    logger.debug("Outputted to: {}", output)


@cli.command()
@click.argument("data_file_path", type=click.Path(exists=True))
@click.option(
    "--config", "-c", help="Yaml Config for plot", type=click.Path(exists=True)
)
@click.option("--ycol", "-y", default="Sample", help="Column for the Y axis, can also be configured in config yaml", type=str)
@click.option("--from", "-f", "from_", default=None, help="Depth From Column", type=str)
@click.option("--to", "-t", default=None, help="Depth To Column", type=str)
@click.option("--ignore_rows", "-i", help="Any rows to ignore starting from 0", multiple=True, default=None, type=int)
@click.option(
    "--output", "-o", default="output.html", help="File to output to should end in .html", type=click.Path()
)
def plot_downhole(data_file_path, config, ycol, from_, to, ignore_rows, output):
    logger.debug("Plotting data from {}", data_file_path)

    import yaml
    from colorcet import b_glasbey_bw

    colours = b_glasbey_bw
    variables = None
    if config:
        with open(config, "r") as stream:
            try:
                plot_config = yaml.safe_load(stream)
                if "y_column" in plot_config:
                    ycol = plot_config['y_column']
                    logger.info(f"Y Column:  {ycol}")
                if "depth_from" in plot_config:
                    from_ = plot_config['depth_from']
                if "depth_to" in plot_config:
                    to = plot_config['depth_to']
                    logger.info(f"To Column:  {to}")
                if "ignore_rows" in plot_config:
                    ignore_rows = plot_config['ignore_rows']
                if "variables" in plot_config:
                    variables = plot_config['variables']
                    logger.info(f"Variables:  {' '.join(variables)}")
                if "colours" in plot_config:
                    colours = plot_config['colours']
                    logger.info(f"Colours:  {' '.join(colours)}")
            except yaml.YAMLError as exc:
                logger.error(f"Couldn't load {config}")
                logger.error(exc)

    down_hole_signal_plots(
        data_file_path,
        y_column=ycol,
        from_column=from_,
        to_column=to,
        var_columns=variables,
        colours=colours,
        output_file=output,
        ignore_rows=ignore_rows
    )
    logger.debug("Outputted to: {}", output)


if __name__ == "__main__":
    cli()
