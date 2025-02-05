class BMEBotError(Exception):
    """Base exception for BME IT Bot"""
    pass

class TeamDynamixError(BMEBotError):
    """TeamDynamix related errors"""
    pass

class AuthenticationError(BMEBotError):
    """Authentication related errors"""
    pass

class RateLimitError(BMEBotError):
    """Rate limiting related errors"""
    pass

class ValidationError(BMEBotError):
    """Data validation errors"""
    pass

class TemplateError(BMEBotError):
    """Template related errors"""
    pass 