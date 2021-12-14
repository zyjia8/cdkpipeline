from aws_cdk import core
from .cdkdemo_stack import CdkdemoStack

class WebServiceStage(core.Stage):
  def __init__(self, scope: core.Construct, id: str, **kwargs):
    super().__init__(scope, id, **kwargs)

    service = CdkdemoStack(self, 'WebService')

    self.url_output = service.url_output