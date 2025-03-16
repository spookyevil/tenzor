import os
import zipfile
import logging
from datetime import datetime
from git import Repo

# Настройка логгера
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def create_version_file(version, files_list, path_to_src_dir):
    """
    Создает служебный файл version.json с информацией о версиях и списке файлов.
    :param version: Версия продукта.
    :param files_list: Список файлов в каталоге.
    :param path_to_src_dir: Путь к каталогу с исходниками.
    """
    version_data = {
        "name": "hello world",
        "version": version,
        "files": files_list
    }
    with open(os.path.join(path_to_src_dir, 'version.json'), 'w') as f:
        f.write(str(version_data))

def filter_files(file_extensions, directory_path):
    """
    Возвращает список файлов с заданными расширениями из указанного каталога.
    :param file_extensions: Расширения файлов, которые нужно включить.
    :param directory_path: Путь к каталогу.
    """
    filtered_files = []
    for root, _, files in os.walk(directory_path):
        for filename in files:
            ext = os.path.splitext(filename)[1]
            if ext.lower() in file_extensions:
                filtered_files.append(os.path.relpath(os.path.join(root, filename), directory_path))
    return filtered_files

def clean_directory(repo_root, keep_paths):
    """
    Удаляет все директории в корневом каталоге, кроме указанных в параметре keep_paths.
    :param repo_root: Корневой каталог репозитория.
    :param keep_paths: Пути к каталогам, которые нужно оставить.
    """
    for dirpath, dirnames, filenames in os.walk(repo_root):
        if not any([dirpath.startswith(os.path.join(repo_root, x)) for x in keep_paths]):
            logging.info(f"Удаляю директорию: {dirpath}")
            shutil.rmtree(dirpath)

def archive_directory(src_dir, archive_name):
    """
    Упаковывает содержимое указанной директории в ZIP-архив.
    :param src_dir: Директория, которую нужно упаковать.
    :param archive_name: Имя создаваемого архива.
    """
    logging.info(f"Паковка содержимого {src_dir} в архив {archive_name}.zip...")
    with zipfile.ZipFile(archive_name + '.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, src_dir)
                zf.write(full_path, arcname=rel_path)
    logging.info(f"Архив {archive_name}.zip успешно создан!")

def main(repo_url, relative_src_path, version):
    """
    Основной метод для сборки проекта.
    :param repo_url: Адрес репозитория.
    :param relative_src_path: Относительный путь до директории с исходниками.
    :param version: Версия продукта.
    """
    # Клонируем репозиторий
    repo_name = os.path.basename(repo_url)
    repo_root = os.path.join('.', repo_name)
    logging.info(f"Клонирование репозитория {repo_url} в директорию {repo_root}...")
    Repo.clone_from(repo_url, repo_root)

    # Определяем путь к директории с исходниками
    src_dir = os.path.join(repo_root, relative_src_path)
    logging.info(f"Директория с исходниками: {src_dir}")

    # Удаляем все директории, кроме директории с исходниками
    clean_directory(repo_root, [relative_src_path])

    # Собираем список файлов с нужными расширениями
    file_extensions = ['.py', '.js', '.sh']
    files_list = filter_files(file_extensions, src_dir)
    logging.info(f"Список файлов: {files_list}")

    # Создаем служебный файл version.json
    create_version_file(version, files_list, src_dir)

    # Формируем имя архива
    now = datetime.now().strftime("%Y%m%d")
    last_part_of_src_dir = os.path.basename(relative_src_path)
    archive_name = f"{last_part_of_src_dir}{now}"

    # Упаковка в архив
    archive_directory(src_dir, archive_name)

    # Завершение работы
    logging.info("Сборка выполнена успешно!")

if __name__ == '__main__':
    # Параметры
    repo_url = "https://github.com/paulbouwer/hello-kubernetes.git"
    relative_src_path = "src/app"
    version = "25.3000"

    # Запуск основной функции
    main(repo_url, relative_src_path, version)
