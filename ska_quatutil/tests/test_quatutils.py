# Licensed under a 3-clause BSD style license - see LICENSE.rst
import numpy as np

import ska_quatutil
from Quaternion import Quat


ra1 = 10.
dec1 = 20.
ra2 = ra1 + .5
dec2 = dec1 - .1
roll = 30.
q0 = Quat([ra1, dec1, roll])


def test_radec2eci():
    eci = ska_quatutil.radec2eci(ra1, dec1)
    assert np.allclose(eci[0], 0.92541658)
    assert np.allclose(eci[1], 0.16317591)
    assert np.allclose(eci[2], 0.34202014)


def test_radec2yagzag():
    yag, zag = ska_quatutil.radec2yagzag(ra2, dec2, q0)
    assert np.allclose(yag, 0.35751029916939936)
    assert np.allclose(zag, -0.32107186086370215)


def test_eci2radec():
    eci = np.array([0.92541658, 0.16317591, 0.34202014])
    tra, tdec = ska_quatutil.eci2radec(eci)
    assert np.allclose(tra, 9.9999999129952908)
    assert np.allclose(tdec, 19.999999794004037)


def test_vectorized_eci2radec():
    eci = np.array([[0.92541658, 0.9248273],
                    [0.16317591, -0.16307201],
                    [0.34202014, 0.34365969]])
    tra, tdec = ska_quatutil.eci2radec(eci)
    assert np.allclose(tra[0], 9.9999999129952908)
    assert np.allclose(tra[1], 349.9999997287627)
    assert np.allclose(tdec[0], 19.999999794004037)
    assert np.allclose(tdec[1], 20.099999743270516)


def test_yagzag2radec():
    yag = 0.35751029916939936
    zag = -0.32107186086370215
    tra, tdec = ska_quatutil.yagzag2radec(yag, zag, q0)
    assert np.allclose(tra, ra2)
    assert np.allclose(tdec, dec2)


def test_vectorized_radec():
    ras = np.arange(10)
    decs = np.arange(10)
    ecis = ska_quatutil.radec2eci(ras, decs)
    assert ecis.shape == (3, 10)
    ra1s, dec1s = ska_quatutil.eci2radec(ecis)
    for ra, ra1, dec, dec1 in zip(ras, ra1s, decs, dec1s):
        assert np.allclose(ra, ra1)
        assert np.allclose(dec, dec1)


def test_vectorized_yagzag():
    ras = np.arange(1, 11)
    decs = np.arange(1, 11)
    yags, zags = ska_quatutil.radec2yagzag(ras, decs, q0)
    assert yags.shape == (10,)
    assert zags.shape == (10,)
    ra1s, dec1s = ska_quatutil.yagzag2radec(yags, zags, q0)
    for ra, ra1, dec, dec1 in zip(ras, ra1s, decs, dec1s):
        assert np.allclose(ra, ra1)
        assert np.allclose(dec, dec1)


def test_quat_x_to_vec():
    vecs = np.random.random((100, 3)) - 0.5
    for vec in vecs:
        vec = ska_quatutil.norm(vec)
        for method in ('keep_z', 'shortest', 'radec'):
            q = ska_quatutil.quat_x_to_vec(vec, method)
            vec1 = np.dot(q.transform, [1.0, 0, 0])
            print(method, vec, vec1)
            for i in range(3):
                assert np.allclose(vec[i], vec1[i])
            if method == 'radec':
                assert np.allclose(q.roll, 0.0)
            elif method == 'keep_z':
                vec1 = np.dot(q.transform, [0, 0, 1.0])
                assert np.allclose(vec1[1], 0.0)
