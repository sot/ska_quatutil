import numpy as np
from numpy import sin, cos, tan, arctan2, radians, degrees, sqrt

def radec2eci(ra, dec):
    """
    Convert from RA,Dec to ECI.  The input ``ra`` and ``dec`` values can be 1-d
    arrays of length N in which case the output ``ECI`` will be an array with
    shape (3,N).

    :param ra: Right Ascension (degrees)
    :param dec: Declination (degrees)
    :returns: numpy array ECI (3-vector or 3xN array)
    """
    r = radians(ra)
    d = radians(dec)
    return np.array([cos(r) * cos(d), sin(r) * cos(d), sin(d)])

def eci2radec(eci):
    """
    Convert from ECI vector(s) to RA, Dec.  The input ``eci`` value
    can be an array of 3-vectors having shape (3,N) in which case
    the output RA, Dec will be arrays of length N.

    :param eci: ECI as 3-vector or (3,N) array
    :rtype: list ra, dec (degrees)
    """
    ra  = degrees(arctan2(eci[1], eci[0]))
    dec = degrees(arctan2(eci[2], sqrt(eci[1]**2 + eci[0]**2)))
    ok = ra < 0
    try:
        ra[ok] += 360
    except (ValueError, IndexError):
        if ok:
            ra += 360
    return ra, dec

def radec2yagzag(ra, dec, q):
    """
    Given RA, Dec, and pointing quaternion, determine ACA Y-ang, Z-ang.  The
    input ``ra`` and ``dec`` values can be 1-d arrays in which case the output
    ``yag`` and ``zag`` will be corresponding arrays of the same length.

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
    Given ACA Y-ang, Z-ang and pointing quaternion determine RA, Dec. The
    input ``yag`` and ``zag`` values can be 1-d arrays in which case the output
    ``ra`` and ``dec`` will be corresponding arrays of the same length.

    :param yag: ACA Y angle (degrees)
    :param zag: ACA Z angle (degrees)
    :param q: Quaternion
    :rtype: list ra, dec (degrees)
    """
    try:
        one = np.ones(len(yag))
    except TypeError:
        one = 1.0
    d_aca = np.array([one, tan(radians(yag)), tan(radians(zag))])
    d_aca *= 1.0 / np.sum(d_aca**2)
    eci = np.dot(q.transform, d_aca)
    return eci2radec(eci);
