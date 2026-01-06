from math import radians, cos, sin, asin, sqrt
from app.config import settings


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two points using Haversine formula.
    Returns distance in kilometers.
    """
    R = 6371  # Earth's radius in kilometers

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    return R * c


def is_within_range(lat1: float, lon1: float, lat2: float, lon2: float) -> bool:
    """Check if two points are within MAX_DISTANCE_KM."""
    distance = calculate_distance(lat1, lon1, lat2, lon2)
    return distance <= settings.MAX_DISTANCE_KM
