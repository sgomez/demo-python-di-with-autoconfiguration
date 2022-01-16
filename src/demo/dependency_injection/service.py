import logging
from typing import Dict

from dependency_injector.wiring import inject, providers

logger = logging.getLogger("uvicorn")

services: Dict[str, providers.Provider] = {}


def service(name: str):
    def handler(cls):
        logger.info(f"Service {cls.__module__}.{cls.__name__} registered.")
        services[name] = providers.Factory(cls)

        return cls

    return inject(handler)
