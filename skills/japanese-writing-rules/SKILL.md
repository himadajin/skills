---
name: japanese-writing-rules
description: Japanese writing, editing, and review support with strict grammar, wording, and formatting rules. Use when Codex needs to write Japanese text from scratch, revise or rewrite existing Japanese prose, check Japanese documentation or messages for issues, or normalize wording to satisfy the bundled Japanese style rules.
---

# 日本語文章ルール

## Overview

日本語の文章を執筆、編集、チェックする際に使う。`references/style-rules.md` を基準とし、曖昧さを減らして、文法、言葉遣い、体裁をそろえる。

## Workflow

1. 依頼内容を整理する。作業を `執筆` `編集` `チェック` のいずれか、またはその組み合わせとして捉え、出力形式、読者、語調、敬体と常体、長さの制約を確認する。
2. `references/style-rules.md` を読み、文法、言葉遣い、体裁の規則を作業全体に適用する。
3. 入力文または要件を確認する。主語の曖昧さ、係り受けの曖昧さ、指示語の不明確さ、不要な語句、曖昧な推量表現、箇条書きの不整合を洗い出す。
4. 依頼内容に応じて作業する。執筆では要件を満たす本文を組み立てる。編集では文意と前提を保ったまま書き換える。チェックでは問題点を特定し、必要なら修正案を添える。
5. 完成前に見直す。`references/style-rules.md` に反する表現が残っていないか確認し、語調、用語、構成を全体でそろえる。
6. 情報が不足する場合は扱いを分ける。軽微な前提は文脈から補い、補うと意味が変わる場合は確認事項として明示する。

## Output

ユーザーが出力形式を指定した場合は従う。指定がない場合は、依頼内容に応じて次の形を基本とする。

1. 執筆では完成した本文を返す。前提の補足や確認事項がある場合だけ短く添える。
2. 編集では修正文を返す。修正意図の説明が有用な場合だけ、主要な修正点を添える。
3. チェックでは問題点を返す。修正文や言い換え案が有用なら併記する。

## Notes

- 生成する日本語本文では、文法、言葉遣い、体裁の判断を `references/style-rules.md` に合わせる。
- 生成する日本語本文では、Markdown 記法の太字は使わない。
- ユーザーの目的が明確な場合は、逐語的に修正するのではなく、読みやすさと明確さを優先して構成から整える。
- 箇条書きを使う場合は、各項目の品詞と抽象度をそろえる。条件分岐が混ざる場合は文章で書く。
