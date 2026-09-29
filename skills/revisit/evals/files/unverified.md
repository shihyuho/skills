# Synthetic observations: invoicing issue #19

- User prompt: `$revisit https://example.invalid/invoicing/issues/19`
- Available title: "Duplicate invoice after a timeout and retry".
- Body: "See incident log for request sequence." The referenced log is no longer available. There are no comments, linked fixes, or recorded decisions.
- Recorded current version: invoicing 3.4.0, commit `invoice-retry-check` (synthetic fixture revision).
- The available test sends two requests with different request IDs and produces two invoices. There is no captured original request ID, timeout location, retry payload, or reproduction of the reported duplicate.
- Source inspection shows a request-ID lookup, but the lifetime and reuse of the incident's IDs cannot be established from this fixture.
- No repair has been verified. No new implementation is authorized.
