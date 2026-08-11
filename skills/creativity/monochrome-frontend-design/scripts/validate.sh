#!/usr/bin/env bash
# monochrome-frontend-design: 禁止事項の機械検査
# 使い方: scripts/validate.sh <対象ファイル...>   (HTML / CSS / JSX など)
# ERROR（言語違反）があれば exit 1。WARN は目視確認を促すのみ。
set -u

if [ "$#" -eq 0 ]; then
  echo "usage: $(basename "$0") <file...>" >&2
  exit 2
fi

files=("$@" /dev/null) # /dev/null: 1 ファイル指定でも grep がファイル名を出すため
errors=0
warnings=0

report() { # $1=level $2=label $3=hits
  [ -z "$3" ] && return 0
  if [ "$1" = "ERROR" ]; then errors=$((errors + 1)); else warnings=$((warnings + 1)); fi
  printf '[%s] %s\n%s\n\n' "$1" "$2" "$3"
}

# --- ERROR: 機械判定できる言語違反 ---

report ERROR "font-weight 700 以上 / bold（600 が天井）" \
  "$(grep -nEi 'font-weight:[[:space:]]*(700|800|900|bold)|font-bold|font-extrabold|font-black' "${files[@]}")"

report ERROR "イタリック" \
  "$(grep -nEi "font-style:[[:space:]]*italic|[\"' ]italic[\"' ]" "${files[@]}")"

report ERROR "影（深度はガラスとヘアラインで表現する）" \
  "$(grep -nEi 'box-shadow|drop-shadow|[" ]shadow-(sm|md|lg|xl|2xl)' "${files[@]}" |
    grep -vEi 'box-shadow:[[:space:]]*none')"

report ERROR "グラデーション" \
  "$(grep -nEi 'linear-gradient|radial-gradient|conic-gradient|bg-gradient' "${files[@]}")"

report ERROR "波線" \
  "$(grep -nEi 'wavy' "${files[@]}")"

# --- WARN: 目視確認が必要な候補 ---

# 角丸: 0 / 4px / 0.25rem（インラインコード）以外を検出
report WARN "角丸の候補（許容はインラインコードの 4px のみ）" \
  "$(grep -nEi 'border-radius|[" ]rounded' "${files[@]}" |
    grep -vEi 'border-radius:[[:space:]]*(0|4px|0\.25rem)[[:space:];]|rounded-none')"

# トークン外の色: 5 トークン（+ 透明度 2 桁）と #d4d4d4（スクロールバー）以外の hex
report WARN "トークン外の色（シンタックステーマ等は要確認）" \
  "$(grep -noEi '#[0-9a-f]{3,8}' "${files[@]}" |
    grep -vEi ':#(fafafa|171717|f5f5f5|ebebeb|ffc799|d4d4d4)([0-9a-f]{2})?$')"

# --- 結果 ---

echo "----"
echo "ERROR: $errors  WARN: $warnings"
if [ "$errors" -gt 0 ]; then
  echo "言語違反があります。修正してから確定してください。"
  exit 1
fi
if [ "$warnings" -gt 0 ]; then
  echo "警告のみ。各行が意味を運ぶ差か確認してください（意味を 1 文で言えない差は作らない）。"
fi
exit 0
