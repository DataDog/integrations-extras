# (C) Datadog, Inc. 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from __future__ import annotations

from typing import Optional
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from datadog_checks.base.utils.functions import identity
from datadog_checks.base.utils.models import validation

from . import defaults, validators


class InstanceConfig(BaseModel):
    model_config = ConfigDict(
        validate_default=True,
        arbitrary_types_allowed=True,
        frozen=True,
    )
    empty_default_hostname: Optional[bool] = None
    min_collection_interval: Optional[float] = None
    service: Optional[str] = None
    tags: Optional[tuple[str, ...]] = None
    url: str
    username: str
    password: str = Field(repr=False)
    cd_node: str
    cd_port: int = 1363
    cd_protocol: str = 'TCPIP'
    tls_verify: bool = True
    timeout: float = 10
    statistics_lookback_minutes: int = 2
    statistics_timezone: Optional[str] = None

    @field_validator('url')
    @classmethod
    def validate_url(cls, value: str) -> str:
        from urllib.parse import urlparse

        parsed = urlparse(value)
        if parsed.scheme not in ('http', 'https') or not parsed.netloc:
            raise ValueError('url must be an absolute HTTP or HTTPS URL')
        return value.rstrip('/')

    @field_validator('timeout')
    @classmethod
    def validate_timeout(cls, value: float) -> float:
        if value <= 0:
            raise ValueError('timeout must be greater than zero')
        return value

    @field_validator('statistics_lookback_minutes')
    @classmethod
    def validate_statistics_lookback(cls, value: int) -> int:
        if value <= 0:
            raise ValueError('statistics_lookback_minutes must be greater than zero')
        return value

    @field_validator('statistics_timezone')
    @classmethod
    def validate_statistics_timezone(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            try:
                ZoneInfo(value)
            except (TypeError, ValueError, ZoneInfoNotFoundError) as err:
                raise ValueError('statistics_timezone must be a valid IANA timezone') from err
        return value

    @model_validator(mode='before')
    def _initial_validation(cls, values):
        return validation.core.initialize_config(getattr(validators, 'initialize_instance', identity)(values))

    @field_validator('*', mode='before')
    def _validate(cls, value, info):
        field = cls.model_fields[info.field_name]
        field_name = field.alias or info.field_name
        if field_name in info.context['configured_fields']:
            value = getattr(validators, f'instance_{info.field_name}', identity)(value, field=field)
        elif info.field_name not in (
            'url', 'username', 'password', 'cd_node', 'cd_port', 'cd_protocol', 'tls_verify', 'timeout',
            'statistics_lookback_minutes',
            'statistics_timezone',
        ):
            value = getattr(defaults, f'instance_{info.field_name}', lambda: value)()

        return validation.utils.make_immutable(value)

    @model_validator(mode='after')
    def _final_validation(cls, model):
        return validation.core.check_model(getattr(validators, 'check_instance', identity)(model))
