from download_stats.pepy import stats 
from download_stats.pypistats import recent
from download_stats.pypistats import system
from download_stats.pypistats import version
from typing import Union

from rich.console import Console
from rich.table import Table

import sys

def summary_table(package: str) -> None:
    data = stats(package)
    table = Table(title="Downloads Summary")

    table.add_column("Total", justify="right", style="cyan", no_wrap=True)
    table.add_column("30 Days", style="magenta")
    table.add_column("7 Days", justify="right", style="green")

    table.add_row(data['total'], data['30_days'], data['7_days'])

    console = Console()
    console.print(table)

def main():
    summary_table(sys.argv[1])
