from sys import argv
import zlib
from os.path import basename
from pathlib import Path


def get_branches(repo_path):
    heads = repo_path / "refs/heads/"
    return [basename(x) for x in heads.iterdir()]


def get_last_commit_hash(branch_path):
    with open(branch_path) as f:
        return f.read().strip()


def get_tree_hash(blob):
    for line in blob.splitlines():
        if line.startswith("tree"):
            return line.split()[1]


def parse_tree(tree_data):
    _, _, content = tree_data.partition(b"\x00")
    files = []
    while content:
        mode_name, content = content.split(b"\x00", 1)
        mode, name = mode_name.split(b" ", 1)
        sha1, content = content[:20], content[20:]
        sha1_hex = sha1.hex()
        obj_type = "blob" if mode.startswith(b"10") else "tree"
        files.append(f"{obj_type} {sha1_hex} {name.decode()}")
    return files


def get_object(repo_path, obj_hash):
    obj_path = repo_path / f"objects/{obj_hash[:2]}/{obj_hash[2:]}"
    if obj_path.exists():
        return zlib.decompress(obj_path.read_bytes())
    return None


def show_commit_history(repo_path, commit_hash):
    curr_commit = get_object(repo_path, commit_hash)
    if not curr_commit:
        return

    head, _, blob = curr_commit.partition(b"\x00")
    blob = blob.decode()
    tree = get_tree_hash(blob)
    if tree:
        tree_obj = get_object(repo_path, tree)
        if tree_obj:
            print(f"TREE for commit {commit_hash}")
            print("\n".join(parse_tree(tree_obj)))

    for line in blob.splitlines():
        if line.startswith("parent"):
            show_commit_history(repo_path, line.split()[1])
            break


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
        commit_object = get_object(repo_path, last_commit)
        head, _, blob = commit_object.partition(b"\x00")
        blob = blob.decode()
        print(blob)

        show_commit_history(repo_path, last_commit)