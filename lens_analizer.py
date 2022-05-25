from collections import defaultdict
from os import path, walk
from exif import Image


FILES_DATA = defaultdict()


def walk_files(src_dir: str):
    files_list(src_dir)


def files_list(src_dir: str):
    dirs = next(walk(src_dir))[1]
    for folder in dirs:
        folder_path = path.join(src_dir, folder)
        files = next(walk(folder_path))[2]
        for file_path in files:
            with open(file_path, 'rb') as image_file:
                image = Image(image_file)
                if not image.has_exif:
                    print(f'Файл пропущен: {file_path}')
                FILES_DATA.setdefault()

    pass


def save_file_info(file_path: str):
    pass


if __name__ == '__main__':
    file = r'/Users/a.gumerov/Pictures/RAW'

