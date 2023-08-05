# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

try:
    from ._models_py3 import BlobDetails
    from ._models_py3 import ErrorData
    from ._models_py3 import JobDetails
    from ._models_py3 import JobDetailsList
    from ._models_py3 import ProviderStatus
    from ._models_py3 import ProviderStatusList
    from ._models_py3 import Quota
    from ._models_py3 import QuotaList
    from ._models_py3 import RestError
    from ._models_py3 import SasUriResponse
    from ._models_py3 import TargetStatus
except (SyntaxError, ImportError):
    from ._models import BlobDetails  # type: ignore
    from ._models import ErrorData  # type: ignore
    from ._models import JobDetails  # type: ignore
    from ._models import JobDetailsList  # type: ignore
    from ._models import ProviderStatus  # type: ignore
    from ._models import ProviderStatusList  # type: ignore
    from ._models import Quota  # type: ignore
    from ._models import QuotaList  # type: ignore
    from ._models import RestError  # type: ignore
    from ._models import SasUriResponse  # type: ignore
    from ._models import TargetStatus  # type: ignore

from ._quantum_client_enums import (
    DimensionScope,
    JobStatus,
    MeterPeriod,
    ProviderAvailability,
    TargetAvailability,
)

__all__ = [
    'BlobDetails',
    'ErrorData',
    'JobDetails',
    'JobDetailsList',
    'ProviderStatus',
    'ProviderStatusList',
    'Quota',
    'QuotaList',
    'RestError',
    'SasUriResponse',
    'TargetStatus',
    'DimensionScope',
    'JobStatus',
    'MeterPeriod',
    'ProviderAvailability',
    'TargetAvailability',
]
