"""Deterministic, offline lead router. Never sends a message or updates a CRM."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any
import re

E164 = re.compile(r'^\+[1-9]\d{7,14}$')
CHANNELS = {'whatsapp', 'instagram', 'forms'}

@dataclass(frozen=True)
class Decision:
    lead_id: str
    status: str
    route: str | None
    reason: str
    phone: str | None
    duplicate_of: str | None = None


def normalize_phone(raw: Any) -> str | None:
    """Require an explicit + country code; never infer geography from a local number."""
    if not isinstance(raw, str):
        return None
    value = re.sub(r'[\s().-]', '', raw)
    return value if E164.fullmatch(value) else None


def route_leads(leads: list[dict]) -> dict:
    if not isinstance(leads, list):
        raise ValueError('leads must be a list')
    seen_ids: set[str] = set()
    seen_phones: dict[str, str] = {}
    decisions: list[Decision] = []
    for item in leads:
        if not isinstance(item, dict):
            raise ValueError('Each lead must be an object')
        lead_id = str(item.get('id', '')).strip()
        if not lead_id or lead_id in seen_ids:
            raise ValueError('Lead IDs must be unique and nonempty')
        seen_ids.add(lead_id)
        channel = item.get('channel')
        phone = normalize_phone(item.get('phone'))
        if channel not in CHANNELS:
            decisions.append(Decision(lead_id, 'review', 'human_queue', 'unsupported_channel', phone))
        elif not phone:
            decisions.append(Decision(lead_id, 'review', 'human_queue', 'invalid_or_missing_e164', None))
        elif phone in seen_phones:
            decisions.append(Decision(lead_id, 'duplicate', None, 'phone_candidate_match', phone, seen_phones[phone]))
        else:
            # Reserve the valid phone even when later qualification needs review.
            seen_phones[phone] = lead_id
            if item.get('consent') is not True:
                decisions.append(Decision(lead_id, 'review', 'human_queue', 'consent_not_verified', phone))
            elif item.get('intent') == 'sales' and item.get('budget_confirmed') is True:
                decisions.append(Decision(lead_id, 'qualified', 'sales_queue', 'qualified_sales_inquiry', phone))
            elif item.get('intent') in {'support', 'unknown'}:
                decisions.append(Decision(lead_id, 'review', 'human_queue', 'needs_human_triage', phone))
            elif item.get('intent') == 'sales':
                decisions.append(Decision(lead_id, 'review', 'human_queue', 'budget_unconfirmed', phone))
            else:
                decisions.append(Decision(lead_id, 'review', 'human_queue', 'unrecognized_intent', phone))
    return {
        'mode': 'simulation_only',
        'decisions': [asdict(d) for d in decisions],
        'counts': {name: sum(d.status == name for d in decisions) for name in ('qualified', 'review', 'duplicate')},
        'outbound_messages': 0,
    }
