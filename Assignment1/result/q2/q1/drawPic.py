import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


dims = np.load("./3d_dims.npy")
p = np.load("./3d_p.npy")
passRate = np.load("./3d_passRate.npy")

fig = plt.figure()
ax = Axes3D(fig)
ax.plot_surface(dims, p, passRate, rstride=1, cstride=1, cmap='rainbow')
plt.show()