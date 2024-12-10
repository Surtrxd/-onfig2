import xml.etree.ElementTree as ET
import os
import requests

def analyze_dependencies(pom_file: str, base_path: str) -> dict:
    if not os.path.exists(pom_file):
        raise FileNotFoundError(f"Файл {pom_file} не найден.")

    dependencies = {}
    processed_files = set()  # Чтобы не заходить в одни и те же POM по кругу

    # Стек для обхода. Каждый элемент: (источник, содержимое_pom, удалённый_ли_файл)
    # Если удалённый, то content содержит строку с POM, если локальный, то content=None
    stack = [(pom_file, None, False)]

    while stack:
        current_source, content, is_remote = stack.pop()

        # Проверка, чтобы не обрабатывать один и тот же pom более одного раза
        if current_source in processed_files:
            continue
        processed_files.add(current_source)

        # Парсим либо из локального файла, либо из строки
        if is_remote:
            root = ET.fromstring(content)
        else:
            tree = ET.parse(current_source)
            root = tree.getroot()

        # Пытаемся определить версию. Если версия не указана в текущем POM,
        # берём версию из родительского (parent) проекта, если есть.
        version = root.findtext('./version')
        if version is None:
            version = root.findtext('./parent/version')

        # Если версия не найдена, можно либо пропустить, либо задать заглушку.
        if not version:
            version = "latest"

        # Получаем список зависимостей
        for dependency in root.findall(".//dependency"):
            group_id = dependency.find("groupId").text
            artifact_id = dependency.find("artifactId").text
            dep_version = dependency.findtext("version") or version

            package_name = f"{group_id}:{artifact_id}"
            if package_name not in dependencies:
                dependencies[package_name] = set()

            # Формируем URL для удалённого pom
            base_url = "https://repo1.maven.org/maven2"
            pom_url = f"{base_url}/{group_id.replace('.', '/')}/{artifact_id}/{dep_version}/{artifact_id}-{dep_version}.pom"

            # Получаем зависимость по сети, если доступна
            response = requests.get(pom_url)
            if response.status_code == 200:
                stack.append((pom_url, response.text, True))

    return dependencies
