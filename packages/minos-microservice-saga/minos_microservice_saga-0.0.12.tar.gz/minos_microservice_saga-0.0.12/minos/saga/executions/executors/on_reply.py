from typing import (
    Optional,
)

from minos.common import (
    CommandReply,
    CommandStatus,
)

from ...context import (
    SagaContext,
)
from ...definitions import (
    SagaOperation,
)
from ...exceptions import (
    MinosCommandReplyFailedException,
    MinosSagaExecutorException,
    MinosSagaFailedExecutionStepException,
    MinosSagaPausedExecutionStepException,
)
from .local import (
    LocalExecutor,
)


class OnReplyExecutor(LocalExecutor):
    """On Reply Executor class."""

    # noinspection PyUnusedLocal
    async def exec(
        self, operation: SagaOperation, context: SagaContext, reply: Optional[CommandReply] = None, *args, **kwargs
    ) -> SagaContext:
        """Execute the on reply operation.

        :param operation: Operation to be executed.
        :param context: Actual execution context.
        :param reply: Command Reply which contains the response.
        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        :return: An updated context instance.
        """
        if reply is None:
            raise MinosSagaPausedExecutionStepException()

        if reply.status != CommandStatus.SUCCESS:
            raise MinosCommandReplyFailedException(f"CommandReply failed with {reply.status!s} status: {reply.data!s}")

        if operation is None:
            return context

        try:
            response = await self.exec_operation(operation, reply.data)
        except MinosSagaExecutorException as exc:
            raise MinosSagaFailedExecutionStepException(exc.exception)

        try:
            context[operation.name] = response
        except Exception as exc:
            raise MinosSagaFailedExecutionStepException(exc)

        return context
