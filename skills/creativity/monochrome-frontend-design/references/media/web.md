# Web での実装

Web プロジェクト（主に Tailwind CSS v4 の CSS-first 設定）に
デザイン言語を組み込む実装仕様。
原則は `../design-system.md` と `../interaction.md` を参照。

## フォント

variable 版は 1 ファイルで 400〜600 をカバーしてウェイト欠けが起きないため、
Fontsource の variable 版を導入する:

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
  --background: #ffffff;
  --foreground: #171717;
  --accent: #171717;
  --muted: #f5f5f5;
  --border: #ebebeb;
  --header-h: 3.5rem; /* クローム帯の高さ */
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
    @apply bg-background font-sans text-foreground;
  }
  a,
  button {
    @apply outline-offset-1 focus-visible:outline-2;
  }
}

/* メタ情報の単一スケールラベル: 11px / 0.10em / weight 400 */
@utility meta-label {
  @apply font-mono text-[0.6875rem] leading-4 font-normal tracking-[0.1em] uppercase;
}

/* クローム共通のガラス材質 */
@utility glass-panel {
  @apply bg-background/75 backdrop-blur-md;
}
```

- `focus-visible:outline-2` はデフォルトで実線になる。
  破線フォーカスは意味論に反するため、`outline-dashed` を付けない。
- サイズ・太さは meta-label に焼き込み、呼び出し側で上書きしない。
  差を付けるのは濃度だけ。

## 頻出パターン

- 本文リンク（prose 内）:
  `decoration-foreground/35 decoration-dashed underline-offset-4 hover:decoration-foreground`
- クローム内リンク（hover で破線が浮かぶ）:
  `text-foreground/70 decoration-foreground/35 decoration-dashed underline-offset-4 hover:text-foreground hover:underline`
- ナビの現在地:
  `underline decoration-foreground decoration-2 underline-offset-4`
- タグ:
  `meta-label text-foreground/70 border-b border-dashed border-foreground/35 hover:border-accent hover:text-accent`
  （接頭に mono の `#` を `opacity-50` の span で置く。アイコンは使わない）
- ページタイトル: `text-2xl font-semibold tracking-tight`（レスポンシブで育てない）
- ページ説明文: `mt-2 mb-6 font-mono text-[0.8125rem] text-foreground/70`
- 本文コンテナ: `prose leading-[1.65]` に、段落・リスト前後 `my-4`、
  リスト項目 `my-1`、h2 `mt-8 mb-2`、h3 `mt-6 mb-2`、hr `my-8` を上書きする。

## ガラスクローム（sticky ヘッダー）

```html
<header
  id="site-header"
  class="glass-panel sticky top-0 z-50 border-b border-transparent transition-[border-color] duration-200 data-scrolled:border-border"
>
  <div class="mx-auto flex h-(--header-h) max-w-3xl items-center justify-between px-4">
    <a href="/" class="text-base font-semibold tracking-tight">site</a>
    <nav class="flex items-center gap-1"><!-- クローム内リンク --></nav>
  </div>
</header>
```

スクロール連動のヘアライン（最上部では紙に溶け、
スクロールした瞬間に層として立ち上がる）:

```js
const header = document.getElementById("site-header");
const update = () => header.toggleAttribute("data-scrolled", window.scrollY > 8);
document.addEventListener("scroll", update, { passive: true });
update();
```

付随して必要になる調整:

- アンカージャンプの逃げ: `:target { scroll-margin-block: calc(var(--header-h) + 1rem); }`
- ステージ: ヘッダー下端から最初の要素まで 48px（パンくずなら `mt-12`、
  パンくず→タイトルは `mb-2`）。全ページで同一値にする。
- ページ内ツールバー（言語トグル等）は
  `glass-panel sticky top-(--header-h) z-10 w-fit` で計器としてヘッダー直下に吸着。
  全幅のバーにしない。選択中は実線下線（`after` の 1px 線）、
  非選択の hover は破線出現。

## コードブロック（Shiki）

テーマは `min-light`（light/dark 両方に指定）にし、
白地 + インク枠の引用面として組む:

```css
.code-block-wrapper {
  @apply my-4 overflow-hidden border border-foreground bg-background;
  /* 角丸なし */
}
.code-block-wrapper .astro-code {
  @apply m-0 overflow-x-auto rounded-none border-0;
  scrollbar-color: #d4d4d4 transparent;
}
.code-block-header {
  @apply flex min-h-7 items-center justify-between border-b border-border px-3;
}
.code-block-language {
  @apply meta-label text-foreground/50;
}
/* コピーボタンは「計器」: 枠を持つ面。角丸なし */
.copy-code {
  @apply grid size-6 place-items-center border border-border text-foreground/50;
  @apply hover:bg-muted hover:text-foreground;
}
```

インラインコードは紙面の muted 地に残す:
`rounded bg-muted/75 p-1`（インラインのみ角丸 4px 許容）。
