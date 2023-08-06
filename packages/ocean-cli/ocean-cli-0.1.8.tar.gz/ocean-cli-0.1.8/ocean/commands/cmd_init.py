import click
import os

from ocean import code
from ocean.main import Environment
from ocean.utils import print, PrintType


@click.command()
@click.option("--url", default="http://ocean-backend-svc:8000", help="pass backend url")
def cli(url):
    ctx = Environment(load=False)

    # make .oceanrc on home-dir
    if not ctx.config_path.exists():
        ctx.config_path.parent.mkdir(exist_ok=True)
        ctx.config_path.touch()

    # save env
    ctx.update_config(code.OCEAN_URL, url)
    ctx.update_config("presets", [])

    print("Setup Success.", PrintType.SUCCESS)
