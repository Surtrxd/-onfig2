import argparse
import os
from analyzer import analyze_dependencies
from graph_generator import generate_plantuml_graph
from visualizer import visualize_with_plantuml

def main():
    parser = argparse.ArgumentParser(description="Инструмент для анализа Maven-зависимостей.")
    parser.add_argument("--plantuml-path", required=True, help="Путь к JAR-файлу PlantUML.")
    parser.add_argument("--pom-file", required=True, help="Путь к pom.xml.")
    parser.add_argument("--output-file", required=True, help="Путь для сохранения графа (.png).")
    args = parser.parse_args()

    if not os.path.exists(args.pom_file):
        print(f"Ошибка: файл {args.pom_file} не найден.")
        return

    # Анализ зависимостей
    dependencies = analyze_dependencies(args.pom_file)
    print(f"Словарь зависимостей: {dependencies}")

    # Генерация графа
    uml_file = args.output_file.replace('.png', '.uml')
    generate_plantuml_graph(dependencies, uml_file)

    # Визуализация
    visualize_with_plantuml(args.plantuml_path, uml_file, args.output_file)
    print("Граф зависимостей успешно создан:", args.output_file)

if __name__ == "__main__":
    main()
