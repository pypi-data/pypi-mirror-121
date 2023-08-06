from typing import List, Optional, Union
from numbers import Number

from . import measurement

import dataclasses
import datetime
import decimal

import logging
logger = logging.getLogger(__name__)

@dataclasses.dataclass
class Ingestion:
    id: str
    measurements: List[measurement.Measurement] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        if not self.id:
            no_ids_given_error = f"Please provide a ingestion ID"
            raise ValueError(no_ids_given_error)
            
    def add_measurement(
        self, 
        date: Union[datetime.datetime, Number, str], 
        number: Optional[Union[decimal.Decimal, Number, str]] = None,
        location: Optional[dict] = None, 
    ) -> None:
        new_measurement = measurement.Measurement(date=date, number=number, location=location)
        
        if len(self.measurements) > 0 and new_measurement._get_data_type() != self.measurements[-1]._get_data_type():
            inconsistent_use_of_data_type_error = f"Inconsistent use of data types, data type: {new_measurement._get_data_type()} does not equal data type of previous measurement added to this ingestion: {self.measurements[-1]._get_data_type()}"
            raise ValueError(inconsistent_use_of_data_type_error)
        
        self.measurements.append(new_measurement)

    def clear(self):
        self.measurements.clear()

    def get_measurement_count(self):
        return len(self.measurements)