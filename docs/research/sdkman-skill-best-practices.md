# Research: agent 使用 SDKMAN 執行 Java／Maven／Gradle 工作的最佳方案

> 研究問題：agent 應如何在不混淆 shell JDK、build runtime 與 project toolchain 的前提下使用 SDKMAN。
> 一手來源：SDKMAN 官方文件與 2026-08-05 的官方原始碼、Apache Maven 官方文件、Gradle 9.7.0 官方文件、OpenAI Codex 與 Anthropic Claude Code 官方 agent 文件。
> 撰寫日期：2026-08-12

## 結論

最佳方案不是「看到 Java 版本就先跑 `sdk use`」，而是依責任分成三層：

1. **專案 build 層**宣告編譯、測試與執行需要的 JDK：Maven 用 Toolchains，Gradle 用 Java Toolchains；產物相容性另用 Maven `maven.compiler.release` 或 Gradle `options.release`。
2. **build runtime 層**負責啟動 Maven 或 Gradle：只有啟動 JVM 本身不相容、舊專案未宣告 toolchain、使用者指定 JDK／vendor，或專案明確要求 `.sdkmanrc` 時，agent 才切 shell JDK。
3. **本機 SDK 管理層**由 SDKMAN 提供已安裝的候選版本。預設只在單次 shell 中 `sdk use` 或 `sdk env`；`sdk install`、`sdk env install`、`sdk default` 與啟用 auto-env 都是持久或下載操作，不應由 agent 靜默執行。

理由是 compiler target、build runtime、project toolchain 是不同控制面。Maven 官方明確說 `source` 不保證使用指定 JDK，Toolchains 才能讓 plugin 使用與 Maven 啟動 JDK 不同的 JDK；Gradle 官方也把 Client JVM、Daemon JVM 與 project toolchain 分開。[Maven Compiler Plugin：`source`／`target`](https://maven.apache.org/plugins/maven-compiler-plugin/examples/set-compiler-source-and-target.html) [Maven Toolchains](https://maven.apache.org/guides/mini/guide-using-toolchains) [Gradle Daemon](https://docs.gradle.org/current/userguide/gradle_daemon.html) [Gradle Java Toolchains](https://docs.gradle.org/current/userguide/toolchains.html)

主要取捨是：讓 build toolchain 管理 JDK 可重現性較高，卻要求專案已有正確設定；單次 `sdk use` 能救援舊 build 或不相容的 launcher，但只代表 agent 當下 shell，不能取代專案契約。Hook 可以補充 deterministic 檢查，卻不是完整 enforcement boundary，也不應自動改寫所有 Java build command。[OpenAI Codex Hooks：tool coverage](https://developers.openai.com/codex/hooks#tool-coverage) [Claude Code Hooks](https://code.claude.com/docs/en/hooks)

## 推薦架構

| 判斷層 | Source of truth | Agent 預設行為 | 不應做的事 |
| --- | --- | --- | --- |
| Build tool 版本 | `mvnw`／`gradlew` 與 wrapper 設定 | 優先使用專案 wrapper | 因 SDKMAN 已裝 Maven／Gradle 就繞過 wrapper |
| Build runtime JVM | Maven 的啟動需求；Gradle compatibility、Daemon JVM criteria 或 `org.gradle.java.home` | 先確認 launcher 是否相容；必要時才在同一 shell 切 JDK | 從 compiler target 反推 launcher 必須完全同版 |
| Compile／test JVM | Maven／Gradle toolchain 宣告 | 交給 build tool 選擇與診斷 | 在 toolchain 已可用時強制改 `JAVA_HOME` |
| 產物相容性 | Maven `release`；Gradle `options.release` | 保留專案設定 | 把 `source`／`target` 當成完整 API 相容保證 |
| SDK 安裝與預設 | 使用者授權、已安裝 SDKMAN candidates | 只用已安裝的精確 id；下載與全域變更先詢問 | 靜默 `install`、`env install`、`default` 或改 auto-env |

Gradle 官方建議使用 Wrapper；它執行專案宣告的 Gradle 版本，必要時自行下載 distribution。Maven Wrapper 同樣由專案的 `mvnw` 啟動指定 Maven distribution。因此，SDKMAN 管理 Maven／Gradle executable 應是「無 wrapper 或使用者明確要求」的後備路徑。[Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html) [Maven Wrapper](https://maven.apache.org/tools/wrapper/index.html)

## SDKMAN 語義與安全邊界

### `sdk use` 與 `sdk default`

**來源事實：**SDKMAN 官方文件把 `sdk use <candidate> <version>` 定義為只切換目前 shell；`sdk default` 則讓之後開啟的 shells 使用該版本。[SDKMAN Usage：Use／Default Version](https://sdkman.io/usage/#use-version)

目前 Bash 實作會先確認版本目錄已安裝，再更新 candidate home 與目前 shell 的 `PATH`；它不會下載。若該 candidate 尚無 `current` link，`sdk use` 有一個例外：會建立 default link，因此「永遠零持久副作用」並非原始碼層級的絕對保證。[`sdkman-use.sh`，2026-08-05 snapshot](https://github.com/sdkman/sdkman-cli/blob/f02e5de113ea46a95e5e2fd795eabe6f2b7d4095/src/main/bash/sdkman-use.sh) `sdk default` 則直接更新 `current` link。[`sdkman-default.sh`](https://github.com/sdkman/sdkman-cli/blob/f02e5de113ea46a95e5e2fd795eabe6f2b7d4095/src/main/bash/sdkman-default.sh)

**設計推論：**agent 應把 `sdk use` 與實際 workload 放在同一個 shell invocation，並在執行前確認精確的已安裝 id。不要假設下一次 tool call 繼承該 shell，也不要為了單次 build 改 default。

### `.sdkmanrc`、`sdk env` 與 auto-env

**來源事實：**`.sdkmanrc` 是專案根目錄的 `candidate=version` 清單；`sdk env` 對每個條目確認版本已安裝後，呼叫 `sdk use` 更新目前 shell。現行 parser 會移除註解與空白，並只接受小寫 candidate 名稱加 `=` 的格式；它不會把 `.sdkmanrc` 當 shell script `source`。[SDKMAN Usage：Env Command](https://sdkman.io/usage/#env-command) [`sdkman-env.sh`](https://github.com/sdkman/sdkman-cli/blob/f02e5de113ea46a95e5e2fd795eabe6f2b7d4095/src/main/bash/sdkman-env.sh)

若指定版本缺少，普通 `sdk env` 會停止並提示 `sdk env install`；後者才逐項安裝，並刻意保留原 default，最後把版本載入目前 shell。[`sdkman-env.sh`](https://github.com/sdkman/sdkman-cli/blob/f02e5de113ea46a95e5e2fd795eabe6f2b7d4095/src/main/bash/sdkman-env.sh) `sdkman_auto_env=true` 會在 zsh 的目錄變更或 Bash prompt 路徑上自動執行 `sdk env`，離開環境時再 clear 回 default。[`sdkman-init.sh`](https://github.com/sdkman/sdkman-cli/blob/f02e5de113ea46a95e5e2fd795eabe6f2b7d4095/src/main/bash/sdkman-init.sh)

**設計推論：**已納入版本控制的 `.sdkmanrc` 是強烈的專案意圖，但 agent 仍應先讀其全部 candidates，因為它可能同時切 Java、Maven、Gradle、Kotlin 等工具。普通 `sdk env` 可作為已安裝版本的單次切換；`sdk env install` 是下載／持久寫入，必須另行授權。Agent 不應修改使用者的全域 SDKMAN config 來開啟 auto-env；非互動工具呼叫也不應依賴 `cd` hook 自動生效。

### `sdk install` 的持久與供應鏈邊界

**來源事實：**`sdk install` 會下載並解壓 candidate；互動模式還會詢問是否設為 default。[SDKMAN Usage：Installing an SDK](https://sdkman.io/usage/#installing-an-sdk) 現行原始碼顯示 install 會寫入 `${SDKMAN_DIR}/candidates`，並從 SDKMAN API 下載 candidate-specific post-installation hook、`source` 後執行，再驗證產生的 archive checksum。[`sdkman-install.sh`](https://github.com/sdkman/sdkman-cli/blob/f02e5de113ea46a95e5e2fd795eabe6f2b7d4095/src/main/bash/sdkman-install.sh)

**設計推論：**對 agent 而言，install 不只是「補一個目錄」，而是網路下載、本機持久寫入與執行官方遠端安裝 hook 的組合。缺少版本時應列出相容的已安裝 ids，沒有可用項目才向使用者確認 exact candidate id／vendor 後安裝。不得自行設 `sdkman_auto_answer=true` 來繞過確認。

### SDKMAN 本身的 shell 邊界

**來源事實：**`sdk` 是載入在目前 Bash／zsh 的 shell function；初始化檔會讀 `${SDKMAN_DIR}/etc/config`、載入模組 scripts、設定 candidate home 與 `PATH`。[`sdkman-init.sh`](https://github.com/sdkman/sdkman-cli/blob/f02e5de113ea46a95e5e2fd795eabe6f2b7d4095/src/main/bash/sdkman-init.sh) SDKMAN 官方文件也只承諾 `sdk use` 作用於目前 terminal。[SDKMAN Usage](https://sdkman.io/usage/#use-version)

**設計推論：**agent 應顯式載入 `sdkman-init.sh`，然後在同一 invocation 執行 `sdk use`／`sdk env` 與 workload。若 detached process 或 host 每次建立新 shell，單獨先跑一次 `sdk use` 沒有可證明的後續效果。

## Maven：target 與執行 JDK 不是同一件事

### `release`、`source`、`target`

**來源事實：**從 JDK 9 起，`javac --release` 同時限制語言規則、class target 與指定 Java SE release 的 public API；Maven Compiler Plugin 以 `maven.compiler.release` 暴露它。可用 release 包含目前 JDK release 與有限數量的舊 release。[Maven Compiler Plugin：`--release`](https://maven.apache.org/plugins/maven-compiler-plugin/examples/set-compiler-release.html)

`maven.compiler.source` 只限制 source language level，`target` 只控制 bytecode level。官方明說，`target` 不阻止誤用較新 JRE API，而 `source` 不保證程式能在該版本 JDK 編譯；若要使用與 Maven launcher 不同的指定 JDK，應用 Toolchains。[Maven Compiler Plugin：`source`／`target`](https://maven.apache.org/plugins/maven-compiler-plugin/examples/set-compiler-source-and-target.html)

**設計推論：**看到 `<maven.compiler.release>17</maven.compiler.release>` 不足以推論必須先 `sdk use java 17-*`。若 Maven 正跑在相容的較新 JDK，且 compiler 支援 release 17，這個設定本來就可能成功。`invalid target release` 等錯誤也應先判斷實際 compiler 來源與 toolchain，而不是只看 POM 數字。

### Maven Toolchains 的角色

**來源事實：**Maven Toolchains 讓專案指定一個與 Maven 執行 JDK 獨立的 JDK，並把選到的 toolchain 放進 MavenSession，供 compiler、Surefire、Failsafe、Javadoc 等 toolchain-aware plugins 使用。[Maven Guide to Using Toolchains](https://maven.apache.org/guides/mini/guide-using-toolchains) Compiler Plugin 預設使用執行 Maven 的 JDK compiler，但可由 Toolchains 覆寫。[Maven Compiler Plugin：compile goal](https://maven.apache.org/plugins/maven-compiler-plugin/compile-mojo.html)

Toolchains Plugin 3.2.0 起可自動探索已安裝 JDK；官方範例直接顯示它能發現 `~/.sdkman/candidates/java/...`。`select-jdk-toolchain` 可從明示 `toolchains.xml` 與探索結果選擇，若關閉 discovery 才限於明示設定。[Maven JDK discovery](https://maven.apache.org/plugins/maven-toolchains-plugin/toolchains/jdk-discovery.html)

**設計推論：**專案已有 Maven Toolchains 時，agent 應先讓 build 自己選擇；toolchain 缺少就回報／診斷 toolchain，不要先改 shell 以掩蓋專案或機器設定。Shell JDK 仍要能啟動 Maven 本身及執行 build extensions／未採用 toolchain 的 plugins；Toolchains 不是 Maven launcher 的替代品，也不能保證第三方 plugin 都使用它。

## Gradle：project toolchain、Client 與 Daemon 必須分開

### Java Toolchains

**來源事實：**Gradle Java Toolchains 可在 project 或 task 層指定 compiler、test launcher、JavaExec 與 Javadoc 所用 JDK；`options.release` 另負責嚴格 cross-compilation。官方比較表明 toolchain 確保 JDK、`--release` 防止誤用較新 API，而 `sourceCompatibility`／`targetCompatibility` 兩者都不完整。[Gradle Java Toolchains：comparison](https://docs.gradle.org/current/userguide/toolchains.html#sec:combining_java_toolchains)

Gradle 預設會自動偵測本機 JDK，明確支援 SDKMAN、`JAVA_HOME`、Maven Toolchains 等來源。只有找不到符合項目，且專案已設定 toolchain download repository 時，auto-provisioning 才會下載 JDK 到 Gradle User Home；已下載 JDK 不會自動升級。[Gradle Java Toolchains：auto-detection／provisioning](https://docs.gradle.org/current/userguide/toolchains.html#sec:auto_detection)

**設計推論：**專案已有 Gradle toolchain 時，不必把 SDKMAN candidate 切成目前 JDK；Gradle 可直接發現它。Agent 可用 `./gradlew -q javaToolchains` 診斷實際選項。不要為修一個 build 靜默切換 `org.gradle.java.installations.auto-detect`／`auto-download`，也不要把 Gradle provisioning 誤報成 SDKMAN install。

### Client JVM、Daemon JVM 與 project JVM

**來源事實：**Gradle command 涉及可使用不同 Java 版本的 Client JVM 與 Daemon JVM。Client 由 wrapper script 的 `JAVA_HOME`／`PATH`／IDE 啟動；Daemon 可由 `org.gradle.java.home`、Tooling API 或 Daemon JVM criteria 決定。若存在 `gradle/gradle-daemon-jvm.properties` criteria，它優先於 `JAVA_HOME` 與 `org.gradle.java.home`。[Gradle Daemon：Client vs Daemon](https://docs.gradle.org/current/userguide/gradle_daemon.html#sec:gradle_daemon) [Gradle Daemon JVM criteria](https://docs.gradle.org/current/userguide/gradle_daemon.html#daemon_jvm_criteria)

Gradle 9.7.0 本身需 JVM 17 至 26，但較舊 JDK 仍可透過 toolchain 編譯、較舊 JVM 可執行 tests；能執行 Gradle 與能作為 task toolchain 是兩個相容性軸。[Gradle 9.7.0 Compatibility Matrix](https://docs.gradle.org/current/userguide/compatibility.html#java_runtime)

**設計推論：**切 shell JDK 主要改的是 Client 啟動來源；它不一定覆寫既有 Daemon criteria，也不等於 JavaCompile／Test 使用同一 JDK。遇到 Gradle mismatch 時應分別確認 wrapper 版本、Client／Daemon JVM、project toolchain 與失敗 task。Toolchain 設定剛改而 daemon cache 仍舊時，才把 `./gradlew --stop` 當針對性診斷，不要每次 build 都停止 daemon。

## 何時切 shell JDK

### 真的需要切

- 使用者明確指定 SDKMAN candidate、Java major 或 vendor。
- 專案有已審視的 `.sdkmanrc`，而工作就是按該專案環境執行。
- Maven／Gradle launcher 無法在目前 JVM 啟動，例如 wrapper 與 runtime compatibility 不符；這發生在 build toolchain 有機會接手之前。
- 舊專案沒有 build toolchain，實際 compiler／test／plugin 明確依賴 launcher JDK。
- 真實執行輸出證明 runtime class-file 不相容，且因果鏈指向目前 shell／launcher，而不是某個 forked task、daemon 或 toolchain。

### 應交給 build toolchain

- POM 只有 `maven.compiler.release`／`source`／`target`，或 Gradle 只有 `options.release`／compatibility 設定。
- Maven Toolchains 已宣告並能找到 matching JDK。
- Gradle Java Toolchain 已宣告，所需 JDK 可由 auto-detection 找到。
- compile／test JDK 可與 Maven launcher 或 Gradle Daemon JDK 不同。
- Gradle Daemon JVM criteria 已固定 build runtime；shell `JAVA_HOME` 不具最高優先權。

### 決策順序

1. 使用專案 wrapper，辨識目前失敗發生在 launcher、build configuration、compile、test 還是 application runtime。
2. 讀 `.sdkmanrc`、Maven toolchain 設定、Gradle Java Toolchains／Daemon JVM criteria；不要只讀 compiler target。
3. 確認實際 runtime：Maven 可用 `./mvnw -version`；Gradle 可從 `./gradlew --version`、`javaToolchains` 與 daemon 設定分層判讀。
4. build toolchain 可滿足就不切 shell。只有 launcher／legacy path 需要時，選已安裝 exact SDKMAN id，在同一 shell 切換並執行原命令。
5. 版本未安裝時停止；列出已安裝 alternatives。下載、vendor 選擇、default 與全域 auto-env 需要使用者決定。

## Agent skill 的觸發與 hook 設計

### 官方可證明的部分

OpenAI Codex 一開始只把 skill 的 `name` 與 `description` 放進 context，模型決定使用後才載入完整 `SKILL.md`；implicit invocation 是任務與 `description` 的語意配對。官方也明說 skill 清單有 context budget，描述可能縮短或 skill 可能省略。[OpenAI Codex Skills](https://developers.openai.com/codex/skills#how-chatgpt-and-codex-use-skills) Claude Code 同樣以 description 讓 Claude 判斷相關性，並提供 `disable-model-invocation` 控制只允許明確調用。[Claude Code Skills](https://code.claude.com/docs/en/skills)

Codex `PreToolUse`／`PostToolUse` matcher 比對的是 tool name；`Bash` hook 必須再自行檢查 `tool_input.command`。官方明說 specialized tool paths 可能不進入預設 hook path，因此 hooks 是 guardrail，不是完整 enforcement boundary。[OpenAI Codex Hooks：matchers／coverage](https://developers.openai.com/codex/hooks#matcher-patterns) Codex 的 `PostToolUse` 在 command 執行後才能讀到 `tool_input` 與 `tool_response`，無法撤銷已發生副作用。[OpenAI Codex Hooks：PostToolUse](https://developers.openai.com/codex/hooks#posttooluse)

Claude Code 有 `PreToolUse`、`PostToolUse` 與 `PostToolUseFailure` 等事件；Bash permission matching 可辨識部分 compound command 與固定 wrappers，但官方也列出 `direnv exec`、`mise exec`、`docker exec` 等不會被剝除。[Claude Code Hooks](https://code.claude.com/docs/en/hooks) [Claude Code Bash matching](https://code.claude.com/docs/en/permissions#bash-command-matching) Skill-local hooks 只在 skill 啟用期間生效，不能用來先偵測 build command 再啟動同一 skill。[Claude Code hook locations](https://code.claude.com/docs/en/hooks#hook-locations)

### 對本 skill 的建議推論

1. **保留 implicit-enabled，但把邊界寫進 description。**適用觸發包括使用者要求 SDKMAN／特定 vendor／`.sdkmanrc`，或已確認是 shell／launcher JDK mismatch；明確排除只有 compiler target 的情況。這符合兩個 host 以 description 做語意路由的官方模型，但不是每次 build 的保證 gate。
2. **不要用 hook 自動攔截每個 `java`、`mvn`、`gradle`。**官方只能證明支援的 top-level tool event；不能證明看穿 wrapper、script、Docker、IDE、子程序或外部 terminal，也不能證明 hook context 一定使模型載入指定 skill。
3. **若保留 hook，只做窄且結構化的 advisory detector。**先確認 `tool_name` 是 shell、`tool_input.command` 是實際 build command、結果確實失敗，再用 exit status／結構化 failure 欄位與錯誤模式提供 diagnosis context。不要只掃 `tool_response` 的字串，否則讀文件、原始碼或 diff 也可能包含相同錯誤文字。
4. **若要 preflight enforcement，另做明確可測的 command wrapper。**只對可解析的 direct Maven／Gradle invocation 生效；確認 `.sdkmanrc` 與 candidate 已安裝後，才可把 `sdk env`／`sdk use` 和原命令組合在同一 shell。無法唯一判定、需下載、涉及 default，或偵測到既有 build toolchain 時應 fail open 並提示，不得猜測 vendor。
5. **跨 host 不宣稱等價。**Codex matcher 只到 tool name；Claude Code 雖能更細分 Bash command，仍有 wrapper 盲點。共用 skill 應表達決策語義，各 host hook 只作 capability-gated enhancement。

上列 3–5 是由官方 hook coverage、事件時序與 skill invocation 模型導出的設計推論；官方沒有提供「SDKMAN skill hook」的標準實作，也沒有證據保證任一 hook 能攔截所有 Java command。

## 檢驗清單

### 行為正確性

- [ ] 有 `.sdkmanrc` 且 candidates 已安裝：同一 shell 中 `sdk env` 後執行原 build，未改 default。
- [ ] `.sdkmanrc` 缺少 candidate：停止並請求 install 授權；沒有執行 `sdk env install`。
- [ ] 只有 Maven `release`／`source`／`target`：不因 target 數字自動切 JDK。
- [ ] Maven Toolchains 可用：由 Maven 選 toolchain；shell JDK 只需滿足 launcher。
- [ ] Maven Toolchains 缺少：報 matching constraint 與 discovered candidates，不以任意 `JAVA_HOME` 掩蓋。
- [ ] Gradle toolchain 可偵測 SDKMAN JDK：不先 `sdk use`，以 `javaToolchains` 驗證。
- [ ] Gradle Daemon criteria 存在：不宣稱 shell `JAVA_HOME` 會覆寫它。
- [ ] wrapper 與目前 launcher JVM 不相容：只切已安裝 candidate，重跑完全相同命令並保留 exit status。
- [ ] install／default／auto-env：每一種都另有明確授權與 exact id／vendor。

### Trigger 與 hook eval

- [ ] 正向 prompts：`use Java 17 with SDKMAN`、`follow .sdkmanrc`、已確認 launcher class-file mismatch 會觸發 skill。
- [ ] 負向 prompts：只提 `maven.compiler.release=17`、Gradle `options.release=11`、toolchain 已正常選取時不切 shell。
- [ ] Hook 只接受真正的 shell build command；`sed`／`cat`／`git diff` 輸出含 `UnsupportedClassVersionError` 或 class-file 文字時不觸發。
- [ ] Hook 檢查真實 failure／exit status，不把成功 command 中的歷史 log 當本次失敗。
- [ ] Direct `mvn`、`./mvnw`、`gradle`、`./gradlew`、compound command、wrapper 中間接執行分開測；未覆蓋者明確記為 unsupported。
- [ ] Codex 與 Claude Code 各自驗證 matcher、輸入 schema、trust／enable 狀態；不以單一 host 結果宣稱跨 host qualified。
- [ ] 所有 retry 都證明 workload 在成功切換的同一 shell 啟動，並保留原 command 與 exit code。

## 一手來源

- [SDKMAN Usage](https://sdkman.io/usage/)
- [SDKMAN CLI source snapshot `f02e5de`](https://github.com/sdkman/sdkman-cli/tree/f02e5de113ea46a95e5e2fd795eabe6f2b7d4095)
- [Maven Compiler Plugin：`--release`](https://maven.apache.org/plugins/maven-compiler-plugin/examples/set-compiler-release.html)
- [Maven Compiler Plugin：`source`／`target`](https://maven.apache.org/plugins/maven-compiler-plugin/examples/set-compiler-source-and-target.html)
- [Maven Guide to Using Toolchains](https://maven.apache.org/guides/mini/guide-using-toolchains)
- [Maven Toolchains JDK discovery](https://maven.apache.org/plugins/maven-toolchains-plugin/toolchains/jdk-discovery.html)
- [Gradle Java Toolchains](https://docs.gradle.org/current/userguide/toolchains.html)
- [Gradle Daemon](https://docs.gradle.org/current/userguide/gradle_daemon.html)
- [Gradle 9.7.0 Compatibility Matrix](https://docs.gradle.org/current/userguide/compatibility.html)
- [OpenAI Codex Skills](https://developers.openai.com/codex/skills)
- [OpenAI Codex Hooks](https://developers.openai.com/codex/hooks)
- [Anthropic Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Anthropic Claude Code Hooks](https://code.claude.com/docs/en/hooks)
- [Anthropic Claude Code Permissions](https://code.claude.com/docs/en/permissions)
