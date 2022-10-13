from bs4 import BeautifulSoup
import requests

import config


def run():
    table = __get_table()
    for item in table:
        print(item)
        print("=" * 35)


def __get_html(group_id: int = 103) -> str:
    url = config.BASE_URL + config.GROUPS[group_id]["_id"]

    result = requests.get(url)
    if result.status_code != 200:
        return ""
    return result.text


def __get_table() -> list:
    data = []
    soup = BeautifulSoup(__get_html(), "lxml")
    table = soup.select_one(config.TABLE_SELECTOR)

    rows = table.find_all("tr")
    schedule_date = rows[0].find("th", {"class": "schedule-date"})
    schedule_time = rows[0].find("th", {"class": "schedule-time"})
    schedule_subgroup = rows[0].find("th", {"class": "schedule-subgroup"})
    schedule_dis = rows[0].find("th", {"class": "schedule-dis"})
    schedule_type = rows[0].find("th", {"class": "schedule-type"})
    schedule_bldg = rows[0].find("th", {"class": "schedule-bldg"})
    schedule_hall = rows[0].find("th", {"class": "schedule-hall"})
    schedule_lector = rows[0].find("th", {"class": "schedule-lector"})
    for row in rows[1:]:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])  # Get rid of empty values

    return data
