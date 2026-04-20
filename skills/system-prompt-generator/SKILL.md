---
name: system-prompt-generator
description: 手順書、AGENTS.md、SKILL.md などの定義から、LLM/エージェント向けのシステムプロンプトを生成するスキル。入力が本文でもファイルパスでも扱い、`references/` に保存した公式システムプロンプト実例から、企業・サービス・モデル・バリアントごとの近い完成形を選んで同等の体裁で出力する必要があるときに使う。
---

# system-prompt-generator

手順書やスキル定義を、対象エージェント向けのシステムプロンプトに変換する。
本文に変換規則を増やしすぎず、`references/` に置いた完成形から構造と体裁を合わせて生成すること。

## 入力を確定する

- 入力が本文かファイルパスかを確認する。
- ファイルパスなら内容を読む。`AGENTS.md`、`SKILL.md`、運用手順書、エージェント定義を優先して確認する。
- 入力が複数ある場合は、役割、制約、作業手順、出力方針を統合し、競合があれば明示する。

## reference を選ぶ

- まず `references/` のファイル名一覧を確認する。
- `references/` 配下にディレクトリはない。すべてフラットなファイル名で管理される。
- ファイル名は原則として `<vendor>-<surface>-<model>[-<variant>].md` を使う。`vendor` は `anthropic` / `openai` / `google` / `xai`、`surface` は `claude` / `chatgpt` / `codex` / `gemini` / `grok` など利用面を表す。
- バージョン違いがあるトラックでは、`references/` には最新と一つ前だけが置かれている前提で選ぶ。
- image generation 用 prompt、軽量モデルの prompt、`o3`、Gemini 2.x、text-first ではないサービス、beta、notebook 系は `references/` に置かれない前提で扱う。
- ターゲットが明示されている場合は、まず vendor と surface を合わせ、次に model と variant を合わせる。
- ターゲットが不明な場合はユーザーに確認する。確認できない場合は、生成先に最も近い surface を選び、その前提を明示する。汎用 fallback 用の example は置かれていない。
- reference の文面をそのまま写すのではなく、構造、粒度、語調、見出しの切り方を抽出して適用する。
- reference が長い場合は、冒頭のメタ情報と主要セクション構造を優先して読み、必要な箇所だけ追加で読む。

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

- `references/` には `works/system_prompts_leaks` からコピーした公式 prompt 実例だけを置く。
- ベンダー別に `anthropic-*`, `openai-*`, `google-*`, `xai-*` を確認する。
- 代表例:
  - `references/anthropic-claude-code.md`
  - `references/openai-codex-gpt-5.4.md`
  - `references/google-gemini-cli.md`
  - `references/xai-grok-4.2.md`
- 古い世代を広く集めるのではなく、各トラックで最新と一つ前だけを参照候補として扱う。
- ただし image generation、軽量モデル、`o3`、Gemini 2.x、text-first ではないサービス、beta、notebook 系は参照候補から外す。
