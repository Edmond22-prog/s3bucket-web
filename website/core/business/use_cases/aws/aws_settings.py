import logging
import os
from pathlib import Path
from typing import Optional, Any, Tuple

from website.core.business.interface.isettings import ISettings


class AwsSettings(ISettings):
    def __init__(self, region=None, access_key_id=None, secret_access_key=None, output=None):
        self._region = region
        self._access_key_id = access_key_id
        self._secret_access_key = secret_access_key
        self._output = output

    def get_region(self) -> Optional[str]:
        logging.info("Getting AWS Region")
        status, _path = self._aws_config_file_exist()
        if status:
            with open(_path, "r") as file:
                for line in file.readlines():
                    if "region" in line:
                        self._region = line.split("=")[1].rstrip("\n")
                        return self._region

        return None

    def get_credentials(self) -> Optional[dict]:
        logging.info("Getting AWS Credentials")

        status, _path = self._aws_credentials_file_exist()
        if status:
            with open(_path, "r") as file:
                for line in file.readlines():
                    if "aws_access_key_id" in line:
                        self._access_key_id = line.split("=")[1].rstrip("\n")

                    if "aws_secret_access_key" in line:
                        self._secret_access_key = line.split("=")[1].rstrip("\n")
                return {
                    "access_key_id": self._access_key_id,
                    "secret_access_key": self._secret_access_key,
                }

        return None

    def set_credentials(self, *args) -> None:
        logging.info("Setting AWS Credentials")

        status, _path = self._aws_folder_exist()
        _, file_credentials_path = self._aws_credentials_file_exist()

        if not status:
            os.mkdir(_path)  # aws folder created

        with open(file_credentials_path, "w") as file:
            file.write("[default]\n")
            file.write(f"aws_access_key_id={args[0]}\n")
            file.write(f"aws_secret_access_key={args[1]}\n")

    def get_config(self) -> Optional[dict]:
        logging.info("Getting AWS Configuration")

        status, _path = self._aws_config_file_exist()
        if status:
            with open(_path, "r") as file:
                for line in file.readlines():
                    if "output" in line:
                        self._output = line.split("=")[1].rstrip("\n")

                return {"region": self._region, "output": self._output}

        return None

    def set_config(self, region: str, output="json") -> None:
        logging.info("Setting AWS Configuration")

        statut, _path = self._aws_folder_exist()
        _, file_config_path = self._aws_config_file_exist()

        if not statut:
            os.mkdir(_path)  # aws folder created

        with open(file_config_path, "w") as file:
            file.write("[default]\n")
            file.write(f"region={region}\n")
            file.write(f"output={output}\n")

    @staticmethod
    def _aws_folder_exist() -> Tuple[bool, str]:
        home = Path.home()
        directory_aws = os.path.join(str(home), ".aws/")
        aws_folder = os.path.isdir(directory_aws)
        return aws_folder, directory_aws

    @staticmethod
    def _check_existence(path: str, file: str) -> Tuple[bool, str]:
        file_path = os.path.join(path, file)
        aws_file_exist = Path(file_path).is_file()
        return aws_file_exist, file_path

    def _aws_credentials_file_exist(self) -> Tuple[bool, str]:
        _, _path = self._aws_folder_exist()
        return self._check_existence(_path, "credentials")

    def _aws_config_file_exist(self) -> Tuple[bool, str]:
        _, _path = self._aws_folder_exist()
        return self._check_existence(_path, "config")

    def authentication(self, access_key: str, secret_access_key: str) -> Any:
        ...
