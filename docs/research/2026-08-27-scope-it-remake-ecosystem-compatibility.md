# `scope-it-remake` 與常見工程 workflow 的相容性研究

日期：2026-08-27

## 結論

`scope-it-remake` 現有的 `scope → tickets → delivery` frontier，以及以可觀察行為、驗收證據、blocker、stable pointer 為核心的 artifact contract，能接住 Superpowers 與 `addyosmani/agent-skills` 已完成且已核准的規劃產物；但不應把任一套 ecosystem 綁成 runtime dependency、偵測對象或具名 provider profile。

建議維持 ecosystem-neutral，做三個最小 contract 調整：

1. 將「可主動調用的 producer contract」與「既有 artifact 的 acceptance contract」分開。
2. 在 Delivery Map 記錄 artifact 的角色與狀態，至少區分 `scope`、`delivery tickets`、`execution plan`；不要把 plan task、檔案或 coding step 自動當成 ticket。
3. 將「寫入核准」與「內容核准」拆成可獨立滿足的 gate；frontier 只在必要 gate 都有 durable evidence 時才前進。

另建議支援一條 ecosystem-neutral 的 compact path：當工作已明確、只有一個 delivery unit，而且上游流程刻意不產生 spec／plan file 時，可將已核准的對話 checkpoint 或既有 tracker issue 視為 scope artifact，避免為了符合管線而製造沒有決策價值的文件。

## 研究方法與版本

依專案規範，先用 `ghq list -e -p <org>/<repo>` 精確解析本機官方 mirror，再由協作者於兩個 repository 的乾淨 `main` 執行 `git pull --ff-only`。本文只使用更新後、工作樹乾淨的 checkout，不使用更新前的讀取結果。

| Ecosystem | 本機 mirror | 更新後 HEAD | 版本描述 |
|---|---|---|---|
| Superpowers | `/Users/matt/code/github.com/obra/superpowers` | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | `v6.3.0` |
| addyosmani/agent-skills | `/Users/matt/code/github.com/addyosmani/agent-skills` | `5a5ea45e806f82273549fd85e60adb95d55f510d` | `0.6.7-2-g5a5ea45` |

外部事實只引用上述兩個官方 repository 的 SHA-pinned source。本文沒有以第三方文章、搜尋摘要或 marketplace 說明作為判斷依據。

受評估的 `scope-it-remake` 當時尚未 commit；研究與整合結果後來保存於 `1df4eea5632e1ccd69d3289768515d6640799370`。本文保留當時研究快照，以下引用固定為該歷史版本；畢業後的 runtime 以 [scope-it](../../skills/scope-it/SKILL.md) 為準。

- frontier 固定為 `scope → tickets → delivery → done`，每次只處理一個 frontier（[`skills/scope-it-remake/SKILL.md`](https://github.com/shihyuho/skills/blob/1df4eea5632e1ccd69d3289768515d6640799370/skills/scope-it-remake/SKILL.md#L69-L82)）。
- active producer 要先回傳 mutation-free draft；ticket producer 要回傳 title、end-to-end outcome、acceptance evidence、blocker 與獨立可執行性（[`references/sources.md`](https://github.com/shihyuho/skills/blob/1df4eea5632e1ccd69d3289768515d6640799370/skills/scope-it-remake/references/sources.md#L48-L107)）。
- completed artifact 現在使用獨立 acceptance contract，並記錄 role、revision 與 approval state（[`references/artifacts.md`](https://github.com/shihyuho/skills/blob/1df4eea5632e1ccd69d3289768515d6640799370/skills/scope-it-remake/references/artifacts.md#L5-L42)）。
- delivery frontier 只在有 scope-owned worktree changes 或需要多 ticket 原子落地時載入額外規則（[`skills/scope-it-remake/SKILL.md`](https://github.com/shihyuho/skills/blob/1df4eea5632e1ccd69d3289768515d6640799370/skills/scope-it-remake/SKILL.md#L90-L99)）。

## 相容性總覽

| Seam | Superpowers | addyosmani/agent-skills | 判斷 |
|---|---|---|---|
| 已核准 scope artifact | Architectural design doc 高度相容；bounded chat design 需要 compact path | Spec file 高度相容；大型需求另有 capability map | 可用 artifact acceptance contract 統一接入 |
| 主動 scope producer | 有自己的分類、逐段核准、寫檔、commit、書面複核與固定 handoff，不能安全折疊成一個 checkpoint | 有自己的 phase gates，且 spec 是 living document | 不應由 runtime 偵測或控制；消費已核准 artifact 較穩定 |
| Delivery tickets | Implementation-plan tasks 不是 tracker tickets | 明確支援 external tracker，一個 task 對一個 tracker item；預設仍是 Markdown todo | 只有符合 ticket semantic contract 的 tracker items 才可直接採用 |
| Execution plan | 有明確 plan artifact 與 execution handoff | 固定產生 `tasks/plan.md`，下游逐 task 執行 | Map 應另記 `execution plan`，不可塞入 ticket graph |
| Implementation handoff | 執行時要求 isolated workspace 並先 review plan | 逐一 vertical slice、test、verify、commit | `scope-it-remake` 應提供 pointer 與第一個可執行 ticket，不接管執行 workflow |

## Superpowers

### 確認事實

1. Brainstorming 先將工作分類為 spike、bounded 或 architectural；三條路徑的 artifact 重量不同，但 implementation 前都保留使用者核准 gate。Bounded path 明定 design 只留在 chat，不建立 spec file 或 implementation plan；architectural path 才寫 design doc 並轉交 plan workflow（官方 source：[`obra/superpowers@b36e082`, `skills/brainstorming/SKILL.md:14-61`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/brainstorming/SKILL.md#L14-L61)、[`75-103`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/brainstorming/SKILL.md#L75-L103)）。
2. Architectural path 會先由使用者逐段核准 design，之後寫入並 commit design doc，再由使用者 review 書面 spec；只有通過第二個 gate 才進入 writing-plans（官方 source：[`brainstorming/SKILL.md:94-103`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/brainstorming/SKILL.md#L94-L103)、[`105-145`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/brainstorming/SKILL.md#L105-L145)）。
3. Writing-plans 的 task 是 reviewer gate 與獨立 test cycle 的最小單位，但內容刻意深入到 exact files、interfaces、2–5 分鐘 coding/test/commit steps；plan 同時必須指回 spec（官方 source：[`obra/superpowers@b36e082`, `skills/writing-plans/SKILL.md:21-52`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/writing-plans/SKILL.md#L21-L52)、[`54-129`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/writing-plans/SKILL.md#L54-L129)）。
4. Plan 完成後會讓使用者選 execution workflow；執行端會先確保 isolated workspace、critical review plan、逐 task 驗證，遇到 blocker 或 plan gap 即停下詢問（官方 source：[`writing-plans/SKILL.md:153-171`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/writing-plans/SKILL.md#L153-L171)、[`executing-plans/SKILL.md:16-64`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/executing-plans/SKILL.md#L16-L64)）。
5. Worktree workflow 會先偵測既有 isolation；若已在 linked worktree 就沿用，否則需要既有偏好或使用者同意後才建立（官方 source：[`obra/superpowers@b36e082`, `skills/using-git-worktrees/SKILL.md:16-61`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/using-git-worktrees/SKILL.md#L16-L61)）。

### 相容 seam

- 已完成且通過書面 review 的 architectural design doc，具備 objective、architecture、boundaries、testing 與 durable revision，可直接對應 scope artifact。
- Writing plan 對 spec 有明確 pointer，且有 reviewable tasks、interfaces、驗證步驟，可作為獨立的 execution-plan artifact；它能補強 delivery handoff，但不需要進入低解析度 Delivery Map 的 ticket graph。
- 「先核准、再 implementation」與 `scope-it-remake` 的 mutation gate、每 frontier 停止點方向一致。
- 若 `scope-it-remake` 因 Carry 已建立 isolated worktree，後續 executor 的「偵測既有 isolation」可安全沿用；若沒有 Carry，workspace 建立仍可留給 executor。

### 衝突

- 現有 common source contract 假設 source-specific confirmation 可以折進單一 frontier checkpoint；Superpowers architectural path 至少有 design approval 與 written-spec review 兩個不同語義的 gate，不能視為同一件事。
- Bounded path 明確不產生 spec file 或 plan document。若 `scope-it-remake` 一律要求獨立 scope publication，會反向增加該 workflow 刻意移除的 ceremony。
- Writing-plan task 可包含 component、file、interface 與 coding steps。即使 task 可獨立 review，也不能因此自動滿足「ticket node 必須是 end-to-end delivery outcome」的限制。
- Brainstorming 對 architectural path 有固定下一步，writing-plans 也有固定 execution handoff。讓 `scope-it-remake` 在 runtime 直接 invoke 並重新安排其順序，會同時有兩個 workflow owner。

### 推論

- 最穩定的接法是 artifact-first：讓上游 workflow 完成自己的 gate，再由 `scope-it-remake` 讀取已核准 design／plan；不是將該 workflow 註冊成 provider。
- Bounded work 若已有明確核准的 chat design，且只需一張 delivery ticket，可以用 durable transcript pointer 或既有 issue 承擔 scope evidence；這需要 compact scope acceptance，而不是另造 spec file。
- Implementation plan 裡的 task 只有在每個 task 經語義檢查後確實代表 end-to-end outcome，才可轉為 ticket proposal；否則應保留為 ticket 內部 execution plan，或以一張 ticket 指向完整 plan。

## addyosmani/agent-skills

### 確認事實

1. Meta workflow 依 phase 選 skill，典型生命週期是 intent／idea → spec → task breakdown → context／source verification → incremental implementation → verify／review／ship；skill 是按順序執行的 workflow，不是可任意抽取的 suggestion（官方 source：[`addyosmani/agent-skills@5a5ea45`, `skills/using-agent-skills/SKILL.md:12-42`](https://github.com/addyosmani/agent-skills/blob/5a5ea45e806f82273549fd85e60adb95d55f510d/skills/using-agent-skills/SKILL.md#L12-L42)、[`130-163`](https://github.com/addyosmani/agent-skills/blob/5a5ea45e806f82273549fd85e60adb95d55f510d/skills/using-agent-skills/SKILL.md#L130-L163)）。
2. Spec workflow 明定 `SPECIFY → PLAN → TASKS → IMPLEMENT`，每一 phase 都由 human review；大型 request 先建立另有語義的 capability map，再按 module id 各自跑完整生命週期（官方 source：[`addyosmani/agent-skills@5a5ea45`, `skills/spec-driven-development/SKILL.md:22-65`](https://github.com/addyosmani/agent-skills/blob/5a5ea45e806f82273549fd85e60adb95d55f510d/skills/spec-driven-development/SKILL.md#L22-L65)）。
3. Spec template 包含 objective、commands、project structure、style、testing、boundaries、success criteria 與 open questions；implementation 前要有 human approval、specific criteria 與 repository file（官方 source：[`spec-driven-development/SKILL.md:67-148`](https://github.com/addyosmani/agent-skills/blob/5a5ea45e806f82273549fd85e60adb95d55f510d/skills/spec-driven-development/SKILL.md#L67-L148)、[`235-245`](https://github.com/addyosmani/agent-skills/blob/5a5ea45e806f82273549fd85e60adb95d55f510d/skills/spec-driven-development/SKILL.md#L235-L245)）。
4. Task breakdown 先以 read-only plan mode 讀 spec、code patterns、dependencies、risks；偏好能交付 working/testable functionality 的 vertical slices。每個 task 有 description、acceptance criteria、verification、dependencies 與 likely files（官方 source：[`addyosmani/agent-skills@5a5ea45`, `skills/planning-and-task-breakdown/SKILL.md:22-104`](https://github.com/addyosmani/agent-skills/blob/5a5ea45e806f82273549fd85e60adb95d55f510d/skills/planning-and-task-breakdown/SKILL.md#L22-L104)）。
5. Plan 永遠寫到 `tasks/plan.md`；task list 預設是 `tasks/todo.md`。只有 repository guidance 或使用者指定 external tracker 時，才改成每 task 一個 tracker item，並把 acceptance、verification 與 dependencies 映射到 tracker fields／links（官方 source：[`planning-and-task-breakdown/SKILL.md:143-157`](https://github.com/addyosmani/agent-skills/blob/5a5ea45e806f82273549fd85e60adb95d55f510d/skills/planning-and-task-breakdown/SKILL.md#L143-L157)）。
6. Implementation 逐一完成 vertical slice，對每一 slice implement、test、verify、commit，再進下一 slice；每個 task 完成後仍有完整 verification gate（官方 source：[`addyosmani/agent-skills@5a5ea45`, `skills/incremental-implementation/SKILL.md:21-64`](https://github.com/addyosmani/agent-skills/blob/5a5ea45e806f82273549fd85e60adb95d55f510d/skills/incremental-implementation/SKILL.md#L21-L64)、[`199-245`](https://github.com/addyosmani/agent-skills/blob/5a5ea45e806f82273549fd85e60adb95d55f510d/skills/incremental-implementation/SKILL.md#L199-L245)）。

### 相容 seam

- 已核准 spec 的欄位完整覆蓋 scope source 所需的 observable outcome、boundaries、constraints、validation seams 與 unresolved questions。
- External-tracker 模式與 ticket contract 高度一致：一 task 一 tracker item、明確 acceptance、verification、dependency，而且 vertical slicing 追求 working/testable outcome。
- 固定的 `tasks/plan.md` 可作為 execution-plan artifact；tracker item index 則可作為 Delivery Map 的 ticket pointers，兩者不必重複內容。
- 各 phase 有 human review，與 frontier checkpoint 的漸進核准方向一致；incremental implementation 也能從「第一張可執行 ticket」自然接手。

### 衝突

- 預設 task list 是 local Markdown checklist，不是具有 native containment／blocker relationship 的 tracker tickets。不能只因欄位相似就聲稱 delivery-ticket publication 已完成。
- Capability map 的 node 是 module，目的在 spec 前分解產品能力；Delivery Map 的 node 是 delivery ticket。兩張圖不可互換，也不能把 module dependency 直接發布成 ticket blocker。
- Spec 是 living document，決策或 scope 改變時會先更新 spec。`scope-it-remake` 若只記 artifact pointer、不記 revision／approval state，可能在後續 session 誤用已變更但未重新核准的內容。
- Active planning workflow 會同時產生 plan file 與 task target，且有自己的 phase review。現有「每 frontier 只做該 frontier writes」需要能接受一個 source 產生多種、但角色不同的 artifact，或只在完成後 ingest。

### 推論

- External tracker 已由 repository guidance 或使用者指定時，其 tasks 是目前兩套 ecosystem 中最接近直接 ticket source 的產物；仍應逐項驗證 end-to-end outcome 與獨立可驗證性，而不是按來源名稱放行。
- 使用預設 `tasks/todo.md` 時，最小互通方式是把它與 `tasks/plan.md` 一起記成 execution-plan evidence，再由 ticket frontier 決定要復用一張既有 issue，或另外提出真正的 tracker tickets。
- Capability map 應作為 scope artifact 的 supporting pointer；它可幫助判斷 ticket 邊界，但不能取代 Delivery Map。

## 建議的最小 ecosystem-neutral contract 調整

以下調整只描述能力與 artifact，不在 runtime 文件中加入任何 ecosystem 名稱、安裝要求、偵測規則或具名 profile。

### 1. 分開 producer 與 artifact acceptance

保留現有 active producer contract，另加一個 completed artifact acceptance contract。既有 artifact 不必證明它的 producer 能被目前 agent invoke 或能在單一 checkpoint 後 resume；只需證明：

- 有 durable pointer，能取得 revision 或等價 identity 時一併記錄；
- 能映射到該 frontier 的必要內容欄位；
- 有內容核准狀態及其 durable evidence，或明確標為仍待核准；
- unresolved decisions 與 contradictions 已分離；
- readback 結果與 Map 記錄一致。

這可修正目前 Selection 第 3 項雖允許 completed artifact，卻仍讓它受 active source resume／write-preview 能力約束的語義混淆。

### 2. 在 Map 記錄 role、mode、revision 與 approval state

建議將單純的 source name／pointer 擴成最小結構：

```markdown
## Sources
- Scope: <identity or pending>; mode: <invoked | supplied-artifact | pending>
- Tickets: <identity or pending>; mode: <invoked | supplied-artifact | pending>

## Artifacts
- Scope: <pointer>; revision: <identity or unavailable>; approval: <approved | pending>
- Tickets: <pointers>; revision: <identity or unavailable>; approval: <approved | pending>
- Execution plan: <pointer or none>; revision: <identity or unavailable>; approval: <approved | pending>
```

`identity` 是 lineage，不是下次 runtime invocation 的授權。若 artifact revision 改變，既有內容核准不能自動沿用。

### 3. 明定 artifact role，不按外觀自動升格

- `scope` 說明 what／why／boundaries／success evidence。
- `delivery ticket` 是 tracker 可執行、可驗證、可排 blocker 的 end-to-end outcome。
- `execution plan` 說明 how，包括 files、interfaces、coding steps、commands 與 commits。
- supporting maps／module indexes 只是 scope evidence，不是 ticket graph。

Plan task 只有通過 ticket semantic contract 時才可提出為 ticket；有 checkbox、task title 或 dependency list 都不足以自動升格。

### 4. 分開 mutation approval 與 content approval

將現有「source-specific confirmation points folded into current frontier checkpoint」收斂為：

- `scope-it-remake` 的 checkpoint 擁有即將發生之 writes 的 mutation approval；
- artifact-owning workflow 可以保留一個以上的 content approval gate；
- publication 完成不代表內容已核准；
- frontier 只有在必要 mutation approval、content approval 與 readback 都有證據後才前進。

如此可接住「先核准方向、寫入 artifact、再 review 書面內容」與「spec／plan／tasks 分 phase review」等流程，而不需要知道產物來自哪一套 skill。

### 5. 加入 compact scope acceptance

當 durable evidence 顯示工作是單一、明確且只有一個 delivery unit，可允許：

- 已核准的 conversation checkpoint 或既有 tracker issue 作為 scope artifact；
- 單一既有 issue 同時承擔 delivery ticket；
- 不要求另建 spec file、plan file 或多張 tickets。

仍須記錄 observable result、boundaries、acceptance evidence、核准 pointer 與 readback。這是縮短 artifact，不是降低核准或驗證門檻。

### 6. 保持 implementation handoff 邊界

Delivery frontier 應回傳：

- 第一張可執行 ticket；
- scope、ticket 與 execution-plan pointers；
- 已核准的 delivery topology；
- workspace／branch 已存在時的 durable pointer，否則標示由 executor 決定。

不要為了相容常見 workflow 而預先綁定 executor、建立 worktree、選 subagent 策略或規定 commit cycle。若 Carry 已觸發 Planning Carrier，後續 executor 應能偵測並沿用既有 isolation；若未觸發，workspace policy 留給 execution workflow。

## 不建議採用的設計

- 不在 `SKILL.md` 或 runtime references 出現 Superpowers 或 addyosmani/agent-skills 名稱。
- 不掃描安裝目錄、skill 名稱或 marketplace 來決定 provider。
- 不新增兩套 ecosystem 的 fixed compatibility profile。
- 不把 upstream module graph、plan phase、Markdown checklist 或 coding steps 直接轉成 Delivery Map ticket nodes。
- 不讓 source lineage 變成下一次 invoke explicit-only skill 的授權。
- 不由 `scope-it-remake` 覆蓋 artifact-owning workflow 的核准順序。

## 最終判斷

目前規劃的方向可融入兩套常見 workflow，但「融入」應定義為 capability/artifact interoperability，而非 runtime orchestration：

- 對 Superpowers：architectural design 與 implementation plan 可被穩定 ingest；bounded work 需要 compact path；plan tasks 不直接等於 tickets。
- 對 addyosmani/agent-skills：spec 與 external-tracker tasks 幾乎直接符合 scope／ticket contract；預設 Markdown tasks 應保留為 execution-plan evidence；capability map 不等於 Delivery Map。
- 對 `scope-it-remake`：frontier order 不必改。真正要改的是 source contract 的分層、artifact role/state，以及多 gate 的完成判定。
