import exifread
import json
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_exif_data_exifread(image_path):
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f, details=True)
            if tags:
                return {tag: str(value) for tag, value in tags.items()}
            else:
                return {}
    except Exception as e:
        print(f"Error processing {image_path} with exifread: {e}")
        return None


def convert_fraction_string_to_float(fraction_str):
    s_fraction_str = str(fraction_str)
    if '/' in s_fraction_str:
        try:
            numerator_str, denominator_str = s_fraction_str.split('/')
            numerator = float(numerator_str)
            denominator = float(denominator_str)
            if denominator == 0:
                raise ValueError("Denominator is zero.")
            return numerator / denominator
        except ValueError as e:
            logging.error(f"Error parsing fraction '{s_fraction_str}': {e}")
            return None
    try:
        return float(s_fraction_str)
    except ValueError as e:
        logging.error(f"Error converting non-fraction string '{s_fraction_str}' to float: {e}")
        return None


def convert_dms_string_to_decimal(dms_string, ref='N'):
    try:
        cleaned_string = dms_string.strip('[]').strip()
        components_str = [comp.strip() for comp in cleaned_string.split(',')]

        if len(components_str) != 3:
            raise ValueError(f"DMS string '{dms_string}' must contain 3 components: [degrees, minutes, seconds]")

        degrees = float(components_str[0])
        minutes = float(components_str[1])
        seconds = convert_fraction_string_to_float(components_str[2])

        if seconds is None:
            return None

        decimal_degrees = degrees + (minutes / 60.0) + (seconds / 3600.0)

        if ref.upper() in ['S', 'W']:
            decimal_degrees *= -1

        return decimal_degrees
    except Exception as e:
        logging.error(f"Error converting DMS string '{dms_string}': {e}")
        return None


def get_lat_lon_from_jpeg(image_path):
    exif_data = get_exif_data_exifread(image_path)
    if not exif_data:
        return None, None

    lat_str = exif_data.get('GPS GPSLatitude')
    lon_str = exif_data.get('GPS GPSLongitude')
    lat_ref = exif_data.get('GPS GPSLatitudeRef', 'N')
    lon_ref = exif_data.get('GPS GPSLongitudeRef', 'E')

    if lat_str and lon_str:
        latitude = convert_dms_string_to_decimal(lat_str, lat_ref)
        longitude = convert_dms_string_to_decimal(lon_str, lon_ref)
        return latitude, longitude
    else:
        return None, None


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python gps_extractor.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    lat, lon = get_lat_lon_from_jpeg(image_path)

    if lat is not None and lon is not None:
        print(f"Latitude: {lat}, Longitude: {lon}")
    else:
        print("Could not extract GPS coordinates.")