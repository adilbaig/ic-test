from config.constants import *


def distance_from_hq(latitude: float, longitude: float) -> float:
    """
    Given a GPS coordinate, find the distance to the office (in kms)

    :param latitude:
    :param longitude:
    :return: float
    """

    return spherical_distance_degrees(latitude, longitude, HQ_LAT, HQ_LON)


def spherical_distance_degrees(latitude1: float, longitude1: float, latitude2: float, longitude2: float) -> float:
    """
    Similar to `spherical_distance`, coordinates are in degrees

    :param latitude1:
    :param longitude1:
    :param latitude2:
    :param longitude2:
    :return: Distance in kms
    """
    from math import radians

    return spherical_distance(
        radians(latitude1),
        radians(longitude1),
        radians(latitude2),
        radians(longitude2),
    )


def spherical_distance(latitude1: float, longitude1: float, latitude2: float, longitude2: float) -> float:
    """
    Given two coordinates (in radians) calculate the distance (in kms) between them, as measured along the surface of a sphere.

    The great-circle distance or orthodromic distance is the shortest distance between two points on the surface of a sphere.
    The Earth is nearly spherical (see Earth radius), so great-circle distance formulas give the distance between points
    on the surface of the Earth correct to within about 0.5%

    @see https://en.wikipedia.org/wiki/Great-circle_distance

    :param latitude1:
    :param longitude1:
    :param latitude2:
    :param longitude2:

    :return: Distance in kms
    """

    from math import fabs, acos, sin, cos

    diff_long = fabs(longitude1 - longitude2)
    central_angle = acos(sin(latitude1) * sin(latitude2) + (cos(latitude1) * cos(latitude2) * cos(diff_long)))
    return EARTH_RADIUS_KM * central_angle
