# Dependency injection in python with autoconfiguration

This is a demo using [ets-labs/python-dependency-injector
](https://github.com/ets-labs/python-dependency-injector).

The base is a DynamicContainer to autoconfigure services using the decorators `@services` for regular services and `@command_handler` for using command pattern.

# Run the project

You need to have installed [poetry](https://python-poetry.org/):

1. poetry install
2. poetry run dev
3. Open http://localhost:8000/docs/
