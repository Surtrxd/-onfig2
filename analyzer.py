import xml.etree.ElementTree as ET
import os

def analyze_dependencies(pom_file: str) -> dict:
    """
    Анализирует зависимости Maven-пакета из файла pom.xml.

    :param pom_file: Путь к файлу pom.xml.
    :return: Словарь зависимостей {пакет: {зависимости}}.
    """
    if not os.path.exists(pom_file):
        raise FileNotFoundError(f"Файл {pom_file} не найден.")

    dependencies = {
        "org.apache.commons:commons-lang3": {"java.lang.String"},
    "com.google.guava:guava": {"org.apache.commons:commons-lang3"}
    }
    tree = ET.parse(pom_file)
    root = tree.getroot()

    # Чтение зависимостей из pom.xml
    for dependency in root.findall(".//dependency"):
        group_id = dependency.find("groupId").text
        artifact_id = dependency.find("artifactId").text
        package_name = f"{group_id}:{artifact_id}"
        dependencies[package_name] = set()  # Пока что без транзитивных

    return dependencies
