import re
from logging import getLogger
from os import listdir, path, remove, walk
from os.path import isfile, join
from re import compile


class FileRemover:
    @classmethod
    def get_files_list(cls, src_path: str) -> list[str]:
        """Walk through path folder and clean files names from type."""
        logger = getLogger()
        if not path.isdir(src_path):
            logger.info('Указанный путь не является директорией')
            return []
        return [f for f in listdir(src_path) if isfile(join(src_path, f))]

    @classmethod
    def extension_cleaner(cls, files_list: list[str], file_type: str) -> list[str]:
        type_pat = compile('\.' + file_type + '$', flags=re.IGNORECASE)
        return [type_pat.sub('', f_name) for f_name in files_list if type_pat.search(f_name)]

    @classmethod
    def list_difference(cls, files_to_remove: list[str], files_to_exclude: list[str]) -> set[str]:
        return set(files_to_remove) - set(files_to_exclude)

    @classmethod
    def files_remover(cls, origin_dir: str, to_remove_dir: str,
                      origin_ext: str = None, to_remove_ext: str = None) -> None:
        origin_list = cls.get_files_list(origin_dir)
        remove_list = cls.get_files_list(to_remove_dir)
        diff = cls.list_difference(cls.extension_cleaner(remove_list, to_remove_ext),
                                   cls.extension_cleaner(origin_list, origin_ext))
        print(f'Подтвердите удаление {len(diff)} файлов из папки {to_remove_dir}')
        if input() != 'y':
            return
        for f_name in diff:
            file_path = path.join(to_remove_dir, f_name + '.' + to_remove_ext)
            if isfile(file_path):
                remove(file_path)

    @classmethod
    def get_max_files_size(cls, path_dir: str, from_size: int):
        total_size = 0
        for i in walk(path_dir):
            for f in i[2]:
                fp = path.join(i[0], f)
                size = path.getsize(fp) / 1024 / 1024
                if size > from_size:
                    total_size += size
                    print(fp, size)
        print(total_size)


if __name__ == '__main__':
    origin_files = r'/Users/a.gumerov/Pictures/JPEG/2022 Авто'
    files_to_remove = r'/Users/a.gumerov/Pictures/RAW/2022 Авто'
    FileRemover.files_remover(origin_files, files_to_remove, 'jpg', 'orf')
    print('Done')
