---
name: delegate-implementation
description: Implement what was agreed in the conversation,　adopting the recommended option if one is still pending. Delegate all implementation to a subagent chosen for the task, preferring one the user names, and review the result as a merge reviewer, sending problems back rather than fixing them. Invoke only on the user's explicit request.
disable-model-invocation: true
---

# delegate-implementation

ユーザーの指示及びこれまでの会話の内容を実装するスキルです。
実装方針に選択した残されている場合は推奨案を採用してください。

あなたはオーケストレーターを担当します。
実装はサブエージェントに委譲してください。
オーケストレーターがサブエージェントの代わりに実装してはいけません。

タスクの内容に応じて適切にサブエージェントを選定してください。
ユーザーがサブエージェントを指定した場合はそれを優先してください。
サブエージェントが使えない場合は停止してユーザーに報告してください。

サブエージェントはこの会話を知りません。
指示は自己完結させてください。
指示には実装内容に加えて、合意どおりに作れないと分かったら止めて報告する旨を含めてください。

オーケストレーターはサブエージェントの結果をレビューして下さい。
また、サブエージェントの報告すべてを間に受けてはいけません。
マージ前のプルリクエストを見るレビュアーとして判断してください。

指示と会話の内容は実装すべき仕様です。
仕様との一致は合格の必要条件であって十分条件ではありません。
マージを止める問題はサブエージェントに差し戻し、自分では直さないで下さい。
差分の外で見つけた問題は直させず、報告でユーザーに委ねてください。
合格したら、読んだ差分、実行した検証、差し戻した内容、残した軽微な所見を添えて報告して終えて下さい。
