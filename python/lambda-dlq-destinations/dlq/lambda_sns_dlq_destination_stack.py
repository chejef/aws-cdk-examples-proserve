from aws_cdk import (
    aws_sns as sns,
    Stack,
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
        function = core_lambda.create_lambda_with_dlq_destination(self, "lambda", function_name="dlq_lambda",
                                                                  handler="lambda.handler", path="dlq/function",
                                                                  **kwargs)
        # associate lambda with sns as event source.
        core_lambda.add_sns_event_source(self, function, topic)

