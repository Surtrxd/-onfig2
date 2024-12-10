import xml.etree.ElementTree as ET
import requests


def analyze_dependencies(pom_file: str) -> dict:
    """
    Анализирует зависимости Maven-пакета из файла pom.xml, включая транзитивные зависимости через HTTP-запросы.

    :param pom_file: Путь к основному файлу pom.xml.
    :return: Словарь зависимостей {пакет: {зависимости}}.
    """
    dependencies = {}
    processed = set()

    def fetch_pom(group_id: str, artifact_id: str, version: str) -> str:
        """
        Загружает pom.xml зависимости из Maven Central Repository.

        :param group_id: Идентификатор группы (groupId).
        :param artifact_id: Артефакт (artifactId).
        :param version: Версия зависимости.
        :return: Содержимое pom.xml в виде строки.
        """
        base_url = "https://repo1.maven.org/maven2"
        pom_url = f"{base_url}/{group_id.replace('.', '/')}/{artifact_id}/{version}/{artifact_id}-{version}.pom"
        response = requests.get(pom_url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Не удалось загрузить pom.xml по адресу {pom_url}")
            return None

    def parse_pom(file_content, is_remote=False):
        """
        Парсит pom.xml и добавляет зависимости в граф.

        :param file_content: Содержимое pom.xml (строка или путь к файлу).
        :param is_remote: Указывает, является ли содержимое строкой (True) или локальным файлом (False).
        """
        if file_content in processed:
            return
        processed.add(file_content)

        if is_remote:
            root = ET.fromstring(file_content)
        else:
            tree = ET.parse(file_content)
            root = tree.getroot()

        for dependency in root.findall(".//dependency"):
            group_id = dependency.find("groupId").text
            artifact_id = dependency.find("artifactId").text
            version = dependency.find("version").text
            package_name = f"{group_id}:{artifact_id}"

            if package_name not in dependencies:
                dependencies[package_name] = set()

            if version:
                remote_pom = fetch_pom(group_id, artifact_id, version)
                if remote_pom:
                    parse_pom(remote_pom, is_remote=True)
                    # Добавляем транзитивные зависимости текущему пакету
                    dependencies[package_name].update(dependencies.keys())



    parse_pom(pom_file)
    return dependencies
