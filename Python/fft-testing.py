import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
from scipy.signal.windows import hann
from scipy.io import wavfile

# Parameters
sample_rate = 44100  # Sample rate in Hz
duration = 1.0       # Duration in seconds
frequency = 10.0    # Frequency in Hz

# Generate the time values
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Create a 440Hz sine wave
sine_wave = np.sin(2 * np.pi * frequency * t)

# Apply Hanning window
window = hann(len(sine_wave))
sine_wave *= window  # Apply the window to the sine wave

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

// Function to perform phase manipulation on the inputBuffer
void phaseManipulation(float* inputBuffer, int bufferSize, float phase_shift) 
{
    for (int i = 0; i < bufferSize; ++i) 
	{
        float realPart = inputBuffer[2 * i];
        float imagPart = inputBuffer[2 * i + 1];
        
        // Calculate the magnitude and phase
        float magnitude = std::sqrt(realPart * realPart + imagPart * imagPart);
        float angle = std::atan2(imagPart, realPart);
        
        // Apply the phase shift
        angle += phase_shift;

        // Update the real and imaginary parts
        inputBuffer[2 * i] = magnitude * std::cos(angle);
        inputBuffer[2 * i + 1] = magnitude * std::sin(angle);
    }
}
"""
def phase_shift(input, shift_amount):
    return input * np.exp(1j * shift_amount)

fft_result = phase_shift(fft_result, 5)

# Perform IFFT
ifft_result = ifft(fft_result)

# Plot the original wave
plt.subplot(2, 1, 1)
plt.plot(t, sine_wave)
plt.title("Original 440Hz Sine Wave with Hanning Window")

# Plot the manipulated IFFT result
plt.subplot(2, 1, 2)
plt.plot(t, ifft_result.real)
plt.plot(t, ifft_result.imag)
plt.title("Manipulated Reconstructed Wave (IFFT)")

plt.tight_layout()
plt.show()

# Save the manipulated waveform as a WAV file
output_filename = "output.wav"
# Scale the waveform back to the original amplitude range [−32768, 32767]
scaled_waveform = np.int16(ifft_result.real * 32767)
wavfile.write(output_filename, sample_rate, scaled_waveform)
