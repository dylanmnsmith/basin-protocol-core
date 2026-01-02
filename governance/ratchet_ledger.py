"""
The Ratchet Ledger: An immutable, Merkle-chained log for Basin Protocol events.
"""
import hashlib, time, os, json, sys
from typing import Dict, List, Tuple

class RatchetLedger:
    def __init__(self, ledger_path: str, genesis_hash: str = None):
        self.ledger_path = ledger_path
        self.genesis_hash = genesis_hash or self._compute_hash("BASIN_GENESIS_BLOCK")
        os.makedirs(os.path.dirname(ledger_path), exist_ok=True)
        if not os.path.exists(ledger_path): self._write_genesis()
    
    def _write_genesis(self):
        entry = {'entry_hash': self.genesis_hash, 'timestamp': 0, 'event_type': 'GENESIS', 'previous_hash': '0'*64}
        self._write_entry(entry)

    def _compute_hash(self, data: str) -> str:
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def _write_entry(self, entry: Dict):
        with open(self.ledger_path, 'a') as f:
            f.write(json.dumps(entry, sort_keys=True, separators=(',', ':')) + '\n')
            f.flush()
            os.fsync(f.fileno())

    def append_entry(self, event_type: str, data: Dict) -> str:
        # Simplified for efficiency: Read last line, get hash, chain it.
        try:
            with open(self.ledger_path, 'r') as f: lines = f.readlines()
            last_entry = json.loads(lines[-1])
            prev_hash = last_entry['entry_hash']
        except: prev_hash = self.genesis_hash

        entry = {
            'timestamp': time.time(),
            'event_type': event_type,
            'data': data,
            'previous_hash': prev_hash
        }
        # Hashing logic
        content = json.dumps(entry, sort_keys=True, separators=(',', ':'))
        entry['entry_hash'] = self._compute_hash(content)
        self._write_entry(entry)
        return entry['entry_hash']
