# UltraBrain Skill Design

## Goal

強化 `skills/ultrabrain/SKILL.md`，讓 skill 在建立或更新卡片時，更穩定產出自洽內容，而不是把關鍵脈絡外包給 source note。

## Problem Statement

目前真實使用回饋顯示，資訊過薄不只發生在 `lessons` 類卡片，`general` cards 也可能太短，導致閱讀者需要回 source 才知道前因後果。

這代表 skill 目前雖然清楚區分了 `notes / maps / sources`，但對「一張 card 至少要自洽到什麼程度」還不夠明確。

## Design Direction

### 1. 所有 cards 先有通用最低自洽標準

對所有 card types 補一條 base rule：

- card 應可單獨理解核心內容
- card 不應依賴 source note 才能理解其主要主張
- card 不應把關鍵前提、定義、或判斷脈絡藏在外部上下文裡

這條規則的目標不是把每張卡寫長，而是避免卡片薄到只剩結論標語。

### 2. reusable lessons 再加一層更高標準

對明顯屬於 reusable lesson、decision rule、heuristic 的 cards，增加一層 stronger guidance：

- 說清楚 lesson 是什麼
- 說清楚它在哪種情境下成立
- 說清楚什麼時候該套用

這層是 enhancement，不是所有 note 都要硬套模板。

### 3. source note 的邊界要更明確

skill 需要更直接地說明：

- source note 只負責 provenance 與追溯
- source note 不能用來替 card 補洞
- 若 card 的主要可理解性仰賴 source，代表 card 本身還沒寫好

### 4. lenses 重新定位

`by-source-moc` 與 `by-confidence-moc` 不再暗示成主要 recall 入口，而是 review lenses：

- `by-confidence-moc` 用來定期 review tentative cards
- `by-source-moc` 用來 review provenance 依賴與 source note 保留價值

這樣 skill 不會把維護頁面誤導成主要導航層。

## Intended SKILL.md Changes

### Card Rules

- 新增通用 card self-contained rule
- 補充「短不等於薄」的說明，允許簡潔，但不允許需要回 source 才看懂

### Lesson-Oriented Guidance

- 新增一小節，專門描述 reusable lessons / heuristics 應額外包含的資訊
- 避免引入完整 rigid template，只提供最小結構提示

### Source Notes

- 補強 source note 的 non-goal：不是用來承載 card 遺漏的背景
- 在建立 source note 條件旁補一句反向檢查規則

### Recall Workflow / Lens Maps

- 把 `by-source-moc`、`by-confidence-moc` 的角色改寫為 optional review lenses
- 避免和 `home`、domain MOCs、`lessons-moc` 同層暗示成主要 recall path

## Out of Scope

- 不直接修改使用者的知識庫內容
- 不在這一輪完整重寫 `ultrabrain` 的全部 workflow
- 不把 `lessons-learned` 的獨立 storage / index 系統搬進 UltraBrain

## Expected Outcome

skill 改版後，模型在使用 UltraBrain 時應更傾向：

- 先把 card 寫到可單讀理解
- 把 source 留作 provenance，而不是背景補丁
- 對 reusable lessons 提供更完整的適用脈絡
- 把 `by-source-moc` / `by-confidence-moc` 視為 review 頁，而不是主要 recall 入口
