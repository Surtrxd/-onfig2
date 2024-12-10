import os
from analyzer import analyze_dependencies

def test_analyze_dependencies():
    # Создаем тестовый pom.xml
    pom_content = """<project>
        <modelVersion>4.0.0</modelVersion>
        <groupId>com.example</groupId>
        <artifactId>sample-project</artifactId>
        <version>1.0-SNAPSHOT</version>
        <dependencies>
            <dependency>
                <groupId>org.apache.commons</groupId>
                <artifactId>commons-lang3</artifactId>
                <version>3.12.0</version>
            </dependency>
            <dependency>
                <groupId>com.google.guava</groupId>
                <artifactId>guava</artifactId>
                <version>31.1-jre</version>
            </dependency>
        </dependencies>
    </project>"""

    # Сохраняем временный файл
    pom_file = "test_pom.xml"
    with open(pom_file, "w") as f:
        f.write(pom_content)

    # Анализируем зависимости
    dependencies = analyze_dependencies(pom_file)

    # Проверяем результат
    assert "org.apache.commons:commons-lang3" in dependencies
    assert "com.google.guava:guava" in dependencies
    assert dependencies["com.google.guava:guava"] == {"org.apache.commons:commons-lang3"}

    # Удаляем временный файл
    os.remove(pom_file)
