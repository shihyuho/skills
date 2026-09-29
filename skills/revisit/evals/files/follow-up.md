# Synthetic continuation of the #750 discussion

## Established conversation

Assistant: 手動下載與正式交付共用檔名序號。例如正式交付上次用到 005，手動下載會消耗 006，下一次交付就用 007。這是示意例子；已驗證目前下載會推進序號。原票希望只看下一號、不保留它，但仍要決定哪些下載算正式交付。

User: 同意一般下載不佔號，直接繼續討論備份輸出。

## New user message

勾選「同時觸發備份輸出」時，為什麼你建議保留正式配號？

## Available observations

- The option writes a copy to the configured output destination as well as returning the download.
- Preview allocation does not reserve a number; another output may use that number before the copy is delivered.
- Normal-download semantics have been agreed. The user has not decided backup-output semantics and has not authorized implementation.
- The explanation and current-version investigation from the initial discussion are already established; there is no new contradictory evidence.
