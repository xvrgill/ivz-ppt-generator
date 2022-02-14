from api import app
from pyairtable import Table


class AirTableController:
    def __init__(
        self, api_key: str = app.config["AIR_TABLE_API_KEY"], base_id: str = app.config["AIR_TABLE_BASE_ID"], table_names: list[str] = [app.config["POST_GROUPS_TABLE"], app.config["POSTS_TABLE"]]
    ) -> None:
        self.api_key = api_key
        self.base_id = base_id
        self.table_names = table_names

    def get_post_group(self, id):
        post_groups_table = Table(self.api_key, self.base_id, self.table_names[0])
        return post_groups_table.get(id)

    def get_post(self, id):
        posts_table = Table(self.api_key, self.base_id, self.table_names[1])
        return posts_table.get(id)
