# Research: grill-minimal 該不該改用 essential

> 研究問題：**essential**（例如 Fred Brooks 在〈No Silver Bullet〉裡的 essential vs accidental complexity）能不能一字同時承擔「只留 essential 的」（smallest）與「essential 的都要留」（complete）？分三個層次判斷：(1) skill 名稱 `grill-minimal` → `grill-essentials`；(2) 用它取代 SKILL.md 與 README 的 leading word _smallest complete_；(3) 不改名，只借 essential vs accidental complexity 來加強「the simplest approach」這半邊。本文建立在 [`grill-minimal-leading-word.md`](grill-minimal-leading-word.md) 之上，不重做 simplest 與 smallest complete 的比較。
> 一手來源：Brooks〈No Silver Bullet: Essence and Accidents of Software Engineering〉，UNC 技術報告 TR86-020（1986）；Moseley & Marks〈Out of the Tar Pit〉（2006）；Vitsœ 官方網站上的 Dieter Rams ten principles；Greg McKeown 官方網站的 Essentialism 書頁；Wes McKinney 的 blog；Jake Nations 在 AI Engineer 的演講頁與逐字稿；本機 `mattpocock/skills`、`addyosmani/agent-skills`、`anthropics/skills`、`anthropics/claude-code`、`openai/codex` 的全文搜尋。
> 撰寫日期：2026-10-20

## 結論

**名稱與 leading word 都不改；mechanism 值得採用，但用白話寫，不要掛上 essential／accidental 這兩個標籤。** 三個層次分別如下。

### 1. Skill 名稱：維持 `grill-minimal`，不改成 `grill-essentials`

**設計推論：**名稱只有一個工作：讓人在呼叫前知道這個 skill 會把計畫往「少」的方向拉。README 也明白警告「grill-minimal will keep proposing cuts to a design you mean to keep broad」，minimal 正好傳達這個方向。essentials 雖然理論上同時帶有「只留」和「全留」兩層意思，但作為複數名詞，它在日常英文裡最常見的意思是「基本款、入門必備」。下面第 2 點會說明，這個讀法剛好會把 skill 往 MVP 的方向拉。在名稱這個層次，名字之外沒有定義句可以把意思校正回來，所以這個風險比放在內文時更大。改名的代價也是實際存在的：`/grill-minimal` 的呼叫方式、root README、`agents/openai.yaml`、evals 都要一起改。

**取捨：**minimal 只帶出 smallest 這一半，complete 那一半要靠 README 開頭的 job sentence 補上；essentials 單看字面比較對稱。但 Rams 的「less, but better」與 McKeown 的「doing less, but better」（見下文）顯示，連以 essential 為核心的來源，也需要再加一個字（better）才能把品質護欄帶進來。可見 essential 本身並沒有帶護欄，對稱只是表面上的。

### 2. Leading word：保留 _smallest complete_，不換成 _essential_

**設計推論：**換掉有三個問題，都來自來源本身的定義。

1. **一手來源裡的 essential／accidental，會把 complete 的後半段歸到 accidental。** Moseley & Marks 把 essential 嚴格限定為「strictly essential to the users' problem」，並明說效能屬於 accidental，還把「Performance」列為「Required Accidental Complexity」的主要理由。把 Brooks 用在 AI coding 上的實務者也這樣分類：Jake Nations 把「workarounds, defensive code, frameworks」列為 accidental，說這些是「the stuff that we put together to make the code itself work」；Wes McKinney 則把 agent 產出的「defensive boilerplate」當作新的 accidental complexity。grill-minimal 的 complete 刻意保留的「what makes the kept scope work: correct behavior, edge cases, security, tests, the quality bar」，正好就是這些來源歸為 accidental 的東西。如果用 essential 當 leading word，模型的 pretrained prior 會把那一段讀成可以砍的部分，complete 就失去作用了。
2. **essential 的 prior 不帶可檢查的準則，而且容易被讀成由判斷者自己決定。** Brooks 的 essence 是「difficulties inherent in the nature of the software」，談的是軟體本身的困難，不是某一份計畫裡哪些 scope 必要。McKeown 的 Essentialism 是個人選擇的紀律（「regaining control of our own choices」），在那個脈絡裡，判斷什麼是 essential 的人就是使用者本人。換到 agent 情境，執行判斷的變成 agent。現行的「trace it to the goal or constraint that needs it」把判斷權綁在使用者陳述過的目標上，essential 沒有這層綁定。唯一接近可檢查準則的是 Tar Pit 的「have to」測試（見第 3 點），但那個準則是寫在定義裡的，essential 這個字本身沒有帶著它。
3. **字面上也看不出兩個軸。** 前一份研究的結論是：smallest 管 scope 軸，定義句裡的 simplest approach 管 approach 軸。essential 在 Brooks 與 Tar Pit 裡都是 complexity 的分類，偏向 approach 軸，對 scope 軸（capability 要不要做）幾乎沒有說法。Brooks 在這篇論文裡唯一接近「功能過多」的評論，是說 Ada「is perhaps over-rich」。

**取捨：**essential 的 pretrained prior 很強（「No Silver Bullet」是軟體工程最常被引用的論文之一），而且一個字就同時暗示「只」和「全」。代價是這個 prior 對 complete 後半段的分類方向剛好相反，而 leading word 的價值正是在不重述定義的情況下靠 prior 運作。smallest complete 比較生硬，但不會反過來拉錯方向。

### 3. Mechanism：採用，用白話寫進 `## Smallest complete` 的最後一段

**設計推論：**Brooks 與 Tar Pit 確實能補上現行文字缺少的一塊：smallest 對 scope 有可檢查的測試（能否追溯到 goal／constraint），approach 軸卻只有「the simplest approach」這個形容詞，沒有測試。Tar Pit 的定義正好提供一個測試：「if there is any possible way that the team could produce a system that the users will consider correct without having to be concerned with a given type of complexity then that complexity is not essential」。換成 grill-minimal 的用語就是：做法裡的某個複雜度，如果有另一個更簡單、同樣滿足 goals 與 constraints、而且能運作的做法可以避開它，就應該砍掉。Brooks 的 conformity 一節也剛好替 constraints 背書：外部介面強加的複雜度「cannot be simplified out by any redesign of the software alone」，所以 constraint 帶來的複雜度要留下。

**取捨：**要拿到這個測試，但不能讓 accidental 這個標籤把 complete 的後半段拉走，所以句子用白話寫，並且明說「works」那一半也算在 constraint 內。另外，要求 agent 說出那個更簡單的替代做法，讓 approach 軸的砍除跟 scope 軸的追溯一樣，可以由使用者檢查。

**建議的 SKILL.md 句子**（取代現行 `## Smallest complete` 的最後一段）：

```markdown
Each recommended answer is the smallest complete one: the simplest approach that fully meets the goals and constraints and works. The goals and constraints carry complexity of their own, and that stays; complexity the approach alone brings in goes, whenever a simpler approach would meet the same goals and constraints and still work. Name that simpler approach when you recommend the cut.
```

**設計推論：**「complexity the approach alone brings in」對應 Tar Pit 的 accidental（「all the rest」），但不使用那個字；「and still work」把 complete 的後半段（edge cases、security、tests、quality bar）放在砍除的門檻之內，防止它們被當成 approach 自己帶來的複雜度砍掉；「Name that simpler approach」則是 approach 軸上相當於「traces to a stated goal or constraint」的檢查點。README 的 `## Smallest complete` 如果要同步，可以補一句「Complexity a simpler approach could avoid comes back to you as a cut too, with that approach named.」。

## Fred Brooks：No Silver Bullet

**限制：**UNC 技術報告是掃描檔，引文是從 PDF 抽出的文字，只修正了明顯的 OCR 錯字（例如「s0 that」改成「so that」），其餘字詞沒有改動。頁碼是報告本身印的頁碼。

### essence 與 accidents 是什麼

**來源事實：**Brooks 依照 Aristotle 的區分，把軟體的困難分成兩類：「Following Aristotle, I divide them into essence, the difficulties inherent in the nature of the software, and accidents, those difficulties which today attend its production but which are not inherent.」[UNC TR86-020 p.2](https://techreports.cs.unc.edu/papers/86-020.pdf) 他對 essence 的定義是：「The essence of a software entity is a construct of interlocking concepts: data sets, relationships among data items, algorithms, and invocations of functions. This essence is abstract, in that the conceptual construct is the same under many different representations.」[同上 p.2](https://techreports.cs.unc.edu/papers/86-020.pdf)

**來源事實：**摘要把 accidental 定義為「representation」：「All software construction involves essential tasks, the fashioning of the complex conceptual structures that compose the abstract software entity, and accidental tasks, the representation of these abstract entities in programming languages and the mapping of these onto machine languages within space and speed constraints.」[同上，Abstract](https://techreports.cs.unc.edu/papers/86-020.pdf) 談到 OOP 時他也說：「such advances can do no more than to remove all the accidental difficulties from the expression of the design. The complexity of the design itself is essential」。[同上 p.8](https://techreports.cs.unc.edu/papers/86-020.pdf)

**設計推論：**所以 Brooks 的區分是「概念結構」與「它的表示方式」之間的區分，不是「問題」與「解法」之間的區分。在 Brooks 的框架裡，設計本身（包含解法的概念結構）屬於 essential。這點跟後來 Tar Pit 與實務者口中的「problem vs solution」不同，引用時要注意。

### essential 是否涉及 scope 或 features

**來源事實：**Brooks 把「決定要做什麼」放在 essence 的核心：「The hardest single part of building a software system is deciding precisely what to build.」[同上 p.14](https://techreports.cs.unc.edu/papers/86-020.pdf) 但他的處方是和客戶反覆迭代，不是刪減：「the most important function that the software builder does for his client is the iterative extraction and refinement of the product requirements. For the truth is, the client does not know what he wants.」[同上 p.15](https://techreports.cs.unc.edu/papers/86-020.pdf)

**來源事實：**談到 conformity 時，他把外部強加的複雜度歸為不可消除：「Much of the complexity he must master is arbitrary complexity, forced without rhyme or reason by the many human institutions and systems to which his interfaces must conform.」以及「this cannot be simplified out by any redesign of the software alone.」[同上 p.4](https://techreports.cs.unc.edu/papers/86-020.pdf)

**來源事實：**這篇論文中唯一接近「功能過多」的評論是關於 Ada：「Ada is perhaps over-rich, the natural product of the process by which requirements were laid on its design.」[同上 p.7](https://techreports.cs.unc.edu/papers/86-020.pdf)

**來源事實：**Brooks 描述 prototype 時明說它會省略哪些東西：「Prototypes typically perform the mainline tasks of the application, but make no attempt to handle the exceptions, respond correctly to invalid inputs, abort cleanly, etc. The purpose of the prototype is to make real the conceptual structure specified, so that the client can test it for consistency and usability.」[同上 p.15](https://techreports.cs.unc.edu/papers/86-020.pdf)

**設計推論：**Brooks 沒有提供「哪些 feature 該砍」的準則。他的 essence 包含需求本身，而需求是跟客戶一起找出來的，這跟 grill-minimal「goals 屬於使用者」的立場一致。conformity 一節則替「constraint 帶來的複雜度要留下」提供了直接的出處。prototype 那段剛好描繪了「essentials only」的 MVP 讀法：只做 mainline，不處理 exceptions 與 invalid inputs。Brooks 把那當成釐清需求用的工具，不是交付物，而這正是 complete 要擋住的方向。

### No Silver Bullet Refired

**限制：**〈"No Silver Bullet" Refired〉收錄在《The Mythical Man-Month》20 週年版，這次沒有取得原文。網路上只找到課程投影片與二手文章，轉述 Brooks 在文中澄清 accidental 不是「mishap」的意思，所以本文不引用它。Moseley & Marks 在自己的論文裡提到同一點（見下節），但那是他們的轉述，不是 Brooks 的原話。

## Moseley & Marks：Out of the Tar Pit

**限制：**本文使用的 PDF 來自 [curtclifton.net](https://curtclifton.net/papers/MoseleyMarks06a.pdf)，這是業界最常引用的副本，標註作者 Ben Moseley 與 Peter Marks，日期 2006-02-06，但不是作者本人的網站。下面的頁碼是論文本身印的頁碼。

### 重新定義：以 users' problem 為準

**來源事實：**兩人把 essential 綁在使用者眼中的問題上：「Essential Complexity is inherent in, and the essence of, the problem (as seen by the users). Accidental Complexity is all the rest — complexity with which the development team would not have to deal in the ideal world (e.g. complexity arising from performance issues and from suboptimal language and infrastructure).」[Out of the Tar Pit p.21](https://curtclifton.net/papers/MoseleyMarks06a.pdf) 而且刻意比日常用法嚴格：「when we use the term essential we will mean strictly essential to the users' problem (as opposed to — perhaps — essential to some specific, implemented, system, or even — essential to software in general).」[同上 p.21](https://curtclifton.net/papers/MoseleyMarks06a.pdf) accident 的意思則是：「Here (as with Brooks) we use it in the more general sense of "something non-essential which is present".」[同上 p.21](https://curtclifton.net/papers/MoseleyMarks06a.pdf)

**來源事實：**他們的判準是一個「have to」測試：「Note that the "have to" part of this observation is critical — if there is any possible way that the team could produce a system that the users will consider correct without having to be concerned with a given type of complexity then that complexity is not essential.」[同上 p.22](https://curtclifton.net/papers/MoseleyMarks06a.pdf) 以及：「if the user doesn't even know what something is (e.g. a thread pool or a loop counter — to pick two arbitrary examples) then it cannot possibly be essential by our definition」。[同上 p.22](https://curtclifton.net/papers/MoseleyMarks06a.pdf)

**來源事實：**這個測試從 informal requirements 出發：「Even in the ideal world we need to start somewhere, and it seems reasonable to assume that we need to start with a set of informal requirements from the prospective users.」[同上 p.23](https://curtclifton.net/papers/MoseleyMarks06a.pdf) 例如：「All data mentioned in the users' informal requirements is of concern to the users, and is as such essential.」[同上 p.24](https://curtclifton.net/papers/MoseleyMarks06a.pdf)

**設計推論：**這是所有來源裡唯一跟「traces to a stated goal or constraint」同構的可檢查準則：先看使用者的需求，再問有沒有別的方式不必承擔這個複雜度。不過它檢查的是 state 與 control 這類 complexity，不是 capability。在 grill-minimal 裡，它適合放在 approach 軸，不適合取代 scope 軸的追溯。

### 效能與「讓它能運作」被歸為 accidental

**來源事實：**論文明說理想世界不考慮效能：「In the ideal world we are not concerned with performance」。[同上 p.23](https://curtclifton.net/papers/MoseleyMarks06a.pdf) 在現實裡，他們承認仍然需要一些 accidental complexity：「We have seen two possible reasons why in practice — even with optimal language and infrastructure — we may require complexity which strictly is accidental.」理由是 Performance 與 Ease of Expression，並說「Of the two, we believe that performance will be the most common.」[同上 p.30](https://curtclifton.net/papers/MoseleyMarks06a.pdf)

**來源事實：**他們的建議是 Avoid 與 Separate：「the overriding aim must be to avoid state and control where they are not absolutely and truly essential. The recommendation of avoidance is however tempered by the acknowledgement that there will sometimes be complexity that either is truly essential (section 7.1.1) or, whilst not truly essential, is useful from a practical point of view (section 7.2.3).」[同上 p.31](https://curtclifton.net/papers/MoseleyMarks06a.pdf) 對應的 Table 2 把複雜度分成 Essential Logic、Essential Complexity、Accidental Useful Complexity、Accidental Useless Complexity，只有最後一類的建議是「Avoid」。[同上 p.33](https://curtclifton.net/papers/MoseleyMarks06a.pdf)

**設計推論：**Tar Pit 自己也需要第三類「Accidental Useful」，才不會把效能這類必要的東西一起砍掉。換句話說，essential／accidental 二分法本身不足以作為砍除準則，原作者也補上了護欄。grill-minimal 的 complete 後半段（「what makes the kept scope work」）在 Tar Pit 的分類裡大多會落在「Accidental Useful」。如果 SKILL.md 寫「cut accidental complexity」，模型就得自己分辨 useful 與 useless，而原作者用了一整個章節才處理這件事。所以第 3 點的建議句用「a simpler approach would ... still work」來表達這個門檻，不使用 accidental 這個字。

## Dieter Rams：Less, but better

**來源事實：**Vitsœ 官方網站上 Rams 的原則「Good design is as little design as possible」寫的是：「Less, but better – because it concentrates on the essential aspects, and the products are not burdened with non-essentials.」以及「Back to purity, back to simplicity.」[Vitsœ：Good design](https://www.vitsoe.com/us/about/good-design)

**來源事實：**同一組原則裡另外有「Good design is thorough down to the last detail」：「Nothing must be arbitrary or left to chance. Care and accuracy in the design process show respect towards the user.」以及「Good design makes a product useful」：「Good design emphasizes the usefulness of a product whilst disregarding anything that could possibly detract from it.」[Vitsœ：Good design](https://www.vitsoe.com/us/about/good-design)

**設計推論：**Rams 的 essential 是「少」的那一邊，「thorough down to the last detail」才是「全」的那一邊，兩者是不同的原則。「less, but better」本身就是兩個字互相約束的結構，跟 smallest complete 的結構相同。這反而說明 essential 單獨使用時不帶完整性護欄，Rams 也需要另外寫出來。

## Greg McKeown：Essentialism

**來源事實：**McKeown 官方網站的書頁寫道：「The Way of the Essentialist involves doing less, but better, so you can make the highest possible contribution.」以及「The Way of the Essentialist isn't about getting more done in less time. It's not about getting less done. It's about getting only the right things done.」[gregmckeown.com：Essentialism](https://gregmckeown.com/books/essentialism/) 同一頁也寫道：「By applying a more selective criteria for what is essential, the pursuit of less allows us to regain control of our own choices so we can channel our time, energy and effort into making the highest possible contribution toward the goals and activities that matter.」[同上](https://gregmckeown.com/books/essentialism/)

**限制：**本文只讀了官方書頁，沒有讀書的正文，所以不引用書中對「vital few」或判斷流程的細節。

**設計推論：**McKeown 明確否認 Essentialism 等於「getting less done」，這跟 complete 反對 MVP 化的立場一致。但他的準則是「the goals and activities that matter」，由選擇者本人判斷，而且他談的是個人的時間分配，不是軟體的 scope。如果搬進 agent 的 SKILL.md，「誰來判斷什麼 matter」就從使用者變成了 agent。grill-minimal 寫明「They are the user's to set」，正是為了擋住這一點。

## 實務者把 essential／accidental 用在 AI coding 上

### Wes McKinney：The Mythical Agent-Month

**來源事實：**McKinney 在 2026-02-17 的文章寫道：「Essential complexity is fundamental to achieving your goal: if you made the system any simpler, it would fall short of its problem statement. Accidental complexity is everything else imposed by our tools and processes」。[wesmckinney.com：The Mythical Agent-Month](https://wesmckinney.com/blog/mythical-agent-month/) 他接著說：「the accidental complexity is no problem at all anymore, but what's left is the essential complexity which was always the hard part. Agents can't reliably tell the difference.」又說 agent「also often tend to introduce unnecessary complexity, generating large amounts of defensive boilerplate that is rarely needed in real-world use.」[同上](https://wesmckinney.com/blog/mythical-agent-month/)

**來源事實：**談到 scope 時他寫道：「we still have to make good design decisions, say no to most product ideas, maintain conceptual integrity, and know when something is "done".」[同上](https://wesmckinney.com/blog/mythical-agent-month/)

**限制：**McKinney 說這組定義來自 Brooks「a follow-up essay to TMMM」，但他的措辭（「if you made the system any simpler, it would fall short of its problem statement」）是他自己的轉述，不是 Brooks 的原文。Brooks 的原文見上一節。

**設計推論：**McKinney 直接替第 2 點的風險作證：「Agents can't reliably tell the difference.」如果 leading word 要 agent 自己區分 essential 與 accidental，就是把這個它做不好的判斷交給它。他把「defensive boilerplate」歸為 accidental，代表這個 prior 會把防禦性程式碼往砍的方向推；grill-minimal 的 complete 只保留 kept scope 需要的防禦，所以兩者的方向不同。不過他的「say no to most product ideas」與「know when something is "done"」，正是 smallest 與 complete 這兩半。

### Jake Nations（Netflix）：The Infinite Software Crisis

**來源事實：**AI Engineer 官方演講頁的逐字稿中，Nations 說：「There's the essential complexity, which is really the fundamental difficulty of the actual problem you're trying to solve. Users need to pay for things. Orders must be fulfilled. This is the complexity of why your software system exists in the first place. And then second, there's this idea of accidental complexity. Everything else we've added along the way, workarounds, defensive code, frameworks, abstractions that made sense a while ago. It's all the stuff that we put together to make the code itself work.」[ai.engineer：The Infinite Software Crisis（7:41–8:03）](https://www.ai.engineer/talks/eIoohUmYpGI-infinite-software-crisis) 他也說：「In a real codebase, these two types of complexity are everywhere, and they get so tangled together that separating them requires context, history, and experience.」接著說「The generated output makes no such distinction」。[同上（8:13–8:21）](https://www.ai.engineer/talks/eIoohUmYpGI-infinite-software-crisis)

**限制：**引文取自演講頁上的自動逐字稿；頁面上的段落摘要是編輯整理的，所以本文只引用逐字稿。

**設計推論：**「all the stuff that we put together to make the code itself work」幾乎就是 grill-minimal 定義中「what makes the kept scope work」的字面。在實務者的用法裡，這一類東西屬於 accidental。這是不把 essential 當 leading word、也不在 mechanism 句子裡寫出 accidental 的最直接理由。

### Agent skill 與廠商官方指引

**來源事實：**在本機 `mattpocock/skills`、`addyosmani/agent-skills`、`anthropics/skills`、`anthropics/claude-code`、`openai/codex` 的 Markdown 檔案裡全文搜尋「essential complexity」、「accidental complexity」、「essentialism」，都沒有找到命中。essential 這個字只以一般語意出現，例如 `anthropics/skills` 的 model-migration 文件引用的 prompt「Skip non-essential context, and keep examples minimal.」（[`skills/claude-api/shared/model-migration.md` L673](https://github.com/anthropics/skills/blob/main/skills/claude-api/shared/model-migration.md)）。用網路搜尋 anthropic.com、platform.claude.com、openai.com、developers.openai.com 上的「accidental complexity」，也沒有找到官方頁面。

**限制：**Kent Beck、Addy Osmani、Matt Pocock 是否在其他地方（付費 newsletter、演講）用 essential complexity 來引導 agent，這次沒有找到一手來源，所以無法確認。

**設計推論：**前一份研究找到的 agent 指引，用的都是 simple／minimal／smallest 加上護欄（「clearly necessary」、「the smallest change that solves the problem」），沒有人用 essential 當主要的引導字。要用 essential 來引導 agent 的 scope，沒有現成的實務先例可以參考。

## 風險整理

| 風險 | 來源依據 | 現行 smallest complete 是否擋住 | 換成 essential 後 |
| --- | --- | --- | --- |
| agent 自己決定什麼是必要的，蓋過使用者的 goals | McKinney「Agents can't reliably tell the difference」；McKeown 的判斷者是選擇者本人 | 是：「trace it to the goal or constraint」、「They are the user's to set」 | 字面沒有綁定，要靠定義句補 |
| 「essentials only」被讀成 MVP、偷工減料 | Brooks 的 prototype「make no attempt to handle the exceptions」；essentials 的日常語意 | 是：complete 明列 edge cases、security、tests | prior 偏向基本款 |
| 把讓 scope 能運作的東西歸為 accidental 而砍掉 | Tar Pit 把 performance 列為 accidental；Nations 把 defensive code 列為 accidental；McKinney 的「defensive boilerplate」 | 是：「what makes the kept scope work」 | prior 方向相反 |
| approach 軸沒有可檢查的測試 | Tar Pit 的「have to」測試 | 否：只有「the simplest approach」 | 字本身不帶測試；建議用第 3 點的白話句補上 |
