import os


class LargeFilesBetween:
    __script_type = 'File Manager'

    __image_types = ['.jpeg', '.jpg', '.svg', '.gif', '.tiff', '.bmp', '.png', '.eps', '.raw', '.cr2', '.nef',
                     '.orf', '.sr2']
    __video_types = ['.webm', '.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', '.ogg', '.mp4', '.m4p', '.m4v', '.avi', '.wmv',
                     '.mov', '.qt', 'flv', '.swf']
    __audio_types = ['.mp3', '.aac', '.ogg', '.flac', '.alac', '.wav', '.aiff', '.dsd', '.pcm']
    __type_to_search = ''

    zero = 0

    def __init__(self, min_size, max_size, drive):
        self.min_size = min_size * 1000000
        self.max_size = max_size * 1000000
        self.drive = drive

    def __str__(self):
        return 'MIN FILE SIZE -> {0} ' \
               'MAX FILE SIZE -> {1} ' \
               'DRIVE TO SEARCH -> {2} '.format(self.min_size, self.max_size, self.drive)

    def find_with_type(self, file_type):
        for parent, direcectory, files in os.walk(self.drive):
            try:
                os.chdir(parent)
            except PermissionError:
                continue
            try:
                for file in files:
                    if (os.path.getsize(file)) >= self.min_size and file.endswith(file_type):
                        if (os.path.getsize(file)) <= self.max_size:
                            self.zero += 1
                            print(f'[{self.zero}]: {os.path.abspath(file)}')
            except FileNotFoundError:
                continue
        self.zero = 0

    def search_for_all_types(self):
        for parent, direcectory, files in os.walk(self.drive):
            try:
                os.chdir(parent)
            except PermissionError:
                continue
            for file in files:
                try:
                    if (os.path.getsize(file)) >= self.min_size:
                        if (os.path.getsize(file)) <= self.max_size:
                            for file_type in self.__type_to_search:
                                if file.endswith(file_type):
                                    self.zero += 1
                                    print(f'[{self.zero}]{os.path.abspath(file)}')
                except FileNotFoundError:
                    continue
        self.zero = 0

    def any_large_file(self):
        for parent, direcectory, files in os.walk(self.drive):
            try:
                os.chdir(parent)
            except PermissionError:
                continue
            for file in files:
                try:
                    if (os.path.getsize(file)) >= self.min_size:
                        if (os.path.getsize(file)) <= self.max_size:
                            self.zero += 1
                            print(f'[{self.zero}]{os.path.abspath(file)}')
                except FileNotFoundError:
                    continue
        self.zero = 0

    def set_type(self, passed_option):
        if passed_option == 1:
            self.__type_to_search = self.__image_types

        elif passed_option == 2:
            self.__type_to_search = self.__video_types

        elif passed_option == 3:
            self.__type_to_search = self.__audio_types


def check_path(drive):
    if os.path.exists(drive):
        return True
    print('[*]: Drive Specifed Does Not Exist!')
    return False


def convert_btyes_to_mega_bytes(size):
    return size * 1000000


def main_menu():
    min_size = int(input('[*]: Min Size Of File: '))
    max_size = int(input('[*]: Max Size Of File: '))
    drive_to_search = str(input('[*]: Which Drive: ')) + ':\\'
    check_path(drive_to_search)

    user_search = LargeFilesBetween(min_size, max_size, drive_to_search)
    option = 1

    while option != 5:
        print('''
                [1]: Show Files With A Specfied Type
                [2]: Show All Images
                [3]: Show All Videos
                [4]: Show All Audios
                [6]: Show Any Large Files
                [7]: Exit
            ''')
        option = int(input('\n[*]: Enter Your Option: '))

        if option == 1:
            file_type = str(input('[*]: Enter Type To Search: '))
            user_search.find_with_type(file_type)

        elif option == 2:
            user_search.set_type(1)
            user_search.search_for_all_types()

        elif option == 3:
            user_search.set_type(2)
            user_search.search_for_all_types()

        elif option == 4:
            user_search.set_type(3)
            user_search.search_for_all_types()

        elif option == 5:
            user_search.any_large_file()

        elif option > 5:    
            exit(not 0)

        option = int(input('\n[*]: Enter Your Option: '))


if __name__ == '__main__':
    main_menu()