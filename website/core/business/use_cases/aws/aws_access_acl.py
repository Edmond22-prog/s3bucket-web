"""
    Source: https://github.com/nkeumosoft/s3bucket_finder
    From Author: Noutcheu Libert Joran

"""

import logging
import os
from typing import Optional

import environ
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from ....business.entities import AwsBucketEntity
from ....business.exceptions import PermissionException, TypeException

REGIONS_NAME = [
    "us-east-2",
    "us-east-1",
    "us-west-1",
    "us-west-2",
    "af-south-1",
    "ap-south-1",
    "ap-northeast-3",
    "ap-northeast-2",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-northeast-1",
    "ca-central-1",
    "eu-central-1",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "eu-south-1",
    "eu-west-3",
    "me-south-1",
    "sa-east-1",
]

env = environ.Env()
environ.Env.read_env()


class AwsAccessAcl(object):
    def __init__(self, bucket: AwsBucketEntity, client: BaseClient):
        self._bucket = bucket
        # self._aws_settings = settings
        self._aws_client = client
        # self._indice_region = -1
        # self._initial_region = env("AWS_DEFAULT_REGION")

    def __exit__(self, exception_type, exception_value, traceback):
        os.environ.pop("AWS_DEFAULT_REGION")

    def get_bucket_acl(self, indice_region=-1) -> AwsBucketEntity:
        try:
            responses_of_read_acl = self._check_read_acl_permissions(self._bucket)
            if responses_of_read_acl is not None:
                if responses_of_read_acl["permission"] == PermissionException.ACCESS_DENIED:
                    acl: dict = {"Grants": {}}

                    self._bucket.properties = self._bucket_human_read_acl(acl, PermissionException.ACCESS_DENIED)

                elif responses_of_read_acl["permission"] == PermissionException.LIST_BUCKET_RESULT:
                    self._bucket.properties = self._bucket_human_read_acl(
                        responses_of_read_acl["acl_property"],
                        PermissionException.LIST_BUCKET_RESULT,
                    )

                else:
                    # If the access it is not allow or denied
                    # Then  the region  is not good, and we change it
                    indice_region += 1
                    if indice_region <= len(REGIONS_NAME) - 1:
                        os.environ["AWS_DEFAULT_REGION"] = REGIONS_NAME[indice_region]
                        self.get_bucket_acl(indice_region)

        except ClientError as aws_error:
            logging.error(aws_error)

        return self._bucket

    def _check_read_acl_permissions(self, bucket: AwsBucketEntity) -> Optional[dict]:
        s3_client = self._aws_client
        acl_permission_response = {}

        if self._check_head_bucket(bucket):
            try:
                acl_properties = s3_client.get_bucket_acl(Bucket=bucket.name)
                acl_permission_response = {
                    "permission": PermissionException.LIST_BUCKET_RESULT,
                    "acl_property": acl_properties,
                }

                return acl_permission_response

            except ClientError as aws_error:
                aws_resp = aws_error.response

                if aws_resp["Error"]["Code"] == "AccessDenied" or aws_resp["Error"]["Code"] == "AllAccessDisabled":
                    acl_permission_response["permission"] = PermissionException.ACCESS_DENIED

                elif aws_resp.get("Error").get("Code") == TypeException.ILLEGAL_LOCATION:
                    acl_permission_response["permission"] = "LocationConstraintException"

            return acl_permission_response

        return None

    def _check_head_bucket(self, bucket: AwsBucketEntity) -> bool:
        try:
            if not isinstance(bucket, AwsBucketEntity):
                raise ValueError("You must send a bucket object")

            self._aws_client.head_bucket(Bucket=bucket.name)

        except ClientError as error:
            resp_error = error.response
            if resp_error.get("Error").get("Code") == "404":
                logging.error("Bucket not %s found", bucket.name)
                return False

        except ValueError:
            logging.error("You must send a bucket object")
            exit(0)

        return True

    def _bucket_human_read_acl(self, acl_property: dict, access=PermissionException.LIST_BUCKET_RESULT):
        result_permissions = {
            "Owner_ID": "",
            "private-acl": False,
            "public-read": False,
            "public-write": False,
            "public-read-write": False,
            "public-read-acp": False,
            "public-write-acp": False,
            "aws-exec-read": False,
            "authenticated-read": False,
            "log-delivery-write": False,
        }

        # Check if the bucket is private
        if len(acl_property["Grants"]) == 1 or access == PermissionException.ACCESS_DENIED:
            result_permissions["private-acl"] = True
            return result_permissions

        # For any element in grant, check if bucket acl is
        # public-read | public read and write | user authentication
        for grant in acl_property["Grants"]:
            try:
                if grant.get("Grantee").get("Type") == "Group":
                    result_permissions = self._display_acl_properties(grant, result_permissions)

            except KeyError:
                pass

        if acl_property is not None:
            result_permissions["Owner_ID"] = acl_property["Owner"]["ID"]

        return result_permissions

    def _display_acl_properties(self, grant: dict, result_permissions: dict) -> dict:
        if grant is not None:
            acl_property_url = grant["Grantee"]["URI"]
            if acl_property_url == "http://acs.amazonaws.com/groups/global/AllUsers":
                result_permissions = self._access_control_unauthenticated_user(result_permissions, grant)

            result_permissions["authenticated-read"] = (
                acl_property_url == "http://acs.amazonaws.com/groups/global/AuthenticatedUsers"
            )
            result_permissions["log-delivery-write"] = (
                acl_property_url == "http://acs.amazonaws.com/groups/s3/LogDelivery"
            )

        return result_permissions

    @staticmethod
    def _access_control_unauthenticated_user(result_permissions: dict, permission: dict) -> dict:
        result_permissions["public-read-write"] = permission["Permission"] == "FULL_CONTROL"
        result_permissions["public-read"] = permission["Permission"] == "READ"
        result_permissions["public-read-acp"] = permission["Permission"] == "READ_ACP"
        result_permissions["public-write"] = permission["Permission"] == "WRITE"
        result_permissions["public-write-acp"] = permission["Permission"] == "WRITE_ACP"

        return result_permissions
