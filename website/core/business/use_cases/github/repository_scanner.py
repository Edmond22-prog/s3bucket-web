import logging

import environ
from github import Github

from core.business.interface.iscrapping import IScrapping

logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)

env = environ.Env()
environ.Env.read_env()


class RepositoryScanner(IScrapping):
    def __init__(self, repository: str):
        self._repository_name = ""
        self._clean_value(repository)

    def _clean_value(self, repository):
        if repository.startswith("https://github.com/"):
            self._repository_name = repository.lstrip("https://github.com/")

        elif "/" in repository:
            self._repository_name = repository

        else:
            self._repository_name = None

    def run(self):
        if self._repository_name is None:
            logging.error("Invalide repository name")

        github = Github(env("GITHUB_TOKEN"))
        repository = github.get_repo(self._repository_name)

        logging.info(f"REPOSITORY NAME: {repository.name}")
        logging.info(f"REPOSITORY DESCRIPTION: {repository.description}")
        logging.info(f"REPOSITORY URL: {repository.html_url}")
        logging.info(f"REPOSITORY CREATED AT: {repository.created_at}")
        logging.info(f"REPOSITORY UPDATED AT: {repository.updated_at}")
        logging.info(f"REPOSITORY LANGUAGES: {repository.get_languages()}")
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
                    self._scan_file(file_content)

    @staticmethod
    def _scan_file(file_content):
        logging.info(f":::: Scanning <{file_content.name}> file ::::")
        line = 0
        try:
            for data in file_content.decoded_content.decode().splitlines():
                line += 1
                # # Verify if the file contains a password
                if 'password="' in data.lower() or 'password = "' in data.lower():
                    # # Verify if it's not a comment
                    # if "#" not in data.lower() and "//" not in data.lower():
                    #     logging.warning(f"PASSWORD FOUND IN LINE {line}: {data}")
                    logging.warning(f"PASSWORD FOUND IN LINE {line}: {data}")

                if "password='" in data.lower() or "password = '" in data.lower():
                    logging.warning(f"PASSWORD FOUND IN LINE {line}: {data}")

                # # Verify if the file contains a secret key
                if 'secret_key="' in data.lower() or 'secret_key = "' in data.lower():
                    # Verify if it's not a comment
                    # if "#" not in data.lower() and "//" not in data.lower():
                    #     logging.warning(f"SECRET KEY FOUND IN LINE {line}: {data}")
                    logging.warning(f"SECRET KEY FOUND IN LINE {line}: {data}")

                if "secret_key='" in data.lower() or "secret_key = '" in data.lower():
                    logging.warning(f"SECRET KEY FOUND IN LINE {line}: {data}")

                # # Verify if the file contains access key
                if 'access_key="' in data.lower() or 'access_key = "' in data.lower():
                    # Verify if it's not a comment
                    # if "#" not in data.lower() and "//" not in data.lower():
                    #     logging.warning(f"ACCESS KEY FOUND IN LINE {line}: {data}")
                    logging.warning(f"ACCESS KEY FOUND IN LINE {line}: {data}")

                if "access_key='" in data.lower() or "access_key = '" in data.lower():
                    logging.warning(f"ACCESS KEY FOUND IN LINE {line}: {data}")

                # # Verify if the file contains a token
                if 'token="' in data.lower() or 'token = "' in data.lower():
                    # Verify if it's not a comment
                    # if "#" not in data.lower() and "//" not in data.lower():
                    #     logging.warning(f"TOKEN FOUND IN LINE {line}: {data}")
                    logging.warning(f"TOKEN FOUND IN LINE {line}: {data}")

                if "token='" in data.lower() or "token = '" in data.lower():
                    logging.warning(f"TOKEN FOUND IN LINE {line}: {data}")

        except UnicodeDecodeError:
            logging.warning(f"Can't decode file <{file_content.name}>")

        except Exception as e:
            logging.error(f"Error: {e}")

        logging.info(f"End of the scan of <{file_content.name}> file.\n")


if __name__ == "__main__":
    rs = RepositoryScanner("dilane3/tundah-app")
    rs.run()
