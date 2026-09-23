---
name: grill-to-tickets
description: Grill a request into shape with the installed grilling skill, then file the agreed tickets on GitHub, GitLab, or Jira. Invoke only on the user's explicit request.
disable-model-invocation: true
---
# grill-to-tickets

grilling スキルを使用し、ユーザーの要望をチケットにできる状態まで詰めてから、チケットを作成してください。

1. grilling スキルを呼び出し、ユーザーの意図を汲み取り、チケットの範囲・完了条件が決まるまで意思決定の分岐を一緒にたどる。
2. 作成するチケットの案（タイトルと本文）を提示し、ユーザーの合意を得る。
3. 合意した案のとおりにチケットを作成し、作成したチケットの URL を報告して終了する。

必ずしも要望を一つのチケットにまとめる必要はありません。
複数のチケットに分割したり、親チケットや子チケットを作成する方が好ましい場合は、
ユーザーに提案してください。

作成先のトラッカーと操作手段は、リポジトリのリモートや使えるツールから判断してください。
判断できなければユーザーに尋ねてください。
