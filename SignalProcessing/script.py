import numpy as np
import matplotlib.pyplot as plt
import csv
import pywt

# Sampling rate
sr = 25000
ts = 1.0 / sr

x, y = [], []
x1, y2 = [], []

# Read first CSV
with open('four_seconds(5000).csv', 'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for i, row in enumerate(lines):
        if i > 13:
            try:
                x.append(float(row[0]))
                y.append(float(row[1]))
            except ValueError:
                continue

# Read second CSV
with open('outer_inner(5000).csv', 'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for i, row in enumerate(lines):
        if i > 13:
            try:
                x1.append(float(row[0]))
                y2.append(float(row[1]))
            except ValueError:
                continue

# Align lengths
min_len = min(len(y), len(y2))
x = x[:min_len]
x1 = x1[:min_len]
y = y[:min_len]
y2 = y2[:min_len]

# Convert to numpy arrays
y_np = np.array(y)
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

y_denoised = wavelet_denoise(y_np)
y2_denoised = wavelet_denoise(y2_np)

# Compute difference in time domain
y_diff = y_denoised - y2_denoised

# Compute FFTs
Y1 = np.fft.fft(y_denoised)
Y2 = np.fft.fft(y2_denoised)
Y_diff = np.abs(Y1) - np.abs(Y2)

N = min_len
n = np.arange(N)
T = N / sr
freq = n / T

# Padded limit helper
def padded_limits(data, lower=1, upper=99, pad=0.05):
    pmin, pmax = np.percentile(data, [lower, upper])
    prange = pmax - pmin
    return pmin - prange * pad, pmax + prange * pad

# Padded limits
fft_min1, fft_max1 = padded_limits(np.abs(Y1[200:801]))
fft_min2, fft_max2 = padded_limits(np.abs(Y2[200:801]))
fft_diff_min, fft_diff_max = padded_limits(np.abs(Y_diff[200:801]))
ts_diff_min, ts_diff_max = padded_limits(y_diff)

# Plotting
plt.figure(figsize=(16, 12))

# Time Series - four_seconds (denoised)
plt.subplot(3, 2, 1)
plt.plot(x, y_denoised, color='b')
plt.title('Time Series (Denoised) - four_seconds')
plt.xlabel('Time (s)')
plt.ylabel('Voltage')
plt.grid(True)

# Time Series - outer_inner (denoised)
plt.subplot(3, 2, 2)
plt.plot(x1, y2_denoised, color='r')
plt.title('Time Series (Denoised) - outer_inner')
plt.xlabel('Time (s)')
plt.ylabel('Voltage')
plt.grid(True)

# FFT - four_seconds
plt.subplot(3, 2, 3)
plt.plot(freq[:N//2], np.abs(Y1)[:N//2], color='b')
plt.title('FFT - four_seconds (Denoised)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('|FFT|')
plt.grid(True)
plt.xlim(200, 800)
plt.ylim(fft_min1, fft_max1)

peak1_idx = np.argmax(np.abs(Y1[:N//2]))
peak1_freq = freq[peak1_idx]
peak1_val = np.abs(Y1[peak1_idx])
plt.annotate(f'Peak: {peak1_freq:.1f} Hz', xy=(peak1_freq, peak1_val),
             xytext=(peak1_freq + 30, peak1_val),
             arrowprops=dict(facecolor='black', shrink=0.05),
             fontsize=9)

# FFT - outer_inner
plt.subplot(3, 2, 4)
plt.plot(freq[:N//2], np.abs(Y2)[:N//2], color='r')
plt.title('FFT - outer_inner (Denoised)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('|FFT|')
plt.grid(True)
plt.xlim(200, 800)
plt.ylim(fft_min2, fft_max2)

peak2_idx = np.argmax(np.abs(Y2[:N//2]))
peak2_freq = freq[peak2_idx]
peak2_val = np.abs(Y2[peak2_idx])
plt.annotate(f'Peak: {peak2_freq:.1f} Hz', xy=(peak2_freq, peak2_val),
             xytext=(peak2_freq + 30, peak2_val),
             arrowprops=dict(facecolor='black', shrink=0.05),
             fontsize=9)

# Time Series Difference
plt.subplot(3, 2, 5)
plt.plot(x, y_diff, color='purple')
plt.title('Time Series - Difference (Denoised)')
plt.xlabel('Time (s)')
plt.ylabel('Voltage Difference')
plt.grid(True)
plt.ylim(ts_diff_min, ts_diff_max)

# FFT Difference
plt.subplot(3, 2, 6)
plt.plot(freq[:N//2], np.abs(Y_diff[:N//2]), color='purple')
plt.title('FFT - Magnitude Difference (Denoised)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude Difference')
plt.grid(True)
plt.xlim(200, 800)
plt.ylim(fft_diff_min, fft_diff_max)

peak_diff_idx = np.argmax(np.abs(Y_diff[:N//2]))
peak_diff_freq = freq[peak_diff_idx]
peak_diff_val = np.abs(Y_diff[peak_diff_idx])
plt.annotate(f'Peak: {peak_diff_freq:.1f} Hz', xy=(peak_diff_freq, peak_diff_val),
             xytext=(peak_diff_freq + 30, peak_diff_val),
             arrowprops=dict(facecolor='black', shrink=0.05),
             fontsize=9)

plt.tight_layout()
plt.show()
