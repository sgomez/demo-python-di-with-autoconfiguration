from dataclasses import dataclass

from demo.dependency_injection.dispatcher import Command, Handler, command_handler
from demo.services.hello import GREETING_SERVICE
from dependency_injector.wiring import Provide

from ..services.hello import GREETING_SERVICE, AbstractGreetingService


@dataclass
class GreetingsCommand(Command):
    name: str


@command_handler(GreetingsCommand)
class GreetingsCommandHandler(Handler):

    __greetingService: AbstractGreetingService

    def __init__(self, greetingService: AbstractGreetingService = Provide[GREETING_SERVICE]) -> None:
        self.__greetingService = greetingService

    async def handle(self, command: GreetingsCommand) -> str:
        return await self.__greetingService.say_hello(command.name)
