"""Markdown の参照先が実在するかを調べ、中身が骨組みのままのスキルを一覧にする。

    python tools/check_links.py [--exclude <フォルダ> ...]

調べるもの:
- `[文字](相対パス)` のリンク先
- バッククォートで書かれた `.github/...` `tools/...` のパス
  (`<名前>` `*` `{case}` のような置き換え記号を含むものは除く)
- `TODO(分野の知識)` が残っているスキル (エラーにはしない)

参照先がなければ終了コード 1。
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {".git", ".claude", "node_modules", "__pycache__"}
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
CODE = re.compile(r"`((?:\.github|tools)/[^`\s]+)`")
FENCE = re.compile(r"^(`{3,})", re.M)
TODO = "TODO(分野の知識)"


def strip_fences(text):
    """コードブロックの中身は調べない (書式の例が入るため)。"""
    out, pos, open_len = [], 0, 0
    for m in FENCE.finditer(text):
        n = len(m.group(1))
        if not open_len:
            out.append(text[pos:m.start()])
            open_len = n
        elif n >= open_len:
            pos, open_len = m.end(), 0
    if not open_len:
        out.append(text[pos:])
    return "".join(out)


def targets(md, text):
    for m in LINK.finditer(text):
        t = m.group(1)
        if re.match(r"[a-z]+:|#", t):
            continue
        yield t, (md.parent / t.split("#")[0]).resolve()
    for m in CODE.finditer(text):
        t = m.group(1)
        if re.search(r"[<>*{}…]", t):
            continue
        yield t, (ROOT / t.rstrip("/")).resolve()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    skip = SKIP | {args[i + 1] for i, a in enumerate(args[:-1]) if a == "--exclude"}
    missing, todo, count = [], [], 0
    for md in sorted(ROOT.rglob("*.md")):
        rel = md.relative_to(ROOT)
        if skip & set(rel.parts):
            continue
        count += 1
        raw = md.read_text(encoding="utf-8")
        if TODO in raw and rel.name == "SKILL.md":
            todo.append(rel)
        for t, path in targets(md, strip_fences(raw)):
            if not path.exists():
                missing.append(f"{rel.as_posix()}: {t}")
    for line in missing:
        print("参照先がない: " + line)
    for rel in todo:
        print("未記入のスキル: " + rel.as_posix())
    print(f"{count} 個の Markdown を調べた。参照先の抜け {len(missing)} 件、未記入のスキル {len(todo)} 件")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
