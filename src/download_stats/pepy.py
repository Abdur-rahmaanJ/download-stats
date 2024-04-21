import os 
import time
from datetime import datetime 

from rich.console import Console
import requests

def parse_datetime(datetime_str):
    return datetime.strptime(datetime_str, '%Y-%m-%d')

console = Console()

def fetch_raw_data(project_name):
    try:
        api_key = os.environ.get("PEPY_API_KEY")
    except KeyError:
        raise Exception("Please set pepy.tech's api key in a variable named PEPY_API_KEY. Get one by signing in.")
    if api_key is None:
        raise Exception("Variable named PEPY_API_KEY is empty. Please provide a new key. Get one by signing in.")

    result = requests.get(f'https://api.pepy.tech/api/v2/projects/{project_name}', headers={'X-Api-Key': api_key})
    return result

def extract_data(project):
    raw_result = fetch_raw_data(project)

    raw_result_json = raw_result.json() 

    total_downloads = raw_result_json['total_downloads']
    sum7days = 0
    sum30days = 0

    target_versions = []

    if len(raw_result_json['versions'][::-1]) >= 2:
        i = 0
        while i <= 2:
            target_versions.append(raw_result_json['versions'][-i])
            i += 1
    first_row = ['Date']
    for v in target_versions:
        first_row.append(v)
    first_row.extend(['Sum', 'Total'])
    table = [
            first_row
            # ["2022-09-01", "0", "1", "3", "4", "24"],
            # ["2022-08-31", "2", "1", "17", "20", "126"],
            # ["2022-06-04", "0", "0", "0", "0", "9"],
        ]
    
    row_data = []
    for date in raw_result_json['downloads']:
        datetime_obj = parse_datetime(date)
        current_datetime = datetime.now()
        days_delta = (current_datetime-datetime_obj).days

        
        row = {

        }
        date_downloads = 0
        for version in raw_result_json['downloads'][date]:
            num_dwnlds = raw_result_json['downloads'][date][version]

            if days_delta <= 7:
                sum7days += num_dwnlds
            if days_delta <= 30:
                sum30days += num_dwnlds
        

            date_downloads += num_dwnlds
            if version in target_versions:
               row[version] = num_dwnlds

        row_data.append([date, row, date_downloads])
    
    for _row in row_data:
        date = _row[0]
        row = _row[1]
        total = _row[2]
        version_row = []
        if row == {}:
            continue
        for t in target_versions:
            if t in row:
                version_row.append(str(row[t]))
            else:
                version_row.append('0')
        
        sum_version_row = sum([int(i) for i in version_row])
        table_row = [date]
        table_row.extend(version_row)
        table_row.extend([str(sum_version_row),str(total)])
        table.append(table_row)


    return {
        'total': str(total_downloads),
        "30_days": str(sum30days),
        "7_days": str(sum7days),
        "by_version": table,
    }


def stats(project: str, no_rich=False) -> dict:

    if no_rich:
        data = extract_data(project)
        time.sleep(5)
    else:
        with console.status("[bold green]Getting content...") as status:
            data = extract_data(project)
            time.sleep(5)

    return data