import inspect
from typing import (
    Any,
    Callable,
)

from ...definitions import (
    SagaOperation,
)
from ...exceptions import (
    MinosSagaExecutorException,
)


class LocalExecutor:
    """Local executor class."""

    def __init__(self, *args, **kwargs):
        pass

    async def exec_operation(self, operation: SagaOperation, *args, **kwargs) -> Any:
        """Execute the given operation locally.

        :param operation: The operation to be executed.
        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        :return: The execution response.
        """

        if operation.parameterized:
            kwargs = {**operation.parameters, **kwargs}

        return await self.exec_function(operation.callback, *args, **kwargs)

    @staticmethod
    async def exec_function(func: Callable, *args, **kwargs) -> Any:
        """Execute a function.

        :param func: Function to be executed.
        :param args: Additional positional arguments to the function.
        :param kwargs: Additional named arguments to the function.
        :return: The ``func`` result.
        """
        try:
            result = func(*args, **kwargs)
            if inspect.isawaitable(result):
                result = await result
        except Exception as exc:
            raise MinosSagaExecutorException(exc)
        return result
