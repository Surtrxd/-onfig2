def generate_plantuml_graph(dependencies: dict, output_file: str):
    """
    Генерирует описание графа зависимостей в формате PlantUML.

    :param dependencies: Словарь зависимостей {пакет: {зависимости}}.
    :param output_file: Путь к выходному файлу (.uml).
    """
    with open(output_file, "w") as f:
        f.write("@startuml\n")
        f.write("skinparam packageStyle rectangle\n")

        for package in dependencies:
            # Объявляем каждый узел как прямоугольник
            f.write(f'rectangle "{package}" as {package.replace(":", "_").replace("-", "_")}\n')

        for package, deps in dependencies.items():
            for dep in deps:
                # Добавляем стрелки только для различных пакетов
                if package != dep:
                    f.write(f'{package.replace(":", "_").replace("-", "_")} --> {dep.replace(":", "_").replace("-", "_")}\n')

        f.write("@enduml\n")
