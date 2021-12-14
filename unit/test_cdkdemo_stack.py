import aws_cdk.core as core
import aws_cdk.assertions as assertions

from cdkdemo.cdkdemo_stack import CdkdemoStack

def test_lambda_handler():
    # Given
    app = core.App()

    # When
    CdkdemoStack(app, 'Stack')

    # Then
    template = app.synth().get_stack_by_name('Stack').template
    functions = [resource for resource in template['Resources'].values()
                    if resource['Type'] == 'AWS::Lambda::Function']
    assert len(functions) == 1
    assert functions[0]['Properties']['Handler'] == 'handler.handler'