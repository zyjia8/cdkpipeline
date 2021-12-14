from aws_cdk import core
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines
from constructs import Construct

class CdkPipelineStack(core.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        pipelines.CdkPipeline(self, 'CdkDemoPipeline',
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
                synth_command='cdk synth'
            )
        )