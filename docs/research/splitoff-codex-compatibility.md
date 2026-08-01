# Research: `splitoff` 的 Codex 相容性

> 研究對象：`skills/splitoff/SKILL.md`
> 一手來源：OpenAI 官方 Codex 文件、本機 `codex-cli 0.144.5` 的 help，以及目前 Codex desktop 暴露的 tool metadata。
> 撰寫日期：2026-08-01

## TL;DR

可以支援 Codex，但不能把目前的 Claude Code 指令逐字翻成 Codex CLI 指令。

建議把 `splitoff` 改成「依 host capability 選擇 handoff 機制」：

1. Claude Code 維持現有 `/handoff` + `claude --bg` 流程。
2. Codex 的預設實作使用原生 subagent delegation；這是官方支援的背景／平行工作模型，使用者可從 CLI 的 `/agent` 或 `/subagents` 檢視 child threads。[Subagents](https://developers.openai.com/codex/subagents)
3. 若使用者明確要求建立可獨立回訪的 Codex task，且目前 host 提供 task/thread creation capability，再使用該 host adapter；不要把特定內部 tool name 寫成可攜的 `SKILL.md` 契約。
4. 不建議在 skill 裡以 detached `codex exec` 模擬原生背景 task；它可以執行 handoff prompt，但沒有 `claude --bg --name` 與 `claude agents` 的等價管理體驗。[Non-interactive mode](https://developers.openai.com/codex/noninteractive)

### `codex exec` 與 Codex App 的實測

2026-08-01 以本機 `codex-cli 0.144.5` 建立 non-interactive thread `019fbab4-13e1-7633-b771-8f02ef81b8d4`。執行完成後，Codex desktop 的 recent-thread 清單沒有該精確 ID。它仍可用 `codex exec resume <SESSION_ID>` 續接，因此「CLI 可 resume」不等於「App 側欄可見」。

原因是 `codex exec` 儲存為 `Exec` source，而歷史清單的預設 filter 只含 interactive `Cli`、`VsCode` source；除非 host 特別要求 `Exec`，不要依賴它成為 App 可見 chat。[v0.144.5 App Server source filter](https://github.com/openai/codex/blob/rust-v0.144.5/codex-rs/app-server/README.md#L368-L381)

## 現行 skill 的 Claude Code 耦合

`skills/splitoff/SKILL.md` 目前依賴三個 Claude Code 專屬能力：

- 另一個 `/handoff` skill 產生暫存摘要檔。
- `claude --bg --name ... --model ...` 建立 named background agent。
- `claude agents` 讓使用者後續管理 agent。

這三者在 Codex CLI 沒有一對一的同名介面，因此不能只替換 executable 名稱。

## Codex 有哪些可用機制

### 1. Subagents：最接近且最可攜的預設

Codex 官方把 subagents 定義為由主 agent 委派的 child agent threads；主 agent 可 spawn、steer、wait，最後彙整結果。CLI 可用 `/agent` 或 `/subagents` 檢視 active threads。這與 `splitoff` 的「把整理過的 context 交給 fresh background agent」最接近，而且 skill 或 `AGENTS.md` 可以明確要求 delegation。[Subagents](https://developers.openai.com/codex/subagents)

差異是 ownership：subagent 是 parent-owned work，結果回到目前 task；它不是一個使用者日後獨立繼續的 sibling task。Codex 官方把 `/new`、`/fork`、`/resume` 等 chat lifecycle 與 subagent delegation 分開描述。[CLI slash commands](https://developers.openai.com/codex/cli/slash-commands)

### 2. 獨立 Codex task：只有 host adapter 能可靠建立

目前 Codex desktop runtime 的 tool metadata 有建立 task、設定 title、指定 local/worktree target、等待進度與傳送 follow-up 的能力；但這些是 host/session capability，不是公開的可攜 `SKILL.md` primitive。

因此 skill 應描述意圖，例如「若使用者明確要求獨立 task，使用 host 提供的 task creation capability」，而不是承諾所有 Codex surface 都存在固定的 `create_thread` tool。Codex IDE 也不支援 plugins；desktop 與 CLI 才支援，所以 plugin skill 本身就不能假設每個 Codex surface 相同。[Plugins](https://developers.openai.com/codex/plugins)

若要自行開發穩定的外部整合，Codex App Server 提供 `thread/start`、`thread/fork`、`thread/resume`、`thread/list`、`turn/start` 等 JSON-RPC 方法；這適合 repo 另帶一個 orchestrator，不適合只靠 instruction-only skill 直接驅動。[App Server](https://developers.openai.com/codex/app-server)

### 3. `codex exec`：可執行，但不是原生背景 task

本機 `codex-cli 0.144.5` 顯示：

```text
codex exec [OPTIONS] [PROMPT]
  prompt 可由參數或 stdin 傳入
  -m, --model <MODEL>
  -C, --cd <DIR>
  --json
  --ephemeral
  codex exec resume <SESSION_ID>
```

官方文件也把 `codex exec` 定位為 non-interactive automation，可輸出 JSONL 並 resume persisted session。[Non-interactive mode](https://developers.openai.com/codex/noninteractive)

但是它缺少 `--bg`、`--name` 與原生 background-agent job list；在 OS 層做 detached process 也無法自然處理 fresh approval。若 repo 未打算維護 supervisor／App Server orchestrator，不應把它當 `splitoff` 的 Codex 預設。

本機 `codex fork` 可以從既有 session 建立 fork，並接受 optional prompt；它是 interactive／chat lifecycle，不是「立刻回傳、由背景 agent 工作」的替代品。

## 建議的相容設計

將 `splitoff` 的共同契約收斂成：

1. 把目前目標、已完成事項、未完成事項、關鍵檔案、驗證狀態與限制整理成 self-contained handoff prompt。
2. 尊重使用者明確指定的 model／reasoning；未指定時沿用 host 的 inheritance/default，不強迫 agent 猜出目前 model slug。
3. 選擇目前 surface 的第一方機制：
   - Claude Code：現有 named background agent。
   - Codex：原生 subagent delegation。
   - Codex 且使用者明確要求獨立 task：可用時採 host task adapter。
4. 只有在使用者明確要求 shell automation，且接受缺少 native task UI／approval flow 時，才使用 `codex exec` 外部程序。
5. 若 surface 沒有符合語意的 capability，清楚回報不支援，不以未記錄的 private tool 或猜測指令替代。

`SKILL.md` 不宜硬編 `spawn_agent`、`create_thread`、`wait_threads` 等 tool 名稱。這些名稱會依 Codex host／session 改變；skill 應表達 delegation 與 ownership 語意，讓當前 runtime 對應到它實際暴露的工具。

## 建議的 UX 分流

- `$splitoff <name>`：背景委派；Claude Code 建 background agent，Codex 建 subagent。
- `$splitoff --task <name>`：使用者明確要求獨立可回訪的 task；只在 host 有 task creation capability 時執行。
- `$splitoff --model <model> <name>`：把使用者明確指定的 model 傳給可支援的 host；不支援時先告知，而不是靜默忽略。

這樣保留原本的 user-invoke 分類與 handoff 目的，同時把「背景 delegation」和「建立新的 user-owned task」兩種不同 ownership 語意說清楚。

## 限制與待驗證項目

- Subagent 的 naming、model inheritance、最大 nesting／concurrency 由目前 Codex host 與 agent configuration 決定，不能假設完全等同 Claude Code flags。[Subagents](https://developers.openai.com/codex/subagents)
- Plugins 僅在 Codex desktop／CLI 可用；IDE 只能依 standalone skill installation 支援同一套流程。[Plugins](https://developers.openai.com/codex/plugins)
- App Server 仍是需要版本管理的 integration surface；WebSocket transport 在官方文件中標示 experimental，若未來採用應鎖定與測試 client/server schema。[App Server](https://developers.openai.com/codex/app-server)
- 真正修改 `splitoff` 前，應以 Codex desktop 與 CLI 各做一次 end-to-end eval：驗證 handoff context、cwd、user-specified model、parent/subagent completion，以及 `--task` 的回訪體驗。

## 一手來源

- [Codex subagents](https://developers.openai.com/codex/subagents)
- [Codex CLI slash commands](https://developers.openai.com/codex/cli/slash-commands)
- [Codex non-interactive mode](https://developers.openai.com/codex/noninteractive)
- [Codex App Server](https://developers.openai.com/codex/app-server)
- [Codex plugins](https://developers.openai.com/codex/plugins)
- 本機 `codex --version`、`codex --help`、`codex exec --help`、`codex fork --help`（2026-08-01）
- 本機 `skills/splitoff/SKILL.md`
