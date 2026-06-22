---
name: decision-reconcile
description: This skill should be used only when the user explicitly asks to run the decision-reconcile skill. It reviews the discussion so far and relevant project sources, distinguishes verified facts, explicit decisions, necessary consequences, AI assumptions or inferences, and unresolved topics, and asks questions to resolve genuine contradictions.
---

これまでの議論と、判断に関係するコード、ドキュメント、参照されたWebページを読む。
調べれば分かることは、それらの情報源から確認する。

確認できた事実、明示的に決まったこと、そこから必然的に導かれる帰結、仮定・推測、
まだ議論中のことを区別して整理する。

同じ前提で同時に成立できない内容だけを矛盾として扱う。
後の発言が以前の内容を明示的に修正している場合は、更新として反映する。

質問は矛盾の解消に限定する。矛盾が複数ある場合は、影響の大きいものから一度に一つ、
衝突している内容を示してユーザーに確認する。回答を反映してから、残る矛盾を改めて判断する。

最後に、現在の共通認識を簡潔に示す。
