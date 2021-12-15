from aws_cdk import core
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines
from constructs import Construct
from .webservice_stage import WebServiceStage

class CdkPipelineStack(core.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        pipeline = pipelines.CdkPipeline(self, 'CdkDemoPipeline',
            cloud_assembly_artifact=cloud_assembly_artifact,
            pipeline_name='WebinarPipeline',
            source_action=cpactions.GitHubSourceAction(
                action_name='GitHub',
                output=source_artifact,
                oauth_token=core.SecretValue.secrets_manager('MobilizeGithubRepoToken'),
                owner='zyjia8',
                repo='cdkpipeline',
                trigger=cpactions.GitHubTrigger.POLL),
            synth_action=pipelines.SimpleSynthAction(
                source_artifact=source_artifact,
                cloud_assembly_artifact=cloud_assembly_artifact,
                install_command='npm install -g aws-cdk && pip install -r requirements.txt',
                build_command='pytest unit',
                synth_command='cdk synth'
            )
        )
        pre_prod_app = WebServiceStage(self,'Pre-Prod', env={
            'account': '292574139048',
            'region': 'us-east-2'
        })

        pre_prod_stage = pipeline.add_application_stage(pre_prod_app)
        pre_prod_stage.add_actions(pipelines.ShellScriptAction(
            action_name='Integ',
            run_order=pre_prod_stage.next_sequential_run_order(),
            additional_artifacts=[source_artifact],
            commands=[
                'pip install -r requirements.txt',
                'pytest integtests',
            ],
            use_outputs={
                'SERVICE_URL': pipeline.stack_output(pre_prod_app.url_output)
            }
        ))

        pre_prod_stage.add_manual_approval_action(action_name='PromoteToProd')

        pipeline.add_application_stage(WebServiceStage(self,'Prod', env={
            'account': '890395779521',
            'region': 'us-east-2'
        }))        