---
name: e04
description: Decode 注音文, Chinese typed as Zhuyin keystrokes on an English keyboard, into the Chinese the user meant.
license: MIT
disable-model-invocation: true
---

# e04

Decode 注音文, Chinese typed as Zhuyin keystrokes on an English keyboard, into the Chinese the user meant. Unlike reading letters and digits as English, typos or identifiers, read a suspect fragment as keystrokes on the standard Zhuyin (大千) layout, and keep a reading only when every keystroke group spells a real Mandarin syllable.

## Layout

```
1 ㄅ  2 ㄉ  3 ˇ  4 ˋ  5 ㄓ  6 ˊ  7 ˙  8 ㄚ  9 ㄞ  0 ㄢ  - ㄦ
q ㄆ  w ㄊ  e ㄍ  r ㄐ  t ㄔ  y ㄗ  u ㄧ  i ㄛ  o ㄟ  p ㄣ
a ㄇ  s ㄋ  d ㄎ  f ㄑ  g ㄕ  h ㄘ  j ㄨ  k ㄜ  l ㄠ  ; ㄤ
z ㄈ  x ㄌ  c ㄏ  v ㄒ  b ㄖ  n ㄙ  m ㄩ  , ㄝ  . ㄡ  / ㄥ
```

- **Initials**: ㄅㄆㄇㄈ ㄉㄊㄋㄌ ㄍㄎㄏ ㄐㄑㄒ ㄓㄔㄕㄖ ㄗㄘㄙ
- **Medials**: ㄧㄨㄩ
- **Finals**: ㄚㄛㄜㄝ ㄞㄟㄠㄡ ㄢㄣㄤㄥ ㄦ
- **Tones**: `6` ˊ, `3` ˇ, `4` ˋ, `7` ˙. The first tone is the space bar and is usually left out.

## Read the keystrokes

1. **Map** each key through the layout.
2. **Split** into syllables. A syllable runs initial, medial, final, tone, each optional, in that order. A tone key closes it; otherwise the next syllable starts at the first key that cannot continue it: an initial after anything, a medial after a medial or final, a final after a final. `2jiu2u03` splits as ㄉㄨㄛ | ㄧ | ㄉㄧㄢˇ, 多一點. Where a toneless syllable leaves the split open, let the sentence decide.
3. **Confirm** it is 注音文: every syllable is a real Mandarin syllable and the reading fits the sentence. Otherwise the fragment means what it says and stays as written: `k8s` (ㄜ ㄚ ㄋ) and `s3` (ㄋˇ) spell no syllable, and `t3.micro`, an error code or an English word reads as itself in context.
4. **Choose** the characters the surrounding sentence calls for among the homophones.

## Reply

- When the user asks what a fragment means, show each one as `「cl3」→ ㄏㄠˇ → 好`, then the restored sentence when there is one.
- When 注音文 sits inside a request, state the reading in one line, such as `「ru03t86」→ 檢查`, and carry out the restored request.
- When candidate readings would lead to different actions, list them and ask before acting.
