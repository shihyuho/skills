# Event handler

`handle_event(event_id, processed_ids, effects)` handles sequential event deliveries in one process. Callers retain the same set and list across calls.

The handler records processed event IDs and ignores duplicate deliveries so that each ID produces at most one effect in `effects`.
