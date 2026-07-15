# Research: `planning-with-files` plugin

> 研究對象:`/Users/matt/code/github.com/othmanadi/planning-with-files`(本機 clone,version 3.5.1)
> 一手來源:該 repo 的原始碼與內文。以下所有 `檔案:行號` 皆相對於該 repo 根目錄。
> 撰寫日期:2026-07-15

---

## TL;DR

`planning-with-files` 是一個 **Manus 風格的「檔案即工作記憶」規劃 skill**:對每個複雜任務,在專案目錄裡維護三個 Markdown 檔 —— `task_plan.md`(階段/決策/錯誤)、`findings.md`(研究發現)、`progress.md`(逐次工作日誌)—— 讓工作狀態離開 volatile 的 context window、落到 persistent 的磁碟上,於是能撐過 `/clear`、compaction 與 crash(`README.md:329-355`)。它靠 **SKILL.md 裡的行為指示 + Claude Code 五個生命週期 hooks** 驅動「隨時記錄」與「每回合把 plan 重新注入 context」。

對你最關心的兩點先講結論:

- **它沒有一個叫 `summary.md` 的專屬產出檔。** 最接近「summary」的持久檔是 `progress.md`(session log)。另外有兩種「摘要」是**臨時合成、不落檔**的:v3 模式下 `ledger-summary.sh` 合成的 `=== RUN LEDGER ===` 區塊(注入用),以及 `session-catchup.py` 印到 stdout 的「catchup report」。repo 內另有一個**選用慣例** `handoffs/<topic>.md`(Topic Handoff Pattern),那才是最像「跨 session 的豐富 recap artifact」的東西。
- **三個核心檔預設被 gitignore、且被設計成用完即棄**(root 模式下會被下一個任務覆寫)。它們是純 Markdown,任何 session/工具/人都能直接讀;但「自動注入 / 完成 gate / catchup / ledger 摘要」這些行為都耦合在本 skill 自己的 hooks/scripts 上。

---

## 1. 這 plugin 解決什麼問題、整體模型是什麼?

**一句話定位:** 給 AI coding agents 的「持久化、以檔案為基礎的規劃 skill」,把當前任務的執行狀態寫到磁碟並在每回合重新注入,解決 context rot 與 plan 遺失(`llms.txt:3`、`README.md:209`)。

**核心運作模型 —— RAM/Disk 類比:**

```
Context Window = RAM (volatile, limited)
Filesystem     = Disk (persistent, unlimited)
→ Anything important gets written to disk.
```
出處:`skills/planning-with-files/SKILL.md:86-91`、`README.md:350-355`。

- **3-file pattern**:每個複雜任務建立 `task_plan.md` / `findings.md` / `progress.md`(`README.md:338-346`、`skills/planning-with-files/SKILL.md:93-99`)。
- **Manus 原則對應**(`README.md:357-366`):filesystem as memory、attention manipulation(決策前重讀 plan)、error persistence、goal tracking、completion verification。
- **與 memory 工具的區別**:它管的是「當前任務的活躍執行狀態」(phases、status、dependencies、completion check),不是跨 session 的事實檢索;定位為 planning continuity 而非 retrieval,兩者互補(`README.md:565-567`)。
- **定位邊界**:不是 vector store、不是 MCP server(`llms.txt:15`)。
- 名義上是 Claude Code plugin,但透過 SKILL.md open standard 宣稱可裝在 60+ agents(`README.md:11`、`.claude-plugin/plugin.json:4`)。repo 裡有大量 per-IDE 鏡像目錄(`.codex/`、`.cursor/`、`.gemini/`、`.pi/` …),canonical 版本在 `skills/planning-with-files/`。

---

## 2. 它如何/何時讓 AI「隨時記錄現在在做的事」?

### 2a. 觸發機制:行為指示 + hooks 並用

寫入動作本身是**由 model 依 SKILL.md 的行為規範執行的**(不是 hook 幫你寫檔);hooks 負責「提醒寫」與「每回合把既有 plan 讀回 context」。

**SKILL.md 的行為規範(model 執行寫入):**
- Rule 4「Update After Act」:完成任一 phase 後把 status 由 `in_progress → complete`、記錄錯誤、記下改動檔案(`skills/planning-with-files/SKILL.md:114-119`)。
- Rule 2「2-Action Rule」:每做 2 次 view/browser/search 就立刻把重點存進檔(`:106-110`)。
- Rule 5「Log ALL Errors」:每個錯誤都進 plan 檔(`:120-129`)。
- Anti-pattern 明列「別用 TodoWrite 做持久化,改建 `task_plan.md`」(`:446-448`)。

**Claude Code 的五個 hooks(定義在 SKILL.md frontmatter,不是 plugin.json)**(`skills/planning-with-files/SKILL.md:6-29`;彙整表見 `README.md:404-411`、`docs/workflow.md:133-140`):

| Hook | 何時 | 做什麼 | 出處 |
|---|---|---|---|
| `UserPromptSubmit` | 每回合開頭 | 呼叫 `inject-plan.sh --context=userprompt`,注入 plan head + 進度摘要 | `SKILL.md:7-10` |
| `PreToolUse`(Write/Edit/Bash/Read/Glob/Grep) | 每次工具呼叫前 | 注入 plan head(legacy);autonomous/gated 模式下**丟棄**此注入 | `SKILL.md:11-15`、`inject-plan.sh:158-165` |
| `PostToolUse`(Write/Edit) | 每次寫檔後 | 印提醒:「Update progress.md with what you just did…」 | `SKILL.md:16-20` |
| `Stop` | agent 想停時 | 跑 `gate-stop.sh` / `check-complete.ps1`,回報是否全 phase 完成(legacy 純 advisory) | `SKILL.md:21-24` |
| `PreCompact`(`*`) | `/compact` 與 auto-compact 前 | 提醒在壓縮前把進度 flush 到 progress.md,附上 attested SHA | `SKILL.md:25-29`、`inject-plan.sh:217-225` |

也有 slash commands 觸發**建立**檔案:`/plan`、`/pwf`、`/planning`(`commands/plan.md`、`commands/pwf.md`、`commands/start.md:5-11`),但這些只是叫 model 去跑 skill 流程,不是自動化寫檔。

### 2b. on-disk 佈局

兩種佈局(由 `init-session.sh` 決定,`scripts/init-session.sh:4-23`):

- **Legacy / root 模式**(零參數):直接在專案根寫 `task_plan.md`、`findings.md`、`progress.md`(`init-session.sh:356-367`)。
- **Slug 模式**(給名字或 `--plan-dir`):寫到 `.planning/YYYY-MM-DD-<slug>/{task_plan,findings,progress}.md`,並用 `.planning/.active_plan` 指標記錄目前 active 的 plan(`init-session.sh:328-355`)。可多任務並行(`skills/planning-with-files/SKILL.md:224-244`、`docs/workflow.md:208-228`)。

v3 opt-in 模式會在 plan 目錄再放狀態 dotfile:`.mode`(autonomous/gate 標記)、`.nonce`(delimiter framing)、`.attestation`、`.stop_blocks`(gate 計數器)、以及 append-only 的 `ledger-<agent>.jsonl`(`init-session.sh:136-165`、`skills/planning-with-files/SKILL.md:392-395`)。

### 2c. 寫入格式/schema(有固定模板)

模板在 `templates/`(root)與 `skills/planning-with-files/templates/`。實際區塊:

**`task_plan.md`**(`templates/task_plan.md`):
- `## Goal` 一句話(`:8-14`)
- `## Current Phase`(`:16-21`)
- `## Phases` → 每個 `### Phase N: …` 底下有 checkbox 清單 + `- **Status:** pending|in_progress|complete`(`:23-84`)。這個 `### Phase` 與 `**Status:**` 字串是 `check-complete.sh`/`ledger-summary.sh` 用 grep 數 phase 的依據。
- `## Decisions Made`(表:Decision | Rationale,`:97-107`)
- `## Errors Encountered`(表:Error | Attempt | Resolution,`:109-120`)

**`progress.md`**(`templates/progress.md`)—— 這是「session log」,也是最接近人類可讀 summary 的檔:
- `## Session: [DATE]`(`:8`)
- 每個 `### Phase N` 有 Status / Started / Actions taken / Files created-modified(`:15-56`)
- `## Test Results`(表:Test | Input | Expected | Actual | Status,`:58-69`)
- `## Error Log`(表:Timestamp | Error | Attempt | Resolution,`:71-83`)
- `## 5-Question Reboot Check`(Where am I / going / goal / learned / done,`:85-105`)

**`findings.md`**(`templates/findings.md`):Requirements / Research Findings / Technical Decisions(表)/ Issues Encountered / Resources / Visual-Browser Findings(`:8-86`)。

**`task_plan_autonomous.md`**(v3,`skills/planning-with-files/templates/task_plan_autonomous.md`):在標準模板上加 `## Run Contract`(Mode / Gate cap / Stall window / Attestation policy / Single-writer rule,`:16-49`)、per-phase 的 `DependsOn`/`Owner`/`AcceptanceCheck` 行(`:109-145`)、`## Model Routing` 建議表(`:158-171`)。

### 2d. 更新節奏

**model 驅動、事件觸發,不是每個 turn 硬性寫檔:**
- 完成一個 phase 後更新 `task_plan.md` + `progress.md`(`skills/planning-with-files/SKILL.md:114-119`、`docs/workflow.md:153-165`)。
- 任何發現後、或每 2 次 view/browser/search 後更新 `findings.md`(2-Action Rule,`SKILL.md:106-110`、`docs/workflow.md:142-151`)。
- 錯誤發生當下即記(`SKILL.md:120-129`)。
- `PostToolUse` hook 在每次 Write/Edit 後提醒去更新 progress(`SKILL.md:16-20`)——提醒,不是自動寫。

---

## 3. 有沒有「summary」類的產出?

**沒有一個專屬的 `summary.md`。** 但有四種東西扮演不同層次的「摘要」角色,差別在「是否落檔、誰觸發、給誰看」:

### (A) `progress.md` —— 持久的人類可讀 session summary
- 檔名/位置:專案根或 `.planning/<slug>/progress.md`。
- 欄位:見 §2c(Session 日期、逐 phase 的 Actions/Files、Test Results 表、Error Log 表、5-Question Reboot)。
- 何時更新:貫穿 session、每個 phase(`templates/progress.md:113-114`)。由 **model** 更新,`PostToolUse` hook 提醒。
- 這是唯一「本來就落檔、之後任何人/session 都能直接讀」的摘要。

### (B) `=== RUN LEDGER ===` 合成摘要 —— 臨時、注入用(v3)
- **不是檔案**,是 `scripts/ledger-summary.sh` 即時合成後注入 context 的區塊,取代 legacy 的 `tail -20 progress.md`(`inject-plan.sh:272-291`)。
- 固定形狀(`ledger-summary.sh:19-27`、`:114-132`):
```
=== RUN LEDGER ===
entries: <N>
phases: <complete>/<total> complete
in_progress: <phase heading or none>
agent <name>: <last event type>
==================
```
- 刻意**不含時間戳、不含 disk 上任何 free text**,以維持 KV-cache 前綴穩定(`ledger-summary.sh:1-9`)。
- 背後資料:machine ledger `.planning/<id>/ledger-<agent>.jsonl`,append-only,每行一個 JSON:`{"tick","ts","agent","phase","event","summary","files"}`(`ledger-append.sh:26-32`、`:204-216`);event 限 `progress|phase_complete|error|gate_block|attest|note`(`ledger-append.sh:39`)。worker 各寫自己的 ledger,orchestrator 獨佔 `task_plan.md`(`SKILL.md:392-395`)。

### (C) `session-catchup.py` 的「catchup report」—— 臨時、reorient 用
- **不落檔**,印到 stdout(`scripts/session-catchup.py:517-555`)。
- 內容:標題 `SESSION CATCHUP DETECTED`、最後一次 planning 檔更新在哪個 session、未同步訊息數、`--- UNSYNCED CONTEXT ---`(重建自上次 planning 更新以後的對話/工具呼叫),結尾 `--- RECOMMENDED ---`:1) `git diff --stat` 2) 讀三個檔 3) 依上文更新 planning 檔 4) 繼續(`:526-555`)。
- 觸發:model 依 SKILL.md「FIRST: Restore Context」在新 session 手動跑(`SKILL.md:43-60`)。

### (D) `/status` 指令輸出 —— 臨時、螢幕上的一眼摘要
- `commands/status.md`:讀 `task_plan.md` 印 `📋 Planning Status`(current phase、phase 進度 %、phase 清單、error 數、三檔存在與否),刻意精簡只答「where am I」(`commands/status.md:22-49`)。

### (E) 附帶:Topic Handoff(見 §5)—— repo 內最像「豐富 recap artifact」的東西
`handoffs/<topic>.md` 是一個**選用慣例**:current state、commands、validation、risks、rollback、PR links;`progress.md` 當索引(`docs/workflow.md:230-251`、`docs/quickstart.md:92-110`)。這是文件裡描述的模式,**沒有自動化**、沒有模板檔。

---

## 4. 切回來/新開 session 如何 reorient?

有既定流程,寫在 SKILL.md 開頭「FIRST: Restore Context」(`skills/planning-with-files/SKILL.md:38-60`):

1. 若 `task_plan.md` 存在,**立刻**依序讀 `task_plan.md` → `progress.md` → `findings.md`(`:42`)。這個三檔讀取順序在多處重申(`inject-plan.sh` 注入順序、`session-catchup.py:553`、`docs/workflow.md:254-264` 的 5-Question 表)。
2. 跑 `scripts/session-catchup.py "$(pwd)"` 找上一個 session 之後未同步的 context(`:45-54`)。
3. 若有未同步:`git diff --stat` → 重讀 planning 檔 → 依 catchup + diff 更新 → 再繼續(`:56-60`)。

**自動的部分:** 每回合開頭 `UserPromptSubmit` hook 透過 `inject-plan.sh` 把 plan head(`head -50`)+ 進度/ledger 摘要注入(`inject-plan.sh:252-295`)。所以即使不手動操作,plan 也會被重新拉回 attention window —— 這正是 FAQ 說的 anti-context-rot 機制(`README.md:569-571`)。

**session-catchup.py 讀哪裡:** 依 IDE 而定 —— Claude Code 讀 `~/.claude/projects/<sanitized-path>/*.jsonl`(`session-catchup.py:47-72`、`:464-511`);OpenCode 讀 SQLite `~/.local/share/opencode/opencode.db`(`:266-453`)。它掃「最後一次寫 planning 檔」的點,收集其後到現在跨 session 的訊息(`:477-524`)。

**要 reorient 到哪個 plan(多 plan 時的解析順序,`inject-plan.sh:93-118`、`resolve-plan-dir.sh`):**
`$PLAN_ID` env → `.planning/.active_plan` → 最新 mtime 的 `.planning/<dir>/` → legacy 根 `./task_plan.md`。

**快速指令:** `/status`(§3D)給「where am I」;`/plan-goal`、`/plan-loop` 是 babysit-until-done 而非 reorient(`SKILL.md:274-318`)。沒有一個叫 `/resume` 或 `/catchup` 的專屬指令 —— reorient 是「讀三檔 + 跑 catchup script」的既定流程,不是單一 command。

---

## 5. 可攜性與借用角度(能否借它的產出當跨 session handoff/recap?)

### 產出的可攜事實

| 面向 | 事實 | 出處 |
|---|---|---|
| 路徑 | **per-repo,放在專案內**(根或 `.planning/<slug>/`)。**沒有中央集中存放**。 | `init-session.sh:328-367`、`SKILL.md:62-71` |
| 格式 | 三核心檔純 Markdown(有固定區塊);ledger 是 JSONL;狀態是 dotfile。 | `templates/*.md`、`ledger-append.sh:26-32` |
| 更新頻率 | model 驅動,per-phase / per-discovery / per-error。 | `SKILL.md:101-142` |
| 誰能讀 | 三核心檔任何工具/session/人都能直接讀(純 md);但「自動注入/gate/catchup/ledger 摘要」需要本 skill 的 hooks+scripts。 | 整體 |

### 與 git / AGENTS.md / 原生 session 的關係

- **git:互斥(預設不追蹤)。** `.gitignore` 忽略 `task_plan.md`、`findings.md`、`progress.md`(`.gitignore:13-15)`)、`.planning/`、`.plan-attestation`(`.gitignore:44`),連 skill 自己的 `CLAUDE.md` 也忽略。FAQ 明說:這是 working memory 不是 tracked deliverable,root 模式下**下一個任務會覆寫**,`.planning/<slug>/` 用完就不再 active,**沒有自動 archive**(`README.md:577-579`、`docs/workflow.md:115-127`)。想保留要自己 un-ignore 或搬走。
  - **例外(對你很關鍵):** `handoffs/<topic>.md` **不在** `.gitignore` 裡(已用 `git check-ignore` 驗證:三核心檔與 `.planning/` 被 match,`handoffs/topic.md` 沒有)。所以 Topic Handoff 檔預設就是 **git-tracked** 的 —— 這正是它適合當跨 session/跨 thread 持久 recap 的原因(`docs/workflow.md:230-251`)。
- **CLAUDE.md / AGENTS.md:互補。** 那些是靜態指示;planning 檔是動態執行狀態。本 repo 的 `AGENTS.md` 是給貢獻者/agent 的 repo 操作卡,與產出無耦合。
- **Claude Code 原生 session:互補 + 取代 TodoWrite。** 它明確反對用 TodoWrite 做持久化(`SKILL.md:446-448`);同時**讀取**原生 session store 來做 catchup(`session-catchup.py:464-511`),並用 hooks 把 plan 重新注入。

### 耦合點(borrow 時要注意)

1. **借「檔案」很乾淨,借「行為」會拖進整套 hook 系統。** 三核心檔是純 Markdown,任何人/session/工具直接可讀;但自動注入(`inject-plan.sh`)、完成 gate(`check-complete.sh:132-253`)、catchup(`session-catchup.py`)、ledger 摘要(`ledger-summary.sh`)全都要本 skill 的 hooks/scripts 到位才會動。
2. **兩種「摘要」是臨時 stdout,不可被別的工具「事後讀」。** RUN LEDGER 與 catchup report 都是即時再生,不落檔(§3B、§3C)。
3. **ledger 摘要需要 script(或 trivial 重寫)。** `ledger-*.jsonl` 本身可讀,但「摘要形狀」由 `ledger-summary.sh` 產生。
4. **v3 的注入耦合 attestation/nonce/mode 慣例。** autonomous/gated 模式下,未 attest 的 plan body 會被**拒絕注入**(`inject-plan.sh:202-215`、`:253-256`);`.active_plan`/`.mode`/`.nonce` 是本 skill 專屬慣例。這些只在本 skill 的 hook 流程內有意義,拿檔案本身去別處讀不受影響。
5. **prompt-injection 姿態會一起繼承。** `task_plan.md` 被 hooks 自動讀,故被當「不可信 data」用 BEGIN/END delimiter 包起、可選 SHA attestation 鎖定;`findings.md` 被視為納入第三方不可信內容(`SKILL.md:412-443`)。若把這些檔塞進另一套注入流程,要一併考慮這個信任模型。

### 借用為 layer-2 handoff/recap 的評估

**適合直接借(pure Markdown、語意清楚、不需本 skill 才讀得懂):**
- `progress.md` —— 固定區塊的 session log(Actions / Files changed / Test Results / Error Log / 5-Question Reboot),是最現成的 recap 底稿(`templates/progress.md`)。
- `task_plan.md` —— Goal + phases+status + Decisions 表 + Errors 表,是「現在在哪/還剩什麼/為何這樣決定」的快照(`templates/task_plan.md`)。
- **5-Question Reboot 框架**(Where am I / going / goal / learned / done)幾乎可直接當 handoff schema 的骨架(`SKILL.md:179-189`、`docs/workflow.md:254-264`)。
- **Topic Handoff 慣例 `handoffs/<topic>.md`** —— repo 內已存在的 handoff artifact 構想,且**預設 git-tracked**、跨多 session/thread 設計,欄位(state/commands/validation/risks/rollback/PR)正是 layer-2 recap 想要的(`docs/workflow.md:230-251`、`docs/quickstart.md:92-110`)。這點最值得借。
- `findings.md` —— 持久研究/決策沉澱。

**不適合直接借 / 要小心:**
- **預設 ephemeral + gitignore**:三核心檔設計成用完即棄、會被下一任務覆寫;要當持久 handoff 必須自己退出 gitignore 或另存。repo 明說 completion-triggered archive **未內建**(`README.md:577-579`、`docs/workflow.md:115-127`)。
- **per-repo、無中央存放**:跨 repo recap 得自己聚合;對「不同 repo 性質差很多」的情境,沒有現成的統一落點(`SKILL.md:62-71`)。
- **沒有單一 consolidated summary 檔**:要 recap 得從三檔拼;`progress.md` 最接近但不完整。
- **RUN LEDGER / catchup report 不落檔**:不能當「別的工具去讀的 artifact」,只能在本 skill 流程內即時再生。
- **borrow 行為 = 綁 hooks**:若想要「自動注入 + gate + catchup」的那套體驗,等於引入整個 hook/script 系統與其 attestation 信任模型;若只要「一份能被任何 session 讀的 md recap」,直接沿用 `progress.md`/`handoffs/*.md` 的**結構**即可,不必帶 runtime。

---

## 附:一手來源清單

- Skill 定義與 hooks:`skills/planning-with-files/SKILL.md`
- 模板:`templates/{task_plan,progress,findings}.md`、`skills/planning-with-files/templates/task_plan_autonomous.md`
- 建立/解析:`scripts/init-session.sh`、`scripts/resolve-plan-dir.sh`、`scripts/inject-plan.sh`
- 摘要/ledger:`scripts/ledger-summary.sh`、`scripts/ledger-append.sh`
- 完成 gate:`scripts/check-complete.sh`(與 `gate-stop.sh`)
- Reorient/catchup:`scripts/session-catchup.py`
- 指令:`commands/{plan,start,pwf,status,plan-goal,plan-loop,plan-attest}.md`
- 文件:`README.md`、`llms.txt`、`docs/workflow.md`、`docs/quickstart.md`、`MIGRATION.md`
- Git/manifest:`.gitignore`、`.claude-plugin/{plugin,marketplace}.json`
