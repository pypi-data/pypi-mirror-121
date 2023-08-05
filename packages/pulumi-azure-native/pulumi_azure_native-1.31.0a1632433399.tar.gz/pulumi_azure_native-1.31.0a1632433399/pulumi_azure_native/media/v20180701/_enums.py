# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AacAudioProfile',
    'AnalysisResolution',
    'AssetContainerPermission',
    'ContentKeyPolicyFairPlayRentalAndLeaseKeyType',
    'ContentKeyPolicyPlayReadyContentType',
    'ContentKeyPolicyPlayReadyLicenseType',
    'ContentKeyPolicyPlayReadyUnknownOutputPassingOption',
    'ContentKeyPolicyRestrictionTokenType',
    'DeinterlaceMode',
    'DeinterlaceParity',
    'EncoderNamedPreset',
    'EntropyMode',
    'FilterTrackPropertyCompareOperation',
    'FilterTrackPropertyType',
    'H264Complexity',
    'H264VideoProfile',
    'InsightsType',
    'LiveEventEncodingType',
    'LiveEventInputProtocol',
    'OnErrorType',
    'Priority',
    'Rotation',
    'StorageAccountType',
    'StreamOptionsFlag',
    'StretchMode',
    'TrackPropertyCompareOperation',
    'TrackPropertyType',
]


class AacAudioProfile(str, Enum):
    """
    The encoding profile to be used when encoding audio with AAC.
    """
    AAC_LC = "AacLc"
    """Specifies that the output audio is to be encoded into AAC Low Complexity profile (AAC-LC)."""
    HE_AAC_V1 = "HeAacV1"
    """Specifies that the output audio is to be encoded into HE-AAC v1 profile."""
    HE_AAC_V2 = "HeAacV2"
    """Specifies that the output audio is to be encoded into HE-AAC v2 profile."""


class AnalysisResolution(str, Enum):
    """
    Specifies the maximum resolution at which your video is analyzed. The default behavior is "SourceResolution," which will keep the input video at its original resolution when analyzed. Using "StandardDefinition" will resize input videos to standard definition while preserving the appropriate aspect ratio. It will only resize if the video is of higher resolution. For example, a 1920x1080 input would be scaled to 640x360 before processing. Switching to "StandardDefinition" will reduce the time it takes to process high resolution video. It may also reduce the cost of using this component (see https://azure.microsoft.com/en-us/pricing/details/media-services/#analytics for details). However, faces that end up being too small in the resized video may not be detected.
    """
    SOURCE_RESOLUTION = "SourceResolution"
    STANDARD_DEFINITION = "StandardDefinition"


class AssetContainerPermission(str, Enum):
    """
    The permissions to set on the SAS URL.
    """
    READ = "Read"
    """The SAS URL will allow read access to the container."""
    READ_WRITE = "ReadWrite"
    """The SAS URL will allow read and write access to the container."""
    READ_WRITE_DELETE = "ReadWriteDelete"
    """The SAS URL will allow read, write and delete access to the container."""


class ContentKeyPolicyFairPlayRentalAndLeaseKeyType(str, Enum):
    """
    The rental and lease key type.
    """
    UNKNOWN = "Unknown"
    """Represents a ContentKeyPolicyFairPlayRentalAndLeaseKeyType that is unavailable in current API version."""
    UNDEFINED = "Undefined"
    """Key duration is not specified."""
    DUAL_EXPIRY = "DualExpiry"
    """Dual expiry for offline rental."""
    PERSISTENT_UNLIMITED = "PersistentUnlimited"
    """Content key can be persisted with an unlimited duration"""
    PERSISTENT_LIMITED = "PersistentLimited"
    """Content key can be persisted and the valid duration is limited by the Rental Duration value"""


class ContentKeyPolicyPlayReadyContentType(str, Enum):
    """
    The PlayReady content type.
    """
    UNKNOWN = "Unknown"
    """Represents a ContentKeyPolicyPlayReadyContentType that is unavailable in current API version."""
    UNSPECIFIED = "Unspecified"
    """Unspecified content type."""
    ULTRA_VIOLET_DOWNLOAD = "UltraVioletDownload"
    """Ultraviolet download content type."""
    ULTRA_VIOLET_STREAMING = "UltraVioletStreaming"
    """Ultraviolet streaming content type."""


class ContentKeyPolicyPlayReadyLicenseType(str, Enum):
    """
    The license type.
    """
    UNKNOWN = "Unknown"
    """Represents a ContentKeyPolicyPlayReadyLicenseType that is unavailable in current API version."""
    NON_PERSISTENT = "NonPersistent"
    """Non persistent license."""
    PERSISTENT = "Persistent"
    """Persistent license. Allows offline playback."""


class ContentKeyPolicyPlayReadyUnknownOutputPassingOption(str, Enum):
    """
    Configures Unknown output handling settings of the license.
    """
    UNKNOWN = "Unknown"
    """Represents a ContentKeyPolicyPlayReadyUnknownOutputPassingOption that is unavailable in current API version."""
    NOT_ALLOWED = "NotAllowed"
    """Passing the video portion of protected content to an Unknown Output is not allowed."""
    ALLOWED = "Allowed"
    """Passing the video portion of protected content to an Unknown Output is allowed."""
    ALLOWED_WITH_VIDEO_CONSTRICTION = "AllowedWithVideoConstriction"
    """Passing the video portion of protected content to an Unknown Output is allowed but with constrained resolution."""


class ContentKeyPolicyRestrictionTokenType(str, Enum):
    """
    The type of token.
    """
    UNKNOWN = "Unknown"
    """Represents a ContentKeyPolicyRestrictionTokenType that is unavailable in current API version."""
    SWT = "Swt"
    """Simple Web Token."""
    JWT = "Jwt"
    """JSON Web Token."""


class DeinterlaceMode(str, Enum):
    """
    The deinterlacing mode. Defaults to AutoPixelAdaptive.
    """
    OFF = "Off"
    """Disables de-interlacing of the source video."""
    AUTO_PIXEL_ADAPTIVE = "AutoPixelAdaptive"
    """Apply automatic pixel adaptive de-interlacing on each frame in the input video."""


class DeinterlaceParity(str, Enum):
    """
    The field parity for de-interlacing, defaults to Auto.
    """
    AUTO = "Auto"
    """Automatically detect the order of fields"""
    TOP_FIELD_FIRST = "TopFieldFirst"
    """Apply top field first processing of input video."""
    BOTTOM_FIELD_FIRST = "BottomFieldFirst"
    """Apply bottom field first processing of input video."""


class EncoderNamedPreset(str, Enum):
    """
    The built-in preset to be used for encoding videos.
    """
    H264_SINGLE_BITRATE_SD = "H264SingleBitrateSD"
    """Produces an MP4 file where the video is encoded with H.264 codec at 2200 kbps and a picture height of 480 pixels, and the stereo audio is encoded with AAC-LC codec at 64 kbps."""
    H264_SINGLE_BITRATE720P = "H264SingleBitrate720p"
    """Produces an MP4 file where the video is encoded with H.264 codec at 4500 kbps and a picture height of 720 pixels, and the stereo audio is encoded with AAC-LC codec at 64 kbps."""
    H264_SINGLE_BITRATE1080P = "H264SingleBitrate1080p"
    """Produces an MP4 file where the video is encoded with H.264 codec at 6750 kbps and a picture height of 1080 pixels, and the stereo audio is encoded with AAC-LC codec at 64 kbps."""
    ADAPTIVE_STREAMING = "AdaptiveStreaming"
    """Produces a set of GOP aligned MP4 files with H.264 video and stereo AAC audio. Auto-generates a bitrate ladder based on the input resolution and bitrate. The auto-generated preset will never exceed the input resolution and bitrate. For example, if the input is 720p at 3 Mbps, output will remain 720p at best, and will start at rates lower than 3 Mbps. The output will have video and audio in separate MP4 files, which is optimal for adaptive streaming."""
    AAC_GOOD_QUALITY_AUDIO = "AACGoodQualityAudio"
    """Produces a single MP4 file containing only stereo audio encoded at 192 kbps."""
    CONTENT_AWARE_ENCODING_EXPERIMENTAL = "ContentAwareEncodingExperimental"
    """Exposes an experimental preset for content-aware encoding. Given any input content, the service attempts to automatically determine the optimal number of layers, appropriate bitrate and resolution settings for delivery by adaptive streaming. The underlying algorithms will continue to evolve over time. The output will contain MP4 files with video and audio interleaved."""
    CONTENT_AWARE_ENCODING = "ContentAwareEncoding"
    """Produces a set of GOP-aligned MP4s by using content-aware encoding. Given any input content, the service performs an initial lightweight analysis of the input content, and uses the results to determine the optimal number of layers, appropriate bitrate and resolution settings for delivery by adaptive streaming. This preset is particularly effective for low and medium complexity videos, where the output files will be at lower bitrates but at a quality that still delivers a good experience to viewers. The output will contain MP4 files with video and audio interleaved."""
    H264_MULTIPLE_BITRATE1080P = "H264MultipleBitrate1080p"
    """Produces a set of 8 GOP-aligned MP4 files, ranging from 6000 kbps to 400 kbps, and stereo AAC audio. Resolution starts at 1080p and goes down to 360p."""
    H264_MULTIPLE_BITRATE720P = "H264MultipleBitrate720p"
    """Produces a set of 6 GOP-aligned MP4 files, ranging from 3400 kbps to 400 kbps, and stereo AAC audio. Resolution starts at 720p and goes down to 360p."""
    H264_MULTIPLE_BITRATE_SD = "H264MultipleBitrateSD"
    """Produces a set of 5 GOP-aligned MP4 files, ranging from 1600kbps to 400 kbps, and stereo AAC audio. Resolution starts at 480p and goes down to 360p."""


class EntropyMode(str, Enum):
    """
    The entropy mode to be used for this layer. If not specified, the encoder chooses the mode that is appropriate for the profile and level.
    """
    CABAC = "Cabac"
    """Context Adaptive Binary Arithmetic Coder (CABAC) entropy encoding."""
    CAVLC = "Cavlc"
    """Context Adaptive Variable Length Coder (CAVLC) entropy encoding."""


class FilterTrackPropertyCompareOperation(str, Enum):
    """
    The track property condition operation.
    """
    EQUAL = "Equal"
    """The equal operation."""
    NOT_EQUAL = "NotEqual"
    """The not equal operation."""


class FilterTrackPropertyType(str, Enum):
    """
    The track property type.
    """
    UNKNOWN = "Unknown"
    """The unknown track property type."""
    TYPE = "Type"
    """The type."""
    NAME = "Name"
    """The name."""
    LANGUAGE = "Language"
    """The language."""
    FOUR_CC = "FourCC"
    """The fourCC."""
    BITRATE = "Bitrate"
    """The bitrate."""


class H264Complexity(str, Enum):
    """
    Tells the encoder how to choose its encoding settings. The default value is Balanced.
    """
    SPEED = "Speed"
    """Tells the encoder to use settings that are optimized for faster encoding. Quality is sacrificed to decrease encoding time."""
    BALANCED = "Balanced"
    """Tells the encoder to use settings that achieve a balance between speed and quality."""
    QUALITY = "Quality"
    """Tells the encoder to use settings that are optimized to produce higher quality output at the expense of slower overall encode time."""


class H264VideoProfile(str, Enum):
    """
    We currently support Baseline, Main, High, High422, High444. Default is Auto.
    """
    AUTO = "Auto"
    """Tells the encoder to automatically determine the appropriate H.264 profile."""
    BASELINE = "Baseline"
    """Baseline profile"""
    MAIN = "Main"
    """Main profile"""
    HIGH = "High"
    """High profile."""
    HIGH422 = "High422"
    """High 4:2:2 profile."""
    HIGH444 = "High444"
    """High 4:4:4 predictive profile."""


class InsightsType(str, Enum):
    """
    Defines the type of insights that you want the service to generate. The allowed values are 'AudioInsightsOnly', 'VideoInsightsOnly', and 'AllInsights'. The default is AllInsights. If you set this to AllInsights and the input is audio only, then only audio insights are generated. Similarly if the input is video only, then only video insights are generated. It is recommended that you not use AudioInsightsOnly if you expect some of your inputs to be video only; or use VideoInsightsOnly if you expect some of your inputs to be audio only. Your Jobs in such conditions would error out.
    """
    AUDIO_INSIGHTS_ONLY = "AudioInsightsOnly"
    """Generate audio only insights. Ignore video even if present. Fails if no audio is present."""
    VIDEO_INSIGHTS_ONLY = "VideoInsightsOnly"
    """Generate video only insights. Ignore audio if present. Fails if no video is present."""
    ALL_INSIGHTS = "AllInsights"
    """Generate both audio and video insights. Fails if either audio or video Insights fail."""


class LiveEventEncodingType(str, Enum):
    """
    The encoding type for Live Event.  This value is specified at creation time and cannot be updated.
    """
    NONE = "None"
    BASIC = "Basic"
    STANDARD = "Standard"
    PREMIUM1080P = "Premium1080p"


class LiveEventInputProtocol(str, Enum):
    """
    The streaming protocol for the Live Event.  This is specified at creation time and cannot be updated.
    """
    FRAGMENTED_MP4 = "FragmentedMP4"
    RTMP = "RTMP"


class OnErrorType(str, Enum):
    """
    A Transform can define more than one outputs. This property defines what the service should do when one output fails - either continue to produce other outputs, or, stop the other outputs. The overall Job state will not reflect failures of outputs that are specified with 'ContinueJob'. The default is 'StopProcessingJob'.
    """
    STOP_PROCESSING_JOB = "StopProcessingJob"
    """Tells the service that if this TransformOutput fails, then any other incomplete TransformOutputs can be stopped."""
    CONTINUE_JOB = "ContinueJob"
    """Tells the service that if this TransformOutput fails, then allow any other TransformOutput to continue."""


class Priority(str, Enum):
    """
    Sets the relative priority of the TransformOutputs within a Transform. This sets the priority that the service uses for processing TransformOutputs. The default priority is Normal.
    """
    LOW = "Low"
    """Used for TransformOutputs that can be generated after Normal and High priority TransformOutputs."""
    NORMAL = "Normal"
    """Used for TransformOutputs that can be generated at Normal priority."""
    HIGH = "High"
    """Used for TransformOutputs that should take precedence over others."""


class Rotation(str, Enum):
    """
    The rotation, if any, to be applied to the input video, before it is encoded. Default is Auto
    """
    AUTO = "Auto"
    """Automatically detect and rotate as needed."""
    NONE = "None"
    """Do not rotate the video.  If the output format supports it, any metadata about rotation is kept intact."""
    ROTATE0 = "Rotate0"
    """Do not rotate the video but remove any metadata about the rotation."""
    ROTATE90 = "Rotate90"
    """Rotate 90 degrees clockwise."""
    ROTATE180 = "Rotate180"
    """Rotate 180 degrees clockwise."""
    ROTATE270 = "Rotate270"
    """Rotate 270 degrees clockwise."""


class StorageAccountType(str, Enum):
    """
    The type of the storage account.
    """
    PRIMARY = "Primary"
    """The primary storage account for the Media Services account."""
    SECONDARY = "Secondary"
    """A secondary storage account for the Media Services account."""


class StreamOptionsFlag(str, Enum):
    DEFAULT = "Default"
    LOW_LATENCY = "LowLatency"


class StretchMode(str, Enum):
    """
    The resizing mode - how the input video will be resized to fit the desired output resolution(s). Default is AutoSize
    """
    NONE = "None"
    """Strictly respect the output resolution without considering the pixel aspect ratio or display aspect ratio of the input video."""
    AUTO_SIZE = "AutoSize"
    """Override the output resolution, and change it to match the display aspect ratio of the input, without padding. For example, if the input is 1920x1080 and the encoding preset asks for 1280x1280, then the value in the preset is overridden, and the output will be at 1280x720, which maintains the input aspect ratio of 16:9."""
    AUTO_FIT = "AutoFit"
    """Pad the output (with either letterbox or pillar box) to honor the output resolution, while ensuring that the active video region in the output has the same aspect ratio as the input. For example, if the input is 1920x1080 and the encoding preset asks for 1280x1280, then the output will be at 1280x1280, which contains an inner rectangle of 1280x720 at aspect ratio of 16:9, and pillar box regions 280 pixels wide at the left and right."""


class TrackPropertyCompareOperation(str, Enum):
    """
    Track property condition operation
    """
    UNKNOWN = "Unknown"
    """Unknown track property compare operation"""
    EQUAL = "Equal"
    """Equal operation"""


class TrackPropertyType(str, Enum):
    """
    Track property type
    """
    UNKNOWN = "Unknown"
    """Unknown track property"""
    FOUR_CC = "FourCC"
    """Track FourCC"""
