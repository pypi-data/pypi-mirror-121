"""
Type annotations for pinpoint service literal definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/literals.html)

Usage::

    ```python
    from mypy_boto3_pinpoint.literals import ActionType

    data: ActionType = "DEEP_LINK"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "ActionType",
    "AlignmentType",
    "AttributeTypeType",
    "ButtonActionType",
    "CampaignStatusType",
    "ChannelTypeType",
    "DeliveryStatusType",
    "DimensionTypeType",
    "DurationType",
    "EndpointTypesElementType",
    "FilterTypeType",
    "FormatType",
    "FrequencyType",
    "IncludeType",
    "JobStatusType",
    "LayoutType",
    "MessageTypeType",
    "ModeType",
    "OperatorType",
    "RecencyTypeType",
    "SegmentTypeType",
    "SourceTypeType",
    "StateType",
    "TemplateTypeType",
    "TypeType",
    "ServiceName",
)

ActionType = Literal["DEEP_LINK", "OPEN_APP", "URL"]
AlignmentType = Literal["CENTER", "LEFT", "RIGHT"]
AttributeTypeType = Literal[
    "AFTER", "BEFORE", "BETWEEN", "CONTAINS", "EXCLUSIVE", "INCLUSIVE", "ON"
]
ButtonActionType = Literal["CLOSE", "DEEP_LINK", "LINK"]
CampaignStatusType = Literal[
    "COMPLETED", "DELETED", "EXECUTING", "INVALID", "PAUSED", "PENDING_NEXT_RUN", "SCHEDULED"
]
ChannelTypeType = Literal[
    "ADM",
    "APNS",
    "APNS_SANDBOX",
    "APNS_VOIP",
    "APNS_VOIP_SANDBOX",
    "BAIDU",
    "CUSTOM",
    "EMAIL",
    "GCM",
    "IN_APP",
    "PUSH",
    "SMS",
    "VOICE",
]
DeliveryStatusType = Literal[
    "DUPLICATE",
    "OPT_OUT",
    "PERMANENT_FAILURE",
    "SUCCESSFUL",
    "TEMPORARY_FAILURE",
    "THROTTLED",
    "UNKNOWN_FAILURE",
]
DimensionTypeType = Literal["EXCLUSIVE", "INCLUSIVE"]
DurationType = Literal["DAY_14", "DAY_30", "DAY_7", "HR_24"]
EndpointTypesElementType = Literal[
    "ADM",
    "APNS",
    "APNS_SANDBOX",
    "APNS_VOIP",
    "APNS_VOIP_SANDBOX",
    "BAIDU",
    "CUSTOM",
    "EMAIL",
    "GCM",
    "IN_APP",
    "PUSH",
    "SMS",
    "VOICE",
]
FilterTypeType = Literal["ENDPOINT", "SYSTEM"]
FormatType = Literal["CSV", "JSON"]
FrequencyType = Literal["DAILY", "EVENT", "HOURLY", "IN_APP_EVENT", "MONTHLY", "ONCE", "WEEKLY"]
IncludeType = Literal["ALL", "ANY", "NONE"]
JobStatusType = Literal[
    "COMPLETED",
    "COMPLETING",
    "CREATED",
    "FAILED",
    "FAILING",
    "INITIALIZING",
    "PENDING_JOB",
    "PREPARING_FOR_INITIALIZATION",
    "PROCESSING",
]
LayoutType = Literal[
    "BOTTOM_BANNER", "CAROUSEL", "MIDDLE_BANNER", "MOBILE_FEED", "OVERLAYS", "TOP_BANNER"
]
MessageTypeType = Literal["PROMOTIONAL", "TRANSACTIONAL"]
ModeType = Literal["DELIVERY", "FILTER"]
OperatorType = Literal["ALL", "ANY"]
RecencyTypeType = Literal["ACTIVE", "INACTIVE"]
SegmentTypeType = Literal["DIMENSIONAL", "IMPORT"]
SourceTypeType = Literal["ALL", "ANY", "NONE"]
StateType = Literal["ACTIVE", "CANCELLED", "CLOSED", "COMPLETED", "DRAFT", "PAUSED"]
TemplateTypeType = Literal["EMAIL", "INAPP", "PUSH", "SMS", "VOICE"]
TypeType = Literal["ALL", "ANY", "NONE"]
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
