"""Strict, local payment-intent preflight for an AI agent.

NO signing, network or asset transfer code is included here. This is the policy
and reservation layer to be paired with separately enforced wallet policies.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import json, sqlite3, re

class TreasuryError(ValueError):
    pass

@dataclass
class Intent:
    request_id: str
    action: str
    asset: str
    amount_units: str
    recipient: str
    expires_at: str

class Treasury:
    def __init__(self, database_path: str, policy: dict):
        self.database_path = database_path
        self.policy = policy
        with sqlite3.connect(database_path) as db:
            db.execute("""CREATE TABLE IF NOT EXISTS intents (
                request_id TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                asset TEXT NOT NULL,
                utc_day TEXT NOT NULL,
                amount_minor INTEGER NOT NULL CHECK(amount_minor>0),
                status TEXT NOT NULL CHECK(status IN ('reserved_not_sent','cancelled'))
            )""")

    def _validate(self, intent: Intent, now: datetime) -> int:
        if self.policy.get('execution_enabled') is not True:
            raise TreasuryError('Policy disabled: all financial write intents blocked')
        if not isinstance(intent, Intent) or not isinstance(intent.request_id,str) or not re.fullmatch(r'[A-Za-z0-9_-]{3,80}', intent.request_id):
            raise TreasuryError('Invalid idempotency key')
        if intent.action != 'transfer':
            raise TreasuryError('Only transfer intent preflight is supported; mint and trades are denied')
        config = self.policy.get('assets', {}).get(intent.asset)
        if not isinstance(config, dict):
            raise TreasuryError('Asset not permitted')
        if intent.recipient not in config.get('recipients', []):
            raise TreasuryError('Recipient not allowlisted')
        if not isinstance(intent.expires_at,str):
            raise TreasuryError('Missing expiration')
        try:
            expiry = datetime.fromisoformat(intent.expires_at.replace('Z','+00:00'))
        except ValueError:
            raise TreasuryError('Invalid expiration')
        if now.tzinfo is None or expiry.tzinfo is None or not now < expiry <= now.replace(hour=23,minute=59,second=59,microsecond=999999):
            raise TreasuryError('Intent expired or beyond same UTC day')
        decimal_places = config.get('decimals')
        if not isinstance(decimal_places,int) or not 0<=decimal_places<=18:
            raise TreasuryError('Invalid asset decimal configuration')
        if not isinstance(intent.amount_units,str):
            raise TreasuryError('Amount must be a decimal string, not a float')
        try:
            amt = Decimal(intent.amount_units)
            if not amt.is_finite() or amt <= 0:
                raise TreasuryError('Amount not positive or finite')
            scaled=amt*(10**decimal_places)
            if scaled != scaled.to_integral_value():
                raise TreasuryError('Amount has more decimals than the asset allows')
            amount_minor=int(scaled)
            max_per=int(Decimal(str(config['max_transfer_units']))*(10**decimal_places))
            if not 0<amount_minor<=max_per:
                raise TreasuryError('Transaction exceeds per-transfer limit')
            return amount_minor
        except (InvalidOperation, KeyError, TypeError, OverflowError) as exc:
            raise TreasuryError('Invalid amount or policy') from exc

    def reserve(self, intent: Intent, now: datetime | None=None) -> dict:
        now = now or datetime.now(timezone.utc)
        amount_minor = self._validate(intent, now)
        day=now.astimezone(timezone.utc).strftime('%Y-%m-%d')
        payload=json.dumps(asdict(intent),sort_keys=True,separators=(',',':'))
        config=self.policy['assets'][intent.asset]
        daily_minor=int(Decimal(str(config['daily_units']))*(10**config['decimals']))
        if daily_minor <= 0:
            raise TreasuryError('Invalid daily cap')
        with sqlite3.connect(self.database_path,timeout=10,isolation_level=None) as db:
            db.execute('BEGIN IMMEDIATE')
            previous=db.execute('SELECT payload,asset,amount_minor,status FROM intents WHERE request_id=?',(intent.request_id,)).fetchone()
            if previous:
                if previous[0]!=payload: raise TreasuryError('Idempotency key reused for a different transaction')
                return {'request_id': intent.request_id,'asset':previous[1],'amount_minor':previous[2],'status':previous[3]}
            used=db.execute("SELECT COALESCE(SUM(amount_minor),0) FROM intents WHERE asset=? AND utc_day=? AND status='reserved_not_sent'",(intent.asset,day)).fetchone()[0]
            if used+amount_minor>daily_minor:
                raise TreasuryError('Daily limit exceeded')
            db.execute('INSERT INTO intents(request_id,payload,asset,utc_day,amount_minor,status) VALUES(?,?,?,?,?,?)',
                       (intent.request_id,payload,intent.asset,day,amount_minor,'reserved_not_sent'))
        return {'request_id':intent.request_id,'asset':intent.asset,'amount_minor':amount_minor,'status':'reserved_not_sent'}

    def cancel(self, request_id: str)->dict:
        with sqlite3.connect(self.database_path) as db:
            cur=db.execute("UPDATE intents SET status='cancelled' WHERE request_id=? AND status='reserved_not_sent'",(request_id,))
            if cur.rowcount!=1: raise TreasuryError('Unknown or already cancelled request')
        return {'request_id':request_id,'status':'cancelled'}

    def record_confirmation(self, request_id:str, txid:str, unverified_claim:bool)->dict:
        """Intentionally reject local confirmation; a trusted chain verifier is absent."""
        raise TreasuryError('Cannot claim onchain confirmation without external chain verification')
