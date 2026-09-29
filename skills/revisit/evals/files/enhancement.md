# Synthetic observations: audit issue #28

- User prompt: `$revisit https://example.invalid/audit/issues/28`
- A compliance operator currently exports one month's audit rows at a time, then manually combines the files to prepare a quarterly report. The existing monthly export behaves as specified.
- The ticket requests one export spanning a user-selected date range. A comment asks for the same filters as monthly export. Another suggests background processing if large ranges exceed the request timeout; no async requirement or performance failure has been established.
- Recorded current version: audit 5.1.0, commit `monthly-export-current` (synthetic fixture revision).
- A recorded API inspection and request check confirm the endpoint still accepts one month only. It applies the existing filters. No measurements of a multi-month export exist.
- Supporting multiple months is still a missing capability. Range limits and background processing remain proposals to discuss, not approved requirements. No implementation is authorized.
