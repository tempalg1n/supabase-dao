from supabase import Client
from tqdm import tqdm

from utils.dto import Table, Image


class TableDAO:
    """
    Data access object for tables
    """

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
    """
    Data access object for storages. But for now it's just for pictures.
    """
    BUCKET_NAME = 'jpg_test'

    def __init__(self, client: Client):
        self.client = client

    def upload_images(self, objects: list[Image]):
        if not self._check_preview(objects):
            raise ValueError("The number of previews is not equal to the number of original shots. Check the "
                             "input data.")

        exists: None | str = self._check_existing(objects)
        if exists is not None:
            raise ValueError(f"File {exists} is already exists in directory {self.BUCKET_NAME}.")

        with tqdm(total=len(objects)) as progress_bar:
            progress_bar.set_description("Uploading data")
            for obj in objects:
                with open(obj.path, 'rb') as f:
                    self.client.storage.from_(self.BUCKET_NAME).upload(f'/{obj.title}', f)
                progress_bar.update()

    @staticmethod
    def _check_preview(objects: list[Image]) -> bool:
        """
        checking that the number of previews is equal to the number of non-previews
        """

        previews_check = {
            "preview": 0,
            "original": 0
        }
        for object in objects:
            if object.is_preview:
                previews_check["preview"] += 1
            if not object.is_preview:
                previews_check["original"] += 1

        print("Previews: ", previews_check["preview"])
        print("Originals: ", previews_check["original"])
        return previews_check["preview"] == previews_check["original"]

    def _check_existing(self, objects: list[Image]):
        """
        checking that none of those files that we want to upload to the server are there yet


        Returns: None if it's all ok, or imposter's name

        """
        existing_files = []
        for file_data in self.client.storage.from_(self.BUCKET_NAME).list():
            existing_files.append(file_data.get("name", None))
        for obj in objects:
            if obj.title in existing_files:
                return obj.title
