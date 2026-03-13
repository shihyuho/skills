# UltraBrain MOC Taxonomy Design

## Goal

重整 `ultrabrain` 的 map taxonomy，讓 `Core Model`、`Map Structure`、`Recall Workflow`、`MOC Grooming` 使用同一組清楚的 map classes，避免把 primary recall paths 與 review lenses 混成同一層概念。

## Problem Statement

目前 `SKILL.md` 已經開始區分 domain MOCs 與 review lenses，但分類仍主要散落在 `Map Structure`、`Recall Workflow` 與 `MOC Grooming` 的敘述中。

這造成幾個問題：

- `Core Model` 只定義了 `maps/notes/sources` 三層，沒有定義 map layer 內部的 class system
- `Map Structure` 同時承擔了「類型定義」與「導航說明」，語義容易漂移
- `MOC Grooming` 仍像是在描述一種通用 MOC，沒有按 map class 區分維護目標
- `Recall Workflow` 雖然已暗示 review lenses 不是主要入口，但這個優先序沒有被更上層概念明確支撐

結果是 skill 的局部段落各自合理，但整體模型還不夠穩：讀者很容易把 `by-source-moc`、`by-confidence-moc` 誤讀成與 `domain maps`、`lessons-moc`、`general-moc` 同級的主要導航層。

## Design Direction

### 1. 把 map taxonomy 提升到 Core Model

`Core Model` 應新增一個 `Map Classes` 小節，明確定義 map layer 內部的功能分類。

建議 taxonomy：

- `home`
- `domain maps`
- `lessons-moc`
- `general-moc`
- `review lenses`

其中 `home` 是入口頁，不是其他 map classes 的 parent class。這個 taxonomy 描述的是功能角色，不是檔案樹或頁面巢狀階層。

這裡的重點不是做資料夾階層，而是定義功能角色：

- `home` 是入口與方向盤
- `domain maps`、`lessons-moc`、`general-moc` 共同構成 default recall maps
- `review lenses` 是整理與審查用視角，不是日常主導航，也不是 canonical homes for knowledge

在日常 first-pass recall 中，通常先進相關 `domain maps`；`lessons-moc` 與 `general-moc` 仍屬主導航的一部分，但不是每次都和 domain maps 同優先級進入。

這也代表像 `debugging-moc` 這種頁面應回到 `domain maps` 內理解，而不是被提升成獨立的 troubleshooting class。

### 2. 讓 Map Structure 只負責導航關係

`Map Structure` 不應再重新發明分類，只描述：

- 預設路徑是 `home -> relevant map -> cards`
- `review lenses` 可以連到既有 cards 或 maps，但不是 canonical homes for knowledge
- 同一張 card 可以被多個 maps / review lenses 連到，但主要歸屬脈絡仍應先由 `domain maps`、`lessons-moc` 或 `general-moc` 承擔

這樣 `Map Structure` 就是在回答「怎麼導航」，而不是「有哪些類型」。

### 3. 讓 MOC Grooming 改成 class-specific maintenance

`MOC Grooming` 應從通用規則改成依 map class 分段：

- `home grooming`
- `default recall map grooming`
- `review lens grooming`

每一類的維護目標不同：

- `home` 重點是入口清楚、節制、可掃描
- `domain maps`、`lessons-moc`、`general-moc` 重點是主題邊界、主導航穩定性、重複入口治理
- `review lenses` 重點是提供審查視角，而不是取代 recall path

### 4. 用 taxonomy 支撐 Recall Workflow 的優先序

有了 `Core Model` 裡的 taxonomy，`Recall Workflow` 可以更自然地建立優先序：

- 預設先走 `home`，再進相關 `domain maps`、`lessons-moc` 或 `general-moc`
- 只有在 provenance review 或 uncertainty review 時，才進入 `review lenses`

核心原則應明說：

- `domain maps`、`lessons-moc`、`general-moc` are the default recall path
- `review lenses` are conditional views, not default homes for knowledge

## Proposed Section Ownership

### Core Model

負責回答：

- 有哪些 map classes
- 每個 class 的主要任務是什麼
- 哪些 map pages 是 default recall path，哪些是 conditional views

### Map Structure

負責回答：

- 這些 classes 如何連接
- 使用者平常如何從 `home` 走到相關的 default recall maps
- `review lenses` 如何引用既有知識而不搶主導航角色

### MOC Grooming

負責回答：

- 不同 map class 各自要怎麼維護
- 哪些症狀代表要整理、合併、拆分、降級或保留
- 什麼情況下 review lens 有維護價值

## Intended SKILL.md Changes

### Core Model

- 新增 `Map Classes` 小節
- 明確列出 `home`、`domain maps`、`lessons-moc`、`general-moc`、`review lenses`
- 明講 `domain maps`、`lessons-moc`、`general-moc` 是預設 recall path

### Map Structure

- 拿掉重複的類型定義語氣
- 改成描述 `home -> relevant map -> cards` 的預設導航
- 保留 `review lenses` 的用途，但降回 conditional entry points

### Recall Workflow

- 不需要大改流程順序
- 只需把現有 map 選擇規則，重新接到新 taxonomy 上

### MOC Grooming

- 依 map class 重寫 grooming intent
- 補上 `review lenses` 不應搶 default recall path 的維護原則

## Out of Scope

- 不重寫整個 `Recall Workflow`
- 不新增新的 vault storage layer
- 不要求使用者立刻改自己的知識庫地圖名稱
- 不把 `review lenses` 變成硬性必備頁面

## Expected Outcome

這次改版後，`ultrabrain` 應更清楚地表達：

- map layer 內部不是單一種類的 MOC，而是不同 class 的導航物件
- `domain maps`、`lessons-moc`、`general-moc` 才是預設 recall path
- `review lenses` 是條件式視角，不是日常主入口
- `MOC Grooming` 應按 map class 維護，而不是用同一套規則處理所有 maps
