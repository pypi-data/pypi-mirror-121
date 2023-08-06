from __future__ import (
    annotations,
)

from typing import (
    Any,
    Optional,
)
from uuid import (
    UUID,
)

from dependency_injector.wiring import (
    Provide,
    inject,
)

from minos.common import (
    MinosBroker,
    MinosBrokerNotProvidedException,
)

from ... import (
    MinosSagaFailedExecutionStepException,
)
from ...context import (
    SagaContext,
)
from ...definitions import (
    SagaOperation,
)
from ...exceptions import (
    MinosSagaExecutorException,
)
from .local import (
    LocalExecutor,
)


class PublishExecutor(LocalExecutor):
    """Publish Executor class.

    This class has the responsibility to publish command on the corresponding broker's queue.
    """

    @inject
    def __init__(
        self,
        *args,
        execution_uuid: UUID,
        reply_topic: Optional[str],
        broker: MinosBroker = Provide["command_broker"],
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.execution_uuid = execution_uuid
        self.reply_topic = reply_topic

        if broker is None or isinstance(broker, Provide):
            raise MinosBrokerNotProvidedException("A broker instance is required.")

        self.broker = broker

    async def exec(self, operation: SagaOperation, context: SagaContext) -> SagaContext:
        """Exec method, that perform the publishing logic run an pre-callback function to generate the command contents.

        :param operation: Operation to be executed.
        :param context: Execution context.
        :return: A saga context instance.
        """
        if operation is None:
            return context

        try:
            request = await self.exec_operation(operation, context)
            await self._publish(operation, request)
        except MinosSagaExecutorException as exc:
            raise MinosSagaFailedExecutionStepException(exc.exception)
        return context

    async def _publish(self, operation: SagaOperation, data: Any) -> None:
        fn = self.broker.send
        topic = operation.name
        saga = self.execution_uuid
        reply_topic = self.reply_topic
        await self.exec_function(fn, topic=topic, data=data, saga=saga, reply_topic=reply_topic)
