import numpy as np
import matplotlib.pyplot as plt
import csv
import pywt

# Sampling rate
sr = 25000
ts = 1.0 / sr

x1, y1 = [], []

# Padded limit helper
def padded_limits(data, lower=1, upper=99, pad=0.05):
    pmin, pmax = np.percentile(data, [lower, upper])
    prange = pmax - pmin
    return pmin - prange * pad, pmax + prange * pad

# Mean absolute deviation
def madev(d, axis=None):
    return np.mean(np.abs(d - np.mean(d, axis)), axis)

# Wavelet Denoising
def wavelet_denoise(x, wavelet='db4', level=4):
    coeff = pywt.wavedec(x, wavelet, mode="per")
    sigma = (1/0.6745) * madev(coeff[-level])
    uthresh = sigma * np.sqrt(2 * np.log(len(x)))
    coeff[1:] = (pywt.threshold(i, value=uthresh, mode='hard') for i in coeff[1:])
    return pywt.waverec(coeff, wavelet, mode='per')

# Load CSV helper
def load_csv(filepath):
    x, y = [], []
    with open(filepath, 'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for i, row in enumerate(lines):
            if i > 13:
                try:
                    x.append(float(row[0]))
                    y.append(float(row[1]))
                except ValueError:
                    continue
    return x, y

# Load Input 1
x1, y1 = load_csv('csvs/input_four.csv')
y1_np = np.array(y1)
y1_denoised = wavelet_denoise(y1_np)
x1_trimmed = x1[:len(y1_denoised)]  # Align x1 length with denoised output

# Plotting
plt.figure(figsize=(16, 12))

# Input 1 - Denoised
plt.subplot(4, 1, 1)
plt.plot(x1_trimmed, y1_denoised, color='b')
plt.title('Time Series - Input four (Denoised)')
plt.xlabel('Time (s)')
plt.ylabel('Voltage')
plt.grid(True)

# Comparison Inputs
for cnum, inum in zip(("one", "two", "three"), (2, 3, 4)):
    x2, y2 = load_csv(f'csvs/input_{cnum}.csv')

    # Align to shortest raw length
    min_len_raw = min(len(y1), len(y2))
    y1_crop = y1[:min_len_raw]
    y2_crop = y2[:min_len_raw]

    # Denoise both
    y1_d = wavelet_denoise(np.array(y1_crop))
    y2_d = wavelet_denoise(np.array(y2_crop))

    # Align denoised lengths
    min_dlen = min(len(y1_d), len(y2_d))
    y1_d = y1_d[:min_dlen]
    y2_d = y2_d[:min_dlen]
    x_plot = x1[:min_dlen]  # Use original x1 sliced to match denoised

    # Difference signal
    y_diff = y1_d - y2_d
    ts_diff_min, ts_diff_max = padded_limits(y_diff)

    # Plot difference
    plt.subplot(4, 1, inum)
    plt.plot(x_plot, y_diff, color='purple')
    plt.title(f'Time Series Difference - Input four vs Input {cnum}')
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage Difference')
    plt.grid(True)
    plt.ylim(ts_diff_min, ts_diff_max)

plt.tight_layout()
plt.show()
