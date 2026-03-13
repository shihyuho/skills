# UltraBrain 第一輪知識庫回顧

## 目前判斷

這份第一輪 vault 已經比較像可導航知識庫，而不是整理過的來源摘錄。

關鍵原因：

- `maps/home.md` 已明確定義知識庫目的與入口。
- `maps/lessons-moc.md`、`maps/workflow-moc.md`、`maps/general-moc.md` 已開始承擔導航功能，而不是只列檔名。
- `notes/` 的卡片大多是單一命題、可重用、可回想的 heuristics。
- `sources/` 保留的是 provenance，不是全文封存。

## 目前做得好的地方

### 1. 三層分工已經成立

- `notes/` 承載穩定知識。
- `maps/` 承載導航與入口。
- `sources/` 承載來源脈絡。

這點很重要，因為很多第一輪 vault 其實只有「整理後的摘錄」，沒有真的分出這三層。

### 2. map-first recall 方向是對的

`home.md` 先給入口，再往 `workflow-moc`、`debugging-moc`、`lessons-moc` 導，是正確方向。這代表未來回想不需要先從全文搜尋開始。

### 3. lesson card 品質不錯

像 `copy-build-workspaces-off-nfs-when-containerd-builds-are-slow`、`api-timeouts-can-trigger-duplicate-side-effects` 這類卡片，都有做到：

- 命名直接描述知識本身
- 一張卡一個命題
- brief 清楚
- confidence 沒有亂灌到 1.0

### 4. source note 沒有失控

`sources/2026-03-12-devops-slack-threads.md` 有 metadata、summary、key extracts、derived notes、why it matters，資訊足夠，但沒有退回 archive 模式。

### 5. 已經開始把整理流程本身變成知識

`notes/slack-export-curation-workflow.md` 很有價值，因為它不只是整理這批資料，而是把「之後怎麼持續整理」抽成可複用 workflow。

## 目前最值得優先修的地方

### 1. `related` 稍微偏多

目前 21 張 notes 裡有 16 張帶 `related`。這不算嚴重失控，但在這個規模下，容易慢慢變成用圖連結撐結構，而不是由 MOC 負責導航。

建議原則：

- 只保留會改變判斷或提供非直覺下一跳的 card-to-card 連結
- 主題歸類不要靠 `related` 補齊，回到 MOC 處理

### 2. lens 還不夠像真正的 lens

目前 `by-source-moc` 與 `by-confidence-moc` 已經有用，但它們比較偏維護視角與稽核視角，不是跨領域思考鏡頭。

下一輪更有價值的是補這種 lens：

- timeout / retry / idempotency
- network path suspicion
- workspace locality
- compatibility / support matrix
- state invalidation / cache coherence

這樣未來 recall 會更像「我遇到哪種問題」，而不是「這張卡從哪裡來」。

### 3. 問題導向入口還可以更強

`workflow-moc.md` 已經不錯，但如果要更接近實戰 recall，下一步應該把入口寫得更偏 symptom / failure mode，例如：

- 部署失敗
- 建置異常變慢
- 看似認證錯誤但其實是平台或憑證問題
- 重複 side effect / timeout / retry 類事故

這會讓 vault 更像工作時可直接進入的導航面，而不是整理好的主題清單。

## 建議的第二輪優先順序

### 第一優先：強化問題導向 MOC

先重整 `debugging-moc.md` 與 `workflow-moc.md`，讓它們更像「遇到什麼情境就從哪裡進」，而不是主題分類頁。

### 第二優先：新增真正的 lenses

從既有 cards 抽 5-7 個跨領域判斷鏡頭，讓不同主題的卡片能被同一種 troubleshooting frame 串起來。

### 第三優先：做一次 `related` grooming

把只是「同主題」的關聯撤掉，只保留：

- 會讓人想到不同診斷方向的跳轉
- 會讓人補上缺的前提條件
- 會讓人避免常見誤判的連結

## 一句總評

你這輪不是在做資料整理，而是在做知識庫的骨架，而且骨架已經立起來了。下一步不是繼續無限 capture，而是開始做真正的 grooming：強化入口、補 lenses、收斂 `related`。

## 對 `docs/第一輪想法.txt` 的第二輪回饋

### 1. 關於「有 source 的卡片反而太簡潔」

這個觀察有抓到真正的問題，但原因要稍微修正。

問題不是「有 source note，所以 card 就應該寫短」，而是很容易在實作時，心理上把脈絡外包給 source，導致 card 只剩結論。這會讓 card 失去獨立回想能力。

更好的原則是：

- card 要先能單獨被理解
- source 只負責 provenance
- source 不能拿來替 card 補洞

我會建議替 card 補一個最低自洽門檻：

- 主張是什麼
- 為什麼成立
- 何時適用

如果少了這三件事，就算有 source，card 也還是不夠完整。

### 2. 關於 source note 到底有沒有必要

如果一張 card 已經足夠自洽，而且來源沒有未來追溯價值，那 source note 本來就可以不要有。

source note 比較值得保留的情況是：

- 一個來源衍生多張 cards
- 來源可能之後會消失
- 你之後可能要回頭驗證脈絡
- 你不想把相同 provenance 重複寫進多張 cards

所以 source 的必要性，不在於「幫你把卡片寫完整」，而在於「之後還需不需要追溯這份脈絡」。

### 3. lessons 類卡片能不能借鏡 `lessons-learned`

可以借，但不要整套搬。

我覺得最值得借的是讓 lesson card 更自洽的骨架，例如：

- Context 或 Trigger
- Lesson
- When to Apply

這些欄位剛好能補你現在感受到的問題：有些卡只剩結論，沒有足夠的使用時機與判斷脈絡。

但不要直接把 `lessons-learned` 的整套 storage 與流程搬進來，例如：

- `docs/lessons/` 那套獨立儲存
- `scope`
- `source`
- `_index.md`
- 固定 recall 限額

因為 UltraBrain 的核心還是 map-first recall 與 notes/maps/sources 分層，不是 lessons 專用記憶系統。

### 4. 關於目前 lenses 的價值太弱

這個判斷我同意。

`by-source-moc` 與 `by-confidence-moc` 不是完全沒用，但它們比較像維護 lens 或 review lens，不像工作中會自然進去的 recall lens。

我會把它們降級成次要頁面，而不是主要入口：

- `by-confidence-moc`：定期檢查哪些卡還是 tentative，哪些該升降 confidence
- `by-source-moc`：檢查哪些知識還強依賴某個來源、哪些 source 可以合併或淘汰

真正更值得新增的，是 problem-oriented 或 reasoning-oriented lenses，例如：

- timeout / retry / idempotency
- network path suspicion
- workspace locality
- compatibility / support matrix
- state invalidation / cache coherence

這類 lens 才會真的提升 recall。

## 我建議加進第二輪的結構原則

### 1. 先定義 card 的最低自洽標準

每張 lesson-ish card 至少要讓人不回 source 也能理解：

- 核心主張
- 觸發情境或判斷脈絡
- 何時套用

### 2. 只對 lesson 類卡片加輕量骨架

不是每張 note 都要變成模板化長文，但 lesson 類卡片可以考慮加這種輕量段落：

- Context / Trigger
- Lesson
- When to Apply

### 3. 把 maps 分成 primary recall 與 review lenses

- primary recall：`home`、domain MOCs、problem MOCs、`lessons-moc`
- review lenses：`by-confidence-moc`、`by-source-moc`

這樣就不會把治理視角誤當成主要入口。

### 4. 每個 lens 都要對應一個固定使用動作

如果一個 lens 沒有對應的 review ritual，它就很容易只是形式存在。

例如：

- `by-confidence-moc` 用於定期清 tentative cards
- `by-source-moc` 用於定期檢查 provenance 依賴與 source note 是否還值得保留

### 5. source 不補洞，related 不補分類

- source 不負責替 card 補上下文
- `related` 不負責替 MOC 補主題分類

這兩條如果守住，整體結構會穩很多。

## 目前我最想回你的那一句話

不要用 source 補 card 的洞；先把 card 寫到能獨立被理解與重用，source 才只留下真正值得追溯的 provenance。
