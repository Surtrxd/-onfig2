import os
from graph_generator import generate_plantuml_graph

def test_generate_plantuml_graph():
    # Зависимости для теста
    dependencies = {
        "org.apache.commons:commons-lang3": set(),
        "com.google.guava:guava": {"org.apache.commons:commons-lang3"}
    }

    # Генерируем файл UML
    uml_file = "test_output.uml"
    generate_plantuml_graph(dependencies, uml_file)

    # Проверяем содержимое файла
    with open(uml_file, "r") as f:
        content = f.read()

    assert "@startuml" in content
    assert "org_apache_commons_commons_lang3" in content
    assert "com_google_guava_guava" in content
    assert "com_google_guava_guava --> org_apache_commons_commons_lang3" in content

    # Удаляем временный файл
    os.remove(uml_file)
