# リリースの仕組み

このリポジトリのリリースは、チャットサービス(Claude、ChatGPT など)にスキルを
アップロードするための zip ファイルを配布する目的で作られている。

## 成果物

リリースには `skills/` 配下の各スキルが `<skill-name>.zip` として 1 スキル 1 ファイルで
添付される。zip の直下には `<skill-name>/` フォルダがあり、その中に `SKILL.md` と
関連ファイルが入っている。これは Claude と ChatGPT のスキルアップロードが期待する
共通の形式である。最新のリリースは
<https://github.com/himadajin/skills/releases/latest> から取得できる。

## リリースが作られる過程

リリースは、リポジトリ所有者が GitHub Actions の `Release` ワークフロー
(`.github/workflows/release.yml`)を手動実行したときにだけ作られる。
自動でリリースされることはない。実行の入口は次の 2 つである。

- GitHub の Actions タブ → `Release` → `Run workflow`(ブランチは `main`)
- CLI: `gh workflow run release.yml`

ワークフローは次を順に行う。途中で失敗した場合、タグもリリースも作られない。

1. `scripts/validate_skills.py` で全スキルを検証する
2. 日付ベースのタグ名を計算する(下記)
3. スキルごとに zip を作成する
4. タグとリリース(リリースノートは自動生成)を作成し、zip を添付する

## バージョン(タグ)の規則

タグは日付ベースの CalVer で、`vYYYY.MM.DD`(JST 基準)。同じ日に複数回リリース
した場合は `vYYYY.MM.DD.1`, `vYYYY.MM.DD.2`, … と枝番が付く。番号はワークフローが
既存タグを見て自動で決めるため、人が採番することはない。

## 日常の検証との関係

リリース時と同じ検証は CI(`.github/workflows/ci.yml`)として PR と main への
push でも実行される。壊れたスキルは main に入る前に検出されるため、リリース時の
検証は安全網として機能する。
