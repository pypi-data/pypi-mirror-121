from typing import Any, Optional, Union
import decimal

import dataclasses

from blockbax_sdk.util import validation
from blockbax_sdk import types

import logging
logger = logging.getLogger(__name__)

@dataclasses.dataclass(eq=False)
class PropertyValue:
    # Base Property value
    id: Optional[str] = dataclasses.field(default = None)    
    caption: Optional[str] = dataclasses.field(default = None)
    inherit: Optional[bool] = dataclasses.field(default = None)
    
    _value: Any = dataclasses.field(default=None, repr=False, compare=False)

    @classmethod
    def from_dict(cls, property_value_dict: dict):
        # Get any of the subclasses that the `property_value_dict` contains, then call this classmethod as that class type
        for property_value_option in cls.__subclasses__():
            if property_value_option.get_data_type() in property_value_dict:
                return property_value_option.from_dict(property_value_dict=property_value_dict)
        
        # Create a property value either if there is a value or whenever the value is going to be inherited
        if property_value_dict.get(cls.get_data_type()) is not None or property_value_dict.get("inherit") is True:
            return cls(
                id =  property_value_dict.get("id") or  property_value_dict.get("valueId"),
                caption =  property_value_dict.get("caption"),
                inherit =  property_value_dict.get("inherit"),
                _value = property_value_dict.get(cls.get_data_type()),
            )
        # Neither a value given or indicated that the value will be inherited
        return None

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PropertyValue):           
            return other.get_value() == self.get_value() and (other.id == self.id if self.id and other.id else True)
        else:
            return self._has_value(other)

    def get_value(self) -> Optional[Union[str, dict, decimal.Decimal]]:
        return None

    @classmethod
    def get_data_type(cls) -> str:
        return ""

    def _has_value(self, value: Any) -> bool:
        return False

    def _set_value(self, new_value: Any):
        pass

    
@dataclasses.dataclass(eq=False)
class NumberPropertyValue(PropertyValue):
    number: Optional[decimal.Decimal] = dataclasses.field(default=None)

    def __post_init__(self):
        self.number = validation.check_number_and_convert_to_decimal(self.number)
    
    @classmethod
    def get_data_type(cls) -> str:
        return ""

    def get_value(self) -> Optional[Union[str, dict, decimal.Decimal]]:
        return None

    def _has_value(self, value: Any) -> bool:
        return False

    def _set_value(self, new_value: Any) -> None:
        pass

@dataclasses.dataclass(eq=False)
class NumberPropertyValue(PropertyValue):
    number: Optional[decimal.Decimal] = dataclasses.field(default=None)
    
    def __post_init__(self):
        self.number = validation.check_number_and_convert_to_decimal(self._value if self._value is not None else self.number)
        
    @classmethod
    def get_data_type(cls) -> str:
        return types.PropertyDataTypes.NUMBER.value

    def get_value(self) -> Optional[decimal.Decimal]:
        return self.number

    def _has_value(self, value: Any) -> bool:
        if isinstance(value, (int, float, decimal.Decimal)):
            return  self.number == validation.check_number_and_convert_to_decimal(value)
        return self.number == value
    
    def _set_value(self, new_value: Any):
        self.number = new_value

@dataclasses.dataclass(eq=False)
class TextPropertyValue(PropertyValue):
    text: Optional[str] = dataclasses.field(default=None)

    def __post_init__(self):
        self.text = validation.check_text(self._value if self._value is not None else self.text)
        
    @classmethod
    def get_data_type(cls) -> str:
        return types.PropertyDataTypes.TEXT.value

    def get_value(self) -> Optional[str]:
        return self.text

    def _has_value(self, value: str) -> bool:
        return self.text == value
    
    def _set_value(self, new_value: str):
        self.text = new_value

@dataclasses.dataclass(eq=False)
class LocationPropertyValue(PropertyValue):
    location: Optional[dict] = dataclasses.field(default=None)

    def __post_init__(self):
        self.location = validation.check_location_and_convert(self._value if self._value is not None else self.location)

    @classmethod
    def get_data_type(cls) -> str:
        return types.PropertyDataTypes.LOCATION.value

    def get_value(self) -> Optional[dict]:
        return self.location

    def _has_value(self, value: dict) -> bool:
        if isinstance(value, dict):
            return  self.location == validation.check_location_and_convert(value)
        return self.location == value
    
    def _set_value(self, new_value: dict):
        self.location = new_value

@dataclasses.dataclass(eq=False)
class MapLayerPropertyValue(PropertyValue):
    map_layer: Optional[dict] = dataclasses.field(default=None)

    def __post_init__(self):
        self.map_layer = validation.check_map_layer_and_convert(self._value if self._value is not None else self.map_layer)

    @classmethod
    def get_data_type(cls) -> str:
        return types.PropertyDataTypes.MAP_LAYER.value

    def get_value(self) -> Optional[dict]:
        return self.map_layer

    def _has_value(self, value: dict) -> bool:
        if isinstance(value, dict):
            return self.map_layer == validation.check_map_layer_and_convert(self.map_layer)
        return self.map_layer == value
    
    def _set_value(self, new_value: dict):
        self.map_layer = new_value

@dataclasses.dataclass(eq=False)
class ImagePropertyValue(PropertyValue):
    image: Optional[dict] = dataclasses.field(default=None)

    def __post_init__(self):
        self.image = validation.check_image(self._value if self._value is not None else self.image)

    @classmethod
    def get_data_type(cls) -> str:
        return types.PropertyDataTypes.IMAGE.value

    def get_value(self) -> Optional[dict]:
        return self.image

    def _has_value(self, value: str) -> bool:
        return self.image == value
    
    def _set_value(self, new_value: dict):
        self.image = new_value