from typing import Tuple

import attr
import click


@attr.s(kw_only=True, auto_attribs=True)
class GANParams:
    data_source: str
    output_directory: str
    image_resolution: Tuple[int, int]
    batch_size: int
    n_iters: int


@click.group()
def cli():
    ...


@cli.group()
@click.option("--data-source", type=str, envvar="IMAGE_DATA_SOURCE")
@click.option("--output-directory", type=str, envvar="OUTPUT_DIRECTORY")
@click.option("--image-resolution", type=(int, int), default=(128, 128), envvar="IMAGE_RESOLUTION")
@click.option("--batch-size", type=int, default=32)
@click.option("--n-iters", type=int, default=10000)
@click.pass_context
def training(
    ctx: click.Context,
    data_source: str,
    output_directory: str,
    image_resolution: Tuple[int, int],
    batch_size: int,
    n_iters: int,
):
    """CLI command to train different GAN models."""
    ctx.ensure_object(dict)
    ctx.obj = GANParams(
        data_source=data_source,
        output_directory=output_directory,
        image_resolution=image_resolution,
        batch_size=batch_size,
        n_iters=n_iters,
    )
