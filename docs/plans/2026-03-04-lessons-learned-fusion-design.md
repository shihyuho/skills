# Lessons-Learned 融合版設計（已核可）

## 目標

以「融合版」策略優化 `skills/lessons-learned/`，採低風險分階段落地：

- P0：規則瘦身與去重
- P1：導入 `confidence` 核心能力
- P2：條件式演化（非預設啟用）

本設計遵守以下邊界：

- 不引入 hooks、background agent、daemon 或新平台依賴。
- 不改變整體 repo workflow，只調整 `lessons-learned` skill 相關內容。
- 每一階段可獨立驗收與回退。

## 架構與邊界

採「文件規則優先、行為演化後置」的順序：

1. 先將規則語意與結構收斂（P0）。
2. 再導入 `confidence` 以提升 recall 排序品質（P1）。
3. 最後才導入演化能力（P2），且需觀測條件滿足才啟用。

改動範圍聚焦：

- `skills/lessons-learned/SKILL.md`
- `skills/lessons-learned/references/card-template.md`
- `docs/plans/`（設計與實作計畫文件）

## 元件與檔案設計

### P0（結構瘦身）

1. 精簡 `related` 規則，保留「高關聯才加、最多 1-2 個」原則。
2. 移除 `Benchmark Targets`（從 `SKILL.md` 主體移出）。
3. 合併重複段落（Trigger / Integration / Validation 的重疊語意）。
4. `index recovery` 精簡為單句可執行規則。
5. 刪除 `skills/lessons-learned/references/eval-cases.md`。

### P1（核心能力）

1. 在 lesson card frontmatter 導入 `confidence` 欄位。
2. 更新 recall 排序規則為：
   `tag -> scope -> confidence(desc) -> date(desc)`。
3. 更新 `references/card-template.md`，補上 `confidence` 欄位與填寫說明。
4. 同步更新 validation 規則，避免 `SKILL.md` 與 template 雙重標準。

### P2（條件式演化）

1. 保留 scope promotion（`feature -> module -> project`）。
2. 導入 `confidence decay` 的條件式機制（預設不啟用）。
3. 若觀測指標顯示低價值卡片累積，再啟用衰減（如月 `-0.05`、下限 `0.2`）。

## 資料流與行為規則

### Capture（P1）

依 `source` 指派初始 `confidence`：

- `user-correction`: `0.7`
- `bug-fix`: `0.5`
- `retrospective`: `0.3`

並保留正向回饋調整規則：

- 確認有用可 `+0.1`（上限 `0.9`）。

### Recall（P1）

先比對語意相關性（tag/scope），再以 `confidence` 做優先排序，
最後以日期作 tie-break，確保高價值且近期的 lessons 優先載入。

### Evolution（P2）

先手動 promotion，不做早期自動化。
decay 僅在觀測條件滿足後啟用，避免無資料時過度設計。

## 錯誤處理與風險控制

1. `related` 目標缺失：忽略並警告（non-blocking）。
2. `_index.md` 缺失：
   - 無 cards：視為 first run，跳過 recall。
   - 有 cards：由現有 frontmatter 重建 index。
3. 單一權威來源原則：
   - `SKILL.md` 聚焦流程與行為。
   - `card-template.md` 聚焦欄位與格式。

## 測試與驗收設計

### 驗證指令

- `npx --yes skills-ref validate ./skills/lessons-learned`

### 分階段驗收

- P0：`SKILL.md` 明顯精簡，無重複/互斥規則。
- P1：`confidence` 規則可解釋 recall 載入理由；template 與 validation 對齊。
- P2：僅在條件滿足才啟用 decay，且可比較啟用前後效果。

### 非功能驗收

- 不新增平台依賴。
- 不新增背景常駐流程。
- 維持 skill 輕量與可維護性。

## 本次已核可決策

1. 採融合版策略。
2. 規劃範圍為完整 P0-P2。
3. `confidence decay` 採 P2 條件式導入。
4. `eval-cases.md` 刪除（不搬移）。

## 下一步

載入 `writing-plans`，將本設計轉成可執行的實作計劃（含步驟、檔案清單、驗證點與風險控制）。
