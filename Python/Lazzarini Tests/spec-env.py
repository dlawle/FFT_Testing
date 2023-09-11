import numpy as np
import matplotlib.pyplot as plt
import pylab as pl

# Parameters
sample_rate = 44100  # Sample rate in Hz
duration = 1.0      # Duration of the sine wave in seconds
frequency = 1.0   # Frequency of the sine wave in Hz

# Generate a sine wave
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
sine_wave = np.sin(2 * np.pi * frequency * t)

# Perform FFT
fft_result = np.fft.fft(sine_wave)
abs_fft_result = abs(fft_result.real)

def spec_env(frame, coefs):
    mags = abs(frame)
    N = len(mags)
    ceps = pl.rfft(pl.log(mags))
    ceps[coefs:] = 0
    mags = pl.exp(pl.irfft(ceps))
    
    return mags

new_wave = spec_env(abs_fft_result, 5)

# Calculate the maximum value in new_wave
max_value = np.max(new_wave)

# Calculate the minimum value in new_wave
min_value = np.min(new_wave)

# Normalize new_wave to be between 0 and 1
normalized_new_wave = (new_wave - min_value) / (max_value - min_value)

plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(t, abs_fft_result)
plt.title('absolute value of peak freq')

plt.subplot(2, 1, 2)
plt.plot(t, normalized_new_wave)
plt.title('normalized_new_wave')

plt.tight_layout()
plt.show()
