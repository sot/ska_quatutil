import numpy as np
from numpy import sin, cos, tan, arctan2, radians, degrees, sqrt
from Quaternion import Quat

__version__ = '0.3.1'


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
    if isinstance(ok, np.ndarray):
        ra[ok] += 360
    elif ok:
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

def _norm(vec):
    return vec / np.sqrt(np.sum(vec**2))

def quat_x_to_vec(vec, method='radec'):
    """Generate quaternion that rotates X-axis into ``vec``.

    The ``method`` parameter can take one of three values: "shortest",
    "keep_z", or "radec" (default).  The "shortest" method takes the shortest
    path between the two vectors.  The "radec" method does the transformation
    as the corresponding (RA, Dec, Roll=0) attitude.  The "keep_z" method does
    a roll about X-axis (followed by the "shortest" path) such that the
    transformed Z-axis is in the original X-Z plane.  In equations::

      T: "shortest" quaternion taking X-axis to vec
      Rx(theta): Rotation by theta about X-axis = [[1,0,0], [0,c,s], [0,-s,c]]
      Z: Z-axis [0,0,1]

      [T * Rx(theta) * Z]_y = 0
      T[1,1] * sin(theta) + T[1,2]*cos(theta) = 0
      theta = atan2(T[1,2], T[1,1]) 

    :param vec: Input 3-vector
    :param method: method for determining path (shortest|keep_z|radec)
    :returns: Quaternion object
    """
    x = np.array([1.,0,0])
    vec = _norm(np.array(vec))
    if method in ("shortest", "keep_z"):
        dot = np.dot(x, vec)
        if abs(dot) > 1-1e-8:
            x = _norm(np.array([1., 0., 1e-7]))
            dot = np.dot(vec, x)
        angle = np.arccos(dot)
        axis = _norm(np.cross(x, vec))
        sin_a = np.sin(angle / 2)
        cos_a = np.cos(angle / 2)
        q = Quat([axis[0] * sin_a,
                  axis[1] * sin_a,
                  axis[2] * sin_a,
                  cos_a])

        if method == "keep_z":
            T = q.transform
            theta = np.arctan2(T[1,2], T[1,1])
            qroll = Quat([0, 0, degrees(theta)])
            q = q * qroll
    else:
        ra = np.degrees(np.arctan2(vec[1], vec[0]))
        dec = np.degrees(np.arcsin(vec[2]))
        q = Quat([ra, dec, 0])

    return q

