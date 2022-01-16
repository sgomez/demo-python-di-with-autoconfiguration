import logging
from abc import abstractmethod
from dataclasses import dataclass
from importlib import import_module
from typing import Any, Dict, Final

from dependency_injector import providers, wiring

logger = logging.getLogger("uvicorn")

DISPATCHER: Final[str] = "dispatcher_factory"


class Command:
    ...


class Handler:
    __command__: Command

    @abstractmethod
    async def handle(self, command: Command) -> Any:
        raise NotImplementedError


def command_handler(command: Command):
    logger.info(f"Catched command_handler annotation with {command}")

    def wrapper(handler: Handler):
        logger.info(f"Import {handler.__module__}")

        import_module(handler.__module__)
        handler.__command__ = command

        return handler

    return wrapper


@dataclass
class Dispatcher:
    command_handlers: Dict[str, Handler]

    async def dispatch(self, command: Command) -> Any:
        command_handler = self.command_handlers.get(command.__class__)
        if not command_handler:
            logger.warning(f"Command handler for {command} not found.")
            return None

        return await command_handler.handle(command)


def autoconfigure_handlers() -> Dict[str, providers.Factory]:
    command_handlers: Dict[str, providers.Factory] = {}
    for handler in Handler.__subclasses__():
        if not hasattr(handler, "__command__"):
            logger.warning(f"Missed @handle decorator in {handler.__name__} handler.")
            continue

        command = getattr(handler, "__command__")
        if not issubclass(command, Command):
            logger.warning(f"Invalid @handle decorator, {command.__name__} must be a Command.")
            continue

        logger.info(f"Command handler {handler.__module__}.{handler.__name__} registered.")
        command_handlers[command] = providers.Factory(wiring.inject(handler))

    return command_handlers


class DispatcherFactory(providers.Factory):
    __slots__ = ("factory",)

    def __init__(self):
        super().__init__(
            provides=Dispatcher,
            command_handlers=providers.Dict(autoconfigure_handlers()),
        )
