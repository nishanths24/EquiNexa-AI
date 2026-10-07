class MarketDataError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ProviderSymbolUnsupported(MarketDataError):
    def __init__(self, symbol: str):
        super().__init__(
            code="PROVIDER_SYMBOL_UNSUPPORTED",
            message=f"The requested symbol {symbol} is not supported by the provider.",
            status_code=404
        )

class InvalidDateRange(MarketDataError):
    def __init__(self, message: str):
        super().__init__(code="INVALID_DATE_RANGE", message=message, status_code=422)

class UnsupportedIntervalRange(MarketDataError):
    def __init__(self, message: str):
        super().__init__(code="UNSUPPORTED_INTERVAL_RANGE", message=message, status_code=422)
