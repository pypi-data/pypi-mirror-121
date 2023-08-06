import os
from urllib.parse import unquote_plus
import boto3
import s3fs
import fnmatch

client = boto3.client("s3")
fs = s3fs.S3FileSystem()


def validate_folder_structure(key: str):
    """The function will validate the folder structure (prefix) of S3 objects in the
    landing bucket to ensure they conform to the structure required by downstream
    processes.
    Parameters
    ----------
    key : str
        The S3 object key.
    """
    valid_prefixes = [
        "data/database_name=*_*/table_name=*/extraction_timestamp=*",
        "logs/database_name=*/table_name=*/extraction_timestamp=*",
        "metadata/database_name=*/table_name=db_and_table_list/extraction_timestamp=*",
    ]
    for prefix in valid_prefixes:
        if fnmatch.fnmatch(key, prefix):
            return True


def move_object(destination_bucket: str, source_bucket: str, source_key: str):
    """The function will copy the object in S3 to the "destination_bucket" bucket,
    while adding a timestamp to the filename. It will then
    delete the original object from "source_bucket".
    Parameters
    ----------
    destination_bucket : str
        The bucket where the S3 object will be copied to.
    source_bucket : str
        The bucket where the S3 object is.
    source_key : str
        The object S3 key.
    """
    client = boto3.client("s3")

    client.copy_object(
        Bucket=destination_bucket,
        CopySource={"Bucket": source_bucket, "Key": source_key},
        Key=source_key,
        ServerSideEncryption="AES256",
        ACL="bucket-owner-full-control",
    )
    client.delete_object(Bucket=source_bucket, Key=source_key)


class EmptyFileError(Exception):
    """Raised when the file opened has no contents"""

    pass


class FileValidator:
    """
    A class to validate data in the Land-to-History pipeline. Currently
    merely checks that the file can be opened, and contains a non-zero
    amount of bytestream content. If both conditions are met, it moves
    to the pass bucket, otherwise moves the object to the fail bucket.
    Attributes
    ----------
    key : str
        The AWS S3 key of the file being validated.
    pass_bucket : str
        The name of the bucket for files that pass validation.
    fail_bucket : str
        The name of the bucket for files that fail validation.
    source_bucket : str
        The name of the bucket that contains the file being validated.
    """

    def __init__(
        self,
        key: str,
        size: int,
        pass_bucket: str,
        fail_bucket: str,
        source_bucket: str,
    ):
        """
        Parameters
        ----------
        key : str
            The AWS S3 key of the file being validated.
        size : int
            The size of the file being validated.
        pass_bucket : str
            The name of the bucket for files that pass validation.
        fail_bucket : str
            The name of the bucket for files that fail validation.
        source_bucket : str
            The name of the bucket that contains the file being validated.
        """
        self.key = key
        self.size = size
        self.fail_bucket = fail_bucket
        self.pass_bucket = pass_bucket
        self.source_bucket = source_bucket
        self.errors = []

    def _add_error(self, error: str):
        """Collects and aggregates error messges into a list.
        Parameters
        ----------
        error : str
            An error message
        """
        if error not in self.errors:
            self.errors.append(error)

    def _validate_file(self, key, size):
        """
        Parameters
        ----------
        key : str
            The AWS S3 key of the file being validated.
        size : int
            The size of the file being validated.
        """
        if validate_folder_structure(self.key) is not True:
            self._add_error(error=f"'{self.key}' Folder structure is invalid")
        elif self.size < 1:
            self._add_error(error=f"'{self.key}' File has no content")
            print(self.key, self.size)

    def execute(self):
        self._validate_file(self.key, self.size)
        if len(self.errors) > 0:
            move_object(
                destination_bucket=self.fail_bucket,
                source_bucket=self.source_bucket,
                source_key=self.key,
            )
            return {"validation_outcome": "Fail"}
        else:
            move_object(
                destination_bucket=self.pass_bucket,
                source_bucket=self.source_bucket,
                source_key=self.key,
            )
            return {"validation_outcome": "Pass"}


def handler(event, context):

    if event.get("scheduled_event"):
        source_bucket = os.environ["SOURCE_BUCKET"]
        paginator = client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=source_bucket)
        for page in pages:
            for obj in page["Contents"]:
                pass_bucket = os.environ["PASS_BUCKET"]
                fail_bucket = os.environ["FAIL_BUCKET"]
                key = obj["Key"]
                size = obj["Size"]

                fileValidator = FileValidator(
                    key=key,
                    size=size,
                    pass_bucket=pass_bucket,
                    fail_bucket=fail_bucket,
                    source_bucket=source_bucket,
                )

                fileValidator.execute()

    elif event.get("Records"):
        for record in event["Records"]:
            source_bucket = record["s3"]["bucket"]["name"]
            pass_bucket = os.environ["PASS_BUCKET"]
            fail_bucket = os.environ["FAIL_BUCKET"]
            key = unquote_plus(record["s3"]["object"]["key"])
            size = record["s3"]["object"]["size"]

            fileValidator = FileValidator(
                key=key,
                size=size,
                pass_bucket=pass_bucket,
                fail_bucket=fail_bucket,
                source_bucket=source_bucket,
            )

            fileValidator.execute()

    else:
        raise KeyError
