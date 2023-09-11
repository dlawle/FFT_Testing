import pylab as pl
import scipy.io.wavfile as wf
import sys

"""
The following program is a skeleton for a spectral masking application. The function mask(mags,...) 
can be replaced by a different user-defined operation on
the magnitude spectrum, taking the original values and returning a modified array.
The example supplied creates a band-pass filter centred at fc. The command-line
for this program takes two file names (input and output):
$ python3 mask.py input1.wav output.wav
"""
def stft(x, w):
    X = pl.rfft(w * x)
    return X

def istft(X, w):
    xn = pl.irfft(X)
    return xn * w

def p2r(mags, phs):
    return mags * pl.cos(phs) + 1j * mags * pl.sin(phs)

def mask(mags, fc):
    m = pl.zeros(N // 2 + 1)
    d = int((fc / 2) * N / sr)
    b = int(fc * N / sr)
    m[b - d:b + d] = pl.hanning(2 * d)
    mags *= m
    return mags

N = 1024
D = 4
H = N // D
zdbfs = 32768
(sr, signal) = wf.read(sys.argv[1])
signal = signal / zdbfs
L = len(signal)
output = pl.zeros(L)
win = pl.hanning(N)
scal = 1.5 * D / 4

fc = 1000
fe = 5000
incr = (fe - fc) * (H / L)

for n in range(0, L - H, H):  # Removed n argument from the loop
    if (L - n < N):
        break
    frame = stft(signal[n:n + N], win)  # Removed n argument
    mags = abs(frame)
    phs = pl.angle(frame)
    mags = mask(mags, fc)
    fc += incr
    frame = p2r(mags, phs)
    output[n:n + N] += istft(frame, win)  # Removed n argument

output = pl.array(output * zdbfs / scal, dtype='int16')
wf.write(sys.argv[2], sr, output)
