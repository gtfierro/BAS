"""Utility functions for geography and geometry"""
from simpletransform import applyTransformToPoint

def applyTransformToRegions(mtx, regions):
    for poly in regions:
        for pt in poly:
            applyTransformToPoint(mtx, pt)

def identityMtx():
    return [[1.0, 0.0, 0.0],[0.0, 1.0, 0.0]]

def inverse(((m00, m01, m02), (m10, m11, m12))):
    # TODO: improve inverse calculation
    m20 = 0
    m21 = 0
    m22 = 1
    det = m00*m11*m22 + m01*m12*m20 + m02*m10*m21 - m00*m12*m21 - m01*m10*m22 - m02*m11*m20;
    return [[float(m11*m22 - m12*m21)/det,
             float(m02*m21 - m01*m22)/det,
             float(m01*m12 - m02*m11)/det],
            [float(m12*m20 - m10*m22)/det,
             float(m00*m22 - m02*m20)/det,
             float(m02*m10 - m00*m12)/det
             ]]
