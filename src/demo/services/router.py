import uvicorn
from dependency_injector.wiring import inject
from fastapi import APIRouter, FastAPI, Response
from fastapi.routing import APIRoute

_router = APIRouter()


def api_route(
    path: str,
):
    def wrapped(fn):
        _router.add_api_route(path=path, endpoint=fn)

        return inject(fn)

    return wrapped
