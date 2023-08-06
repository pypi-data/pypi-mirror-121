import numpy as np

def cdist(XA, XB):
  if len(XA.shape) != 2:
    raise ValueError('Error: XA must be a 2D array')
  if len(XB.shape) != 2:
    raise ValueError('Error: XB must be a 2D array')
  ma, na = XA.shape
  mb, nb = XB.shape
  if (na != nb):
    raise ValueError('Error: XA and XB must have the same second dimension')

  cd = np.zeros((ma, mb))

  for ia, va in enumerate(XA):
    dx = XB - va
    r = np.sqrt((dx * dx).sum(axis=1))
    cd[ia] = r

  return cd
