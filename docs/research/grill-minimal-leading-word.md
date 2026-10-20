# Research: grill-minimal 的 leading word 該用 simplest 還是 smallest complete

> 研究問題：`skills/grill-minimal` 的 leading word 目前是 **smallest complete**；改成 **simplest** 是否更貼近軟體開發實務、更適合引導 AI coding agent？實務者如何區分「簡單」與「最小範圍」，又如何防止砍掉真正必要的東西？
> 一手來源：Matt Pocock 的 `mattpocock/skills` repo（commit `49dd158`）與 aihero.dev；Lauren Tan 的 pstack（`cursor/plugins`，commit `88d4751`）；Addy Osmani 的 addyosmani.com 與 `addyosmani/agent-skills`（commit `1401c8b`）；Ward Cunningham 的 Artima 訪談與 c2 wiki；Kent Beck 的 newsletter；Martin Fowler 的 bliki；Rich Hickey 演講的 InfoQ 官方頁；Andrej Karpathy 的 X 貼文；Simon Willison 的 blog；Anthropic 與 OpenAI 的官方 prompting／agent 文件。
> 撰寫日期：2026-10-20

## 結論

**保留 smallest complete，不改成 simplest。** 理由有三，全部來自來源本身的用詞分工：

1. **simple 與 small 在實務裡是兩條不同的軸。** simple／simplest 談的是做法的複雜度（Beck、Cunningham、Hickey、Anthropic「simplest solution possible」）；small／smallest／minimal 談的是範圍或 diff 的大小（Pocock 的 tracer bullet「narrow」、Lauren Tan 的「smallest change」、Claude 文件的「minimum needed」、OpenAI 的「minimal and focused」）。Addy Osmani 的 `incremental-implementation` skill 把兩者拆成兩條規則：「Rule 0: Simplicity First」與「Rule 0.5: Scope Discipline」，同一份 skill 又寫「Implement the smallest complete piece of functionality」。grill-minimal 的核心動作是「把 scope 追溯到 goal／constraint，追不到就提議砍掉」，這是 scope 軸，所以 leading word 落在 smallest 那一邊才對位；approach 軸由定義裡的「the simplest approach」承擔，現行寫法已經同時涵蓋兩軸。
2. **每一位來源都替「減少」配了一個護欄，而 simplest 單獨使用時沒有護欄。** Cunningham 的原句後半是「that could possibly work」，他也引用 Einstein 的「as simple as possible, but no simpler」；Beck 的四條 simple design rules 把「passes the tests」排第一；Lauren Tan 寫「the smallest change that solves the problem」；Pocock 寫「narrow but complete path」；OpenAI Codex 指南寫「cover the root cause or core ask, not just a symptom or a narrow slice」。complete 正是這個護欄的一字版本。反過來，Cunningham 明說這句話原本是卡住時的探索提問，「Let's not even worry about whether it will work」；Hickey 則指出 simple 常被誤當成 easy。Addy 的「70% problem」把 security hardening、edge cases 列為 AI 最常留下的那 30%，這正好就是 SOC 2 稽核紀錄這一類「昂貴但必要」的東西。
3. **complete 單獨使用也有反向風險，所以要成對。** Pocock 觀察到 AI「wants to produce complete solutions all at once」，也就是把 complete 理解成「一次全部做完」。smallest 限制 complete，complete 再限制 smallest，兩字互相約束，對應現行定義的「Complete bounds smallest」。

**取捨：** simplest 的 pretrained prior 比較強（直接連到「the simplest thing that could possibly work」與 YAGNI 文化），讀起來也比較順；代價是 leading word 本身不再攜帶完整性護欄，得靠定義句補回來，而 leading word 的價值本來就在於不需要每次重述。smallest complete 稍微生硬，但它已經以幾乎相同的字面出現在 Addy Osmani（「smallest complete piece of functionality」）與 Pocock（「narrow but complete path」）的 skill 裡，也和本 repo `revisit` 的「smallest complete change」一致，並不是脫離實務的自創詞。其他候選字的結論見下方「候選字比較」：YAGNI、MVP、tracer bullet 都只蓋到一部分。

## 候選字比較

| 候選字 | 來源用法 | 涵蓋 scope 軸 | 涵蓋 approach 軸 | 內建完整性護欄 |
| --- | --- | --- | --- | --- |
| **smallest complete**（現行） | Addy「smallest complete piece of functionality」；Pocock「narrow but complete path」 | 是 | 由定義裡的「simplest approach」補上 | 是（complete） |
| simplest | Beck、Cunningham、Anthropic、Hickey | 弱 | 是 | 否；要加上「that could possibly work」或「but no simpler」 |
| simplest thing that could possibly work | Cunningham、Beck 的 system prompt | 弱 | 是 | 部分；原意是卡住時的探索提問 |
| YAGNI | Fowler、Pocock 的 `improve-codebase-architecture` | 只限 presumptive feature | 否 | 否；Fowler 補充它不能當成忽略 code health 的理由 |
| tracer bullet | Pocock | 是（切片的方式） | 否 | 是（complete path）；但它是切分工作的手法，不是用來砍範圍 |
| MVP／minimum viable | Addy `idea-refine` | 是（產品層級） | 否 | 是（viable）；不過偏向產品驗證，不適合技術決策 |

**設計推論：**沒有任何一個單字同時涵蓋兩軸又帶護欄。「smallest complete」加上定義句「the simplest approach that fully meets the goals and constraints」，是目前讓兩軸與護欄都到位、且 token 最少的組合。

## Matt Pocock

### Leading word 的選字準則

**來源事實：**`writing-for-agents` 把 leading word 定義為「a compact concept already living in the model's pretraining that the agent thinks with while running the document」，並說「a made-up word recruits no priors: you pay in definition tokens what a pretrained word gives free; reach for an existing word first.」[`writing-for-agents/SKILL.md` L63](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/writing-for-agents/SKILL.md#L63) 同一份文件也說，太弱、壓不過預設行為的字是 no-op：「a word too weak to beat the default ... is a no-op, and the fix is a stronger word」。[L81](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/writing-for-agents/SKILL.md#L81)

**設計推論：**照這個準則，simplest 的 prior 比較強，這是它的優點。不過 smallest 與 complete 都是現成的英文字，組合起來也已經出現在其他實務者的 skill 裡，不算 made-up word。關鍵在於它要拉出的行為是哪一種：simplest 的 prior 會拉向「降低做法的複雜度」，而 grill-minimal 要的是「砍掉沒有對應目標的 scope、保住必要的部分」。

### Tracer bullet：narrow but complete

**來源事實：**`to-tickets` 規定「Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests)」。[`to-tickets/SKILL.md` L31](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/to-tickets/SKILL.md#L31) 對應的文件寫「Every ticket is a **tracer bullet**: a narrow but complete path through every layer of the change」。[`docs/engineering/to-tickets.md` L5](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/docs/engineering/to-tickets.md#L5)

**來源事實：**在 aihero.dev 的〈Tracer Bullets: Keeping AI Slop Under Control〉裡，Pocock 寫道：「In code, this means it wants to produce complete solutions all at once. It has in mind the idea for a finished file, or a finished feature, and it produces all of the code needed in one leap.」結論則是「Force the agent to think small, build end-to-end, get feedback, and move forward with confidence.」[aihero.dev：Tracer Bullets](https://www.aihero.dev/tracer-bullets)

**設計推論：**Pocock 的用字是「narrow／small」加「complete」，跟 smallest complete 同構。他也示範了 complete 單用時的風險：agent 會把它讀成「一次全部做完」。所以 complete 不能單獨當 leading word，必須由 smallest 約束。

### YAGNI 與 TDD 的「minimal」

**來源事實：**`improve-codebase-architecture` 用「**Scope before you scan: YAGNI.**」作為探索步驟的標題。[`improve-codebase-architecture/SKILL.md` L20](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/improve-codebase-architecture/SKILL.md#L20) `tdd` 寫「**Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.」以及「One seam, one test, one minimal implementation per cycle.」[`tdd/SKILL.md` L36-L37](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/tdd/SKILL.md#L36-L37)

**來源事實：**Pocock 的 `grilling` skill 本身沒有談 scope 或簡單性；它只負責 design tree、frontier 與推薦答案。[`grilling/SKILL.md`](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/grilling/SKILL.md) aihero 字典對 grilling 的解釋是：「The result looks complete, and the guesses are indistinguishable from the choices」。[AI Coding Dictionary：Grilling](https://www.aihero.dev/ai-coding-dictionary/grilling)

**設計推論：**Pocock 在 TDD 裡用 minimal 時，護欄是測試（「only enough code to pass it」），護欄不在 minimal 這個字裡。grill-minimal 在討論計畫的階段還沒有測試可用，所以護欄必須寫進字裡，這也是 complete 存在的理由。在 Pocock 的 skills repo 與上述兩篇 aihero 文章中，沒有找到他把 simplest 當作 leading word 的例子。

## Lauren Tan（poteto）

**來源事實：**pstack 的 `plugin.json` 把作者標為「Lauren Tan」，描述是「pstack helps you write less, but higher quality code.」[`pstack/.cursor-plugin/plugin.json`](https://github.com/cursor/plugins/blob/88d47514b82e7c44f00f2b2a72ff6dd12158038c/pstack/.cursor-plugin/plugin.json) 她的 `principle-laziness-protocol` 寫「**Minimize the diff.** Make the smallest change that solves the problem. Fewer lines beat "elegant" boilerplate.」[`principle-laziness-protocol/SKILL.md`](https://github.com/cursor/plugins/blob/88d47514b82e7c44f00f2b2a72ff6dd12158038c/pstack/skills/principle-laziness-protocol/SKILL.md)

**來源事實：**`poteto-mode` 的原則索引同時列出「**Subtract Before You Add.** ... Remove dead weight first, then build on the simpler base.」與「**Experience First.** Product, UX, or feature-scope tradeoffs. Choose user delight over implementation convenience.」它還寫：「**No is an acceptable answer.** Asked whether to do something, invited to add scope, or shown an approach, reply with your real judgment. Decline, push back, or say "this doesn't earn its place" when true.」[`poteto-mode/SKILL.md` L44-L51、L89](https://github.com/cursor/plugins/blob/88d47514b82e7c44f00f2b2a72ff6dd12158038c/pstack/skills/poteto-mode/SKILL.md#L44-L89)

**設計推論：**Lauren Tan 用「smallest」描述 diff 與 scope，並以「that solves the problem」作為護欄；「simpler」則用來描述刪減後留下的程式基礎。「Choose user delight over implementation convenience」明確拒絕把 easy 當成目標，對應 Hickey 的 simple ≠ easy。她的「doesn't earn its place」和 grill-minimal「追不到 goal 就提議砍掉」是同一個動作。

**限制：**她在 X 上發表的文章與演講（例如〈How I Use Cursor〉、2,500 PR 的那篇）這次沒有抓到原文，只看到二手摘要，所以本文不引用它們。

## Addy Osmani

**來源事實：**〈The 70% Problem〉寫道：「Then you hit the other 30%. The edge case where the function receives null instead of an empty array. The race condition that only shows up under load. The accessibility requirement that the generated component ignores. The security vulnerability hidden behind plausible-looking code.」並列出「The other 30%: Error handling, edge cases, performance optimization, security hardening, accessibility, integration testing, deployment concerns」。[addyosmani.com：The 70% Problem](https://addyosmani.com/agentic-engineering/the-70-percent-problem/)

**來源事實：**他的 `incremental-implementation` skill 在流程裡寫「**Implement** the smallest complete piece of functionality」，[L38](https://github.com/addyosmani/agent-skills/blob/1401c8b8030e023baeebb31781a6653fe8e93026/skills/incremental-implementation/SKILL.md#L38) 接著把兩條軸分開處理。「Rule 0: Simplicity First」寫的是「Before writing any code, ask: "What is the simplest thing that could work?"」以及「Implement the naive, obviously-correct version first.」；「Rule 0.5: Scope Discipline」寫的是「Touch only what the task requires.」[L91-L115](https://github.com/addyosmani/agent-skills/blob/1401c8b8030e023baeebb31781a6653fe8e93026/skills/incremental-implementation/SKILL.md#L91-L115)

**來源事實：**他的 `idea-refine` skill 寫「Push toward the simplest version that still solves the real problem.」[`idea-refine/SKILL.md` L45](https://github.com/addyosmani/agent-skills/blob/1401c8b8030e023baeebb31781a6653fe8e93026/skills/idea-refine/SKILL.md#L45)

**設計推論：**這是最直接的證據。Addy 在同一份 skill 裡同時使用「smallest complete」（描述 scope 單位）與「simplest thing that could work」（描述做法），而且把它們寫成兩條規則；每次提到 simplest 時都附上護欄（「obviously-correct」、「that still solves the real problem」）。70% problem 列出的那 30%，正是 simplest 被讀成 easiest 時最先被砍掉的部分。

## Ward Cunningham：the simplest thing that could possibly work

**來源事實：**在 2004 年的 Artima 訪談中，Cunningham 說明這句話的出處：「if we were stuck more than a minute, I'd stop and say, "Kent, what's the simplest thing that could possibly work?"」以及「Let's not worry about whether it's efficient. Let's not even worry about whether it will work. Let's just write the simplest thing that could possibly work.」[Artima：The Simplest Thing that Could Possibly Work](https://www.artima.com/articles/the-simplest-thing-that-could-possibly-work)

**來源事實：**他也指出這句話後來被誤用：「I think the advice got turned into a command: "Do the simplest thing that could possibly work." That's a little more confusing, because there isn't this notion that as soon as you've done it, we'll evaluate it.」他把 simplicity 定義為「Simplicity is the shortest path to a solution.」並引用「Einstein said, "As simple as possible, but no simpler."」[同上](https://www.artima.com/articles/the-simplest-thing-that-could-possibly-work)

**設計推論：**這句話的原意是卡住時拿來探索的提問，前提是做完之後馬上評估；它刻意先不管「will it work」。grill-minimal 的推薦答案則是要讓使用者直接採納的決策，正好需要原句刻意擱置的那個完整性。拿 simplest 當 leading word，等於引入這句話的 prior，卻沒有它原本「先做再評估」的情境。

## Kent Beck

**來源事實：**Fowler 整理的 Beck 四條 simple design rules 依優先序是「Passes the tests / Reveals intention / No duplication / Fewest elements」，並說明「The rules are in priority order」、「The most important of the rules is "passes the tests"」。[Fowler：BeckDesignRules](https://martinfowler.com/bliki/BeckDesignRules.html)

**來源事實：**在〈Augmented Coding: Beyond the Vibes〉（2025-06-25）裡，Beck 把「Functionality I hadn't asked for (even if it was a reasonable next step).」列為 genie 走偏的警訊之一，並寫道「I'm still working on getting the genie to care as much as I do about simplicity.」他附上的 system prompt 同時包含「Implement the minimum code needed to make tests pass」、「Use the simplest solution that could possibly work」與「Repeat until the feature is complete」。[Kent Beck：Augmented Coding: Beyond the Vibes](https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes)

**設計推論：**Beck 的 simple 一直排在「passes the tests」之下；在他給 agent 的 prompt 裡，minimum／simplest 管每一步，「until the feature is complete」管終點。這跟 smallest（每一塊 scope）加 complete（目標全部達成）的分工相同。他的其他 augmented coding 文章多數需要付費，這次沒有讀到全文。

## Martin Fowler：YAGNI

**來源事實：**Fowler 說「Yagni only applies to capabilities built into the software to support a presumptive feature, it does not apply to effort to make the software easier to modify.」以及「Yagni is not a justification for neglecting the health of your code base.」他也寫道「any abstraction that makes it harder to understand the code for current requirements is presumed guilty.」[Fowler：Yagni](https://martinfowler.com/bliki/Yagni.html)

**設計推論：**YAGNI 的護欄是「current requirements」，跟 grill-minimal 的「trace to a stated goal or constraint」一致，但它只處理「為未來預先建造的功能」，不處理現在就過度複雜的做法，也不處理現在就必要卻昂貴的部分。因此它適合作為 smallest 的一個註腳，不適合取代 leading word。

## Rich Hickey：Simple Made Easy

**來源事實：**InfoQ 的官方演講頁摘要寫道：「Rich Hickey emphasizes simplicity's virtues over easiness', showing that while many choose easiness they may end up with complexity」。編輯整理的 Key Takeaways 寫「Simple is often erroneously mistaken for easy.」以及「"Simple" is the opposite of "complex" which means "being intertwined", "being tied together". Simple != easy.」[InfoQ：Simple Made Easy](https://www.infoq.com/presentations/Simple-Made-Easy/)

**限制：**上面引的是 InfoQ 編輯的摘要與 show notes，不是 Hickey 的逐字原話。演講本身只有影片，這次沒有取得官方逐字稿。

**設計推論：**Hickey 定義的 simple 是「不交纏」，跟範圍大小無關：一個 scope 很大的系統也可以很 simple。另外，他直接點出 simple 最常被誤讀成 easy，而這正是 eval 裡「為了 ship faster 跳過 SOC 2 稽核紀錄」那類回答背後的讀法。

## Andrej Karpathy

**來源事實：**在 2026-01-26 的貼文裡，Karpathy 寫道：「They also really like to overcomplicate code and APIs, they bloat abstractions, they don't clean up dead code after themselves, etc. They will implement an inefficient, bloated, brittle construction over 1000 lines of code and it's up to you to be like "umm couldn't you just do this instead?" and they will be like "of course!" and immediately cut it down to 100 lines.」同一篇也說「Write the naive algorithm that is very likely correct first, then ask it to optimize it while preserving correctness.」[X：@karpathy/status/2015883857489522876](https://x.com/karpathy/status/2015883857489522876)

**限制：**x.com 無法直接抓取，原文是透過 `api.fxtwitter.com` 這個 X 鏡像 API 取得的同一則貼文全文。

**設計推論：**Karpathy 抱怨的是做法的複雜度（approach 軸），這是 simplest 擅長處理的部分；但他的護欄是「very likely correct」與「preserving correctness」。grill-minimal 的定義句「the simplest approach that fully meets the goals and constraints」已經把這兩點都納入了。

## Simon Willison

**來源事實：**〈Here's how I use LLMs to help me write code〉（2025-03-11）寫道：「For complex coding tasks try getting the LLM to write a simpler version first, check that it works and then iterate on building to the more sophisticated implementation.」[simonwillison.net](https://simonwillison.net/2025/Mar/11/using-llms-for-code/) 〈Vibe engineering〉（2025-10-07）把「Automated testing」列為前提，並寫道「Without tests? Your agent might claim something works without having actually tested it at all」。[simonwillison.net](https://simonwillison.net/2025/Oct/7/vibe-engineering/)

**設計推論：**Willison 的 simpler 是迭代的起點，不是終點；護欄是「check that it works」與測試。這呼應 Cunningham 的原意，但不適用於 grill-minimal 這種要定案的推薦答案。

## Anthropic 官方指引

**來源事實：**Claude prompting best practices 的「Overeagerness」一節指出，Claude Opus 4.5 與 4.6 有「a tendency to overengineer by creating extra files, adding unnecessary abstractions, or building in flexibility that wasn't requested」。範例 prompt 是「Avoid over-engineering. Only make changes that are directly requested or clearly necessary. Keep solutions simple and focused」，並寫「The right amount of complexity is the minimum needed for the current task.」[Claude Docs：Overeagerness](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#overeagerness) 緊接的一節則提醒另一個方向：「Implement a solution that works correctly for all valid inputs, not just the test cases.」[Claude Docs：Avoid focusing on passing tests and hardcoding](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#avoid-focusing-on-passing-tests-and-hardcoding)

**來源事實：**〈Building effective agents〉寫道：「we recommend finding the simplest solution possible, and only increasing complexity when needed」。[Anthropic Engineering：Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)

**設計推論：**Anthropic 把「simple and focused」與「minimum needed」並用，護欄是「clearly necessary」與「for the current task」，下一節又防止過度精簡導致解法不完整。這兩節合起來，跟 smallest complete 是同一個結構。

## OpenAI 官方指引

**來源事實：**Codex prompting guide 寫道：「Act as a discerning engineer: optimize for correctness, clarity, and reliability over speed; avoid risky shortcuts, speculative changes, and messy hacks just to get the code to work; cover the root cause or core ask, not just a symptom or a narrow slice.」以及「Finish the website or app to completion, within the scope of what's possible without adding entire adjacent features or services.」[OpenAI Cookbook：`codex_prompting_guide.ipynb`](https://github.com/openai/openai-cookbook/blob/main/examples/gpt-5/codex_prompting_guide.ipynb)

**來源事實：**GPT-5 prompting guide 的範例寫「Changes should be minimal and focused on the task.」[`gpt-5_prompting_guide.ipynb`](https://github.com/openai/openai-cookbook/blob/main/examples/gpt-5/gpt-5_prompting_guide.ipynb) GPT-5.2 指南有一段「Preventing Scope drift」，寫「No extra features, no added components, no UX embellishments.」與「If any instruction is ambiguous, choose the simplest valid interpretation.」，並建議「Make scope discipline explicit (don't expand problem surface area).」[`gpt-5-2_prompting_guide.ipynb`](https://github.com/openai/openai-cookbook/blob/main/examples/gpt-5/gpt-5-2_prompting_guide.ipynb)

**設計推論：**OpenAI 明確反對「risky shortcuts ... just to get the code to work」與「a narrow slice」，同時要求「to completion」、「without adding entire adjacent features」，等於同時要求 complete 與 smallest。它的 simplest 帶著「valid」這個護欄。「optimize for correctness ... over speed」幾乎就是對「為了 ship faster 砍掉稽核紀錄」的直接否定。

## 對 grill-minimal 的具體建議（設計推論）

- leading word 維持 **smallest complete**；`## Smallest complete` 的定義句「the simplest approach that fully meets the goals and constraints」保留，讓 simplest 繼續負責 approach 軸。
- 如果想讓讀者明白這個用字出自實務，可以在 `README.md` 補一句來源脈絡，例如 Addy Osmani 的「smallest complete piece of functionality」或 Pocock 的「narrow but complete」。`SKILL.md` 不需要為此加字。
- 不建議改用「simplest thing that could possibly work」：它的原意是卡住時的探索提問，會帶進「先別管能不能用」的 prior。
