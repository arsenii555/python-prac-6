from sys import argv
import zlib
from glob import iglob
from os.path import basename, dirname
from pathlib import Path


def get_branches(repo_path):
    heads = repo_path / "refs/heads/"
    return [basename(x) for x in heads.iterdir()]


def get_last_commit_hash(branch_path):
    with open(branch_path) as f:
        return f.read().strip()


match len(argv):
    case 1:
        print("Ошибка запуска. Должен быть задан путь к git репозиторию.")
    case 2:
        repo_path = Path(argv[1])
        for branch in get_branches(repo_path):
            print(branch)
    case 3:
        repo_path = Path(argv[1])
        branch = argv[2]
        if branch not in get_branches(repo_path):
            print("Ветка не найдена")
            exit()
        last_commit = get_last_commit_hash(repo_path / "refs/heads" / branch)
        commit_object = zlib.decompress((repo_path / f"objects/{last_commit[:2]}/{last_commit[2:]}").read_bytes())
        head, _, blob = commit_object.partition(b"\x00")
        blob = blob.decode()
        print(blob)
