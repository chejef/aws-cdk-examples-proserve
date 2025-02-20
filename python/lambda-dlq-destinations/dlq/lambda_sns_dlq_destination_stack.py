from aws_cdk import (
    Stack,
    aws_sns as sns,
    aws_sqs as sqs,
    aws_lambda as _lambda,
    aws_lambda_destinations as destination,
)
from constructs import Construct
from dlq import core_lambda


class LambdaSnsDlqDestinationStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        """
        Constructor for Lambda function with SNS as event source as well as Lambda Destinations and DLQ
        for un-successfully processed events.

        Args:
            scope (Construct): the scope object, all child constructs are defined within this scope.
            construct_id(str): id for the construct, used uniquely.
        """
        super().__init__(scope, construct_id, **kwargs)

        # create SNS topic for aggregate data notification.
        topic = sns.Topic(self, "topic", display_name="topic", topic_name="lambda_topic")

        # create lambda function.
        function = create_lambda_with_dlq_destination(self, "lambda", function_name="dlq_lambda",
                                                      handler="lambda.handler", path="dlq/function", **kwargs)
        # associate lambda with sns as event source.
        core_lambda.add_sns_event_source(self, function, topic)


def create_lambda_with_dlq_destination(scope: Construct, construct_id: str, function_name: str, handler: str,
                                       path: str, **kwargs) -> _lambda.Function:
    """
    Create lambda function with have DLQ and Destinations.

    Args:
        scope (Construct): the scope object, all child constructs are defined within this scope.
        construct_id(str): id for the construct, used uniquely.
        function_name(str): name of lambda function.
        handler: name of method that Lambda calls to execute function.
        path: source code path of Lambda function.
    """
    # create lambda on success destination.
    on_success = destination.SqsDestination(
        sqs.Queue(scope, "lambda-on-success_destination", retention_period=core_lambda.retention_period,
                  visibility_timeout=core_lambda.visibility_timeout))
    on_failure = destination.SqsDestination(
        sqs.Queue(scope, "lambda-on-failure-destination", retention_period=core_lambda.retention_period,
                  visibility_timeout=core_lambda.visibility_timeout))

    function = _lambda.Function(scope, construct_id,
                                function_name=function_name,
                                runtime=_lambda.Runtime.PYTHON_3_9,
                                handler=handler, code=_lambda.Code.from_asset(path=path),
                                dead_letter_queue_enabled=True,
                                retry_attempts=core_lambda.lambda_retry_attempt,
                                on_success=on_success,
                                on_failure=on_failure,
                                timeout=core_lambda.lambda_timeout, **kwargs)

    return function
