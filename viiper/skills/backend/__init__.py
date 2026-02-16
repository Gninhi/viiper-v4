"""Backend skills package."""

from viiper.skills.backend.jwt_auth import JWTAuthenticationSkill
from viiper.skills.backend.api_routes import RESTAPIRoutesSkill
from viiper.skills.backend.database_models import DatabaseModelsSkill
from viiper.skills.backend.error_handling import ErrorHandlingSkill
from viiper.skills.backend.validation import InputValidationSkill
from viiper.skills.backend.security import SecurityConfigSkill
from viiper.skills.backend.file_upload import FileUploadSkill
from viiper.skills.backend.email_service import EmailServiceSkill
from viiper.skills.backend.caching import CachingSkill
from viiper.skills.backend.pagination import PaginationSkill
from viiper.skills.backend.logging import LoggingSkill
from viiper.skills.backend.websockets import WebSocketsSkill
from viiper.skills.backend.rate_limiting import RateLimitingSkill
from viiper.skills.backend.background_jobs import BackgroundJobsSkill
from viiper.skills.backend.health_checks import HealthChecksSkill
from viiper.skills.backend.api_documentation import APIDocumentationSkill

__all__ = [
    "JWTAuthenticationSkill",
    "RESTAPIRoutesSkill",
    "DatabaseModelsSkill",
    "ErrorHandlingSkill",
    "InputValidationSkill",
    "SecurityConfigSkill",
    "FileUploadSkill",
    "EmailServiceSkill",
    "CachingSkill",
    "PaginationSkill",
    "LoggingSkill",
    "WebSocketsSkill",
    "RateLimitingSkill",
    "BackgroundJobsSkill",
    "HealthChecksSkill",
    "APIDocumentationSkill",
]
