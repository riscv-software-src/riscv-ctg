# See LICENSE.incore for details
"""Console script for riscv_ctg."""

import click

from riscv_ctg.ctg import ctg
from riscv_ctg.__init__ import __version__

@click.command()
@click.version_option(version=__version__)
@click.option('--verbose', '-v', default='error', help='Set verbose level')
@click.option('--dir', '-d', default='', type=click.Path(), help='Work directory path')
@click.option('--clean','-c', is_flag='True', help='Clean builds')
def cli(verbose, dir, clean):
    ctg(verbose, dir, clean)

if __name__ == '__main__':
    cli()
