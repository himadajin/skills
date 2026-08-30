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
「どこから手を付けるべきか」に推奨実装順序で答える。

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

レポートは調査の網羅ではなく、
「どこから手を付けるか」という質問への回答である。
読者が知りたい順に書く: 結論が先、理由と詳細が後。
分析で得た事実でも、推奨順序を変えないものは書かない。
同じ事実は、それが順序を決めている場所で一度だけ述べる。
手順 3 の分類は順序と確信度を決めるための分析であって
レポートの骨組みではないので、依存関係を独立したセクションとして列挙しない。

issue 番号だけでは人間は内容を思い出せないので、
言及は常に `#N(数語の説明)` の形にする。URL は貼らない。
issue 以外の根拠(設計文書・契約・コード)はパスで示し、
推定依存を順序の理由に使うときは(推定)と明示して根拠のパスを添える。

次の構成で報告する。

```md
## 結論

- 最初の行で「どこから・なぜ」を一言で答える
- 人間の判断・承認だけが妨げの issue があれば、依頼を先に出すことを次に挙げる
- 対象範囲を 1 行で(リポジトリ、基準時刻、open issue/PR 数、絞り込み条件)

## レーン図

- mermaid フローチャート 1 枚。この図が答えるのは
  「どれが直列で、どれが並行できるか」だけで、それ以外は描かない
- 並行できるレーンごとに subgraph を分け、レーン内の直列順序を矢印で結ぶ
- エッジは順序を強制する関係のみ。関連・相互参照は描かない
- ノードは `#N 数語の説明`、人間の判断ゲートは別形状(例: `{{…}}`)
- 保留中の issue は描かない。15 ノードを超えるなら描く対象をさらに削る

## 推奨実装順序

- フェーズ順に、各 issue を「#N(説明) — この位置に置く理由」の形で挙げる。
  理由は、なぜその順序が手戻りや待ち時間を減らすのかの一文
- 並行できる組はフェーズ内で明示する
- 最後のフェーズとして、着手条件つきで保留する issue を 1 行ずつまとめる
- どの open issue も、いずれかのフェーズか保留リストにちょうど一度現れる

## 補足

- 順序の判断に影響しうる注意(スナップショットの鮮度など)があるときだけ
```

長さの目安は、読者が数分で読み切って着手判断できること。
フェーズ内の 1 issue は 1〜2 行、保留する issue は 1 行に収める。
それを超える詳細は、順序を変えない限り捨てる。
