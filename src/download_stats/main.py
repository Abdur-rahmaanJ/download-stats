from download_stats.pepy import stats 
from download_stats.pypistats import recent
from download_stats.pypistats import system
from download_stats.pypistats import version
from typing import Union

from rich.console import Console
from rich.table import Table

import sys

def summary_table(package: str) -> None:
    print(f'Stats for {package}')
    data = stats(package)
    table = Table(title="Downloads Summary")

    table.add_column("Total", justify="right", style="cyan", no_wrap=True)
    table.add_column("30 Days", style="magenta")
    table.add_column("7 Days", justify="right", style="green")

    table.add_row(data['total'], data['30_days'], data['7_days'])

    console = Console()
    console.print(table)

    versions_table(data, package)


def compare_table(packages: list) -> None:
    packages_str = ','.join(packages)
    queried_packages = []
    
    table = Table(title="Downloads Summary")

    table.add_column("Name", justify="right", style="cyan", no_wrap=True)
    table.add_column("Total", justify="right", style="cyan", no_wrap=True)
    table.add_column("30 Days", style="magenta")
    table.add_column("7 Days", justify="right", style="green")


    for package in packages:
        try:
            data = stats(package)
            table.add_row(package, data['total'], data['30_days'], data['7_days'])
            queried_packages.append(package)
        except Exception as e:
            pass

    packages_str = ', '.join(queried_packages)
    print(f'Stats for packages: {packages_str}')
    console = Console()
    console.print(table)


def versions_table(data: list, package: str) -> None:
    table = Table(title="Versions Summary")

    table.add_column(data['by_version'][0][0], justify="right", style="cyan", no_wrap=True)
    table.add_column(data['by_version'][0][1], style="magenta")
    table.add_column(data['by_version'][0][2], style="magenta")
    table.add_column(data['by_version'][0][3], style="magenta")
    table.add_column(data['by_version'][0][4], justify="right", style="green")
    table.add_column(data['by_version'][0][5], justify="right", style="green")

    for i, r in enumerate(data['by_version']):
        if i > 0:
            table.add_row(r[0], r[1], r[2], r[3], r[4], r[5])

    console = Console()
    console.print(table)

def main():
    if len(sys.argv) == 1:
        sys.exit('Package args needed!')
    if not sys.argv[1].startswith('--'):
        summary_table(sys.argv[1])
    if sys.argv[1].casefold() == '--compare':
        if len(sys.argv) >= 3:
            compare_table(sys.argv[2:])


    
