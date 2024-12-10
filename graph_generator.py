def generate_plantuml_graph(dependencies: dict, output_file: str):
    """
    Генерирует описание графа зависимостей в формате PlantUML.

    :param dependencies: Словарь зависимостей {пакет: {зависимости}}.
    :param output_file: Путь к выходному файлу (.uml).
    """
    with open(output_file, "w") as f:
        f.write("@startuml\n")
        f.write("skinparam packageStyle rectangle\n")

        # Объявляем узлы как прямоугольники
        for package in dependencies:
            f.write(f'rectangle "{package}" as {package.replace(":", "_")}\n')

        # Генерируем связи между узлами
        for package, deps in dependencies.items():
            for dep in deps:
                f.write(f'{package.replace(":", "_")} --> {dep.replace(":", "_")}\n')

        f.write("@enduml\n")
