
from typing import Union
import decimal

from blockbax_sdk.util import validation
from blockbax_sdk  import types
from blockbax_sdk  import errors

import dataclasses

import logging
logger = logging.getLogger(__name__)

@dataclasses.dataclass
class Measurement:
    date: int
    number: decimal.Decimal = dataclasses.field(default=None)
    location: dict = dataclasses.field(default=None)
    __data_type: types.MeasurementDataType = dataclasses.field(init=False, repr=False, default=None) # private field to track data_type
    
    def __post_init__(self):
        # validation
        self.date = validation.check_date_and_convert_to_unix(self.date)
        
        has_number: bool = self.number is not None
        has_location: bool = self.location is not None
        
        if has_number and has_location or not has_number and not has_location:
            location_and_number_error = "Only one of number or location can be configured, not more than one or none"
            raise errors.MeasurementValidationError(location_and_number_error)
        
        if has_number:
            self.number = validation.check_number_and_convert_to_decimal(self.number)
            self.__data_type = types.MeasurementDataTypes.NUMBER
        if has_location:
            self.location = validation.check_location_and_convert(self.location)
            self.__data_type = types.MeasurementDataTypes.LOCATION
        
    @classmethod
    def from_api_response(cls, api_response: dict):
        return cls(
            date = api_response.get("date"),
            number = api_response.get("number"),
            location = api_response.get("location")
        )
    
    def get_value(self) -> Union[decimal.Decimal, dict]:
        if self.__data_type == types.MeasurementDataTypes.NUMBER:
            return self.number
        elif self.__data_type == types.MeasurementDataTypes.LOCATION:
            return self.location
        else:
            return None

    def _get_data_type(self) -> str:
        return self.__data_type.value
