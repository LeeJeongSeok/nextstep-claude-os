import json
import sys
from pathlib import Path

TODOS_FILE = Path(__file__).parent / "todos.json"


def load_todos():
    if not TODOS_FILE.exists():
        return []
    return json.loads(TODOS_FILE.read_text(encoding="utf-8"))


def save_todos(todos):
    TODOS_FILE.write_text(json.dumps(todos, ensure_ascii=False, indent=2), encoding="utf-8")


def next_id(todos):
    return max((t["id"] for t in todos), default=0) + 1


def cmd_add(todos, text):
    todos.append({"id": next_id(todos), "text": text, "done": False})
    save_todos(todos)
    print(f"추가됨: {text}")


def cmd_list(todos):
    if not todos:
        print("할일이 없습니다.")
        return
    for t in todos:
        mark = "v" if t["done"] else " "
        print(f"[{mark}] {t['id']}. {t['text']}")


def cmd_done(todos, todo_id):
    for t in todos:
        if t["id"] == todo_id:
            t["done"] = True
            save_todos(todos)
            print(f"완료: {t['text']}")
            return
    print(f"id {todo_id} 항목을 찾을 수 없습니다.")


def cmd_delete(todos, todo_id):
    filtered = [t for t in todos if t["id"] != todo_id]
    if len(filtered) == len(todos):
        print(f"id {todo_id} 항목을 찾을 수 없습니다.")
        return
    save_todos(filtered)
    print(f"삭제됨: id {todo_id}")


USAGE = """사용법:
  python todo.py add <할일>
  python todo.py list
  python todo.py done <id>
  python todo.py delete <id>"""


def main():
    args = sys.argv[1:]
    if not args:
        print(USAGE)
        return

    todos = load_todos()
    cmd = args[0]

    if cmd == "add" and len(args) >= 2:
        cmd_add(todos, " ".join(args[1:]))
    elif cmd == "list":
        cmd_list(todos)
    elif cmd == "done" and len(args) == 2:
        cmd_done(todos, int(args[1]))
    elif cmd == "delete" and len(args) == 2:
        cmd_delete(todos, int(args[1]))
    else:
        print(USAGE)


if __name__ == "__main__":
    main()
