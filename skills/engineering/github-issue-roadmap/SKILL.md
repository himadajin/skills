---
name: github-issue-roadmap
description: >-
  Analyze a GitHub repository's open issue backlog as one portfolio: group workstreams,
  distinguish explicitly stated dependencies from those grounded in code or design, inspect referenced issues and pull requests,
  assess importance, and recommend an implementation order with parallelizable work.
  Use whenever a user asks to review, prioritize, sequence, or map dependencies across multiple
  open GitHub issues or an issue backlog. Do not use for investigating only one issue.
compatibility: Requires Python 3 and an authenticated GitHub CLI (`gh`) with repository access.
---

# github-issue-roadmap

GitHub の複数の open issue を一つのポートフォリオとして分析し、推奨する実装順序を示して「どこから手を付けるべきか」に答える。

このスキルは `gh` コマンドを使用する。

## 手順

### 1. スナップショットを取得する

`scripts/collect_issue_snapshot.py` スクリプトを実行する。
`OWNER/REPO` を省略すると、現在の checkout の `origin` から推定する。

```bash
python3 {SKILL_DIR}/scripts/collect_issue_snapshot.py [OWNER/REPO] [--out DIR]
```

標準出力には、issue ごとの関係や状態だけをまとめた索引が表示される。
索引には、親子関係（GitHub sub-issue）、本文やコメントが言及する `#N` とその状態、他の issue/PR からの逆参照、open PR とそれが閉じる issue が含まれる。
本文とコメントは `DIR/issues.md` に ID 順で書き出されるので、全文を読む。
`DIR/snapshot.json` は同じ内容の機械可読版（`openIssues`、`openPullRequests`、`references`、`unresolvedReferences` の配列）で、必要なときだけ参照する。

索引が数百件を超える規模なら、全件を同じ深さで扱わず、label、milestone、ユーザーの指定で対象を絞ってから本文を読む。

### 2. 根拠を必要な範囲で読む

GitHub の本文とコメントは計画の明示的な根拠として、設計文書とコードは実装上の結合を確かめる根拠として扱う。

- コメントが本文より新しい場合は、その差分が計画を変更していないか確認する。
- 参照先の closed issue や merged PR は、open issue の計画がその内容を前提にしているときに本文を読み、その前提が成立しているかを確かめる。
- ローカル checkout がある場合は、適用される `AGENTS.md`、ドキュメントの案内、issue が直接参照する設計文書やコードを読む。
- コードや設計に基づく依存関係を判断するときは、issue が挙げるファイルパスや関数名で `grep` し、複数の issue が同じ実装箇所を変更するかを実際に確かめる。
- コードを読む範囲は依存関係の判断に必要な箇所に限定する。

### 3. 依存関係を分類する

各関係を次のいずれかに分類する。

- **明示的な必須依存**：sub-issue の親子、`depends on`、`after`、`blocked by`、epic の完了条件など、本文またはコメントが前提としている関係。
  リポジトリの契約や設計文書が「A が入るまで B は満たせない」と明記している関係も、issue 本文になくてもこの分類に含める。
- **明示的な推奨順序**：`desirable before`、`coordinates with` など、順序は書かれているが blocker ではない関係。
- **コードや設計に基づく依存関係**：同じ契約やデータ構造を先に安定させる必要がある、基盤をそれを利用する側より先に入れると手戻りを避けられる、同じ実装箇所の変更順で競合を減らせる、といったコードや設計上の関係。
- **関連のみ**：同じ領域に属するが順序制約はなく、並行できる関係。

### 4. 重要度と実装順序を決める

次の順で重み付けする。
ユーザーの指定がある場合はそれを優先する。

1. 正確性、セキュリティ、データ損失、明文化された契約違反
2. 多数の後続 issue に着手できるようにする基盤、または手戻りを防ぐ設計変更
3. product epic や明確なユーザー価値を完成させる機能
4. 効果が未計測で、採用判断そのものが目的の性能課題

順序は作業量だけでなく待ち時間で決まる。
人間の承認や方針決定を必要とする issue は、その判断を早く依頼できるよう独立して挙げ、待っている間に進められる独立した作業を並べて所要時間を縮める。

### 5. レポートを作る

レポートは調査結果を網羅するためのものではなく、「どこから手を付けるか」という質問への回答である。
読者が知りたい順に、結論を先に、理由と詳細を後に書く。
分析で得た事実でも、推奨順序を変えないものは書かない。
同じ事実は、それが順序を決めている場所で一度だけ述べる。
手順 3 の分類は順序と確信度を決めるための分析であってレポートの構成ではないので、依存関係を独立したセクションとして列挙しない。

issue 番号だけでは人間は内容を思い出せないので、言及するときは常に `#N(数語の説明)` の形にする。
URL は貼らない。
issue 以外の根拠（設計文書、契約、コード）はパスで示す。
コードや設計に基づく依存関係を順序の理由に使うときは、確認した実装上の関係と、それが順序を決める理由を説明する。

次の構成で報告する。

```md
## 結論

- 最初の行で「どこから・なぜ」を一言で答える
- 人間の判断・承認だけが妨げの issue があれば、依頼を先に出すことを次に挙げる
- 対象範囲を 1 行で(リポジトリ、基準時刻、open issue/PR 数、絞り込み条件)

## 推奨実装順序

- フェーズ順に、各 issue を「#N(説明) — この位置に置く理由」の形で挙げる。
  理由は、なぜその順序が手戻りや待ち時間を減らすのかの一文
- 並行できる組はフェーズ内で明示する
- 最後のフェーズとして、着手条件つきで保留する issue を 1 行ずつまとめる
- どの open issue も、いずれかのフェーズか保留リストにちょうど一度現れる
- mermaid フローチャートを作成する。
  - エッジは順序を表す。
  - ノードは `#N 簡潔な説明`、人間の判断ゲートは別形状(例: `{{…}}`)

## 補足 (optional)

- 結論と推奨実装順序に書けなかったが、ユーザーに伝えるべき事実や注意点がある場合はここに書く。
```

フェーズ内の 1 issue は 1〜2 行、保留する issue は 1 行に収める。
それを超える詳細は、順序を変えない限り省く。
