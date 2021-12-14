#!/usr/bin/env python3
import os

import aws_cdk.core as cdk

from cdkdemo.cdkdemo_stack import CdkdemoStack
from cdkdemo.pipeline_stack import CdkPipelineStack

app = cdk.App()
CdkdemoStack(app, "CdkdemoStack")
CdkPipelineStack(app, "PipelineStack", env={
    'account': '914456827738',
    'region': 'us-east-2'
})
app.synth()
