# Research: `writing-agents-md` 最佳實務

截至 2026-08-12 的結論：`AGENTS.md` 應是精簡、可驗證的跨 agent 專案指令，但「精簡」不等於刪除所有可從 repo 發現的資訊。應保留會避免昂貴錯誤的 build／test、風格與安全規則，並以巢狀檔案或 path-scoped rules 限縮局部規則；多步驟、可重複的任務流程才移入 skill。

## 目前平台語義

| 平台 | Discovery、scope 與 precedence | 適合放入的內容 |
| --- | --- | --- |
| Codex | 先讀全域 `AGENTS.override.md`（否則 `AGENTS.md`），再從 Git root 走到 cwd；每層最多採一檔，`*.override.md` 優先。內容由 root 往 cwd 合併，較近 cwd 的指令在後，因此可覆寫較上層規則；預設累計上限為 32 KiB。 | 全域或專案層級的明確約束；把 package／目錄特有規則置於對應子目錄的巢狀 `AGENTS.md`。 |
| `agents.md` 格式 | 根目錄檔可涵蓋 build/test commands、code style、testing 與 security；大型 monorepo 可在子專案放巢狀 `AGENTS.md`，最近的檔案優先。 | 新進協作者也需要知道、且可直接執行或檢查的專案規則，例如正確驗證指令與安全注意事項。 |
| Claude Code | `CLAUDE.md` 是其原生檔案；在 cwd 的祖先鏈於啟動時由 root 往 cwd 串接，子目錄檔於讀取該目錄檔案時載入。repo 已採 `AGENTS.md` 時，使用 `CLAUDE.md` 的 `@AGENTS.md` 匯入（或無 Claude 專屬內容時 symlink）。 | 保持每個 `CLAUDE.md` 少於 200 行、具體、簡潔；build/test 指令可保留。局部檔案規則用 `.claude/rules/` 的 `paths`，任務專屬流程用 skill。 |

上述層級是功能，不是例外：把規則全塞在 root 會增加每次啟動的 context 成本，亦使不相關指令互相衝突。反之，只把所有內容移出全域檔，會讓 agent 缺失每個工作都須遵守的關鍵命令或安全界線。

## 現行 `skills/writing-agents-md` 的缺口

1. 以「可發現即刪」作為強預設太絕對；官方範例與 Claude 指引都把明確的 build/test commands 視為適合常駐的專案指令。
2. 將既有 `AGENTS.md`／`CLAUDE.md` 僅當「歷史輸入」，並在衝突時一律以 repo 現況為準，不安全。既有檔可能承載外部服務、部署或安全限制，無法單靠靜態 repo 還原；應先逐條驗證、保守保留未能反證的 safety-critical 規則。
3. 只提供「move-to-skill」分流，遺漏巢狀 `AGENTS.md` 與 Claude path-scoped rules；因此容易把只適用子專案／檔案類型的規則錯刪或提升為全域規則。
4. 評估流程只朝 pruning：沒有要求以錯誤重現、code-review 回饋或重複人工提示為信號新增規則，也沒有檢查 ancestor/nested 規則的矛盾、scope 與 precedence。

## 具體修改方案與取捨

修改目標是將目前的「刪除優先」改為「最小但完整、並正確分層」。

1. 在 Overview／Core Filter 補上保留測試：一條可發現的資訊，若是常用、精確、可驗證，且省下錯誤或探索成本，仍可留在 root；典型例子為 build/test/lint 指令與安全守則。取捨是較長的常駐 context，故每條必須有明確收益。
2. 把既有檔案改為「待驗證的現有契約」：與 repo 衝突時，先查 CI、設定、維運文件與 owner；若仍不確定，標示待確認或保留安全限制，不得自動刪除。取捨是審查較慢，但避免把不可見的作業或安全要求移除。
3. 在分類結果新增 `move-to-nested-agents-md`、`move-to-path-rule` 及其判準：子專案專屬規則放最近的 `AGENTS.md`；Claude 的檔案類型／路徑規則放 `.claude/rules/` + `paths`；可重複、多步驟工作流才放 skill。取捨是結構多一層，但能降低噪音並維持 scope 正確。
4. 將 workflow 擴充為雙向評估：除刪除過期規則外，也由重複錯誤、review feedback、反覆聊天澄清判斷新增規則；最後列出從 root 到 target directory 的指令鏈、潛在矛盾與驗證命令。取捨是多一段 audit，但符合 Codex／Claude 的實際載入模型。
5. 保留「短、高訊號」原則，明示 Codex 的 32 KiB 累計限制與 Claude 每檔少於 200 行目標；大段參考資料不以 import 偽裝搬運，因為 Claude import 仍會在啟動時佔用 context。

## Claude 5 context engineering 對改版方向的校正

[Anthropic 於 2026-07-24 公開的第一方經驗](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)不推翻上述分層方向，但將改版的重心從「更完整的分類規則」校正為「更少的常駐規則，加上正確的按需載入」。

- **明確主張：新模型需要的過度約束變少。** Anthropic 從 Claude Code 針對 Claude Opus 5 與 Fable 5 的 system prompt 刪除超過 80%，coding eval 無可測損失；文章也記錄重疊、衝突的禁令會迫使模型花更多推理才能判斷意圖。這強化現行 skill 的精簡主張，也意味著改版不應在主檔新增大量 host 分支、禁令與邊界案例。取捨是模型會擁有更多判斷空間；安全、不可逆或高成本區域仍可保留強約束。[來源](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)
- **明確主張：由規則與範例轉向判斷與介面。** 文章將絕對性的 comment 規則改成「跟隨周邊程式碼的密度、命名與慣例」，並主張以表達力足夠的 tool/file interface 取代操作範例。這修正了原擬「為每種去處加上詳細判準」的做法：`writing-agents-md` 應提供一個簡單的 routing interface（scope、持續性、執行機制），少用強配對的 bad/good 範例。取捨是初用者少了可拷貝的範本，但較不會把範例誤當全域規則。[來源](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)
- **明確主張：常駐 context 要輕，細節要 progressive disclosure。** Anthropic 已將 verification 與 code review 從 system prompt 移入按需啟用的 skills，並建議 `CLAUDE.md` 只簡述 repo 用途，把多數 tokens 留給難以從程式碼看出的 gotchas。這支持 move-to-skill，但也是現行「一律刪除 repo summary」的明確反例：可保留一到兩句定位，不應擴張成目錄導覽。當 verification 只有一個簡短、必用、非顯而易見的 canonical command 時可直接保留；有多個條件分支時才移入 skill。取捨是這不再是一個純粹的「可發現即刪」測試。[來源](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)
- **明確主張：skill 是輕量、按需找資訊的指引。** 文章建議 skill 編碼個人、團隊或產品特有的意見與知識，長 skill 再以多檔案漸進披露，只在高重要性區域過度約束。因此改版應精簡 `SKILL.md` 的重複 filter，將 host-specific discovery 詳情與完整檢查表留在 references；但不應只為了縮短而把正確性要件切碎到難以發現。[來源](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)
- **適用性邊界：「刪除 80%」不是跨模型的通用除錯准則。** 文章的無損結果明確來自 Claude Opus 5 與 Fable 5 的 Claude Code coding eval；`writing-agents-md` 同時服務 Claude Code 與 Codex，不能僅依這個結果刪除跨 host 安全或工具規則。設計上應將「模型已會做」當成需由 target host/model eval 驗證的假設，而不是靜態刪除理由。取捨是無法用一個極簡單的長度或 discoverability threshold 決定全部內容，但可避免把單一供應商、單一代模型的經驗過度外推。[來源](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)

綜合後的改版準則是：**先刪重複、衝突與沒有觀察到價值的規則；再把剩餘規則放到最小正確 scope；只對高成本錯誤與 target eval 顯示的能力缺口加上強約束。**

## Sources

- [OpenAI Codex: Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md) — 全域／root-to-cwd discovery、override、合併順序與 32 KiB 預設上限。
- [agents.md: How to use AGENTS.md?](https://agents.md/) — build、test、style、security 與巢狀 scope 的格式指引。
- [Claude Code: How Claude remembers your project](https://code.claude.com/docs/en/memory) — `CLAUDE.md` scope/precedence、少於 200 行、`@AGENTS.md`、rules 與 `paths`。
- [Claude Code: Extend Claude Code](https://code.claude.com/docs/en/features-overview) — 常駐 `CLAUDE.md` 與按需 skill 的適用邊界。
- [Claude: The new rules of context engineering for Claude 5 generation models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models) — Claude 5 下的 prompt 精簡、判斷、interface design、progressive disclosure 與跨模型適用邊界。
- [GitHub Docs: About GitHub Copilot code review](https://docs.github.com/en/copilot/concepts/agents/code-review) — agentic code review 會蒐集完整專案 context，佐證 repo guidance 應可供跨工具理解。
