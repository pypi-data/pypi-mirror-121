"""
Type annotations for robomaker service literal definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_robomaker/literals.html)

Usage::

    ```python
    from mypy_boto3_robomaker.literals import ArchitectureType

    data: ArchitectureType = "ARM64"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "ArchitectureType",
    "DeploymentJobErrorCodeType",
    "DeploymentStatusType",
    "ExitBehaviorType",
    "FailureBehaviorType",
    "ListDeploymentJobsPaginatorName",
    "ListFleetsPaginatorName",
    "ListRobotApplicationsPaginatorName",
    "ListRobotsPaginatorName",
    "ListSimulationApplicationsPaginatorName",
    "ListSimulationJobBatchesPaginatorName",
    "ListSimulationJobsPaginatorName",
    "ListWorldExportJobsPaginatorName",
    "ListWorldGenerationJobsPaginatorName",
    "ListWorldTemplatesPaginatorName",
    "ListWorldsPaginatorName",
    "RenderingEngineTypeType",
    "RobotDeploymentStepType",
    "RobotSoftwareSuiteTypeType",
    "RobotSoftwareSuiteVersionTypeType",
    "RobotStatusType",
    "SimulationJobBatchErrorCodeType",
    "SimulationJobBatchStatusType",
    "SimulationJobErrorCodeType",
    "SimulationJobStatusType",
    "SimulationSoftwareSuiteTypeType",
    "UploadBehaviorType",
    "WorldExportJobErrorCodeType",
    "WorldExportJobStatusType",
    "WorldGenerationJobErrorCodeType",
    "WorldGenerationJobStatusType",
    "ServiceName",
)

ArchitectureType = Literal["ARM64", "ARMHF", "X86_64"]
DeploymentJobErrorCodeType = Literal[
    "BadLambdaAssociated",
    "BadPermissionError",
    "DeploymentFleetDoesNotExist",
    "DownloadConditionFailed",
    "EnvironmentSetupError",
    "EtagMismatch",
    "ExtractingBundleFailure",
    "FailureThresholdBreached",
    "FleetDeploymentTimeout",
    "GreengrassDeploymentFailed",
    "GreengrassGroupVersionDoesNotExist",
    "InternalServerError",
    "InvalidGreengrassGroup",
    "LambdaDeleted",
    "MissingRobotApplicationArchitecture",
    "MissingRobotArchitecture",
    "MissingRobotDeploymentResource",
    "PostLaunchFileFailure",
    "PreLaunchFileFailure",
    "ResourceNotFound",
    "RobotAgentConnectionTimeout",
    "RobotApplicationDoesNotExist",
    "RobotDeploymentAborted",
    "RobotDeploymentNoResponse",
]
DeploymentStatusType = Literal[
    "Canceled", "Failed", "InProgress", "Pending", "Preparing", "Succeeded"
]
ExitBehaviorType = Literal["FAIL", "RESTART"]
FailureBehaviorType = Literal["Continue", "Fail"]
ListDeploymentJobsPaginatorName = Literal["list_deployment_jobs"]
ListFleetsPaginatorName = Literal["list_fleets"]
ListRobotApplicationsPaginatorName = Literal["list_robot_applications"]
ListRobotsPaginatorName = Literal["list_robots"]
ListSimulationApplicationsPaginatorName = Literal["list_simulation_applications"]
ListSimulationJobBatchesPaginatorName = Literal["list_simulation_job_batches"]
ListSimulationJobsPaginatorName = Literal["list_simulation_jobs"]
ListWorldExportJobsPaginatorName = Literal["list_world_export_jobs"]
ListWorldGenerationJobsPaginatorName = Literal["list_world_generation_jobs"]
ListWorldTemplatesPaginatorName = Literal["list_world_templates"]
ListWorldsPaginatorName = Literal["list_worlds"]
RenderingEngineTypeType = Literal["OGRE"]
RobotDeploymentStepType = Literal[
    "DownloadingExtracting",
    "ExecutingDownloadCondition",
    "ExecutingPostLaunch",
    "ExecutingPreLaunch",
    "Finished",
    "Launching",
    "Validating",
]
RobotSoftwareSuiteTypeType = Literal["ROS", "ROS2"]
RobotSoftwareSuiteVersionTypeType = Literal["Dashing", "Foxy", "Kinetic", "Melodic"]
RobotStatusType = Literal[
    "Available", "Deploying", "Failed", "InSync", "NoResponse", "PendingNewDeployment", "Registered"
]
SimulationJobBatchErrorCodeType = Literal["InternalServiceError"]
SimulationJobBatchStatusType = Literal[
    "Canceled",
    "Canceling",
    "Completed",
    "Completing",
    "Failed",
    "InProgress",
    "Pending",
    "TimedOut",
    "TimingOut",
]
SimulationJobErrorCodeType = Literal[
    "BadPermissionsCloudwatchLogs",
    "BadPermissionsRobotApplication",
    "BadPermissionsS3Object",
    "BadPermissionsS3Output",
    "BadPermissionsSimulationApplication",
    "BadPermissionsUserCredentials",
    "BatchCanceled",
    "BatchTimedOut",
    "ENILimitExceeded",
    "InternalServiceError",
    "InvalidBundleRobotApplication",
    "InvalidBundleSimulationApplication",
    "InvalidInput",
    "InvalidS3Resource",
    "LimitExceeded",
    "MismatchedEtag",
    "RequestThrottled",
    "ResourceNotFound",
    "RobotApplicationCrash",
    "RobotApplicationHealthCheckFailure",
    "RobotApplicationVersionMismatchedEtag",
    "SimulationApplicationCrash",
    "SimulationApplicationHealthCheckFailure",
    "SimulationApplicationVersionMismatchedEtag",
    "SubnetIpLimitExceeded",
    "ThrottlingError",
    "UploadContentMismatchError",
    "WrongRegionRobotApplication",
    "WrongRegionS3Bucket",
    "WrongRegionS3Output",
    "WrongRegionSimulationApplication",
]
SimulationJobStatusType = Literal[
    "Canceled",
    "Completed",
    "Failed",
    "Pending",
    "Preparing",
    "Restarting",
    "Running",
    "RunningFailed",
    "Terminated",
    "Terminating",
]
SimulationSoftwareSuiteTypeType = Literal["Gazebo", "RosbagPlay"]
UploadBehaviorType = Literal["UPLOAD_ON_TERMINATE", "UPLOAD_ROLLING_AUTO_REMOVE"]
WorldExportJobErrorCodeType = Literal[
    "AccessDenied",
    "InternalServiceError",
    "InvalidInput",
    "LimitExceeded",
    "RequestThrottled",
    "ResourceNotFound",
]
WorldExportJobStatusType = Literal[
    "Canceled", "Canceling", "Completed", "Failed", "Pending", "Running"
]
WorldGenerationJobErrorCodeType = Literal[
    "AllWorldGenerationFailed",
    "InternalServiceError",
    "InvalidInput",
    "LimitExceeded",
    "RequestThrottled",
    "ResourceNotFound",
]
WorldGenerationJobStatusType = Literal[
    "Canceled", "Canceling", "Completed", "Failed", "PartialFailed", "Pending", "Running"
]
ServiceName = Literal[
    "accessanalyzer",
    "acm",
    "acm-pca",
    "alexaforbusiness",
    "amp",
    "amplify",
    "amplifybackend",
    "apigateway",
    "apigatewaymanagementapi",
    "apigatewayv2",
    "appconfig",
    "appflow",
    "appintegrations",
    "application-autoscaling",
    "application-insights",
    "applicationcostprofiler",
    "appmesh",
    "apprunner",
    "appstream",
    "appsync",
    "athena",
    "auditmanager",
    "autoscaling",
    "autoscaling-plans",
    "backup",
    "batch",
    "braket",
    "budgets",
    "ce",
    "chime",
    "chime-sdk-identity",
    "chime-sdk-messaging",
    "cloud9",
    "clouddirectory",
    "cloudformation",
    "cloudfront",
    "cloudhsm",
    "cloudhsmv2",
    "cloudsearch",
    "cloudsearchdomain",
    "cloudtrail",
    "cloudwatch",
    "codeartifact",
    "codebuild",
    "codecommit",
    "codedeploy",
    "codeguru-reviewer",
    "codeguruprofiler",
    "codepipeline",
    "codestar",
    "codestar-connections",
    "codestar-notifications",
    "cognito-identity",
    "cognito-idp",
    "cognito-sync",
    "comprehend",
    "comprehendmedical",
    "compute-optimizer",
    "config",
    "connect",
    "connect-contact-lens",
    "connectparticipant",
    "cur",
    "customer-profiles",
    "databrew",
    "dataexchange",
    "datapipeline",
    "datasync",
    "dax",
    "detective",
    "devicefarm",
    "devops-guru",
    "directconnect",
    "discovery",
    "dlm",
    "dms",
    "docdb",
    "ds",
    "dynamodb",
    "dynamodbstreams",
    "ebs",
    "ec2",
    "ec2-instance-connect",
    "ecr",
    "ecr-public",
    "ecs",
    "efs",
    "eks",
    "elastic-inference",
    "elasticache",
    "elasticbeanstalk",
    "elastictranscoder",
    "elb",
    "elbv2",
    "emr",
    "emr-containers",
    "es",
    "events",
    "finspace",
    "finspace-data",
    "firehose",
    "fis",
    "fms",
    "forecast",
    "forecastquery",
    "frauddetector",
    "fsx",
    "gamelift",
    "glacier",
    "globalaccelerator",
    "glue",
    "greengrass",
    "greengrassv2",
    "groundstation",
    "guardduty",
    "health",
    "healthlake",
    "honeycode",
    "iam",
    "identitystore",
    "imagebuilder",
    "importexport",
    "inspector",
    "iot",
    "iot-data",
    "iot-jobs-data",
    "iot1click-devices",
    "iot1click-projects",
    "iotanalytics",
    "iotdeviceadvisor",
    "iotevents",
    "iotevents-data",
    "iotfleethub",
    "iotsecuretunneling",
    "iotsitewise",
    "iotthingsgraph",
    "iotwireless",
    "ivs",
    "kafka",
    "kafkaconnect",
    "kendra",
    "kinesis",
    "kinesis-video-archived-media",
    "kinesis-video-media",
    "kinesis-video-signaling",
    "kinesisanalytics",
    "kinesisanalyticsv2",
    "kinesisvideo",
    "kms",
    "lakeformation",
    "lambda",
    "lex-models",
    "lex-runtime",
    "lexv2-models",
    "lexv2-runtime",
    "license-manager",
    "lightsail",
    "location",
    "logs",
    "lookoutequipment",
    "lookoutmetrics",
    "lookoutvision",
    "machinelearning",
    "macie",
    "macie2",
    "managedblockchain",
    "marketplace-catalog",
    "marketplace-entitlement",
    "marketplacecommerceanalytics",
    "mediaconnect",
    "mediaconvert",
    "medialive",
    "mediapackage",
    "mediapackage-vod",
    "mediastore",
    "mediastore-data",
    "mediatailor",
    "memorydb",
    "meteringmarketplace",
    "mgh",
    "mgn",
    "migrationhub-config",
    "mobile",
    "mq",
    "mturk",
    "mwaa",
    "neptune",
    "network-firewall",
    "networkmanager",
    "nimble",
    "opensearch",
    "opsworks",
    "opsworkscm",
    "organizations",
    "outposts",
    "personalize",
    "personalize-events",
    "personalize-runtime",
    "pi",
    "pinpoint",
    "pinpoint-email",
    "pinpoint-sms-voice",
    "polly",
    "pricing",
    "proton",
    "qldb",
    "qldb-session",
    "quicksight",
    "ram",
    "rds",
    "rds-data",
    "redshift",
    "redshift-data",
    "rekognition",
    "resource-groups",
    "resourcegroupstaggingapi",
    "robomaker",
    "route53",
    "route53-recovery-cluster",
    "route53-recovery-control-config",
    "route53-recovery-readiness",
    "route53domains",
    "route53resolver",
    "s3",
    "s3control",
    "s3outposts",
    "sagemaker",
    "sagemaker-a2i-runtime",
    "sagemaker-edge",
    "sagemaker-featurestore-runtime",
    "sagemaker-runtime",
    "savingsplans",
    "schemas",
    "sdb",
    "secretsmanager",
    "securityhub",
    "serverlessrepo",
    "service-quotas",
    "servicecatalog",
    "servicecatalog-appregistry",
    "servicediscovery",
    "ses",
    "sesv2",
    "shield",
    "signer",
    "sms",
    "sms-voice",
    "snow-device-management",
    "snowball",
    "sns",
    "sqs",
    "ssm",
    "ssm-contacts",
    "ssm-incidents",
    "sso",
    "sso-admin",
    "sso-oidc",
    "stepfunctions",
    "storagegateway",
    "sts",
    "support",
    "swf",
    "synthetics",
    "textract",
    "timestream-query",
    "timestream-write",
    "transcribe",
    "transfer",
    "translate",
    "waf",
    "waf-regional",
    "wafv2",
    "wellarchitected",
    "workdocs",
    "worklink",
    "workmail",
    "workmailmessageflow",
    "workspaces",
    "xray",
]
