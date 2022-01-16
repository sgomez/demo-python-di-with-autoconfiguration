from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.responses import JSONResponse

from ..commands.say_hello_command import GreetingsCommand
from ..dependency_injection.dispatcher import DISPATCHER, Dispatcher
from ..services.router import api_route


@api_route(path="/hello")
@inject
async def hello(
    name: Optional[str] = None,
    dispatcher: Dispatcher = Depends(Provide[DISPATCHER]),
):
    greeting = await dispatcher.dispatch(GreetingsCommand(name=name))

    return JSONResponse(content={"message": greeting})
