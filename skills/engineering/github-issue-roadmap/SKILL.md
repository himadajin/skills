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

複数の GitHub open issue を一つのポートフォリオとして分析し、
依存関係と推奨実装順序をユーザーに報告する。

`gh` を必須とする。
`gh` が使用できない場合は別の方法に迂回せず、エラーをそのまま簡潔に伝え、停止する。

## process

### 1. スナップショットを取得する

このスキルのディレクトリにあるスクリプトを実行する
(パスはこの SKILL.md からの相対で、作業ディレクトリ基準ではない)。
`OWNER/REPO` を省略すると、現在の checkout の `origin` から推定する。

```bash
python3 <このスキルのディレクトリ>/scripts/collect_issue_snapshot.py [OWNER/REPO] [--out DIR]
```

標準出力には issue ごとの構造だけを並べた索引が出る:
親子 (GitHub sub-issue)、本文・コメントが言及する `#N` とその状態、
他の issue/PR からの逆参照、open PR とそれが閉じる issue。
本文とコメントは `DIR/issues.md` に ID 順で書き出されるので、
ファイル読み取りツールで(大きければ分割して)全文を読む。
`DIR/snapshot.json` は同じ内容の機械可読版
(`openIssues`、`openPullRequests`、`references`、`unresolvedReferences` の配列)で、
必要なときだけ参照する。
索引の先頭にある取得時刻をレポートの基準時刻として使う。

索引が数百件を超える規模なら、全件を同じ深さで扱わず、
label・milestone・ユーザーの指定で対象を絞ってから本文を読む。

### 2. 根拠を必要な範囲で読む

GitHub の本文とコメントは計画の明示的な根拠、
設計文書とコードは実装上の結合を確かめる根拠として扱う。

- コメントが本文より新しい場合は、その差分が計画を変更していないか確認する。
- 参照先の closed issue や merged PR は、
  open issue の計画がその内容を前提にしているときに本文を読む。
  閉じているだけではマージされたことにならないので、
  索引の `merged` 表示かローカルの `git log` で着地を確かめる。
- ローカル checkout がある場合は、適用される `AGENTS.md`、
  ドキュメントの案内、issue が直接参照する設計文書やコードを読む。
- 推定依存を立てるときは、issue が挙げるファイルパスや関数名で `grep` し、
  複数の issue が同じ実装箇所を変更するかを実際に確かめる。
  本文に書かれていない競合はこの照合でしか見つからない。
- コードを読む範囲は依存関係の判断に必要な箇所に限り、リポジトリ全体を漫然と探索しない。

### 3. 依存関係を分類する

各関係を次のいずれかに分類する。

- **明示的な必須依存**: sub-issue の親子、`depends on`、`after`、`blocked by`、
  epic の完了条件など、本文またはコメントが前提としている関係。
  リポジトリの契約・設計文書が「A が入るまで B は満たせない」と
  明記している関係も、issue 本文に無くてもここに入れる。
- **明示的な推奨順序**: `desirable before`、`coordinates with` など、
  順序は書かれているが blocker ではない関係。
- **推定依存**: 同じ契約やデータ構造を先に安定させる必要がある、
  基盤を消費側より先に入れると手戻りを避けられる、
  同じ実装箇所の変更順で競合を減らせる、といったコード・設計上の関係。
- **関連のみ**: 同じ領域に属するが順序制約はなく、並行できる関係。

### 4. 重要度と実装順序を決める

次の順で重み付けする。ユーザーの指定がある場合はそれを優先する。

1. 正確性、セキュリティ、データ損失、明文化された契約違反
2. 多数の後続 issue を解放する基盤、または手戻りを防ぐ設計変更
3. product epic や明確なユーザー価値を完成させる機能
4. 独立した UX 改善と内部リファクタリング
5. 効果が未計測で、採用判断そのものが目的の性能課題

順序は作業量だけでなく待ち時間で決まる。
人間の承認や方針決定を必要とする issue は、
その判断を早く依頼できるよう独立して挙げ、
待っている間に進められる独立作業を並べて所要時間を縮める。

### 5. レポートを作る

解析の結果を次の形式で報告する。

```md
## 全体像

- 基準時刻と対象範囲(open issue 数、open PR 数、絞り込みがあればその条件)
- ワークストリームごとに、属する issue を列挙し、それぞれを一行で説明する
- クリティカルパス: 最長の直列鎖と、それが長い理由

## 依存関係

- 明示的な必須依存
- 明示的な推奨順序
- 推定依存(根拠となるファイル・文書を添える)
- mermaid フローチャート。実線 = 明示的な必須依存、点線 = 推奨順序と推定依存

## 推奨実装順序

- フェーズまたはレーンごとに、順序と理由
- 並行できる作業
- 人間の判断・承認を先に要する issue

## 要点・補足
```

事実には GitHub issue/PR のリンクまたはローカル文書のパスを添える。
依存関係を単に列挙せず、なぜその順序が手戻りやリスクを減らすのかを一文で説明する。
