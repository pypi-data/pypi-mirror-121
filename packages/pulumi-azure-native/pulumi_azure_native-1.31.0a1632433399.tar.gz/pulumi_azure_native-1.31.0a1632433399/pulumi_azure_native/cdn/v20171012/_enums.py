# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'GeoFilterActions',
    'OptimizationType',
    'QueryStringCachingBehavior',
    'SkuName',
]


class GeoFilterActions(str, Enum):
    """
    Action of the geo filter, i.e. allow or block access.
    """
    BLOCK = "Block"
    ALLOW = "Allow"


class OptimizationType(str, Enum):
    """
    Specifies what scenario the customer wants this CDN endpoint to optimize for, e.g. Download, Media services. With this information, CDN can apply scenario driven optimization.
    """
    GENERAL_WEB_DELIVERY = "GeneralWebDelivery"
    GENERAL_MEDIA_STREAMING = "GeneralMediaStreaming"
    VIDEO_ON_DEMAND_MEDIA_STREAMING = "VideoOnDemandMediaStreaming"
    LARGE_FILE_DOWNLOAD = "LargeFileDownload"
    DYNAMIC_SITE_ACCELERATION = "DynamicSiteAcceleration"


class QueryStringCachingBehavior(str, Enum):
    """
    Defines how CDN caches requests that include query strings. You can ignore any query strings when caching, bypass caching to prevent requests that contain query strings from being cached, or cache every request with a unique URL.
    """
    IGNORE_QUERY_STRING = "IgnoreQueryString"
    BYPASS_CACHING = "BypassCaching"
    USE_QUERY_STRING = "UseQueryString"
    NOT_SET = "NotSet"


class SkuName(str, Enum):
    """
    Name of the pricing tier.
    """
    STANDARD_VERIZON = "Standard_Verizon"
    PREMIUM_VERIZON = "Premium_Verizon"
    CUSTOM_VERIZON = "Custom_Verizon"
    STANDARD_AKAMAI = "Standard_Akamai"
    STANDARD_CHINA_CDN = "Standard_ChinaCdn"
    PREMIUM_CHINA_CDN = "Premium_ChinaCdn"
    STANDARD_MICROSOFT = "Standard_Microsoft"
