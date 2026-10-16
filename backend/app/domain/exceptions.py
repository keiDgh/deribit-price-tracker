"""Доменные исключения"""

class CurrencyError(Exception):
    pass

class CurrencyNotFoundError(CurrencyError):
    pass

class TickerAlreadyExistsError(CurrencyError):
    pass


class PriceError(Exception):
    pass

class PriceNotFoundError(PriceError):
    pass

class RelatedCurrencyNotFound(PriceError):
    """Попытка сослаться на несуществующую валюту при создании"""
    pass