from aws_cdk import (
    aws_sqs as sqs,
    Stack,
)
from constructs import Construct
from dlq import core_lambda

_dlq_retry_count = 3


class LambdaSQSDlqStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        """
        Constructor for Lambda function with SQS as event source and SQS DLQ for un-successfully processed events.

        Args:
            scope (Construct): the scope object, all child constructs are defined within this scope.
            construct_id(str): id for the construct, used uniquely.
        """
        super().__init__(scope, construct_id, **kwargs)

        # create dlq for sqs queue.
        dlq = sqs.Queue(self, "sqs-dlq", retention_period=core_lambda.retention_period,
                        visibility_timeout=core_lambda.visibility_timeout)
        # create sqs queue.
        queue = sqs.Queue(self, "sqs", retention_period=core_lambda.retention_period,
                          visibility_timeout=core_lambda.visibility_timeout,
                          dead_letter_queue=sqs.DeadLetterQueue(max_receive_count=_dlq_retry_count, queue=dlq))
        # create lambda function.
        function = core_lambda.create_lambda(self, "lambda", function_name="dlq_lambda", handler="lambda.handler",
                                             path="dlq/function", **kwargs)
        # associate lambda with sqs as event source.
        core_lambda.add_sqs_event_source(self, function, queue)

