'''
This module contains functions to generate n-D rotation matrices.
'''
import math
import numpy as np

def rotation_from_angle_and_plane(angle, vector1, vector2, abs_tolerance_orthogonal_check=1e-10):
    '''
    generates an nxn rotation matrix from a given angle and
    a plane spanned by two given orthogonal vectors of length n:
    https://de.wikipedia.org/wiki/Drehmatrix#Drehmatrizen_des_Raumes_%7F'%22%60UNIQ--postMath-0000003B-QINU%60%22'%7F

    The formula used is

    .. math::

        M = 𝟙 + (\cos\\alpha-1)\cdot(v_1\otimes v_1 + v_2\otimes v_2) - \sin\\alpha\cdot(v_1\otimes v_2 - v_2\otimes v_1)

    with :math:`M` being the returned matrix, :math:`v_1` and :math:`v_2` being the two
    given vectors and :math:`\\alpha` being the given angle. It differs from the formula
    on wikipedia in that it is the transposed matrix to yield results that are consistent
    with the 2D and 3D cases.

    :param angle: the angle by which to rotate
    :type angle: float
    :param vector1: one of the two vectors that span the plane in which to rotate
                    (no normalisation required)
    :type vector1: array like
    :param vector2: the other of the two vectors that span the plane in which to rotate
                    (no normalisation required)
    :type vector2: array like
    :param abs_tolerance_orthogonal_check: The absolute tolerance to use when checking if vectors are orthogonal.
                                           Default is 1e-10, but this might be inadequate for your application.
    :type abs_tolerance_orthogonal_check: float

    .. warning:: Make sure that the two given vectors are orthogonal to each other.

    :returns: the rotation matrix
    :rtype: an nxn :any:`numpy.ndarray`
    '''
    vector1 = np.asarray(vector1)/np.linalg.norm(vector1)
    vector2 = np.asarray(vector2)/np.linalg.norm(vector2)

    if len(vector1) != len(vector2):
        raise ValueError(
            'Given vectors must have the same length but are: {}, {}'.format(len(vector1), len(vector2)))

    if not math.isclose(vector1.dot(vector2), 0, abs_tol=abs_tolerance_orthogonal_check):
        raise ValueError(
            'Given vectors are not orthogonal for given numerical tolerance: {:.0e}'.format(abs_tolerance_orthogonal_check))

    V = np.outer(vector1, vector1) + np.outer(vector2, vector2)
    W = np.outer(vector1, vector2) - np.outer(vector2, vector1)

    return np.eye(len(vector1)) + (math.cos(angle) - 1)*V - math.sin(angle)*W