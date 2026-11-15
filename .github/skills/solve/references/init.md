# init: 最初の設定

既にあるファイルは上書きしない。足りないものだけ作る。

1. 作業フォルダを軽く調べ (構成、既にある成果物)、分からない項目だけ利用者に質問する。
2. `.solve/project.yml` を作る。

```yaml
default_mode: lite       # lite | standard
tracker: none          # 案件の置き場所。github | manual | none
audience: ""   # いつも決める相手と関係部門。例: 部長、情報システム部門、法務、調達
doc_format: "1 枚 + 補足"   # 提案資料の形。社内の様式があれば library に登録する
library_dir: ""          # 参考資料の索引。使うなら .solve/library
docs:                    # 成果物の名称と場所。呼び方と置き場所に合わせて変える
  SIT: {name: 状況整理, path: cases/{case}/situation.md}
  ISS: {name: 論点, path: cases/{case}/issues.md}
  OPT: {name: 選択肢と評価, path: cases/{case}/options.md}
  ARG: {name: 説得の筋道, path: cases/{case}/argument.md}
  DOC: {name: 提案資料, path: cases/{case}/proposal.md}
  PLN: {name: 実行計画, path: cases/{case}/plan.md}
agent_skills: {}         # エージェントに追加で読ませるスキル。例: {<エージェント名>: [.github/skills/<名前>/SKILL.md]}
```

3. 利用者に尋ねて設定する。
   - 案件をどこで管理するか (github | manual | none)。`manual` の場合は `.solve/outbox/` を `.gitignore` に追加する。
   - 規定、過去の成果物、参考資料を参照させるか。使う場合は `library_dir` を設定し、見出し行だけの `index.md` を作る。git で管理するかどうかを尋ね、しない場合は `.gitignore` に追加する。登録は `library add` で行うと案内する。
   - 既にある成果物があれば `docs` の場所をそれに合わせる。Markdown 以外 (Word、Excel、PowerPoint) の場合は、エージェントが読み書きできる形にする方法を相談する。
4. 見出しだけのファイルを作る: `.solve/rules.md` (「固有ルール」)、`.solve/lessons.md` (「学びの記録」)。

トレース表、未整合台帳、成果物のファイルは init では作らない。最初にその工程を実行したときに担当エージェントが作る。
