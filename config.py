import configparser
from pathlib import Path


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('settings.ini')

        self.replay_folder_path = self.parse_path(self.config['DEFAULT']['ReplayFolder'])
        self.stash_folder_path = self.parse_path(self.config['DEFAULT']['StashFolder'])

    @staticmethod
    def parse_path(path_: str) -> Path:
        path_ = path_.replace('~', str(Path.home()))
        path_ = path_.replace('\\', "/")
        return Path(path_)

    def __str__(self) -> str:
        return str(self.__dict__)


if __name__ == '__main__':
    print(Config())
