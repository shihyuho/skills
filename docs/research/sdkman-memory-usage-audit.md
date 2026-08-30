# SDKMAN memory usage audit（Issue #26）

> 稽核日期：2026-08-30
>
> 範圍：`/Users/matt/.codex/memories/MEMORY.md` 直接指向、且含 SDKMAN 或 JDK 執行環境證據的 rollout summaries；另比對目前 `skills/sdkman/{SKILL.md,README.md,evals/evals.json}` 與 `docs/research/sdkman-skill-best-practices.md`。
>
> 證據規則：只採 memory／repo 內可追溯文字；summary 未記錄的 tool call 數、token、時間或 skill invocation 一律標為 `unknown`，不從結果反推過程。

## 結論

目前 `sdkman` skill 的**規格層**已處理 2026-08-12 重構前最明確的瓶頸：全 Bash output 掃描造成的 false positive 與固定開銷、跨 worktree 借用 `.sdkmanrc`、把 compiler target 誤當 shell JDK、忘記 shell-local 邊界、猜 vendor／patch，以及把環境初始化失敗誤報為 test failure。現行 SKILL、README 與 14 個 assertion-based eval prompts 對這些規則大致一致。（來源：`rollout_summaries/2026-08-12T14-18-16-UAuE-refactor_sdkman_skill_worktree_aware_resolution.md:21-44`；`skills/sdkman/SKILL.md:9-55`；`skills/sdkman/README.md:3-14`）

但 memory 無法證明這些規則在真實工作中已穩定被觸發與遵守。真實 rollout 仍出現先執行 formatter 才發現沒有 Java、硬編碼 `/Users/matt/.sdkman`、用 `;` 而非 failure-gated `&&` 串接 `sdk use` 與 workload，以及同一 repo 記錄 `25.0.1-tem`／`25-tem`、`mvn`／`./mvnw` 等不同路徑卻沒有 selection rationale。這些不是足以宣告現行 SKILL 有錯的證據，而是**adoption 與 observability bottleneck**；目前狀態是 `unknown`。（來源：`rollout_summaries/2026-08-14T04-27-43-xqWy-fairybell_pr_982_merge_conflict_resolution.md:21-28,37-42`；`rollout_summaries/2026-08-17T08-37-28-TS3r-issue_996_flow_field_mapping_namespace_pr1005.md:34-50`；`rollout_summaries/2026-08-26T01-59-07-0v9P-fairybell_issue_1023_remove_policy_envers_history_pr_1027.md:35-46`）

量測面只有一個可用歷史數字：舊 hook 的 100 次 no-op 約 3.55 秒；沒有移除後對照、with-skill／without-skill pass rate、真實 rollout 的 tool-call 數、failed-probe rate、token 或分類準確率。因此 Issue #26 若要判斷「memory usage 是否改善」，下一步應先建立可重跑 baseline，而不是再擴寫規則。（來源：`rollout_summaries/2026-08-12T14-18-16-UAuE-refactor_sdkman_skill_worktree_aware_resolution.md:21-31`；`docs/research/sdkman-skill-best-practices.md:143-165`）

## 語料範圍

### 核心 rollout：有實際 SDKMAN／launcher 行為

| 專案 | Rollout | 可證明內容 |
| --- | --- | --- |
| `shihyuho/skills` | SDKMAN worktree-aware 重構 | 舊 hook false positive、100 no-op／3.55 秒、規格重構與 14 evals。（來源：`MEMORY.md:2002-2010`；`rollout_summaries/2026-08-12T14-18-16-UAuE-refactor_sdkman_skill_worktree_aware_resolution.md:21-44`） |
| `softleader/fairybell` | PR #982 merge conflict | 第一次 formatter 因 PATH 無 Java 失敗；之後以 SDKMAN `25.0.1-tem` 成功啟動 wrapper。（來源：`MEMORY.md:2293-2297,2422-2422`；`rollout_summaries/2026-08-14T04-27-43-xqWy-fairybell_pr_982_merge_conflict_resolution.md:21-28,37-42`） |
| `softleader/fairybell` | Issue #996／PR #1005 | 記錄可用的 same-shell Java 25 invocation；focused tests 綠、full suite 有已知 manifest 例外。（來源：`MEMORY.md:1074-1082,1099-1108`；`rollout_summaries/2026-08-17T08-37-28-TS3r-issue_996_flow_field_mapping_namespace_pr1005.md:28-37,41-50`） |
| `softleader/fairybell` | Issue #1023／PR #1027 | 記錄 Java 25、`mvn -pl app -am` 與 same-shell `sdk use java 25-tem`；full suite 再遇已知 manifest 例外。（來源：`MEMORY.md:159-167,185-195`；`rollout_summaries/2026-08-26T01-59-07-0v9P-fairybell_issue_1023_remove_policy_envers_history_pr_1027.md:25-36`） |
| `softleader/kapok` | Issue #1098 diagnosis | 在 `sdk use java 17.0.6-tem` 下重跑 repro 兩次；窄測試缺少 reactor 會走遠端依賴，第一個 Spring probe 另有 harness 設定錯誤。（來源：`MEMORY.md:1681-1699,1713-1713`；`rollout_summaries/2026-08-12T03-48-08-gywu-diagnose_and_scope_issue_1098_dual_branch.md:18-40`） |

### 補充 rollout：只有 JDK baseline／runtime context

這些 summaries 可界定代表情境，但不能證明 sdkman skill 被載入或環境切換如何執行：

- Fairybell PR #919 的 summary 記錄 wrapper／Make 驗證與既有 `KapokVersion` failure；其 MEMORY task 另記 Java 25 baseline，並指示 Java 不可用時在 Maven 同 shell 使用 `sdk use java 25-tem`。Summary 本身沒有留下 selection command，因此只作補充情境。（來源：`MEMORY.md:2146-2154,2376-2376`；`rollout_summaries/2026-08-05T13-27-53-SqBL-fix_pr_919_spec_import_validation_and_push.md:21-25`）
- Fairybell Issue #1001 只記錄 Java 25 baseline 與最終驗證，沒有 SDKMAN command／failure。（來源：`rollout_summaries/2026-08-21T05-56-07-792M-fairybell_issue_1001_execution_history_pr_1013.md:7-27,44-57`）
- Fairybell PR #971 顯示 JDK 25 加兩顆 CPU／一個 common-pool worker 導致 timeout；這是 runtime capacity 分類，不是 shell JDK mismatch。（來源：`rollout_summaries/2026-08-12T15-22-30-EMRL-fairybell_pr_971_fresh_static_review.md:20-37`）
- Fairybell main CI diagnosis 在相同 SHA、Java 25 的 detached worktree 成功重跑 focused test，卻仍看到已知 `KapokVersion=null` full-suite failure；JDK 版本不是根因。（來源：`rollout_summaries/2026-08-11T09-59-05-vP3Z-fairybell_main_ci_brave_async_tracing_race.md:20-36`）
- Kapok Issue #1090 記錄 Java 17 build baseline 與 JDK `HttpsServer`／`keytool` API 使用；沒有 SDKMAN selection 過程。（來源：`rollout_summaries/2026-08-10T02-30-30-k3TL-kapok_issue_1090_trust_all_test_pr_1099.md:20-35`）

Hermes 與 Berth summaries 雖被廣義 `toolchain` 搜尋命中，但只談未來 Java/Vue toolchain preparation 或一般 toolchain exploration，沒有 JDK environment resolution、SDKMAN command、candidate 或 failure，故不納入行為統計。（來源：`rollout_summaries/2026-08-19T07-57-40-1WWO-hermes_agent_pool_afk_agent_spec_integration_branch.md:45-52`；`rollout_summaries/2026-08-19T02-29-15-p2Cs-berth_issue6_localization_spec_and_planning_baseline.md:7-11`）

## 已解決瓶頸

| 瓶頸 | Memory 證據 | 現行 repo 對應 | 判定 |
| --- | --- | --- | --- |
| 每個 Bash output 都掃 Java error 字串 | 舊 `PostToolUse` 會把 docs／source 文字誤判，100 no-op 約 3.55 秒；重構移除舊 hook 檔。（來源：`rollout_summaries/2026-08-12T14-18-16-UAuE-refactor_sdkman_skill_worktree_aware_resolution.md:21-24,33-34,47-53`） | frontmatter 只把明確版本／vendor／`.sdkmanrc`／實際 mismatch 列為觸發；research 明確反對 output-only detector。（來源：`skills/sdkman/SKILL.md:1-4`；`docs/research/sdkman-skill-best-practices.md:123-141`） | **已在規格／hook architecture 解決**；post-removal overhead 未量測。 |
| `sdk use` 跨 tool call 失效 | 重構把 shell-local invariant 寫入；Fairybell／Kapok 成功案例也都描述 same-shell。（來源：`rollout_summaries/2026-08-12T14-18-16-UAuE-refactor_sdkman_skill_worktree_aware_resolution.md:25-29,39-43`；`rollout_summaries/2026-08-17T08-37-28-TS3r-issue_996_flow_field_mapping_namespace_pr1005.md:34-37`） | SKILL 明示同一 invocation，範例使用 `sdk use ... && <command>`。（來源：`skills/sdkman/SKILL.md:7-10,70-79`） | **規格已解決**。 |
| 跨 worktree 借錯 `.sdkmanrc`／改變 cwd | 重構明確記錄 workload boundary、只在當前 worktree 搜尋、還原 cwd。（來源：`rollout_summaries/2026-08-12T14-18-16-UAuE-refactor_sdkman_skill_worktree_aware_resolution.md:25-30,33-37`） | SKILL lines 11–19 定義 boundary；eval 11–12 測「worktree 無 `.sdkmanrc`」與 nested cwd。（來源：`skills/sdkman/SKILL.md:11-19,81-94`；`skills/sdkman/evals/evals.json:121-141`） | **規格與 prompt coverage 已解決**；real rollout coverage `unknown`。 |
| compiler target／toolchain／launcher 混為一談 | 重構與 MEMORY 都要求分辨 launcher、client／daemon、task toolchain、application runtime。（來源：`MEMORY.md:2075-2076,2093-2093`；`rollout_summaries/2026-08-12T14-18-16-UAuE-refactor_sdkman_skill_worktree_aware_resolution.md:26-28,33-37`） | SKILL 決策表、launcher probe、Gradle JVM layers 完整對應；research 提供 Maven／Gradle 一手來源。（來源：`skills/sdkman/SKILL.md:21-57`；`docs/research/sdkman-skill-best-practices.md:61-121`） | **規格已解決**。 |
| 猜 exact id／vendor、靜默 install/default | 重構把 exact id 視為 reproducibility contract。（來源：`rollout_summaries/2026-08-12T14-18-16-UAuE-refactor_sdkman_skill_worktree_aware_resolution.md:26-27,39-43`） | SKILL 定義 selection order、缺 exact id 停止、persistent action 需授權；eval 3、13、14 覆蓋。（來源：`skills/sdkman/SKILL.md:36-49,96-106,122-131`；`skills/sdkman/evals/evals.json:28-38,143-163`） | **規格與 prompt coverage 已解決**；真實 missing-candidate 流程 `unknown`。 |
| 把 setup failure 說成 test failure | 重構新增 launcher probe 與 boundary reporting。（來源：`rollout_summaries/2026-08-12T14-18-16-UAuE-refactor_sdkman_skill_worktree_aware_resolution.md:28-30,33-37`） | SKILL 要先 probe、初始化成功後才啟動 workload，eval 14 明確要求「workload did not start」。（來源：`skills/sdkman/SKILL.md:51-55,122-129`；`skills/sdkman/evals/evals.json:154-163`） | **規格已解決**。 |

## 仍存在的瓶頸與 unknown

### 1. 真實工作仍偏 reactive，是否實際使用 launcher probe 為 unknown

PR #982 是最直接的現場證據：formatter 已啟動並失敗後，才發現 PATH 沒有 Java，再用 SDKMAN 重跑。Summary 沒記錄先執行 `./mvnw -version` 或其他 non-workload probe。（來源：`rollout_summaries/2026-08-14T04-27-43-xqWy-fairybell_pr_982_merge_conflict_resolution.md:15-28`）

現行 SKILL 已要求 Java availability 不明時先做 launcher probe，但沒有後續 rollout 證明 adoption rate。（來源：`skills/sdkman/SKILL.md:30-34,51-55`）

判定：**規則存在；真實採用率 `unknown`。**

### 2. 命令 gating 與可攜性沒有 real-rollout conformance evidence

PR #982 的 summary reference 使用 `...; sdk use java 25.0.1-tem; ./mvnw ...`；若 `sdk use` 失敗，第二個分號不保證 workload 停止。Issue #996 又硬編碼 `/Users/matt/.sdkman/bin/sdkman-init.sh`。現行 SKILL 範例則用 `${SDKMAN_DIR:-$HOME/.sdkman}` 與 `&&`，並要求初始化成功才啟動 workload。（來源：`rollout_summaries/2026-08-14T04-27-43-xqWy-fairybell_pr_982_merge_conflict_resolution.md:37-42`；`rollout_summaries/2026-08-17T08-37-28-TS3r-issue_996_flow_field_mapping_namespace_pr1005.md:34-37`；`skills/sdkman/SKILL.md:70-79,122-129`）

判定：**現行規格較安全；rollout 是否由 skill 產生、後續是否已一致改用安全型態皆 `unknown`。**

### 3. Candidate selection rationale 沒有被記錄

Fairybell summaries 分別使用 `25.0.1-tem` 與 `25-tem`；Kapok 使用 `17.0.6-tem`。沒有 summary 記錄 candidate 是使用者 exact request、`.sdkmanrc`、current/default、唯一相容 installed candidate，或人工選擇。（來源：`rollout_summaries/2026-08-14T04-27-43-xqWy-fairybell_pr_982_merge_conflict_resolution.md:21-28,41-42`；`rollout_summaries/2026-08-26T01-59-07-0v9P-fairybell_issue_1023_remove_policy_envers_history_pr_1027.md:35-36`；`rollout_summaries/2026-08-12T03-48-08-gywu-diagnose_and_scope_issue_1098_dual_branch.md:37-40`）

判定：版本成功執行可證明；**selection reproducibility `unknown`。**

### 4. Wrapper 使用不一致，原因 unknown

同一 Fairybell project 有 `./mvnw`（PR #982）與直接 `mvn`（Issues #996／#1023）紀錄；SKILL／README 都說優先 wrapper，但 summaries 沒交代直接 Maven 是否由 repo command、Makefile、使用者原命令或已選 SDKMAN Maven 驅動。（來源：`rollout_summaries/2026-08-14T04-27-43-xqWy-fairybell_pr_982_merge_conflict_resolution.md:21-23,41-42`；`rollout_summaries/2026-08-17T08-37-28-TS3r-issue_996_flow_field_mapping_namespace_pr1005.md:41-50`；`rollout_summaries/2026-08-26T01-59-07-0v9P-fairybell_issue_1023_remove_policy_envers_history_pr_1027.md:35-37`；`skills/sdkman/SKILL.md:25-34`）

判定：**是否違反「保留原 workload command」或「優先 wrapper」為 `unknown`。**

### 5. Real-world coverage 集中在 Java＋Maven

五份核心 rollout 都是 Java／Maven；沒有直接指向的 rollout 證明 `.sdkmanrc`、Gradle Client／Daemon／task toolchain、non-Java SDKMAN candidate、missing exact candidate、SDKMAN absent 或 direct-environment fallback 在真實任務運作。這些只存在 SKILL／synthetic eval 中。（來源：`skills/sdkman/SKILL.md:57-120`；`skills/sdkman/evals/evals.json:16-38,51-62,86-120,121-163`）

判定：**規格 coverage 有；production evidence `unknown`。**

### 6. README 適合作為行為摘要，但沒有 observability contract

README 準確概括 same-shell、worktree-local、wrapper/toolchain、vendor 與 persistent-state 邊界；它沒有告訴評估者應記錄 selection source、probe count、workload-started、exit status、state mutation 或 token。README 本來不必承擔完整內部格式，但目前 repo 其他地方也沒有 sdkman-specific run receipt schema。（來源：`skills/sdkman/README.md:3-14`；`skills/sdkman/SKILL.md:122-131`）

判定：**end-user 說明已足夠；可量測性仍缺。**

## 重複 tool calls 與 failed probes

| 現象 | 最小可證明次數 | 分類 | 是否浪費 |
| --- | ---: | --- | --- |
| 舊 hook 對 Bash output 做 no-op 掃描 | benchmark 明示 100 次 | 重複 detector call／固定 overhead | **已證明有固定時間成本**：約 3.55 秒／100 次；token 成本 `unknown`。（來源：`rollout_summaries/2026-08-12T14-18-16-UAuE-refactor_sdkman_skill_worktree_aware_resolution.md:21-24`） |
| PR #982 formatter 先失敗、設定 Java 後重跑 | 至少 2 次 formatter attempt | avoidable launcher preflight miss | 第一次 workload attempt 可由 launcher probe 避免；個別耗時／token `unknown`。（來源：`rollout_summaries/2026-08-14T04-27-43-xqWy-fairybell_pr_982_merge_conflict_resolution.md:21-28`） |
| Kapok #1098 repro 在 Java 17 下重跑 | 明示 2 次 | intentional reproducibility check | **不是浪費**；兩次一致 red 是診斷證據。（來源：`rollout_summaries/2026-08-12T03-48-08-gywu-diagnose_and_scope_issue_1098_dual_branch.md:18-26`） |
| Kapok #1098 窄測試未帶 reactor | 至少 1 次 | failed／mis-scoped dependency probe | 造成 remote dependency resolution；之後 `-am` reactor 才是可靠路徑。耗時／token `unknown`。（來源：`rollout_summaries/2026-08-12T03-48-08-gywu-diagnose_and_scope_issue_1098_dual_branch.md:28-40`） |
| Kapok #1098 第一個 Spring probe | 1 次 | harness setup failure | 缺 `ContextAnnotationAutowireCandidateResolver`，不是 issue 或 JDK failure；修正後 4 probes 綠。（來源：`rollout_summaries/2026-08-12T03-48-08-gywu-diagnose_and_scope_issue_1098_dual_branch.md:22-30,37-40`） |
| Fairybell 已知 `KapokVersion.getVersion() == null` full-suite failure | 4 份 rollout 各至少 1 次 | known repository／manifest environment failure | 是否是浪費 `unknown`：full suite 仍可能是必要 coverage，但重複失敗應可預先分類。來源分別為 PR #919、Issue #996、Issue #1023、main CI diagnosis。（來源：`rollout_summaries/2026-08-05T13-27-53-SqBL-fix_pr_919_spec_import_validation_and_push.md:21-25`；`rollout_summaries/2026-08-17T08-37-28-TS3r-issue_996_flow_field_mapping_namespace_pr1005.md:28-37`；`rollout_summaries/2026-08-26T01-59-07-0v9P-fairybell_issue_1023_remove_policy_envers_history_pr_1027.md:25-36`；`rollout_summaries/2026-08-11T09-59-05-vP3Z-fairybell_main_ci_brave_async_tracing_race.md:23-35`） |

除上述明示次數外，**每個 rollout 的總 shell/tool calls、候選清單 probe 次數、重複 `java -version`／`sdk list`／filesystem discovery 次數均為 `unknown`**；rollout summaries 沒有完整 tool trace，不能從 final command 數倒推。

## 錯誤分類稽核

| 類型 | 證據範例 | 正確處置 | 現行 coverage |
| --- | --- | --- | --- |
| Launcher unavailable | macOS 回報 `Unable to locate a Java Runtime`。（來源：`rollout_summaries/2026-08-14T04-27-43-xqWy-fairybell_pr_982_merge_conflict_resolution.md:21-28`） | 先做 non-workload launcher probe；選有證據的 installed JDK；初始化與原 workload 同 shell。 | SKILL 有；真實 preflight adoption `unknown`。（來源：`skills/sdkman/SKILL.md:30-34,51-55,70-79`） |
| SDKMAN initialization／missing exact candidate | real rollout 無案例；eval 14 是 synthetic。（來源：`skills/sdkman/evals/evals.json:154-163`） | 停止、報 workload 未開始、詢問 exact install，不 substitute。 | Prompt coverage 有；real evidence `unknown`。 |
| Compiler target／toolchain layer | 舊設計會從 `release`／`source`／`target` 推錯 shell JDK。（來源：`MEMORY.md:2075-2076,2093-2093`） | 分 launcher、Maven/Gradle toolchain、Gradle Client/Daemon、task/application runtime。 | SKILL／research 已覆蓋。（來源：`skills/sdkman/SKILL.md:51-57`；`docs/research/sdkman-skill-best-practices.md:61-121`） |
| Reactor／dependency topology | Kapok narrow test 從 remote 解依賴，`-am` reactor 才可靠。（來源：`rollout_summaries/2026-08-12T03-48-08-gywu-diagnose_and_scope_issue_1098_dual_branch.md:28-40`） | 保持正確 JDK，但修正 Maven reactor scope；不要再切 JDK。 | sdkman eval 未有代表 case。 |
| Test harness setup | Spring probe 缺 resolver。（來源：`rollout_summaries/2026-08-12T03-48-08-gywu-diagnose_and_scope_issue_1098_dual_branch.md:22-30`） | 修 harness；不要歸因 JDK／production bug。 | sdkman eval 未有「JDK 正確但 harness 錯」case。 |
| Known repo／manifest environment failure | Fairybell `KapokVersion.getVersion() == null`。（來源：`rollout_summaries/2026-08-17T08-37-28-TS3r-issue_996_flow_field_mapping_namespace_pr1005.md:28-37`） | 報 workload 已啟動、focused/CI 與 full-suite scope分開；不可叫 SDKMAN setup failure。 | Completion contract 可表達，但 eval 只有 init-fails case，缺 init-success/workload-fails case。（來源：`skills/sdkman/SKILL.md:122-129`；`skills/sdkman/evals/evals.json:154-163`） |
| Runtime capacity/concurrency | Jenkins JDK 25＋2 CPUs 只剩一個 common-pool worker。（來源：`rollout_summaries/2026-08-12T15-22-30-EMRL-fairybell_pr_971_fresh_static_review.md:34-39`） | 修 executor/capacity assumption；切同版或他版 JDK 都不是已證明修法。 | 現行 description 的「actual Java version failure」可避免誤觸，但無專門 negative eval。 |
| Quoted／historical error text | 舊 hook 讀 docs/source 也會 false positive。（來源：`rollout_summaries/2026-08-12T14-18-16-UAuE-refactor_sdkman_skill_worktree_aware_resolution.md:21-24,33-34`） | 檢查 command、exit status 與實際 failed layer。 | eval 6 已覆蓋。（來源：`skills/sdkman/evals/evals.json:63-72`） |

## Token 浪費模式

### 已證明

1. 舊 catch-all hook 對不相關 Bash call 產生固定 work，且會注入 false-positive diagnosis；唯一量化是 100 no-op 約 3.55 秒。它證明 latency waste，不證明 token 數。（來源：`rollout_summaries/2026-08-12T14-18-16-UAuE-refactor_sdkman_skill_worktree_aware_resolution.md:21-24`）
2. 未先 probe launcher 會多一次 failed workload attempt；PR #982 已證明至少發生一次。（來源：`rollout_summaries/2026-08-14T04-27-43-xqWy-fairybell_pr_982_merge_conflict_resolution.md:21-28`）
3. 未使用正確 Maven reactor scope 會產生一次無效／偏離目的的依賴解析 probe；Kapok #1098 已證明此模式。（來源：`rollout_summaries/2026-08-12T03-48-08-gywu-diagnose_and_scope_issue_1098_dual_branch.md:28-40`）

### 可能但未證明，故標 unknown

- skill discovery／載入本身用了多少 tokens：`unknown`。
- 舊 hook false positive 額外產生多少模型輸入／回應 tokens：`unknown`。
- 每次候選版本 discovery 是否重複 `ls`／`sdk list`／`java -version`：`unknown`。
- 反覆跑已知 `KapokVersion` failure 的 full suite 是否屬不必要成本：`unknown`；沒有每次任務的驗證授權與 coverage necessity 資料。
- 現行 14 evals 相對 baseline 是否節省 tokens 或 tool calls：`unknown`；repo 只有期望輸出與 assertions，沒有 run artifacts。

## Evals 與缺少的代表情境

目前 14 個 evals 已涵蓋：ephemeral switch、worktree-local `.sdkmanrc`、missing vendor、compiler release negative、Gradle toolchain／daemon、quoted error、真實 class-file mismatch、non-Java candidate、wrapper preference、cwd restoration、vendor ambiguity，以及 init-vs-test failure。（來源：`skills/sdkman/evals/evals.json:1-166`）

但所有 14 個 case 的 `files` 都是空陣列，所以它們主要測模型輸出語義，不會建立真實 worktree、candidate tree、current symlink、wrapper exit status 或 shell process boundary。（來源：`skills/sdkman/evals/evals.json:5-21,29-45,52-68,75-91,99-114,121-159`）

缺少的代表情境如下：

1. **真實 macOS launcher unavailable**：`./mvnw -version` 先失敗為 `Unable to locate a Java Runtime`，已安裝 exact Temurin 後原 workload 只啟動一次；來自 PR #982。（來源：`rollout_summaries/2026-08-14T04-27-43-xqWy-fairybell_pr_982_merge_conflict_resolution.md:21-28`）
2. **`sdk use` 失敗必須阻止 workload**：專門辨識 `;` 與 `&&` gating，並驗證 exit status；現行 SKILL 要求這點，但沒有 executable eval。（來源：`skills/sdkman/SKILL.md:70-79,122-129`）
3. **Portable SDKMAN_DIR**：SDKMAN 不在 `$HOME/.sdkman`，檢查不能硬編碼使用者路徑；真實 summary 曾硬編碼。（來源：`rollout_summaries/2026-08-17T08-37-28-TS3r-issue_996_flow_field_mapping_namespace_pr1005.md:34-37`；`skills/sdkman/SKILL.md:59-68`）
4. **初始化成功、workload 因已知 manifest／repo issue 失敗**：須正確報「workload started and failed」，不能再切 JDK；對應四次 Fairybell 記錄。（來源：`rollout_summaries/2026-08-05T13-27-53-SqBL-fix_pr_919_spec_import_validation_and_push.md:21-25`；`rollout_summaries/2026-08-17T08-37-28-TS3r-issue_996_flow_field_mapping_namespace_pr1005.md:28-37`；`rollout_summaries/2026-08-26T01-59-07-0v9P-fairybell_issue_1023_remove_policy_envers_history_pr_1027.md:25-36`；`rollout_summaries/2026-08-11T09-59-05-vP3Z-fairybell_main_ci_brave_async_tracing_race.md:23-35`）
5. **Maven reactor topology failure**：正確 Java 17 下，without `-am` 走 remote dependency，with `-am` 才可靠；不可誤判 JDK。（來源：`rollout_summaries/2026-08-12T03-48-08-gywu-diagnose_and_scope_issue_1098_dual_branch.md:28-40`）
6. **Runtime capacity negative**：JDK 25＋低 CPU 導致 common-pool starvation，預期不觸發 candidate switch。（來源：`rollout_summaries/2026-08-12T15-22-30-EMRL-fairybell_pr_971_fresh_static_review.md:34-39`）
7. **真實 tracked `.sdkmanrc` 多 candidate**：Java／Maven／Gradle 同時宣告，其中一個 exact id missing；驗證不 partial-start workload，也不 `sdk env install`。目前只有文字設計。（來源：`docs/research/sdkman-skill-best-practices.md:41-53`；`skills/sdkman/SKILL.md:81-100`）
8. **SDKMAN absent／另一 version manager 存在**：要報 SDKMAN path unavailable 並遵守 project owner，不自行改 `JAVA_HOME`；目前只有 SKILL 規則。（來源：`skills/sdkman/SKILL.md:47-49,59-68`）
9. **`current` link 原本不存在**：`sdk use` 可能建立 link；比較 direct-environment fallback 是否保持 state。Research 與 SKILL 都提到副作用，eval 未實作。（來源：`docs/research/sdkman-skill-best-practices.md:33-39`；`skills/sdkman/SKILL.md:70-79,108-120`）
10. **Real Gradle Client／Daemon／task JVM fixture**：目前只有 prompt assertion，沒有 wrapper、daemon criteria 與 toolchain 的可執行狀態。（來源：`skills/sdkman/evals/evals.json:51-62,109-119`）

## 缺少的可量測 baseline

### 現有 baseline

| 指標 | 現有值 | 限制 |
| --- | ---: | --- |
| 舊 hook no-op latency | 約 3.55 秒／100 invocations | 沒有移除後對照、分布、host／機器資訊或 token。（來源：`rollout_summaries/2026-08-12T14-18-16-UAuE-refactor_sdkman_skill_worktree_aware_resolution.md:21-24`） |
| Eval 數 | 14 | 只有 prompts／expected output／assertions；沒有 execution results、baseline runs 或 fixture state。（來源：`rollout_summaries/2026-08-12T14-18-16-UAuE-refactor_sdkman_skill_worktree_aware_resolution.md:28-31`；`skills/sdkman/evals/evals.json:1-166`） |
| 真實成功案例 | 可辨識 Fairybell 3 份 operational summaries、另有 1 份 MEMORY reusable entry，以及 Kapok 1 份 selected-JDK 記錄 | summaries 未記錄 skill 是否載入、selection probes、總 calls、time、tokens 或 state diff。 |
| 真實 launcher miss | PR #982 至少 1 次 | 沒有 probe-to-workload timeline 或修正前後 calls/time。 |

### 建議建立的最小 baseline（proposal）

以現有 14 prompts 加上前節 10 個缺口，建立 executable fixtures；每個 case 分別跑 **without-skill baseline** 與 **with-skill**，至少記錄：

1. routing：是否載入 skill；正向 recall、負向 precision。
2. environment probes：workload 啟動前 tool calls、重複 probes、failed probes。
3. correctness：candidate selection source、exact id、vendor、workload cwd、原 command、workload 是否啟動、exit status、error category。
4. persistence：candidate `current` link、SDKMAN default/config、project files 的 before/after diff。
5. efficiency：wall time、input/output tokens、tool-call 數、首次正確分類前 turns。
6. discrimination：assertion pass rate 與 with-skill 相對 baseline 的 delta；不能只報 coverage。Repo 已有 lesson 明確指出 coverage prompt 可能無法區分 baseline。（來源：`docs/lessons/eval-coverage-and-discrimination-are-different.md:23-27`）

建議的主要 outcome metrics：

- `environment_success_rate`：初始化正確且原 workload 在同一 shell 啟動的比例。
- `misclassification_rate`：把 docs text、harness、reactor、known repo failure 或 runtime capacity 問題誤叫 JDK mismatch 的比例。
- `avoidable_failed_probe_rate`：可由既有 evidence／launcher probe 避免的 failed calls ÷ 全部 environment calls。
- `command_preservation_rate`：command、cwd、exit status 三者都保留的比例。
- `unauthorized_persistence_rate`：未授權 install/default/config/project file/current-link mutation 的比例，目標 0；`current` link 例外須分列。
- `tool_calls_to_workload_start`、`tokens_to_workload_start`、`wall_time_to_workload_start`：用中位數與 p95，比較 with/without skill。

### 無法從現有證據建立的 baseline

- 每個 rollout 的實際 token 總量與 SDKMAN-specific token share：`unknown`。
- 現行 skill 的 trigger precision／recall：`unknown`。
- 14 evals 的 with-skill／baseline pass rate：`unknown`。
- hook 移除後 100 no-op 的相同機器 latency：`unknown`。
- real `.sdkmanrc`、Gradle、non-Java candidate、missing candidate 的成功率：`unknown`。

## 對目前文件的整體判定

- `SKILL.md`：decision contract 完整，且已吸收 memory 中可辨識的主要失敗分類；最缺的是可觀測 receipt／executable conformance，而不是更多規則。（來源：`skills/sdkman/SKILL.md:11-131`）
- `README.md`：準確、簡潔地呈現 end-user decision-changing behavior；沒有發現與 SKILL 的語義衝突。（來源：`skills/sdkman/README.md:1-24`）
- `evals/evals.json`：行為 coverage 廣，但全是無 fixture 的 assertion prompts；無法量測 shell/process/filesystem state 或 skill 的增量價值。（來源：`skills/sdkman/evals/evals.json:1-166`）
- `docs/research/sdkman-skill-best-practices.md`：一手來源研究與現行 SKILL 大致一致，也早已列出 hook、trigger、command coverage 與 retry verification checklist；目前未見 checklist 的 run artifact。（來源：`docs/research/sdkman-skill-best-practices.md:7-29,31-59,115-165`）

最 defensible 的 Issue #26 下一步是：**先把上述真實 memory 情境轉成 executable、with/without-skill baseline，並收集 tool-call／token／classification／state-diff 指標；量測後再決定是否需要修改 skill。** 現有證據不支持直接宣告需要另一輪文字重構。
