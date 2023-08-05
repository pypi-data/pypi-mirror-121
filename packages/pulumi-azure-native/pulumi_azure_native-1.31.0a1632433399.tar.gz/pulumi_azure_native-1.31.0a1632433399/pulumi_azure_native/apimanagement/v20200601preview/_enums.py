# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AlwaysLog',
    'ApiType',
    'ApimIdentityType',
    'AppType',
    'AuthorizationMethod',
    'BackendProtocol',
    'BearerTokenSendingMethod',
    'BearerTokenSendingMethods',
    'ClientAuthenticationMethod',
    'Confirmation',
    'ContentFormat',
    'DataMaskingMode',
    'GrantType',
    'GroupType',
    'HostnameType',
    'HttpCorrelationProtocol',
    'IdentityProviderType',
    'KeyType',
    'LoggerType',
    'OperationNameFormat',
    'PolicyContentFormat',
    'ProductState',
    'Protocol',
    'ProvisioningState',
    'SamplingType',
    'SkuType',
    'SoapApiType',
    'State',
    'SubscriptionState',
    'UserState',
    'Verbosity',
    'VersioningScheme',
    'VirtualNetworkType',
]


class AlwaysLog(str, Enum):
    """
    Specifies for what type of messages sampling settings should not apply.
    """
    ALL_ERRORS = "allErrors"
    """Always log all erroneous request regardless of sampling settings."""


class ApiType(str, Enum):
    """
    Type of API.
    """
    HTTP = "http"
    SOAP = "soap"


class ApimIdentityType(str, Enum):
    """
    The type of identity used for the resource. The type 'SystemAssigned, UserAssigned' includes both an implicitly created identity and a set of user assigned identities. The type 'None' will remove any identities from the service.
    """
    SYSTEM_ASSIGNED = "SystemAssigned"
    USER_ASSIGNED = "UserAssigned"
    SYSTEM_ASSIGNED_USER_ASSIGNED = "SystemAssigned, UserAssigned"
    NONE = "None"


class AppType(str, Enum):
    """
    Determines the type of application which send the create user request. Default is legacy portal.
    """
    PORTAL = "portal"
    """User create request was sent by legacy developer portal."""
    DEVELOPER_PORTAL = "developerPortal"
    """User create request was sent by new developer portal."""


class AuthorizationMethod(str, Enum):
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class BackendProtocol(str, Enum):
    """
    Backend communication protocol.
    """
    HTTP = "http"
    """The Backend is a RESTful service."""
    SOAP = "soap"
    """The Backend is a SOAP service."""


class BearerTokenSendingMethod(str, Enum):
    AUTHORIZATION_HEADER = "authorizationHeader"
    QUERY = "query"


class BearerTokenSendingMethods(str, Enum):
    """
    Form of an authorization grant, which the client uses to request the access token.
    """
    AUTHORIZATION_HEADER = "authorizationHeader"
    """Access token will be transmitted in the Authorization header using Bearer schema"""
    QUERY = "query"
    """Access token will be transmitted as query parameters."""


class ClientAuthenticationMethod(str, Enum):
    BASIC = "Basic"
    """Basic Client Authentication method."""
    BODY = "Body"
    """Body based Authentication method."""


class Confirmation(str, Enum):
    """
    Determines the type of confirmation e-mail that will be sent to the newly created user.
    """
    SIGNUP = "signup"
    """Send an e-mail to the user confirming they have successfully signed up."""
    INVITE = "invite"
    """Send an e-mail inviting the user to sign-up and complete registration."""


class ContentFormat(str, Enum):
    """
    Format of the Content in which the API is getting imported.
    """
    WADL_XML = "wadl-xml"
    """The contents are inline and Content type is a WADL document."""
    WADL_LINK_JSON = "wadl-link-json"
    """The WADL document is hosted on a publicly accessible internet address."""
    SWAGGER_JSON = "swagger-json"
    """The contents are inline and Content Type is a OpenAPI 2.0 JSON Document."""
    SWAGGER_LINK_JSON = "swagger-link-json"
    """The OpenAPI 2.0 JSON document is hosted on a publicly accessible internet address."""
    WSDL = "wsdl"
    """The contents are inline and the document is a WSDL/Soap document."""
    WSDL_LINK = "wsdl-link"
    """The WSDL document is hosted on a publicly accessible internet address."""
    OPENAPI = "openapi"
    """The contents are inline and Content Type is a OpenAPI 3.0 YAML Document."""
    OPENAPI_JSON = "openapi+json"
    """The contents are inline and Content Type is a OpenAPI 3.0 JSON Document."""
    OPENAPI_LINK = "openapi-link"
    """The OpenAPI 3.0 YAML document is hosted on a publicly accessible internet address."""
    OPENAPI_JSON_LINK = "openapi+json-link"
    """The OpenAPI 3.0 JSON document is hosted on a publicly accessible internet address."""


class DataMaskingMode(str, Enum):
    """
    Data masking mode.
    """
    MASK = "Mask"
    """Mask the value of an entity."""
    HIDE = "Hide"
    """Hide the presence of an entity."""


class GrantType(str, Enum):
    AUTHORIZATION_CODE = "authorizationCode"
    """Authorization Code Grant flow as described https://tools.ietf.org/html/rfc6749#section-4.1."""
    IMPLICIT = "implicit"
    """Implicit Code Grant flow as described https://tools.ietf.org/html/rfc6749#section-4.2."""
    RESOURCE_OWNER_PASSWORD = "resourceOwnerPassword"
    """Resource Owner Password Grant flow as described https://tools.ietf.org/html/rfc6749#section-4.3."""
    CLIENT_CREDENTIALS = "clientCredentials"
    """Client Credentials Grant flow as described https://tools.ietf.org/html/rfc6749#section-4.4."""


class GroupType(str, Enum):
    """
    Group type.
    """
    CUSTOM = "custom"
    SYSTEM = "system"
    EXTERNAL = "external"


class HostnameType(str, Enum):
    """
    Hostname type.
    """
    PROXY = "Proxy"
    PORTAL = "Portal"
    MANAGEMENT = "Management"
    SCM = "Scm"
    DEVELOPER_PORTAL = "DeveloperPortal"


class HttpCorrelationProtocol(str, Enum):
    """
    Sets correlation protocol to use for Application Insights diagnostics.
    """
    NONE = "None"
    """Do not read and inject correlation headers."""
    LEGACY = "Legacy"
    """Inject Request-Id and Request-Context headers with request correlation data. See https://github.com/dotnet/corefx/blob/master/src/System.Diagnostics.DiagnosticSource/src/HttpCorrelationProtocol.md."""
    W3_C = "W3C"
    """Inject Trace Context headers. See https://w3c.github.io/trace-context."""


class IdentityProviderType(str, Enum):
    """
    Identity Provider Type identifier.
    """
    FACEBOOK = "facebook"
    """Facebook as Identity provider."""
    GOOGLE = "google"
    """Google as Identity provider."""
    MICROSOFT = "microsoft"
    """Microsoft Live as Identity provider."""
    TWITTER = "twitter"
    """Twitter as Identity provider."""
    AAD = "aad"
    """Azure Active Directory as Identity provider."""
    AAD_B2_C = "aadB2C"
    """Azure Active Directory B2C as Identity provider."""


class KeyType(str, Enum):
    """
    The Key to be used to generate token for user.
    """
    PRIMARY = "primary"
    SECONDARY = "secondary"


class LoggerType(str, Enum):
    """
    Logger type.
    """
    AZURE_EVENT_HUB = "azureEventHub"
    """Azure Event Hub as log destination."""
    APPLICATION_INSIGHTS = "applicationInsights"
    """Azure Application Insights as log destination."""
    AZURE_MONITOR = "azureMonitor"
    """Azure Monitor"""


class OperationNameFormat(str, Enum):
    """
    The format of the Operation Name for Application Insights telemetries. Default is Name.
    """
    NAME = "Name"
    """API_NAME;rev=API_REVISION - OPERATION_NAME"""
    URL = "Url"
    """HTTP_VERB URL"""


class PolicyContentFormat(str, Enum):
    """
    Format of the policyContent.
    """
    XML = "xml"
    """The contents are inline and Content type is an XML document."""
    XML_LINK = "xml-link"
    """The policy XML document is hosted on a http endpoint accessible from the API Management service."""
    RAWXML = "rawxml"
    """The contents are inline and Content type is a non XML encoded policy document."""
    RAWXML_LINK = "rawxml-link"
    """The policy document is not Xml encoded and is hosted on a http endpoint accessible from the API Management service."""


class ProductState(str, Enum):
    """
    whether product is published or not. Published products are discoverable by users of developer portal. Non published products are visible only to administrators. Default state of Product is notPublished.
    """
    NOT_PUBLISHED = "notPublished"
    PUBLISHED = "published"


class Protocol(str, Enum):
    HTTP = "http"
    HTTPS = "https"


class ProvisioningState(str, Enum):
    """
    Provisioning state.
    """
    CREATED = "created"


class SamplingType(str, Enum):
    """
    Sampling type.
    """
    FIXED = "fixed"
    """Fixed-rate sampling."""


class SkuType(str, Enum):
    """
    Name of the Sku.
    """
    DEVELOPER = "Developer"
    """Developer SKU of Api Management."""
    STANDARD = "Standard"
    """Standard SKU of Api Management."""
    PREMIUM = "Premium"
    """Premium SKU of Api Management."""
    BASIC = "Basic"
    """Basic SKU of Api Management."""
    CONSUMPTION = "Consumption"
    """Consumption SKU of Api Management."""
    ISOLATED = "Isolated"
    """Isolated SKU of Api Management."""


class SoapApiType(str, Enum):
    """
    Type of Api to create. 
     * `http` creates a SOAP to REST API 
     * `soap` creates a SOAP pass-through API .
    """
    SOAP_TO_REST = "http"
    """Imports a SOAP API having a RESTful front end."""
    SOAP_PASS_THROUGH = "soap"
    """Imports the Soap API having a SOAP front end."""


class State(str, Enum):
    """
    Status of the issue.
    """
    PROPOSED = "proposed"
    """The issue is proposed."""
    OPEN = "open"
    """The issue is opened."""
    REMOVED = "removed"
    """The issue was removed."""
    RESOLVED = "resolved"
    """The issue is now resolved."""
    CLOSED = "closed"
    """The issue was closed."""


class SubscriptionState(str, Enum):
    """
    Initial subscription state. If no value is specified, subscription is created with Submitted state. Possible states are * active – the subscription is active, * suspended – the subscription is blocked, and the subscriber cannot call any APIs of the product, * submitted – the subscription request has been made by the developer, but has not yet been approved or rejected, * rejected – the subscription request has been denied by an administrator, * cancelled – the subscription has been cancelled by the developer or administrator, * expired – the subscription reached its expiration date and was deactivated.
    """
    SUSPENDED = "suspended"
    ACTIVE = "active"
    EXPIRED = "expired"
    SUBMITTED = "submitted"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class UserState(str, Enum):
    """
    Account state. Specifies whether the user is active or not. Blocked users are unable to sign into the developer portal or call any APIs of subscribed products. Default state is Active.
    """
    ACTIVE = "active"
    """User state is active."""
    BLOCKED = "blocked"
    """User is blocked. Blocked users cannot authenticate at developer portal or call API."""
    PENDING = "pending"
    """User account is pending. Requires identity confirmation before it can be made active."""
    DELETED = "deleted"
    """User account is closed. All identities and related entities are removed."""


class Verbosity(str, Enum):
    """
    The verbosity level applied to traces emitted by trace policies.
    """
    VERBOSE = "verbose"
    """All the traces emitted by trace policies will be sent to the logger attached to this diagnostic instance."""
    INFORMATION = "information"
    """Traces with 'severity' set to 'information' and 'error' will be sent to the logger attached to this diagnostic instance."""
    ERROR = "error"
    """Only traces with 'severity' set to 'error' will be sent to the logger attached to this diagnostic instance."""


class VersioningScheme(str, Enum):
    """
    An value that determines where the API Version identifier will be located in a HTTP request.
    """
    SEGMENT = "Segment"
    """The API Version is passed in a path segment."""
    QUERY = "Query"
    """The API Version is passed in a query parameter."""
    HEADER = "Header"
    """The API Version is passed in a HTTP header."""


class VirtualNetworkType(str, Enum):
    """
    The type of VPN in which API Management service needs to be configured in. None (Default Value) means the API Management service is not part of any Virtual Network, External means the API Management deployment is set up inside a Virtual Network having an Internet Facing Endpoint, and Internal means that API Management deployment is setup inside a Virtual Network having an Intranet Facing Endpoint only.
    """
    NONE = "None"
    """The service is not part of any Virtual Network."""
    EXTERNAL = "External"
    """The service is part of Virtual Network and it is accessible from Internet."""
    INTERNAL = "Internal"
    """The service is part of Virtual Network and it is only accessible from within the virtual network."""
