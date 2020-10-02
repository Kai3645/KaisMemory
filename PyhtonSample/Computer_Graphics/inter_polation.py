import matplotlib.pyplot as plt
import numpy as np

methods = [None, 'none', 'nearest', 'bilinear', 'bicubic', 'spline16',
           'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
           'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos']

grid = np.random.random((8, 8))

fig, axs = plt.subplots(nrows = 3, ncols = 6, figsize = (9, 6),
                        subplot_kw = {'xticks': [], 'yticks': []})

for ax, interp_method in zip(axs.flat, methods):
	ax.imshow(grid, interpolation = interp_method, cmap = 'hot')
	ax.set_title(str(interp_method))

plt.tight_layout()
plt.show()
