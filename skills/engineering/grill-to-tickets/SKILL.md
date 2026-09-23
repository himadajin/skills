---
name: grill-to-tickets
description: Grill a request into shape with the installed grilling skill, then file the agreed tickets on GitHub, GitLab, or Jira. Invoke only on the user's explicit request.
disable-model-invocation: true
---
# grill-to-tickets

grilling スキルを使用し、ユーザーの要望をチケットにできる状態まで詰めてから、チケットを作成してください。

1. 要望と既存の状況を把握する。関連するコードや既存のチケットなど、自分で確認できる事実は自分で調べる。
2. grilling で、各チケットの意図・範囲・完了条件が決まるまで質問する。
3. 作成するチケットの案（タイトルと本文）を提示し、ユーザーの合意を得る。
4. 合意した案のとおりにチケットを作成し、作成したチケットの URL を報告して終了する。

作成先のトラッカーと操作手段は、リポジトリのリモートや使えるツールから判断してください。
判断できなければユーザーに尋ねてください。
