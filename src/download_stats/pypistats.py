import requests
from typing import Union


domain = 'https://pypistats.org'




def recent(package: str, period: str=None) -> dict:
    args = {}
    if period:
        if period.casefold() in ['day', 'week', 'month']:
            args = {'period': period}
        else:
            raise Exception('Period should be in day, week, month')
    req = requests.get(domain+f'/api/packages/{package}/recent', params=args)
    return req.json()


def version(package: str, version: Union[int, float]=None, type: str=None) -> dict:
    type_ = type
    args = {}

    if type_:
        if type_.casefold() in ['major']:
            url = url = domain+f'/api/packages/{package}/python_major'
        elif type_.casefold() in ['minor']:
            url = domain+f'/api/packages/{package}/python_minor'
        else:
            raise Exception('type should be major or minor')
    else:
        url = url = domain+f'/api/packages/{package}/python_major'
    if version:
        if isinstance(version, int):
            url = domain+f'/api/packages/{package}/python_major'
            args = {'version': version}
        elif isinstance(version, float):
            url = domain+f'/api/packages/{package}/python_minor'
            args = {'version': version}
        else:
            raise Exception('version should be an integer or float')
    req = requests.get(url, params=args)
    return req.json()


def system(package: str, name: str=None) -> dict:
    args = {}
    if name:
        os_names = ['windows', 'linux', 'darwin', 'other']
        if name.casefold() in os_names:
            args = {'os': name}
        else:
            raise Exception('Os name should be in:'+','.join(os_names))
    req = requests.get(domain+f'/api/packages/{package}/system', params=args)
    return req.json()