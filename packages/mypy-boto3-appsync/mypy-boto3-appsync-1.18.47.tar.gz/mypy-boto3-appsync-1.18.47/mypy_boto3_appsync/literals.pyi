"""
Type annotations for appsync service literal definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_appsync/literals.html)

Usage::

    ```python
    from mypy_boto3_appsync.literals import ApiCacheStatusType

    data: ApiCacheStatusType = "AVAILABLE"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "ApiCacheStatusType",
    "ApiCacheTypeType",
    "ApiCachingBehaviorType",
    "AuthenticationTypeType",
    "AuthorizationTypeType",
    "ConflictDetectionTypeType",
    "ConflictHandlerTypeType",
    "DataSourceTypeType",
    "DefaultActionType",
    "FieldLogLevelType",
    "ListApiKeysPaginatorName",
    "ListDataSourcesPaginatorName",
    "ListFunctionsPaginatorName",
    "ListGraphqlApisPaginatorName",
    "ListResolversByFunctionPaginatorName",
    "ListResolversPaginatorName",
    "ListTypesPaginatorName",
    "OutputTypeType",
    "RelationalDatabaseSourceTypeType",
    "ResolverKindType",
    "SchemaStatusType",
    "TypeDefinitionFormatType",
    "ServiceName",
)

ApiCacheStatusType = Literal["AVAILABLE", "CREATING", "DELETING", "FAILED", "MODIFYING"]
ApiCacheTypeType = Literal[
    "LARGE",
    "LARGE_12X",
    "LARGE_2X",
    "LARGE_4X",
    "LARGE_8X",
    "MEDIUM",
    "R4_2XLARGE",
    "R4_4XLARGE",
    "R4_8XLARGE",
    "R4_LARGE",
    "R4_XLARGE",
    "SMALL",
    "T2_MEDIUM",
    "T2_SMALL",
    "XLARGE",
]
ApiCachingBehaviorType = Literal["FULL_REQUEST_CACHING", "PER_RESOLVER_CACHING"]
AuthenticationTypeType = Literal[
    "AMAZON_COGNITO_USER_POOLS", "API_KEY", "AWS_IAM", "AWS_LAMBDA", "OPENID_CONNECT"
]
AuthorizationTypeType = Literal["AWS_IAM"]
ConflictDetectionTypeType = Literal["NONE", "VERSION"]
ConflictHandlerTypeType = Literal["AUTOMERGE", "LAMBDA", "NONE", "OPTIMISTIC_CONCURRENCY"]
DataSourceTypeType = Literal[
    "AMAZON_DYNAMODB",
    "AMAZON_ELASTICSEARCH",
    "AMAZON_OPENSEARCH_SERVICE",
    "AWS_LAMBDA",
    "HTTP",
    "NONE",
    "RELATIONAL_DATABASE",
]
DefaultActionType = Literal["ALLOW", "DENY"]
FieldLogLevelType = Literal["ALL", "ERROR", "NONE"]
ListApiKeysPaginatorName = Literal["list_api_keys"]
ListDataSourcesPaginatorName = Literal["list_data_sources"]
ListFunctionsPaginatorName = Literal["list_functions"]
ListGraphqlApisPaginatorName = Literal["list_graphql_apis"]
ListResolversByFunctionPaginatorName = Literal["list_resolvers_by_function"]
ListResolversPaginatorName = Literal["list_resolvers"]
ListTypesPaginatorName = Literal["list_types"]
OutputTypeType = Literal["JSON", "SDL"]
RelationalDatabaseSourceTypeType = Literal["RDS_HTTP_ENDPOINT"]
ResolverKindType = Literal["PIPELINE", "UNIT"]
SchemaStatusType = Literal[
    "ACTIVE", "DELETING", "FAILED", "NOT_APPLICABLE", "PROCESSING", "SUCCESS"
]
TypeDefinitionFormatType = Literal["JSON", "SDL"]
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
