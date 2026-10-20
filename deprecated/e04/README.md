# e04

Decode 注音文, Chinese typed as Zhuyin keystrokes on an English keyboard, into the Chinese you meant.

Unlike reading letters and digits as English, typos or identifiers, it reads a suspect fragment as keystrokes on the standard Zhuyin (大千) layout, and keeps a reading only when every keystroke group spells a real Mandarin syllable: `cp3` becomes 很, while `k8s` stays `k8s`.

## When to use

- You typed Chinese with the Zhuyin IME switched off, so `cp3` landed where 很 should be.
- Someone sent you 注音文 and you want it read.

This skill must be invoked explicitly.

## Getting started

Write as you normally would:

```text
幫我寫一個 Python 函式 ru03t86 email 格式對不對
```

The agent reads `ru03t86` as 檢查 and writes the function.

## Keystrokes

| Situation | What the agent does |
| --- | --- |
| You ask what a fragment means | Shows the keystrokes and the reading, `「cl3」→ ㄏㄠˇ → 好`, then the restored sentence |
| 注音文 sits inside a request | States the reading in one line, then does what the restored request asks |
| Two readings would lead to different actions | Lists them and asks before acting |
| The keys spell no real syllable, such as `k8s` (ㄜ ㄚ ㄋ) or `s3` (ㄋˇ) | Leaves the fragment as written |
| The keys spell a syllable but context says otherwise, such as `t3.micro` | Leaves the fragment as written |

You can leave out the first-tone space bar, as most people do: `2jiu2u03` still reads as ㄉㄨㄛ ㄧ ㄉㄧㄢˇ, 多一點.

## It's working if

- `cp3` in your message comes back as 很 in a one-line reading, and the work goes on without a "what do you mean?" round trip.
- `k8s`, `s3`, `v2` and other identifiers in a Chinese sentence get no Zhuyin reading.
- A misread shows up in the reading line before the agent acts on it.

## Common questions

**Why is it in `deprecated/`?**
On Opus, the agent decoded every evaluated 注音文 sentence as well without the skill as with it, so its always-loaded description no longer paid for itself. It no longer ships with the plugin.

**Does it read Zhuyin symbols such as ㄕㄨㄛ?**
No. The agent reads Zhuyin symbols, abbreviated ones included, without this skill; it handles only keystrokes typed on an English keyboard.

## Limitations

- It knows only the standard 大千 layout; keystrokes from other layouts such as 倚天 or 許氏 decode wrongly or not at all.
- Keystrokes spell sounds, not characters: a homophone is picked from the surrounding sentence, so a bare fragment with no sentence around it may come back with candidates to choose from.
