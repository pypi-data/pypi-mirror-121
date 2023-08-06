import logging
from enum import Enum

from azure.storage.blob import BlobServiceClient

from mxsearchstorage.schema import BatchError, Type

logger = logging.getLogger(__name__)
RETRY_COUNT = 3

class BlobStorage(object):

    def __init__(self, primary_connectionString, secondary_connectionString):
       self.primary_store = BlobServiceClient.from_connection_string(conn_str=primary_connectionString)
       self.secondary_store = BlobServiceClient.from_connection_string(conn_str=secondary_connectionString)


    def get_connection(self, type):
        if type == Type.PRIMARY:
            return self.primary_store
        if type == Type.SECONDARY:
            return self.secondary_store
        raise BatchError(
            "failed to get connection for {}".format(type)
        )

    def create_container(self, type, container_name):
        conn = self.get_connection(type)
        try:
            conn.create_container(container_name)
            logging.info("create container {}".format(container_name))
        except Exception as e:
            logger.error(
                "failed create container {} : {}".format(container_name, e)
            )

    def upload_object_single(self, type, container_name, file_name, file_path):
        conn = self.get_connection(type)
        blob_client = conn.get_blob_client(container_name, file_name)
        for index in range(RETRY_COUNT):
            try:
                with open(file_path, 'rb') as data:
                    blob_client.upload_blob(data)
                logging.info(f"Following models have been uploaded successfully:{file_name} ____.")
                break
            except Exception as e:
                logger.error(
                    "failed to upload file {} in {} of {} data center with error: {}".format(
                        file_name, container_name, type, e
                    )
                )
                logger.error("Retry {} time".format(str(index + 1)))
                if index == RETRY_COUNT - 1:
                    logger.error(
                        "failed to retry uploading pickle files in {} in {} : {}".format(container_name,type, e)
                    )


    def list_objects(self, type, container_name):
        conn = self.get_connection(type)
        blob_list = []
        try:
            container_client = conn.get_container_client(container_name)
            blob_list = container_client.list_blobs()
        except Exception as e:
            logger.error(
                "failed to list files in {} with error: {}".format(
                    container_name, e
                )
            )
        return blob_list

    def download_object(self, type, container_name, file_name, target_path):
        conn = self.get_connection(type)
        try:
            blob_client = conn.get_blob_client(container_name, file_name)
            with open(target_path, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())
        except Exception as e:
            logger.error(
                "failed to upload file {} in {} with error: {}".format(file_name,
                    container_name, e
                )
            )
            return False
        return True

    def upload_object(self, container_name, file_name, file_path):
        self.upload_object_single(Type.PRIMARY, container_name, file_name, file_path)
        self.upload_object_single(Type.SECONDARY, container_name, file_name, file_path)

    def delete_object(self, type, container_name, file_name):
        conn = self.get_connection(type)
        try:
            container_client = conn.get_container_client(container_name)
            container_client.delete_blob(file_name)
        except Exception as e:
            logger.error(
                "failed to delete file {} in {} in {} with error: {}".format(file_name,
                    container_name, type, e
                )
            )
            return False
        return True

    def swpie_container(self, type, container_name):
        conn = self.get_connection(type)
        blob_list = self.list_objects(type, container_name)
        try:
            for blob in blob_list:
                container_client = conn.get_container_client(container_name)
                container_client.delete_blob(blob)
        except Exception as e:
            logger.error("failed to swpie {} in {} with error: {}".format(container_name, type, e))
            return False
        return True