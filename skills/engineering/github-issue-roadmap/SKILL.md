---
name: github-issue-roadmap
description: >-
  Analyze a GitHub repository's open issue backlog as one portfolio: group workstreams,
  distinguish explicit from inferred dependencies, inspect referenced issues and pull requests,
  assess importance, and recommend an implementation order with parallelizable work.
  Use whenever a user asks to review, prioritize, sequence, or map dependencies across multiple
  open GitHub issues or an issue backlog. Do not use for investigating only one issue.
compatibility: Requires Python 3 and an authenticated GitHub CLI (`gh`) with repository access.
---

# github-issue-roadmap

複数の GitHub open issue の依存関係を分析し、ユーザーに報告する。

`gh` を必須とする。
`gh`が使用できない場合は別の方法に迂回せず、エラーをそのまま簡潔に伝え、停止する。

## process

### 1. スナップショットを取得する

次を実行する。`OWNER/REPO` が指定されていない場合、スクリプトは現在の checkout の `origin` から推定する。

```bash
python3 scripts/collect_issue_snapshot.py [OWNER/REPO]
```

スクリプトの JSON には、open issue の本文、metadata、コメントと、本文・コメント中の同一リポジトリの
`#N` 参照先が含まれる。取得時刻をレポートの基準時刻として使う。

### 2. リポジトリの根拠を必要な範囲で読む

ローカル checkout がある場合は、適用される `AGENTS.md`、ドキュメントの案内、issue が直接参照する設計文書やコードを読む。
コードを読む場合は依存関係の判断に必要な箇所を対象にし、リポジトリ全体を漫然と探索しない。

GitHub の本文やコメントは計画の明示的な根拠、設計文書とコードは実装上の結合を確かめる根拠として扱う。
コメントが本文より新しい場合は、その差分が計画を変更していないか確認する。

### 3. 依存関係を分類する

各関係を次のいずれかに分類する。

- **明示的な必須依存**: `depends on`、`after`、`blocked by`、sub-issue、epic の完了条件など、本文または
  コメントが前提としている関係。
- **明示的な推奨順序**: `desirable before`、`coordinates with` など、順序は書かれているが blocker ではない関係。
- **推定依存**: 同じ契約やデータ構造を先に安定させる必要がある、基盤を消費側より先に入れると手戻りを
  避けられる、同じ実装箇所の変更順で競合を減らせる、といったコード・設計上の関係。
- **関連のみ**: 同じ領域に属するが順序制約はなく、並行できる関係。

### 4. 重要度と実装順序を決める

次の順で重み付けする。ユーザーの指定がある場合はそれを優先する。

1. 正確性、セキュリティ、データ損失、明文化された契約違反
2. 多数の後続 issue を解放する基盤、または手戻りを防ぐ設計変更
3. product epic や明確なユーザー価値を完成させる機能
4. 独立した UX 改善と内部リファクタリング
5. 効果が未計測で、採用判断そのものが目的の性能課題


### 5. レポートを作る

解析の結果を次の形式で報告する。

```md
## 全体像

- issueの一覧をID順に並べ、それぞれを数行で説明する。
- クリティカルパスを説明する。

## 推奨実装順序

- 推定順序を説明する
- 依存関係をmermaid形式のフローチャートで書く。

## 要点・補足

- 


```

事実には GitHub issue/PR のリンクまたはローカル文書のパスを添える。
依存関係を単に列挙せず、なぜその順序が手戻りやリスクを減らすのかを一文で説明する。
