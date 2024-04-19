import os 
import time

from rich.console import Console
import requests

console = Console()

def fetch_raw_data(project_name):
    try:
        api_key = os.environ.get("PEPY_API_KEY")
    except KeyError:
        raise Exception("Please set pepy.tech's api key in a variable named PEPY_API_KEY. Get one by signing in.")
    if api_key is None:
        raise Exception("Please set pepy.tech's api key in a variable named PEPY_API_KEY. Get one by signing in.")

    result = requests.get(f'https://api.pepy.tech/api/v2/projects/{project_name}', headers={'X-Api-Key': api_key})
    return result

def stats(project: str, no_rich=False) -> dict:

    if no_rich:
        raw_result = fetch_raw_data(project)

        raw_result_json = raw_result.json() 
        total_downloads = raw_result_json['total_downloads']
        time.sleep(5)
    else:
        with console.status("[bold green]Getting content...") as status:
            raw_result = fetch_raw_data(project)

            raw_result_json = raw_result.json() 
            total_downloads = raw_result_json['total_downloads']
            time.sleep(5)

    

    return {
        'total': str(total_downloads),
        "30_days": "1484",
        "7_days": "506",
        "by_version": [
            ["Date", "4.5.7", "4.5.8", "4.6.0", "Sum", "Total"],
            ["2022-09-01", "0", "1", "3", "4", "24"],
            ["2022-08-31", "2", "1", "17", "20", "126"],
            ["2022-06-04", "0", "0", "0", "0", "9"],
        ],
    }