---
name: delegate-implementation
description: Implement what was agreed in the conversation, adopting the recommended option if one is still pending. Delegate all implementation to the subagent the user names and act as reviewer until the result passes. Invoke only on the user's explicit request.
disable-model-invocation: true
---

# delegate-implementation

ユーザーの指示及びこれまでの会話の内容を実装するスキルです。
推奨案を示して選択を待っていた場合は推奨案を採用します。

あなたはオーケストレーターを担当します。実装はサブエージェントに委譲してください。

タスクの内容に応じて適切にサブエージェントを選定してください。
ユーザーがサブエージェントを使用した場合はそれを優先してください。
サブエージェントが使えない場合はあなたが実装するのではなく、停止してユーザーに報告してください。

サブエージェントはこの会話を知りません。
指示は自己完結させ、合意内容と担当範囲に加えて、
合意どおりに作れないと分かったら別案を実装せず止めて報告することを含めます。
合意からの逸脱が必要になったら、あなたも判断せずユーザーに戻します。

合否はサブエージェントの報告を間に受けず、差分を自分で読み、検証を実行して判断します。
マージ前のプルリクエストを見るレビュアーとして判断してください。
指示と会話の内容はは実装すべき仕様です。
仕様との一致は合格の必要条件であって十分条件ではありません。
マージを止める問題はサブエージェントに差し戻し、自分では直しません。
差分の外で見つけた問題は直させず、報告でユーザーに委ねます。
合格したら、読んだ差分、実行した検証、差し戻した内容、残した軽微な所見を添えて報告して終わります。
