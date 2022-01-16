from abc import abstractmethod
from typing import Final, Optional

from demo.dependency_injection.service import service
from dependency_injector.wiring import Provide

GREETING_SERVICE: Final[str] = "greeting_service"


class AbstractGreetingService:
    @abstractmethod
    def say_hello(self, name: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def say_bye(self, name: str) -> str:
        raise NotImplementedError


@service(GREETING_SERVICE)
class GreetingService(AbstractGreetingService):
    __default_name: str

    def __init__(
        self,
        default_name=Provide["config.demo.name"],
    ) -> None:
        self.__default_name = default_name

    async def say_hello(self, name: Optional[str]) -> str:
        if not name:
            return f"Hello, {self.__default_name}"

        return f"Hello, {name}"

    async def say_bye(self, name: Optional[str]) -> str:
        if not name:
            return f"Bye, {self.__default_name}"

        return f"Bye, {name}"
