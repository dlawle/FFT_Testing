import numpy as np
import sys
from scipy.io import wavfile

"""
The following program outputs the convolution of two input files, using an FFT
overlap-add method. It works with audio files of the RIFF-Wave type, taking three
arguments,
$ python3 conv.py input1.wav input2.wav output.wav
"""

def convert_to_mono(audio):
    if audio.ndim == 2:
        # If the audio is stereo, convert it to mono by averaging the channels
        return np.mean(audio, axis=1)
    else:
        # If the audio is already mono, return it as-is
        return audio

def conv(signal, ir):
    N = len(ir)
    L = len(signal)
    M = 2
    while(M <= 2 * N - 1):
        M *= 2

    h = np.zeros(M)
    x = np.zeros(M)
    y = np.zeros(L + N - 1)

    h[0:N] = ir
    H = np.fft.rfft(h)
    n = N

    for p in range(0, L, N):
        if p + n > L:
            n = L - p
            x[n:] = np.zeros(M - n)
        x[0:n] = signal[p:p + n]
        y[p:p + 2 * n - 1] += np.fft.irfft(H * np.fft.rfft(x))[0:2 * n - 1]
    return y

# Read the input WAV files and convert to mono
sr, x1 = wavfile.read(sys.argv[1])
sr, x2 = wavfile.read(sys.argv[2])
x1 = convert_to_mono(x1)
x2 = convert_to_mono(x2)
scal = 32768

if len(x1) > len(x2):
    y = conv(x1, x2 / scal)
    a = np.max(x1)
else:
    y = conv(x2, x1 / scal)
    a = np.max(x2)

s = np.max(y)
out = np.array(y * a / s, dtype='int16')

# Write the output WAV file
wavfile.write(sys.argv[3], sr, out)
