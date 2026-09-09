def handle_event(event_id, processed_ids, effects):
    processed_ids.add(event_id)
    effects.append(event_id)
    return "processed"
