---
name: system-prompt-generator
description: 手順書・運用ルール・スキル定義などのドキュメントから LLM やエージェント向けのシステムプロンプトを生成するスキル。ターゲットモデルの公式システムプロンプト実例を体裁の手本にし、入力の手順・制約・ポリシーを再構成して出力する。システムプロンプトの新規作成、既存ドキュメントからの変換、別モデル向けの書き直しを求められたときに使う。
---

# system-prompt-generator

手順書やスキル定義を、対象エージェント向けのシステムプロンプトに変換する。
本文に変換規則を増やしすぎず、`references/` に置いた完成形から構造と体裁を合わせて生成すること。

## 入力を確定する

- 入力が本文かファイルパスかを確認する。
- ファイルパスなら内容を読む。`AGENTS.md`、`SKILL.md`、運用手順書、エージェント定義を優先して確認する。
- 入力が複数ある場合は、役割、制約、作業手順、出力方針を統合し、競合があれば明示する。

## reference を選ぶ

`references/` の公式システムプロンプト実例は「体裁の参考」と「内容の参考」の二つの目的で使い分ける。
まず `references/` のファイル名一覧を確認する。ファイルはフラットに `<vendor>-<surface>-<model>[-<variant>].md` 形式で管理される。

### 体裁の参考 — ターゲットモデルに合わせる

生成するプロンプトの構造・見出しの切り方・粒度・語調・マークアップ形式は、ターゲットモデルの既存システムプロンプトに倣う。

- ターゲットが明示されている場合は、まず vendor と surface を合わせ、次に model と variant を合わせる。
- 完全一致がなくても、同じ vendor・surface の別バージョンや同系統モデルのファイルを体裁テンプレートとして使う。
- ターゲットが不明な場合はユーザーに確認する。確認できなければ最も近い surface を選び、前提を明示する。汎用 fallback 用の実例は置かれていない。
- reference の文面をそのまま写さず、体裁パターンを抽出して適用する。

### 内容の参考 — 他モデルから知見を得る

references は「システムプロンプトに何を書くべきか」の知見の集積である。体裁テンプレートを決めた後、生成目的に応じて他モデルのプロンプトも横断的に参照し、書くべき項目の抜け漏れを防ぐ。

- ターゲットモデルのプロンプトだけをテンプレートとして扱わない。他モデルが同種の機能や制約をどう表現しているかを確認する。
- 例: コーディングエージェント向けなら `anthropic-claude-code.md`、`openai-codex-gpt-5.4.md`、`google-gemini-cli.md` を横断し、ツール使用規則・安全制約・自律性指針の共通パターンを把握する。
- 例: ツール固有の指示を含めるなら `openai-tool-*.md` を参照し、ツール指示の粒度や記述パターンを確認する。
- 例: 個性やスタイル定義を含めるなら `anthropic-default-styles.md`、`openai-codex-personality-*.md`、`xai-grok-personas.md` を参照する。
- 横断参照の結果はターゲットモデルの体裁に統一して反映する。他モデルの形式をそのまま混ぜない。

### 読み方

- reference が長い場合は冒頭のメタ情報と主要セクション構造を優先して読み、必要な箇所だけ追加で読む。
- バージョン違いがあるトラックでは最新と一つ前だけが置かれている前提で選ぶ。
- image generation 用、軽量モデル、`o3`、Gemini 2.x、text-first でないサービス、beta、notebook 系は置かれない前提で扱う。

## 変換する

- 入力から `role`、`scope`、`priorities`、`workflow`、`tool rules`、`safety constraints`、`response style`、`output contract` を抽出する。
- 入力にある項目名を無理に固定フォーマットへ押し込まず、選んだ reference と同等の読みやすさで再構成する。
- スキル定義から変換する場合は、`description` を役割定義と適用条件に展開し、本文から実行手順、判断基準、補助資料の使い方を抽出する。
- 手順書から変換する場合は、作業順序、禁止事項、確認事項、例外時の扱いを優先して反映する。
- 一般論を増やしすぎず、入力にない仕様は推測で確定しない。

## 出力する

- 出力形式の指定があればそれに従う。
- 保存先の指定があればそれに従う。
- 保存先未指定でファイル生成が求められている場合は、カレントディレクトリに `./system-prompt-<target>.md` を生成する。ターゲット不明なら `./system-prompt.md` を使う。
- ファイル生成が明示されていなければ、最終プロンプト本文をそのまま返す。
- 併せて、使った reference とターゲットを短く示す。

## references

`references/` には `works/system_prompts_leaks` からコピーした公式システムプロンプト実例だけを置く。ベンダー別に `anthropic-*`, `openai-*`, `google-*`, `xai-*` を確認する。内容は以下のカテゴリに分かれる。

- **コーディングエージェント**: `anthropic-claude-code.md`, `openai-codex-gpt-5.4.md`, `google-gemini-cli.md`, `google-jules.md` — ツール使用規則、安全制約、自律性指針の参考
- **チャットモデル**: `anthropic-claude-opus-*.md`, `anthropic-claude-sonnet-*.md`, `openai-chatgpt-*.md`, `google-gemini-3*.md`, `xai-grok-4*.md` — 役割定義、応答スタイル、制約の参考
- **ツール固有指示**: `openai-tool-*.md` — 検索、コード実行、ファイル操作などツール別の指示パターンの参考
- **スタイル・個性**: `anthropic-default-styles.md`, `openai-codex-personality-*.md`, `xai-grok-personas.md` — 語調・個性定義の参考
- **ポリシー・安全**: `openai-policy-automation-context.md`, `xai-grok-safety-instructions.md`, `anthropic-claude-ai-injections.md` — 安全指針の参考

