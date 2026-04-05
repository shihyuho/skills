# LYT + Atlas Spec

日期：2026-03-11
狀態：final

## 目前決議

### Atlas 定位

- `Atlas` 是知識入口層，重點是導航，不是單純收納。
- 目前只先規劃 `Atlas`，不處理 `Calendar` 與 `Efforts`。
- `Atlas` 是風格與架構概念，不要求在實際卡片或 MOC 名稱中出現 `Atlas` 字樣。
- `Atlas` 先採用這個基本分層：

```text
docs/ultrabrain/
  maps/
  notes/
  sources/
```

- `docs/ultrabrain/maps/`：放 MOC、入口頁、索引頁
- `docs/ultrabrain/notes/`：放知識卡片本體
- `docs/ultrabrain/sources/`：放來源整理，如文章、對話、書摘、會議摘要

### MOC 原則

- MOC 是地圖，不是資料夾。
- 一則 note 可以出現在多個 MOC。
- MOC 應幫助人與 AI 先看到全貌，再決定深入哪些 notes。
- MOC 放在 `Atlas/Maps/`。
- MOC 應持續演進，由 AI 協助維護，但最終應反映使用者的思考方式。
- 卡片不應保存會隨 MOC 重整而頻繁變動的外生關聯。

### 分類方向

- 第一層主導航不用主題，改用較穩定的 `domain`。
- 分類借鏡 `continuous-learning-v2` 的 `domain / source / confidence`。
- 第一版先不納入 `scope`。

### Domain MOCs（主導航）

- `code-style-moc`
- `testing-moc`
- `git-moc`
- `debugging-moc`
- `workflow-moc`
- `general-moc`
- `lessons-moc`

各 domain 職責：

- `code-style-moc`：命名、結構、抽象方式、可讀性、程式風格偏好
- `testing-moc`：測試策略、驗證方法、回歸測試、測試設計
- `git-moc`：commit 習慣、branch workflow、版本控制原則、PR 思維
- `debugging-moc`：排錯流程、定位技巧、失敗模式、驗證路徑
- `workflow-moc`：做事流程、研究流程、AI 協作方式、執行順序
- `general-moc`：跨 domain 的通用原則，不適合放進單一類別的知識
- `lessons-moc`：高價值 lesson、教訓、決策規則、容易忘記的前置條件

### Lens MOCs（輔助視角）

- `by-source-moc`
- `by-confidence-moc`

### 使用者自訂分類

- 第一版不預設自訂分類索引頁。
- 若使用者逐漸形成穩定的個人分類，由 AI 直接建立對應 MOC。
- 自訂 MOC 是否存在，以實際知識群聚是否成形為準，不預先保留空位。
- `home.md` 只保留少量高價值入口，避免膨脹成大型索引頁。

### 目前推薦的最小 Atlas 結構

```text
docs/ultrabrain/
  maps/
    home.md
    code-style-moc.md
    testing-moc.md
    git-moc.md
    debugging-moc.md
    workflow-moc.md
    general-moc.md
    lessons-moc.md
    by-source-moc.md
    by-confidence-moc.md
  notes/
  sources/
```

### Sources 的定位

- `Sources` 不是原文保存區，而是 `provenance / evidence layer`
- 不追求保存完整原始內容，只保存形成知識卡所需的最小來源脈絡
- 目標是讓之後的人或 AI 知道：這張卡從哪來、當時根據了什麼、是否值得回頭查
- `source` 關聯由 source note 與 MOC 維護，不作為卡片 canonical 欄位

一句話：`Sources` 是來源摘要層，不是全文倉庫。

在這個定位下：

- `maps`：導航
- `notes`：提煉後知識
- `sources`：形成知識的最小證據與上下文

### 何時建立 source note

AI 應建立 source note，當符合以下任一條件：

- 同一個來源產出 `2` 張以上知識卡
- 來源之後可能消失，但其脈絡仍值得保留
- 之後可能需要回頭驗證這張卡是怎麼來的
- 該來源本身有高密度資訊，值得保留摘要
- conversation / 爬文過程中的脈絡，對理解結論很重要
- 多張 note 共享同一來源，建立 source note 會比把來源資訊重複寫進每張卡更乾淨

AI 不需要建立 source note，當：

- 來源只是一次性觸發，且卡片本身已足夠自洽
- 原始來源沒有後續追溯價值
- 建立 source note 只會重複很薄的資訊

判準：如果來源的上下文對未來仍有價值，就建 source note；沒有，就不建。

### source note 最小模板

```md
# <source-title>

## Metadata
- Type: conversation | directory-scan | article | book | meeting
- Date: YYYY-MM-DD
- Origin: <URL / path / conversation topic / directory>
- Status: ephemeral | available | archived

## Summary
- 這個來源在說什麼
- 為什麼值得留下

## Key Extracts
- 重點 1
- 重點 2
- 重點 3

## Derived Notes
- [[某張知識卡]]
- [[另一張知識卡]]

## Why It Matters
- 這份來源之所以保留，是因為它提供了哪些脈絡、依據或分支線索
```

### Sources 的決策流程

```text
1. 這個來源是否會消失？
2. 它是否產出多張卡？
3. 未來是否可能需要追溯？
-> 任一為是：建立 source note
-> 否：直接轉卡，不建 source note
```

### 暫定 AI 閱讀順序

```text
1. 先讀 docs/ultrabrain/maps/home.md
2. 找到相關 Domain MOC
3. 視需要再讀對應 Lens MOC（source / confidence）
4. 進入 docs/ultrabrain/notes/ 的具體卡片
5. 需要原始脈絡時再讀 docs/ultrabrain/sources/
```

### 命名原則

- `Atlas` 只用來描述整體風格與結構，不作為實際卡片命名規則
- 實際 MOC 應直接用內容命名，例如 `workflow-moc`、`debugging-moc`、`lessons-moc`
- 實際首頁可命名為 `home.md`，不需要寫成 `atlas-home`
- 實際卡片應以內容本身命名，不需在標題中額外加上 `Atlas`

## Recall / Capture / MOC 整理流程

### 整體順序

```text
1. Atlas recall
2. Plan
3. Lessons recall
4. Task execution
5. Capture
6. MOC 整理（manual trigger）
```

### 1. Atlas recall

- 觸發時機：`plan` 之前
- 目的：在規劃前先載入既有知識地圖與相關 notes，避免從零開始思考
- 主要對象：`docs/ultrabrain/maps/` 與命中的 `docs/ultrabrain/notes/`
- 原則：
  - 先讀 `home.md`
  - 再讀相關 `domain moc`
  - 視需要再讀 `by-source-moc`、`by-confidence-moc`
  - 只載入最相關的 notes，不做全庫掃描

輸出：

- 本次規劃可依賴的既有知識
- 目前已知的相關脈絡與可重用材料

### 2. Lessons recall

- 觸發時機：`task` 之前
- 目的：在實際執行前載入高價值 lesson，作為執行約束
- 設計原則：跟 `skills/lessons-learned/SKILL.md` 的 recall 精神一致
- 原則：
  - 不作為常駐背景層
  - 僅在進入 task 前觸發
  - 載入少量高價值 lessons，避免過度干擾

輸出：

- 本次 task 應避免重犯的錯誤
- 本次 task 應遵守的高價值 decision rules

### 3. Task execution

- 先完成規劃與 lessons recall，再執行 task
- task 中可做輕量暫記，但不要求正式 capture 立即發生
- 正式知識沉澱以 task 後處理為主

### 4. Capture

- 觸發時機：`task` 之後
- 目的：把本次 task 產生的高價值知識沉澱為可重用 note
- 對象：
  - 新的知識卡
  - 既有知識卡的更新
  - 必要時建立 source note
  - 必要時產生 lesson candidate

原則：

- capture 以 `note-first` 為主
- 先判斷是否值得成卡
- 再判斷是 `create` 還是 `update`
- 最後更新相關 metadata 與掛載位置

### 5. MOC 整理

- 觸發方式：手動觸發
- 目的：讓 MOC 維持可導航，而不是每次 capture 都被自動改寫
- 原則：
  - 不把 MOC 整理綁進每次 capture
  - 需要時才由 AI 整理、建立、更新、拆分 MOC
  - MOC 層的變動應比 note 層保守

採手動觸發的理由：

- 避免 MOC 過度震盪
- 避免每次 capture 都重寫地圖
- 保持 Atlas 作為穩定導航層

## AI 何時建立／更新／拆分 MOC

### 1. 何時建立 MOC

AI 應建立新 MOC，當以下條件多數成立時：

- 已有一組 notes 明顯圍繞同一脈絡，但還沒有清楚入口
- 這組 notes 約有 `5` 則以上，或雖然未達 `5` 則，但已經開始難以導航
- 這組 notes 之間有可描述的結構，例如概念、方法、例子、洞察、問題
- 新 note 持續被掛進同一群聚，代表脈絡已穩定形成
- 建立地圖會比繼續平鋪連結更容易閱讀

判準：當一組知識開始需要入口頁時，就建立 MOC。

AI 建立 MOC 時：

- 先收納最核心的 `5-12` 則 note
- 只建立少量 section，不要一開始過度細分
- 優先讓新 MOC 可導航，而不是追求完整

### 2. 何時更新既有 MOC

AI 應優先更新既有 MOC，當：

- 已存在足以容納該 note 的 MOC
- 新 note 只是補充既有脈絡，不改變整體結構
- 只是某個 section 需要新增少量 note
- 某些 note 的順序需要重排，但還不需要拆出新圖
- 某張 MOC 的 summary、section title、閱讀順序需要微調

判準：如果這則 note 明顯有既有入口可回，就更新，不新建。

AI 更新 MOC 時：

- 把 note 掛進既有 section
- 必要時微調 section 順序與摘要
- 避免每新增一則 note 就重寫整張 MOC

### 3. 何時拆分 MOC

AI 應拆分 MOC，當一張地圖已失去導航作用：

- MOC 底下累積太多 note，讀起來像清單，不像地圖
- 同一張 MOC 已出現 `2-3` 個明顯子脈絡
- 使用者或 AI 需要在同一張 MOC 裡反覆搜尋，代表它過胖
- section 太多、太深、太雜，無法一眼看懂
- 新加入的 notes 已讓原本命名變模糊
- 某個子區塊已足以獨立成一張有意義的 MOC

判準：當 MOC 不再縮短理解路徑，反而增加理解成本時，就拆分。

AI 拆分 MOC 時：

- 保留原本 MOC 作為上層入口
- 將明顯子群拆成新的子 MOC
- 原 MOC 改成 `map of maps`，不要直接刪除

### 操作優先序

AI 面對新 note 時，依序判斷：

```text
1. 有沒有適合的既有 MOC？
   -> 有：先更新
2. 若沒有，是否已形成穩定群聚？
   -> 有：新建 MOC
3. 若既有 MOC 已過胖、過雜、失去導航性
   -> 拆分 MOC
```

## 待處理

- 無

## 模板草案

### 1. `home.md` 模板

`home.md` 是 Atlas 的總入口，只保留少量高價值入口，不做大型總表。

```md
# home

## Core Maps
- [[code-style-moc]]
- [[testing-moc]]
- [[git-moc]]
- [[debugging-moc]]
- [[workflow-moc]]
- [[general-moc]]
- [[lessons-moc]]

## Lens Maps
- [[by-source-moc]]
- [[by-confidence-moc]]

## Active Maps
- [[<近期活躍 MOC 1>]]
- [[<近期活躍 MOC 2>]]

## Starting Points
- 如果要找做事方法，先看 [[workflow-moc]]
- 如果要找排錯經驗，先看 [[debugging-moc]]
- 如果要找高價值教訓，先看 [[lessons-moc]]
```

`home.md` 維護原則：

- 只保留少量穩定入口
- `Active Maps` 可由 AI 動態更新
- 不把所有 MOC 都堆進首頁

### 2. `domain-moc` 模板

每張 `domain-moc` 都應該是可導航的地圖，而不是單純的 note 清單。

```md
# <domain-name>-moc

## Purpose
- 這張 MOC 用來導航 <domain> 相關知識。

## Core Concepts
- [[<核心概念卡 1>]]
- [[<核心概念卡 2>]]

## Methods and Practices
- [[<方法卡 1>]]
- [[<方法卡 2>]]

## Insights and Patterns
- [[<洞察卡 1>]]
- [[<洞察卡 2>]]

## Open Questions
- [[<問題卡 1>]]
- [[<問題卡 2>]]

## Related Maps
- [[by-source-moc]]
- [[by-confidence-moc]]
```

`domain-moc` 維護原則：

- 優先讓 section 能幫助閱讀，不追求固定欄位數
- 常見 section 可用：`Core Concepts`、`Methods and Practices`、`Insights and Patterns`、`Open Questions`
- 若某個 section 長出明顯子脈絡，可進一步拆成新的 MOC
- 如果該 domain 內沒有某種內容，可以省略該 section

### 2a. `by-source-moc` 模板

`by-source-moc` 用來回答：這些知識主要是自己想通的、承襲來的，還是從外部材料消化而來。

```md
# by-source-moc

## Personal
- [[<你的洞察卡 1>]]
- [[<你的洞察卡 2>]]

## Inherited
- [[<承襲觀念卡 1>]]
- [[<承襲觀念卡 2>]]

## Source-derived
- [[<從文章或掃描材料提煉的卡 1>]]
- [[<從文章或掃描材料提煉的卡 2>]]

## Related Maps
- [[workflow-moc]]
- [[lessons-moc]]
```

維護原則：

- `Personal` 優先收你自己的洞察、判斷、比喻、原則
- `Inherited` 收直接沿用或明顯受他人框架影響的知識
- `Source-derived` 收從文章、目錄掃描、文件等來源提煉出的知識
- 分類依據來自 source note 與人工/AI 判讀，不要求每張卡片在 frontmatter 保存 `source`
- 這張 MOC 是 lens，不應取代 domain MOC

### 2b. `by-confidence-moc` 模板

`by-confidence-moc` 用來回答：目前哪些知識已相對穩定，哪些仍在探索中。

```md
# by-confidence-moc

## High Confidence
- [[<高信心卡 1>]]
- [[<高信心卡 2>]]

## Tentative
- [[<暫定卡 1>]]
- [[<暫定卡 2>]]

## Related Maps
- [[debugging-moc]]
- [[workflow-moc]]
```

維護原則：

- `High Confidence` 可用 `confidence >= 0.7` 作為預設切線
- `Tentative` 可用 `confidence < 0.7` 作為預設切線
- 若一張卡從 `Tentative` 變穩定，應更新其數值 `confidence`，而不是重建新卡
- 這張 MOC 是 lens，不應取代 domain MOC

### 3. note frontmatter v1

第一版 frontmatter 先只保留最能支撐 Atlas 導航的欄位。

```yaml
---
title: <note title>
type: statement
confidence: 0.7
brief: "<一句話摘要這張卡的核心觀點>"
related:
  - "[[另一張相關卡]]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - tag1
  - tag2
---
```

欄位說明：

- `title`：note 標題
- `type`：知識角色，第一版限定為 `statement | thing | question | quote | person`
- `confidence`：數值信心度，採 `0.0-0.9` 區間，對齊 `lessons-learned` 的做法
- `brief`：一句話濃縮這張卡的核心觀點、結論或用途
- `related`：高價值橫向連結，連到其他相關卡片
- `created`：建立日期
- `updated`：最後更新日期
- `tags`：輔助搜尋與篩選

frontmatter v1 原則：

- 卡片只保留「自己是什麼」的內生欄位，不保留會隨整理變動的外生關聯
- `domain`、`source`、`up` 由 MOC 與 source note 維護，不作為卡片 canonical 欄位
- `type` 先作為卡片 metadata 保留，不在第一版建立 `By Note Type MOC`
- `brief` 與 `confidence` 用於 recall ranking、快速預覽與 AI 判讀

### AI 掛載規則（v1）

- 每張 note 應被至少一張主要 domain MOC 收錄，但這個關聯保存在 MOC，不保存在卡片 frontmatter
- 若 note 明顯符合 `By Source` 或 `By Confidence` 的視角，可同步由對應 MOC 收錄
- 若後續形成穩定自訂分類，AI 可直接建立對應 MOC 並收錄相關卡片
- 若找不到適合 domain，暫時由 `general-moc` 收錄，但應優先視為待整理狀態

## 收納邊界

### `general-moc` 邊界

`general-moc` 是暫時收納跨 domain 通用原則的地方，但不能成為垃圾桶。

應放入 `general-moc` 的內容：

- 橫跨多個 domain 的通用原則
- 暫時無法穩定歸入單一 domain，但已具知識價值的卡
- Atlas 結構、知識管理方法、分類原則等 meta 層內容

不應放入 `general-moc` 的內容：

- 其實已明顯屬於 `Workflow`、`Debugging`、`Testing` 等 domain 的卡
- 只是尚未整理的雜項筆記
- 缺乏提煉、尚未成卡的原始材料

治理規則：

- 若 `general-moc` 中某類卡片開始形成穩定群聚，應優先移出並建立新 MOC
- `general-moc` 應定期被 AI 檢查，避免累積成未分類倉庫

### `lessons-moc` 邊界

`lessons-moc` 暫時定義為「高價值、可重用的 lesson 與 decision rule」，先作為 Atlas domain 存在，但不等同於 `lessons-learned` skill 的正式存放層。

應放入 `lessons-moc` 的內容：

- 可重用的教訓
- 多次驗證後可直接套用的 decision rule
- 容易忘記但影響大的前置條件
- 從錯誤、修正、反覆實作中得到的穩定規則

不應放入 `lessons-moc` 的內容：

- 一般概念定義
- 單純的來源摘要
- 尚未提煉成規則的觀察
- 僅對某一次 conversation 有意義的零碎心得

治理規則：

- `lessons-moc` 先作為 Atlas 內的知識入口，不預設和 `lessons-learned` 的資料模型綁定
- 未來若要整合 `lessons-learned`，應以這裡的邊界為語意基準，再決定儲存與同步方式
