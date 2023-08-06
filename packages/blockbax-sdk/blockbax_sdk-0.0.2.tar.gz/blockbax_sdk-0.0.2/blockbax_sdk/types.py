import datetime
import enum
from numbers import Number
from decimal import Decimal
from typing import Literal, Union

import logging
logger = logging.getLogger(__name__)

# Generic types

AnyDate = Union[datetime.datetime, int, str]
AnyNumber = Union[int, float, Number, Decimal]

# Blockbax types

# Measurement data types

MeasurementDataTypeString = Literal["NUMBER","LOCATION"]
class MeasurementDataTypes(str, enum.Enum):
    NUMBER="number"
    LOCATION="location"
    
    @classmethod
    def _missing_(cls, value: MeasurementDataTypeString):
        return _check_missing_is_upper_name(cls, value)

MeasurementDataType = Literal[MeasurementDataTypes.NUMBER, MeasurementDataTypes.LOCATION]

# Property data types

PropertyDataTypeString = Literal["TEXT", "MAP_LAYER", "IMAGE", MeasurementDataTypeString]
class PropertyDataTypes(str, enum.Enum):
    TEXT="text"
    NUMBER="number"
    LOCATION="location"
    MAP_LAYER="mapLayer"
    IMAGE="image"
    
    @classmethod
    def _missing_(cls, value: PropertyDataTypeString):
        return _check_missing_is_upper_name(cls, value)

type_1 = PropertyDataTypes.TEXT

PropertyDataType = Literal[
    PropertyDataTypes.TEXT, 
    PropertyDataTypes.NUMBER, 
    PropertyDataTypes.LOCATION,
    PropertyDataTypes.MAP_LAYER,
    PropertyDataTypes.IMAGE,
    ]

# Primary location (Subject Type) types

PrimaryLocationTypeString = Literal["PROPERTY_TYPE", "METRIC"]   
class PrimaryLocationTypes(str, enum.Enum):
    PROPERTY_TYPE= "PROPERTY_TYPE"
    METRIC = "METRIC"
    
    @classmethod
    def _missing_(cls, value: PrimaryLocationTypeString):
        return _check_missing_is_upper_name(cls, value)

PrimaryLocationType = Literal[PrimaryLocationTypes.PROPERTY_TYPE, PrimaryLocationTypes.METRIC]

# Metric types

SupportedMetricTypeString = Literal["INGESTED"]
UnSupportedMetricTypeString = Literal["SIMULATED","CALCULATED"]
MetricTypeString = Literal[SupportedMetricTypeString, UnSupportedMetricTypeString]  
class MetricTypes(str, enum.Enum):
    INGESTED= "INGESTED"
    SIMULATED = "SIMULATED"
    CALCULATED = "CALCULATED"
    
    @classmethod
    def _missing_(cls, value: MetricTypeString):
        return _check_missing_is_upper_name(cls, value)

SupportedMetricType = Literal[MetricTypes.INGESTED]
UnSupportedMetricType = Literal[MetricTypes.SIMULATED, MetricTypes.CALCULATED]
MetricType = Literal[SupportedMetricType, UnSupportedMetricType]

# Check if given value is actually its lower counter part

AnyTypeString = Literal[PropertyDataTypeString, PrimaryLocationTypeString, MetricTypeString]
AnyType = Literal[PropertyDataType, PrimaryLocationType, MetricType]

def _check_missing_is_upper_name(cls, value: AnyTypeString):
    known_types = []
    for member in cls:
        known_types.append(member)
        if member.name == str(value).upper():
            return member
    error_unknown_type = f"'{value}' is not a known data type, known data types: {', '.join(known_types)}"
    raise ValueError(error_unknown_type)
