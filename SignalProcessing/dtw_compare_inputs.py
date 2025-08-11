import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from dtaidistance import dtw
from scipy.stats import pearsonr
import pandas as pd
import csv
import pywt
import cython

x1, y1 = [], []
x2, y2 = [], []

# Read first CSV
with open('csvs/TrafficLight - Sheet1 (on).csv', 'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for i, row in enumerate(lines):
        try:
            x1.append(float(row[0]))
            y1.append(float(row[1]))
        except ValueError:
            continue

# Read second CSV
with open('csvs/TrafficLight - Sheet2 (off).csv', 'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for i, row in enumerate(lines):
        try:
            x2.append(float(row[0]))
            y2.append(float(row[1]))
        except ValueError:
            continue

# Convert to numpy arrays
y1_np = np.array(y1)
y2_np = np.array(y2)

#-------- Mean absolute deviation of signal -----------#
def madev(d, axis=None):
    return np.mean(np.absolute(d - np.mean(d, axis)), axis)


# ----- Wavelet Denoising -----
def wavelet_denoise(x, wavelet='db4', level=4):
    coeff = pywt.wavedec(x, wavelet, mode="per")
    sigma = (1/0.6745) * madev(coeff[-level])
    uthresh = sigma * np.sqrt(2 * np.log(len(x)))
    coeff[1:] = (pywt.threshold(i, value=uthresh, mode='hard') for i in coeff[1:])
    return pywt.waverec(coeff, wavelet, mode='per')

y1_denoised = wavelet_denoise(y1_np)
y2_denoised = wavelet_denoise(y2_np)

# Optional: downsample for speed
factor = 70
y1_d = y1_denoised[::factor]
y2_d = y2_denoised[::factor]

# Compute fast DTW distance (no path, no matrix)
distance = dtw.distance(y1_d, y2_d)


# Calculate DTW distance and obtain the warping paths (no need for the C library)
distance, paths = dtw.warping_paths(y1_d, y2_d, use_c=True)
best_path = dtw.best_path(paths)

# Estimate similarity score by normalizing with length
similarity_score = distance / len(y1_d)  # or len(y2_d)
print(f"Similarity Score: {similarity_score:.4f}")

print(similarity_score)

plt.figure(figsize=(12, 8))

# Original Time Series Plot
ax1 = plt.subplot2grid((2, 2), (0, 0))
ax1.plot(y1_denoised, label='Input 1', color='blue')
ax1.plot(y2_denoised, label='Input 2', linestyle='--',color='orange')
ax1.set_title('Original Time Series')
ax1.legend()

# Shortest Path Plot (Cost Matrix with the path)
# In this example, only the path is plotted, not the entire cost matrix.

ax2 = plt.subplot2grid((2, 2), (0, 1))
ax2.plot(np.array(best_path)[:, 0], np.array(best_path)[:, 1], 'green', marker='o', linestyle='-')
ax2.set_title('Shortest Path (Best Path)')
ax2.set_xlabel('Input 1')
ax2.set_ylabel('Input 2')
ax2.grid(True)

# Point-to-Point Comparison Plot
ax3 = plt.subplot2grid((2, 2), (1, 0), colspan=2)
ax3.plot(y1_denoised, label='Input 1', color='blue', marker='o')
ax3.plot(y2_denoised, label='Input 2', color='orange', marker='x', linestyle='--')
for a, b in best_path:
    ax3.plot([a, b], [y1_denoised[a], y2_denoised[b]], color='grey', linestyle='-', linewidth=1, alpha = 0.5)
ax3.set_title('Point-to-Point Comparison After DTW Alignment')
ax3.legend()

plt.tight_layout()
plt.show()