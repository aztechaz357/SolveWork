"""`.github/` の定義から Claude Code 用のファイルを生成する。

元になるのは `.github/agents/*.agent.md` と、利用者が直接呼ぶスキル
(`.github/skills/*/SKILL.md` のうち `user-invocable: false` でないもの)。
エージェントやスキルの割当てを変えたら、これを実行して `.claude/` を作り直す。

    python tools/sync_agents.py          生成する
    python tools/sync_agents.py --check  生成結果が最新かどうかだけ調べる (CI 用)
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC_AGENTS = ROOT / ".github" / "agents"
SRC_SKILLS = ROOT / ".github" / "skills"
DST_AGENTS = ROOT / ".claude" / "agents"
DST_SKILLS = ROOT / ".claude" / "skills"

# Copilot のツール別名 -> Claude Code のツール名
TOOLS = {
    "read": ["Read"],
    "search": ["Grep", "Glob"],
    "edit": ["Edit", "Write"],
    "execute": ["Bash"],
}
NOTE = "<!-- tools/sync_agents.py が生成。直接編集せず .github/ 側を直す -->\n"


def split(text):
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        raise ValueError("frontmatter がない")
    return m.group(1), m.group(2)


def field(front, key):
    m = re.search(rf"^{key}:\s*(.*)$", front, re.M)
    return m.group(1).strip() if m else ""


def claude_agent(text):
    front, body = split(text)
    aliases = re.findall(r'"([^"]+)"', field(front, "tools"))
    lines = [f"name: {field(front, 'name')}", f"description: {field(front, 'description')}"]
    # ほかのエージェントを呼ぶ役は tools を省き、すべてのツールを使えるようにする
    if aliases and "agent" not in aliases:
        tools = [t for a in aliases for t in TOOLS.get(a, [])]
        lines.append("tools: " + ", ".join(tools))
    return "---\n" + "\n".join(lines) + "\n---\n" + NOTE + body


def claude_entry_skill(name, text):
    front, _ = split(text)
    return (
        "---\n" + front + "\n---\n" + NOTE + "\n"
        f"本体は GitHub Copilot と共用するため `.github/skills/{name}/` にある。"
        f"`.github/skills/{name}/SKILL.md` を読み、渡された引数でその手順どおりに実行する。\n"
    )


def outputs():
    out = {}
    for src in sorted(SRC_SKILLS.glob("*/SKILL.md")):
        text = src.read_text(encoding="utf-8")
        if field(split(text)[0], "user-invocable") == "false":
            continue  # 担当エージェントがパスで読むスキル。Claude Code 用の入口は作らない
        name = src.parent.name
        out[DST_SKILLS / name / "SKILL.md"] = claude_entry_skill(name, text)
    for src in sorted(SRC_AGENTS.glob("*.agent.md")):
        name = src.name[: -len(".agent.md")]
        out[DST_AGENTS / f"{name}.md"] = claude_agent(src.read_text(encoding="utf-8"))
    return out


def generated(paths):
    """以前にこの道具が生成したファイルだけを返す (手で置いたものは消さない)。"""
    return [p for p in paths if p.is_file() and NOTE in p.read_text(encoding="utf-8")]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    check = "--check" in sys.argv
    out = outputs()
    existing = generated(list(DST_AGENTS.glob("*.md")) + list(DST_SKILLS.glob("*/SKILL.md")))
    stale = [p for p in existing if p not in out]
    changed = []
    for path, text in out.items():
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if old != text:
            changed.append(path)
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8", newline="\n")
    if not check:
        for p in stale:
            p.unlink()
    for p in changed + stale:
        print(("古い: " if check else "更新: ") + str(p.relative_to(ROOT)))
    if check and (changed or stale):
        sys.exit(1)
    print(f"{len(out)} 個のファイルを確認した")


if __name__ == "__main__":
    main()
