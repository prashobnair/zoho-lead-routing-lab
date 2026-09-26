# Event and operator design

## Event boundary

Each input is a fictional normalized event, not a Meta, uChat, Pabbly, Zoho Bigin or Zoho CRM webhook. Channels are labels only. The simulator processes list order, uses the first *valid* phone as a duplicate reference, and does not merge records. `phone_candidate_match` is deliberately weaker than identity confirmation. Unsupported fields are not forwarded or disclosed. The sample international numbers are fictional and must never be used to contact anyone.

## Routing matrix

| Condition | Status | Destination | Operator action |
| --- | --- | --- | --- |
| Unsupported channel or invalid E.164 | review | human_queue | Verify source and number |
| Same normalized phone as earlier lead | duplicate | none | Compare identities; choose merge/keep only after review |
| Consent not explicitly true | review | human_queue | Verify scope and lawful contact basis |
| Sales + consent + confirmed budget | qualified | sales_queue | Human follow-up; no message automatically sent |
| Support/unknown intent or sales without budget | review | human_queue | Triage and collect missing details |

The first valid phone is reserved even if it later requires review. That prevents a later same-phone event from bypassing review by pretending it is fresh. In production, duplicate policy needs a durable, tenant-scoped store, concurrency safety and audited human decisions.

## Acceptance and limits

Six unit tests cover expected routes/counts, E.164 normalization without region guessing, consent, fail-closed handoff, duplicate IDs and deterministic replay. Before a live integration, add authentic payload contract tests, signature verification, replay protection, retry isolation, sensitive-data redaction, race conditions, queue acknowledgments and operator SLA tests. No actual workflow, service, dashboard or API adapter is shipped here. This is a portfolio engineering slice, not a production integration.
