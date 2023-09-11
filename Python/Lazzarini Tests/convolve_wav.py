import numpy as np
from scipy import signal
import pylab as pl

frequency = 1000  # Hz
duration = 4.0  # seconds
sampling_rate = 41000  # Hz
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
saw_wave = signal.sawtooth(t)
square_wave = signal.square(t)
scal = 32768

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

x1 = saw_wave
x2 = square_wave

if len(x1) > len(x2):
    y = conv(x1, x2 / scal)
    a = np.max(x1)
else:
    y = conv(x2, x1 / scal)
    a = np.max(x2)

s = np.max(y)
out = np.array(y * a / s)


pl.plot(out)
pl.show()