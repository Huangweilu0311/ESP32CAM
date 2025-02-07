#test_filter
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# 濾波器函數
def butter_filter(data, cutoff, fs, btype, order=4):
    nyquist = 0.5 * fs  # 取樣頻率
    
    if isinstance(cutoff, list):
        normal_cutoff = [c / nyquist for c in cutoff]#截止頻率正規化
    else:
        normal_cutoff = cutoff / nyquist

    b, a = butter(order, normal_cutoff, btype)
    y = filtfilt(b, a, data)  
    return y
fs = 1000  
t = np.linspace(0, 1, fs, endpoint=False) 
signal = np.cos(2 * np.pi * 20 * t) + 3 * np.cos(2 * np.pi * 5 * t)

low_cutoff = 10  
high_cutoff = 10  

low_passed = butter_filter(signal, low_cutoff, fs, 'low')  
high_passed = butter_filter(signal, high_cutoff, fs, 'high')  
band_passed = butter_filter(signal, [4, 21], fs, 'band') 
plt.figure(figsize=(12, 8))
plt.subplot(4, 1, 1)
plt.plot(t, signal, label='Original Signal')
plt.title('Original Signal')
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(t, low_passed, label='Low-Passed Signal (<10 Hz)', color='g')
plt.title('Low-Passed Signal')
plt.legend()

plt.subplot(4, 1, 3)
plt.plot(t, high_passed, label='High-Passed Signal (>10 Hz)', color='r')
plt.title('High-Passed Signal')
plt.legend()

plt.subplot(4, 1, 4)
plt.plot(t, band_passed, label='Band-Passed Signal (4-21 Hz)', color='m')
plt.title('Band-Passed Signal')
plt.legend()

plt.tight_layout()
plt.show()
