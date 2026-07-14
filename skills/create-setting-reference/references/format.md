# 体裁

設定資料集HTMLの体裁の定義。デザインはここで固定されており、実行時に変更しない。

## 原則

- 単一HTMLファイルとする。外部CSS、外部JavaScript、CDN、外部フォントを使わない。
- JavaScriptを使わない。
- ライトモード固定。ダークモード対応をしない。
- 色はグレースケールのみ。作品の雰囲気に合わせた配色、装飾、アイコン、絵文字を加えない。
- 色による状態分類や、検討中・矛盾・要確認などの状態表示を作らない。
- 後述のCSSを一字一句そのまま `<style>` に埋め込む。追加・変更・削除をしない。

## 文書構造

次の骨格を使用する。

```html
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>(作品タイトル、未定なら「タイトル:未定」)設定資料集</title>
<style>
(後述のCSSをそのまま埋め込む)
</style>
</head>
<body>
<main>
  <h1>(作品タイトル、未定なら「タイトル:未定」)</h1>

  <nav aria-label="目次">
    <h2>目次</h2>
    <ul>
      <li><a href="#characters">登場人物</a>
        <ul><li><a href="#(人物のid)">(人物名)</a></li></ul>
      </li>
      <li><a href="#relationships">人間関係</a></li>
      <li><a href="#terms">固有用語</a></li>
      <li><a href="#timeline">時系列</a></li>
    </ul>
  </nav>

  <section id="characters">
    <h2>登場人物</h2>
    <section id="(人物のid)">
      <h3>(人物名)</h3>
      <h4>基本情報</h4>
      <dl>
        <dt>(項目名)</dt>
        <dd>(確定している値)</dd>
      </dl>
      <h4>概要</h4>
      <p>…</p>
      <!-- 経歴・過去、目的、特徴も同様に h4 + p / ul -->
    </section>
  </section>

  <section id="relationships">
    <h2>人間関係</h2>
    <section id="(ペアのid)">
      <h3>(人物A)と(人物B)</h3>
      <h4>関係</h4>
      <p>…</p>
      <h4>(人物A)から(人物B)</h4>
      <p>…</p>
      <h4>(人物B)から(人物A)</h4>
      <p>…</p>
    </section>
  </section>

  <section id="terms">
    <h2>固有用語</h2>
    <section id="(用語のid)">
      <h3>(用語名)</h3>
      <p>…</p>
    </section>
  </section>

  <section id="timeline">
    <h2>時系列</h2>
    <p>同じ時期区分内の掲載順は、明示されていない限り前後関係を表さない。</p>
    <section id="(時点のid)">
      <h3>(時点)</h3>
      <section id="(場面のid)">
        <h4>(場面)</h4>
        <ol>
          <li>…</li>
        </ol>
      </section>
    </section>
  </section>
</main>
</body>
</html>
```

## マークアップの規約

- 見出し階層は、h1=文書タイトル、h2=章、h3=項目(人物名、人物ペア、用語名、時点)、h4=項目内の小見出し(基本情報、関係、場面など)とする。
- 章の `id` は `characters` / `relationships` / `terms` / `timeline` に固定する。
- 項目の `id` は内容が識別できるものを付ける。日本語のままでよい(例: `id="蓮"`)。同名衝突がある場合だけ接尾辞で区別する。
- 目次には章と項目(h3相当)までを載せる。小見出し(h4)は載せない。
- キーと値の組(基本情報など)は `dl` を使う。順序が確定した流れは `ol`、順不同の列挙は `ul` を使う。
- 情報が存在しない章・項目は、目次からも本文からも省略する。

## CSS

```css
:root {
  color-scheme: light only;
}

body {
  margin: 0;
  background: #ffffff;
  color: #1a1a1a;
  font-family: "Hiragino Kaku Gothic ProN", "Hiragino Sans", "Noto Sans JP",
    "Yu Gothic", Meiryo, sans-serif;
  font-size: 16px;
  line-height: 1.8;
}

main {
  max-width: 720px;
  margin: 0 auto;
  padding: 2.5rem 1.25rem 5rem;
}

h1 {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 0 1.5em;
}

h2 {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 3em 0 1em;
  padding-bottom: 0.3em;
  border-bottom: 1px solid #cccccc;
}

h3 {
  font-size: 1.1rem;
  font-weight: 700;
  margin: 2.5em 0 0.75em;
}

h4 {
  font-size: 1rem;
  font-weight: 700;
  margin: 1.75em 0 0.5em;
  color: #555555;
}

p {
  margin: 0.5em 0;
}

ul,
ol {
  margin: 0.5em 0;
  padding-left: 1.6em;
}

li {
  margin: 0.2em 0;
}

dl {
  margin: 0.5em 0;
}

dt {
  font-weight: 700;
}

dd {
  margin: 0 0 0.6em 1em;
}

a {
  color: #1a1a1a;
  text-decoration: underline;
}

nav ul {
  list-style: none;
  padding-left: 1.2em;
}

nav > ul {
  padding-left: 0;
}

@media print {
  body {
    font-size: 11pt;
  }

  main {
    max-width: none;
    padding: 0;
  }

  h2 {
    break-before: page;
  }

  nav {
    display: none;
  }

  section {
    break-inside: avoid-page;
  }
}
```
