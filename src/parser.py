import datetime
from pprint import pprint

import html_to_json
import requests

import config

cfg = config.Config()


def run(day: str):
    html_ = __get_html(group_id=103)
    output_json = html_to_json.convert(html_)
    table = output_json["html"][0]["body"][0]["div"][0]["div"][1]["div"][0]["div"][1]["div"][0]["div"][1]["div"][0]["table"][0]

    day_schedule = __get_day_schedule(table["tr"], day)
    # print("=" * 30)
    # print(day_schedule)
    # print("=" * 30)
    # print(len(day_schedule["classess"]))
    pprint(day_schedule["classess"])


def __get_day_schedule(table: dict, schedule_date: str) -> dict:
    day_schedule = dict()
    needed_date = datetime.datetime.strptime(schedule_date, cfg.DATE_FORMAT)
    counter = 1
    cursor = 1
    while counter < len(table):
        if len(table[counter]["td"]) < 7:
            counter += 1
            continue

        if len(table[counter]["td"]) == 8:
            sd = datetime.datetime.strptime(
                table[counter]["td"][0]["span"][0]["_value"]
                .split(" ")[0]
                .replace(",", ""),
                cfg.DATE_FORMAT,
            )
            if sd == needed_date:
                teacher_name = __get_teacher_name(table[counter])
                day_schedule["day"] = needed_date
                day_schedule["classess"] = list()
                day_schedule["classess"].append(
                    __get_lectures(table[counter]["td"], teacher_name)
                )

                try:
                    while len(table[counter + cursor]["td"]) != 8:
                        teacher_name = __get_teacher_name(table[counter + cursor])
                        day_schedule["classess"].append(
                            __get_lectures(table[counter + cursor]["td"], teacher_name)
                        )
                        cursor += 1
                except IndexError as e:
                    print(f"fuck: {e}")
        counter += 1
    return day_schedule


def __get_lectures(td: dict, teacher_name: str) -> dict:
    if len(td) == 8:
        return {
            str(td[1]["_value"]): {
                "lecture": str(td[3]["_value"]),
                "class_room": str(td[6]["_value"]),
                "type": str(td[4]["span"][0]["_value"]),
                "corps": str(td[5]["span"][0]["_value"]),
                "teacher_name": teacher_name,
            }
        }
    else:
        return {
            str(td[0]["_value"]): {
                "lecture": str(td[2]["_value"]),
                "class_room": str(td[5]["_value"]),
                "type": str(td[3]["span"][0]["_value"]),
                "corps": str(td[4]["span"][0]["_value"]),
                "teacher_name": teacher_name,
            }
        }


def __get_teacher_name(tr: dict) -> str:

    try:
        teacher_name = tr["td"][-1]["a"][0]["_value"]
        return str(teacher_name)
    except KeyError or TypeError:
        return "Учитель не назначен"


def __get_html(group_id: int = 103) -> str:
    url = cfg.schedule_url + str(cfg.get_group(group_id)["_id"])
    result = requests.get(url)

    if result.status_code != 200:
        return ""

    return result.text
