# Validation contract

Invalid requests must be rejected before a success acknowledgment is returned.

The synchronous path validates before responding. The proposed queue path acknowledges a successful enqueue, then validates in a worker; it has no synchronous validation before acknowledgment.

No production measurement currently demonstrates that the synchronous path misses the throughput target.
