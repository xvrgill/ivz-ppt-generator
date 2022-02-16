from api import app
from pyairtable import Table


class AirTableController:
    def __init__(self, api_key: str = "keyDFVLu56iM5h3za", base_id: str = "appPxABnbFX7yd6LQ", table_names: list[str] = ["Social Post Groups", "Social Posts"]) -> None:
        self.api_key = api_key
        self.base_id = base_id
        self.table_names = table_names

    def get_post_group(self, id):
        post_groups_table = Table(self.api_key, self.base_id, self.table_names[0])
        return dict(post_groups_table.get(id))

    def get_post(self, id):
        posts_table = Table(self.api_key, self.base_id, self.table_names[1])
        return dict(posts_table.get(id))
