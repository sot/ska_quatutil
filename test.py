from nose.tools import *
import numpy as np

import Ska.quatutil
from Quaternion import Quat


ra1 = 10.
dec1 = 20.
ra2 = ra1 + .5
dec2 = dec1 - .1
roll = 30.
q0 = Quat([ra1,dec1,roll])

def test_radec2eci():
    eci = Ska.quatutil.radec2eci(ra1, dec1)
    assert_almost_equal(eci[0], 0.92541658)
    assert_almost_equal(eci[1], 0.16317591)
    assert_almost_equal(eci[2], 0.34202014)

def test_radec2yagzag():
    yag, zag = Ska.quatutil.radec2yagzag(ra2, dec2, q0)
    assert_almost_equal(yag, 0.35751029916939936)
    assert_almost_equal(zag, -0.32107186086370215)

def test_eci2radec():
    eci = np.array([ 0.92541658, 0.16317591, 0.34202014])
    tra, tdec = Ska.quatutil.eci2radec(eci)
    assert_almost_equal(tra, 9.9999999129952908 )
    assert_almost_equal(tdec, 19.999999794004037)

def test_yagzag2radec():
    yag = 0.35751029916939936
    zag = -0.32107186086370215
    tra, tdec = Ska.quatutil.yagzag2radec( yag, zag, q0)
    assert_almost_equal( tra, ra2)
    assert_almost_equal( tdec, dec2)
    
def test_vectorized_radec():
    ras = np.arange(10)
    decs = np.arange(10)
    ecis = Ska.quatutil.radec2eci(ras, decs)
    assert_equal(ecis.shape, (3, 10))
    ra1s, dec1s = Ska.quatutil.eci2radec(ecis)
    for ra, ra1, dec, dec1 in zip(ras, ra1s, decs, dec1s):
        assert_almost_equal(ra, ra1)
        assert_almost_equal(dec, dec1)

def test_vectorized_yagzag():
    ras = np.arange(1,11)
    decs = np.arange(1,11)
    yags, zags = Ska.quatutil.radec2yagzag(ras, decs, q0)
    assert_equal(yags.shape, (10,))
    assert_equal(zags.shape, (10,))
    ra1s, dec1s = Ska.quatutil.yagzag2radec(yags, zags, q0)
    for ra, ra1, dec, dec1 in zip(ras, ra1s, decs, dec1s):
        assert_almost_equal(ra, ra1)
        assert_almost_equal(dec, dec1)
        
def test_quat_x_to_vec():
    vecs = np.random.random((100, 3)) - 0.5
    for vec in vecs:
        vec = Ska.quatutil._norm(vec)
        q = Ska.quatutil.quat_x_to_vec(vec, keep_z=False)
        vec1 = np.dot(q.transform, [1.0, 0, 0])
        for i in range(3):
            assert_almost_equal(vec[i], vec1[i])

def test_quat_x_to_vec_keep_z():
    vecs = np.random.random((100, 3)) - 0.5
    for vec in vecs:
        vec = Ska.quatutil._norm(vec)
        q = Ska.quatutil.quat_x_to_vec(vec, keep_z=True)
        vec1 = np.dot(q.transform, [1., 0, 0])
        for i in range(3):
            assert_almost_equal(vec[i], vec1[i])
            
        vec1 = np.dot(q.transform, [0, 0, 1.0])
        assert_almost_equal(vec1[1], 0.0)

