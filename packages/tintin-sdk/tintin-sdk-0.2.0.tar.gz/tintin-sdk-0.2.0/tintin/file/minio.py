import os
import sys
import logging

from minio import Minio
from minio.error import S3Error

from tintin.env import Environ
from tintin.logging import httpclient_logging_activate
from tintin.file.file_manager import FileManagerInterface
from tintin.util import list_all_files

class FileManager(FileManagerInterface):
    """FileManager
        Implements minio/s3 interface for upload/download files
    """
    def __init__(self, host: str, verbose: bool):
        """__init__.

        Args:
            host (str): host
            verbose (bool): verbose
        """

        self.env = Environ()
        self.bucket = self.env.minio_bucket
        self.client = Minio(self.env.minio_endpoint,
                access_key=self.env.minio_access_key,
                secret_key=self.env.minio_access_secret,
                secure=False,
        )

        if verbose:
            self.client.trace_on(sys.stdout)

        self.__ensure_bucket_exist()

    def __ensure_bucket_exist(self):
        if not self.client.bucket_exists(self.bucket):
            raise RuntimeError('Failed to connect bucket ({})'.format(self.bucket))

    def list(self, prefix: str, recursive: bool) -> [str]:
        """list.

        Args:
            prefix (str): prefix

        Returns:
            [str]:
        """

        objects = self.client.list_objects(self.bucket, prefix=prefix, recursive=recursive)
        objects_in_names_list = []
        for object in objects:
            objects_in_names_list.append(object.object_name)
        return objects_in_names_list

    def strip_local_path(self, path: str) -> str:
        if path.startswith('/'):
            return path[len('/'):]
        if path.startswith('./'):
            return path[len('./'):]
        return path

    def upload(self, prefix: str, local_dir: str):
        """upload.

        Args:
            prefix (str): prefix
            local_dir (str): local_dir
        """
 
        local_file_paths = list_all_files(local_dir)
        if not local_file_paths:
            logging.info('nothing to be uploaded')
            return False
        for local_file_path in local_file_paths:
            dst_path = self.strip_local_path(os.path.join(prefix,
                self.strip_local_path(local_file_path)))
            try:
                self.client.fput_object(
                    self.bucket,
                    dst_path,
                    local_file_path,
                )
            except S3Error as err:
                logging.info('{} upload failed, error msg:{}'.format(local_file_path, err))
                return False
            logging.info('{} has been upload.'.format(dst_path))
        return True

    def download(self, dst: str, objectpaths: [str], recursive: bool = False):
        """download.

        Args:
            dst (str): dst
            objectpaths ([str]): objectpaths
            recursive (bool): recursive
        """
        resolved_object_paths:[str] = []
        # resolve filepaths all
        for object_path in objectpaths:
            resolved_object_paths.extend(self.list(object_path, recursive))
        if not resolved_object_paths:
            logging.info('{} download failed, no resolved object paths'.format(objectpaths))
            return False
        for object_path in resolved_object_paths:
            dst_path = os.path.join(dst, self.strip_local_path(object_path))
            try:
                self.client.fget_object(self.bucket, object_path, dst_path)
            except S3Error as err:
                logging.info('{} download failed, error msg:{}'.format(object_path, err))
                return False
            logging.info('{} has been downloaded.'.format(dst_path))
        return True

