"""
Type annotations for cloudformation service literal definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/literals.html)

Usage::

    ```python
    from mypy_boto3_cloudformation.literals import AccountGateStatusType

    data: AccountGateStatusType = "FAILED"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "AccountGateStatusType",
    "CallAsType",
    "CapabilityType",
    "CategoryType",
    "ChangeActionType",
    "ChangeSetCreateCompleteWaiterName",
    "ChangeSetStatusType",
    "ChangeSetTypeType",
    "ChangeSourceType",
    "ChangeTypeType",
    "DeprecatedStatusType",
    "DescribeAccountLimitsPaginatorName",
    "DescribeChangeSetPaginatorName",
    "DescribeStackEventsPaginatorName",
    "DescribeStacksPaginatorName",
    "DifferenceTypeType",
    "EvaluationTypeType",
    "ExecutionStatusType",
    "HandlerErrorCodeType",
    "IdentityProviderType",
    "ListChangeSetsPaginatorName",
    "ListExportsPaginatorName",
    "ListImportsPaginatorName",
    "ListStackInstancesPaginatorName",
    "ListStackResourcesPaginatorName",
    "ListStackSetOperationResultsPaginatorName",
    "ListStackSetOperationsPaginatorName",
    "ListStackSetsPaginatorName",
    "ListStacksPaginatorName",
    "ListTypesPaginatorName",
    "OnFailureType",
    "OperationStatusType",
    "PermissionModelsType",
    "ProvisioningTypeType",
    "PublisherStatusType",
    "RegionConcurrencyTypeType",
    "RegistrationStatusType",
    "RegistryTypeType",
    "ReplacementType",
    "RequiresRecreationType",
    "ResourceAttributeType",
    "ResourceSignalStatusType",
    "ResourceStatusType",
    "StackCreateCompleteWaiterName",
    "StackDeleteCompleteWaiterName",
    "StackDriftDetectionStatusType",
    "StackDriftStatusType",
    "StackExistsWaiterName",
    "StackImportCompleteWaiterName",
    "StackInstanceDetailedStatusType",
    "StackInstanceFilterNameType",
    "StackInstanceStatusType",
    "StackResourceDriftStatusType",
    "StackRollbackCompleteWaiterName",
    "StackSetDriftDetectionStatusType",
    "StackSetDriftStatusType",
    "StackSetOperationActionType",
    "StackSetOperationResultStatusType",
    "StackSetOperationStatusType",
    "StackSetStatusType",
    "StackStatusType",
    "StackUpdateCompleteWaiterName",
    "TemplateStageType",
    "ThirdPartyTypeType",
    "TypeRegistrationCompleteWaiterName",
    "TypeTestsStatusType",
    "VersionBumpType",
    "VisibilityType",
    "ServiceName",
)


AccountGateStatusType = Literal["FAILED", "SKIPPED", "SUCCEEDED"]
CallAsType = Literal["DELEGATED_ADMIN", "SELF"]
CapabilityType = Literal["CAPABILITY_AUTO_EXPAND", "CAPABILITY_IAM", "CAPABILITY_NAMED_IAM"]
CategoryType = Literal["ACTIVATED", "AWS_TYPES", "REGISTERED", "THIRD_PARTY"]
ChangeActionType = Literal["Add", "Dynamic", "Import", "Modify", "Remove"]
ChangeSetCreateCompleteWaiterName = Literal["change_set_create_complete"]
ChangeSetStatusType = Literal[
    "CREATE_COMPLETE",
    "CREATE_IN_PROGRESS",
    "CREATE_PENDING",
    "DELETE_COMPLETE",
    "DELETE_FAILED",
    "DELETE_IN_PROGRESS",
    "DELETE_PENDING",
    "FAILED",
]
ChangeSetTypeType = Literal["CREATE", "IMPORT", "UPDATE"]
ChangeSourceType = Literal[
    "Automatic",
    "DirectModification",
    "ParameterReference",
    "ResourceAttribute",
    "ResourceReference",
]
ChangeTypeType = Literal["Resource"]
DeprecatedStatusType = Literal["DEPRECATED", "LIVE"]
DescribeAccountLimitsPaginatorName = Literal["describe_account_limits"]
DescribeChangeSetPaginatorName = Literal["describe_change_set"]
DescribeStackEventsPaginatorName = Literal["describe_stack_events"]
DescribeStacksPaginatorName = Literal["describe_stacks"]
DifferenceTypeType = Literal["ADD", "NOT_EQUAL", "REMOVE"]
EvaluationTypeType = Literal["Dynamic", "Static"]
ExecutionStatusType = Literal[
    "AVAILABLE",
    "EXECUTE_COMPLETE",
    "EXECUTE_FAILED",
    "EXECUTE_IN_PROGRESS",
    "OBSOLETE",
    "UNAVAILABLE",
]
HandlerErrorCodeType = Literal[
    "AccessDenied",
    "AlreadyExists",
    "GeneralServiceException",
    "InternalFailure",
    "InvalidCredentials",
    "InvalidRequest",
    "InvalidTypeConfiguration",
    "NetworkFailure",
    "NotFound",
    "NotStabilized",
    "NotUpdatable",
    "ResourceConflict",
    "ServiceInternalError",
    "ServiceLimitExceeded",
    "Throttling",
]
IdentityProviderType = Literal["AWS_Marketplace", "Bitbucket", "GitHub"]
ListChangeSetsPaginatorName = Literal["list_change_sets"]
ListExportsPaginatorName = Literal["list_exports"]
ListImportsPaginatorName = Literal["list_imports"]
ListStackInstancesPaginatorName = Literal["list_stack_instances"]
ListStackResourcesPaginatorName = Literal["list_stack_resources"]
ListStackSetOperationResultsPaginatorName = Literal["list_stack_set_operation_results"]
ListStackSetOperationsPaginatorName = Literal["list_stack_set_operations"]
ListStackSetsPaginatorName = Literal["list_stack_sets"]
ListStacksPaginatorName = Literal["list_stacks"]
ListTypesPaginatorName = Literal["list_types"]
OnFailureType = Literal["DELETE", "DO_NOTHING", "ROLLBACK"]
OperationStatusType = Literal["FAILED", "IN_PROGRESS", "PENDING", "SUCCESS"]
PermissionModelsType = Literal["SELF_MANAGED", "SERVICE_MANAGED"]
ProvisioningTypeType = Literal["FULLY_MUTABLE", "IMMUTABLE", "NON_PROVISIONABLE"]
PublisherStatusType = Literal["UNVERIFIED", "VERIFIED"]
RegionConcurrencyTypeType = Literal["PARALLEL", "SEQUENTIAL"]
RegistrationStatusType = Literal["COMPLETE", "FAILED", "IN_PROGRESS"]
RegistryTypeType = Literal["MODULE", "RESOURCE"]
ReplacementType = Literal["Conditional", "False", "True"]
RequiresRecreationType = Literal["Always", "Conditionally", "Never"]
ResourceAttributeType = Literal[
    "CreationPolicy", "DeletionPolicy", "Metadata", "Properties", "Tags", "UpdatePolicy"
]
ResourceSignalStatusType = Literal["FAILURE", "SUCCESS"]
ResourceStatusType = Literal[
    "CREATE_COMPLETE",
    "CREATE_FAILED",
    "CREATE_IN_PROGRESS",
    "DELETE_COMPLETE",
    "DELETE_FAILED",
    "DELETE_IN_PROGRESS",
    "DELETE_SKIPPED",
    "IMPORT_COMPLETE",
    "IMPORT_FAILED",
    "IMPORT_IN_PROGRESS",
    "IMPORT_ROLLBACK_COMPLETE",
    "IMPORT_ROLLBACK_FAILED",
    "IMPORT_ROLLBACK_IN_PROGRESS",
    "ROLLBACK_COMPLETE",
    "ROLLBACK_FAILED",
    "ROLLBACK_IN_PROGRESS",
    "UPDATE_COMPLETE",
    "UPDATE_COMPLETE_CLEANUP_IN_PROGRESS",
    "UPDATE_FAILED",
    "UPDATE_IN_PROGRESS",
    "UPDATE_ROLLBACK_COMPLETE",
    "UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS",
    "UPDATE_ROLLBACK_FAILED",
    "UPDATE_ROLLBACK_IN_PROGRESS",
]
StackCreateCompleteWaiterName = Literal["stack_create_complete"]
StackDeleteCompleteWaiterName = Literal["stack_delete_complete"]
StackDriftDetectionStatusType = Literal[
    "DETECTION_COMPLETE", "DETECTION_FAILED", "DETECTION_IN_PROGRESS"
]
StackDriftStatusType = Literal["DRIFTED", "IN_SYNC", "NOT_CHECKED", "UNKNOWN"]
StackExistsWaiterName = Literal["stack_exists"]
StackImportCompleteWaiterName = Literal["stack_import_complete"]
StackInstanceDetailedStatusType = Literal[
    "CANCELLED", "FAILED", "INOPERABLE", "PENDING", "RUNNING", "SUCCEEDED"
]
StackInstanceFilterNameType = Literal["DETAILED_STATUS"]
StackInstanceStatusType = Literal["CURRENT", "INOPERABLE", "OUTDATED"]
StackResourceDriftStatusType = Literal["DELETED", "IN_SYNC", "MODIFIED", "NOT_CHECKED"]
StackRollbackCompleteWaiterName = Literal["stack_rollback_complete"]
StackSetDriftDetectionStatusType = Literal[
    "COMPLETED", "FAILED", "IN_PROGRESS", "PARTIAL_SUCCESS", "STOPPED"
]
StackSetDriftStatusType = Literal["DRIFTED", "IN_SYNC", "NOT_CHECKED"]
StackSetOperationActionType = Literal["CREATE", "DELETE", "DETECT_DRIFT", "UPDATE"]
StackSetOperationResultStatusType = Literal[
    "CANCELLED", "FAILED", "PENDING", "RUNNING", "SUCCEEDED"
]
StackSetOperationStatusType = Literal[
    "FAILED", "QUEUED", "RUNNING", "STOPPED", "STOPPING", "SUCCEEDED"
]
StackSetStatusType = Literal["ACTIVE", "DELETED"]
StackStatusType = Literal[
    "CREATE_COMPLETE",
    "CREATE_FAILED",
    "CREATE_IN_PROGRESS",
    "DELETE_COMPLETE",
    "DELETE_FAILED",
    "DELETE_IN_PROGRESS",
    "IMPORT_COMPLETE",
    "IMPORT_IN_PROGRESS",
    "IMPORT_ROLLBACK_COMPLETE",
    "IMPORT_ROLLBACK_FAILED",
    "IMPORT_ROLLBACK_IN_PROGRESS",
    "REVIEW_IN_PROGRESS",
    "ROLLBACK_COMPLETE",
    "ROLLBACK_FAILED",
    "ROLLBACK_IN_PROGRESS",
    "UPDATE_COMPLETE",
    "UPDATE_COMPLETE_CLEANUP_IN_PROGRESS",
    "UPDATE_FAILED",
    "UPDATE_IN_PROGRESS",
    "UPDATE_ROLLBACK_COMPLETE",
    "UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS",
    "UPDATE_ROLLBACK_FAILED",
    "UPDATE_ROLLBACK_IN_PROGRESS",
]
StackUpdateCompleteWaiterName = Literal["stack_update_complete"]
TemplateStageType = Literal["Original", "Processed"]
ThirdPartyTypeType = Literal["MODULE", "RESOURCE"]
TypeRegistrationCompleteWaiterName = Literal["type_registration_complete"]
TypeTestsStatusType = Literal["FAILED", "IN_PROGRESS", "NOT_TESTED", "PASSED"]
VersionBumpType = Literal["MAJOR", "MINOR"]
VisibilityType = Literal["PRIVATE", "PUBLIC"]
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
