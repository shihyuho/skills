# Skill User Data 目錄規範

本文件定義此 repository 的 skills 應如何放置跨多次執行保留的 skill-owned data。規範只決定 config 與 cache 的根目錄；每個 skill 仍自行決定是否需要這些資料，以及各自目錄內的檔名與結構。

## 先分類，再決定目錄

用「刪除後會發生什麼事」分類：

- **Config**：刪除後會失去使用者設定、憑證、preset、durable metadata 或 state，改變後續行為，或使正常流程必須等待重新設定、輸入或遷移才能等價繼續。放在 config 目錄。
- **Cache**：刪除後，正常流程會自動重新下載或重算並得到等價結果；只影響時間、網路或運算成本，不會失去唯一一份使用者資料。放在 cache 目錄。

無法確定時歸類為 config。Cache 必須能安全刪除並由正常流程自動恢復；不可把 secret、使用者設定或無法自動重建的唯一資料只放在 cache。

## Root 解析順序

Config root 與 cache root 分開解析，不共用一個 root。兩者各自依下列相同順序取得，命中後即停止：

1. **已生效的使用者層級 instructions**：若當前 agent 已生效的使用者層級 instructions 明確指定 skill config root 或 cache root，對相應類別使用該路徑。Agent 不需要額外搜尋未載入的設定檔。
2. **預設位置**：
   - Config root：`~/.config/softleader/agent-skills`
   - Cache root：`~/.cache/softleader/agent-skills`

這兩個預設位置與 softleader/agent-skills 共用，各 skill 以 canonical name 分目錄。其中 `~` 代表當前使用者的 home 目錄。所有作業系統都使用相同的預設位置，不另外切換到 XDG、`APPDATA`、`LOCALAPPDATA` 或其他平台目錄。若 instructions 只指定其中一種 root，另一種仍依自己的解析順序決定位置。

若高順位的 root 已明確設定卻無法使用，應回報該路徑與原因，不可靜默降級到下一順位。

## 每個 skill 的目錄

解析 root 後，以 `SKILL.md` frontmatter 的 canonical `name` 建立該 skill 的目錄：

```text
<resolved-config-root>/<canonical-skill-name>/
<resolved-cache-root>/<canonical-skill-name>/
```

例如，使用預設 root 時，`scope-it` 的 config 目錄與 cache 目錄分別為：

```text
~/.config/softleader/agent-skills/scope-it/
~/.cache/softleader/agent-skills/scope-it/
```

Skill 只建立實際需要的類別，不必同時建立兩個目錄。Skill 可在自己的 config 或 cache 目錄內自由規劃檔名與子目錄；新的文件、範例與程式不得把這些資料寫入 skill source、安裝目錄或 marketplace installation cache。

## 適用邊界

- 使用者手動建立與 skill 自動產生的 skill-owned data，都使用本規範分類。
- 使用者指定輸出位置的交付物，以及 repository、workspace 本身管理的檔案，不屬於 skill-owned data。
- 只在單次執行期間使用、並會於執行結束時清除的暫存資料，不屬於 config 或 cache。
- 純環境變數、system keychain、`gh auth`、kubectl credential store、agent host 的原生 hook／plugin 設定，或其他外部工具擁有的資料可維持原生作法，不需要複製進這兩個目錄。
- 本規範不強制共用 CLI flag、resolver library 或 host protocol。各 agent 與 skill 依自身執行環境實作相同的分類與解析結果。

## Legacy 路徑與遷移

現有 skill 若已在其他位置保存 config 或 cache，對每一類資料分別套用下列規則：

1. Canonical config 或 cache 目錄永遠優先。
2. 只有相應的 canonical data 不存在時，才可以唯讀方式回退讀取同類 legacy data。
3. Legacy fallback 可永續保留，但每次命中都必須警告使用者，並指出相應的 canonical destination。
4. 不可合併 canonical 與 legacy 內容，也不可把 legacy config 當成 cache。
5. 只有使用者明確要求遷移時，agent 才可以移動 legacy data。

執行遷移時：

- 先以唯讀方式確認精確的來源、資料類別、目的地與衝突狀態。
- 建立相應的 canonical skill 目錄，但不覆寫或合併已存在的 canonical data。
- 移動後依該 skill 的驗證方式確認新位置可用；跨檔案系統時，先完成安全複製與驗證，再移除 legacy 原檔。
- 除非使用者另有要求，不留下另一份可用的 secret 備份。
- 完成後回報資料類別、原路徑、新路徑與驗證結果。
