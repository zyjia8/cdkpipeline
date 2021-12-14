import aws_cdk as core
import aws_cdk.assertions as assertions

from cdkdemo.cdkdemo_stack import CdkdemoStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdkdemo/cdkdemo_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkdemoStack(app, "cdkdemo")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
