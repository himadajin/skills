# Tailwind CSS v4 での実装

Tailwind v4（CSS-first 設定）のプロジェクトにトークンを組み込む手順。

## フォント

Fontsource の variable 版を導入する
（variable 版は 1 ファイルで 400〜600 をカバーし、ウェイト欠けが起きない）:

```sh
npm install @fontsource-variable/geist @fontsource-variable/geist-mono @fontsource-variable/noto-sans-jp
```

レイアウトの入口（Astro なら Layout.astro、Next.js なら root layout）で
グローバル CSS より先に import する:

```js
import "@fontsource-variable/geist";
import "@fontsource-variable/geist-mono";
import "@fontsource-variable/noto-sans-jp";
import "./global.css";
```

## トークン定義（global.css）

```css
@import "tailwindcss";

:root {
  --background: #fafafa;
  --foreground: #171717;
  --accent: #171717;
  --muted: #f5f5f5;
  --border: #ebebeb;
  /* コードブロック用のターミナル面（Shiki の vesper と揃える） */
  --terminal: #101010;
  --terminal-border: #282828;
}

@theme inline {
  --font-sans:
    "Geist Variable", "Noto Sans JP Variable", system-ui, -apple-system,
    "Hiragino Sans", "Yu Gothic", Meiryo, sans-serif;
  --font-mono:
    "Geist Mono Variable", ui-monospace, SFMono-Regular, Menlo, Consolas,
    monospace;
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-accent: var(--accent);
  --color-muted: var(--muted);
  --color-border: var(--border);
  --color-terminal: var(--terminal);
  --color-terminal-border: var(--terminal-border);
}
```

`--font-mono` を `@theme` に定義すると、Tailwind v4 の preflight が
`--default-mono-font-family` として `pre` / `code` に自動適用する。

## ベーススタイルとユーティリティ

```css
@layer base {
  * {
    @apply border-border outline-accent;
  }
  body {
    @apply bg-background font-sans text-foreground selection:bg-foreground selection:text-background;
  }
  a,
  button {
    @apply outline-offset-1 focus-visible:outline-2;
  }
}

/* メタ情報用の mono 大文字ラベル */
@utility meta-label {
  @apply font-mono tracking-[0.08em] uppercase;
}
```

`focus-visible:outline-2` はデフォルトで実線になる
（`outline-dashed` を付けない。破線フォーカスは意味論に反する）。

## 頻出パターン

- 本文リンク（prose 内）:
  `decoration-foreground/35 decoration-dashed underline-offset-4 hover:decoration-foreground`
- ナビの現在地:
  `underline decoration-foreground decoration-2 underline-offset-8`
- メタ情報のリンク（パンくず等）:
  `text-foreground/70 hover:text-accent`（濃度で状態を作る）
- タグ:
  `meta-label text-xs border-b border-dashed border-foreground/35 hover:border-accent hover:text-accent`
- ページタイトル:
  `text-3xl font-medium tracking-tight sm:text-4xl`
- ページ説明文:
  `font-mono text-[0.8125rem] text-foreground/60`（イタリック禁止）
- 見出しの余白: h2 に `mt-10 mb-3`、h3 に `mt-8 mb-3`

## コードブロック（Shiki）

Shiki を使う場合はテーマを `vesper` にし、外枠を terminal トークンで組む:

```css
.code-block-wrapper {
  @apply my-6 overflow-hidden rounded-md border border-terminal-border bg-terminal;
}
.code-block-header {
  @apply flex min-h-7 items-center justify-between border-b border-terminal-border bg-white/3 px-3;
}
.code-block-language {
  @apply meta-label text-[0.6875rem] font-medium text-white/45;
}
.copy-code {
  @apply rounded border border-white/15 bg-white/5 text-white/55;
  @apply hover:bg-white/10 hover:text-white;
}
/* ターミナル面内の選択はポラリティ反転 */
.code-block-wrapper ::selection {
  background: #f5f5f5;
  color: var(--terminal);
}
```
