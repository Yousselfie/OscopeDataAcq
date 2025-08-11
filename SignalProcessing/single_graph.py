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

# Read first CSV
with open('csvs/splg0016.csv', 'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for i, row in enumerate(lines):
        if i >13:
            try:
                x1.append(float(row[0]))
                y1.append(float(row[1]))
            except ValueError:
                continue


# Convert to numpy array
y1_np = np.array(y1)


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


#Offset; row 15185 is where the time is 3034 ms which is when Q3 starts; Q3 is the first output to turnon in this capture
offset = 17715
offset = offset - 13 #minus 13 because we skipped 13 rows at the beginning when reading the csv


x1 = x1[offset:]
y1_denoised = y1_denoised[offset:]

plt.figure(figsize=(12, 8))

# Wavelet Denoised Time Series Plot
ax1 = plt.subplot2grid((2, 2), (0, 0))
ax1.plot(x1, y1_denoised, label='Input 0', color='blue')
plt.axvline(x = 3.54, color = 'r', label = 'Q3')
plt.axvline(x = 6.239, color = 'g', label = 'Q1')
plt.axvline(x = 11.240, color = 'y', label = 'Q2')
plt.axvline(x = 13.007, color = 'orange', label = 'Blink')
ax1.set_title('Time Series')
ax1.legend()


plt.tight_layout()
plt.show()