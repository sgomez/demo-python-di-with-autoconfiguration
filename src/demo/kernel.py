import uvicorn
from dependency_injector.containers import DynamicContainer
from fastapi import FastAPI

from demo.dependency_injection.containers import ContainerFactory

from .controllers.hello import hello


class App(FastAPI):
    container: DynamicContainer


class Kernel:
    def boot(self):
        app = App(debug=True)
        app.container = ContainerFactory().build(
            config_file="config/config.yaml",
            packages=[
                "demo.commands",
                "demo.controllers",
                "demo.services",
            ],
        )

        app.add_api_route(path="/hello", endpoint=hello)

        return app


def main():
    uvicorn.run("demo.kernel:app", host="0.0.0.0", port=8000, reload=True, workers=2)


app = Kernel().boot()
