#!/usr/bin/env python3

import aws_cdk.core as cdk

from cdkdemo.pipeline_stack import CdkPipelineStack

app = cdk.App()
CdkPipelineStack(app, "PipelineDemoStack", env={
    'account': '914456827738',
    'region': 'us-east-2'
})
app.synth()
