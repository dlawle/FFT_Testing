import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft, ifftshift
from scipy.signal.windows import *
from scipy.io import wavfile
from scipy.interpolate import interp1d, CubicHermiteSpline

# Parameters
sample_rate = 44100  # Sample rate in Hz
duration = 3.0       # Duration in seconds
frequency = 10.0    # Frequency in Hz

# Generate the time values
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Create a 440Hz sine wave
sine_wave = np.sin(2 * np.pi * frequency * t)

# Apply Hanning window
window = hann(len(sine_wave))
# sine_wave *= window  # Apply the window to the sine wave

# Perform FFT
fft_result = fft(sine_wave)

""" 
    Notes:

    Accessing FFT bins:
    fft_result is an array containing complex values representing the frequency domain.
    To access the magnitude and phase of each bin, you can use the following:
    
        magnitude = np.abs(fft_result)  # Magnitude of each bin
        phase = np.angle(fft_result)   # Phase of each bin

    You can then access individual bins by indexing fft_result like fft_result[index].
    Manipulate the FFT result
    Suggestions for manipulation/effects:
        - Frequency Shifting
        - Magnitude Scaling
        - Phase Manipulation
        - Filtering
        - Noise Addition
        - Time-Stretching/Compression
        - Harmonic Generation

    Example: Scale the magnitude of all bins by a factor of 0.5
    fft_result = fft_result * 0.5
"""

# Stretch factor (1.5 for 1.5x time stretching)
stretch_factor = 3
# Stretch the signal in the frequency domain
# Calculate the new length after stretching
new_length = int(len(fft_result) * stretch_factor)

# Create an interpolating function for the frequency domain
interp_func = interp1d(np.arange(len(fft_result)), fft_result)

# Interpolate to the new length
stretched_fft_result = interp_func(np.linspace(0, len(fft_result) - 1, new_length))

# Perform IFFT on the stretched FFT result

stretched_ifft_result = ifft(stretched_fft_result)

# Generate the new time values for the stretched signal
t_stretched = np.linspace(0, duration * stretch_factor, len(stretched_ifft_result), endpoint=False)



# Plot the original wave
plt.subplot(2, 1, 1)
plt.plot(t, sine_wave)
plt.title("Original 440Hz Sine Wave with Hanning Window")

# Plot the manipulated IFFT result
plt.subplot(2, 1, 2)
plt.plot(t_stretched, stretched_ifft_result.real)
plt.plot(t_stretched, stretched_ifft_result.imag)
plt.title("Stretched Reconstructed Wave (IFFT)")

plt.tight_layout()
plt.show()

# Save the manipulated waveform as a WAV file
output_filename = "output_stretched.wav"
# Scale the waveform back to the original amplitude range [−32768, 32767]
scaled_waveform = np.int16(stretched_ifft_result.real * 32767)
wavfile.write(output_filename, sample_rate, scaled_waveform)