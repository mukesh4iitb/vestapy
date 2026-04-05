import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

# Load data
data = np.loadtxt("ext_values.txt").reshape(-1)  # flatten to 1D

# Define colormap
cmap = plt.colormaps['rainbow']

# -----------------------
# Nonlinear Norm Classes
# -----------------------

# 1. PowerNorm (gamma)
power_norm = colors.PowerNorm(gamma=0.3, vmin=data.min(), vmax=data.max())

# 2. LogNorm (requires positive data)
# shift data to positive for log
data_shifted = data - data.min() + 1e-6
log_norm = colors.LogNorm(vmin=data_shifted.min(), vmax=data_shifted.max())

# 3. CustomNorm (piecewise linear example)
class CustomNorm(colors.Normalize):
    def __call__(self, value, clip=None):
        # map [min, mid, max] -> [0, 0.5, 1] nonlinear
        vmin, vmax = self.vmin, self.vmax
        mid = (vmin + vmax)/2
        result = np.zeros_like(value, dtype=float)
        mask1 = value <= mid
        mask2 = value > mid
        result[mask1] = 0.5 * (value[mask1] - vmin)/(mid - vmin)
        result[mask2] = 0.5 + 0.5 * (value[mask2] - mid)/(vmax - mid)
        return result

custom_norm = CustomNorm(vmin=data.min(), vmax=data.max())

# 4. ExponentialNorm
class ExponentialNorm(colors.Normalize):
    def __call__(self, value, clip=None):
        normed = (value - self.vmin)/(self.vmax - self.vmin)
        return (np.exp(normed) - 1)/(np.e - 1)

exp_norm = ExponentialNorm(vmin=data.min(), vmax=data.max())

# 5. Hyperbolic tangent normalization
class TanhNorm(colors.Normalize):
    def __call__(self, value, clip=None):
        normed = (value - self.vmin)/(self.vmax - self.vmin)
        return (np.tanh(2*(normed - 0.5)) + 1)/2

tanh_norm = TanhNorm(vmin=data.min(), vmax=data.max())

# 6. Sigmoid normalization
class SigmoidNorm(colors.Normalize):
    def __call__(self, value, clip=None):
        normed = (value - self.vmin)/(self.vmax - self.vmin)
        return 1/(1 + np.exp(-10*(normed - 0.5)))

sigmoid_norm = SigmoidNorm(vmin=data.min(), vmax=data.max())

# -----------------------
# Plotting
# -----------------------
norm_list = [
    ("Linear", colors.Normalize(vmin=data.min(), vmax=data.max())),
    ("PowerNorm (0.3)", power_norm),
    ("LogNorm", log_norm),
    ("CustomNorm", custom_norm),
    ("ExponentialNorm", exp_norm),
    ("TanhNorm", tanh_norm),
    ("SigmoidNorm", sigmoid_norm)
]

fig, axes = plt.subplots(1, len(norm_list), figsize=(18, 6))
for ax, (title, norm) in zip(axes, norm_list):
    rgba = cmap(norm(data))
    ax.imshow(rgba.reshape(-1,1,4), aspect='auto')
    ax.set_yticks(range(len(data)))
    ax.set_yticklabels([f"{v:.2f}" for v in data])
    ax.set_xticks([])
    ax.set_title(title, fontsize=10)

plt.tight_layout()
plt.show()



import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

# Example data
data = np.array([0.055, 0.055, 0.016, 0.016, 0.022, 0.022, 0.002, 0.002,
                 0.002, 0.002, 0.003, 0.003, 0.021, 0.021, 0.053, 0.053,
                 0.041, 0.041, 0.005, 0.005, 0.000, 0.000, -0.009, -0.009,
                 0.018, 0.018, 0.009, 0.009, -0.003, -0.003, -0.003, -0.003,
                 0.009, 0.009, -0.000, -0.000, -0.000, -0.000, -0.005, -0.005,
                 0.002, 0.002, 0.021, 0.021, 0.024, 0.024, -0.014, -0.014,
                 -0.014, -0.014, 0.008, 0.008, -0.004, -0.004, -0.017, -0.017,
                 -0.004, -0.004, 0.000, 0.000, -0.000, -0.000, 0.001, 0.001,
                 -0.000, -0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000,
                 -2.692])

# Choose colormap
cmap = plt.colormaps['rainbow']

# Use SymLogNorm to handle small values + outlier
norm = colors.SymLogNorm(linthresh=0.01, linscale=1.0, vmin=data.min(), vmax=data.max())

# Create figure & axes
fig, ax = plt.subplots(figsize=(2, 6))

# Plot data as a vertical strip and get the image object
im = ax.imshow(data.reshape(-1, 1), cmap=cmap, norm=norm, aspect='auto')

# Y-axis labels
ax.set_yticks(range(len(data)))
ax.set_yticklabels([f"{v:.3f}" for v in data])
ax.set_xticks([])

# Add colorbar attached to the same axes
cbar = fig.colorbar(im, ax=ax, orientation='vertical')
cbar.set_label('Value')

plt.title("Color mapping strip")
plt.show()


