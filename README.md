# Zoho Lead Routing Lab

A local, **simulation-only** lead intake pipeline. It accepts fictional Forms, WhatsApp and Instagram events, normalizes explicitly international phone numbers, flags duplicate candidates, qualifies a narrow sales case and queues uncertain records for a human. There are no real messages, chatbots, webhooks, Bigin writes or Zoho credentials.

## Why this project

The [Zoho CRM contract board](https://www.upwork.com/freelance-jobs/zoho-crm/) samples WhatsApp/CRM integration work. A more detailed [Bigin/uChat/Pabbly/Meta brief](https://www.upwork.com/freelance-jobs/apply/Automation-ChatBot-Expert-Zoho-Bigin-uChat-Pabbly-Connect-Meta-api_~022094648010652558581/) asks for multichannel lead qualification, E.164 deduplication, qualified/unqualified routing and human handover. This repo tests that decision logic offline; it does not imply a live implementation of those platforms or a client engagement.

## Run it

Python 3.10+ and standard library only. From the repository root:

```sh
python3 cli.py examples.json
python3 -m unittest discover -p 'test_*.py' -v
```

No trial account, API key, Docker, webhook endpoint or paid service is needed. The sample is fictional. The five events yield one qualified sales lead, one duplicate candidate and three human-review cases (invalid phone, unverified consent and support inquiry). Output explicitly reports `outbound_messages: 0`.

## Input contract and decisions

`examples.json` contains `leads`, each with unique `id`, `channel` (`forms`, `whatsapp`, `instagram`), explicit international `phone`, `consent`, `intent` and `budget_confirmed`. The phone parser accepts punctuation around an E.164 number but never guesses a country code. It does not prove that the phone belongs to the same person: a match is only a duplicate *candidate*. An unsupported channel, invalid phone, no consent, support/unknown intent or unconfirmed budget goes to `human_queue`. Only an explicitly consented sales inquiry with confirmed budget reaches `sales_queue`. The status is a demo policy, not a CRM or legal consent rule.

The result is a decision ledger, not an action queue being executed. No automated reply is sent even for a qualified lead. See `DESIGN.md` for the event boundary, test matrix and operational handoff.

## Real integration boundary

A real implementation would need reviewed consent and retention rules, tenant-specific Bigin/CRM module metadata, documented API/webhook payloads, verified Meta channel permissions, signature checks, idempotency keys and retry/dead-letter behavior, rate limits, protected credentials, and an actual staffed human queue with service ownership. This repository deliberately invents a simple intermediate event schema rather than asserting vendor payload fidelity. Do not add client leads or real phone numbers to fixtures.
