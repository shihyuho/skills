# Content skill default

Read this for `--save` or `--clear`. When a request both saves and clears, settle which one the user means before running either.

`scripts/config.py --help` owns the command interface. The default file is `~/.config/shihyuho/skills/ask-owners/config.json`; pass `--config-root` only when the user's own instructions select another root, and report an unusable root as an error. `clear` removes and `save` replaces only the `contentSkill` member; the rest of the file stays as it is.

## Clear

Run `clear` and report the result, including a no-op. Then choose the content skill for this run as `SKILL.md` describes.

## Save

`--save` needs a choice made in this invocation: an explicit selector, or the user's answer to your recommendation, even when a default already exists. Save only after the chosen skill and its required references have loaded.

Saving records consent, so tell the user what it permits: this content skill may run future discussions, with its necessary content checks, whenever they explicitly invoke `ask-owners`. It grants no publication, Git operations, implementation or other explicit-only workflows. The user's `--save`, or their explicit request to remember the skill, is that consent; record it without asking again.

Save the most exact selector for the loaded source: its runtime-qualified name, else a unique canonical name, else the exact path the user gave. Run `save --selector <selector>`, passing the selector as one argument, and report `previous` and `current`. A successful save holds even if the discussion is later blocked; a failed save leaves the previous file intact and the request unresolved.

## Stored format

```json
{"contentSkill":{"selector":"skills:grill-minimal","consent":"discussion-v1"}}
```

`discussion-v1` marks the consent above. The helper rejects a bare selector or another consent version; clarify with the user rather than upgrading it.
