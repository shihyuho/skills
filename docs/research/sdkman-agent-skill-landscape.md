# SDKMAN agent skill 與自動化方案地景研究

> Research ticket: [#29](https://github.com/shihyuho/skills/issues/29)
>
> 查核日期：2026-08-30
>
> 性質：Wayfinder research evidence；本文不替 map Issue #24 作最終採用決策。

## 結論摘要

截至查核日，沒有找到一個經第一方來源驗證、可直接取代本 repo `sdkman` skill，且同時覆蓋下列五項契約的外部方案：

1. 在目前 worktree 內解析設定與執行 workload；
2. 保留 SDKMAN exact candidate identifier，包括 Java vendor suffix；
3. `install`、`default`、建立或修改 `.sdkmanrc` 前取得持久操作授權；
4. 區分 SDKMAN setup failure 與 Maven／Gradle／workload failure；
5. 以成功情境 token 成本為基準，且不犧牲 correctness／safety 的 benchmark。

最接近的可借鑑來源分成三類：

- `SamWang32191/codex-plugins` 的 `sdkman-switch-jdk` 是最接近的 agent skill：同樣要求把 `source`、`sdk use` 與 workload 放在同一 shell，且靜態文字很小；但只處理 JDK，沒有 worktree、vendor ambiguity、failure-layer 與 benchmark 契約，repository 也沒有可確認的 license。
- SDKMAN 官方 MCP server 提供 typed tool 與結構化錯誤的方向；但現況是 alpha，只完成 2／15 tools，唯一有副作用的 tool 是安裝 SDKMAN，且 tool schema 本身沒有逐次確認參數。
- GitHub 官方 `actions/setup-java` 能從 `.sdkmanrc` 解析 Java 版本與 vendor suffix，展示了可維護的 vendor mapping；但它把 SDKMAN identifier 轉成 GitHub distribution，並不保留 exact SDKMAN artifact identity，執行環境也只限 CI runner。

所有外部候選都沒有發布可與 map 契約直接比較的 LLM token／tool-call benchmark。下文只整理 keep／absorb／replace 的證據強弱，不做最終採用裁決。

## 研究問題與判準

本研究尋找 SDKMAN 官方、大型組織與社群提供的 agent skill、plugin、prompt、action 或自動化方案。搜尋引擎、GitHub code search 與 skills registry 只用來發現候選；功能、維護狀態、license、host 與執行模型均回到 repository metadata、manifest、source、release 或第一方文件查核。

### 本 map 的比較基線

比較基線來自本 repo 現行 `skills/sdkman/SKILL.md`、其 14 個 eval cases，以及 map Issue [#24](https://github.com/shihyuho/skills/issues/24)：

| 契約 | 比較問題 |
|---|---|
| Worktree | 是否只在目前 worktree 內找最近的 `.sdkmanrc`，保留原 cwd，且不跨越 worktree 邊界？ |
| Exact vendor | 是否保留完整 SDKMAN candidate identifier，而非把 `21.0.5-tem` 降格成只有 `21` 或任意替代 vendor？ |
| Persistent-action authorization | `install`、`default`、建立／修改 `.sdkmanrc` 等持久操作是否需明確授權？ |
| Failure layer | 是否能把 SDKMAN 初始化／切換失敗，與 Maven launcher、Gradle client／daemon、測試或 workload 失敗分開？ |
| Benchmark | 是否公開靜態 context、工具呼叫、失敗 probe／retry、總 input／output token 與每個成功情境 token？ |

## 候選總覽

「Token footprint 線索」只記錄可重現的靜態大小、tool 數或執行步數線索；沒有公開 LLM benchmark 時一律標為 unknown，不用文字長度臆測實際 token 成本。

| 候選 | 來源／host | 維護狀態（截至 2026-08-30） | License | 功能與執行模型 | Token footprint 線索 |
|---|---|---|---|---|---|
| [SDKMAN MCP Server](https://github.com/sdkman/sdkman-mcp-server/tree/9acd7f03cf25f16d46a120b2c3a34c96cb4a2a86) | SDKMAN 官方；支援 stdio MCP 的 host | README 標示 Alpha `v0.0.1`；目前 2／15 tools；無 GitHub release；目前 snapshot 最新 commit 為 2026-03-17 | [Apache-2.0](https://github.com/sdkman/sdkman-mcp-server/blob/9acd7f03cf25f16d46a120b2c3a34c96cb4a2a86/LICENSE) | Rust MCP server；目前查版本與安裝 SDKMAN | 2 個現行 tool descriptor；PRD 的效能目標是 wall time／memory，不是 LLM token；完整 benchmark unknown |
| [SDKMAN Prompt Library](https://github.com/sdkman/prompt-library/tree/3caa7609c224161eab9321296e87ddf1d5dd2165) | SDKMAN 官方；任何可引用 Markdown 的 agent host | 2026-04-27 仍有 commit；無 release | **Unknown**：repository metadata 與 tree 未找到 license | 通用 Kotlin／Rust／DDD／MCP rules 與規格、實作 plan templates；以 submodule／手動 prompt 引用 | 單檔約 1.6–10 KB，可選擇性載入；沒有 token benchmark |
| [SDKMAN Action](https://github.com/sdkman/sdkman-action/tree/0d6be56d0fc950d42944ae7b38f07affdfed65aa) | SDKMAN 官方；GitHub Actions | Repository 已 archived；只有 preview tags，未見穩定 release | **Unknown**：未見 license | Composite action；安裝 SDKMAN，依 input 執行 `sdk install` 或依 cwd `.sdkmanrc` 執行 `sdk env install` | 固定 workflow steps；不含 LLM context；agent token benchmark 不適用／unknown |
| [`actions/setup-java@v6.0.0`](https://github.com/actions/setup-java/tree/dd06d9cba3e5552c54d9f8ea23572deb30010f7c) | GitHub 官方；GitHub Actions runner | v6.0.0 於 2026-08-24 發布；持續維護 | [MIT](https://github.com/actions/setup-java/blob/dd06d9cba3e5552c54d9f8ea23572deb30010f7c/LICENSE) | Java toolcache action；可讀 `.sdkmanrc` 並映射 SDKMAN vendor suffix | Action inputs 與固定 JS workflow；沒有 LLM token benchmark |
| [`sdkman-switch-jdk`](https://github.com/SamWang32191/codex-plugins/blob/a262ea8dc834f91551dabe66d7fe6525716abc6e/plugins/dev/skills/sdkman-switch-jdk/SKILL.md) | 社群；Codex plugin／Agent Skill | Repo 未 archived，2026-08-24 有 push；plugin manifest `0.1.22`；無 GitHub release | **Unknown**：repository metadata 與 tree 未找到 license | 只切換本機已安裝 JDK；同一個 `bash -c` 內 source、`sdk use`、run command | `SKILL.md` 1,352 bytes；無 eval 或 token benchmark |
| [`setup-java-sdkman`](https://github.com/renatoathaydes/setup-java-sdkman/tree/1253a7eed45cc6191dc4bd9cacd3542878479569) | 社群；GitHub Actions runner | 最新 source／release 線索停在 2020；Node 12 action | [MIT](https://github.com/renatoathaydes/setup-java-sdkman/blob/1253a7eed45cc6191dc4bd9cacd3542878479569/LICENSE) | 以 exact SDKMAN JDK identifier 安裝並切換 Java，可追加 `sdkCommand` | 固定 action input；沒有 LLM token benchmark |
| [`Comcast/ansible-sdkman`](https://github.com/Comcast/ansible-sdkman/tree/e973093b593d991767b4199152d289c895fc7a5c) | 大型組織；Ansible host | Repo 未 archived；default branch 最後 code snapshot 為 2022-01-23 | [Apache-2.0](https://github.com/Comcast/ansible-sdkman/blob/e973093b593d991767b4199152d289c895fc7a5c/LICENSE) | Declarative role；管理 SDKMAN、candidate versions、defaults、config、uninstall | YAML role 固定 tasks；沒有 LLM token benchmark |
| [SDKMAN native CLI](https://github.com/sdkman/sdkman-cli-native/tree/v0.7.34) | SDKMAN 官方；標準 SDKMAN 安裝內的 native subcommands | v0.7.34 於 2026-04-30 發布；持續維護 | [Apache-2.0](https://github.com/sdkman/sdkman-cli-native/blob/v0.7.34/LICENSE) | Rust subcommands，仍由 shell `sdk` wrapper 呼叫；不是 agent package | 可減少部分 CLI 自行解析成本的可能性，但無 machine-readable／LLM benchmark 證據 |
| SDKMAN-specific skill registry 搜尋 | skills.sh／GitHub search；只作 discovery | 找到本 repo 與少量社群結果；不是完整 universe | 各 repo 分別判定 | bounded search，不是可執行方案 | 搜尋結果不能代表能力或 token 成本 |

### 排除但已查核的官方相鄰方案

- [`sdkman-release-action`](https://github.com/sdkman/sdkman-release-action/tree/d83abd0f746e1178a2a4f8ab7010ca921fcb1c59) 是 vendor 將新版本發布到 SDKMAN 的 action，不處理開發者本機候選解析或 workload；它維護活躍、Apache-2.0，但不在本 map 的 local toolchain scope。
- [`sdkman-default-action`](https://github.com/sdkman/sdkman-default-action/tree/38ca710dbacfada85ccfb609953e4c92a717e557) 透過 vendor API 把某版本設為 SDKMAN 生態系的預設版本，不等同使用者本機 `sdk default`；無可確認 license，且語意近似容易造成誤採用。
- SDKMAN 官方 prompt library 沒有找到專門操作 SDKMAN local environment 的 prompt、skill manifest 或 marketplace package。這是對目前 repository snapshot 的 bounded absence，不是對所有外部來源的存在性證明。

## 第一方證據詳查

### 1. SDKMAN 官方 MCP server

現況由 [README](https://github.com/sdkman/sdkman-mcp-server/blob/9acd7f03cf25f16d46a120b2c3a34c96cb4a2a86/README.md)、[tool registration](https://github.com/sdkman/sdkman-mcp-server/blob/9acd7f03cf25f16d46a120b2c3a34c96cb4a2a86/src/main.rs) 與 [installation source](https://github.com/sdkman/sdkman-mcp-server/blob/9acd7f03cf25f16d46a120b2c3a34c96cb4a2a86/src/installation.rs) 交叉驗證：

- 目前只有 `get_sdkman_version` 與 `install_sdkman` 兩個 tools，README 也明列為 2／15。
- `install_sdkman` 的 source signature 沒有 arguments。README 所寫的 optional `update_rc_files` 尚未出現在 tool schema；source 會先檢查 rc files 是否可寫，再決定 installer 是否更新它們。
- 安裝流程下載 `get.sdkman.io` installer text 後執行。README 的 SHA-256 security 敘述在目前 installation source 中找不到對應 checksum verification；因此「目前已驗證下載內容」不能成立。
- [error types](https://github.com/sdkman/sdkman-mcp-server/blob/9acd7f03cf25f16d46a120b2c3a34c96cb4a2a86/src/utils/error.rs) 有 unsupported platform、Bash 不可用、network、permission 與 internal error，這是可吸收的 typed setup-failure vocabulary。

[Draft PRD](https://github.com/sdkman/sdkman-mcp-server/blob/9acd7f03cf25f16d46a120b2c3a34c96cb4a2a86/specs/PRD.md) 規劃 15 tools 與 3 resources，但不能當成已交付能力：

- `sdk use` 因 shell-scoped 明確排除於 v1，替代方向是 persistent `set_default_version`。
- `.sdkmanrc`／`sdk env` 延到 P2／v2。
- PRD prose 提到執行 installer 前由使用者確認，但目前 tool schema 沒有確認欄位。host 是否另有逐次確認 UI 為 **unknown**，不能推定 MCP 自身已滿足 authorization contract。
- PRD 有 latency 與 memory KPI，未見 LLM static context、tool calls、retries 或 per-success token 指標。

與 map 的差距：沒有 worktree 模型、沒有 exact candidate discovery／switch、沒有 shell-local workload、沒有 launcher／workload failure layer，也沒有 map 要求的 benchmark envelope。它適合吸收 typed tools／errors 的設計線索，現況不足以作 replacement evidence。

### 2. SDKMAN 官方 Prompt Library

[Repository tree](https://github.com/sdkman/prompt-library/tree/3caa7609c224161eab9321296e87ddf1d5dd2165) 提供 Kotlin、Rust、DDD、hexagonal architecture、simple design、Kotest、MCP best practices，以及 feature specification／implementation plan templates。第一方 README 建議以 Git submodule 取得，再把所需檔案手動加入 prompt。

這種「按任務選擇小型 rule／template」可借鑑為 progressive disclosure；但 repository 沒有 SDKMAN environment resolution workflow，也沒有 `SKILL.md`、Codex／Claude plugin manifest 或 SDKMAN-specific eval。更重要的是，未找到 license，因此即使文字可借鑑，也不能把內容直接複製視為已獲授權。維護狀態可確認，直接重用授權為 **unknown**。

### 3. SDKMAN 官方與社群 GitHub Actions

#### `sdkman/sdkman-action`

[action definition](https://github.com/sdkman/sdkman-action/blob/0d6be56d0fc950d42944ae7b38f07affdfed65aa/action.yml) 顯示：Linux／macOS 先安裝 SDKMAN；若未給 candidate／version，便從 runner cwd 執行 `sdk env install`，否則執行 `sdk install <candidate> <version>`；最後把 candidate bin 加入 `GITHUB_PATH`。這是 CI provisioning，不是 shell-local agent execution。

它能接受 exact candidate/version，但所有主要路徑都會做持久安裝；workflow invocation 可視為 pipeline-level authority，並不等同 agent 對每次持久操作取得明確使用者授權。Repository 已 archived、未見 license、也沒有 worktree containment、failure taxonomy 或 token benchmark。

#### `actions/setup-java`

[`java-version-file` 文件](https://github.com/actions/setup-java/blob/dd06d9cba3e5552c54d9f8ea23572deb30010f7c/action.yml) 支援 `.sdkmanrc`；[parser source](https://github.com/actions/setup-java/blob/dd06d9cba3e5552c54d9f8ea23572deb30010f7c/src/util.ts) 把 `tem`、`sem`、`albba`、`amzn`、`graal` 等 suffix 映射到 setup-java distributions。

這證明 vendor suffix 應被明確解析，不應默默丟掉；但 mapping 產物是 GitHub Action 的 distribution 與 numeric Java version，不是原 SDKMAN candidate identifier。因此它是 vendor mapping 的 absorb evidence，不是 exact-vendor replacement。`set-default` 是明確 action input，但其預設值為 `true`；這是 workflow configuration，不是聊天中的持久操作授權。它只處理 Java、只在 CI runner 生效，沒有 worktree 或 workload failure layer。

#### `renatoathaydes/setup-java-sdkman`

[action source](https://github.com/renatoathaydes/setup-java-sdkman/tree/1253a7eed45cc6191dc4bd9cacd3542878479569) 保留完整 SDKMAN JDK identifier，也能執行額外 `sdkCommand`。但它會安裝 SDKMAN／JDK、只服務 GitHub Actions，而且停留在 Node 12 與 2020 維護線索。其 exact-ID handling 值得當歷史 evidence，維護與 host 差距使它不構成目前 replacement candidate。

### 4. 社群 Codex plugin：`sdkman-switch-jdk`

這是 registry 搜尋中唯一經 source 驗證、且與本 map 直接重疊的 SDKMAN-specific Agent Skill。其 [SKILL.md](https://github.com/SamWang32191/codex-plugins/blob/a262ea8dc834f91551dabe66d7fe6525716abc6e/plugins/dev/skills/sdkman-switch-jdk/SKILL.md) 與 [Codex plugin manifest](https://github.com/SamWang32191/codex-plugins/blob/a262ea8dc834f91551dabe66d7fe6525716abc6e/plugins/dev/.codex-plugin/plugin.json) 顯示：

- host 是 Codex plugin，skill 專門處理本機已安裝 JDK。
- 以 `${SDKMAN_DIR:-$HOME/.sdkman}/candidates/java` 枚舉已安裝 identifiers。
- 要求在同一個 `bash -c` 內 `source sdkman-init.sh`、`sdk use java <identifier>` 與執行 workload，正確承認 tool calls 可能開新 shell。
- 安裝 JDK、`sdk default`、修改 `.sdkmanrc` 僅在 explicit request 時執行。
- `SKILL.md` 為 1,352 bytes，對靜態 context 是有利線索；但 repo 沒有可確認 license，未找到此 skill 的 eval／token benchmark。

與本 map 的主要差距：只涵蓋 Java；未解析 worktree 內最近 `.sdkmanrc`；沒有 ambiguous vendor resolution；沒有 wrappers／Maven／Gradle daemon precedence；只在 `sdk use` 失敗時停止，沒有正式 failure-layer taxonomy；沒有 benchmark。它是值得 absorb 的最小 shell execution pattern，但是否能直接重用文字或 code 因 license 為 **unknown**。

### 5. 大型組織 provisioning：`Comcast/ansible-sdkman`

[Role defaults 與 tasks](https://github.com/Comcast/ansible-sdkman/tree/e973093b593d991767b4199152d289c895fc7a5c) 把 SDKMAN installation、candidate/version、default、configuration、flush、uninstall 表成 declarative desired state。這可借鑑兩點：持久操作要可枚舉，而 exact candidate/version 應是明確資料，不靠自然語言猜測。

但 playbook execution 本身就是對持久系統設定的授權，與 agent 每次 action 前的 interactive authorization 不同；它也不處理 shell-local workload、worktree 邊界、launcher／daemon failure 或 LLM benchmark。Default branch 的 code 維護線索停在 2022，因此只能作設計參照。

### 6. SDKMAN native CLI

[官方 README](https://github.com/sdkman/sdkman-cli-native/blob/v0.7.34/README.md) 說明 native components 已包含在標準 SDKMAN installation，仍透過 `sdk` wrapper shell function 使用。[`current` source](https://github.com/sdkman/sdkman-cli-native/blob/v0.7.34/src/bin/current/main.rs) 顯示輸出是 human-readable text，未見 stable JSON mode。

它可能降低部分 SDKMAN 查詢的 process／解析成本，但不能消除 `sdk use` 的 shell-local requirement，也不是 agent skill／plugin。是否能降低 map 的 token 指標仍為 **unknown**；需要同一 benchmark harness 實測，不能由 Rust 實作或 binary 大小推定。

## 契約差距矩陣

`✓` 表示 source 明確覆蓋；`△` 表示只部分覆蓋或 host 語意不同；`✗` 表示未覆蓋；`?` 表示第一方證據不足。

| 候選 | Worktree | Exact vendor | Persistent authorization | Failure layer | Benchmark contract |
|---|---:|---:|---:|---:|---:|
| SDKMAN MCP Server（現況） | ✗ | ✗ | ✗／? host UI | △ typed setup errors only | ✗ |
| SDKMAN Prompt Library | ✗ | ✗ | ✗ | ✗ | ✗ |
| SDKMAN Action | ✗ | △ exact input、但安裝導向 | △ workflow-level only | ✗ | ✗ |
| `actions/setup-java` | ✗ | △ suffix mapping、非 exact SDKMAN identity | △ workflow input | ✗ | ✗ |
| `sdkman-switch-jdk` | ✗ | △ 保留已知 ID、無 ambiguity policy | ✓ 文字規則 | △ switch stop only | ✗ |
| `setup-java-sdkman` | ✗ | ✓ input passthrough | △ workflow-level only | ✗ | ✗ |
| `Comcast/ansible-sdkman` | ✗ | ✓ declarative input | △ playbook-level only | ✗ | ✗ |
| SDKMAN native CLI | ✗ | △ CLI primitive only | ✗ | △ command exit only | ✗ |

## Keep／absorb／replace evidence table

這張表是「目前有哪些證據支持或反駁某個方向」，不是決策表。最終判斷仍需 map #24 將同一批 correctness／safety eval 與 token benchmark 跑在可比較版本上。

| 方向 | 支持證據 | 反證／未滿足條件 | 目前證據狀態 |
|---|---|---|---|
| **Keep** 現行 repo skill 作主體 | 現行設計已有五項 map 契約與 14 個 eval cases；所有外部候選至少缺兩項核心契約，多數缺 worktree、failure layer 與 benchmark | 現行 `SKILL.md` 為 8,518 bytes，可能有更小靜態 context 的空間；外部 typed tool 或 native primitive 也可能減少 probes | **支持保留作 benchmark baseline**；是否長期 keep 仍待量測 |
| **Absorb** 社群 skill 的最小 shell pattern | `sdkman-switch-jdk` 以 1,352-byte skill 正確表達 same-shell `source`／`sdk use`／workload，並將 persistent actions 綁到 explicit request | 只處理 JDK，無 worktree／vendor ambiguity／failure taxonomy／eval；license unknown，不能直接複製 | **強設計證據、弱直接重用證據** |
| **Absorb** `setup-java` vendor mapping | GitHub 官方 source 明列 SDKMAN suffix 到 distribution 的 mapping，可作 vendor recognition table 的參照 | Mapping 會改變 identity space，不能用來替換 exact SDKMAN candidate；Java／CI only | **強解析參照、非 replacement** |
| **Absorb** MCP typed tools／errors | 官方 MCP 已有 typed tool boundary 與 network／permission／platform error vocabulary；未來 resources 可能減少 ad-hoc probes | 現況 2／15、安裝 tool 無逐次確認參數、無 switch／worktree／workload；README 與 source 對 `update_rc_files` 不一致 | **可吸收介面方向；實作成熟度不足** |
| **Absorb** declarative persistent-action inventory | Comcast role 與官方／社群 actions 將 install、default、candidate/version 等持久狀態顯式化 | Pipeline／playbook authority 不等於 agent interactive authorization；有些候選 archived、stale 或無 license | **可吸收 action taxonomy，不吸收授權假設** |
| **Replace** 以 SDKMAN MCP server | 官方、Apache-2.0、host-neutral MCP 是正面訊號 | 缺五項契約中的大部分；現行唯一 mutation 是 installer；無 token benchmark | **目前證據反對直接 replace**；未來版本需重查 |
| **Replace** 以 `sdkman-switch-jdk` | 與現行核心 same-shell workflow 最接近，context 小，Codex host 可直接 discovery | 範圍縮成 JDK，缺 map 核心 eval，license unknown | **目前證據不足** |
| **Replace** 以 GitHub／Ansible automation | exact inputs 與成熟 automation model 可重現 | Host、生命週期與授權模型不同，不能執行本機 agent workload | **不符合本 map host／execution scope** |

## 後續驗證建議（不屬於本 ticket 決策）

若 map #24 要進入決策階段，應用同一 harness 比較至少三個變體：現行 skill、保留五項契約但採 `sdkman-switch-jdk` 式縮短文字的變體、以及以 MCP／native CLI 提供 read-only probes 的混合變體。每個變體都應記錄：

1. invocation 前載入的靜態 skill tokens；
2. tool call 數、失敗 probe 與 retry；
3. 總 input／output tokens；
4. 每個成功情境的 median tokens；
5. 14 個既有 correctness／safety cases，外加 MCP install authorization、README／source drift、worktree escape 與 vendor mapping regression cases。

目前沒有外部候選發布這組資料，所以任何「更省 token」或「可直接替換」的敘述都應維持 **unknown**，直到同一 workload 下實測。

## Sources

所有連結均指向第一方 repository、固定 commit／tag、manifest、source 或第一方 Issue：

- [SDKMAN MCP server snapshot](https://github.com/sdkman/sdkman-mcp-server/tree/9acd7f03cf25f16d46a120b2c3a34c96cb4a2a86)
- [SDKMAN prompt library snapshot](https://github.com/sdkman/prompt-library/tree/3caa7609c224161eab9321296e87ddf1d5dd2165)
- [SDKMAN Action snapshot](https://github.com/sdkman/sdkman-action/tree/0d6be56d0fc950d42944ae7b38f07affdfed65aa)
- [`actions/setup-java@v6.0.0`](https://github.com/actions/setup-java/tree/dd06d9cba3e5552c54d9f8ea23572deb30010f7c)
- [`SamWang32191/codex-plugins` snapshot](https://github.com/SamWang32191/codex-plugins/tree/a262ea8dc834f91551dabe66d7fe6525716abc6e)
- [`renatoathaydes/setup-java-sdkman` snapshot](https://github.com/renatoathaydes/setup-java-sdkman/tree/1253a7eed45cc6191dc4bd9cacd3542878479569)
- [`Comcast/ansible-sdkman` snapshot](https://github.com/Comcast/ansible-sdkman/tree/e973093b593d991767b4199152d289c895fc7a5c)
- [SDKMAN native CLI v0.7.34](https://github.com/sdkman/sdkman-cli-native/tree/v0.7.34)
- [Wayfinder map Issue #24](https://github.com/shihyuho/skills/issues/24)
- [Research ticket #29](https://github.com/shihyuho/skills/issues/29)
