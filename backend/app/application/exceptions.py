"""Исключения слоя приложения"""
class ApplicationError(Exception):
    pass


class ExternalServiceError(ApplicationError):
    """Базовая ошибка обращения к внешнему сервису (deribit)"""

class ExternalServiceTransientError(ExternalServiceError): #возможен retry
    pass

class ExternalServiceBusinessError(ExternalServiceError):
    pass


class RedisError(ApplicationError):
    pass


class CacheError(ApplicationError):
    pass

class CacheInvalidError(CacheError):
    pass