def kabsch2(float[:,:] xa, float[:, :] xb):
    """
    Fit xa to xb

    Args:
        xa ([N, 3] array): coordinates to fit
        xb ([N, 3] array): coordinates of reference

    Returns:
        R: [3,3] rotation marix
        T: [3] translation vector
        rmsd: rms error (float)
    """
    import numpy as np
    
    cdef Py_ssize_t n = xa.shape[0]
    cdef Py_ssize_t i, j, k
    
    cma = np.zeros(3)
    cmb = np.zeros(3)
    umat = np.zeros((3, 3))
    
    cdef double[:] cma_v = cma
    cdef double[:] cmb_v = cmb
    cdef double[:,:] umat_v = umat
    
    cdef double xasq = 0.0
    cdef double xbsq = 0.0
    cdef double cma2 = 0.0
    cdef double cmb2 = 0.0
    cdef double iw = 1.0 / n
    cdef double rmse
    
    for i in range(3):
        for j in range(n):
            for k in range(3):
                umat_v[i, k] += xa[j, i] * xb[j, k]
            cma_v[i] += xa[j, i]
            cmb_v[i] += xb[j, i]
    for i in range(3):
        cma_v[i] = cma_v[i] * iw
        cmb_v[i] = cmb_v[i] * iw
        for k in range(3):
            umat_v[i, k] = umat_v[i, k] * iw
        for j in range(n):
            xasq += xa[j, i] * xa[j, i]
            xbsq += xb[j, i] * xb[j, i]
        cma2 += cma_v[i] * cma_v[i]
        cmb2 += cmb_v[i] * cmb_v[i]
    xasq = xasq * iw
    xbsq = xbsq * iw
    xasq = xasq - cma2
    xbsq = xbsq - cmb2
    umat = umat - np.outer(cma, cmb)
    
    V, S, W = np.linalg.svd(umat)
    d = (np.linalg.det(V) * np.linalg.det(W)) < 0.0

    if d:
        S[-1] = -S[-1]
        V[:, -1] = -V[:, -1]

    # Create Rotation matrix U
    U = np.dot(V, W)
    
    rmse = (xasq + xbsq) - 2.0 * S.sum()
    if rmse < 0.0:
        rmse = 0.0
    rmse = np.sqrt(rmse)
    v = np.zeros(3)
    for i in range(3):
        t = (U[i,:] * cmb).sum()
        v[i] = (cma[i] - t)
    return U, v, rmse
