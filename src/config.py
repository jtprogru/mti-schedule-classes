
class Config:
    GROUPS = {
        101: {"_id": 22051, "name": "ОДКИПо-101"},
        102: {"_id": 22317, "name": "ОДКИПо-102"},
        103: {"_id": 22947, "name": "ОДКИПо-103"},
        104: {"_id": 23134, "name": "ОДКИПо-104"},
    }

    DATE_FORMAT = "%d.%m.%y"

    def __init__(self):
        self.base_url = 'https://mti.edu.ru'
        self.schedule_url = f'{self.base_url}/studentam/raspisanie-zanyatij/?view_mode=student&param='
        # self.

    def get_group(self, group_id: int) -> dict:
        return self.GROUPS[group_id]

