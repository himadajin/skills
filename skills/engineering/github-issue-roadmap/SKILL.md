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

複数の open issue を個別に要約するのではなく、依存関係を持つ一つのポートフォリオとして分析する。
現時点の事実と推定を分け、次に着手できる実装順序を提示する。

## 境界

- 読み取り専用で作業する。issue、label、milestone、project、コメント、ローカルファイルを変更しない。
- 単一 issue の現状確認にはこのスキルを使わない。複数 issue の横断分析が対象である。
- `gh` を必須とする。未導入、未認証、権限不足の場合は取得を止め、エラーをそのまま簡潔に伝える。
  API や別ツールへのフォールバックを作らない。
- ユーザーが事業目標や期限を示した場合はそれを優先する。示されていなければ下記の既定基準を使い、
  優先順位を尋ねるためだけに作業を止めない。

## 手順

### 1. スナップショットを取得する

次を実行する。`OWNER/REPO` が指定されていない場合、スクリプトは現在の checkout の `origin` から推定する。

```bash
python3 scripts/collect_issue_snapshot.py [OWNER/REPO]
```

スクリプトの JSON には、open issue の本文、metadata、コメントと、本文・コメント中の同一リポジトリの
`#N` 参照先が含まれる。取得時刻をレポートの基準時刻として使う。

### 2. リポジトリの根拠を必要な範囲で読む

ローカル checkout がある場合は、適用される `AGENTS.md`、ドキュメントの案内、issue が直接参照する
設計文書やコードを読む。依存関係の判断に必要な箇所を対象にし、リポジトリ全体を漫然と探索しない。

GitHub の本文やコメントは計画の明示的な根拠、設計文書とコードは実装上の結合を確かめる根拠として扱う。
コメントが本文より新しい場合は、その差分が計画を変更していないか確認する。

### 3. 依存関係を分類する

各関係を次のいずれかに分類し、混同しない。

- **明示的な必須依存**: `depends on`、`after`、`blocked by`、sub-issue、epic の完了条件など、本文または
  コメントが前提としている関係。
- **明示的な推奨順序**: `desirable before`、`coordinates with` など、順序は書かれているが blocker ではない関係。
- **推定依存**: 同じ契約やデータ構造を先に安定させる必要がある、基盤を消費側より先に入れると手戻りを
  避けられる、同じ実装箇所の変更順で競合を減らせる、といったコード・設計上の関係。
- **関連のみ**: 同じ領域に属するが順序制約はなく、並行できる関係。

参照先が closed または merged なら前提完了として扱う。その番号を参照する各 open issue の文脈を確認し、
既に完了した前提や解決済みの副次効果が残っていれば、どの issue のどの主張が stale なのかを特定する。
親 epic は実装ステップに重複計上せず、子 issue の完了後に閉じる管理項目として扱う。

### 4. 重要度と実装順序を決める

ユーザー指定がない場合は次の順で重み付けする。

1. 正確性、セキュリティ、データ損失、明文化された契約違反
2. 多数の後続 issue を解放する基盤、または手戻りを防ぐ設計変更
3. product epic や明確なユーザー価値を完成させる機能
4. 独立した UX 改善と内部リファクタリング
5. 効果が未計測で、採用判断そのものが目的の性能課題

重要度と順序は同じではない。高重要度でも未完了の前提があれば後ろに置く。逆に小さな基盤変更が多数を
解放するなら先に置く。独立して安全に進められる作業は、直列の番号だけでなく並行可能な batch として示す。
全 open issue を、実装順、条件付き、要件具体化待ち、親 epic のいずれかに必ず位置付ける。

### 5. レポートを作る

ユーザーの言語で、次の構成を使う。簡潔さを保ちつつ、順序の判断根拠は省略しない。

## 全体像

- 取得日時、open issue 件数、priority metadata の有無を最初に示す。
- workstream ごとに issue をまとめ、各 issue へリンクする。
- クリティカルパスを小さな依存図または短い列で示す。

## 推奨実装順序

- 前提を満たす batch の順に並べる。
- 各 batch で、先に行う理由と並行可能な issue を示す。
- 明示的依存と推定した順序を区別する。

## 要点・補足

- 完了済みの前提、stale な本文、矛盾、metadata 不足を示す。
- 計測後に採否を決める issue と、要件具体化が必要な issue を分ける。
- 重要度が公式 metadata ではなく分析結果なら、その旨を明記する。

事実には GitHub issue/PR のリンクまたはローカル文書のパスを添える。依存関係を単に列挙せず、なぜその順序が
手戻りやリスクを減らすのかを一文で説明する。

送信前に、全 open issue が一度だけ位置付けられていること、同じ依存関係を別の節で矛盾して説明していないこと、
`唯一` や `すべて` のような排他的な断定に一覧全体の裏付けがあることを確認する。
