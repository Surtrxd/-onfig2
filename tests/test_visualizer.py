import os
from visualizer import visualize_with_plantuml

def test_visualize_with_plantuml():
    # Подготовка
    plantuml_path = "C:/path/to/plantuml.jar"  # Убедитесь, что путь к JAR-файлу PlantUML верный
    uml_file = "test_output.uml"
    png_file = "test_output.png"

    # Создаем тестовый UML-файл
    with open(uml_file, "w") as f:
        f.write("@startuml\nrectangle Test\n@enduml")

    # Генерация PNG
    visualize_with_plantuml(plantuml_path, uml_file, png_file)

    # Проверяем, что PNG-файл создан
    assert os.path.exists(png_file)

    # Удаляем временные файлы
    os.remove(uml_file)
    os.remove(png_file)
