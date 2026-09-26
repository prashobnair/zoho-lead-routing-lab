import json
import unittest
from pathlib import Path
from routing import normalize_phone, route_leads

EXAMPLE = json.loads(Path(__file__).with_name('examples.json').read_text())['leads']

class RoutingTests(unittest.TestCase):
    def test_example(self):
        report = route_leads(EXAMPLE)
        self.assertEqual({'qualified':1,'review':3,'duplicate':1}, report['counts'])
        self.assertEqual('lead-1', report['decisions'][1]['duplicate_of'])
        self.assertEqual(0, report['outbound_messages'])

    def test_e164_no_region_guess(self):
        self.assertEqual('+919000000001', normalize_phone('+91 (900) 000-0001'))
        for value in ('9000000001', '00449000000001', '+0123456789', 'hi', None):
            self.assertIsNone(normalize_phone(value))

    def test_consent_blocks_auto_qualification(self):
        lead = dict(EXAMPLE[0], id='new', phone='+919999999999', consent=False)
        result = route_leads([lead])['decisions'][0]
        self.assertEqual('review', result['status'])
        self.assertEqual('consent_not_verified', result['reason'])

    def test_invalid_and_unsupported_to_human(self):
        x = dict(EXAMPLE[0], id='invalid', phone='123')
        y = dict(EXAMPLE[0], id='unsupported', channel='email', phone='+919888888888')
        result = route_leads([x, y])['decisions']
        self.assertTrue(all(d['route'] == 'human_queue' for d in result))

    def test_repeated_id_fails_closed(self):
        with self.assertRaises(ValueError):
            route_leads([EXAMPLE[0], EXAMPLE[0]])

    def test_same_payload_is_deterministic(self):
        self.assertEqual(route_leads(EXAMPLE), route_leads(EXAMPLE))

if __name__ == '__main__':
    unittest.main()
