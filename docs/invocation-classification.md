# Invocation 分類

本文件定義此 repository 所有 skills 共用的 invocation marker、判定規則與維護方式，適用於現有 skills、未來新增的 skills，以及日後 bucket 或 invocation 路徑變更。

實際 runtime 行為由各 skill 的 `SKILL.md` 與 `agents/openai.yaml` marker 決定；根 `README.md` 的 `Model-invoke` 與 `User-invoke` 分組是唯一供人閱讀的目前分類結果。本文件不保存逐 skill 的分類結果或判定理由。

## Marker 定義

- **ADD**：skill 僅能由使用者明確調用，必須成對設定：
  - `SKILL.md` frontmatter：`disable-model-invocation: true`
  - `agents/openai.yaml`：

    ```yaml
    policy:
      allow_implicit_invocation: false
    ```

- **DO NOT ADD**：skill 維持 implicit-enabled：
  - `SKILL.md` 不加入 `disable-model-invocation`。
  - `agents/openai.yaml` 可不加入 `allow_implicit_invocation`，也可明確設定為 `true`。
- `allow_implicit_invocation: true` 代表允許隱式調用，不是 explicit-only marker。
- 不允許只加入其中一個 explicit-only marker，也不使用 `disable-model-invocation: false` 作為佔位值。
- 根 `README.md` 必須將每個 skill 恰好列在一個對應分組：ADD 在 `User-invoke`，DO NOT ADD 在 `Model-invoke`；`Model-invoke` 分組在前。
- 分類只影響 invocation marker 與根 `README.md` 分組，不改變 `description` 的撰寫標準。

## 判定規則

### Bucket 優先規則

1. **WIP 一律 DO NOT ADD**：skill 仍在測試與調整中，讓 Scheduled task、模型路由與實際使用持續驗證行為。Invocation 不代表已授權執行高風險動作，因此不因風險高低建立例外。
2. **Deprecated 一律 ADD**：skill 已準備淘汰，不再讓模型主動選用；真的仍有需要時，由使用者明確調用。現有相依不改變此結果。
3. **其餘 active buckets 逐項判斷**：只有所有支援情境都必須由使用者刻意啟動的獨立流程才 ADD；只要存在一條有具體依據的自動調用路徑，整個 skill 就 DO NOT ADD。

### 明確調用與自動調用

使用者明確調用，是指使用者在當次互動中透過 skill 名稱、command 或 UI 明確選擇該 skill。

已由使用者明確調用的 orchestrator，可以把這次授權委派給其 `SKILL.md` 固定 allowlist 中的 explicit-only phase source。Orchestrator 可透過通用 resolver 解析檔案，但 target 必須由 caller 的固定 allowlist 決定，不得由模型路由、issue、對話或其他任務資料增補或替換。符合這些條件的委派仍屬於該次明確調用，不構成 target skill 的隱式調用路徑。

以下都屬於自動調用：

- 使用者只以自然語言描述任務，由模型判斷該使用哪個 skill。
- 模型自行選用。
- 另一個 skill 在沒有上述明確委派時自行載入或調用。
- Scheduled task、hook 或 CI 自動載入；即使排程內容直接寫出 skill 名稱，仍屬自動調用。

Automation 只直接執行 skill 內的 script、完全不載入 `SKILL.md` 時，不構成 active skill 的自動調用依據。

### Active skill 的依據門檻

判斷採反事實測試：

> 如果現在把 skill 改成 explicit-only，是否有一條現行或已承諾支援的流程，會因為沒有人在當次互動中明確選擇 skill，而失效或漏掉必要行為？

判斷 Active skill 是否符合 DO NOT ADD 時，必須確認以下四個面向：

- **調用者**：誰需要自動載入。
- **觸發條件**：什麼情況需要載入。
- **影響**：改成 explicit-only 後會中斷或遺漏什麼。
- **依據**：repository 規則、skill 相依、排程設定、Issue 或負責人的明確確認等具體證據。

「未來說不定會用到」、「讓模型看得到比較方便」，或只因使用者可能以自然語言描述相同任務，都不是充分依據。只有所有支援情境都必須由使用者刻意啟動時，Active skill 才判為 ADD。

以上面向只用於當次判定，不在本文件維護逐 skill 紀錄。

完成上述依據檢查後仍無法判斷時，預設判為 ADD，以減少 `description` 帶來的 context load；只有日後出現具體的自動調用路徑時，才改判為 DO NOT ADD。

### 維護方式

- 新 skill 不必一律先進 WIP；但加入 repository 時必須依本文件完成分類、設定或移除成對 marker，並更新根 `README.md` 分組。
- 只有 invocation 路徑、bucket、支援的調用者或主要用途改變時需要重新判定；一般內容修正不需重判。
- 根 `README.md` 分組是唯一供人閱讀的目前分類結果，不另建逐 skill 清單或理由紀錄。
- 把 skill 移入 Deprecated 時，檢查所有其他 skill 目錄是否提到其名稱、引用其文件或直接執行其 script。名稱命中必須確認確實指向該 skill，而非一般同名詞彙。
- 發現 Deprecated 相依時，只提醒使用者調整，不阻擋移動，也不改變 Deprecated 一律 ADD。
- Deprecated 相依檢查不涵蓋 Scheduled task、hook、CI、`AGENTS.md` 或其他外部調用來源。
