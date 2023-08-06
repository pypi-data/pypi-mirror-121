import decimal

from . import convertions
from blockbax_sdk import types

import logging
logger = logging.getLogger(__name__)

def check_date_and_convert_to_unix(d: types.AnyDate) -> int:
    """checks if the given date can be converted to a datetime object and returns the unix timestamp"""
    return convertions.convert_any_date_to_unix_millis(d)

def check_text(v: str) -> str:
    """checks if value is instance of str, or Text type, if not raise error """
    if not isinstance(v, str):
        value_not_text_error = f"Text value {v} is not a Text type"
        raise ValueError(value_not_text_error)
    return v

def check_number_and_convert_to_decimal(v: types.AnyNumber) -> decimal.Decimal:
    """Check if value can be converted into a Decimal.  returns a decimal"""
    return convertions.convert_number_to_decimal(v)

def check_latitude_and_convert_to_decimal(latitude: types.AnyNumber) -> decimal.Decimal:
    """Check if latitude can be converted into a Decimal and if within range: 90 < latitude < -90.  returns a decimal"""
    try:
        latitude = convertions.convert_number_to_decimal(latitude)
        if 90 < latitude < -90:
            raise ValueError(f"Latitude is not within correct range: 90 < {latitude} < -90 == {90 < latitude < -90}")
        return latitude
    except (decimal.InvalidOperation, ValueError) as e:
        latitude_convertion_error = f"Could not convert: {latitude}, cause: {e}"
        raise ValueError(latitude_convertion_error)

def check_longitude_and_convert_to_decimal(longitude: types.AnyNumber) -> decimal.Decimal:
    """Check if longitude can be converted into a Decimal and if within range: 180 < longitude < -180.  returns a decimal"""
    try:
        longitude = convertions.convert_number_to_decimal(longitude)
        if 180 < longitude < -180:
            raise ValueError(f"Longitude is not within correct range: 180 < {longitude} < -180 == {180 < longitude < -180}")
        return longitude
    except (decimal.InvalidOperation, ValueError) as e:
        longitude_convertion_error = f"Could not convert: {longitude}, cause: {e}"
        raise ValueError(longitude_convertion_error)

def check_altitude_and_convert_to_decimal(altitude: types.AnyNumber) -> decimal.Decimal:
    """Check if altitude can be converted into a Decimal.  returns a decimal"""
    try:
        altitude = convertions.convert_number_to_decimal(altitude)
        return altitude
    except (decimal.InvalidOperation, ValueError) as e:
        altitude_convertion_error = f"Could not convert: {altitude}, cause: {e}"
        raise ValueError(altitude_convertion_error)

def check_location_and_convert(location: dict) -> dict:
    # check if lat and lon are numeric and if the l dict has lat and lon
    if not isinstance(location, dict):
        raise ValueError("'location' value is not a dict")
    
    location_keys = ["lat", "lon"]
    for key in location_keys:
        missing_keys = []
        if key not in location:
            missing_keys.append(key)
    if len(missing_keys) > 0:
        raise ValueError(f"'location' dict: {location} does not have keys: {missing_keys}")
    
    location["lat"] = check_latitude_and_convert_to_decimal(location["lat"])
    location["lon"] = check_longitude_and_convert_to_decimal(location["lon"])
    if "alt" in location:
        # altitude is optional
        location["alt"] = check_altitude_and_convert_to_decimal(location["alt"])
    return location

def check_map_layer_and_convert(map_layer: dict) -> dict:
    if not isinstance(map_layer, dict):
        raise ValueError("'map_layer' value is not a dict")

    map_layer_keys = ["imagePath", "leftBottom", "leftTop", "rightBottom", "rightTop"]
    for key in map_layer_keys:
        missing_keys = []
        if key not in map_layer:
            missing_keys.append(key)
    if len(missing_keys) > 0:
        raise ValueError(f"'map_layer' dict: {map_layer} does not have keys: {missing_keys}")

    if not isinstance(map_layer["imagePath"], str):
        raise ValueError("'imagePath' is not a 'str'")

    map_layer["leftBottom"] = check_location_and_convert(map_layer["leftBottom"])
    map_layer["leftTop"] = check_location_and_convert(map_layer["leftTop"])
    map_layer["rightBottom"] = check_location_and_convert(map_layer["rightBottom"])
    map_layer["rightTop"] = check_location_and_convert(map_layer["rightTop"])

    return map_layer

def check_image(image: dict):
    if not isinstance(image, dict):
        raise ValueError("'image' value is not a dict")

    if "imagePath" not in image:
        raise ValueError("'image' does not contain 'imagePath'")
    
    if not isinstance(image["imagePath"], str):
        raise ValueError("'imagePath' is not a 'str'")
    
    return image
