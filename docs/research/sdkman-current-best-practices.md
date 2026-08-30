# SDKMAN-managed JVM workload 的現行最佳實務

> Issue：[整理 SDKMAN 與 JVM build tool 的現行最佳實務（#25）](https://github.com/shihyuho/skills/issues/25)
>
> 查核時間：2026-08-30（Asia/Taipei）
>
> 範圍：SDKMAN、Apache Maven、Gradle，以及直接相關的 JVM toolchain 文件。
>
> 歷史文件 `docs/research/sdkman-skill-best-practices.md` 僅用來理解前次設計，不作為證據。

## 摘要結論

現行 `skills/sdkman/SKILL.md` 的核心方向正確：`sdk use`／`sdk env` 與 workload 必須在同一個 shell；project wrapper 優先於 SDKMAN-managed Maven／Gradle；Maven Toolchains 與 Gradle 的 Daemon／task toolchains 不應被 shell `JAVA_HOME` 混為一談；setup 失敗不得誤報成 test／build 失敗。

需要補強的不是更多候選版本選擇演算法，而是四個明確邊界：

1. **`.sdkmanrc` 先完整驗證，再執行 `sdk env`。** 現行 SDKMAN 逐行套用 candidate；若後面的 candidate 缺少，前面的 shell 切換已發生，因此 `sdk env` 不是可假設為 atomic 的 transaction。[`sdkman-env.sh`（2026-08-30 snapshot）](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-env.sh)
2. **SDKMAN 的 network availability 不是強制 no-network mode。** `sdkman_healthcheck_enable=false` 只略過 healthcheck；官方明說需要網路的 command 仍會在實際無網路時失敗。Maven `-o` 與 Gradle `--offline` 只約束各自的 build dependency resolution，也不能保證 wrapper bootstrap 不下載 distribution。[SDKMAN Usage：Network Availability](https://sdkman.io/usage/#network-availability) [Maven CLI `--offline`](https://maven.apache.org/ref/current/maven-embedder/cli.html) [Gradle Dependency Caching：offline mode](https://docs.gradle.org/current/userguide/dependency_caching.html#sec:offline-mode)
3. **安裝與 wrapper 有供應鏈邊界。** SDKMAN 的 Bash install path 會下載並 `source` server-provided post-install hook，之後才在 metadata、config 與本機工具允許時驗證產出的 ZIP／checksum；未觀察到實際 validation path 時，artifact integrity 應標 **unknown**。SDKMAN 只為最新 release 提供 security updates，且 5.23.0 修補了 checksum verification 中的 critical command injection；Gradle 與 Maven Wrapper 也可能下載並執行 build-tool distribution。Agent 不應開啟 `sdkman_insecure_ssl`，也不應把 install／wrapper bootstrap 說成純環境切換。[`sdkman-install.sh`（2026-08-30 snapshot）](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-install.sh) [SDKMAN Security Policy](https://github.com/sdkman/sdkman-cli/security) [SDKMAN 5.23.0 release](https://github.com/sdkman/sdkman-cli/releases/tag/5.23.0) [SDKMAN Usage：Configuration](https://sdkman.io/usage/#configuration) [Gradle Wrapper verification](https://docs.gradle.org/current/userguide/gradle_wrapper.html#sec:verification) [Maven Wrapper checksum verification](https://maven.apache.org/tools/wrapper/#checksum-verification-of-downloaded-binaries)
4. **失敗報告至少要分四層。** Agent environment initialization、wrapper／Client launcher、build runtime／toolchain resolution、requested goal／task 是不同邊界。只有第一層失敗才能直接說「原 workload command 未執行」；wrapper、Maven `validate` toolchain、Gradle Daemon 或 task toolchain 失敗時，原 command 可能已啟動，但 requested test／task action 尚未開始。[Maven Toolchains usage](https://maven.apache.org/plugins/maven-toolchains-plugin/usage.html) [Gradle Client vs. Daemon](https://docs.gradle.org/current/userguide/gradle_daemon.html#sec:gradle_daemon)

## 查核基線與版本敏感性

- SDKMAN 官方 live docs 於 2026-08-30 查核；source facts 固定到官方 `sdkman-cli` commit [`1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8`](https://github.com/sdkman/sdkman-cli/commit/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8)（commit date 2026-08-27）。當時最新正式 release 是 [`5.23.0`](https://github.com/sdkman/sdkman-cli/releases/tag/5.23.0)（2026-05-04）。官方 security policy 只支援 latest release；`master` 可能含尚未進 release 的實作，因此本文以 live docs 定 public contract，以 immutable source 說明可觀察實作細節，不能把 source HEAD 當成已安裝 CLI 的 security 狀態。[SDKMAN Security Policy](https://github.com/sdkman/sdkman-cli/security)
- Maven `current` CLI reference 於 2026-08-30 指向 Maven 3.9.16；Maven Toolchains Plugin 文件顯示 3.3.0，Compiler Plugin 文件顯示 3.15.0。[Maven 3.9.16 CLI](https://maven.apache.org/ref/3.9.16/maven-embedder/cli.html) [Maven Toolchains Plugin](https://maven.apache.org/plugins/maven-toolchains-plugin/) [Maven Compiler Plugin `--release`](https://maven.apache.org/plugins/maven-compiler-plugin/examples/set-compiler-release.html)
- Gradle `current` User Manual 於 2026-08-30 是 9.7.1；其 runtime compatibility、Daemon criteria 與 toolchain provisioning 都是版本敏感內容，本文不把 9.7.1 的數字硬寫成長期 skill policy。[Gradle 9.7.1 compatibility](https://docs.gradle.org/current/userguide/compatibility.html) [Gradle 9.7.1 Daemon](https://docs.gradle.org/current/userguide/gradle_daemon.html) [Gradle 9.7.1 Toolchains](https://docs.gradle.org/current/userguide/toolchains.html)

## 一、SDKMAN 原生語義

### Shell initialization

SDKMAN 官方支援 Bash／zsh；安裝後要開新 terminal，或在目前 shell `source "$HOME/.sdkman/bin/sdkman-init.sh"`，再以 `sdk version` 驗證。[SDKMAN Installation](https://sdkman.io/install/)

現行 source 的 `sdkman-init.sh` 會：

- 預設 `SDKMAN_DIR="$HOME/.sdkman"`，但尊重既有 `SDKMAN_DIR`；
- `source` `${SDKMAN_DIR}/etc/config`；
- `source` `${SDKMAN_DIR}/src` 與 `${SDKMAN_DIR}/ext` 下的 `sdkman-*.sh`；
- 依每個 candidate 的 `current` path 設定 `*_HOME` 與 `PATH`；
- 視 config 安裝 Bash／zsh auto-env hook；
- 在缺少時建立 `${SDKMAN_DIR}/var/delay_upgrade`。

以上是 implementation facts，不應壓進主 skill；它們只用來界定「source SDKMAN」本身會執行本機 extensions 並可能寫入 SDKMAN state，不能宣稱絕對零副作用。[`sdkman-init.sh`（2026-08-30 snapshot）](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-init.sh)

### `sdk use`、`sdk default` 與 exit status

官方 public contract 是：

- `sdk use <candidate> <version>` 只影響目前 shell；
- `sdk default <candidate> <version>` 影響後續 shells；
- candidate version 必須先安裝才能 `use` 或 `default`。[SDKMAN Usage：Use／Default](https://sdkman.io/usage/#use-version)

現行 Bash implementation 會直接更新目前 shell 的 candidate home 與 `PATH`；如果 candidate 尚無 `current` link，第一次 `sdk use` 仍會建立它並把該版本設為 default。因此，「current-shell only」描述的是選擇作用域，不代表檔案系統必然沒有持久變化。[`sdkman-use.sh`（2026-08-30 snapshot）](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-use.sh) [`sdkman-path-helpers.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-path-helpers.sh)

`sdk` shell function 會保留並回傳被 dispatch command 的 return code。[`sdkman-main.sh`（2026-08-30 snapshot）](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-main.sh) Agent orchestration 仍必須把 setup 與 workload 組成 status-preserving gate；精確的 host-shell composition 不屬於本研究允許的 source scope，無法確認時應標 **unknown**，不可只靠 output keyword 判定成功或失敗。

### `.sdkmanrc`、`sdk env` 與 auto-env

官方文件把 `.sdkmanrc` 定位在 project base directory，內容是多個 `candidate=version`；`sdk env` 在目前 shell 套用它，`sdk env clear` 回復 defaults，`sdk env install` 會下載缺少 candidates。`sdkman_auto_env=true` 會在進入有 `.sdkmanrc` 的目錄時自動切換，離開時回復 defaults。[SDKMAN Usage：Env Command](https://sdkman.io/usage/#env-command)

2026-08-30 source 顯示：

- `sdk env` 只找目前目錄的 `.sdkmanrc`，不會原生向 parent directories 搜尋；
- parser 移除 comments／whitespace，只接受小寫 candidate name 的 `candidate=version`；它不會把 `.sdkmanrc` 當 shell script `source`；
- candidates 依檔案順序逐項 check-and-use，遇到缺少版本才回傳失敗；先前成功的 candidate 不會 rollback；
- 全部成功後才設定 `SDKMAN_ENV=$PWD`；
- `sdk env install` 對每個條目執行 install，再 load env；若 candidate 原本已有 default symlink，程式嘗試保留它；若原本沒有 `current` link，後續 `sdk use` 仍可能建立 default link。

因此 skill 必須在呼叫 `sdk env` 前先完整解析並驗證所有 declarations 都已安裝；只做 `test -f .sdkmanrc` 不足以保證 failure 前不會部分切換。[`sdkman-env.sh`（2026-08-30 snapshot）](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-env.sh)

auto-env 在 zsh 註冊 `chpwd_functions`，在 Bash 改寫 `PROMPT_COMMAND`，而且只在目前 `PWD` 有 `.sdkmanrc` 時呼叫 `sdk env`。Agent workload 不應依賴互動 shell hook，也不應為單次 command 改使用者全域 auto-env config。[`sdkman-init.sh`（2026-08-30 snapshot）](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-init.sh)

### Candidate install、default 與 lifecycle

`sdk install` 會下載並安裝 candidate；若目前已有另一個 current version 且不是 auto-answer path，官方流程會詢問是否把新版本設為 default。指定 exact version 是官方支援形式。[SDKMAN Usage：Installing an SDK](https://sdkman.io/usage/#installing-an-sdk)

對 agent 而言應區分三種 mutation：

| 操作 | 可觀察 mutation | Policy |
| --- | --- | --- |
| `sdk use` | 改目前 shell；candidate 沒有 `current` 時可能建立 link | exact installed id 可單次使用；需知道首次 use 的 link side effect |
| `sdk default` | 改 candidate `current`，影響後續 shells | 只有使用者明確要求 persistent default 才做 |
| `sdk install`／`sdk env install` | 網路下載、寫入 candidates；可能伴隨 default link 行為 | 每個 exact id 與下載／安裝都需授權 |

這個 policy 比「install 只是補檔案」更保守，因為現行 install path 會下載 artifact 與 post-install hook、`source` hook、產生 ZIP，之後才進入 archive／checksum validation path；metadata 缺失、checksum 被停用或缺少可用驗證工具時，validation 可能略過。因此未觀察到實際 branch 與結果時，integrity status 是 **unknown**。[`sdkman-install.sh`（2026-08-30 snapshot）](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-install.sh)

### Offline／network availability

SDKMAN 現行 public term 是 **Network Availability**，不是使用者可切換的強制 offline sandbox。SDKMAN 會 healthcheck API；無網路時，需要 internet 的 commands 不可用。`sdkman_healthcheck_enable=false` 只略過檢查並立即繼續，實際需要網路的 command 仍會失敗。[SDKMAN Usage：Network Availability](https://sdkman.io/usage/#network-availability)

現行 source 在 healthcheck 判定 unavailable 時，`sdk list <candidate>` 只顯示 installed versions；已安裝 exact candidate 可由 local state 解析，缺少版本則回報 internet unreachable。[`sdkman-availability.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-availability.sh) [`sdkman-list.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-list.sh) [`sdkman-env-helpers.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-env-helpers.sh)

Policy 結論：

- 「使用已安裝 candidate」與「禁止任何 network attempt」不是同一要求。
- 若使用者只要求 build offline，保留原 wrapper command 並使用 Maven `-o`／Gradle `--offline`；不要把 SDKMAN healthcheck config 當 build offline flag。[Maven CLI](https://maven.apache.org/ref/current/maven-embedder/cli.html) [Gradle CLI](https://docs.gradle.org/current/userguide/command_line_interface.html#sec:command_line_execution_options)
- 若要求嚴格 no-network，SDKMAN healthcheck、wrapper bootstrap、build dependency resolution、Gradle toolchain provisioning 都必須分別控制。官方 primary sources沒有提供一個跨這四層的單一 flag，因此「一個 SDKMAN offline mode 保證全程零網路」標為 **unknown／不存在可證成的 contract**。

### Security

SDKMAN config 的 `sdkman_insecure_ssl=true` 會停用 SSL certificate verification；官方文件直接以「HERE BE DRAGONS」警告。Agent 不應啟用它，也不應為了繞過 TLS failure 修改 config。[SDKMAN Usage：Configuration](https://sdkman.io/usage/#configuration) [`sdkman-utils.sh`（2026-08-30 snapshot）](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-utils.sh)

SDKMAN Bash install source 的 checksum validation 是條件式 artifact integrity control：source ordering 顯示 remote post-install hook 在 checksum path 前已被 `source` 與執行，而 metadata、config 或工具條件也可能讓 checksum validation 略過。這不是官方聲明的完整 threat model；可以證成的只有執行順序與分支條件。因此不得推論 checksum 一定執行、同時驗證了 hook，或 SDKMAN install 是 untrusted-code-free；沒有本次執行證據時，實際 integrity status 為 **unknown**。[`sdkman-install.sh`（2026-08-30 snapshot）](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-install.sh)

SDKMAN 官方只替 latest release 提供 security updates，使用舊版不在支援範圍。查核時的 latest 5.23.0 移除了 checksum verification 中可被利用的 `eval`；官方 advisory 將其列為 critical command injection。因此 skill 應明示先以 `sdk version` 取得實際版本，版本落後時把更新視為另一個需要授權的 setup／mutation 決策，不得默默 self-update，也不得僅因 source HEAD 已修補就宣稱目前安裝安全。[SDKMAN Security Policy](https://github.com/sdkman/sdkman-cli/security) [SDKMAN 5.23.0 release](https://github.com/sdkman/sdkman-cli/releases/tag/5.23.0) [GHSA-jh7h-4x3r-f89r](https://github.com/sdkman/sdkman-cli/security/advisories/GHSA-jh7h-4x3r-f89r)

## 二、Wrapper 是 build-tool version contract，不是 JDK toolchain

### Maven Wrapper

Apache Maven Wrapper 讓 repository 透過 `mvnw`／`mvnw.cmd` 執行 `.mvn/wrapper/maven-wrapper.properties` 指定的 Maven；必要版本不存在時，wrapper 會先下載、安裝再使用。因此 project 有 wrapper 時，使用 wrapper 比 SDKMAN-managed `mvn` 更符合 project 的 build-tool contract。[Apache Maven Wrapper](https://maven.apache.org/tools/wrapper/)

Maven Wrapper 可配置 `wrapperSha256Sum` 與 `distributionSha256Sum`；這是 repository／wrapper configuration 的安全細節，不應由 SDKMAN skill 在每次 workload 靜默改寫。[Apache Maven Wrapper：checksum verification](https://maven.apache.org/tools/wrapper/#checksum-verification-of-downloaded-binaries)

### Gradle Wrapper

Gradle 官方明確推薦以 `./gradlew` 執行 build；wrapper 執行 project 宣告的 Gradle distribution，必要時先下載。[Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html)

Gradle Wrapper 支援 `distributionSha256Sum`，並另外要求注意 checked-in `gradle-wrapper.jar` 的 integrity；官方提供 checksum／PGP verification 與 CI action。這些是 repository governance／reference 細節，不是單次 SDKMAN switch 的責任。[Gradle Wrapper：distribution 與 JAR verification](https://docs.gradle.org/current/userguide/gradle_wrapper.html#sec:verification)

### Offline caveat

Maven `-o` 與 Gradle `--offline` 是 build tool 收到的選項；但兩個 wrapper 的官方流程都可能在 build tool 啟動前下載 distribution。因此，若 distribution 尚未在 wrapper cache，`./mvnw -o ...` 或 `./gradlew --offline ...` 不能從 primary sources 推導為「bootstrap 也不碰網路」。嚴格 no-network 要求下應先確認 wrapper distribution 已可用，否則把 failure 報在 wrapper bootstrap boundary。[Apache Maven Wrapper](https://maven.apache.org/tools/wrapper/) [Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html)

## 三、Maven JDK boundaries

### Maven launcher JVM 與 compiler target

Maven Compiler Plugin 官方範例顯示，JDK 11 可用 `--release 8` 編譯；`release` 同時約束語言規則、class target 與該 Java SE release 的 public API。支援的 release 是目前 JDK release 加有限數量舊 releases，因此不能把「新 JDK 可編舊 release」無限外推。[Maven Compiler Plugin：`--release`](https://maven.apache.org/plugins/maven-compiler-plugin/examples/set-compiler-release.html)

`source`／`target` 不保證使用指定 JDK，`target` 也不阻止誤用較新 JRE API；要讓 build plugins 使用不同於 Maven launcher 的 JDK，應使用 Toolchains。[Maven Compiler Plugin：`source`／`target`](https://maven.apache.org/plugins/maven-compiler-plugin/examples/set-compiler-source-and-target.html)

因此看到 `maven.compiler.release`、`source` 或 `target` 不是 shell JDK switch 的充分證據。Launcher JVM 要能啟動 wrapper 所選的 Maven；compile／test JDK 則可能由 toolchain 選擇。

### Maven Toolchains

Maven Toolchains 允許 project 指定與 Maven 本身執行 JDK 不同的 JDK，並將選到的 toolchain 放入 MavenSession，供 toolchain-aware plugins 使用。官方列出的 aware plugins 包含 Compiler、Surefire、Failsafe、Javadoc 等，但這不是「所有第三方 plugin 必然遵守」的保證。[Guide to Using Toolchains](https://maven.apache.org/guides/mini/guide-using-toolchains)

`toolchains:toolchain` 預設綁在 `validate`（第一個 lifecycle phase）；找不到 matching toolchain 時，原 Maven command 已開始，卻會在 requested compile／test 前失敗。這應報成 build setup／toolchain resolution failure，不是 agent environment initialization failure，也不是 test assertion failure。[Maven Toolchains Plugin：Usage](https://maven.apache.org/plugins/maven-toolchains-plugin/usage.html)

Toolchains Plugin 3.2.0 起可 heuristic discovery；2026-08-30 的 3.3.0 文件明示能發現 `~/.sdkman/candidates/java/...`，且 `select-jdk-toolchain` 可從 `toolchains.xml` 與 discovered JDKs 選擇。Agent 不需要先 `sdk use` 來讓 Maven discovery 看見 SDKMAN-installed JDK。[Maven JDK Toolchain discovery](https://maven.apache.org/plugins/maven-toolchains-plugin/toolchains/jdk-discovery.html)

## 四、Gradle Client JVM、Daemon JVM 與 task JVM

Gradle 9.7.1 官方把三個責任面分開：

| 層 | 官方來源 | SDKMAN shell switch 的影響 |
| --- | --- | --- |
| Client JVM | 啟動 `gradle`／`gradlew` 的 `JAVA_HOME`、`java` on `PATH` 或 IDE | 直接影響 Client launcher |
| Daemon JVM | `org.gradle.java.home`、Tooling API、Daemon JVM criteria；criteria 存在時高於 `JAVA_HOME` 與 `org.gradle.java.home` | 不保證覆寫；可能只影響沒有更高層 criteria 的 default |
| task JVM／tools | Project／task Java toolchain 的 `JavaCompiler`、`JavaLauncher`、`JavadocTool` | 不保證改變 compile、Test、JavaExec、Javadoc 使用的 JDK |

來源：[Gradle Client vs. Daemon](https://docs.gradle.org/current/userguide/gradle_daemon.html#sec:gradle_daemon) [Gradle Daemon JVM criteria](https://docs.gradle.org/current/userguide/gradle_daemon.html#daemon_jvm_criteria) [Gradle Toolchains for tasks](https://docs.gradle.org/current/userguide/toolchains.html#toolchains_for_tasks)

Gradle 會自動偵測 SDKMAN-installed JDK；找不到 matching local toolchain 且 project 已設定 download repository 時，可自動下載 JDK 到 Gradle User Home。下載後的 JDK 不會由 auto-provisioning 自動升級。[Gradle Toolchain auto-detection／provisioning](https://docs.gradle.org/current/userguide/toolchains.html#sec:auto_detection)

這表示：

- project 已宣告 Gradle toolchain 時，預設委派給 Gradle，不要從 target number 先改 shell JDK；
- Gradle auto-provision 是 project-configured native behavior，不是 `sdk install`；但它仍是 network＋persistent download。若原 workload 已獲授權且沒有 offline／no-download 限制，可讓原生工具執行；若使用者禁止下載，必須在 command 前明示這個邊界；
- `./gradlew --version` 能探測 wrapper／Client launcher 與 distribution，但不能證明 Daemon criteria 或特定 task toolchain 一定可解析；後兩者仍由原 workload 暴露；
- 2026-08-30 的 Gradle 9.7.1 runtime matrix 要求 Daemon／Gradle execution JVM 17–26，但 Client／Wrapper 可在 JVM 8；compile 與 test 又有不同支援範圍。這些版本數字只能放 reference，不應硬編成 skill 長期 policy。[Gradle Compatibility Matrix（9.7.1）](https://docs.gradle.org/current/userguide/compatibility.html)

## 五、Exit status 與 setup-vs-workload failure boundaries

### 必須保留的 status contract

推薦形式仍是單一 AND list：

```bash
type sdk >/dev/null 2>&1 || source "${SDKMAN_DIR:-$HOME/.sdkman}/bin/sdkman-init.sh"
sdk use java <exact-installed-id> && <original-command>
```

第一行的 `||` 與第二行的 `&&` 應被視為兩段 setup gate。若需要額外 cleanup／cwd restoration 放在 workload 後面，實作必須先保存 workload status，再 cleanup，最後回傳原 status。這是 skill 必須明示的 orchestration policy；host shell 的精確語義若沒有目前執行環境證據，則標 **unknown**。

不得在重跑時替原 command 加 Maven `--fail-never` 或 Gradle `--continue` 等會改變 failure semantics 的 flags；保留使用者原 command 才能保留其 status contract。[Maven CLI options](https://maven.apache.org/ref/current/maven-embedder/cli.html) [Gradle CLI execution options](https://docs.gradle.org/current/userguide/command_line_interface.html#sec:command_line_execution_options)

### 四層 failure taxonomy

| Boundary | 代表事件 | 正確報告 | 原 command／task 是否開始 |
| --- | --- | --- | --- |
| 1. Agent environment initialization | 找不到 init script、`.sdkmanrc` 不合法／candidate 未安裝、`sdk use`／`sdk env` 失敗、cwd restoration 失敗 | setup failure；原 workload command 未執行；回傳 setup status | command 未開始 |
| 2. Wrapper／Client bootstrap | wrapper script、distribution download／checksum、Maven launcher 或 Gradle Client JVM 無法啟動 | wrapper／launcher setup failure；保留 wrapper command status | 原 command 已呼叫；build engine 未必開始 |
| 3. Build runtime／toolchain resolution | Maven `validate` 找不到 toolchain、Gradle Daemon criteria／Daemon start／task toolchain resolution 失敗 | build setup／toolchain failure；不是 agent SDKMAN init failure | build engine 已開始；requested goal／task action可能未開始 |
| 4. Requested workload | compile、test、application task 等真正失敗 | workload failure；回報原 command status 與實際 failing layer | requested work 已開始 |

這個 taxonomy 是由各工具公開 lifecycle 導出的 agent reporting policy，不是 SDKMAN／Maven／Gradle 共同定義的官方名詞。若 output 無法證明 task action 是否開始，標 **unknown**，不要用猜測補齊。

## 六、哪些內容放在哪裡

### Skill 必須明示的 policy

以下項目會改變 agent 是否執行、是否下載、是否誤報失敗，應留在主 `SKILL.md`：

1. `sdk` 初始化、environment switch 與 workload 必須在同一 shell；只在確實需要 SDKMAN switch 時載入。
2. Exact user／`.sdkmanrc` id 是 contract；缺少時停止，不替換 vendor／patch，不自動 install／default。
3. `.sdkmanrc` 只在明確 workload boundary 內適用；呼叫 `sdk env` 前完整驗證所有 declarations 已安裝，避免 partial application。
4. Project wrapper 優先；wrapper 管 Maven／Gradle version，Maven／Gradle toolchain 管 compile／test JDK，shell JDK 只解決 Client／launcher 或未被 toolchain 隔離的 layer。
5. Maven launcher、Maven toolchain、Gradle Client、Daemon、task toolchain、application runtime 分層診斷；compiler target 不是 shell JDK request。
6. `sdk install`、`sdk env install`、`sdk default`、建立 `.sdkmanrc`、改 auto-env、改 insecure SSL 都是需明確授權的 persistent／security changes；永不啟用 `sdkman_insecure_ssl`。
7. SDKMAN network availability、Maven／Gradle offline 與 strict no-network 是不同 contract；wrapper bootstrap／Gradle provisioning 可能另有下載。
8. 保留原 command、cwd 與 exit status；按四層 boundary 報告，證據不足標 unknown。

### 可壓縮到 reference 的細節

下列內容重要但不應占用每次 invocation 的主 context：

- SDKMAN init 實際 source 哪些 scripts、auto-env 如何掛 Bash／zsh hooks、`.sdkmanrc` parser 正規化規則。
- `sdk use` 首次建立 `current` link、`sdk env install` 保留既有 default 的細節與例外。
- SDKMAN healthcheck、offline installed-list 行為、remote post-install hook 與 checksum ordering。
- Maven Wrapper／Gradle Wrapper 的 cache、download、checksum、PGP／JAR verification 操作方式。
- Maven toolchain-aware plugin 清單、3.3.0 discovery comparator 與 cache 細節。
- Gradle 版本 compatibility matrix、Daemon criteria 檔案格式、toolchain resolver／auto-provisioning 設定。
- 可攜的 candidate enumeration 與 direct-environment fallback 實作；這些應有 platform／SDKMAN-version caveat。

### 可委派給原生工具的行為

在 policy gates 已通過後，以下不應由 agent 重寫 resolver：

- 由 `sdk use` 驗證並套用 exact installed candidate；由 `sdk env` 套用已完整 prevalidated 的 `.sdkmanrc`。
- 由 repository 的 `mvnw`／`gradlew` 選擇與 bootstrap project-declared Maven／Gradle distribution；offline／no-download 限制存在時除外。
- 由 Maven Toolchains 依 project requirements、`toolchains.xml` 與 discovery 選 JDK；失敗就回報 matching requirements，不以任意 shell JDK 掩蓋。
- 由 Gradle Daemon criteria 選 build runtime JVM，由 project／task toolchains 選 compiler／test／exec JVM；允許 project-configured provisioning 只限於已授權且非 offline／no-download workload。
- 由原 workload command 的 process status 決定成功／失敗；agent 只保留並忠實分類，不把 output keyword 取代 status。

## 七、逐項對照現行 `skills/sdkman/SKILL.md`

### 分類定義

- **confirmed**：primary source 直接支持，或是由 source 行為直接導出的必要安全／reporting policy。
- **stale**：曾成立但已被 2026-08-30 的 current docs／source 取代。
- **missing**：Issue #25 要求且會改變決策，但現行 skill 沒明示。
- **over-specified**：寫成強制規則，但 primary sources 不提供該 portability／scope guarantee；可能是合理 repo policy，卻不應冒充原生工具語義。

### 現有內容矩陣

| ID | 現行內容 | 判定 | 依據與結論 |
| --- | --- | --- | --- |
| C01 | `sdk` 是 shell function；`sdk use` 只影響目前 shell | confirmed | 官方 Usage 與 `sdkman-main.sh` 支持；同 shell 執行是必要條件。[Usage](https://sdkman.io/usage/#use-version) [`sdkman-main.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-main.sh) |
| C02 | Agent shell tool calls 通常是 fresh shells | over-specified | SDKMAN／Maven／Gradle primary sources不規範 agent host shell persistence；應保留為 host assumption 或說「除非 host 明示 persistent shell」。 |
| C03 | 從 workload directory 向上找 nearest `.sdkmanrc`，到 Git worktree root 為止 | over-specified | SDKMAN 原生只讀目前目錄 `.sdkmanrc`，official docs 說 project base directory；沒有 Git worktree／nearest-parent 規格。[Env docs](https://sdkman.io/usage/#env-command) [`sdkman-env.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-env.sh) |
| C04 | 不跨 sibling checkout／worktree 取 `.sdkmanrc` | confirmed | 這是避免把非 workload project contract 套入目前 command 的必要 policy；但應明示為 agent isolation policy，不是 SDKMAN discovery behavior。 |
| C05 | `sdk env` 後回原 workload cwd | confirmed | `sdk env` 依目前目錄讀檔；workload cwd 是 command contract，需在執行前回復。[`sdkman-env.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-env.sh) |
| C06 | Exact requested SDKMAN id 用 `sdk use` | confirmed | `sdk use candidate version` 是官方 exact form，且只接受 installed version。[Usage](https://sdkman.io/usage/#use-version) |
| C07 | Non-exact constraint 的 active／default／sole-installed evidence order | over-specified | 官方沒有此排序 contract；Maven／Gradle toolchains另有自己的 resolver。可保留為 agent decision policy，但需標 inference，不能稱 SDKMAN best practice。 |
| C08 | `.sdkmanrc` declarations 交給 `sdk env` | confirmed | 官方 contract；但必須補完整 prevalidation，見 M01。[Env docs](https://sdkman.io/usage/#env-command) |
| C09 | 無 `.sdkmanrc` 時優先 wrapper／toolchains | confirmed | Maven／Gradle wrapper 與 toolchain docs 支持 project-native contracts。[Maven Wrapper](https://maven.apache.org/tools/wrapper/) [Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html) |
| C10 | Wrapper launcher 不相容時才選 shell JDK | confirmed | Compiler／task toolchain可與 launcher分離；shell JDK 應針對實際 launcher layer。[Maven Toolchains](https://maven.apache.org/guides/mini/guide-using-toolchains) [Gradle Daemon](https://docs.gradle.org/current/userguide/gradle_daemon.html) |
| C11 | Absence of `.sdkmanrc` 不是 `sdk env` failure | confirmed | `sdk env` 只在 file 存在時才是適用 path；沒有 file 應選其他 path。[`sdkman-env.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-env.sh) |
| C12 | Exact id／vendor 不可靜默替換 | confirmed | 這是 reproducibility 與 authorization policy；Gradle／Maven也把 vendor／version當 matching criteria。[Maven discovery](https://maven.apache.org/plugins/maven-toolchains-plugin/toolchains/jdk-discovery.html) [Gradle Toolchains](https://docs.gradle.org/current/userguide/toolchains.html) |
| C13 | 只列 alternatives，不藉此繞過 exact contract | confirmed | 安全 policy；沒有 primary source要求 agent替換使用者指定 id。 |
| C14 | Major-only constraint 無 installed match 時要求 exact vendor／id | confirmed | SDKMAN remote list提供多 vendor versions；primary sources沒有唯一合法 vendor resolver，故不得猜測。[SDKMAN Usage：List Versions](https://sdkman.io/usage/#list-versions) |
| C15 | `.java-version` 是 intent，但尊重 owning version manager | over-specified | 本研究允許的 primary sources未定義 `.java-version` ownership；合理但無 SDKMAN／Maven／Gradle primary support。 |
| C16 | Maven `release`／`source`／`target` 與 Gradle `options.release`／compatibility 不等於 shell-JDK request | confirmed | 兩套官方 docs 都分開 target 與 JDK selection。[Maven Compiler](https://maven.apache.org/plugins/maven-compiler-plugin/examples/set-compiler-release.html) [Gradle Toolchains comparison](https://docs.gradle.org/current/userguide/toolchains.html#sec:compilation) |
| C17 | Maven／Gradle configured toolchain 優先自行選 JDK | confirmed | 官方原生能力；Maven只保證 toolchain-aware plugins，這個 caveat 應補到 reference。[Maven Toolchains](https://maven.apache.org/guides/mini/guide-using-toolchains) [Gradle Toolchains](https://docs.gradle.org/current/userguide/toolchains.html) |
| C18 | `./mvnw -version`／`./gradlew --version` 作 launcher probe | confirmed | 能分離 wrapper／launcher setup 與 requested goal／task；但 wrapper可能先下載 distribution，且 Gradle probe不驗證 Daemon／task toolchain，需補 caveat。[Maven Wrapper](https://maven.apache.org/tools/wrapper/) [Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html) |
| C19 | Gradle Client／Daemon／task toolchain 分開 | confirmed | 9.7.1 官方明確分層。[Gradle Daemon](https://docs.gradle.org/current/userguide/gradle_daemon.html#sec:gradle_daemon) [Gradle task toolchains](https://docs.gradle.org/current/userguide/toolchains.html#toolchains_for_tasks) |
| C20 | 直接檢查 init script 與 candidate directory | over-specified | init path受官方 install支持；但 `ls candidates/...` 是內部 layout依賴。官方另提供 `sdk home` 給 scripts，應把 manual layout 降到 fallback reference。[SDKMAN Installation](https://sdkman.io/install/) [SDKMAN Usage：Home](https://sdkman.io/usage/#home) |
| C21 | Source SDKMAN、`sdk use`、workload 同 invocation | confirmed | 官方 current-shell contract支持；status-preserving composition 是 agent policy。[SDKMAN Usage](https://sdkman.io/usage/#use-version) [`sdkman-main.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-main.sh) |
| C22 | `sdk use` 可能在缺少 `current` 時建立 link | confirmed | 現行 source直接支持。[`sdkman-use.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-use.sh) |
| C23 | 為保留 link absence 而用 direct-environment fallback | over-specified | 是 source-layout-dependent workaround，非官方 SDKMAN workflow；應移至 reference並標 version/platform caveat。 |
| C24 | `.sdkmanrc` snippet 只 `test -f` 後直接 `sdk env` | missing | 不是錯誤陳述，但缺少全 candidate prevalidation；現行 source可能 partial apply。[`sdkman-env.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-env.sh) |
| C25 | Missing `.sdkmanrc` candidate 時停止並詢問 install | confirmed | `sdk env` 原生會失敗並提示 `sdk env install`；agent不應自行下載。[Env docs](https://sdkman.io/usage/#env-command) |
| C26 | `sdk default` 只在明確 persistent request；install／env install 要授權 | confirmed | public semantics與 source mutation支持。[SDKMAN Usage](https://sdkman.io/usage/) [`sdkman-install.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-install.sh) |
| C27 | Leave auto-env unchanged | confirmed | auto-env改 shell hooks並在 `cd` 時切換；單次 workload沒有理由改全域 config。[SDKMAN Usage](https://sdkman.io/usage/#env-command) [`sdkman-init.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-init.sh) |
| C28 | 建立／copy／commit `.sdkmanrc` 需明確要求 | confirmed | `sdk env init` 會寫 project file；屬 persistent project contract。[SDKMAN Usage](https://sdkman.io/usage/#env-command) |
| C29 | `sdk list` 只在需要 remote options 時使用 | confirmed | Online list提供 remote options；offline則只列 installed。若只需已安裝清單，可避免無意義 network path。[SDKMAN Usage](https://sdkman.io/usage/#list-versions) [`sdkman-list.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-list.sh) |
| C30 | Direct fallback 手動設 `JAVA_HOME`／`MAVEN_HOME`／`GRADLE_HOME`／`KOTLIN_HOME` 與 `PATH` | over-specified | SDKMAN source動態設 `*_HOME`，但直接組內部 path 不是 public contract；官方 scripts用途優先有 `sdk home`。[`sdkman-path-helpers.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-path-helpers.sh) [SDKMAN Home](https://sdkman.io/usage/#home) |
| C31 | Setup 成功後才啟動 workload；保留 command、cwd、status | confirmed | SDKMAN command會回傳 dispatch status；其餘是必要 orchestration contract，host-shell細節無證據時標 unknown。[`sdkman-main.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-main.sh) |
| C32 | `sdk env`／`sdk use` failure 報 environment initialization，workload未開始 | confirmed | 這是明示 gate 所要求的 agent policy；需補 wrapper／build setup層，見 M06。[`sdkman-env.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-env.sh) [`sdkman-use.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-use.sh) |
| C33 | Workload 執行後失敗就報其 status，不重標 setup failure | confirmed | 正確；但要依 requested task 是否真正開始細分，證據不足標 unknown。 |
| C34 | 保留 defaults、installed candidates、project files、auto-env | confirmed | 對應各操作的持久 mutation；只有使用者授權才能改。[SDKMAN Usage](https://sdkman.io/usage/) |

### 缺漏矩陣

| ID | 缺漏內容 | 判定 | 為何會改變 agent 決策 |
| --- | --- | --- | --- |
| M01 | `sdk env` 逐項套用、失敗不 rollback；需完整 prevalidation | missing | 否則 setup failure 後 shell可能已部分切換。[`sdkman-env.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-env.sh) |
| M02 | SDKMAN Network Availability 與 strict no-network 的差異 | missing | 關閉 healthcheck不是 offline sandbox；會誤宣稱無 network attempt。[SDKMAN Usage](https://sdkman.io/usage/#network-availability) |
| M03 | Maven `-o`、Gradle `--offline` 與 wrapper bootstrap caveat | missing | Build offline flag不證明 wrapper distribution不下載。[Maven CLI](https://maven.apache.org/ref/current/maven-embedder/cli.html) [Gradle offline](https://docs.gradle.org/current/userguide/dependency_caching.html#sec:offline-mode) |
| M04 | SDKMAN TLS／remote post-install hook／條件式 checksum validation | missing | Install 是 network＋code execution boundary；不能只描述成持久下載，也不能在未觀察 validation branch 時宣稱 integrity verified。[SDKMAN config](https://sdkman.io/usage/#configuration) [`sdkman-install.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-install.sh) |
| M05 | Maven／Gradle Wrapper distribution與 integrity controls | missing | Wrapper優先是對的，但它可能下載／執行 binary；security細節應有 reference。[Maven Wrapper](https://maven.apache.org/tools/wrapper/) [Gradle Wrapper verification](https://docs.gradle.org/current/userguide/gradle_wrapper.html#sec:verification) |
| M06 | 四層 setup-vs-workload taxonomy | missing | 現行二分法無法準確描述 wrapper、Maven validate、Gradle Daemon／task toolchain failures。 |
| M07 | Maven Toolchains 只保證 toolchain-aware plugins | missing | 不能說 project有 toolchain就所有 plugin都與 launcher JDK無關。[Maven Toolchains](https://maven.apache.org/guides/mini/guide-using-toolchains) |
| M08 | Maven 3.3.0 discovery可直接看見 SDKMAN JDK | missing | 可減少不必要 shell switch；原生 resolver應優先。[Maven JDK discovery](https://maven.apache.org/plugins/maven-toolchains-plugin/toolchains/jdk-discovery.html) |
| M09 | Gradle auto-provisioning 是另一路 persistent download | missing | 「let build select toolchains」可能觸發下載；offline／no-download 時必須先說明。[Gradle Toolchains](https://docs.gradle.org/current/userguide/toolchains.html#sec:provisioning) |
| M10 | `./gradlew --version` 不驗證 Daemon criteria／task toolchain | missing | Probe成功不能宣稱整個 Gradle workload environment ready。[Gradle Daemon](https://docs.gradle.org/current/userguide/gradle_daemon.html) [Gradle task toolchains](https://docs.gradle.org/current/userguide/toolchains.html#toolchains_for_tasks) |
| M11 | `sdk env install` 在 candidate 無既有 `current` 時仍可能建立 default link | missing | 即使 source嘗試保留 existing default，也不是所有情況零 default mutation。[`sdkman-env.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-env.sh) [`sdkman-use.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-use.sh) |
| M12 | SDKMAN 只支援 latest release；實際安裝版本需先辨識 | missing | 5.23.0 修補 critical checksum command injection；source HEAD 或文件新穎度不能證明目前安裝已修補。更新本身另需授權。[Security Policy](https://github.com/sdkman/sdkman-cli/security) [5.23.0 release](https://github.com/sdkman/sdkman-cli/releases/tag/5.23.0) [GHSA-jh7h-4x3r-f89r](https://github.com/sdkman/sdkman-cli/security/advisories/GHSA-jh7h-4x3r-f89r) |

### Stale 結果

截至 2026-08-30，沒有找到現行 skill 中可直接判定為 **stale** 的 public behavior。值得注意但不構成 stale 的變化是：SDKMAN 已有 native components，Bash `default` implementation 會顯示 legacy deprecation notice，但官方 Usage 仍把 `sdk default` 列為現行 public command；因此 skill 的「只有明確要求才用 default」仍成立，不應因內部 dispatch 改寫而判 stale。[`sdkman-default.sh`（2026-08-30 snapshot）](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-default.sh) [SDKMAN Usage：Default](https://sdkman.io/usage/#default-version)

## 八、Unknowns 與不可過度推論處

1. **Strict no-network 的跨工具保證：unknown。** SDKMAN、wrapper、Maven／Gradle dependency resolution、Gradle provisioning 各有不同控制面；沒有單一官方 flag 可證明整條 execution chain 零 network attempt。
2. **Agent shell 是否每次 fresh：unknown（在允許來源範圍內）。** 這是 host runtime contract，不是 SDKMAN／Maven／Gradle contract；主 skill 應以「若 shell state 不保證持久」條件式描述。
3. **向上搜尋 nearest `.sdkmanrc` 至 Git worktree root：unknown／agent-specific。** SDKMAN primary sources只證明 current directory behavior。若 repository要保留此 isolation policy，需明示它是本 skill 的 workload-resolution規則。
4. **`sdk env` atomicity：不可假設。** Source可證明逐項 mutation與無 rollback；官方文件沒有 atomic guarantee。
5. **SDKMAN install 的實際 integrity status 與完整 threat model：unknown。** Source可證明 remote hook、archive與條件式 checksum path的順序，但不能推論某次 install一定執行 checksum，也不能推論 hook已被同一 checksum驗證。
6. **Probe成功是否代表 workload ready：unknown。** `mvnw -version`／`gradlew --version` 只證明 probe實際經過的層；未經過的 Maven plugin、Gradle Daemon criteria、task toolchain與 application runtime仍未驗證。

## Primary sources 索引

### SDKMAN

- [Installation](https://sdkman.io/install/)
- [Usage](https://sdkman.io/usage/)
- [Security Policy](https://github.com/sdkman/sdkman-cli/security)
- [5.23.0 security release](https://github.com/sdkman/sdkman-cli/releases/tag/5.23.0)
- [GHSA-jh7h-4x3r-f89r](https://github.com/sdkman/sdkman-cli/security/advisories/GHSA-jh7h-4x3r-f89r)
- [`sdkman-cli` immutable snapshot `1ceb412f`](https://github.com/sdkman/sdkman-cli/tree/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8)
- [`sdkman-main.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-main.sh)
- [`sdkman-init.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-init.sh)
- [`sdkman-use.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-use.sh)
- [`sdkman-env.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-env.sh)
- [`sdkman-install.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-install.sh)
- [`sdkman-availability.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-availability.sh)
- [`sdkman-utils.sh`](https://github.com/sdkman/sdkman-cli/blob/1ceb412f5ef98a4ff7c166cf4276243e8d86c1f8/src/main/bash/sdkman-utils.sh)

### Maven

- [Maven Wrapper](https://maven.apache.org/tools/wrapper/)
- [Maven 3.9.16 CLI options](https://maven.apache.org/ref/3.9.16/maven-embedder/cli.html)
- [Guide to Using Toolchains](https://maven.apache.org/guides/mini/guide-using-toolchains)
- [Maven Toolchains Plugin usage](https://maven.apache.org/plugins/maven-toolchains-plugin/usage.html)
- [JDK Toolchain discovery](https://maven.apache.org/plugins/maven-toolchains-plugin/toolchains/jdk-discovery.html)
- [Compiler Plugin `--release`](https://maven.apache.org/plugins/maven-compiler-plugin/examples/set-compiler-release.html)
- [Compiler Plugin `source`／`target`](https://maven.apache.org/plugins/maven-compiler-plugin/examples/set-compiler-source-and-target.html)

### Gradle

- [Gradle Wrapper（9.7.1）](https://docs.gradle.org/current/userguide/gradle_wrapper.html)
- [Gradle Daemon（9.7.1）](https://docs.gradle.org/current/userguide/gradle_daemon.html)
- [JVM Toolchains（9.7.1）](https://docs.gradle.org/current/userguide/toolchains.html)
- [Compatibility Matrix（9.7.1）](https://docs.gradle.org/current/userguide/compatibility.html)
- [Build Environment（9.7.1）](https://docs.gradle.org/current/userguide/build_environment.html)
- [Dependency Caching／Offline（9.7.1）](https://docs.gradle.org/current/userguide/dependency_caching.html#sec:offline-mode)
- [Command-Line Interface（9.7.1）](https://docs.gradle.org/current/userguide/command_line_interface.html)
