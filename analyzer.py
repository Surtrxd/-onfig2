import xml.etree.ElementTree as ET
import os


def analyze_dependencies(pom_file: str, base_path: str) -> dict:
    """
    Анализирует зависимости Maven-пакета из файла pom.xml, включая транзитивные зависимости.

    :param pom_file: Путь к файлу pom.xml.
    :param base_path: Базовый путь для поиска других pom.xml файлов.
    :return: Словарь зависимостей {пакет: {зависимости}}.
    """
    if not os.path.exists(pom_file):
        raise FileNotFoundError(f"Файл {pom_file} не найден.")

    dependencies = {}
    processed_files = set()

    def parse_pom(file_path):
        """
        Рекурсивно анализирует pom.xml и его зависимости.
        """
        if file_path in processed_files:  # Избегаем циклов
            return
        processed_files.add(file_path)

        tree = ET.parse(file_path)
        root = tree.getroot()

        # Извлечение зависимостей
        for dependency in root.findall(".//dependency"):
            group_id = dependency.find("groupId").text
            artifact_id = dependency.find("artifactId").text
            package_name = f"{group_id}:{artifact_id}"

            # Добавляем зависимость в словарь
            if package_name not in dependencies:
                dependencies[package_name] = set()

            # Попробуем найти pom.xml для этой зависимости
            dependency_pom = os.path.join(base_path, package_name.replace(":", "/"), "pom.xml")
            if os.path.exists(dependency_pom):
                parse_pom(dependency_pom)  # Рекурсивно анализируем

                # Добавляем транзитивные зависимости
                dependencies[package_name].update(dependencies.keys())

    # Начинаем анализ с основного файла
    parse_pom(pom_file)

    return dependencies
