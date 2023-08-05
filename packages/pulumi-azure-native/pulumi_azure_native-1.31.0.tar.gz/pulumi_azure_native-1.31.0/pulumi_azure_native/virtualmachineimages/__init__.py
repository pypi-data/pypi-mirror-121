# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from .. import _utilities
import typing
# Export this package's modules as members:
from ._enums import *
from .get_virtual_machine_image_template import *
from .virtual_machine_image_template import *
from ._inputs import *
from . import outputs

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_azure_native.virtualmachineimages.v20180201preview as __v20180201preview
    v20180201preview = __v20180201preview
    import pulumi_azure_native.virtualmachineimages.v20190201preview as __v20190201preview
    v20190201preview = __v20190201preview
    import pulumi_azure_native.virtualmachineimages.v20190501preview as __v20190501preview
    v20190501preview = __v20190501preview
    import pulumi_azure_native.virtualmachineimages.v20200214 as __v20200214
    v20200214 = __v20200214
else:
    v20180201preview = _utilities.lazy_import('pulumi_azure_native.virtualmachineimages.v20180201preview')
    v20190201preview = _utilities.lazy_import('pulumi_azure_native.virtualmachineimages.v20190201preview')
    v20190501preview = _utilities.lazy_import('pulumi_azure_native.virtualmachineimages.v20190501preview')
    v20200214 = _utilities.lazy_import('pulumi_azure_native.virtualmachineimages.v20200214')

