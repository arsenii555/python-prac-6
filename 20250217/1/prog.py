from sys import argv
import zlib
from glob import iglob
from os.path import basename, dirname
from pathlib import Path

def get_branches(repo_link):
    p = Path(repo_link)
    heads = p / 'refs/heads/'
    return (x for x in heads.iterdir())


match len(argv):
    case 1:
        print("Ошибка запуска. Должен быть задан путь к git репозиторию.")
    case 2:
        path = argv[1]
        for branch in get_branches(path):
            print(basename(branch))