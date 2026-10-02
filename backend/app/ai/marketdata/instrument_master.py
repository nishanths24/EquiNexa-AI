import json
from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime

class Instrument(BaseModel):
    instrument_id: str
    symbol: str
    provider_symbols: Dict[str, str]
    name: str
    aliases: List[str] = []
    market: str
    exchange: str
    currency: str
    timezone: str
    instrument_type: str
    sector: Optional[str] = None
    is_active: bool = True
    last_verified_at: Optional[datetime] = None

class InstrumentMaster:
    def __init__(self):
        self._instruments: Dict[str, Instrument] = {}
        
    def add_instrument(self, instrument: Instrument):
        self._instruments[instrument.symbol] = instrument
        
    def get_by_symbol(self, symbol: str) -> Optional[Instrument]:
        return self._instruments.get(symbol)
        
    def resolve_alias(self, alias: str) -> Optional[Instrument]:
        for inst in self._instruments.values():
            if alias.lower() in [a.lower() for a in inst.aliases] or alias.lower() == inst.name.lower() or alias.upper() == inst.symbol.upper():
                return inst
        return None
