from supabase import Client

from dto import Table


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
