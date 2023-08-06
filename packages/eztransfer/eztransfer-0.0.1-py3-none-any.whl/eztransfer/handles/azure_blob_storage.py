from azure.storage.blob import BlobServiceClient

from src.eztransfer.base import BaseHandle
from src.eztransfer.util import typename, insert_logger


@insert_logger
class AzureBlobStorageHandle(BaseHandle):
    def __init__(self, connection_string: str, container: str):
        self._connection_string = connection_string
        self._container = container
        self._client = None

    @property
    def client(self):
        return self._client

    def connect(self):
        self._client = BlobServiceClient.from_connection_string(self._connection_string)
        self.logger.info("Connected")

    def disconnect(self):
        self.client.close()
        self.logger.info("Disconnected")

    def download(self, remote_path: str, local_path: str):
        blob = self.client.get_blob_client(self._container, remote_path)
        with open(local_path, "wb") as download_file:
            download_file.write(blob.download_blob().readall())
        self.logger.info(f"File {remote_path!r} downloaded")

    def upload(self, local_path: str, remote_path: str):
        blob = self.client.get_blob_client(self._container, remote_path)
        with open(local_path, "rb") as source:
            blob.upload_blob(source)
        self.logger.info(f"File {local_path!r} uploaded to {remote_path!r}")

    def __repr__(self):
        return f"{typename(self)}(connection_string={self._connection_string!r}, container={self._container!r})"
