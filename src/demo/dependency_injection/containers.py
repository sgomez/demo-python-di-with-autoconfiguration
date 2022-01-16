from typing import List

from demo.dependency_injection.dispatcher import DispatcherFactory
from dependency_injector import containers, providers
from dependency_injector.wiring import register_loader_containers

from .service import services


class ContainerFactory:
    def build(
        self,
        config_file: str,
        modules: List[str] = [],
        packages: List[str] = [],
    ) -> containers.DynamicContainer:
        container = containers.DynamicContainer()
        register_loader_containers(container)
        container.config = self.__load_config(config_file)
        container.wiring_config = self.__load_wiring_config(modules, packages)
        container.wire()

        container.dispatcher_factory = DispatcherFactory()
        for name, provider in services.items():
            setattr(container, name, provider)

        return container

    def __load_config(self, config_files: str) -> providers.Configuration:
        config = providers.Configuration(strict=True)
        config.from_yaml(config_files, required=True)

        return config

    def __load_wiring_config(self, modules: List[str], packages: List[str]) -> containers.WiringConfiguration:
        return containers.WiringConfiguration(modules=modules, packages=packages)
