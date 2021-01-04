import requests
import json
import pandas as pd


def get_connection():
    url = "https://jobs.github.com/positions.json"
    get_content = requests.get(url).content
    return get_content


def get_pandas_json():
    content = get_connection()
    jobs = pd.read_json(content)
    return jobs


def get_json():
    data = json.loads(get_connection())
    return data
