from azure.storage.blob import BlobServiceClient


class BlobService:
    """
    Defines methods for Azure Blob Storage access.
    """

    def __init__(self):
        self.service = None
        self.connection_string = None

    def set_sas(self, connection_string):
        self.connection_string = connection_string
        self.service = BlobServiceClient.from_connection_string(
            connection_string)

    def upload(self, file_path, shared_storage_container, blob_name):
        blob_client = self.service.get_blob_client(
            container=shared_storage_container, blob=blob_name)

        with open(file_path, "rb") as data:
            blob_client.upload_blob(data)

    def download(self, tempfile, shared_storage_container, blob_name):
        blob_client = self.service.get_blob_client(
            container=shared_storage_container, blob=blob_name)

        with open(tempfile.file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

        return tempfile

    def delete(self, blob_name):
        self.service.delete_blob(blob=blob_name)

    @staticmethod
    def create_anonymous(azure_storage_connection_string):
        blob_service = BlobService()
        blob_service.set_sas(azure_storage_connection_string)
        return blob_service
