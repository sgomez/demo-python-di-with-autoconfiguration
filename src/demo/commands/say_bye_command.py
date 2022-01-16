from dataclasses import dataclass

from demo.dependency_injection.dispatcher import Command, Handler, command_handler
from demo.services.hello import GREETING_SERVICE
from dependency_injector.wiring import Provide

from ..services.hello import GREETING_SERVICE, AbstractGreetingService


@dataclass
class GoodbyeCommand(Command):
    name: str


@command_handler(GoodbyeCommand)
class GoodbyeCommandHandler(Handler):

    __greetingService: AbstractGreetingService

    def __init__(self, greetingService: AbstractGreetingService = Provide[GREETING_SERVICE]) -> None:
        self.__greetingService = greetingService

    async def handle(self, command: GoodbyeCommand) -> str:
        return await self.__greetingService.say_bye(command.name)
