import numpy as np
import matplotlib.pyplot as plt
import csv
import pywt

# Sampling rate
sr = 25000
ts = 1.0 / sr

x, y = [], []
x1, y2 = [], []

# Read first CSV - no inputs active
with open('four_seconds(5000).csv', 'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for i, row in enumerate(lines):
        if i > 13:
            try:
                x.append(float(row[0]))
                y.append(float(row[1]))
            except ValueError:
                continue

# Read other files...


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

