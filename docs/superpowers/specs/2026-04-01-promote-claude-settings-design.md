# promote-claude-settings — Design Spec

## Goal

建立一個 skill，將當前專案的 `.claude/settings.local.json` 內容互動式地 promote 到全域 `~/.claude/settings.json`。

## Trigger

使用者說「promote settings」、「把 local settings 升級到全域」、「sync settings to global」等類似指令。

## Skill 形式

純 SKILL.md 指引，無腳本。Claude 在對話中直接讀取 JSON、比對差異、互動確認、寫入。

## 流程

### Step 1 — 讀取

- 讀取 `.claude/settings.local.json`（當前專案目錄下）
- 讀取 `~/.claude/settings.json`（全域）
- 若 local 不存在或為空物件 `{}`，告知使用者並結束

### Step 2 — Flat diff

對 local 的每個頂層 key 做 deep comparison，產出分類清單：

| 狀態 | 意義 |
|------|------|
| 新增 | global 中不存在此項目，可直接加入 |
| 已存在 | global 中已有完全相同的值，無需動作 |
| 衝突 | global 中存在但值不同，需選擇處理方式 |

對陣列型態（如 `permissions.allow`）逐元素比對，而非整個陣列比較。

### Step 3 — 逐項互動確認

用 question tool 依序問使用者每個非「已存在」的項目：

- **新增項目**：「要加入全域嗎？(Y/N)」
- **衝突項目**：顯示 local 值 vs global 值，讓使用者選「用 local 值覆蓋 / 保留 global 值 / 跳過」

### Step 4 — 寫入全域

根據確認結果用 Edit tool 修改 `~/.claude/settings.json`。

### Step 5 — 清除確認

問使用者是否要從 `settings.local.json` 移除已 promote 的項目。若同意，用 Edit tool 清除。若清除後 local 為空物件 `{}`，提示是否刪除檔案。

## 邊界情況

- `~/.claude/settings.json` 不存在 → 建立新檔，直接寫入所有確認的項目
- local 只有 `{}` → 告知無項目可 promote
- JSON 格式錯誤 → 報錯，不嘗試修復

## 不做的事

- 不處理 `.claude/settings.json`（專案共享設定，那是給團隊用的）
- 不自動備份（使用者有 git）
- 不提供反向操作（demote）
