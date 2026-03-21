# Writing Agents MD Skill Design

## Goal

建立 `writing-agents-md` skill，讓未來 LLM 在撰寫或重寫 `AGENTS.md` / `CLAUDE.md` 時，預設產出精簡、低噪音、低腐化風險的內容，而不是複製 `/init` 式 repo 導覽。

## Problem Statement

目前常見的 `AGENTS.md` / `CLAUDE.md` 產法有三個問題：

1. 把模型本來就能從 repo 發現的內容重寫一次，例如目錄結構、技術棧、scripts、常見檔案位置。
2. 把過多任務型、領域型、風格型指示塞進全域上下文，讓每個任務都付出 token 與注意力成本。
3. 把 legacy 技術、暫時做法、或會快速變動的檔案路徑寫進 always-on 規則檔，導致錨定錯誤與文件腐化。

三份來源共同指出：真正值得留在 `AGENTS.md` / `CLAUDE.md` 的，是模型無法從 repo 穩定推得、卻會明顯影響行為的全域約束與 landmines，而不是 repo 摘要。

## Design Direction

### 1. 用決策篩選取代 repo 導覽

skill 應先教模型做三層篩選，再決定內容是否能進 `AGENTS.md` / `CLAUDE.md`：

- `discoverable vs non-discoverable`
- `global vs task-specific`
- `stable vs likely-to-rot`

只有同時偏向 `non-discoverable`、`global`、`stable` 的內容，才應被保留。

### 2. 把 skill 定位成 rewrite / review 優先

第一版主軸不是「幫 repo 自動生一份完整 AGENTS.md」，而是：

- 審查現有 `AGENTS.md` / `CLAUDE.md`
- 刪除可從 repo 發現的噪音
- 保留真正必要的全域指引
- 指出哪些內容應搬到其他 skills

若 repo 根本沒有足夠的全域非顯而易見資訊，skill 也要允許輸出極短檔案，甚至建議暫時不要建立。

### 3. 內建反 `/init` 與 anti-anchoring 準則

skill 應直接禁止以下常見膨脹來源：

- package scripts 摘要
- repo 目錄與模組導覽
- 技術棧總結
- 可從程式碼輕易搜尋到的架構說明
- 未特別標記的 legacy 技術描述

若必須提到 legacy 技術，必須明確標成 `legacy`, `deprecated`, 或「不要沿用」類型說明，避免模型把它當預設做法。

### 4. 明確分流到 skills

skill 需要教模型辨識：

- 全域環境/工具限制 → 留在 `AGENTS.md` / `CLAUDE.md`
- 任務流程、設計偏好、前後端特定做法、驗證流程 → 改成 skill 或引用既有 skill

這樣 `AGENTS.md` / `CLAUDE.md` 會更像 routing / guardrail layer，而不是巨大的 repo 使用手冊。

### 5. 保留 friction-driven 維護心智模型

skill 應把 `AGENTS.md` / `CLAUDE.md` 定位成「尚未從系統層修掉的摩擦清單」：

- agent 一再用錯套件管理器
- agent 一再忘記某個必要驗證步驟
- agent 一再踩到不易從 repo 判斷的環境坑

優先順序應是先修 codebase / tooling / tests；只有在短期內無法消除摩擦時，才補一條最小規則。

## Intended Skill Package Structure

### `skills/writing-agents-md/SKILL.md`

主體包含：

- 觸發時機與適用範圍
- 三層篩選模型
- rewrite / review workflow
- 內容分類：保留、刪除、搬去 skill
- anti-anchoring 與 anti-rot guardrails
- 產出格式建議

### `skills/writing-agents-md/references/principles.md`

整理三份來源的核心原則、研究與實務觀察，供需要時延伸閱讀。

### `skills/writing-agents-md/references/checklist.md`

提供可執行清單，例如：

- 這條資訊是否可從 repo 直接發現？
- 這條是否每次任務都 relevant？
- 這條是否會因檔名、路徑、架構改動而快速過時？
- 這條是否其實應該是另一個 skill？

### `skills/writing-agents-md/references/examples.md`

放 `bad / better / good` 實例，幫模型快速比對。

## Intended SKILL.md Behavior

skill 被觸發時，模型應：

1. 先讀現有 `AGENTS.md` / `CLAUDE.md` 或需求描述。
2. 逐段標記為：`keep`, `delete`, `rewrite`, `move-to-skill`。
3. 產出一份精簡版本，優先保留：
   - 非顯而易見的工具限制
   - 環境特殊性
   - 會造成高成本失誤的 landmines
4. 對被刪除內容說明理由，避免再次長回去。
5. 若偵測到內容本質上是 workflow / policy / domain instruction，建議拆 skill，而不是繼續塞進全域檔。

## Example Keep/Delete Heuristics

### Keep

- `Use uv, not pip`
- `You are on WSL; path resolution across Windows/Linux is a common failure mode`
- `Run tests with --no-cache because fixtures can produce false positives`
- `legacy/` still has production imports; do not delete blindly`

### Delete or Move Out

- `This project uses React/Vite/TypeScript`
- `Packages live under /packages`
- `Run scripts with pnpm test, pnpm build, pnpm lint` when already visible in `package.json`
- `Backend services live in ...` style directory tours
- Frontend architecture preferences that only matter for some tasks

## Out of Scope

- 不自動維護階層式多層 AGENTS routing 系統
- 不直接替所有 repo 生成子目錄層級的 `AGENTS.md`
- 不在第一版加入自動 benchmark / description optimization 流程
- 不強制使用者一定要保留 `AGENTS.md` / `CLAUDE.md`

## Expected Outcome

skill 完成後，模型在處理 `AGENTS.md` / `CLAUDE.md` 時應更傾向：

- 先刪而不是先加
- 先判斷可否從 repo 自行發現
- 先把任務型規則搬去 skill
- 只留下真正全域、穩定、非顯而易見的約束
- 把 `AGENTS.md` / `CLAUDE.md` 當成最小 guardrail，而不是 repo 使用手冊
