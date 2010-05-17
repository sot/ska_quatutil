import numpy as np
from numpy import sin, cos, tan, arctan2, radians, degrees, sqrt

def radec2eci(ra, dec):
    """
    Convert from RA,Dec to ECI

    :param ra: Right Ascension (degrees)
    :param dec: Declination (degrees)
    :rtype: numpy array ECI (3-vector)
    """
    r = radians(ra)
    d = radians(dec)
    return np.array([cos(r) * cos(d), sin(r) * cos(d), sin(d)])

def eci2radec(eci):
    """
    Convert from ECI to RA,Dec

    :param eci: numpy array ECI (3-vector)
    :rtype: list ra, dec (degrees)
    """
    ra  = degrees(arctan2(eci[1], eci[0]))
    dec = degrees(arctan2(eci[2], sqrt(eci[1]**2 + eci[0]**2)))
    if ra < 0:
        ra += 360
    return ra, dec

def radec2yagzag(ra, dec, q):
    """
    Given RA, Dec, and pointing quaternion, determine ACA Y-ang, Z-ang.

    :param ra: Right Ascension (degrees)
    :param dec: Declination (degrees)
    :param q: Quaternion
    :rtype: list yag, zag (degrees)
    """
    eci = radec2eci(ra, dec);
    d_aca = np.dot(q.transform.transpose(), eci)
    yag = degrees(arctan2(d_aca[1], d_aca[0]))
    zag = degrees(arctan2(d_aca[2], d_aca[0]))
    return yag, zag

def yagzag2radec(yag, zag, q):
    """
    Given ACA Y-ang, Z-ang and pointing quaternion determine RA, Dec

    :param yag: ACA Y angle (degrees)
    :param zag: ACA Z angle (degrees)
    :param q: Quaternion
    :rtype: list ra, dec (degrees)
    """
    d_aca = np.array([1.0, tan(radians(yag)), tan(radians(zag))])
    d_aca *= 1.0 / np.sum(d_aca**2)
    eci = np.dot(q.transform, d_aca)
    return eci2radec(eci);
