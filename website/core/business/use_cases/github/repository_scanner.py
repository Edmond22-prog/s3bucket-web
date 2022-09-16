import logging
from typing import Optional, List

import environ
from github import Github
from github.ContentFile import ContentFile

from website.core.business.interface.irepository import IRepository
from website.core.business.interface.ivulnerability import IVulnerability
from website.core.business.entities import RepositoryEntity, VulnerabilityEntity
from website.core.business.interface.iscrapping import IScrapping

logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)

env = environ.Env()
environ.Env.read_env()


class RepositoryScanner(IScrapping):
    def __init__(self, repository: str):
        self._repository_name = ""
        self._clean_value(repository)
        self._vulnerabilities: List[IVulnerability] = []

    def _clean_value(self, repository):
        if repository.startswith("https://github.com/"):
            self._repository_name = repository.lstrip("https://github.com/")

        elif "/" in repository:
            self._repository_name = repository

        else:
            self._repository_name = None

    def run(self) -> Optional[RepositoryEntity]:
        if self._repository_name is None:
            logging.error("Invalide repository name")
            return None

        github = Github(env("GITHUB_TOKEN"))

        try:
            repository = github.get_repo(self._repository_name)
            repository_entity = RepositoryEntity.factory(
                name=repository.name,
                owner=repository.owner.login,
                url=repository.html_url,
                created_at=repository.created_at,
                updated_at=repository.updated_at,
                languages=repository.get_languages(),
            )

            logging.info(f"REPOSITORY NAME: {repository_entity.name}")
            logging.info(f"REPOSITORY OWNER: {repository_entity.owner}")
            logging.info(f"REPOSITORY URL: {repository_entity.url}")
            logging.info(f"REPOSITORY CREATED AT: {repository_entity.created_at}")
            logging.info(f"REPOSITORY UPDATED AT: {repository_entity.updated_at}")
            logging.info(f"REPOSITORY LANGUAGES: {repository_entity.languages}")
            logging.info("REPOSITORY CONTENTS FILES:\n")
            contents = repository.get_contents("")
            while contents:
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(repository.get_contents(file_content.path))
                else:
                    if not file_content.name.endswith(("png", "jpg", "jpeg", "gif", "svg")):
                        logging.info(file_content.name)
                        if ".env" == file_content.name:
                            logging.warning(f"File <{file_content.name}> found in {file_content.path}")
                            vulnerability_entity = VulnerabilityEntity.factory(
                                name="File .env found",
                                location=file_content.path,
                                code_line=0,
                                code_vulnerability="",
                            )
                            self._vulnerabilities.append(vulnerability_entity)
                            repository_entity.vulnerabilities = self._vulnerabilities

                        self._scan_file(file_content, repository_entity)

            return repository_entity

        except Exception:
            logging.error("Repository not found")
            return None

    def _scan_file(self, file_content: ContentFile, repos: IRepository) -> None:
        logging.info(f":::: Scanning <{file_content.name}> file ::::")
        line = 0
        try:
            for data in file_content.decoded_content.decode().splitlines():
                line += 1
                # # Verify if the file contains a password
                self._search_password(file_content, line, data, repos)

                # # Verify if the file contains a secret key
                self._search_secret_key(file_content, line, data, repos)

                # # Verify if the file contains access key
                self._search_access_key(file_content, line, data, repos)

                # # Verify if the file contains a token
                self._search_token(file_content, line, data, repos)

        except UnicodeDecodeError:
            logging.warning(f"Can't decode file <{file_content.name}>")

        except Exception as e:
            logging.error(f"Error: {e}")

        logging.info(f"End of the scan of <{file_content.name}> file.\n")

    def _search_password(self, file, code_line, data, repository):
        if 'password="' in data.lower() or 'password = "' in data.lower():
            # # Verify if it's not a comment
            # if "#" not in data.lower() and "//" not in data.lower():
            #     logging.warning(f"PASSWORD FOUND IN LINE {line}: {data}")
            logging.warning(f"PASSWORD FOUND IN LINE {code_line}: {data}")
            vulnerability_entity = VulnerabilityEntity.factory(
                name="Password found",
                location=file.path,
                code_line=code_line,
                code_vulnerability=data,
            )
            self._vulnerabilities.append(vulnerability_entity)
            repository.vulnerabilities = self._vulnerabilities

        if "password='" in data.lower() or "password = '" in data.lower():
            logging.warning(f"PASSWORD FOUND IN LINE {code_line}: {data}")
            vulnerability_entity = VulnerabilityEntity.factory(
                name="Password found",
                location=file.path,
                code_line=code_line,
                code_vulnerability=data,
            )
            self._vulnerabilities.append(vulnerability_entity)
            repository.vulnerabilities = self._vulnerabilities

    def _search_secret_key(self, file, code_line, data, repository):
        if 'secret_key="' in data.lower() or 'secret_key = "' in data.lower():
            # Verify if it's not a comment
            # if "#" not in data.lower() and "//" not in data.lower():
            #     logging.warning(f"SECRET KEY FOUND IN LINE {line}: {data}")
            logging.warning(f"SECRET KEY FOUND IN LINE {code_line}: {data}")
            vulnerability_entity = VulnerabilityEntity.factory(
                name="Secret key found",
                location=file.path,
                code_line=code_line,
                code_vulnerability=data,
            )
            self._vulnerabilities.append(vulnerability_entity)
            repository.vulnerabilities = self._vulnerabilities

        if "secret_key='" in data.lower() or "secret_key = '" in data.lower():
            logging.warning(f"SECRET KEY FOUND IN LINE {code_line}: {data}")
            vulnerability_entity = VulnerabilityEntity.factory(
                name="Secret key found",
                location=file.path,
                code_line=code_line,
                code_vulnerability=data,
            )
            self._vulnerabilities.append(vulnerability_entity)
            repository.vulnerabilities = self._vulnerabilities

    def _search_access_key(self, file, code_line, data, repository):
        if 'access_key="' in data.lower() or 'access_key = "' in data.lower():
            # Verify if it's not a comment
            # if "#" not in data.lower() and "//" not in data.lower():
            #     logging.warning(f"ACCESS KEY FOUND IN LINE {line}: {data}")
            logging.warning(f"ACCESS KEY FOUND IN LINE {code_line}: {data}")
            vulnerability_entity = VulnerabilityEntity.factory(
                name="Access key found",
                location=file.path,
                code_line=code_line,
                code_vulnerability=data,
            )
            self._vulnerabilities.append(vulnerability_entity)
            repository.vulnerabilities = self._vulnerabilities

        if "access_key='" in data.lower() or "access_key = '" in data.lower():
            logging.warning(f"ACCESS KEY FOUND IN LINE {code_line}: {data}")
            vulnerability_entity = VulnerabilityEntity.factory(
                name="Access key found",
                location=file.path,
                code_line=code_line,
                code_vulnerability=data,
            )
            self._vulnerabilities.append(vulnerability_entity)
            repository.vulnerabilities = self._vulnerabilities

    def _search_token(self, file, code_line, data, repository):
        if 'token="' in data.lower() or 'token = "' in data.lower():
            # Verify if it's not a comment
            # if "#" not in data.lower() and "//" not in data.lower():
            #     logging.warning(f"TOKEN FOUND IN LINE {line}: {data}")
            logging.warning(f"TOKEN FOUND IN LINE {code_line}: {data}")
            vulnerability_entity = VulnerabilityEntity.factory(
                name="Token found",
                location=file.path,
                code_line=code_line,
                code_vulnerability=data,
            )
            self._vulnerabilities.append(vulnerability_entity)
            repository.vulnerabilities = self._vulnerabilities

        if "token='" in data.lower() or "token = '" in data.lower():
            logging.warning(f"TOKEN FOUND IN LINE {code_line}: {data}")
            vulnerability_entity = VulnerabilityEntity.factory(
                name="Token found",
                location=file.path,
                code_line=code_line,
                code_vulnerability=data,
            )
            self._vulnerabilities.append(vulnerability_entity)
            repository.vulnerabilities = self._vulnerabilities
