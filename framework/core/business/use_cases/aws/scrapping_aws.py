import logging
from typing import Any, Optional

import requests
import xmltodict
from requests import HTTPError, Timeout, RequestException

from core.business.entities import AwsBucketEntity
from core.business.interface.ibucket import IBucket
from core.business.interface.iscrapping import IScrapping


logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)


class ScrappingAws(IScrapping):
    def __init__(self, value: str):
        self._bucket_name: Optional[str] = None
        self._clean_value(value)

    def _clean_value(self, value: str) -> None:
        if value.startswith("http://") or value.startswith("https://"):
            values = value.split("//")
            if values[1].endswith(".amazonaws.com"):
                rest = values[1].rstrip(".amazonaws.com")
                self._bucket_name = rest.split(".s3")[0]

        else:
            self._bucket_name = value

    def run(self) -> IBucket:
        if self._bucket_name is None:
            return None

        try:
            response = requests.get(f"https://{self._bucket_name}.s3.amazonaws.com")

            if response.status_code == 200:
                return self._is_status_200("US", f"https://{self._bucket_name}.s3.amazonaws.com")

            data = xmltodict.parse(response.content)

            if response.status_code in (400, 403, 404):
                if response.status_code == 400:
                    return self._is_status_400(data)

                elif response.status_code == 403:
                    return self._is_status_403("US", f"https://{self._bucket_name}.s3.amazonaws.com")

                else:
                    logging.info(f"Bucket <{self._bucket_name}> || Don't Exist")
                    return None

            if response.status_code == 301:
                return self._is_status_301(data)

        except ConnectionError:
            logging.warning(
                f"Connection error exception for the scan of "
                f"bucket <{self._bucket_name}> (status=301)."
                f"Check your connexion and restart."
            )

        except HTTPError:
            logging.warning(
                f"Http error exception for the scan of "
                f"bucket <{self._bucket_name}> (status=301)."
                f"Check your connexion and restart."
            )

        except Timeout:
            logging.warning(
                f"Timeout exception for the scan of "
                f"bucket <{self._bucket_name}> (status=301)."
                f"Check your connexion and restart."
            )

        except RequestException:
            logging.warning(
                f"Request exception for the scan of "
                f"bucket <{self._bucket_name}> (status=301)."
                f"Check your connexion and restart."
            )

    def _is_status_200(self, location: str, endpoint: str) -> IBucket:
        bucket = AwsBucketEntity.factory(self._bucket_name, "Public", endpoint, location)
        logging.info(bucket)
        return bucket

    def _is_status_403(self, location: str, endpoint: str) -> IBucket:
        bucket = AwsBucketEntity.factory(self._bucket_name, "Private", endpoint, location)
        logging.info(bucket)
        return bucket

    def _is_status_301(self, data: Any) -> IBucket:
        endpoint = data["Error"]["Endpoint"]
        try:
            response = requests.get(f"https://{endpoint}")

            if response.status_code == 200:
                return self._is_status_200("US", f"https://{endpoint}")

            else:
                return self._is_status_403("US", f"https://{endpoint}")

        except ConnectionError:
            logging.warning(
                f"Connection error exception for the scan of "
                f"bucket <{self._bucket_name}> (status=301)."
                f"Check your connexion and restart."
            )

        except HTTPError:
            logging.warning(
                f"Http error exception for the scan of "
                f"bucket <{self._bucket_name}> (status=301)."
                f"Check your connexion and restart."
            )

        except Timeout:
            logging.warning(
                f"Timeout exception for the scan of "
                f"bucket <{self._bucket_name}> (status=301)."
                f"Check your connexion and restart."
            )

        except RequestException:
            logging.warning(
                f"Request exception for the scan of "
                f"bucket <{self._bucket_name}> (status=301)."
                f"Check your connexion and restart."
            )

    def _is_status_400(self, data: Any) -> IBucket:
        error = data["Error"]
        if error["Code"] == "IllegalLocationConstraintException":
            location = error["Message"].split(" ")[1]
            url = f"https://{self._bucket_name}.s3.{location}.amazonaws.com"
            try:
                response = requests.get(url)

                if response.status_code == 200:
                    return self._is_status_200(location, url)

                else:
                    return self._is_status_403(location, url)

            except ConnectionError:
                logging.warning(
                    f"Connection error exception for the scan of "
                    f"bucket <{self._bucket_name}> (status=301)."
                    f"Check your connexion and restart."
                )

            except HTTPError:
                logging.warning(
                    f"Http error exception for the scan of "
                    f"bucket <{self._bucket_name}> (status=301)."
                    f"Check your connexion and restart."
                )

            except Timeout:
                logging.warning(
                    f"Timeout exception for the scan of "
                    f"bucket <{self._bucket_name}> (status=301)."
                    f"Check your connexion and restart."
                )

            except RequestException:
                logging.warning(
                    f"Request exception for the scan of "
                    f"bucket <{self._bucket_name}> (status=301)."
                    f"Check your connexion and restart."
                )

        else:
            logging.error(f"Invalid bucket name <{self._bucket_name}>")
            return None
