from logging import getLogger
from os import getcwd, listdir, path, remove, walk
from os.path import isfile, join
from re import IGNORECASE, compile


class FileRemover:
    @classmethod
    def execute(cls):
        files_types = 'jpg orf'
        check_files_types = input(
            f'Форматы файлов для удаления: {files_types}\n'
            'Верно - y,\n'
            'Неверно - <тип отфильтрованных файлов> '
            '<тип неотфильтрованных файлов>\n'
        )
        if check_files_types != 'y':
            if len(check_files_types.split(' ')) == 2:
                files_types = check_files_types
                print(f'Новые типы файлов: {files_types}')
            else:
                print('Необходимо ввести два формата через пробел')
                exit(-1)

        origin_files = getcwd()
        check_origin = input(
            f'Директория с отфильтрованными файлами: {origin_files}\n'
            'Верно - y,\nНеверно - <путь к директории>\n'
        )
        if check_origin != 'y':
            if path.isdir(check_origin):
                origin_files = check_origin
                print(
                    f'Новая директория с отфильтрованными '
                    f'файлами: {check_origin}'
                )
            else:
                print('Указанный путь не является директорией')
                exit(-1)

        files_to_remove = origin_files.lower().replace('jpeg', 'raw')
        check_target = input(
            f'Директория с неотфильтрованными файлами: {files_to_remove}\n'
            'Верно - y,\nНеверно - <путь к директории>\n'
        )
        if check_target != 'y':
            if path.isdir(check_target):
                files_to_remove = check_target
                print(
                    f'Новая директория с неотфильтрованными '
                    f'файлами: {check_target}'
                )
            else:
                print('Указанный путь не является директорией')
                exit(-1)

        cls.files_remover(
            origin_files, files_to_remove, *files_types.split(' ')
        )

    @classmethod
    def get_files_list(cls, src_path: str) -> list[str]:
        """Walk through path folder and clean files names from type."""
        logger = getLogger()
        if not path.isdir(src_path):
            logger.info('Указанный путь не является директорией')
            return []
        return [f for f in listdir(src_path) if isfile(join(src_path, f))]

    @classmethod
    def extension_cleaner(
            cls, files_list: list[str], file_type: str
    ) -> list[str]:
        type_pat = compile(r'\.' + file_type + r'$', flags=IGNORECASE)
        return [
            type_pat.sub('', f_name)
            for f_name in files_list
            if type_pat.search(f_name)
        ]

    @classmethod
    def list_difference(
            cls, files_to_remove: list[str], files_to_exclude: list[str]
    ) -> set[str]:
        return set(files_to_remove) - set(files_to_exclude)

    @classmethod
    def files_remover(cls, origin_dir: str, to_remove_dir: str,
                      origin_ext: str = None, to_remove_ext: str = None) -> None:
        origin_list = cls.get_files_list(origin_dir)
        remove_list = cls.get_files_list(to_remove_dir)
        diff = cls.list_difference(
            cls.extension_cleaner(remove_list, to_remove_ext),
            cls.extension_cleaner(origin_list, origin_ext)
        )

        need_removing = input(
                f'Подтвердите удаление {len(diff)} '
                f'файлов из папки {to_remove_dir}\n'
        )
        if need_removing != 'y':
            print('Отмена удаления')
            return
        for f_name in diff:
            file_path = path.join(to_remove_dir, f_name + '.' + to_remove_ext)
            if isfile(file_path):
                remove(file_path)
        print('Файлы удалены успешно')

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


FileRemover.execute()
