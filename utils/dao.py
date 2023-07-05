from supabase import Client

from utils.dto import Table, Image


class TableDAO:
    def __init__(self, client: Client):
        self.client = client

    def get_all(
            self,
            table_name: str,
            path_for_csv: str = None
    ):

        result = self.client.table(table_name=table_name).select("*").execute()
        dto = Table(
            rows=result.data
        )
        if path_for_csv:
            dto.to_csv(path_for_csv)
        return dto

    def save(self, table_name: str, obj: Table):
        self.client.table(table_name=table_name).insert(obj.rows).execute()


class StorageDAO:
    def __init__(self, client: Client):
        self.client = client

    def upload_images(self, objects: list[Image]):
        for obj in objects:
            with open(obj.path, 'rb+') as f:
                self.client.storage.from_('jpg_test').upload('/', f)
