# ask-owners

Run a discussion with the people responsible for each decision, using their agreed communication channels.

Choose the discussion style with a content skill; `ask-owners` routes its questions, collects answers and keeps the discussion moving. For example, architecture questions can stay in your conversation while business questions go to an owner in a Slack thread. The selected skill keeps its native behavior, including documents produced by `grill-with-docs`.

```text
$ask-owners grill-minimal — architecture questions come to me; ask Willy about business rules in <Slack thread>.
$ask-owners grill-with-docs --save
$ask-owners
$ask-owners --clear
```

A one-run selection leaves the default unchanged. `--save` remembers the chosen content skill for future explicit invocations across repositories; `--clear` forgets it. Clear natural-language requests work too. With no choice or saved default, the agent recommends available skills and asks you to choose.

Owner assignments apply to the current discussion unless you explicitly request otherwise. Pending external replies are checked every 30 seconds while independent questions continue; you can specify a different interval or deadline. You coordinate conflicting answers and confirm the final design.

Requires the selected content skill to be installed and the agreed channels to be accessible. The skill reports unavailable channels and pending questions so the discussion can resume without duplicate messages.
