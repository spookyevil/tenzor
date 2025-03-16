import json
import re
from itertools import product

def parse_template(template):
    """Парсинг шаблона версии"""
    parts = template.split('.')
    digits = []
    for part in parts:
        if '*' in part:
            # Генерация двух вариантов чисел для каждой звезды (*)
            variants = [int(part.replace('*', '0')), int(part.replace('*', '9'))]
        else:
            variants = [int(part)]
        digits.append(variants)
    return digits

def generate_versions(digits):
    """Генерация всех комбинаций версий на основе парсинга шаблона"""
    versions = []
    for combination in product(*digits):
        version = '.'.join(map(str, combination))
        versions.append(version)
    return versions

def load_config(config_file):
    """Загрузка конфигурации из файла"""
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

def process_templates(config, input_version):
    """Основная логика обработки шаблонов"""
    all_versions = []
    templates = config.items()
    for key, value in templates:
        digits = parse_template(value)
        generated_versions = generate_versions(digits)
        all_versions.extend(generated_versions)
    
    # Сортируем все версии
    sorted_versions = sorted(all_versions)
    
    # Найдем индекс версии из параметров запуска
    index = None
    for idx, ver in enumerate(sorted_versions):
        if ver == input_version:
            index = idx
            break
    
    # Выведем версии старше заданной
    older_versions = sorted_versions[:index]
    
    return sorted_versions, older_versions

def main(input_version, config_file):
    # Загружаем конфигурацию
    config = load_config(config_file)
    
    # Обрабатываем шаблоны и получаем версии
    sorted_versions, older_versions = process_templates(config, input_version)
    
    # Выводим отсортированные версии
    print("\nОтсортированный список всех версий:")
    for version in sorted_versions:
        print(version)
    
    # Выводим версии младше заданной
    print("\nСписок версий младше (старше) версии из параметров запуска:")
    for version in older_versions:
        print(version)

if __name__ == "__main__":
    # Пример использования
    input_version = "3.7.3"
    config_file = "config.json"
    main(input_version, config_file)
