import json
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timezone, timedelta
from treasury import Treasury, TreasuryError, Intent

NOW = datetime(2026, 11, 20, 9, 0, tzinfo=timezone.utc)
RECIPIENT = '7T58drBUbkDHgEaVNQDgzFZEPZyFNHPfzzN2yBScLMBc'
OTHER = '7T58drBUbkDHgEaVNQDgzFZEPZyFNHPfzzN2yBScLMBd'

class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.db = str(Path(self.temp.name)/'ledger.sqlite3')
        self.policy = {
           'execution_enabled': False,
           'assets': {'SOL': {'decimals': 9, 'max_transfer_units': '0.1', 'daily_units': '0.2', 'recipients': [RECIPIENT]}},
        }
        self.treasury = Treasury(self.db, self.policy)

    def intent(self, request_id='req-01', amount='0.05', dest=RECIPIENT, asset='SOL', type_='transfer', valid=True):
        return Intent(request_id=request_id, action=type_, asset=asset, amount_units=amount,
                      recipient=dest, expires_at=(NOW + (timedelta(minutes=5) if valid else -timedelta(minutes=5))).isoformat())

    def test_default_deny_cannot_reserve(self):
        with self.assertRaises(TreasuryError): self.treasury.reserve(self.intent(), now=NOW)

    def test_enabled_whitelisted_transfer_reserved_not_sent(self):
        self.policy['execution_enabled'] = True
        receipt = self.treasury.reserve(self.intent(), now=NOW)
        self.assertEqual(receipt['status'], 'reserved_not_sent')
        self.assertEqual(receipt['amount_minor'], 50_000_000)
        self.assertNotIn('txid', receipt)

    def test_deny_unknown_recipient_and_token(self):
        self.policy['execution_enabled'] = True
        with self.assertRaises(TreasuryError): self.treasury.reserve(self.intent(dest=OTHER), now=NOW)
        with self.assertRaises(TreasuryError): self.treasury.reserve(self.intent(asset='USDC'), now=NOW)

    def test_deny_mint_trade_malformed_and_overlimit(self):
        self.policy['execution_enabled'] = True
        for test in (self.intent(type_='mint'), self.intent(type_='swap'), self.intent(amount='0.5'),
                     self.intent(amount='-1'), self.intent(amount='NaN'), self.intent(amount='0.0000000001')):
            with self.subTest(test=test), self.assertRaises(TreasuryError): self.treasury.reserve(test, now=NOW)

    def test_daily_budget_counts_all_reservations(self):
        self.policy['execution_enabled'] = True
        self.treasury.reserve(self.intent('req-01', '0.1'), now=NOW)
        self.treasury.reserve(self.intent('req-02', '0.1'), now=NOW)
        with self.assertRaises(TreasuryError): self.treasury.reserve(self.intent('req-03', '0.01'), now=NOW)

    def test_idempotency_same_request_same_payload_and_change_denied(self):
        self.policy['execution_enabled'] = True
        first = self.treasury.reserve(self.intent(), now=NOW)
        second = self.treasury.reserve(self.intent(), now=NOW)
        self.assertEqual(first, second)
        with self.assertRaises(TreasuryError): self.treasury.reserve(self.intent(amount='0.03'), now=NOW)

    def test_expired_and_invalid_time_denied(self):
        self.policy['execution_enabled'] = True
        with self.assertRaises(TreasuryError): self.treasury.reserve(self.intent(valid=False), now=NOW)
        broken = self.intent(); broken.expires_at = 'not_a_time'
        with self.assertRaises(TreasuryError): self.treasury.reserve(broken, now=NOW)

    def test_no_mark_confirmed_without_external_chain_evidence(self):
        self.policy['execution_enabled'] = True
        self.treasury.reserve(self.intent(), now=NOW)
        with self.assertRaises(TreasuryError): self.treasury.record_confirmation('req-01','fake-hash',False)
        with self.assertRaises(TreasuryError): self.treasury.record_confirmation('req-01','not-actually-verified',True)
        self.assertEqual(self.treasury.reserve(self.intent(), now=NOW)['status'], 'reserved_not_sent')

    def test_cancellation_frees_budget(self):
        self.policy['execution_enabled'] = True
        self.treasury.reserve(self.intent('req-01', '0.1'), now=NOW)
        self.treasury.cancel('req-01')
        self.treasury.reserve(self.intent('req-02', '0.1'), now=NOW)
        self.treasury.reserve(self.intent('req-03', '0.1'), now=NOW)

if __name__ == '__main__': unittest.main()
