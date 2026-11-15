---
name: solve
description: 定型でない、急に現れる答えのない問題 (上司や組織の説得、進め方がおかしい計画の見直し、業務改善) を、問題の整理、選択肢の比較、提案資料、実行計画の順に進める。利用者と対話し、担当エージェントに仕事を割り振る入口。説得や提案、方針や計画の見直し、業務改善、どう進めればよいか分からない問題の相談で使う。
argument-hint: "<やりたいことを文章で> | [lite|standard] [frame|options|propose|plan|all] <案件名> [補足] | <エージェント名> <依頼> | reconcile | audit | library add <場所> | init | improve"
---
<!-- tools/sync_agents.py が生成。直接編集せず .github/ 側を直す -->

本体は GitHub Copilot と共用するため `.github/skills/solve/` にある。`.github/skills/solve/SKILL.md` を読み、渡された引数でその手順どおりに実行する。
