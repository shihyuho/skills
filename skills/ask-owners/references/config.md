# Content skill preference

Read this for `--save`, or when Python cannot run. The helper's `--help` owns its arguments.

## Save after loading

Derive a persistable selector from the source already loaded: prefer its runtime-qualified name, otherwise a unique canonical name, otherwise the exact user-supplied path that selected it. Resolve uncertainty before saving; a different installed skill is not an equivalent selector.

Explain that remembering the choice permits this content skill to conduct future discussions and its necessary content checks when the user explicitly invokes `ask-owners`. It does not authorize unrelated writes or additional explicit-only workflows. The user's `--save` or explicit request to remember this selected skill supplies that consent; reuse it without another confirmation. Record it only after the source and required references load successfully.

Run `scripts/config.py` with the same root and `save --selector <exact-selector>`, passing the selector as one literal argument. Report the returned `previous` and `current`. A successful save takes effect immediately, even if the subsequent discussion is blocked. A failed save leaves the previous file intact and the requested operation unresolved.

## Storage and native fallback

Use `<config-root>/ask-owners/config.json`, defaulting to the current user's `~/.config/softleader/agent-skills` root. Only effective user-level instructions can select another root; an unusable explicit root is an error, not a reason to fall back.

The owned member is:

```json
{"contentSkill":{"selector":"skills:grill-minimal","consent":"discussion-v1"}}
```

`discussion-v1` records the explicit choice and the bounded future discussion delegation described above. A bare selector or another consent version needs clarification, not an automatic upgrade. Owner assignments are separate discussion data.

When Python is unavailable, preserve the helper's contract with host-native file operations:

- Read UTF-8 JSON as an object. A missing file or member means no default; when present, `contentSkill` must be an object with a non-blank string `selector` and exactly the supported `consent`. Reject malformed data, duplicate keys, non-JSON numbers and unsupported preference data before a write.
- `read` creates nothing. `clear` removes only `contentSkill`; an absent file/member is an idempotent no-op. `save` updates its selector and consent only after exact loading and user-authorized persistence. Preserve unrelated members and numeric values.
- Re-read and validate before an update. Write a complete sibling temporary file, then atomically replace the destination; preserve existing permissions and symlink relationships. On failure, retain the old file and remove only the temporary file created by this operation. If the host cannot perform a safe update, report that limitation.
- Return `operation`, `path`, `previous`, `current` and `changed`; the two choice fields contain selectors or null. Report no unrelated configuration values. Use the same notices and ordering as the Python path.
