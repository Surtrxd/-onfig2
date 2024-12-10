import subprocess
import os


def visualize_with_plantuml(plantuml_path: str, uml_file: str, output_image: str):
    """
    Визуализирует граф с помощью PlantUML.

    :param plantuml_path: Путь к JAR-файлу PlantUML.
    :param uml_file: Путь к файлу .uml.
    :param output_image: Путь к выходному изображению (.png).
    """
    if not os.path.exists(plantuml_path):
        raise FileNotFoundError(f"PlantUML JAR файл {plantuml_path} не найден.")

    subprocess.run(
        ['java', '-jar', plantuml_path, '-tpng', uml_file, '-o', os.path.dirname(output_image)],
        check=True
    )
