from constructs import Construct
from aws_cdk import (
    Duration,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_lambda as _lambda,
    aws_lambda_destinations as destination,
    aws_lambda_event_sources as events,
)

_lambda_timeout = Duration.seconds(15)
visibility_timeout = _lambda_timeout.plus(Duration.seconds(5))
retention_period = Duration.minutes(60)
_lambda_retry_attempt = 2


def create_lambda(scope: Construct, construct_id: str, function_name: str, handler: str,
                  path: str, **kwargs) -> _lambda.Function:
    """
    Create vanilla lambda function that does not have DLQ or Destinations.

    Args:
        scope (Construct): the scope object, all child constructs are defined within this scope.
        construct_id(str): id for the construct, used uniquely.
        function_name(str): name of lambda function.
        handler: name of method that Lambda calls to execute function.
        path: source code path of Lambda function.
    """
    return _lambda.Function(scope, construct_id, function_name=function_name, runtime=_lambda.Runtime.PYTHON_3_9,
                            handler=handler, code=_lambda.Code.from_asset(path=path), timeout=_lambda_timeout, **kwargs)


def create_lambda_with_dlq(scope: Construct, construct_id: str, function_name: str, handler: str,
                           path: str, **kwargs) -> _lambda.Function:
    """
    Create lambda function with have DLQ.

    Args:
        scope (Construct): the scope object, all child constructs are defined within this scope.
        construct_id(str): id for the construct, used uniquely.
        function_name(str): name of lambda function.
        handler: name of method that Lambda calls to execute function.
        path: source code path of Lambda function.
    """
    return _lambda.Function(scope, construct_id, function_name=function_name, runtime=_lambda.Runtime.PYTHON_3_9,
                            handler=handler, code=_lambda.Code.from_asset(path=path),
                            dead_letter_queue_enabled=True,
                            retry_attempts=_lambda_retry_attempt,
                            timeout=_lambda_timeout, **kwargs)


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
        sqs.Queue(scope, "lambda-on-success_destination", retention_period=retention_period,
                  visibility_timeout=visibility_timeout))
    on_failure = destination.SqsDestination(
        sqs.Queue(scope, "lambda-on-failure-destination", retention_period=retention_period,
                  visibility_timeout=visibility_timeout))

    function = _lambda.Function(scope, construct_id,
                                function_name=function_name,
                                runtime=_lambda.Runtime.PYTHON_3_9,
                                handler=handler, code=_lambda.Code.from_asset(path=path),
                                dead_letter_queue_enabled=True,
                                retry_attempts=_lambda_retry_attempt,
                                on_success=on_success,
                                on_failure=on_failure,
                                timeout=_lambda_timeout, **kwargs)

    return function


def add_sqs_event_source(scope: Construct, function: _lambda.Function, queue: sqs.Queue):
    """
    Add SQS as Lambda event source.

    Args:
        scope (Construct): the scope object, all child constructs are defined within this scope.
        function: Lambda function to add event source to.
        queue: SQS queue as the Lambda event source.
    """
    sqs_source = events.SqsEventSource(queue, batch_size=1)
    alias = _lambda.Alias(scope, "alias", alias_name="CURRENT", version=function.current_version)
    alias.add_event_source(sqs_source)


def add_sns_event_source(scope: Construct, function: _lambda.Function, topic: sns.Topic):
    """
    Add SNS topic as Lambda event source.

    Args:
        scope (Construct): the scope object, all child constructs are defined within this scope.
        function: Lambda function to add event source to.
        topic: SNS topic as the Lambda event source.
    """
    sns_source = events.SnsEventSource(topic)
    function.add_event_source(sns_source)
