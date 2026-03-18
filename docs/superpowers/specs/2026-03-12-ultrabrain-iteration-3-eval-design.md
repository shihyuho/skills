# UltraBrain Iteration 3 Eval Design

## Goal

重寫 `ultrabrain` 的 eval prompts，讓它們更能測出 skill 的獨特價值，而不是讓 baseline 靠一般常識與當前 prompt 也答到同樣結論。

## Why iteration-3 is needed

- `iteration-1` 有區辨力，顯示 skill 確實變好。
- `iteration-2` 主要用來驗證 source-note tightening fix 是否生效。
- `iteration-2` 雖然確認 fix 生效，但 eval 4-7 已經全部失去區辨力。

因此，下一步應該改 eval design，而不是繼續改 `SKILL.md`。

## Primary Focus

本輪優先測「邊界混淆」：

- review lenses vs troubleshooting lenses
- rewrite thin card first vs create source note first
- card capture vs MOC grooming
- create/update/skip decision order

## Recommended Design Direction

採用「雙重混淆題」而不是單一知識點題目。

原因：

- 比單變因更接近真實使用情境
- 仍可清楚 grading
- 更容易測出 UltraBrain skill 的結構判斷，而不是一般常識

## Candidate Eval Shapes

### 1. Review vs Troubleshooting Lens Conflict

Prompt 應同時提到：

- 某個具體技術故障症狀
- 又順手提到「我也想看看哪些卡還很 tentative」

測試模型是否能判斷：

- 主要任務是 troubleshooting recall
- review lenses 不是第一入口

### 2. Thin Card + Ephemeral Source + Crowded MOC

Prompt 應同時包含：

- 一張很薄的 card
- 一個 Slack / meeting / thread 來源
- 使用者又說某個 MOC 很擠

測試模型是否會：

- 先重寫 card
- 不先用 source 補洞
- 不把 MOC grooming 混進 card canonical content

### 3. create vs update with tempting duplicate

Prompt 應提供一張已有 card 與一條很像但不完全相同的新 lesson。

測試模型是否能：

- 明確判斷 `decision=update` 或 `decision=create`
- 說清楚為什麼不是另一個

### 4. Review task disguised as planning task

Prompt 表面上像「我要整理 vault」，但核心問題其實是：

- 哪些卡信心太低
- 哪些來源太脆弱

測試模型是否能：

- 看穿這是 review task
- 正確使用 `by-confidence-moc` / `by-source-moc`

### 5. MOC pressure disguised as card update request

Prompt 說「幫我把這張 card 加到 workflow-moc、lessons-moc、debugging-moc，順便把相關關係都寫進卡片 metadata」。

測試模型是否能：

- 拒絕把 MOC membership 寫進 card canonical fields
- 把 card capture 與 MOC updates 分開

### 6. Skip-worthy capture disguised as useful lesson

Prompt 應看起來像一條 lesson，但實際上只有泛泛提醒、沒有新方法、也很可能已被既有 debugging cards 吸收。

測試模型是否能：

- 把 `decision=skip` 當成合法選項
- 先判斷是否值得 capture，再決定要不要動 MOC

## What makes a good discriminator

新題目應滿足至少兩項：

- baseline 容易走向常識式回答
- skill 有明確規則可依賴來做更細緻的結構判斷
- grading 可以檢查「先後順序」與「層次分離」，不只是關鍵字

## What to avoid

- 太直接問「應該用哪個 lens」
- 太明顯讓答案就是 skill 文件原文重述
- 單純常識題，例如「薄卡要不要補內容」
- 沒有先後順序或層次衝突的 prompt

## Chosen Iteration-3 Set

本輪採用以下 5 題：

1. `#4` Review vs troubleshooting 主次衝突題
2. `#5` Thin card + ephemeral source + crowded MOC
3. `#6` create vs update near-duplicate
4. `#7` metadata layer violation
5. `#8` decision=skip 題

這組題目共同目標是：

- 強迫模型做先後順序判斷
- 強迫模型分清 card / source / MOC / lens 層次
- 避免 baseline 只靠一般常識就答對
