from matplotlib import pyplot as plt
import numpy as np
from scipy.fft import fft, ifft
from scipy.signal.windows import hann
from scipy.io import wavfile

# Parameters
output_filename = "output_overlap_add_sine.wav"
overlap_factor = 4  # Adjust this for different overlap factors

# Generate a 440Hz sine wave
sample_rate = 44100  # Sample rate in Hz
duration = 1.0       # Duration in seconds
frequency = 10.0    # Frequency in Hz

# Generate the time values
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Create a 440Hz sine wave
sine_wave = np.sin(2 * np.pi * frequency * t)

# Apply Hanning window to the sine wave
window = hann(len(sine_wave))
sine_wave *= window

# Perform FFT
fft_result = fft(sine_wave)

# Overlap-Add in the Frequency Domain
hop_size = len(fft_result) // overlap_factor
output_length = len(fft_result) * overlap_factor
output_spectrum = np.zeros(output_length, dtype=complex)

for i in range(0, len(fft_result), hop_size):
    if i + len(fft_result) <= output_length:
        output_spectrum[i:i+len(fft_result)] += fft_result

# Perform Inverse FFT to get the time-domain waveform
output_waveform = ifft(output_spectrum).real

# Generate the new time values for the stretched signal
t_stretched = np.linspace(0, duration, len(output_waveform), endpoint=False)


# Plot the original wave
plt.subplot(2, 1, 1)
plt.plot(t, sine_wave)
plt.title("Original 440Hz Sine Wave with Hanning Window")

# Plot the manipulated IFFT result
plt.subplot(2, 1, 2)
plt.plot(t_stretched, output_waveform)
plt.title("Manipulated Reconstructed Wave (Overlap-Add)")

plt.tight_layout()
plt.show()

# Scale the waveform back to the original amplitude range [−32768, 32767]
scaled_waveform = np.int16(output_waveform * 32767)
scaled_original = np.int16(sine_wave * 32767)

# Save the manipulated waveform as a WAV file
wavfile.write(output_filename, sample_rate, scaled_waveform)
wavfile.write("sine_original.wav", sample_rate, scaled_original)
